#!/bin/sh
set -eu

fixture="tests/documents/algorithm-line-numbering.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f algoritmo-linhas-*.aux algoritmo-linhas-*.log algoritmo-linhas-*.out algoritmo-linhas-*.pdf algoritmo-linhas-*.loa
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  job="algoritmo-linhas-$engine"
  "$engine" -jobname="$job" $flags "$fixture" >/tmp/abntexto-ufc-algorithm-numbering.log 2>&1 || {
    cat /tmp/abntexto-ufc-algorithm-numbering.log
    exit 1
  }
  "$engine" -jobname="$job" $flags "$fixture" >/tmp/abntexto-ufc-algorithm-numbering.log 2>&1 || {
    cat /tmp/abntexto-ufc-algorithm-numbering.log
    exit 1
  }

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
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


expected_markers = {
    1: 'NUMERADO-1',
    2: 'NUMERADO-2',
    3: 'NUMERADO-3',
    4: 'NUMERADO-4',
    6: 'NUMERADO-6',
    8: 'NUMERADO-8',
}
for number, marker in expected_markers.items():
    line = line_for(marker)
    if not re.search(rf'(^|\s){number}:\s+\S', line):
        raise SystemExit(f'linha {number} sem prefixo/conteúdo esperado: {line!r}')

numbered = {}
for line in lines:
    match = re.search(r'(^|\s)([1-8]):\s+(\S.*)$', line)
    if match:
        number = int(match.group(2))
        if number in numbered:
            raise SystemExit(f'número de linha duplicado {number}: {line!r}')
        numbered[number] = match.group(3).strip()

if sorted(numbered) != list(range(1, 9)):
    raise SystemExit(f'sequência numerada incompleta: {sorted(numbered)}')
for number, content in numbered.items():
    if not content:
        raise SystemExit(f'linha numerada vazia: {number}')

if 'end if' not in numbered[5].lower():
    raise SystemExit(f'linha 5 deveria tornar EndIf visível: {numbered[5]!r}')
if 'end while' not in numbered[7].lower():
    raise SystemExit(f'linha 7 deveria tornar EndWhile visível: {numbered[7]!r}')

for marker in ('SEM-NUMERO-A', 'SEM-NUMERO-B'):
    line = line_for(marker)
    if re.search(r'(^|\s)\d+:\s+', line):
        raise SystemExit(f'linha deveria estar sem numeração: {line!r}')
PY

done

echo 'Gate de numeração de algoritmos concluído.'
