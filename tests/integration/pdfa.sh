#!/bin/sh
set -eu

pdf="${1:-template/main.pdf}"
report="/tmp/abntexto-ufc-verapdf.xml"
negative_evidence="/tmp/abntexto-ufc-pdfa-negative-validation.json"

[ -f "$pdf" ] || {
  echo "PDF/A validation failed: file not found: $pdf"
  exit 1
}

status=0
if command -v verapdf >/dev/null 2>&1; then
  verapdf -f 2b "$pdf" > "$report" || status=$?
elif command -v docker >/dev/null 2>&1; then
  docker run --rm \
    -v "$PWD:/data:ro" \
    verapdf/cli:v1.30.2 \
    -f 2b "/data/$pdf" > "$report" || status=$?
else
  echo 'PDF/A validation failed: veraPDF or Docker is required for release validation.'
  exit 1
fi

if [ -s "$report" ] && grep -Fq 'isCompliant="true"' "$report"; then
  echo 'PDF/A-2b validation completed.'
  if [ "$pdf" = "template/main.pdf" ] && [ "${UFC_PDFA_NEGATIVE_VALIDATION:-1}" = "1" ]; then
    python3 tests/checks/normative_pdfa.py \
      "$pdf" \
      --positive-report "$report" \
      --json "$negative_evidence"
  fi
  exit 0
fi

[ -s "$report" ] && cat "$report"
echo "PDF/A validation failed: veraPDF rejected the document as PDF/A-2b (exit $status)."
exit 1
