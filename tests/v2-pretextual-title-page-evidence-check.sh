#!/bin/sh
set -eu

academic_fixture="tests/normativa/pretextual-oracle-title-page-academic.tex"
project_fixture="tests/normativa/pretextual-oracle-title-page-project.tex"
anonymized_fixture="tests/normativa/pretextual-oracle-title-page-project-anonymized.tex"
academic_job="pretextual-oracle-title-page-academic"
project_job="pretextual-oracle-title-page-project"
anonymized_job="pretextual-oracle-title-page-project-anonymized"
evidence="artifacts/normative-pretextual/title-page.json"

cleanup() {
  for job in "$academic_job" "$project_job" "$anonymized_job"; do
    rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc"
  done
}
trap cleanup EXIT INT TERM

compile_fixture() {
  fixture="$1"
  job="$2"
  log="/tmp/abntexto-ufc-v2-${job}.log"

  for pass in 1 2; do
    pdflatex \
      -jobname="$job" \
      -interaction=nonstopmode \
      -halt-on-error \
      -file-line-error \
      "$fixture" > "$log" 2>&1 || {
        cat "$log"
        exit 1
      }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Auditoria de folha de rosto falhou: warning ou overflow não reconhecido em $fixture."
    exit 1
  fi
}

compile_fixture "$academic_fixture" "$academic_job"
compile_fixture "$project_fixture" "$project_job"
compile_fixture "$anonymized_fixture" "$anonymized_job"

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_pretextual_title_page.py \
  "$academic_job.pdf" \
  "$project_job.pdf" \
  "$anonymized_job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Auditoria de folha de rosto falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate de evidência N6 para folha de rosto concluído.'
