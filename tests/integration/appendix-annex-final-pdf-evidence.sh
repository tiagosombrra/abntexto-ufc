#!/bin/sh
set -eu

fixture="tests/documents/appendix-annex-final-pdf.tex"
job="appendix-annex-final-pdf"
evidence="artifacts/normative-posttextual/appendix-annex-final-pdf.json"
log="/tmp/abntexto-ufc-v2-appendix-annex-final-pdf.log"

cleanup() {
  rm -f "$job".aux "$job".log "$job".out "$job".pdf "$job".toc
}
trap cleanup EXIT INT TERM

cleanup
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
  echo 'Auditoria de apêndice/anexo falhou: warning ou overflow não reconhecido.'
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_appendix_annex.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Auditoria de apêndice/anexo falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate de evidência final-PDF para apêndice/anexo concluído.'
