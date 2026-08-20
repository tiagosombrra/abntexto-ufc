#!/bin/sh
set -eu

fixture="tests/normativa/objeto-geometria.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f objeto-geometria-*.aux objeto-geometria-*.log objeto-geometria-*.out objeto-geometria-*.pdf
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  job="objeto-geometria-$engine"
  echo "Validando geometria de objetos com $engine..."

  for pass in 1 2; do
    "$engine" -jobname="$job" $flags "$fixture" > /tmp/ufctex-v2-object-geometry.log 2>&1 || {
      cat /tmp/ufctex-v2-object-geometry.log
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
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

def dim(name):
    match = re.search(rf'{re.escape(name)}=([0-9.]+)pt', text)
    if not match:
        raise SystemExit(f'métrica ausente: {name}')
    return float(match.group(1))

def scalar(name):
    match = re.search(rf'{re.escape(name)}=([0-9.]+)', text)
    if not match:
        raise SystemExit(f'métrica ausente: {name}')
    return float(match.group(1))

def close(name, actual, expected, tolerance=0.06):
    if abs(actual - expected) > tolerance:
        raise SystemExit(f'{name}: esperado {expected:.4f}, obtido {actual:.4f}')

pt_per_cm = 72.27 / 2.54
pt_per_bp = 72.27 / 72.0
expected_width = 6.0 * pt_per_cm
close('largura física do objeto', dim('UFC-OBJECT-CONTENT-WIDTH'), expected_width)
close('largura máxima do título', dim('UFC-OBJECT-TITLE-WIDTH'), expected_width)
close('tamanho tipográfico do título', scalar('UFC-OBJECT-TITLE-FONTSIZE'), 10.0 * pt_per_bp)
PY

done

echo 'Gate V2 de geometria de objetos concluído.'
