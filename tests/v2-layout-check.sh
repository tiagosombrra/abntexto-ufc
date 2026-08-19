#!/bin/sh
set -eu

fixtures="tests/normativa/layout-anverso.tex tests/normativa/layout-frente-verso.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

for engine in pdflatex lualatex; do
  for fixture in $fixtures; do
    base=$(basename "$fixture" .tex)
    echo "Validando $fixture com $engine..."
    for pass in 1 2; do
      "$engine" $flags "$fixture" > /tmp/ufctex-v2-layout.log 2>&1 || {
        cat /tmp/ufctex-v2-layout.log
        exit 1
      }
    done

    warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$base.log" | \
      grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
    if [ -n "$warnings" ]; then
      printf '%s\n' "$warnings"
      echo "Layout V2 falhou: $base/$engine contém warning ou overflow não reconhecido."
      exit 1
    fi
  done
done

echo 'Gate V2 de layout concluído.'
