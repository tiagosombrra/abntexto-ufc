#!/bin/sh
set -eu

profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project"
template_dir="template"

for engine in pdflatex lualatex; do
  for profile in $profiles; do
    pdf="$template_dir/perfil-${profile}-${engine}.pdf"
    [ -s "$pdf" ] || {
      echo "PDF/A da matriz falhou: arquivo ausente: $pdf"
      exit 1
    }
    echo "Validando PDF/A-2b de $profile/$engine..."
    sh tests/integration/pdfa.sh "$pdf"
  done
done

echo 'Gate PDF/A-2b dos 12 perfis concluído.'
