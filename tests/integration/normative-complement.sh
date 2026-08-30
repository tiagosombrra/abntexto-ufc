#!/bin/sh
set -eu

fixture="tests/documents/normative-complement.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f normative-complement-*.aux normative-complement-*.log \
    normative-complement-*.out normative-complement-*.pdf \
    normative-complement-*.toc
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  job="normative-complement-$engine"
  log="/tmp/abntexto-ufc-normative-complement-$engine.log"
  echo "Validating complementary normative structures with $engine..."

  for pass in 1 2 3; do
    "$engine" -jobname="$job" $flags "$fixture" > "$log" 2>&1 || {
      cat "$log"
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

  python3 - "$job.log" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")


def value(name: str, unit: bool = False) -> float:
    suffix = r"pt" if unit else ""
    match = re.search(rf"{re.escape(name)}=([0-9.]+){suffix}", text)
    if not match:
        raise SystemExit(f"missing metric: {name}")
    return float(match.group(1))


def close(name: str, actual: float, expected: float, tolerance: float = 0.06) -> None:
    if abs(actual - expected) > tolerance:
        raise SystemExit(f"{name}: expected {expected:.4f}, observed {actual:.4f}")


pt_per_bp = 72.27 / 72.0
pt_per_cm = 72.27 / 2.54
close("long-quotation indentation", value("UFC-LONGQUOTE-HANG", True), 4.0 * pt_per_cm)
close("long-quotation font size", value("UFC-LONGQUOTE-FONTSIZE"), 10.0 * pt_per_bp)
close("long-quotation single spacing", value("UFC-LONGQUOTE-BASELINE", True), 11.5 * pt_per_bp)
PY

  if command -v pdftotext >/dev/null 2>&1; then
    pdftotext -layout "$job.pdf" "/tmp/$job.txt"
    python3 - "/tmp/$job.txt" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

raw = Path(sys.argv[1]).read_text(encoding="utf-8")
text = re.sub(r"\s+", " ", unicodedata.normalize("NFC", raw)).strip()
fold = text.casefold()

# These Portuguese strings are academic fixture payloads, not engineering identifiers.
for marker in (
    "citação direta longa de validação normativa",
    "alínea normativa de primeiro nível",
    "subalínea normativa de segundo nível",
    "conteúdo do apêndice complementar",
    "conteúdo do anexo complementar",
    "referência específica do anexo apresentada no próprio anexo",
):
    if marker.casefold() not in fold:
        raise SystemExit(f"expected academic fixture content is missing from the PDF: {marker}")

if not re.search(r"\ba\)\s+Alínea normativa de primeiro nível", text, re.IGNORECASE):
    raise SystemExit("first-level lettered item did not receive the expected alphabetic label")
if "APÊNDICE A".casefold() not in fold:
    raise SystemExit("appendix identifier is missing")
if "ANEXO A".casefold() not in fold:
    raise SystemExit("annex identifier is missing")
if not re.search(r"Equação\s+1", text, re.IGNORECASE):
    raise SystemExit("numbered-equation reference was not resolved")
if "(1)" not in text:
    raise SystemExit("equation number is missing")
PY
  fi
done

# Keep the deeper long-quotation evidence as part of this complementary-structure gate.
sh tests/integration/long-quotation-evidence.sh

echo 'NORMATIVE-COMPLEMENT-GATE status=PASS'
