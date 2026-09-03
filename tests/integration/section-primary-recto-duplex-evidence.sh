#!/bin/sh
set -eu

fixture="tests/documents/mainmatter-section-primary-recto-duplex-test.tex"
job="validation-section-primary-recto-duplex"
evidence="artifacts/normative-textual/section-primary-recto-duplex.json"
log="/tmp/abntexto-ufc-v2-section-primary-recto-duplex.log"

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
  echo "Audit for início de primary section em recto failed: unrecognized warning or overflow em $fixture."
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_section_primary_recto_duplex.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Audit for início de primary section em recto failed: JSON evidence was not generated.'
  exit 1
}

echo 'Gate for evidence for início de primary section em recto completed.'
