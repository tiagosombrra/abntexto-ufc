#!/bin/sh
set -eu

fixture="tests/documents/references-6023-2025.tex"
job="referencias-6023-2025"

cleanup_job() {
  rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
        "$job".out "$job".pdf "$job".run.xml "$job".toc
}

for engine in pdflatex lualatex; do
  cleanup_job
  echo "Validating $fixture with $engine + Biber..."

  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-6023.log 2>&1 || {
    cat /tmp/abntexto-ufc-6023.log
    exit 1
  }

  biber "$job" > /tmp/abntexto-ufc-6023-biber.log 2>&1 || {
    cat /tmp/abntexto-ufc-6023-biber.log
    exit 1
  }

  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-6023.log 2>&1 || {
    cat /tmp/abntexto-ufc-6023.log
    exit 1
  }
  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-6023.log 2>&1 || {
    cat /tmp/abntexto-ufc-6023.log
    exit 1
  }

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Preflight failed: regression NBR 6023:2025 contains unrecognized warning or overflow."
    exit 1
  fi

done

if command -v pdftotext >/dev/null 2>&1; then
  pdftotext -layout "$job.pdf" /tmp/abntexto-ufc-6023.txt
  python3 - <<'PY'
import re
import unicodedata
from pathlib import Path

text = Path('/tmp/abntexto-ufc-6023.txt').read_text(encoding='utf-8')
text = unicodedata.normalize('NFC', text)
chunks = [re.sub(r'\s+', ' ', part).strip() for part in re.split(r'\n\s*\n', text) if part.strip()]

def entry(marker):
    marker_fold = marker.casefold()
    matches = [part for part in chunks if marker_fold in part.casefold()]
    if not matches:
        raise SystemExit(f'entry of teste missing: {marker}\n{text}')
    return ' '.join(matches)

event = entry('Congresso Brasileiro de Teste')
if re.search(r'\[\s*[Ss]\.\s*[Ll]\.\s*\]', event):
    raise SystemExit('NBR 6023:2025: evento sem cidade recebeu sine loco.')

article = entry('Preservação digital em ambientes acadêmicos')
if 'e202501' not in article:
    raise SystemExit('NBR 6023:2025: e-location missing.')

judgment = entry('Recurso extraordinário de teste')
if 'julgado em' not in judgment.casefold() or '2025' not in judgment:
    raise SystemExit('NBR 6023:2025: data of judgment missing.')

online = entry('Preservação de documentos digitais')
if re.search(r'\[\s*[Ss]\.\s*[Ll]\.', online) or re.search(r'\[\s*[Ss]\.\s*[Nn]\.', online):
    raise SystemExit('NBR 6023:2025: documento eletrônico recebeu indicador of publicação unknown.')

printed = entry('Preservação de documentos impressos')
if not re.search(r'[Ss]\.\s*[Ll]\.', printed) or not re.search(r'[Ss]\.\s*[Nn]\.', printed):
    raise SystemExit('NBR 6023:2025: documento impresso sem dados perdeu [S. l.] ou [s. n.].')

supplement = entry('Indicadores acadêmicos brasileiros')
if 'suplemento' not in supplement.casefold() or supplement.find('2025') > supplement.casefold().find('suplemento'):
    raise SystemExit('NBR 6023:2025: suplemento não está posicionado após a data.')

interview = entry('Eficiência e inovação na gestão')
if 'hamel' not in interview.casefold():
    raise SystemExit('NBR 6023:2025: entrevistado não aparece como autor principal.')

periodical = entry('REVISTA BRASILEIRA DE TESTE. Fortaleza')
if '1234-5678' not in periodical:
    raise SystemExit('NBR 6023:2025: ISSN opcional não foi preservado.')

identifiers = entry('Identificadores persistentes em referências')
if '10.1234/exemplo.2025.1' not in identifiers or '0000-0002-1825-0097' not in identifiers:
    raise SystemExit('NBR 6023:2025: DOI or ORCID supplemental missing.')
PY

  evidence_json="${UFC_EVIDENCE_DIR:-artifacts/validation/reference-semantics}/reference-semantics.json"
  set -- python3 tests/checks/normative_reference_semantics.py \
    /tmp/abntexto-ufc-6023.txt --json "$evidence_json"
  if [ -n "${GITHUB_SHA:-}" ]; then
    set -- "$@" --commit-sha "$GITHUB_SHA"
  fi
  "$@"
  echo 'VALIDATION-EVIDENCE rule=references.nbr6023-2025.test-profile status=PASS expected=nine-profile-cases measured=nine-cases-validated'
fi

echo 'Gate NBR 6023:2025 completed.'
