#!/bin/sh
set -eu

fixture="tests/documents/table-ibge-notes-final-pdf.tex"
tmp_dir="$(mktemp -d)"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  for scenario in both-present general-missing callout-missing not-applicable; do
    job="table-ibge-notes-$scenario"
    rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.lot"
  done
  rm -rf "$tmp_dir"
}
trap cleanup EXIT INT TERM

python3 -m py_compile tests/checks/objects/normative_table_ibge_notes.py

# Generate distinct negative controls from the positive source; fail closed
# whenever the original insertion points drift.
python3 - "$fixture" "$tmp_dir" <<'PY'
from pathlib import Path
import sys

source = Path(sys.argv[1]).read_text(encoding="utf-8")
dest = Path(sys.argv[2])
general = "  remark{Nota}={UFCIBGENOTEGEN Valores meramente ilustrativos.},\n"
specific = "  note{1}={UFCIBGENOTESPEC Valor estimado para a categoria.},\n"
callout = r"\TblrNote{1}"
for needle in (general, specific, callout):
    if source.count(needle) != 1:
        raise SystemExit(f"IBGE note fixture source drift: {needle!r}")
variants = {
    "general-missing": source.replace(general, ""),
    "callout-missing": source.replace(callout, ""),
    "not-applicable": source.replace(general, "").replace(specific, "").replace(callout, ""),
}
if len({source, *variants.values()}) != 4:
    raise SystemExit("IBGE note controlled variants must be distinct")
for scenario, content in variants.items():
    (dest / f"{scenario}.tex").write_text(content, encoding="utf-8")
PY

for scenario in both-present general-missing callout-missing not-applicable; do
  job="table-ibge-notes-$scenario"
  case "$scenario" in
    both-present) document="$fixture" ;;
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
    echo "$job: unexpected warning or overfull box."
    exit 1
  fi

  python3 tests/checks/objects/normative_table_ibge_notes.py "$job.pdf" \
    --expect "$scenario" \
    --json "artifacts/normative-layout/$job.json" \
    --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"
done

# Audit that the four PDF inputs are independently compiled outputs.
python3 - table-ibge-notes-both-present.pdf \
  table-ibge-notes-general-missing.pdf \
  table-ibge-notes-callout-missing.pdf \
  table-ibge-notes-not-applicable.pdf <<'PY'
import hashlib
from pathlib import Path
import sys

digests = [hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in sys.argv[1:]]
if len(set(digests)) != len(digests):
    raise SystemExit("IBGE note scenarios did not generate four distinct PDFs")
print("IBGE-NOTES-PDF-EVIDENCE independent_pdf_count=4")
PY
echo 'IBGE §§4.10-4.12 note order regression completed.'
