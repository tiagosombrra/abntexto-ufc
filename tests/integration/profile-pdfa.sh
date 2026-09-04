#!/bin/sh
set -eu

profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project scientific-article"
template_dir="template"

for engine in pdflatex lualatex; do
  for profile in $profiles; do
    pdf="$template_dir/perfil-${profile}-${engine}.pdf"
    [ -s "$pdf" ] || {
      echo "PDF/A of the matrix failed: file missing: $pdf"
      exit 1
    }
    echo "Validating PDF/A-2b of $profile/$engine..."
    sh tests/integration/pdfa.sh "$pdf"
  done
done

echo 'Gate PDF/A-2b of the 14 profile PDFs completed.'
