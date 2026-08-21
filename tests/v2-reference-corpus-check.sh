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

if [ "${UFC_REQUIRE_REFERENCE_IMAGES:-0}" = 1 ]; then
  python3 <<'PY'
import hashlib
from pathlib import Path

expected = {
    Path('figuras/ufc-campus-pici.jpg'): '5f431612cdbfbb088c37c685a0e3c93852e96ccd',
    Path('figuras/ufc-reitoria.jpg'): 'b6746bb53d82dae52330805ca0a08f029b773b2e',
}
for path, digest in expected.items():
    if not path.is_file():
        raise SystemExit(f'Corpus V2 falhou: fotografia licenciada ausente: {path}')
    actual = hashlib.sha1(path.read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f'Corpus V2 falhou: SHA-1 divergente em {path}: {actual}')
PY
fi

pdftotext -layout documento.pdf /tmp/ufctex-v2-reference-corpus.txt

python3 <<'PY'
from pathlib import Path

text = Path('/tmp/ufctex-v2-reference-corpus.txt').read_text(encoding='utf-8', errors='replace')
required = (
    'CATÁLOGO DE EXEMPLOS E VALIDAÇÃO VISUAL',
    'Figura estreita com legenda curta',
    'Figura de largura intermediária',
    'Figura larga próxima à largura útil',
    'Fluxo de processamento em arquivo PNG raster',
    'Campus do Pici, onde se localiza o Departamento de Computação da UFC',
    'Reitoria da Universidade Federal do Ceará',
    'Distribuição sintética de três categorias em arquivo JPEG',
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
if 'Execute make reference-assets' in text:
    raise SystemExit('Corpus V2 falhou: fallback de fotografia apareceu no PDF de CI.')
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
  'Fluxo de processamento em arquivo PNG raster' \
  'Campus do Pici, onde se localiza o Departamento de Computação da UFC' \
  'Reitoria da Universidade Federal do Ceará' \
  'Distribuição sintética de três categorias em arquivo JPEG' \
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
