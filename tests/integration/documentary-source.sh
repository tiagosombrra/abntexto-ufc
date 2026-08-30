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
  echo "Validando fontes documentais com $engine..."

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
    echo "$job: Biber reportou warning/error."
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
        raise SystemExit(f'marcador documental ausente: {marker}')

source_match = re.search(r'adaptado de.{0,120}silva.{0,120}2026', fold)
if not source_match:
    raise SystemExit('fonte externa não foi apresentada em forma de citação autor-data.')

annex_pos = fold.find('anexo a')
fullref_pos = fold.find('manual de dados de teste')
if annex_pos < 0 or fullref_pos < annex_pos:
    raise SystemExit('referência bibliográfica própria não permaneceu dentro do anexo.')

if 'referências' in fold[annex_pos:]:
    raise SystemExit('fixture criou lista global de referências; o caso deve permanecer local ao anexo.')
PY

done

echo 'Gate V2 de fontes documentais concluído.'
