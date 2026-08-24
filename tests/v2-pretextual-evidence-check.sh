#!/bin/sh
set -eu

fixture="tests/normativa/pretextual-oracle-dedication-epigraph.tex"
job="pretextual-oracle-dedication-epigraph"
evidence="artifacts/normative-pretextual/dedication-epigraph.json"

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
    "$fixture" > /tmp/abntexto-ufc-v2-pretextual-evidence.log 2>&1 || {
      cat /tmp/abntexto-ufc-v2-pretextual-evidence.log
      exit 1
    }
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Auditoria pré-textual falhou: warning ou overflow não reconhecido.'
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/pretextual_oracle.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Auditoria pré-textual falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate de evidência N6 para dedicatória e epígrafes concluído.'
