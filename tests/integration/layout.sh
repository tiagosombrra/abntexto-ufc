#!/bin/sh
set -eu

fixtures="tests/documents/layout-single-sided.tex tests/documents/layout-double-sided.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"
tmp_log="/tmp/abntexto-ufc-layout.log"

cleanup() {
  rm -f \
    layout-single-sided.aux layout-single-sided.log layout-single-sided.out layout-single-sided.pdf layout-single-sided.toc \
    layout-double-sided.aux layout-double-sided.log layout-double-sided.out layout-double-sided.pdf layout-double-sided.toc
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  for fixture in $fixtures; do
    base=$(basename "$fixture" .tex)
    echo "Validating $fixture with $engine..."
    for pass in 1 2; do
      "$engine" $flags "$fixture" > "$tmp_log" 2>&1 || {
        cat "$tmp_log"
        exit 1
      }
    done

    warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$base.log" | \
      grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
    if [ -n "$warnings" ]; then
      printf '%s\n' "$warnings"
      echo "Layout validation failed: $base/$engine contains an unrecognized warning or overflow."
      exit 1
    fi
  done
done

python3 - layout-single-sided.log <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')


def dim(name):
    match = re.search(rf'{re.escape(name)}=([0-9.]+)pt', text)
    if not match:
        raise SystemExit(f'Layout validation: missing metric: {name}')
    return float(match.group(1))


def scalar(name):
    match = re.search(rf'{re.escape(name)}=([0-9.]+)', text)
    if not match:
        raise SystemExit(f'Layout validation: missing metric: {name}')
    return float(match.group(1))


def close(name, actual, expected, tolerance=0.06):
    if abs(actual - expected) > tolerance:
        raise SystemExit(
            f'Layout validation: {name}: expected {expected:.4f}, observed {actual:.4f}'
        )


pt_per_cm = 72.27 / 2.54
pt_per_bp = 72.27 / 72.0
close('first-line indent', dim('UFC-PARINDENT'), 2.0 * pt_per_cm)
close('footnote hanging indent', dim('UFC-FOOTNOTE-HANG'), 2.0 * pt_per_cm)
close('footnote font size', scalar('UFC-FOOTNOTE-FONTSIZE'), 10.0 * pt_per_bp)
close('footnote single spacing', dim('UFC-FOOTNOTE-BASELINE'), 11.5 * pt_per_bp)

match = re.search(r'UFC-FOOTNOTE-HANGAFTER=(-?[0-9]+)', text)
if not match or int(match.group(1)) != 1:
    raise SystemExit('Layout validation: footnote hangafter must be 1.')
PY

sh tests/integration/section-hierarchy-evidence.sh
sh tests/integration/section-indicator-evidence.sh
sh tests/integration/section-primary-after-spacing-evidence.sh
sh tests/integration/subsection-spacing-evidence.sh
sh tests/integration/section-multiline-hanging-evidence.sh
sh tests/integration/section-unnumbered-centered-evidence.sh
sh tests/integration/body-paragraph-evidence.sh
sh tests/integration/footnote-text-evidence.sh
sh tests/integration/footnote-separator-evidence.sh
sh tests/integration/typography-evidence.sh

echo 'Layout gate completed.'
