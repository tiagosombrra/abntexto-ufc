#!/bin/sh
set -eu

profiles="tccgraduacao tccespecializacao dissertacao tese projeto projetoanonimizado"

for engine in pdflatex lualatex; do
  for profile in $profiles; do
    pdf="perfil-${profile}-${engine}.pdf"
    [ -s "$pdf" ] || {
      echo "PDF/A da matriz falhou: arquivo ausente: $pdf"
      exit 1
    }
    echo "Validando PDF/A-2b de $profile/$engine..."
    sh tests/v2-pdfa-check.sh "$pdf"
  done
done

echo 'Gate V2 PDF/A-2b dos 12 perfis concluído.'
