#!/bin/sh
set -eu

fixtures="tests/normativa/layout-anverso.tex tests/normativa/layout-frente-verso.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

for engine in pdflatex lualatex; do
  for fixture in $fixtures; do
    base=$(basename "$fixture" .tex)
    echo "Validando $fixture com $engine..."
    for pass in 1 2; do
      "$engine" $flags "$fixture" > /tmp/abntexto-ufc-v2-layout.log 2>&1 || {
        cat /tmp/abntexto-ufc-v2-layout.log
        exit 1
      }
    done

    warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$base.log" | \
      grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
    if [ -n "$warnings" ]; then
      printf '%s\n' "$warnings"
      echo "Layout V2 falhou: $base/$engine contém warning ou overflow não reconhecido."
      exit 1
    fi
  done
done

python3 - layout-anverso.log <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')

def dim(name):
    match = re.search(rf'{re.escape(name)}=([0-9.]+)pt', text)
    if not match:
        raise SystemExit(f'Layout V2: métrica ausente: {name}')
    return float(match.group(1))

def scalar(name):
    match = re.search(rf'{re.escape(name)}=([0-9.]+)', text)
    if not match:
        raise SystemExit(f'Layout V2: métrica ausente: {name}')
    return float(match.group(1))

def close(name, actual, expected, tolerance=0.06):
    if abs(actual - expected) > tolerance:
        raise SystemExit(f'Layout V2: {name}: esperado {expected:.4f}, obtido {actual:.4f}')

pt_per_cm = 72.27 / 2.54
pt_per_bp = 72.27 / 72.0
close('recuo de primeira linha', dim('UFC-PARINDENT'), 2.0 * pt_per_cm)
close('recuo suspenso da nota', dim('UFC-FOOTNOTE-HANG'), 2.0 * pt_per_cm)
close('tamanho da nota', scalar('UFC-FOOTNOTE-FONTSIZE'), 10.0 * pt_per_bp)
close('entrelinha simples da nota', dim('UFC-FOOTNOTE-BASELINE'), 11.5 * pt_per_bp)

match = re.search(r'UFC-FOOTNOTE-HANGAFTER=(-?[0-9]+)', text)
if not match or int(match.group(1)) != 1:
    raise SystemExit('Layout V2: hangafter da nota deve ser 1.')
PY

sh tests/v2-section-hierarchy-evidence-check.sh
sh tests/v2-section-indicator-evidence-check.sh
sh tests/v2-section-primary-after-spacing-evidence-check.sh
sh tests/v2-subsection-spacing-evidence-check.sh
sh tests/v2-section-multiline-hanging-evidence-check.sh
sh tests/v2-section-unnumbered-centered-evidence-check.sh

echo 'Gate V2 de layout concluído.'
