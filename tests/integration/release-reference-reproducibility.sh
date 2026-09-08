#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
cd "$ROOT"

EVIDENCE="${UFC_REPRO_EVIDENCE:-artifacts/validation/release-reference-reproducibility.json}"
OUTPUT_PDF="${UFC_REPRO_PDF:-artifacts/validation/release-reference-pdf.pdf}"
KEEP_PDFS="${UFC_REPRO_KEEP_PDFS:-0}"

case "$OUTPUT_PDF" in
  /*)
    echo 'Release reference reproducibility failed: UFC_REPRO_PDF must be repository-relative for container validation.'
    exit 1
    ;;
esac

SOURCE_SHA=$(git -c "safe.directory=$ROOT" rev-parse HEAD)
if [ -n "${SOURCE_DATE_EPOCH:-}" ]; then
  EPOCH="$SOURCE_DATE_EPOCH"
  EPOCH_SOURCE="environment"
else
  EPOCH=$(git -c "safe.directory=$ROOT" show -s --format=%ct "$SOURCE_SHA")
  EPOCH_SOURCE="git-commit-time"
fi

case "$EPOCH" in
  ''|*[!0-9]*)
    echo "Release reference reproducibility failed: SOURCE_DATE_EPOCH is not a non-negative integer: $EPOCH"
    exit 1
    ;;
esac

export SOURCE_DATE_EPOCH="$EPOCH"
export FORCE_SOURCE_DATE=1
export TZ=UTC

WORK=$(mktemp -d "${TMPDIR:-/tmp}/abntexto-ufc-reference-repro.XXXXXX")
cleanup() {
  rm -rf "$WORK"
}
trap cleanup EXIT INT TERM

mkdir -p "$(dirname "$EVIDENCE")" "$(dirname "$OUTPUT_PDF")"
ARCHIVE="$WORK/source.tar"
git -c "safe.directory=$ROOT" archive --format=tar "$SOURCE_SHA" > "$ARCHIVE"

build_one() {
  number="$1"
  build="$WORK/build-$number"
  log="$WORK/build-$number.log"
  mkdir -p "$build"
  tar -xf "$ARCHIVE" -C "$build"
  (
    cd "$build"
    make clean
    make compile
  ) > "$log" 2>&1 || {
    cat "$log"
    echo "Release reference reproducibility failed: clean build $number did not compile."
    exit 1
  }
  pdf="$build/template/main.pdf"
  [ -s "$pdf" ] || {
    cat "$log"
    echo "Release reference reproducibility failed: clean build $number did not produce template/main.pdf."
    exit 1
  }
}

build_one 1
build_one 2

PDF1="$WORK/build-1/template/main.pdf"
PDF2="$WORK/build-2/template/main.pdf"
HASH1=$(sha256sum "$PDF1" | awk '{print $1}')
HASH2=$(sha256sum "$PDF2" | awk '{print $1}')
BYTES1=$(wc -c < "$PDF1" | tr -d ' ')
BYTES2=$(wc -c < "$PDF2" | tr -d ' ')

if [ "$HASH1" != "$HASH2" ]; then
  FAIL_DIR=$(dirname "$EVIDENCE")
  cp "$PDF1" "$FAIL_DIR/release-reference-pdf-build1-failed.pdf"
  cp "$PDF2" "$FAIL_DIR/release-reference-pdf-build2-failed.pdf"
  cp "$WORK/build-1.log" "$FAIL_DIR/release-reference-build1-failed.log"
  cp "$WORK/build-2.log" "$FAIL_DIR/release-reference-build2-failed.log"
  python3 - "$EVIDENCE" "$SOURCE_SHA" "$EPOCH" "$EPOCH_SOURCE" "$HASH1" "$HASH2" "$BYTES1" "$BYTES2" <<'PY'
import json
import sys
from pathlib import Path

path, source_sha, epoch, epoch_source, hash1, hash2, bytes1, bytes2 = sys.argv[1:]
payload = {
    "status": "FAIL",
    "source_sha": source_sha,
    "source_date_epoch": int(epoch),
    "epoch_source": epoch_source,
    "builds": [
        {"id": 1, "sha256": hash1, "bytes": int(bytes1)},
        {"id": 2, "sha256": hash2, "bytes": int(bytes2)},
    ],
    "identical_sha256": False,
    "independent_clean_builds": 2,
    "post_build_normalization": False,
}
Path(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY
  echo "REPRODUCIBILITY-EVIDENCE status=FAIL source_sha=$SOURCE_SHA epoch=$EPOCH build1_sha256=$HASH1 build2_sha256=$HASH2 identical=false"
  echo 'Release reference reproducibility failed: independently built PDFs are not byte-identical.'
  exit 1
fi

cp "$PDF1" "$OUTPUT_PDF"
if [ "$KEEP_PDFS" = "1" ]; then
  out_dir=$(dirname "$OUTPUT_PDF")
  cp "$PDF1" "$out_dir/release-reference-pdf-build1.pdf"
  cp "$PDF2" "$out_dir/release-reference-pdf-build2.pdf"
  cp "$WORK/build-1.log" "$out_dir/release-reference-build1.log"
  cp "$WORK/build-2.log" "$out_dir/release-reference-build2.log"
fi

sh tests/integration/font-embedding.sh "$OUTPUT_PDF"
sh tests/integration/pdf-validator.sh "$OUTPUT_PDF"
UFC_PDFA_NEGATIVE_VALIDATION=0 sh tests/integration/pdfa.sh "$OUTPUT_PDF"

TEXT="$WORK/release-reference.txt"
pdftotext "$OUTPUT_PDF" "$TEXT"
python3 - "$TEXT" <<'PY'
import unicodedata
import sys
from pathlib import Path

text = unicodedata.normalize("NFC", Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace"))
for marker in (
    "Universidade Federal do Ceará",
    "RESUMO",
    "INTRODUÇÃO",
    "REFERÊNCIAS",
    "ÍNDICE",
):
    if marker not in text:
        raise SystemExit(f"Release reference reproducibility failed: Unicode extraction marker is missing: {marker}")
PY

python3 - "$EVIDENCE" "$SOURCE_SHA" "$EPOCH" "$EPOCH_SOURCE" "$HASH1" "$BYTES1" "$OUTPUT_PDF" <<'PY'
import json
import sys
from pathlib import Path

path, source_sha, epoch, epoch_source, digest, byte_count, output_pdf = sys.argv[1:]
payload = {
    "status": "PASS",
    "source_sha": source_sha,
    "source_date_epoch": int(epoch),
    "epoch_source": epoch_source,
    "canonical_source": "template/main.tex",
    "canonical_output": output_pdf,
    "builds": [
        {"id": 1, "sha256": digest, "bytes": int(byte_count), "clean_source_tree": True},
        {"id": 2, "sha256": digest, "bytes": int(byte_count), "clean_source_tree": True},
    ],
    "independent_clean_builds": 2,
    "identical_sha256": True,
    "post_build_normalization": False,
    "validation": {
        "font_embedding": "PASS",
        "portable_pdf_validator": "PASS",
        "pdfa_2b": "PASS",
        "unicode_extraction": "PASS",
    },
}
Path(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY

echo "REPRODUCIBILITY-EVIDENCE status=PASS source_sha=$SOURCE_SHA epoch=$EPOCH epoch_source=$EPOCH_SOURCE builds=2 sha256=$HASH1 bytes=$BYTES1 font_embedding=PASS pdf_validator=PASS pdfa_2b=PASS unicode=PASS"
echo 'Release reference reproducibility gate completed.'
