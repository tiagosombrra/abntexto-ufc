#!/bin/sh
set -eu

illustrations_fixture="tests/documents/frontmatter-list-illustrations-present-test.tex"
tables_fixture="tests/documents/frontmatter-list-tables-present-test.tex"
abbreviations_fixture="tests/documents/frontmatter-list-abbreviations-present-test.tex"
symbols_fixture="tests/documents/frontmatter-list-symbols-present-test.tex"
absent_fixture="tests/documents/frontmatter-lists-absent-test.tex"

illustrations_job="frontmatter-validation-list-illustrations-present"
tables_job="frontmatter-validation-list-tables-present"
abbreviations_job="frontmatter-validation-list-abbreviations-present"
symbols_job="frontmatter-validation-list-symbols-present"
absent_job="frontmatter-validation-lists-absent"
evidence="artifacts/frontmatter/optional-lists.json"
alignment_evidence="artifacts/layout/frontmatter-definition-lists.json"

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
    echo "Optional lists audit failed: unrecognized warning or overflow in $fixture."
    exit 1
  fi
}

compile_fixture "$illustrations_fixture" "$illustrations_job"
compile_fixture "$tables_fixture" "$tables_job"
compile_fixture "$abbreviations_fixture" "$abbreviations_job"
compile_fixture "$symbols_fixture" "$symbols_job"
compile_fixture "$absent_fixture" "$absent_job"

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_frontmatter_lists.py \
  "$illustrations_job.pdf" \
  "$tables_job.pdf" \
  "$abbreviations_job.pdf" \
  "$symbols_job.pdf" \
  "$absent_job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}" \
  --enforce

python3 tests/checks/frontmatter_definition_list_alignment.py \
  "$abbreviations_job.pdf" \
  "$symbols_job.pdf" \
  --json "$alignment_evidence"

test -s "$evidence" || {
  echo 'Optional lists audit failed: JSON evidence was not generated.'
  exit 1
}

test -s "$alignment_evidence" || {
  echo 'Optional lists audit failed: alignment evidence was not generated.'
  exit 1
}

echo 'Evidence front matter for lists front matter opcionais gate completed.'
