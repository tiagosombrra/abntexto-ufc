#!/bin/sh
set -eu

fixture="tests/normativa/textual-oracle-section-primary-recto-duplex.tex"
job="textual-oracle-section-primary-recto-duplex"
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
  echo "Auditoria de início de seção primária em anverso falhou: warning ou overflow não reconhecido em $fixture."
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_section_primary_recto_duplex.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Auditoria de início de seção primária em anverso falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate de evidência N6 para início de seção primária em anverso concluído.'
