#!/bin/sh
set -eu

fixture="tests/normativa/normativa-complementar.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f normativa-complementar-*.aux normativa-complementar-*.log \
    normativa-complementar-*.out normativa-complementar-*.pdf \
    normativa-complementar-*.toc
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  job="normativa-complementar-$engine"
  echo "Validando estruturas normativas complementares com $engine..."

  for pass in 1 2 3; do
    "$engine" -jobname="$job" $flags "$fixture" > /tmp/abntexto-ufc-v2-normativa-complementar.log 2>&1 || {
      cat /tmp/abntexto-ufc-v2-normativa-complementar.log
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "$job: warning ou overflow não reconhecido."
    exit 1
  fi

  python3 - "$job.log" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')

def value(name, unit=False):
    suffix = r'pt' if unit else ''
    match = re.search(rf'{re.escape(name)}=([0-9.]+){suffix}', text)
    if not match:
        raise SystemExit(f'métrica ausente: {name}')
    return float(match.group(1))

def close(name, actual, expected, tolerance=0.06):
    if abs(actual - expected) > tolerance:
        raise SystemExit(f'{name}: esperado {expected:.4f}, obtido {actual:.4f}')

pt_per_bp = 72.27 / 72.0
pt_per_cm = 72.27 / 2.54
close('recuo da citação longa', value('UFC-LONGQUOTE-HANG', True), 4.0 * pt_per_cm)
close('tamanho da citação longa', value('UFC-LONGQUOTE-FONTSIZE'), 10.0 * pt_per_bp)
close('entrelinha simples da citação longa', value('UFC-LONGQUOTE-BASELINE', True), 11.5 * pt_per_bp)
PY

  if command -v pdftotext >/dev/null 2>&1; then
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
    'citação direta longa de validação normativa',
    'alínea normativa de primeiro nível',
    'subalínea normativa de segundo nível',
    'conteúdo do apêndice complementar',
    'conteúdo do anexo complementar',
    'referência específica do anexo apresentada no próprio anexo',
):
    if marker.casefold() not in fold:
        raise SystemExit(f'estrutura normativa ausente no PDF: {marker}')

if not re.search(r'\ba\)\s+Alínea normativa de primeiro nível', text, re.IGNORECASE):
    raise SystemExit('alínea de primeiro nível não recebeu rótulo alfabético.')
if 'APÊNDICE A'.casefold() not in fold:
    raise SystemExit('identificação do apêndice ausente.')
if 'ANEXO A'.casefold() not in fold:
    raise SystemExit('identificação do anexo ausente.')
if not re.search(r'Equação\s+1', text, re.IGNORECASE):
    raise SystemExit('referência à equação numerada não foi resolvida.')
if '(1)' not in text:
    raise SystemExit('número da equação ausente.')
PY
  fi
done

sh tests/v2-long-quotation-evidence-check.sh

echo 'Gate V2 de estruturas normativas complementares concluído.'
