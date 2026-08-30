#!/bin/sh
set -eu

fixture="tests/documents/mainmatter-section-unnumbered-centered-test.tex"
job="textual-oracle-section-unnumbered-centered"
evidence="artifacts/normative-textual/section-unnumbered-centered.json"
latex_log="/tmp/abntexto-ufc-v2-section-unnumbered-centered.log"
biber_log="/tmp/abntexto-ufc-v2-section-unnumbered-centered-biber.log"

cleanup() {
  rm -f "$job.aux" "$job.bbl" "$job.bcf" "$job.blg" "$job.log" \
        "$job.out" "$job.pdf" "$job.run.xml" "$job.toc"
}
trap cleanup EXIT INT TERM

pdflatex \
  -jobname="$job" \
  -interaction=nonstopmode \
  -halt-on-error \
  -file-line-error \
  "$fixture" > "$latex_log" 2>&1 || {
    cat "$latex_log"
    exit 1
  }

biber "$job" > "$biber_log" 2>&1 || {
  cat "$biber_log"
  exit 1
}

for pass in 1 2; do
  pdflatex \
    -jobname="$job" \
    -interaction=nonstopmode \
    -halt-on-error \
    -file-line-error \
    "$fixture" > "$latex_log" 2>&1 || {
      cat "$latex_log"
      exit 1
    }
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo "Auditoria de centralização de títulos sem indicativo falhou: warning ou overflow não reconhecido em $fixture."
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_section_unnumbered_centered.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Auditoria de centralização de títulos sem indicativo falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate de evidência N6 para centralização de títulos sem indicativo concluído.'
