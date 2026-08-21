#!/bin/sh
set -eu

[ -s documento.pdf ] || {
  echo 'Corpus V2 falhou: documento.pdf ausente.'
  exit 1
}

for file in documento.loi documento.lot documento.loc documento.loa documento.toc; do
  [ -s "$file" ] || {
    echo "Corpus V2 falhou: arquivo de navegação ausente: $file"
    exit 1
  }
done

pdftotext -layout documento.pdf /tmp/ufctex-v2-reference-corpus.txt

python3 <<'PY'
from pathlib import Path

text = Path('/tmp/ufctex-v2-reference-corpus.txt').read_text(encoding='utf-8', errors='replace')
required = (
    'CATÁLOGO DE EXEMPLOS E VALIDAÇÃO VISUAL',
    'Figura estreita com legenda curta',
    'Figura de largura intermediária',
    'Figura larga próxima à largura útil',
    'Distribuição sintética de três categorias',
    'Comparação de configurações editoriais',
    'Indicadores sintéticos com linhas alternadas',
    'Função de média em Python com números de linha',
    'Função de máximo em C++ sem números de linha',
    'Arquivo Python externo com números de linha',
    'Método Java com numeração a cada duas linhas',
    'Máximo divisor comum com números de linha',
    'Seleção do maior valor sem números de linha',
    'APÊNDICE A',
    'APÊNDICE B',
    'APÊNDICE C',
    'APÊNDICE D',
    'ANEXO A',
    'ANEXO B',
)
missing = [marker for marker in required if marker not in text]
if missing:
    raise SystemExit('Corpus V2 falhou: marcadores ausentes no PDF: ' + ', '.join(missing))
if '??' in text:
    raise SystemExit('Corpus V2 falhou: referência não resolvida encontrada no PDF.')
PY

check_list() {
  file="$1"
  shift
  for marker in "$@"; do
    grep -Fq "$marker" "$file" || {
      echo "Corpus V2 falhou: '$marker' ausente de $file"
      exit 1
    }
  done
}

check_list documento.loi \
  'Figura estreita com legenda curta' \
  'Figura de largura intermediária' \
  'Figura larga próxima à largura útil' \
  'Distribuição sintética de três categorias' \
  'Comparação de configurações editoriais'

check_list documento.lot \
  'Etapas do procedimento' \
  'Indicadores sintéticos com linhas alternadas'

check_list documento.loc \
  'Função de soma em C++' \
  'Função de média em Python com números de linha' \
  'Função de máximo em C++ sem números de linha' \
  'Arquivo Python externo com números de linha' \
  'Método Java com numeração a cada duas linhas' \
  'Arquivo C++ apresentado como apêndice'

check_list documento.loa \
  'Busca linear' \
  'Máximo divisor comum com números de linha' \
  'Seleção do maior valor sem números de linha'

echo 'Corpus visual e semântico do documento de referência validado.'
