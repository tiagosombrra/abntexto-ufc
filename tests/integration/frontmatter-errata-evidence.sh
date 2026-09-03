#!/bin/sh
set -eu

present_fixture="tests/documents/frontmatter-errata-present-test.tex"
absent_fixture="tests/documents/frontmatter-errata-absent-test.tex"
present_job="frontmatter-validation-errata-present"
absent_job="frontmatter-validation-errata-absent"
evidence="artifacts/frontmatter/errata.json"

cleanup() {
  for job in "$present_job" "$absent_job"; do
    rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc"
  done
}
trap cleanup EXIT INT TERM

compile_fixture() {
  fixture="$1"
  job="$2"
  log="/tmp/abntexto-ufc-${job}.log"

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
    echo "Audit for errata failed: unrecognized warning or overflow em $fixture."
    exit 1
  fi
}

compile_fixture "$present_fixture" "$present_job"
compile_fixture "$absent_fixture" "$absent_job"

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_frontmatter_errata.py \
  "$present_job.pdf" \
  "$absent_job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}" \
  --enforce

test -s "$evidence" || {
  echo 'Audit for errata failed: JSON evidence was not generated.'
  exit 1
}

echo 'Gate for evidence front matter for errata completed.'
