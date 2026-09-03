#!/bin/sh
set -eu

duplex_fixture="tests/documents/frontmatter-pagination-duplex-test.tex"
card_fixture="tests/documents/frontmatter-pagination-card-source-test.tex"
catalog_fixture="tests/documents/frontmatter-pagination-catalog-test.tex"

duplex_job="frontmatter-validation-pagination-duplex"
card_job="frontmatter-validation-pagination-card-source"
catalog_job="frontmatter-validation-pagination-catalog"
evidence="artifacts/frontmatter/pagination-transition.json"

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
  "$card_fixture" > /tmp/abntexto-ufc-pagination-card-source.log 2>&1 || {
    cat /tmp/abntexto-ufc-pagination-card-source.log
    exit 1
  }

compile_fixture() {
  fixture="$1"
  job="$2"
  log="/tmp/abntexto-ufc-${job}.log"

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
    echo "Pagination front matter audit failed: unrecognized warning or overflow in $fixture."
    exit 1
  fi
}

compile_fixture "$duplex_fixture" "$duplex_job"
compile_fixture "$catalog_fixture" "$catalog_job"

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_frontmatter_pagination.py \
  "$duplex_job.pdf" \
  "$catalog_job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Pagination front matter audit failed: JSON evidence was not generated.'
  exit 1
}

echo 'Evidence front matter for pagination/transição front matter gate completed.'
