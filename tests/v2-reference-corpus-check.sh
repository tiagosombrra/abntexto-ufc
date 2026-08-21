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
import re
from pathlib import Path


def normalize_pdf_text(value):
    value = value.replace('\u00ad', '')
    value = re.sub(r'-[ \t]*\r?\n[ \t]*(?=\w)', '', value)
    return re.sub(r'\s+', ' ', value)


text = Path('/tmp/ufctex-v2-reference-corpus.txt').read_text(encoding='utf-8', errors='replace')
flat = normalize_pdf_text(text)
required = (
    'CATÁLOGO DE EXEMPLOS E VALIDAÇÃO VISUAL',
    'Normas e diretrizes adotadas',
    'Referências bibliográficas e recursos eletrônicos',
    'Figura estreita com legenda curta',
    'Figura de largura intermediária',
    'Figura larga próxima à largura útil',
    'Fluxo de processamento em arquivo PNG raster',
    'Campus do Pici',
    'Vista da Lagoa do Pici no Campus do Pici',
    'Reitoria da Universidade Federal do Ceará',
    'Distribuição sintética de três categorias',
    'Comparação de configurações editoriais',
    'Indicadores sintéticos com linhas alternadas',
    'Função de média em Python com números de linha',
    'Função de máximo em C++ sem números de linha',
    'Arquivo Python externo com números de linha',
    'Método Java com numeração a cada duas linhas',
    'Máximo divisor comum com números de linha',
    'Seleção do maior valor sem números de linha',
    'Nome do Quinto Membro',
    'Nome do Sexto Membro',
    'ABNT NBR 14724:2024',
    'ABNT NBR 6023:2025',
    'HTTP Semantics',
    'APÊNDICE A',
    'APÊNDICE B',
    'APÊNDICE C',
    'APÊNDICE D',
    'ANEXO A',
    'ANEXO B',
)
missing = [marker for marker in required if marker not in flat]
if missing:
    raise SystemExit('Corpus V2 falhou: marcadores ausentes no PDF: ' + ', '.join(missing))
if '??' in text:
    raise SystemExit('Corpus V2 falhou: referência não resolvida encontrada no PDF.')
if 'Execute make reference-assets' in text:
    raise SystemExit('Corpus V2 falhou: fallback de fotografia apareceu no PDF de CI.')

pages = [normalize_pdf_text(page) for page in text.split('\f')]
committee_pages = [page for page in pages if 'BANCA EXAMINADORA' in page]
if len(committee_pages) != 1:
    raise SystemExit(f'Corpus V2 falhou: esperado exatamente um bloco de banca, encontrados {len(committee_pages)}.')
committee = committee_pages[0]
committee_members = (
    'Nome do Orientador',
    'Nome do Segundo Membro',
    'Nome do Terceiro Membro',
    'Nome do Quarto Membro',
    'Nome do Quinto Membro',
    'Nome do Sexto Membro',
)
missing_committee = [name for name in committee_members if name not in committee]
if missing_committee:
    raise SystemExit('Corpus V2 falhou: banca não cabe integralmente na folha de aprovação: ' + ', '.join(missing_committee))

list_blocks = (
    ('LISTA DE ILUSTRAÇÕES', 'LISTA DE TABELAS', 'Figura 1 — Exemplo de figura no padrão V2'),
    ('LISTA DE TABELAS', 'LISTA DE CÓDIGOS', 'Tabela 1 — Etapas do procedimento'),
    ('LISTA DE CÓDIGOS', 'LISTA DE ALGORITMOS', 'Código 1 — Função de soma em C++'),
    ('LISTA DE ALGORITMOS', 'LISTA DE ABREVIATURAS E SIGLAS', 'Algoritmo 1 — Busca linear'),
)
for start, end, marker in list_blocks:
    start_at = flat.find(start)
    end_at = flat.find(end, start_at + len(start))
    if start_at < 0 or end_at < 0:
        raise SystemExit(f'Corpus V2 falhou: bloco de lista não localizado: {start}.')
    block = flat[start_at:end_at]
    if marker not in block:
        raise SystemExit(f'Corpus V2 falhou: entrada com caixa preservada ausente de {start}: {marker}')
    if marker.upper() in block:
        raise SystemExit(f'Corpus V2 falhou: entrada indevidamente convertida para caixa alta em {start}.')
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
  'Código C++ apresentado como apêndice'

check_list documento.loa \
  'Busca linear' \
  'Máximo divisor comum com números de linha' \
  'Seleção do maior valor sem números de linha'

echo 'Corpus visual e semântico do documento de referência validado.'
