#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/template"

[ -s main.pdf ] || {
  echo 'Corpus failed: main.pdf missing.'
  exit 1
}

# The compact tutorial intentionally renders illustration, table and code lists.
# It does not enable algorithms by default, so main.loa is not part of the
# canonical navigation contract.
for file in main.loi main.lot main.loc main.toc; do
  [ -s "$file" ] || {
    echo "Corpus failed: navigation file is missing: $file"
    exit 1
  }
done

pdftotext -layout main.pdf /tmp/abntexto-ufc-reference-corpus.txt
pdftotext -bbox-layout main.pdf /tmp/abntexto-ufc-reference-corpus-bbox.html

python3 <<'PY'
import re
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path


def normalize_pdf_text(value: str) -> str:
    value = value.replace('\u00ad', '')
    value = re.sub(r'-[ \t]*\r?\n[ \t]*(?=\w)', '', value)
    return re.sub(r'\s+', ' ', value)


def spaced_leader_pattern() -> str:
    return r'(?:\.\s+){1,}\d+\s*$'


ENTRY_START = re.compile(r'^\s*(?:Figura|Tabela|Código)\s+\d+\s+[—-]\s+')


def list_entries(block: str):
    lines = block.splitlines()
    starts = [index for index, line in enumerate(lines) if ENTRY_START.match(line)]
    entries = []
    for position, start_index in enumerate(starts):
        end_index = starts[position + 1] if position + 1 < len(starts) else len(lines)
        raw_entry = '\n'.join(lines[start_index:end_index])
        entries.append((raw_entry, normalize_pdf_text(raw_entry)))
    return entries


def require_dotted_entry(source: str, start: str, end: str, marker: str) -> None:
    start_at = source.find(start)
    end_at = source.find(end, start_at + len(start))
    if start_at < 0 or end_at < 0:
        raise SystemExit(f'Corpus failed: list block not found: {start}.')

    entries = list_entries(source[start_at:end_at])
    matches = [(raw, normalized) for raw, normalized in entries if marker in normalized]
    if len(matches) != 1:
        raise SystemExit(
            f'Corpus failed: expected exactly one entry in {start}: '
            f'{marker}; found {len(matches)}.'
        )

    _, normalized_entry = matches[0]
    if not re.search(spaced_leader_pattern(), normalized_entry):
        raise SystemExit(
            f'Corpus failed: spaced dotted leader missing in {start}: {marker}'
        )


text = Path('/tmp/abntexto-ufc-reference-corpus.txt').read_text(
    encoding='utf-8', errors='replace'
)
flat = normalize_pdf_text(text)

required = (
    'VALIDAÇÃO AUTOMATIZADA DE DOCUMENTOS ACADÊMICOS EM LATEX',
    'INTRODUÇÃO',
    'FUNDAMENTAÇÃO TEÓRICA',
    'METODOLOGIA',
    'RESULTADOS E DISCUSSÃO',
    'CONCLUSÃO',
    'Fluxo simplificado da validação automatizada',
    'Critérios observados no procedimento demonstrativo',
    'Função auxiliar para cálculo da média',
    'Resultados sintéticos da validação',
    'Aprovada em: 12 de setembro de 2026',
    'ABNT NBR 14724:2024',
    'ABNT NBR 6023:2025',
    'ABNT NBR 10520:2023',
    'REFERÊNCIAS',
    'GLOSSÁRIO',
    'APÊNDICE A',
    'ANEXO A',
)
missing = [marker for marker in required if marker not in flat]
if missing:
    raise SystemExit(
        'Corpus failed: markers missing in the tutorial PDF: ' + ', '.join(missing)
    )
if '??' in text:
    raise SystemExit('Corpus failed: unresolved reference found in the tutorial PDF.')

pages = [normalize_pdf_text(page) for page in text.split('\f')]
committee_pages = [page for page in pages if 'BANCA EXAMINADORA' in page]
if len(committee_pages) != 1:
    raise SystemExit(
        f'Corpus failed: expected exactly one committee block, found {len(committee_pages)}.'
    )
committee = committee_pages[0]
for name in (
    'Nome do Orientador',
    'Nome do Segundo Membro',
    'Nome do Terceiro Membro',
):
    if name not in committee:
        raise SystemExit(
            f'Corpus failed: canonical three-member committee is incomplete: {name}'
        )
for forbidden in (
    'Nome do Quarto Membro',
    'Nome do Quinto Membro',
    'Nome do Sexto Membro',
    'Nome do Centro ou Unidade',
    'Departamento ou Unidade Acadêmica',
    'Programa de Pós-Graduação ou Unidade Acadêmica',
    '(Orientador)',
    '(Orientadora)',
):
    if forbidden in committee:
        raise SystemExit(
            f'Corpus failed: retired canonical committee content remains: {forbidden}'
        )

list_blocks = (
    (
        'LISTA DE ILUSTRAÇÕES',
        'LISTA DE TABELAS',
        'Figura 1 — Fluxo simplificado da validação automatizada',
    ),
    (
        'LISTA DE TABELAS',
        'LISTA DE CÓDIGOS',
        'Tabela 1 — Critérios observados no procedimento demonstrativo',
    ),
    (
        'LISTA DE CÓDIGOS',
        'SUMÁRIO',
        'Código 1 — Função auxiliar para cálculo da média',
    ),
)
for start, end, marker in list_blocks:
    start_at = flat.find(start)
    end_at = flat.find(end, start_at + len(start))
    if start_at < 0 or end_at < 0:
        raise SystemExit(f'Corpus failed: list block not found: {start}.')
    block = flat[start_at:end_at]
    if marker not in block:
        raise SystemExit(
            f'Corpus failed: case-preserved entry is missing from {start}: {marker}'
        )
    if marker.upper() in block:
        raise SystemExit(
            f'Corpus failed: entry was incorrectly converted to uppercase in {start}.'
        )
    require_dotted_entry(text, start, end, marker)

