#!/bin/sh
set -eu

fixture="tests/normativa/pretextuais-frente-verso.tex"

for engine in pdflatex lualatex; do
  job="pretextuais-duplex-$engine"
  rm -f "$job".aux "$job".log "$job".out "$job".pdf "$job".toc

  echo "Validando início em anverso dos pré-textuais com $engine..."
  for pass in 1 2 3; do
    "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-v2-duplex-pretextual.log 2>&1 || {
      cat /tmp/abntexto-ufc-v2-duplex-pretextual.log
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Duplex V2 falhou: $job contém warning ou overflow não reconhecido."
    exit 1
  fi

  pdftotext -layout "$job.pdf" "/tmp/$job.txt"
  python3 - "$job" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

job = sys.argv[1]
raw = Path(f'/tmp/{job}.txt').read_text(encoding='utf-8')
pages = raw.split('\f')
if pages and not pages[-1].strip():
    pages.pop()

normalized = []
for page in pages:
    page = re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', page)
    page = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', page)).strip().casefold()
    normalized.append(page)

markers = (
    'autor duplex teste',
    'errata',
    'banca examinadora',
    'à família e às pessoas que contribuíram',
    'agradecimentos',
    'uma citação de exemplo usada apenas para validar',
    'resumo',
    'abstract',
    'lista de abreviaturas e siglas',
    'lista de símbolos',
    'sumário',
    'marcador-textual-duplex',
)

for marker in markers:
    matches = [i + 1 for i, page in enumerate(normalized) if marker.casefold() in page]
    if not matches:
        raise SystemExit(f'{job}: marcador ausente: {marker}')
    page = matches[0]
    if page % 2 == 0:
        raise SystemExit(f'{job}: elemento deveria iniciar no anverso, mas apareceu na página física {page}: {marker}')

print(f'{job}: todos os elementos auditados iniciam no anverso.')
PY
done

sh tests/v2-section-primary-recto-duplex-evidence-check.sh

echo 'Gate V2 de pré-textuais duplex concluído.'
