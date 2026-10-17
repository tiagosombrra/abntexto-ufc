#!/bin/sh
# Actual-class longabnttblr evidence for IBGE 1993 §8.3, bounded to 3 scenarios.
set -eu

fixture="tests/documents/table-ibge-multipage-final-pdf.tex"
evidence_dir="artifacts/normative-layout/ibge-multipage"
tmp="$(mktemp -d)"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  for scenario in positive header-missing source-missing; do
    job="ibge-multipage-$scenario"
    for ext in aux log out pdf lot toc; do
      rm -f "$job.$ext"
    done
  done
  rm -rf "$tmp"
}
trap cleanup EXIT INT TERM

python3 -m py_compile tests/checks/objects/normative_table_ibge_multipage.py

for scenario in positive header-missing source-missing; do
  job="ibge-multipage-$scenario"
  generated="$tmp/$job.tex"

  python3 - "$fixture" "$generated" "$scenario" <<'PY'
from pathlib import Path
import sys

source = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])
scenario = sys.argv[3]
anchor = "@UFC_ROWS@"
if source.count(anchor) != 1:
    raise SystemExit("IBGE §8.3: fixture's rows insertion anchor drifted")
if source.count(r"\begin{longabnttblr}") != 1:
    raise SystemExit("IBGE §8.3: multipage environment must remain longabnttblr")

rows = "\n".join(
    f"UFCIBGEMPROW{i:03d} & {i} " + chr(92) * 2
    for i in range(1, 169)
)
source = source.replace(anchor, rows)
if scenario == "header-missing":
    anchor = "  rowhead=1,"
    if source.count(anchor) != 1:
        raise SystemExit("IBGE §8.3: rowhead fixture drifted")
    source = source.replace(anchor, "  rowhead=0,")
elif scenario == "source-missing":
    anchor = "  remark{Fonte}={UFCIBGEMPSRC Elaboracao sintetica.},\n"
    if source.count(anchor) != 1:
        raise SystemExit("IBGE §8.3: source-removal fixture drifted")
    source = source.replace(anchor, "")
elif scenario != "positive":
    raise SystemExit("IBGE §8.3: unsupported fixture scenario")
out.write_text(source, encoding="utf-8")
PY

  echo "IBGE §8.3 actual PDF build: $scenario"
  for pass in 1 2 3; do
    pdflatex -jobname="$job" $flags "$generated" > "$tmp/$job.log" 2>&1 || {
      cat "$tmp/$job.log"
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" |
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "IBGE §8.3 $scenario: unexpected LaTeX warning or box overflow." >&2
    exit 1
  fi
  test -s "$job.pdf"
  mkdir -p "$evidence_dir"
  cp "$job.pdf" "$evidence_dir/$job.pdf"
  python3 tests/checks/objects/normative_table_ibge_multipage.py "$job.pdf" \
    --scenario "$scenario" \
    --json "$evidence_dir/$job.json" \
    --commit-sha "$(git rev-parse HEAD)"
done

python3 - "$evidence_dir" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

directory = Path(sys.argv[1])
names = ("positive", "header-missing", "source-missing")
records = [
    json.loads((directory / f"ibge-multipage-{name}.json").read_text(encoding="utf-8"))
    for name in names
]
if len({entry["pdf_sha256"] for entry in records}) != len(names):
    raise SystemExit("IBGE §8.3 evidence: PDF bytes are not distinct")
if len({entry["pdf_pages"] for entry in records}) < 1:
    raise SystemExit("IBGE §8.3 evidence: page-count observation missing")
if any(not entry["matches_declared_scenario"] for entry in records):
    raise SystemExit("IBGE §8.3 evidence: declared control case failed")
print(
    "IBGE-MULTIPAGE-PDF-EVIDENCE status=PASS "
    "real_pdfs=3 positive=1 negative=2 "
    "header_repeat=CONTROLLED continuation_labels=CONTROLLED "
    "source_notes_terminal=CONTROLLED proof_state=automatic-partial"
)
PY
