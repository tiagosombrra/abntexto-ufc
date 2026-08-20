#!/bin/sh
set -eu

fixture="tests/normativa/tipografia-codigo.tex"
tmp="ufctex-code-typography.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f "$tmp" tipografia-codigo-*.aux tipografia-codigo-*.log tipografia-codigo-*.out tipografia-codigo-*.pdf
  rm -f tipografia-codigo-*.loa tipografia-codigo-*.loc
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  for family in times arial; do
    sed "s/@UFC_FONT@/$family/g" "$fixture" > "$tmp"
    job="tipografia-codigo-$family-$engine"
    echo "Validando tipografia de código/algoritmo $family com $engine..."

    "$engine" -jobname="$job" $flags "$tmp" > "/tmp/$job.out" 2>&1 || {
      cat "/tmp/$job.out"
      exit 1
    }

    python3 - "$job.log" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')


def marker(name):
    match = re.search(rf'{re.escape(name)}=([^\r\n]+)', text)
    if not match:
        raise SystemExit(f'marcador ausente: {name}')
    return match.group(1).strip()


def scalar(name):
    value = marker(name)
    try:
        return float(value)
    except ValueError as exc:
        raise SystemExit(f'{name}: valor inválido: {value}') from exc


def normalize_family(value):
    return re.sub(r'\([0-9]+\)$', '', value)

text_family = normalize_family(marker('UFC-TEXT-FAMILY'))
code_family = normalize_family(marker('UFC-CODE-FAMILY'))
algorithm_family = normalize_family(marker('UFC-ALGORITHM-FAMILY'))

if code_family != text_family:
    raise SystemExit(f'código mudou de família: texto={text_family}, código={code_family}')
if algorithm_family != text_family:
    raise SystemExit(f'algoritmo mudou de família: texto={text_family}, algoritmo={algorithm_family}')

for name in ('UFC-TEXT-FONTSIZE', 'UFC-CODE-FONTSIZE', 'UFC-ALGORITHM-FONTSIZE'):
    actual = scalar(name)
    if abs(actual - 12.0) > 0.1:
        raise SystemExit(f'{name}: esperado 12 pt nominal, obtido {actual:.4f}')
PY

    sh tests/v2-font-embedding-check.sh "$job.pdf"
  done
done

echo 'Gate V2 de tipografia de código e algoritmos concluído.'
