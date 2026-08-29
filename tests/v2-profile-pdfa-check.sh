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

# The scientific-article gate runs inside the TeX Live container, where
# veraPDF/Docker is intentionally unavailable. Its PDFs are preserved so this
# host-side gate can certify them with the same release validator.
article_pdfs="artigo-canonical-pdflatex.pdf artigo-canonical-lualatex.pdf artigo-legacy-pdflatex.pdf"
for pdf in $article_pdfs; do
  [ -s "$pdf" ] || {
    echo "PDF/A do artigo falhou: arquivo ausente: $pdf"
    exit 1
  }
  echo "Validando PDF/A-2b do artigo: $pdf..."
  sh tests/v2-pdfa-check.sh "$pdf"
done

echo 'N15-EVIDENCE article-pdfa canonical-pdflatex=true canonical-lualatex=true legacy-pdflatex=true status=PASS'
echo 'Gate V2 PDF/A-2b dos 12 perfis e do artigo científico concluído.'
