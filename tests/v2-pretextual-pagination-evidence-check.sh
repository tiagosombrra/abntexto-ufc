#!/bin/sh
set -eu

duplex_fixture="tests/normativa/pretextual-oracle-pagination-duplex.tex"
card_fixture="tests/normativa/pretextual-oracle-pagination-card-source.tex"
catalog_fixture="tests/normativa/pretextual-oracle-pagination-catalog.tex"

duplex_job="pretextual-oracle-pagination-duplex"
card_job="pretextual-oracle-pagination-card-source"
catalog_job="pretextual-oracle-pagination-catalog"
evidence="artifacts/normative-pretextual/pagination-transition.json"

cleanup() {
  for job in "$duplex_job" "$card_job" "$catalog_job"; do
    rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc"
    rm -f "$job.loi" "$job.lof" "$job.lot" "$job.loq" "$job.logr"
  done
}
trap cleanup EXIT INT TERM

pdflatex \
  -jobname="$card_job" \
  -interaction=nonstopmode \
  -halt-on-error \
  -file-line-error \
  "$card_fixture" > /tmp/abntexto-ufc-v2-pagination-card-source.log 2>&1 || {
    cat /tmp/abntexto-ufc-v2-pagination-card-source.log
    exit 1
  }

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
    echo "Auditoria de paginação pré-textual falhou: warning ou overflow não reconhecido em $fixture."
    exit 1
  fi
}

compile_fixture "$duplex_fixture" "$duplex_job"
compile_fixture "$catalog_fixture" "$catalog_job"

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_pretextual_pagination.py \
  "$duplex_job.pdf" \
  "$catalog_job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Auditoria de paginação pré-textual falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate de evidência N6 para paginação/transição pré-textual concluído.'
