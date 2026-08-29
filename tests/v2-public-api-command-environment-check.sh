#!/bin/sh
set -eu

fixture="tests/normativa/public-api-command-environment-aliases.tex"
job="public-api-command-environment-aliases"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf"
}
trap cleanup EXIT INT TERM

[ -f "$fixture" ] || {
  echo "B2R-B3 command/environment smoke fixture missing: $fixture"
  exit 1
}

pdflatex -jobname="$job" $flags "$fixture" > "/tmp/$job.out" 2>&1 || {
  cat "/tmp/$job.out"
  exit 1
}

grep -Fq 'N15-EVIDENCE B2R-B3-COMMAND-ENV PASS' "$job.log" || {
  cat "$job.log"
  echo 'B2R-B3 command/environment smoke evidence marker missing.'
  exit 1
}

echo 'N15-EVIDENCE b2r-b3-command-env-smoke commands=30 environments=5 status=PASS'
echo 'Canonical-English command/environment alias smoke passed.'
