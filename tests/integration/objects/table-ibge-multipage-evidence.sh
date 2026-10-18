#!/bin/sh
# Actual-class longabnttblr evidence for IBGE 1993 §8.3, bounded to 3 scenarios.
set -eu

fixture="tests/documents/table-ibge-multipage-final-pdf.tex"
evidence_dir="artifacts/normative-layout/ibge-multipage"
tmp="$(mktemp -d)"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  for scenario in positive header-missing source-missing nonterminal-rule; do
    job="ibge-multipage-$scenario"
    for ext in aux log out pdf lot toc; do
      rm -f "$job.$ext"
    done
  done
  rm -rf "$tmp"
}
trap cleanup EXIT INT TERM

python3 -m py_compile tests/checks/objects/normative_table_ibge_multipage.py \
  tests/checks/objects/normative_table_ibge_multipage_vector.py

for scenario in positive header-missing source-missing nonterminal-rule; do
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
elif scenario == "positive":
    # The new public opt-in wrapper owns the concluding horizontal separator.
    # This is not a fixture-level internal theme mutation. Existing old
    # longabnttblr plus bottomrule remains the independent negative PDF.
    start = r"\begin{longabnttblr}"
    close = r"\end{longabnttblr}"
    for anchor, new in (
        (start, r"\begin{ufcibgelongtblr}"),
        (close, r"\end{ufcibgelongtblr}"),
    ):
        if source.count(anchor) != 1:
            raise SystemExit("IBGE §8.3(d): expected one wrapper environment anchor")
        source = source.replace(anchor, new)
    bottom = r"\bottomrule"
    if source.count(bottom) != 1:
        raise SystemExit("IBGE §8.3(d): original bottomrule fixture drifted")
    source = source.replace(bottom, "")
elif scenario == "nonterminal-rule":
    # Reproduce the actual upstream defect with unmodified class and theme:
    # tabularray reuses the body-level last \bottomrule on ALL split pages.
    # This PDF must still retain valid title/header/source and a valid final
    # rule, but fail §8.3(d) because earlier pages also show the separator.
    pass
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
  if [ "$scenario" = "positive" ] || [ "$scenario" = "nonterminal-rule" ]; then
    python3 tests/checks/objects/normative_table_ibge_multipage_vector.py "$job.pdf" \
      --scenario "$scenario" \
      --json "$evidence_dir/$job-vector.json" \
      --commit-sha "$(git rev-parse HEAD)"
  fi
done


# Opt-in misuse must fail at TeX compilation with an explicit class error,
# not silently emit a nonconforming repeated footer.
invalid="$tmp/ibge-multipage-optin-invalid.tex"
python3 - "$fixture" "$invalid" <<'PY'
from pathlib import Path
import sys

source = Path(sys.argv[1]).read_text(encoding="utf-8")
source = source.replace(
    r"\begin{longabnttblr}", r"\begin{ufcibgelongtblr}"
).replace(
    r"\end{longabnttblr}", r"\end{ufcibgelongtblr}"
)
if source.count("@UFC_ROWS@") != 1:
    raise SystemExit("IBGE invalid fixture marker drifted")
source = source.replace("@UFC_ROWS@", "\n".join(
    f"UFCIBGEMPROW{i:03d} & {i} " + chr(92) * 2 for i in range(1, 169)
))
out = Path(sys.argv[2])
out.write_text(source, encoding="utf-8")
PY
if pdflatex -jobname=ibge-multipage-optin-invalid $flags "$invalid" \
    > "$tmp/ibge-optin-invalid.log" 2>&1; then
  echo "IBGE §8.3(d): opt-in environment unexpectedly accepted body bottomrule." >&2
  exit 1
fi
grep -F 'ufcibgelongtblr' "$tmp/ibge-optin-invalid.log" >/dev/null
grep -F 'bottomrule' "$tmp/ibge-optin-invalid.log" >/dev/null
rm -f ibge-multipage-optin-invalid.aux ibge-multipage-optin-invalid.log \
  ibge-multipage-optin-invalid.pdf ibge-multipage-optin-invalid.out
echo "IBGE-MULTIPAGE-OPTIN-CONTRACT status=PASS body_bottomrule=REJECTED class_error=true"

python3 - "$evidence_dir" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

directory = Path(sys.argv[1])
names = ("positive", "header-missing", "source-missing", "nonterminal-rule")
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
    "real_pdfs=4 positive=1 negative=3 "
    "header_repeat=CONTROLLED continuation_labels=CONTROLLED "
    "source_notes_terminal=CONTROLLED footer_vector=CONTROLLED "
    "optin_footer=CONTROLLED "
    "proof_state=automatic-partial"
)
PY
