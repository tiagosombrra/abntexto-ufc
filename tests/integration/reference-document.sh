#!/bin/sh
set -eu

sh tests/integration/reference-guide-contract.sh

make clean
make compile

log="template/main.log"
pdf="template/main.pdf"
toc="template/main.toc"

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Underfull \\hbox|Overfull \\vbox' "$log" || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Reference document failed: review the warnings above.'
  exit 1
fi

sh tests/integration/font-embedding.sh "$pdf"

if command -v pdfinfo >/dev/null 2>&1; then
  metadata="/tmp/abntexto-ufc-reference-pdfa-meta.xml"
  pdfinfo -meta "$pdf" > "$metadata"
  grep -Eq '<pdfaid:part>2</pdfaid:part>' "$metadata" || {
    echo 'Reference document failed: PDF/A part 2 declaration is missing.'
    exit 1
  }
  grep -Eq '<pdfaid:conformance>[Bb]</pdfaid:conformance>' "$metadata" || {
    echo 'Reference document failed: PDF/A-2b conformance declaration is missing.'
    exit 1
  }

  pages=$(pdfinfo "$pdf" | awk '/^Pages:/ {print $2}')
  [ "${pages:-0}" -ge 15 ] || {
    echo "Reference document failed: tutorial is unexpectedly short (${pages:-0} pages)."
    exit 1
  }
  [ "$pages" -le 35 ] || {
    echo "Reference document failed: tutorial exceeded the 35-page compactness budget ($pages pages)."
    exit 1
  }
  echo "TUTORIAL-SIZE-EVIDENCE status=PASS pages=$pages min=15 max=35"
fi

python3 <<'PY'
import re
from pathlib import Path

cases = (
    ('template/frontmatter/summary.tex', r'\ufcSummaryKeywords', 'Summary'),
    ('template/frontmatter/abstract.tex', r'\keywords', 'Abstract'),
)

for path, marker, label in cases:
    source = Path(path).read_text(encoding='utf-8')
    body = re.split(marker, source, maxsplit=1)[0]
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*", body)
    if not 150 <= len(words) <= 500:
        raise SystemExit(f'{label} tutorial text outside the 150–500 word range: {len(words)}')
PY

if command -v pdftotext >/dev/null 2>&1; then
  text="/tmp/abntexto-ufc-reference.txt"
  pdftotext "$pdf" "$text"

  for marker in     'RESUMO'     'ABSTRACT'     'LISTA DE ILUSTRAÇÕES'     'LISTA DE TABELAS'     'SUMÁRIO'     'INTRODUÇÃO'     'FUNDAMENTAÇÃO TEÓRICA'     'METODOLOGIA'     'RESULTADOS E DISCUSSÃO'     'CONCLUSÃO'     'REFERÊNCIAS'     'GLOSSÁRIO'
  do
    grep -Fq "$marker" "$text" || {
      echo "Reference document failed: rendered tutorial marker is missing: $marker"
      exit 1
    }
  done

  python3 - "$text" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

path = Path(sys.argv[1])
raw = unicodedata.normalize('NFC', path.read_text(encoding='utf-8', errors='replace'))
flat = re.sub(r'\s+', ' ', raw)

pages = [re.sub(r'\s+', ' ', page) for page in raw.split('\f')]
approval_pages = [page for page in pages if 'BANCA EXAMINADORA' in page]
if len(approval_pages) != 1:
    raise SystemExit(
        f'Reference document failed: expected exactly one approval page, found {len(approval_pages)}.'
    )
approval = approval_pages[0]

expected_approval_date = '12 de setembro de 2026'
if expected_approval_date not in approval:
    raise SystemExit(
        f'Reference document failed: approval date is not the expected concrete date: {expected_approval_date}'
    )

expected_committee = (
    'Prof. Dr. Nome do Orientador',
    'Profa. Dra. Nome do Segundo Membro',
    'Prof. Dr. Nome do Terceiro Membro',
)
for member in expected_committee:
    if member not in approval:
        raise SystemExit(f'Reference document failed: expected committee member is missing: {member}')

for forbidden_member in (
    'Nome do Quarto Membro',
    'Nome do Quinto Membro',
    'Nome do Sexto Membro',
):
    if forbidden_member in approval:
        raise SystemExit(f'Reference document failed: extra committee member rendered: {forbidden_member}')

for forbidden_detail in (
    'Nome do Centro ou Unidade',
    'Departamento ou Unidade Acadêmica',
    'Programa de Pós-Graduação ou Unidade Acadêmica',
    '(Orientador)',
    '(Orientadora)',
):
    if forbidden_detail in approval:
        raise SystemExit(
            f'Reference document failed: committee must render only name and institution; found: {forbidden_detail}'
        )

