#!/bin/sh
set -eu

fixture="tests/documents/mainmatter-footnote-separator-test.tex"
job="validation-footnote-separator"
evidence="artifacts/normative-layout/footnote-separator.json"
log="/tmp/abntexto-ufc-v2-footnote-separator.log"

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
  echo "Filete of footnote audit failed: unrecognized warning or overflow in $fixture."
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_footnote_separator.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Filete of footnote audit failed: JSON evidence was not generated.'
  exit 1
}

echo 'Evidence for o filete of footnote gate completed.'
