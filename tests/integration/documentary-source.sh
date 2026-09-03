#!/bin/sh
set -eu

fixture="tests/documents/documentary-sources.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f fontes-documentais-*.aux fontes-documentais-*.bbl fontes-documentais-*.bcf \
    fontes-documentais-*.blg fontes-documentais-*.log fontes-documentais-*.out \
    fontes-documentais-*.pdf fontes-documentais-*.run.xml
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  job="fontes-documentais-$engine"
  echo "Validating documentary sources with $engine..."

  "$engine" -jobname="$job" $flags "$fixture" > "/tmp/$job.out" 2>&1 || {
    cat "/tmp/$job.out"
    exit 1
  }
  biber "$job" > "/tmp/$job-biber.out" 2>&1 || {
    cat "/tmp/$job-biber.out"
    exit 1
  }
  "$engine" -jobname="$job" $flags "$fixture" > "/tmp/$job.out" 2>&1 || {
    cat "/tmp/$job.out"
    exit 1
  }
  "$engine" -jobname="$job" $flags "$fixture" > "/tmp/$job.out" 2>&1 || {
    cat "/tmp/$job.out"
    exit 1
  }

  if grep -Eq 'WARN|ERROR' "$job.blg"; then
    cat "$job.blg"
    echo "$job: Biber reported a warning/error."
    exit 1
  fi

  pdftotext -layout "$job.pdf" "/tmp/$job.txt"
  python3 - "/tmp/$job.txt" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

raw = Path(sys.argv[1]).read_text(encoding='utf-8')
text = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', raw)).strip()
fold = text.casefold()

for marker in (
    'adaptado de',
    'silva',
    '2026',
    'anexo a',
    'documento com referência própria',
    'manual de dados de teste',
    'editora acadêmica',
):
    if marker.casefold() not in fold:
        raise SystemExit(f'marker documental missing: {marker}')

source_match = re.search(r'adaptado de.{0,120}silva.{0,120}2026', fold)
if not source_match:
    raise SystemExit('external source was not presented in form of citation author-date.')

annex_pos = fold.find('anexo a')
fullref_pos = fold.find('manual de dados de teste')
if annex_pos < 0 or fullref_pos < annex_pos:
    raise SystemExit('The annex-specific bibliographic reference did not remain inside the annex.')

if 'referências' in fold[annex_pos:]:
    raise SystemExit('fixture criou list global of references; o caso deve permanecer local ao annex.')
PY

  echo 'VALIDATION-EVIDENCE rule=illustration.source.external-citation status=PASS expected=author-date-citation measured=adapted-source-citation-present'

done

echo 'Documentary sources gate completed.'