raw_pages = text.split('\f')
toc_starts = [
    index
    for index, page in enumerate(raw_pages)
    if 'SUMÁRIO' in page and 'INTRODUÇÃO' in page
]
if len(toc_starts) != 1:
    raise SystemExit(
        f'Corpus failed: expected one main table of contents, found {len(toc_starts)}.'
    )

toc_start = toc_starts[0]
toc_end = None
for index in range(toc_start + 1, len(raw_pages)):
    normalized_page = normalize_pdf_text(raw_pages[index])
    if re.search(r'\b1\s+INTRODUÇÃO\b', normalized_page):
        toc_end = index
        break
if toc_end is None:
    raise SystemExit(
        'Corpus failed: end of the table of contents was not found before the first textual section.'
    )

toc = '\n'.join(raw_pages[toc_start:toc_end])
toc_flat = normalize_pdf_text(toc)
if 'ÍNDICE REMISSIVO' in toc_flat:
    raise SystemExit(
        'Corpus failed: canonical tutorial table of contents contains the optional remissive index.'
    )

for marker in (
    'INTRODUÇÃO',
    'FUNDAMENTAÇÃO TEÓRICA',
    'METODOLOGIA',
    'RESULTADOS E DISCUSSÃO',
    'CONCLUSÃO',
    'REFERÊNCIAS',
    'GLOSSÁRIO',
    'APÊNDICE A',
    'ANEXO A',
):
    if marker not in toc_flat:
        raise SystemExit(
            f'Corpus failed: required entry is missing from the table of contents: {marker}.'
        )

entry_lines = [line for line in toc.splitlines() if re.search(r'\d+\s*$', line)]
if len(entry_lines) < 15:
    raise SystemExit(
        f'Corpus failed: too few paginated entries in the compact tutorial TOC: {len(entry_lines)}.'
    )
undotted = [
    line.strip()
    for line in entry_lines
    if not re.search(spaced_leader_pattern(), line)
]
if undotted:
    sample = ' | '.join(undotted[:8])
    raise SystemExit(
        f'Corpus failed: {len(undotted)} table-of-contents entries lack spaced dotted leaders: {sample}'
    )

root = ET.parse('/tmp/abntexto-ufc-reference-corpus-bbox.html').getroot()
local = lambda tag: tag.rsplit('}', 1)[-1]
bbox_pages = [node for node in root.iter() if local(node.tag) == 'page']
if toc_end > len(bbox_pages):
    raise SystemExit(
        f'Corpus failed: physical TOC range exceeds BBox pages: '
        f'toc_end={toc_end}, bbox_pages={len(bbox_pages)}.'
    )


def normalized_line_words(line):
    words = [node for node in line if local(node.tag) == 'word']
    raw = ' '.join(''.join(word.itertext()) for word in words)
    normalized = normalize_pdf_text(raw)
    return words, normalized


def toc_title_x(marker: str) -> float:
    matches = []
    for page_index in range(toc_start, toc_end):
        page = bbox_pages[page_index]
        for line in (node for node in page.iter() if local(node.tag) == 'line'):
            words, raw = normalized_line_words(line)
            if not words:
                continue
            # Numbered primary entries may start with "1 ", "2 ", etc.
            cleaned = re.sub(r'^\d+\s+', '', raw)
            if not cleaned.startswith(marker):
                continue
            # For numbered lines, use the first title word rather than the number.
            first_title = words[1] if raw != cleaned and len(words) > 1 else words[0]
            matches.append((raw, float(first_title.attrib['xMin']), page_index + 1))
    if len(matches) != 1:
        raise SystemExit(
            f'Corpus failed: expected one primary TOC heading for {marker}; '
            f'found {len(matches)}.'
        )
    return matches[0][1]


numbered_reference_x = toc_title_x('INTRODUÇÃO')
for marker in (
    'FUNDAMENTAÇÃO TEÓRICA',
    'METODOLOGIA',
    'RESULTADOS E DISCUSSÃO',
    'CONCLUSÃO',
):
    actual_x = toc_title_x(marker)
    if abs(actual_x - numbered_reference_x) > 1.5:
        raise SystemExit(
            f'Corpus failed: numbered entry {marker} is misaligned in the TOC: '
            f'x={actual_x:.2f}, reference={numbered_reference_x:.2f}.'
        )

# References and Glossary are unnumbered but must align with the same primary
# title column. This also rejects visible punctuation before either title.
for marker in ('REFERÊNCIAS', 'GLOSSÁRIO'):
    actual_x = toc_title_x(marker)
    if abs(actual_x - numbered_reference_x) > 1.5:
        raise SystemExit(
            f'Corpus failed: post-textual entry {marker} is misaligned in the TOC: '
            f'x={actual_x:.2f}, numbered-reference={numbered_reference_x:.2f}.'
        )

print(
    'TUTORIAL-CORPUS-EVIDENCE status=PASS '
    'navigation_files=4 list_blocks=3 toc_entries_min=15 '
    'primary_alignment=PASS posttextual_alignment=PASS'
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

check_list main.loi   'Fluxo simplificado da validação automatizada'

check_list main.lot   'Critérios observados no procedimento demonstrativo'   'Resultados sintéticos da validação'

check_list main.loc   'Função auxiliar para cálculo da média'

echo 'Compact tutorial visual, navigation, and semantic reference corpus validated.'
