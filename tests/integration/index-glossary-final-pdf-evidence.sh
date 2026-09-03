#!/bin/sh
set -eu

present_fixture="tests/documents/index-glossary-present-final-pdf.tex"
absent_fixture="tests/documents/index-glossary-absent-final-pdf.tex"
present_job="index-glossary-present-final-pdf"
absent_job="index-glossary-absent-final-pdf"
evidence="artifacts/normative-posttextual/index-glossary-final-pdf.json"
log="/tmp/abntexto-ufc-v2-index-glossary.log"

cleanup_job() {
  job="$1"
  rm -f "$job".aux "$job".glg "$job".glo "$job".gls "$job".idx \
        "$job".ilg "$job".ind "$job".ist "$job".log "$job".out \
        "$job".pdf "$job".toc
}

cleanup() {
  cleanup_job "$present_job"
  cleanup_job "$absent_job"
}
trap cleanup EXIT INT TERM

check_log() {
  job="$1"
  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Audit for index/glossary failed: $job contains unrecognized warning or overflow."
    exit 1
  fi
}

cleanup

lualatex -jobname="$present_job" -interaction=nonstopmode -halt-on-error -file-line-error \
  "$present_fixture" > "$log" 2>&1 || { cat "$log"; exit 1; }
makeglossaries "$present_job" > /tmp/abntexto-ufc-v2-index-glossary-glossary.log 2>&1 || {
  cat /tmp/abntexto-ufc-v2-index-glossary-glossary.log
  exit 1
}
makeindex "$present_job" > /tmp/abntexto-ufc-v2-index-glossary-index.log 2>&1 || {
  cat /tmp/abntexto-ufc-v2-index-glossary-index.log
  exit 1
}
for pass in 1 2; do
  lualatex -jobname="$present_job" -interaction=nonstopmode -halt-on-error -file-line-error \
    "$present_fixture" > "$log" 2>&1 || { cat "$log"; exit 1; }
done
check_log "$present_job"

lualatex -jobname="$absent_job" -interaction=nonstopmode -halt-on-error -file-line-error \
  "$absent_fixture" > "$log" 2>&1 || { cat "$log"; exit 1; }
makeindex "$absent_job" > /tmp/abntexto-ufc-v2-index-glossary-index.log 2>&1 || {
  cat /tmp/abntexto-ufc-v2-index-glossary-index.log
  exit 1
}
for pass in 1 2; do
  lualatex -jobname="$absent_job" -interaction=nonstopmode -halt-on-error -file-line-error \
    "$absent_fixture" > "$log" 2>&1 || { cat "$log"; exit 1; }
done
check_log "$absent_job"

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_index_glossary.py \
  "$present_job.pdf" "$absent_job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Audit for index/glossary failed: JSON evidence was not generated.'
  exit 1
}

echo 'Gate for evidence final-PDF for index/glossary completed.'
