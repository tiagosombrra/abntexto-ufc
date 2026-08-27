#!/bin/sh
set -eu

illustrations_fixture="tests/normativa/pretextual-oracle-list-illustrations-present.tex"
tables_fixture="tests/normativa/pretextual-oracle-list-tables-present.tex"
abbreviations_fixture="tests/normativa/pretextual-oracle-list-abbreviations-present.tex"
symbols_fixture="tests/normativa/pretextual-oracle-list-symbols-present.tex"
absent_fixture="tests/normativa/pretextual-oracle-lists-absent.tex"

illustrations_job="pretextual-oracle-list-illustrations-present"
tables_job="pretextual-oracle-list-tables-present"
abbreviations_job="pretextual-oracle-list-abbreviations-present"
symbols_job="pretextual-oracle-list-symbols-present"
absent_job="pretextual-oracle-lists-absent"
evidence="artifacts/normative-pretextual/optional-lists.json"
alignment_evidence="artifacts/layout/pretextual-definition-lists.json"

cleanup() {
  for job in \
    "$illustrations_job" \
    "$tables_job" \
    "$abbreviations_job" \
    "$symbols_job" \
    "$absent_job"; do
    rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc"
    rm -f "$job.loi" "$job.lof" "$job.lot" "$job.loq" "$job.logr"
  done
}
trap cleanup EXIT INT TERM

compile_fixture() {
  fixture="$1"
  job="$2"
  log="/tmp/abntexto-ufc-v2-${job}.log"

  for pass in 1 2 3; do
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
    echo "Auditoria de listas opcionais falhou: warning ou overflow não reconhecido em $fixture."
    exit 1
  fi
}

compile_fixture "$illustrations_fixture" "$illustrations_job"
compile_fixture "$tables_fixture" "$tables_job"
compile_fixture "$abbreviations_fixture" "$abbreviations_job"
compile_fixture "$symbols_fixture" "$symbols_job"
compile_fixture "$absent_fixture" "$absent_job"

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_pretextual_lists.py \
  "$illustrations_job.pdf" \
  "$tables_job.pdf" \
  "$abbreviations_job.pdf" \
  "$symbols_job.pdf" \
  "$absent_job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

python3 tests/checks/pretextual_definition_list_alignment.py \
  "$abbreviations_job.pdf" \
  "$symbols_job.pdf" \
  --json "$alignment_evidence"

test -s "$evidence" || {
  echo 'Auditoria de listas opcionais falhou: evidência JSON não foi gerada.'
  exit 1
}

test -s "$alignment_evidence" || {
  echo 'Auditoria de listas opcionais falhou: evidência de alinhamento não foi gerada.'
  exit 1
}

echo 'Gate de evidência N6 para listas pré-textuais opcionais concluído.'
