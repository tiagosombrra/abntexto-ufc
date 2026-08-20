#!/bin/sh
set -eu

root="${1:-windows-font-pdfs}"

[ -d "$root" ] || {
  echo "Fontes Windows PDF/A: diretório ausente: $root"
  exit 1
}

for engine in pdflatex lualatex; do
  for family in times arial; do
    pdf="$root/ufctex-${family}-${engine}-strict-poc.pdf"
    [ -s "$pdf" ] || {
      echo "Fontes Windows PDF/A: arquivo ausente: $pdf"
      exit 1
    }

    echo "Fontes Windows PDF/A: validando $family/$engine..."
    sh tests/v2-font-embedding-check.sh "$pdf"
    sh tests/v2-pdfa-check.sh "$pdf"
  done
done

echo 'Gate PDF/A-2b das fontes Microsoft literais concluído.'
