#!/bin/sh
set -eu

fixture="tests/normativa/pdf-oracle-core.tex"
job="pdf-oracle-core"
evidence="artifacts/normative-oracle/core.json"

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
    "$fixture" > /tmp/abntexto-ufc-v2-pdf-oracle-core.log 2>&1 || {
      cat /tmp/abntexto-ufc-v2-pdf-oracle-core.log
      exit 1
    }
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'PDF oracle core falhou: warning ou overflow não reconhecido.'
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/pdf_oracle_core.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'PDF oracle core falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate N5 do núcleo do oracle PDF concluído.'
