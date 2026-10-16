#!/bin/sh
set -eu

fixture="tests/documents/table-ibge-vector-final-pdf.tex"
job="table-ibge-vector-final-pdf"
negative_job="table-ibge-vector-source-missing"
negative_fixture="/tmp/table-ibge-vector-source-missing.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.lot"
  rm -f "$negative_job.aux" "$negative_job.log" "$negative_job.out" "$negative_job.pdf" "$negative_job.lot"
  rm -f "$negative_fixture"
}
trap cleanup EXIT INT TERM

python3 -m py_compile tools/pdf_vector_measurement.py \
  tests/checks/objects/normative_vector_rule_validation.py \
  tests/checks/objects/normative_table_ibge_vector.py \
  tests/checks/objects/normative_table_ibge_text.py

sh tests/integration/objects/vector-rule-validation.sh

for pass in 1 2; do
  pdflatex -jobname="$job" $flags "$fixture" > "/tmp/$job.out" 2>&1 || {
    cat "/tmp/$job.out"
    exit 1
  }
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo "$job: unrecognized warning or overflow."
  exit 1
fi

python3 tests/checks/objects/normative_table_ibge_vector.py "$job.pdf" \
  --json artifacts/normative-layout/table-ibge-vector-final-pdf.json \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"


# IBGE §4.2/§4.10: validate actual PDF caption above table and attribution
# after last row. This does not establish universal IBGE conformity.
python3 tests/checks/objects/normative_table_ibge_text.py "$job.pdf" \
  --expect pass \
  --json artifacts/normative-layout/table-ibge-title-source-positive.json \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

# Generate and compile a genuine negative PDF lacking the source line.
python3 - "$fixture" "$negative_fixture" <<'PY'
from pathlib import Path
import sys
source = Path(sys.argv[1]).read_text(encoding="utf-8")
needle = "  remark{Fonte}={UFCIBGESRC Própria.},\n"
if source.count(needle) != 1:
    raise SystemExit("IBGE source-negative fixture insertion point drifted")
Path(sys.argv[2]).write_text(source.replace(needle, ""), encoding="utf-8")
PY
for pass in 1 2; do
  pdflatex -jobname="$negative_job" $flags "$negative_fixture" > "/tmp/$negative_job.out" 2>&1 || {
    cat "/tmp/$negative_job.out"
    exit 1
  }
done
negative_warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$negative_job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$negative_warnings" ]; then
  printf '%s\n' "$negative_warnings"
  echo "$negative_job: unexpected warning or overflow in negative PDF."
  exit 1
fi
python3 tests/checks/objects/normative_table_ibge_text.py "$negative_job.pdf" \
  --expect source-missing \
  --json artifacts/normative-layout/table-ibge-title-source-negative.json \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

# Keep the new conditional unit proof in the established IBGE object gate.
# Applicability is fixture-declared, never guessed for arbitrary PDFs.
sh tests/integration/objects/table-ibge-unit-evidence.sh

# Include conditional source/general/specific-note ordering in the same PDF gate.
sh tests/integration/objects/table-ibge-notes-evidence.sh

echo 'IBGE rendered title/source positive and negative PDF checks completed.'

echo 'IBGE table vector-geometry evidence gate completed.'
