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

import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

root = Path(sys.argv[1])
version = "3.0.0"
package_name = f"abntexto-ufc-{version}.zip"
expected = {
    package_name,
    f"abntexto-ufc-template-{version}.zip",
    f"abntexto-ufc-overleaf-{version}.zip",
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
            try:
                name.encode("ascii")
            except UnicodeEncodeError:
                raise SystemExit(f"Distribution integrity failed: non-ASCII path in {archive_path.name}: {name}")
            if any(part.startswith(".") for part in pure.parts):
                raise SystemExit(f"Distribution integrity failed: hidden path in {archive_path.name}: {name}")
            if any(re.search(r"\s", part) for part in pure.parts):
                raise SystemExit(f"Distribution integrity failed: whitespace in path in {archive_path.name}: {name}")
            if pure.name.lower() in forbidden_fonts:
                raise SystemExit(f"Distribution integrity failed: proprietary font in {archive_path.name}: {name}")
            if "assets" in pure.parts and "institutional" in pure.parts:
                raise SystemExit(f"Distribution integrity failed: institutional asset in {archive_path.name}: {name}")
        bad = archive.testzip()
        if bad is not None:
            raise SystemExit(f"Distribution integrity failed: corrupt entry in {archive_path.name}: {bad}")

package_path = root / package_name
with zipfile.ZipFile(package_path) as archive:
    names = archive.namelist()
    files = [name for name in names if not name.endswith("/")]
    if not files or any(not name.startswith("abntexto-ufc/") for name in files):
        raise SystemExit("CTAN package must contain exactly one top-level abntexto-ufc directory.")

    required = {
        "abntexto-ufc/README.md",
        "abntexto-ufc/CHANGELOG",
        "abntexto-ufc/LICENSE",
        "abntexto-ufc/abntexto-ufc.cls",
        "abntexto-ufc/abntexto-ufc.tex",
        "abntexto-ufc/abntexto-ufc.pdf",
        "abntexto-ufc/abntexto-ufc-example.tex",
        "abntexto-ufc/abntexto-ufc-example.pdf",
    }
    missing = required - set(names)
    if missing:
        raise SystemExit("CTAN package is missing required files: " + ", ".join(sorted(missing)))

    forbidden_components = {".github", "tests", "artifacts", "tools", "release", "standards", "dist"}
    for name in files:
        pure = PurePosixPath(name)
        if forbidden_components.intersection(pure.parts):
            raise SystemExit(f"CTAN package leaked development infrastructure: {name}")
        if pure.name == "abntexto.cls":
            raise SystemExit("CTAN package must keep abntexto as an external dependency.")
        lowered = pure.name.casefold()
        if any(marker in lowered for marker in ("brasao", "coat-of-arms", "logo-ufc", "ufc-logo")):
            raise SystemExit(f"CTAN package leaked an institutional mark asset: {name}")

    readme = archive.read("abntexto-ufc/README.md").decode("utf-8")
    readme_fold = readme.casefold()
    required_readme = (
        "Version: 3.0.0",
        "License: LaTeX Project Public License 1.3c or later",
        "No UFC logo",
        "Upstream dependency: https://ctan.org/pkg/abntexto",
    )
    for marker in required_readme:
        if marker.casefold() not in readme_fold:
            raise SystemExit(f"CTAN README is missing publication metadata: {marker}")

    for forbidden in (
        "development candidate",
        "v3.0.0 está em desenvolvimento",
        "v3.0.0 ainda não foi publicada",
        "ufctex",
        "modelo-latex-ufc",
    ):
        if forbidden.casefold() in readme_fold:
            raise SystemExit(f"CTAN README contains stale/deprecated publication text: {forbidden}")

    text_suffixes = {".md", ".tex", ".cls", ".def", ".bib", ".txt"}
    for name in files:
        suffix = PurePosixPath(name).suffix.casefold()
        if suffix in text_suffixes or PurePosixPath(name).name == "CHANGELOG":
            data = archive.read(name)
            if data.startswith(b"\xef\xbb\xbf"):
                raise SystemExit(f"CTAN text file contains UTF-8 BOM: {name}")
            if b"\r" in data:
                raise SystemExit(f"CTAN text file does not use LF-only line endings: {name}")

    example = archive.read("abntexto-ufc/abntexto-ufc-example.tex").decode("utf-8").casefold()
    if "coat-of-arms = false" not in example:
        raise SystemExit("CTAN example must compile without an institutional mark asset.")

    for pdf_name in ("abntexto-ufc/abntexto-ufc.pdf", "abntexto-ufc/abntexto-ufc-example.pdf"):
        if not archive.read(pdf_name).startswith(b"%PDF-"):
            raise SystemExit(f"CTAN documentation output is not a PDF: {pdf_name}")

with zipfile.ZipFile(root / f"abntexto-ufc-template-{version}.zip") as archive:
    if any(PurePosixPath(name).name == "abntexto.cls" for name in archive.namelist()):
        raise SystemExit("Editable template bundle must keep abntexto as an external dependency.")

with zipfile.ZipFile(root / f"abntexto-ufc-overleaf-{version}.zip") as archive:
    if not any(PurePosixPath(name).name == "abntexto.cls" for name in archive.namelist()):
        raise SystemExit("Overleaf bundle must include the pinned abntexto dependency.")

checksums = root / "SHA256SUMS"
if not checksums.is_file() or checksums.stat().st_size == 0:
    raise SystemExit("Distribution integrity failed: SHA256SUMS is missing or empty.")
PY

mkdir -p "$evidence_dir"
cat > "$evidence_dir/distribution-bundles.json" <<EOF
{
  "status": "PASS",
  "version": "3.0.0",
  "artifact_count": 3,
  "ctan_upload_archives": 1,
  "ctan_archive": "abntexto-ufc-3.0.0.zip",
  "checksums": "PASS",
  "archive_integrity": "PASS",
  "ctan_single_top_level_directory": true,
  "ctan_external_abntexto_dependency": true,
  "institutional_marks_redistributed": false,
  "proprietary_fonts_redistributed": false,
  "source_date_epoch": "$epoch",
  "source_sha": "$source_sha"
}
EOF

echo "FINAL-CERTIFICATION-EVIDENCE surface=distribution-bundles status=PASS version=3.0.0 artifacts=3 ctan_upload_archives=1 ctan_archive=abntexto-ufc-3.0.0.zip checksums=PASS archive_integrity=PASS institutional_marks_redistributed=false proprietary_fonts_redistributed=false source_date_epoch=$epoch"
echo 'Distribution/public bundle integrity gate completed.'
