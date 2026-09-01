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
  echo "Auditoria do filete de nota de rodapé falhou: warning ou overflow não reconhecido em $fixture."
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_footnote_separator.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Auditoria do filete de nota de rodapé falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate de evidência para o filete de nota de rodapé concluído.'
