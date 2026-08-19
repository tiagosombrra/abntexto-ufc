#!/bin/sh
set -eu

make clean
make compile

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Underfull \\hbox|Overfull \\vbox' documento.log || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Documento V2 falhou: revise os avisos acima.'
  exit 1
fi

if command -v pdffonts >/dev/null 2>&1; then
  if ! pdffonts documento.pdf | tail -n +3 | awk 'NF && $6 != "yes" {bad=1} END{exit bad}'; then
    echo 'Documento V2 falhou: há fonte não incorporada.'
    exit 1
  fi
fi

if command -v pdftotext >/dev/null 2>&1; then
  pdftotext documento.pdf /tmp/ufctex-v2-reference.txt
  for marker in 'RESUMO' 'ABSTRACT' 'LISTA DE ILUSTRAÇÕES' 'SUMÁRIO' 'INTRODUÇÃO' 'REFERÊNCIAS' 'GLOSSÁRIO' 'ÍNDICE'; do
    grep -Fq "$marker" /tmp/ufctex-v2-reference.txt || {
      echo "Documento V2 falhou: marcador ausente: $marker"
      exit 1
    }
  done
fi

grep -Eiq 'Introdu' documento.toc || {
  echo 'Documento V2 falhou: seção textual ausente do Sumário.'
  exit 1
}

if grep -Eiq 'resumo|abstract|lista de ilustra' documento.toc; then
  echo 'Documento V2 falhou: elemento pré-textual entrou no Sumário.'
  exit 1
fi

echo 'Documento V2 de referência validado.'
