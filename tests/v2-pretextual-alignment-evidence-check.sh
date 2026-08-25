#!/bin/sh
set -eu

fixture="tests/normativa/pretextual-oracle-dedication-epigraph-alignment.tex"
job="pretextual-oracle-dedication-epigraph-alignment"
evidence="artifacts/normative-pretextual/dedication-epigraph-alignment.json"

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
    "$fixture" > /tmp/abntexto-ufc-v2-pretextual-alignment.log 2>&1 || {
      cat /tmp/abntexto-ufc-v2-pretextual-alignment.log
      exit 1
    }
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Auditoria de alinhamento pré-textual falhou: warning ou overflow não reconhecido.'
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_pretextual_alignment.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Auditoria de alinhamento pré-textual falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate de evidência N6 para alinhamento de dedicatória e epígrafes concluído.'
