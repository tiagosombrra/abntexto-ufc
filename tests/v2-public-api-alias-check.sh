#!/bin/sh
set -eu

fixture="tests/normativa/public-api-aliases.tex"
job="public-api-aliases"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf"
}
trap cleanup EXIT INT TERM

[ -f "$fixture" ] || {
  echo "B2R-B2 alias smoke fixture missing: $fixture"
  exit 1
}

pdflatex -jobname="$job" $flags "$fixture" > "/tmp/$job.out" 2>&1 || {
  cat "/tmp/$job.out"
  exit 1
}

grep -Fq 'N15-EVIDENCE B2R-B2-ALIASES PASS' "$job.log" || {
  cat "$job.log"
  echo 'B2R-B2 alias smoke evidence marker missing.'
  exit 1
}

echo 'N15-EVIDENCE b2r-b2-alias-smoke keys=65 status=PASS'
echo 'Canonical-English setup alias smoke passed.'
