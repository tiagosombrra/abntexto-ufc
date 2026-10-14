#!/bin/sh
set -eu

fixture="tests/documents/table-ibge-unit-final-pdf.tex"
tmp_dir="$(mktemp -d)"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  for scenario in unit-present required-missing not-applicable; do
    job="table-ibge-unit-$scenario"
    rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.lot"
  done
  rm -rf "$tmp_dir"
}
trap cleanup EXIT INT TERM

python3 -m py_compile tests/checks/objects/normative_table_ibge_unit.py

# Derive a missing-required-unit negative and a separate conditional N/A case.
# The negative PDF intentionally mentions (kg) only in its SOURCE, proving
# that unrelated mentions cannot satisfy the column-header requirement.
python3 - "$fixture" "$tmp_dir/required-missing.tex" "$tmp_dir/not-applicable.tex" <<'PY'
from pathlib import Path
import sys

source = Path(sys.argv[1]).read_text(encoding="utf-8")
unit = r"UFCIBGEUNITHEAD \quad (kg)"
title = "UFCIBGEUNITCAP Massa observada"
source_label = "UFCIBGEUNITSRC Dados sintéticos."
for needle in (unit, title, source_label):
    if source.count(needle) != 1:
        raise SystemExit(f"IBGE conditional-unit fixture drift: {needle!r}")

missing = source.replace(unit, "UFCIBGEUNITHEAD").replace(
    source_label, "UFCIBGEUNITSRC Dados sintéticos (kg)."
)
not_applicable = source.replace(unit, "UFCIBGEUNITHEAD").replace(
    title, "UFCIBGEUNITCAP Contagem de eventos"
).replace(
    source_label, "UFCIBGEUNITSRC Contagens sintéticas."
)
if len({source, missing, not_applicable}) != 3:
    raise SystemExit("IBGE conditional-unit scenarios are not distinct")
Path(sys.argv[2]).write_text(missing, encoding="utf-8")
Path(sys.argv[3]).write_text(not_applicable, encoding="utf-8")
PY

for scenario in unit-present required-missing not-applicable; do
  job="table-ibge-unit-$scenario"
  case "$scenario" in
    unit-present) document="$fixture" ;;
    *) document="$tmp_dir/$scenario.tex" ;;
  esac

  for pass in 1 2; do
    pdflatex -jobname="$job" $flags "$document" > "$job.out" 2>&1 || {
      cat "$job.out"
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" |
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "$job: unexpected LaTeX warning or overflow."
    exit 1
  fi

  python3 tests/checks/objects/normative_table_ibge_unit.py "$job.pdf" \
    --expect "$scenario" \
    --json "artifacts/normative-layout/$job.json" \
    --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"
done

# Require genuinely different compiled PDFs, not just different CLI labels.
python3 - table-ibge-unit-unit-present.pdf \
  table-ibge-unit-required-missing.pdf \
  table-ibge-unit-not-applicable.pdf <<'PY'
import hashlib
from pathlib import Path
import sys

digests = [hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in sys.argv[1:]]
if len(set(digests)) != len(digests):
    raise SystemExit("IBGE conditional-unit PDF scenarios have identical bytes")
print("IBGE-TABLE-UNIT-EVIDENCE distinct_compiled_pdfs=3 scenarios=3")
PY

echo 'IBGE §4.6 controlled conditional-unit PDF evidence gate completed.'
