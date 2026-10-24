#!/bin/sh
# Actual-class longabnttblr evidence for IBGE 1993 §8.3, bounded to 4 scenarios.
set -eu

fixture="tests/documents/table-ibge-multipage-final-pdf.tex"
evidence_dir="artifacts/normative-layout/ibge-multipage"
tmp="$(mktemp -d)"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  for scenario in positive header-missing source-missing nonterminal-rule theme-override; do
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

for scenario in positive header-missing source-missing nonterminal-rule theme-override; do
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
    # The positive now uses the *default* public longabnttblr, unchanged in
    # source syntax, including the familiar literal body-level \bottomrule.
    # The class routes that closing line to the lastfoot template.
    if source.count(r"\bottomrule") != 1:
        raise SystemExit("IBGE §8.3(d): expected one original closing rule")
elif scenario == "theme-override":
    # Preserve the original body-level closing rule under an explicit theme.
    options = "[\n  caption="
    if source.count(options) != 1:
        raise SystemExit("IBGE theme override anchor drift")
    source = source.replace(options, "[\n  theme=abnt,\n  caption=")
elif scenario == "nonterminal-rule":
    # Negative control bypasses ONLY the class-owned compatibility adapter,
    # invoking the upstream public longtblr+abnt theme with a literal
    # \bottomrule. It must show intermediate repeated footer rules.
    start, end = r"\begin{longabnttblr}", r"\end{longabnttblr}"
    if source.count(start) != 1 or source.count(end) != 1:
        raise SystemExit("IBGE §8.3(d): original wrapper drift")
    source = source.replace(start, r"\begin{longtblr}")
    source = source.replace(end, r"\end{longtblr}")
    options = "[\n  caption="
    if source.count(options) != 1:
        raise SystemExit("IBGE §8.3(d): theme injection anchor drift")
    source = source.replace(options, "[\n  theme=abnt,\n  caption=")
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
  validation_scenario="$scenario"
  if [ "$scenario" = "theme-override" ]; then
    validation_scenario="nonterminal-rule"
  fi
  python3 tests/checks/objects/normative_table_ibge_multipage.py "$job.pdf" \
    --scenario "$validation_scenario" \
    --json "$evidence_dir/$job.json" \
    --commit-sha "$(git rev-parse HEAD)"
  if [ "$scenario" = "positive" ] || [ "$scenario" = "nonterminal-rule" ] || [ "$scenario" = "theme-override" ]; then
    python3 tests/checks/objects/normative_table_ibge_multipage_vector.py "$job.pdf" \
      --scenario "$validation_scenario" \
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


# Additional one-page regression for the public opt-in interface. Ensure
# source, note and a physical SVG footer separator survive without spilling.
short_job=ibge-optin-short-final-pdf
short_fixture=tests/documents/table-ibge-optin-short-final-pdf.tex
for pass in 1 2 3; do
  pdflatex -jobname="$short_job" $flags "$short_fixture" \
    > "$tmp/$short_job.log" 2>&1 || {
      cat "$tmp/$short_job.log"
      exit 1
    }
done
short_warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$short_job.log" |
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$short_warnings" ]; then
  printf '%s\n' "$short_warnings"
  echo "IBGE single-page opt-in: unexpected LaTeX warning or box overflow." >&2
  exit 1
fi
cp "$short_job.pdf" "$evidence_dir/$short_job.pdf"
PYTHONPATH=tools:tests/checks/objects python3 - "$short_job.pdf" "$evidence_dir/$short_job.json" <<'PY'
import hashlib
import json
from pathlib import Path
import sys
from pdf_measurement import bbox_pages, normalize
from pdf_vector_measurement import vector_rules
from normative_table_ibge_vector import cluster_axis_rules

pdf = Path(sys.argv[1])
pages = bbox_pages(pdf)
if len(pages) != 1:
    raise SystemExit(f"IBGE opt-in short table spilled: pages={len(pages)}")
page = pages[0]
def one(marker):
    found = [w for w in page.words if normalize(w.text) == marker]
    if len(found) != 1:
        raise SystemExit(f"IBGE opt-in short table marker {marker}: matches={len(found)}")
    return found[0]

header = one("UFCIBGESHORTHEAD")
right = one("UFCIBGESHORTVAL")
last_row = one("UFCIBGESHORTROW")
source = one("UFCIBGESHORTSOURCE")
note = one("UFCIBGESHORTNOTE")
one("UFCIBGESHORTCAP")
if not (header.box.y_max < last_row.box.y_min
        and last_row.box.y_max < source.box.y_min
        and source.box.y_max < note.box.y_min):
    raise SystemExit("IBGE opt-in short table has wrong heading/row/source/note order")