if 'dia de mês de 2026' in flat:
    raise SystemExit('Reference document failed: placeholder approval date remains in canonical output.')
if 'ÍNDICE REMISSIVO' in flat:
    raise SystemExit('Reference document failed: tutorial unexpectedly renders a remissive index.')

complete_author = 'NOME COMPLETO DO AUTOR'
if complete_author not in flat:
    raise SystemExit(
        'Reference document failed: complete-author-name placeholder is missing from generated output.'
    )

object_titles = (
    'Fluxo simplificado da validação automatizada',
    'Critérios observados no procedimento demonstrativo',
    'Função auxiliar para cálculo da média',
    'Resultados sintéticos da validação',
)
for marker in object_titles:
    if marker not in flat:
        raise SystemExit(f'Reference document failed: tutorial object is missing: {marker}')

ufc_phrase = 'Universidade Federal do Ceará (UFC)'
if ufc_phrase not in flat:
    raise SystemExit('Reference document failed: full UFC name followed by acronym is missing.')

intro_source = Path('template/chapters/1-introduction.tex').read_text(encoding='utf-8')
phrase_at = intro_source.find(ufc_phrase)
first_ufc = re.search(r'\bUFC\b', intro_source)
expected_ufc_at = phrase_at + ufc_phrase.index('UFC') if phrase_at >= 0 else -1
if phrase_at < 0 or first_ufc is None or first_ufc.start() != expected_ufc_at:
    raise SystemExit(
        'Reference document failed: the first source-level UFC occurrence is not the full-name introduction.'
    )

legacy_headings = (
    'Estrutura do trabalho acadêmico',
    'Elementos pré-textuais em detalhe',
    'Formatação geral e organização da parte textual',
    'Ilustrações, tabelas e outros objetos acadêmicos',
    'Recursos do abntexto-ufc, elementos pós-textuais e revisão final',
)
for marker in legacy_headings:
    if marker in flat:
        raise SystemExit(f'Reference document failed: legacy manual-style heading remains: {marker}')

annex_heading_tokens = ('ANEXO A', 'DOCUMENTO COMPLEMENTAR EXTERNO')
for marker in annex_heading_tokens:
    if marker not in flat:
        raise SystemExit(f'Reference document failed: tutorial annex heading token is missing: {marker}')

source_marker = 'Instituição ou autor responsável pelo documento externo (ano)'
if source_marker not in flat:
    raise SystemExit('Reference document failed: tutorial annex source attribution is missing.')

print(
    'TUTORIAL-REFERENCE-EVIDENCE status=PASS chapters=5 objects=4 '
    'approval_page=PASS first_ufc_use=PASS annex=PASS legacy_manual_headings=0'
)
PY
fi

grep -Eiq 'Introdu' "$toc" || {
  echo 'Reference document failed: Introduction is missing from the table of contents.'
  exit 1
}

python3 <<'PY'
import re
import unicodedata
from pathlib import Path

toc = Path('template/main.toc').read_text(encoding='utf-8', errors='replace')

for title in ('RESUMO', 'ABSTRACT', 'LISTA DE ILUSTRAÇÕES', 'LISTA DE TABELAS'):
    pattern = re.compile(
        r'\contentsline\s*\{[^}]+\}\s*\{' + re.escape(title) + r'\}\s*\{',
        re.IGNORECASE,
    )
    if pattern.search(toc):
        raise SystemExit(f'Reference document failed: front-matter element entered the table of contents: {title}')

normalized_toc = unicodedata.normalize('NFC', toc).casefold()
if '\toclabelbox{}Referências' in toc or '\toclabelbox{}\MakeUppercase{Glossário}' in toc:
    raise SystemExit(
        'Reference document failed: empty TOC label box reintroduced for unnumbered post-textual entries.'
    )
if 'índice remissivo' in normalized_toc:
    raise SystemExit('Reference document failed: tutorial TOC contains a remissive index.')

for marker in (
    'introdução',
    'fundamentação teórica',
    'metodologia',
    'resultados e discussão',
    'conclusão',
    'anexo',
    'documento complementar externo',
):
    if marker.casefold() not in normalized_toc:
        raise SystemExit(f'Reference document failed: TOC marker is missing: {marker}')

print(
    'TUTORIAL-TOC-EVIDENCE status=PASS chapters=5 '
    'frontmatter_entries=0 annex_entry=PASS posttextual_alignment_guard=PASS'
)
PY

echo 'Reference tutorial document validated.'
