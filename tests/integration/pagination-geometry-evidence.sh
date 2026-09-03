#!/bin/sh
set -eu

fixture="tests/documents/mainmatter-pagination-geometry-test.tex"
job="validation-pagination-geometry"
evidence="artifacts/normative-layout/pagination-geometry.json"
log="/tmp/abntexto-ufc-v2-pagination-geometry.log"

cleanup() {
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc"
}
trap cleanup EXIT INT TERM

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
  echo "Pagination audit failed: unrecognized warning or overflow in $fixture."
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_pagination_geometry.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Pagination audit failed: JSON evidence was not generated.'
  exit 1
}

echo 'Evidence for pagination geometry gate completed.'
