#!/bin/sh
set -eu


compile_project_with_biber() {
  engine="$1"
  job="research-project-15287"
  fixture="tests/documents/research-project-15287.tex"

  rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
        "$job".out "$job".pdf "$job".run.xml "$job".toc

  echo "Validating $fixture com $engine + Biber..."
  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-project.log 2>&1 || {
    cat /tmp/abntexto-ufc-project.log
    exit 1
  }
  biber "$job" > /tmp/abntexto-ufc-project-biber.log 2>&1 || {
    cat /tmp/abntexto-ufc-project-biber.log
    exit 1
  }
  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-project.log 2>&1 || {
    cat /tmp/abntexto-ufc-project.log
    exit 1
  }
  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-project.log 2>&1 || {
    cat /tmp/abntexto-ufc-project.log
    exit 1
  }
}

compile_plain_project() {
  engine="$1"
  fixture="$2"
  job="$3"

  rm -f "$job".aux "$job".log "$job".out "$job".pdf "$job".toc
  echo "Validating $fixture com $engine..."
  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-project.log 2>&1 || {
    cat /tmp/abntexto-ufc-project.log
    exit 1
  }
  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-project.log 2>&1 || {
    cat /tmp/abntexto-ufc-project.log
    exit 1
  }
  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-project.log 2>&1 || {
    cat /tmp/abntexto-ufc-project.log
    exit 1
  }
}

check_log() {
  log="$1"
  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Preflight failed: fixture de research project contains unrecognized warning or overflow."
    exit 1
  fi
}

for engine in pdflatex lualatex; do
  compile_project_with_biber "$engine"
  check_log research-project-15287.log
done

for engine in pdflatex lualatex; do
  compile_plain_project "$engine" tests/documents/research-project-without-cover.tex research-project-without-cover
  check_log research-project-without-cover.log
done

for engine in pdflatex lualatex; do
  compile_plain_project "$engine" tests/documents/frontmatter-anonymized-project.tex frontmatter-anonymized-research-project
  check_log frontmatter-anonymized-research-project.log
done

if grep -Eq 'brasao-ufc\.pdf|logo-ufc\.PNG' research-project-15287.log; then
  echo 'NBR 15287/UFC: coat of arms foi loaded por default na cover de research project.'
  exit 1
fi

if grep -Eq 'brasao-ufc\.pdf|logo-ufc\.PNG' frontmatter-anonymized-research-project.log; then
  echo 'NBR 15287/UFC: coat of arms foi loaded por default no research project anonymized.'
  exit 1
fi

if command -v pdftotext >/dev/null 2>&1; then
  pdftotext -layout research-project-15287.pdf /tmp/abntexto-ufc-project.txt
  pdftotext -layout research-project-without-cover.pdf /tmp/abntexto-ufc-project-no-cover.txt
  pdftotext -layout frontmatter-anonymized-research-project.pdf /tmp/abntexto-ufc-project-anon.txt

  python3 - <<'PY'
import re
import unicodedata
from pathlib import Path


def normalize(path):
    text = Path(path).read_text(encoding='utf-8')
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text)).strip()

project = normalize('/tmp/abntexto-ufc-project.txt')
no_cover = normalize('/tmp/abntexto-ufc-project-no-cover.txt')
anon = normalize('/tmp/abntexto-ufc-project-anon.txt')

for expected in (
    'UNIVERSIDADE FEDERAL DO CEARÁ',
    'AUTOR PROJETO TESTE',
    'PROJETO DE PESQUISA NORMATIVO',
    'VALIDAÇÃO DA NBR 15287',
    'PROJECT RESEARCH NORMATIVE TEST',
    'VOLUME 2',
    'INTRODUÇÃO',
    'REFERENCIAL TEÓRICO',
    'METODOLOGIA',
    'RECURSOS',
    'CRONOGRAMA',
    'REFERÊNCIAS',
):
    if expected.casefold() not in project.casefold():
        raise SystemExit(f'NBR 15287:2025: content required da fixture missing: {expected}')

if 'INSTITUIÇÃO DE ORIGEM TESTE'.casefold() in project.casefold():
    raise SystemExit('NBR 15287:2025: cover de research project used the institution instead of the submission entity.')

for forbidden in ('RESUMO', 'ABSTRACT', 'BANCA EXAMINADORA', 'APROVADA EM'):
    if forbidden.casefold() in project.casefold():
        raise SystemExit(f'NBR 15287:2025: element de work final apareceu no research project: {forbidden}')

if 'MARCADOR CAPA OPCIONAL'.casefold() in no_cover.casefold():
    raise SystemExit('NBR 15287:2025: cover optional foi impressa apesar de cover = false.')
if 'AUTOR SEM CAPA TESTE'.casefold() not in no_cover.casefold():
    raise SystemExit('NBR 15287:2025: title page required missing no research project sem cover.')

if 'AUTOR SIGILOSO TESTE'.casefold() in anon.casefold():
    raise SystemExit('research project anonymized: author vazou no PDF.')
if 'ORIENTADOR SIGILOSO TESTE'.casefold() in anon.casefold():
    raise SystemExit('research project anonymized: advisor vazou no PDF.')
if 'PROJETO-ANONIMO-001'.casefold() not in anon.casefold():
    raise SystemExit('research project anonymized: identifier público missing.')
PY
fi

for expected in 'Introdução' 'Referencial teórico' 'Metodologia' 'Recursos' 'Cronograma' 'Referências'; do
  grep -Fqi "$expected" research-project-15287.toc || {
    echo "NBR 15287:2025: item missing from the table of contents: $expected"
    cat research-project-15287.toc
    exit 1
  }
done

if grep -Eiq 'resumo|abstract|agradecimentos|dedicat[oó]ria|folha de aprova' research-project-15287.toc; then
  echo 'NBR 15287:2025: front-matter element invalid leaked into the table of contents do research project.'
  cat research-project-15287.toc
  exit 1
fi

python3 -m py_compile tests/checks/normative_research_project_structure.py
python3 tests/checks/normative_research_project_structure.py \
  research-project-15287.pdf \
  --json artifacts/normative-project/project-structure-final-pdf.json \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-unknown}}" \
  --enforce

echo 'Gate NBR 15287:2025 completed.'
