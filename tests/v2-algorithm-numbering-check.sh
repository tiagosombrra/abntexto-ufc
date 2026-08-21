#!/bin/sh
set -eu

fixture="tests/normativa/algoritmos-linhas.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f algoritmo-linhas-*.aux algoritmo-linhas-*.log algoritmo-linhas-*.out algoritmo-linhas-*.pdf algoritmo-linhas-*.loa
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  job="algoritmo-linhas-$engine"
  "$engine" -jobname="$job" $flags "$fixture" >/tmp/ufctex-v2-algorithm-numbering.log 2>&1 || {
    cat /tmp/ufctex-v2-algorithm-numbering.log
    exit 1
  }
  "$engine" -jobname="$job" $flags "$fixture" >/tmp/ufctex-v2-algorithm-numbering.log 2>&1 || {
    cat /tmp/ufctex-v2-algorithm-numbering.log
    exit 1
  }

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "$job: warning ou overflow não reconhecido."
    exit 1
  fi

  pdftotext -layout "$job.pdf" "/tmp/$job.txt"
  python3 - "/tmp/$job.txt" <<'PY'
import re
import sys
from pathlib import Path

lines = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace').splitlines()


def line_for(marker):
    for line in lines:
        if marker in line:
            return line
    raise SystemExit(f'marcador ausente: {marker}')


for marker in ('NUMERADO-A', 'NUMERADO-B'):
    line = line_for(marker)
    if not re.search(r'\b[12]:\s+', line):
        raise SystemExit(f'linha numerada sem prefixo esperado: {line!r}')

for marker in ('SEM-NUMERO-A', 'SEM-NUMERO-B'):
    line = line_for(marker)
    if re.search(r'\b\d+:\s+', line):
        raise SystemExit(f'linha deveria estar sem numeração: {line!r}')
PY

done

echo 'Gate V2 de numeração de algoritmos concluído.'
