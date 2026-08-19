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

sh tests/v2-font-embedding-check.sh documento.pdf

if command -v pdfinfo >/dev/null 2>&1; then
  pdfinfo -meta documento.pdf > /tmp/ufctex-v2-pdfa-meta.xml
  grep -Eq '<pdfaid:part>2</pdfaid:part>' /tmp/ufctex-v2-pdfa-meta.xml || {
    echo 'Documento V2 falhou: declaração PDF/A parte 2 ausente.'
    exit 1
  }
  grep -Eq '<pdfaid:conformance>[Bb]</pdfaid:conformance>' /tmp/ufctex-v2-pdfa-meta.xml || {
    echo 'Documento V2 falhou: declaração PDF/A-2b ausente.'
    exit 1
  }
fi

python3 <<'PY'
import re
from pathlib import Path

cases = (
    ('1-pre-textuais/resumo.tex', r'\\palavraschave', 'Resumo'),
    ('1-pre-textuais/abstract.tex', r'\\keywords', 'Abstract'),
)

for path, marker, label in cases:
    source = Path(path).read_text(encoding='utf-8')
    body = re.split(marker, source, maxsplit=1)[0]
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*", body)
    if not 150 <= len(words) <= 500:
        raise SystemExit(f'{label} de referência fora da faixa UFC de 150–500 palavras: {len(words)}')
PY

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
