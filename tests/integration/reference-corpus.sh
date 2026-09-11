#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/template"

[ -s main.pdf ] || {
  echo 'Corpus failed: main.pdf missing.'
  exit 1
}

for file in main.loi main.lot main.loc main.loa main.toc; do
  [ -s "$file" ] || {
    echo "Corpus failed: navigation file is missing: $file"
    exit 1
  }
done

if [ "${UFC_REQUIRE_REFERENCE_IMAGES:-0}" = 1 ]; then
  python3 <<'PY'
import hashlib
from pathlib import Path

expected = {
    Path('figures/ufc-campus-pici.jpg'): '5f431612cdbfbb088c37c685a0e3c93852e96ccd',
    Path('figures/ufc-reitoria.jpg'): 'b6746bb53d82dae52330805ca0a08f029b773b2e',
}
for path, digest in expected.items():
    if not path.is_file():
        raise SystemExit(f'Corpus failed: licensed photograph is missing: {path}')
    actual = hashlib.sha1(path.read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f'Corpus failed: SHA-1 mismatch in {path}: {actual}')
PY
fi

pdftotext -layout main.pdf /tmp/abntexto-ufc-reference-corpus.txt
pdftotext -bbox-layout main.pdf /tmp/abntexto-ufc-reference-corpus-bbox.html

python3 <<'PY'
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def normalize_pdf_text(value):
    value = value.replace('\u00ad', '')
    value = re.sub(r'-[ \t]*\r?\n[ \t]*(?=\w)', '', value)
    return re.sub(r'\s+', ' ', value)


def spaced_leader_pattern():
    return r'(?:\.\s+){1,}\d+\s*$'


ENTRY_START = re.compile(r'^\s*(?:Figura|Tabela|Código|Algoritmo)\s+\d+\s+[—-]\s+')


def list_entries(block):
    lines = block.splitlines()
    starts = [index for index, line in enumerate(lines) if ENTRY_START.match(line)]
    entries = []
    for position, start_index in enumerate(starts):
        end_index = starts[position + 1] if position + 1 < len(starts) else len(lines)
        raw_entry = '\n'.join(lines[start_index:end_index])
        entries.append((raw_entry, normalize_pdf_text(raw_entry)))
    return entries


def require_dotted_entry(source, start, end, marker):
    start_at = source.find(start)
    end_at = source.find(end, start_at + len(start))
    if start_at < 0 or end_at < 0:
        raise SystemExit(f'Corpus failed: block of list not found: {start}.')

    entries = list_entries(source[start_at:end_at])
    matches = [(raw, normalized) for raw, normalized in entries if marker in normalized]
    if len(matches) != 1:
        raise SystemExit(
            f'Corpus failed: expected exactly one entry for {start}: '
            f'{marker}; found {len(matches)}.'
        )

    _, normalized_entry = matches[0]
    if not re.search(spaced_leader_pattern(), normalized_entry):
        raise SystemExit(f'Corpus failed: spaced dotted leader missing in {start}: {marker}')


text = Path('/tmp/abntexto-ufc-reference-corpus.txt').read_text(encoding='utf-8', errors='replace')
flat = normalize_pdf_text(text)

main_source = Path('main.tex').read_text(encoding='utf-8')
if 'approval-date = {11 de setembro de 2026}' not in main_source:
    raise SystemExit('Corpus failed: canonical approval date is not the complete reviewed date.')
if 'index = none' not in main_source or r'\ufcPrintIndex' in main_source:
    raise SystemExit('Corpus failed: canonical TCC still enables or prints the index module.')
for forbidden_key in ('examiner-4 =', 'examiner-5 =', 'examiner-6 ='):
    if forbidden_key in main_source:
        raise SystemExit('Corpus failed: canonical TCC still declares an extra committee member: ' + forbidden_key)
for required_blank in ('advisor-unit = {},', 'examiner-2-unit = {},', 'examiner-3-unit = {},'):
    if required_blank not in main_source:
        raise SystemExit('Corpus failed: canonical committee unit field is not blank: ' + required_blank)
for chapter in sorted(Path('chapters').glob('*.tex')):
    if r'\index{' in chapter.read_text(encoding='utf-8'):
        raise SystemExit('Corpus failed: canonical chapter still contains index markers: ' + str(chapter))

