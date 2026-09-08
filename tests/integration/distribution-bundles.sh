#!/bin/sh
set -eu

work="$(mktemp -d)"
evidence_dir="artifacts/final-certification"
campus="template/figures/ufc-campus-pici.jpg"
reitoria="template/figures/ufc-reitoria.jpg"
campus_preexisting=false
reitoria_preexisting=false
source_sha="${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-local}}"
[ -f "$campus" ] && campus_preexisting=true
[ -f "$reitoria" ] && reitoria_preexisting=true

cleanup() {
  rm -rf "$work"
  [ "$campus_preexisting" = true ] || rm -f "$campus"
  [ "$reitoria_preexisting" = true ] || rm -f "$reitoria"
}
trap cleanup EXIT INT TERM

python3 tools/fetch-reference-images.py
python3 tools/fetch-abntexto.py --output "$work/abntexto.cls"

if [ -n "${SOURCE_DATE_EPOCH:-}" ]; then
  epoch="$SOURCE_DATE_EPOCH"
elif [ "$source_sha" != "local" ]; then
  epoch="$(git -c safe.directory="$PWD" show -s --format=%ct "$source_sha")"
else
  epoch="$(git -c safe.directory="$PWD" log -1 --format=%ct)"
fi

SOURCE_DATE_EPOCH="$epoch" python3 tools/build-distribution-bundles.py \
  --output "$work/dist" \
  --abntexto "$work/abntexto.cls"

(
  cd "$work/dist"
  sha256sum -c SHA256SUMS
)

python3 - "$work/dist" <<'PY'
from __future__ import annotations

import sys
import zipfile
from pathlib import Path, PurePosixPath

root = Path(sys.argv[1])
expected = {
    "abntexto-ufc-3.0.0.zip",
    "abntexto-ufc-ctan-3.0.0.zip",
    "abntexto-ufc-template-3.0.0.zip",
    "abntexto-ufc-overleaf-3.0.0.zip",
}
actual = {path.name for path in root.glob("*.zip")}
if actual != expected:
    raise SystemExit(f"Distribution integrity failed: unexpected archive set: {sorted(actual ^ expected)}")

forbidden_fonts = {
    "times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf",
    "arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf",
}

for archive_path in sorted(root.glob("*.zip")):
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if not names:
            raise SystemExit(f"Distribution integrity failed: empty archive: {archive_path.name}")
        for name in names:
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts:
                raise SystemExit(f"Distribution integrity failed: unsafe path in {archive_path.name}: {name}")
            if pure.name.lower() in forbidden_fonts:
                raise SystemExit(f"Distribution integrity failed: proprietary font in {archive_path.name}: {name}")
            if "assets" in pure.parts and "institutional" in pure.parts:
                raise SystemExit(f"Distribution integrity failed: institutional asset in {archive_path.name}: {name}")
        bad = archive.testzip()
        if bad is not None:
            raise SystemExit(f"Distribution integrity failed: corrupt entry in {archive_path.name}: {bad}")

checksums = root / "SHA256SUMS"
if not checksums.is_file() or checksums.stat().st_size == 0:
    raise SystemExit("Distribution integrity failed: SHA256SUMS is missing or empty.")
PY

mkdir -p "$evidence_dir"
cat > "$evidence_dir/distribution-bundles.json" <<EOF
{
  "status": "PASS",
  "version": "3.0.0",
  "artifact_count": 4,
  "checksums": "PASS",
  "archive_integrity": "PASS",
  "proprietary_fonts_redistributed": false,
  "source_date_epoch": "$epoch",
  "source_sha": "$source_sha"
}
EOF

echo "FINAL-CERTIFICATION-EVIDENCE surface=distribution-bundles status=PASS version=3.0.0 artifacts=4 checksums=PASS archive_integrity=PASS source_date_epoch=$epoch proprietary_fonts_redistributed=false"
echo 'Distribution/public bundle integrity gate completed.'