left_x, right_x = header.box.x_min, right.box.x_max
rules = cluster_axis_rules(
    vector_rules(pdf, page=page.index),
    orientation="horizontal", cluster_tolerance_pt=1.8
)
footer = [
    item for item in rules
    if item.length >= .78 * (right_x-left_x)
    and item.box.x_min <= left_x + 6
    and item.box.x_max >= right_x - 6
    and last_row.box.y_max + 1 <= item.box.center_y <= source.box.y_min - 1
]
if len(footer) != 1:
    raise SystemExit(f"IBGE opt-in short table expected one final rule: {len(footer)}")
report = {
    "component": "table-ibge-optin-single-page",
    "pdf_pages": 1,
    "final_rule_count": 1,
    "source_and_note_only_at_final": True,
    "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
    "source_commit_sha": __import__("subprocess").check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip(),
    "proof_state": "automatic-partial",
    "unrelated_normative_proof_promoted": False
}
Path(sys.argv[2]).write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
print("IBGE-OPTIN-SINGLE-PAGE-EVIDENCE status=PASS pages=1 "
      "lastfoot_rule=1 source_note_order=PASS proof_state=automatic-partial")
PY
rm -f "$short_job".aux "$short_job".log "$short_job".out \
  "$short_job".lot "$short_job".toc "$short_job".pdf


# Separate one-page actual-PDF scenario WITHOUT optional metadata. This
# catches accidental forwarding of xparse's NoValue sentinel into longtblr.
noopts_job=ibge-optin-no-options-final-pdf
noopts_fixture=tests/documents/table-ibge-optin-no-options-final-pdf.tex
for pass in 1 2 3; do
  pdflatex -jobname="$noopts_job" $flags "$noopts_fixture" \
    > "$tmp/$noopts_job.log" 2>&1 || {
      cat "$tmp/$noopts_job.log"
      exit 1
    }
done
noopts_warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$noopts_job.log" |
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$noopts_warnings" ]; then
  printf '%s\n' "$noopts_warnings"
  echo "IBGE opt-in without metadata: unexpected LaTeX warning or box overflow." >&2
  exit 1
fi
test -s "$noopts_job.pdf"
cp "$noopts_job.pdf" "$evidence_dir/$noopts_job.pdf"
PYTHONPATH=tools:tests/checks/objects python3 - "$noopts_job.pdf" "$evidence_dir/$noopts_job.json" <<'PY'
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from pdf_measurement import bbox_pages, normalize
from pdf_vector_measurement import vector_rules
from normative_table_ibge_vector import cluster_axis_rules

pdf = Path(sys.argv[1])
pages = bbox_pages(pdf)
if len(pages) != 1:
    raise SystemExit(f"IBGE optional-free PDF spilled to {len(pages)} pages")
page = pages[0]

def marker(name):
    words = [word for word in page.words if normalize(word.text) == name]
    if len(words) != 1:
        raise SystemExit(f"IBGE optional-free PDF marker {name}: {len(words)} occurrences")
    return words[0]

left = marker("UFCIBGENOOPTHEAD")
right = marker("UFCIBGENOOPTVAL")
row = marker("UFCIBGENOOPTROW")
if not (left.box.y_max < row.box.y_min and right.box.y_max < row.box.y_min):
    raise SystemExit("IBGE optional-free PDF header and data row order invalid")
width = right.box.x_max - left.box.x_min
if width < 90:
    raise SystemExit("IBGE optional-free PDF table width calibration too small")
rules = cluster_axis_rules(
    vector_rules(pdf, page=page.index),
    orientation="horizontal", cluster_tolerance_pt=1.8
)
final = [
    line for line in rules
    if line.length >= width * 0.78
    and line.box.x_min <= left.box.x_min + 6
    and line.box.x_max >= right.box.x_max - 6
    and line.box.center_y > row.box.y_max + 1
    and line.box.center_y < page.height - 15
]
if len(final) != 1:
    raise SystemExit(
        f"IBGE optional-free PDF expected exactly one closing vector line, got {len(final)}"
    )
report = {
    "component": "table-ibge-optin-no-optional-metadata",
    "pdf_pages": 1,
    "observed_final_rule_count": len(final),
    "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
    "source_commit_sha": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip(),
    "proof_state": "automatic-partial",
    "unrelated_normative_proof_promoted": False,
    "limits": [
        "Only the absent-optional-argument parser and a one-page vector footer are measured.",
        "No source or remarks were specified; semantic attribution is not evaluated."
    ],
}
Path(sys.argv[2]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(
    "IBGE-OPTIN-NO-OPTIONS-EVIDENCE status=PASS pages=1 "
    "final_rule=1 no_optional_metadata=SUPPORTED proof_state=automatic-partial"
)
PY
rm -f "$noopts_job".aux "$noopts_job".log "$noopts_job".out \
  "$noopts_job".lot "$noopts_job".toc "$noopts_job".pdf

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
    "optin_footer=CONTROLLED single_page=CONTROLLED no_options=CONTROLLED "
    "proof_state=automatic-partial"
)
PY