required = (
    'MODELO COMENTADO DE TRABALHO ACADÊMICO DA UFC',
    'INTRODUÇÃO E USO DESTE MODELO',
    'Base normativa adotada',
    'ESTRUTURA DO TRABALHO ACADÊMICO',
    'ELEMENTOS PRÉ-TEXTUAIS EM DETALHE',
    'FORMATAÇÃO GERAL E ORGANIZAÇÃO DA PARTE TEXTUAL',
    'CITAÇÕES, NOTAS E REFERÊNCIAS',
    'ILUSTRAÇÕES, TABELAS E OUTROS OBJETOS ACADÊMICOS',
    'RECURSOS DO ABNTEXTO-UFC, ELEMENTOS PÓS-TEXTUAIS E REVISÃO FINAL',
    'Base normativa',
    'Orientação institucional UFC',
    'Política do modelo',
    'Exemplo',
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
    'Aprovada em: 11 de setembro de 2026',
    'ABNT NBR 14724:2024',
    'ABNT NBR 6023:2025',
    'ABNT NBR 10520:2023',
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
    raise SystemExit('Corpus failed: markers missing in the PDF: ' + ', '.join(missing))
if '??' in text:
    raise SystemExit('Corpus failed: unresolved reference found in the PDF.')
require_reference_images = os.environ.get('UFC_REQUIRE_REFERENCE_IMAGES', '0') == '1'
if require_reference_images and 'Execute make reference-assets' in text:
    raise SystemExit('Corpus failed: photograph fallback appeared while reference photographs were required.')

pages = [normalize_pdf_text(page) for page in text.split('\f')]
committee_pages = [page for page in pages if 'BANCA EXAMINADORA' in page]
if len(committee_pages) != 1:
    raise SystemExit(f'Corpus failed: expected exactly one committee block, found {len(committee_pages)}.')
committee = committee_pages[0]
committee_members = (
    'Nome do Orientador',
    'Nome do Segundo Membro',
    'Nome do Terceiro Membro',
)
missing_committee = [name for name in committee_members if name not in committee]
if missing_committee:
    raise SystemExit('Corpus failed: expected three-person committee is incomplete: ' + ', '.join(missing_committee))
for forbidden in (
    'Nome do Quarto Membro',
    'Nome do Quinto Membro',
    'Nome do Sexto Membro',
    'Nome do Centro ou Unidade',
    'Departamento ou Unidade Acadêmica',
    'Centro, Faculdade, Instituto ou Campus',
    'Programa de Pós-Graduação ou Unidade Acadêmica',
):
    if forbidden in committee:
        raise SystemExit('Corpus failed: canonical committee contains forbidden extra member/unit text: ' + forbidden)

if 'ÍNDICE REMISSIVO' in flat:
    raise SystemExit('Corpus failed: canonical TCC must not render an index.')

list_blocks = (
    ('LISTA DE ILUSTRAÇÕES', 'LISTA DE TABELAS', 'Figura 1 — Figura estreita com legenda curta'),
    ('LISTA DE TABELAS', 'LISTA DE CÓDIGOS', 'Tabela 1 — Organização didática dos componentes exercitados pelo documento de referência'),
    ('LISTA DE CÓDIGOS', 'LISTA DE ALGORITMOS', 'Código 1 — Função de média em Python com números de linha'),
    ('LISTA DE ALGORITMOS', 'LISTA DE ABREVIATURAS E SIGLAS', 'Algoritmo 1 — Máximo divisor comum com números de linha'),
)
for start, end, marker in list_blocks:
    start_at = flat.find(start)
    end_at = flat.find(end, start_at + len(start))
    if start_at < 0 or end_at < 0:
        raise SystemExit(f'Corpus failed: block of list not found: {start}.')
    block = flat[start_at:end_at]
    if marker not in block:
        raise SystemExit(f'Corpus failed: case-preserved entry is missing from {start}: {marker}')
    if marker.upper() in block:
        raise SystemExit(f'Corpus failed: entry was incorrectly converted to uppercase in {start}.')
    require_dotted_entry(text, start, end, marker)

raw_pages = text.split('\f')
toc_starts = [
    index for index, page in enumerate(raw_pages)
    if 'SUMÁRIO' in page and 'INTRODUÇÃO E USO DESTE MODELO' in page
]
if len(toc_starts) != 1:
    raise SystemExit(f'Corpus failed: expected one main table of contents, found {len(toc_starts)}.')

toc_start = toc_starts[0]
toc_end = None
for index in range(toc_start + 1, len(raw_pages)):
    if re.search(r'^\s*1\s+INTRODUÇÃO E USO DESTE MODELO\s*$', raw_pages[index], re.M):
        toc_end = index
        break
if toc_end is None:
    raise SystemExit('Corpus failed: end of the table of contents was not found before the first textual section.')

toc = '\n'.join(raw_pages[toc_start:toc_end])
toc_flat = normalize_pdf_text(toc)
for marker in (
    'INTRODUÇÃO E USO DESTE MODELO',
    'Base normativa adotada',
    'ESTRUTURA DO TRABALHO ACADÊMICO',
    'ELEMENTOS PRÉ-TEXTUAIS EM DETALHE',
    'FORMATAÇÃO GERAL E ORGANIZAÇÃO DA PARTE TEXTUAL',
    'CITAÇÕES, NOTAS E REFERÊNCIAS',
    'ILUSTRAÇÕES, TABELAS E OUTROS OBJETOS ACADÊMICOS',
    'RECURSOS DO ABNTEXTO-UFC, ELEMENTOS PÓS-TEXTUAIS E REVISÃO FINAL',
    'REFERÊNCIAS',
    'GLOSSÁRIO',
    'APÊNDICE A',
    'APÊNDICE D',
    'ANEXO A',
    'ANEXO B',
):
    if marker not in toc_flat:
        raise SystemExit(f'Corpus failed: required entry is missing from the table of contents: {marker}.')

entry_lines = [line for line in toc.splitlines() if re.search(r'\d+\s*$', line)]
if len(entry_lines) < 29:
    raise SystemExit(f'Corpus failed: too few paginated entries in the annotated table of contents: {len(entry_lines)}.')

numbered_entry_lines = [
    line for line in entry_lines
    if re.match(r'^\s*\d+(?:\.\d+)*\s+', line)
]
undotted_numbered = [
    line.strip() for line in numbered_entry_lines
    if not re.search(spaced_leader_pattern(), line)
]
if undotted_numbered:
    sample = ' | '.join(undotted_numbered[:8])
    raise SystemExit(
        f'Corpus failed: {len(undotted_numbered)} numbered table-of-contents entries lack dotted leaders: {sample}'
    )

layout_source = Path('../abntexto-ufc/layout.def').read_text(encoding='utf-8')
forced_dot = r'\hbox to 1.1em{\leaders\ufctocdot\hfil}'
if forced_dot in layout_source:
    raise SystemExit('Corpus failed: table of contents still forces a standalone terminal dot before leaders.')

root = ET.parse('/tmp/abntexto-ufc-reference-corpus-bbox.html').getroot()
local = lambda tag: tag.rsplit('}', 1)[-1]
bbox_pages = [node for node in root.iter() if local(node.tag) == 'page']
if toc_end > len(bbox_pages):
    raise SystemExit(
        f'Corpus failed: physical table-of-contents range exceeds BBox pages: '
        f'toc_end={toc_end}, bbox_pages={len(bbox_pages)}.'
    )


def toc_title_x(marker):
    matches = []
    for page_index in range(toc_start, toc_end):
        page = bbox_pages[page_index]
        for line in (node for node in page.iter() if local(node.tag) == 'line'):
            words = [node for node in line if local(node.tag) == 'word']
            if not words:
                continue
            raw = ' '.join(''.join(word.itertext()) for word in words)
            if not raw.startswith(marker):
                continue
            matches.append((raw, float(words[0].attrib['xMin']), page_index + 1))
    if len(matches) != 1:
        raise SystemExit(
            f'Corpus failed: expected one primary table-of-contents heading for {marker}; found {len(matches)}.'
        )
    return matches[0][1]

reference_x = toc_title_x('INTRODUÇÃO E USO DESTE MODELO')
for marker in (
    'ESTRUTURA DO TRABALHO ACADÊMICO',
    'ELEMENTOS PRÉ-TEXTUAIS EM DETALHE',
    'FORMATAÇÃO GERAL E ORGANIZAÇÃO DA PARTE TEXTUAL',
    'CITAÇÕES, NOTAS E REFERÊNCIAS',
    'ILUSTRAÇÕES, TABELAS E OUTROS OBJETOS ACADÊMICOS',
    'RECURSOS DO ABNTEXTO-UFC',
    'REFERÊNCIAS',
    'GLOSSÁRIO',
):
    actual_x = toc_title_x(marker)
    if abs(actual_x - reference_x) > 1.5:
        raise SystemExit(
            f'Corpus failed: {marker} is misaligned in the table of contents: '
            f'x={actual_x:.2f}, reference={reference_x:.2f}'
        )
PY

check_list() {
  file="$1"
  shift
  for marker in "$@"; do
    grep -Fq "$marker" "$file" || {
      echo "Corpus failed: '$marker' is missing from $file"
      exit 1
    }
  done
}

check_list main.loi \
  'Figura estreita com legenda curta' \
  'Figura de largura intermediária' \
  'Figura larga próxima à largura útil' \
  'Fluxo de processamento em arquivo PNG raster' \
  'Campus do Pici, onde se localiza o Departamento de Computação da UFC' \
  'Reitoria da Universidade Federal do Ceará' \
  'Distribuição sintética de três categorias' \
  'Comparação de configurações editoriais'

check_list main.lot \
  'Organização didática dos componentes exercitados pelo documento de referência' \
  'Indicadores sintéticos com linhas alternadas'

check_list main.loc \
  'Função de média em Python com números de linha' \
  'Função de máximo em C++ sem números de linha' \
  'Arquivo Python externo com números de linha' \
  'Método Java com numeração a cada duas linhas' \
  'Código C++ apresentado como apêndice'

check_list main.loa \
  'Máximo divisor comum com números de linha' \
  'Seleção do maior valor sem números de linha'

echo 'Visual, instructional, and semantic reference corpus validated.'
