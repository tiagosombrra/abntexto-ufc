#!/bin/sh
set -eu

fixture="tests/documents/frontmatter-dedication-epigraph-alignment-test.tex"
job="frontmatter-validation-dedication-epigraph-alignment"
evidence="artifacts/frontmatter/dedication-epigraph-alignment.json"

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
    "$fixture" > /tmp/abntexto-ufc-frontmatter-alignment.log 2>&1 || {
      cat /tmp/abntexto-ufc-frontmatter-alignment.log
      exit 1
    }
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Audit for alinhamento front matter failed: unrecognized warning or overflow.'
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_frontmatter_alignment.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}" \
  --enforce

test -s "$evidence" || {
  echo 'Audit for alinhamento front matter failed: JSON evidence was not generated.'
  exit 1
}

echo 'Gate for evidence front matter for alinhamento de dedication and epigraphs completed.'
