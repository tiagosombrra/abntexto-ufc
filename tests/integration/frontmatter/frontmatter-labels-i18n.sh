#!/bin/sh
set -eu

fixture=tests/documents/frontmatter-labels-i18n.tex
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT INT TERM
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

for lang in default pt en es fr; do
  case "$lang" in
    default) options='' ;;
    *) options="labels-language = $lang," ;;
  esac
  # A blank line inside \ufcsetup{...} expands to \par and becomes
  # part of the following l3keys key name ("ufc/\par coat-of-arms").
  # Delete the entire optional-only line for the implicit PT-default path.
  # Never replace the placeholder with empty text on its own line.
  if [ "$lang" = default ]; then
    sed '/^[[:space:]]*@UFC_LABELS_LANGUAGE@[[:space:]]*$/d' \
      "$fixture" > "$work/labels-$lang.tex"
    if grep -Fq 'labels-language' "$work/labels-$lang.tex"; then
      echo "I18N-LABELS-EVIDENCE status=FAIL default_locale_not_implicit=true" >&2
      exit 1
    fi
  else
    sed "s/@UFC_LABELS_LANGUAGE@/$options/" "$fixture" > "$work/labels-$lang.tex"
    if [ "$(grep -c 'labels-language' "$work/labels-$lang.tex")" -ne 1 ]; then
      echo "I18N-LABELS-EVIDENCE status=FAIL language=$lang locale_key_not_unique=true" >&2
      exit 1
    fi
  fi
  if grep -Fq '@UFC_LABELS_LANGUAGE@' "$work/labels-$lang.tex"; then
    echo "I18N-LABELS-EVIDENCE status=FAIL language=$lang placeholder_not_replaced=true" >&2
    exit 1
  fi
  job="ufc-labels-$lang"
  for pass in 1 2; do
    pdflatex -jobname="$job" -output-directory="$work" $flags \
      "$work/labels-$lang.tex" > "$work/$job.stdout" 2>&1 || {
        cat "$work/$job.stdout"
        echo "I18N-LABELS-EVIDENCE status=FAIL language=$lang compilation=FAIL" >&2
        exit 1
      }
  done
  test -s "$work/$job.pdf"
  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$work/$job.log" |
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "I18N-LABELS-EVIDENCE status=FAIL language=$lang warnings=true" >&2
    exit 1
  fi
  pdftotext -layout "$work/$job.pdf" "$work/$job.txt"
done

python3 - "$work" <<'PY'
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import unicodedata

work = Path(sys.argv[1])
names = (
    "acknowledgments", "errata", "illustrations", "figures", "tables",
    "text-tables", "abbreviations", "symbols", "contents",
)
languages = {
    "pt": (
        "Agradecimentos", "Errata", "Lista de Ilustrações",
        "Lista de Figuras", "Lista de Tabelas", "Lista de Quadros",
        "Lista de Abreviaturas e Siglas", "Lista de Símbolos", "Sumário"
    ),
    "en": (
        "Acknowledgments", "Errata", "List of Illustrations",
        "List of Figures", "List of Tables", "List of Text Tables",
        "List of Abbreviations and Acronyms", "List of Symbols", "Contents"
    ),
    "es": (
        "Agradecimientos", "Fe de erratas", "Lista de Ilustraciones",
        "Lista de Figuras", "Lista de Tablas", "Lista de Cuadros",
        "Lista de Abreviaturas y Siglas", "Lista de Símbolos", "Índice general"
    ),
    "fr": (
        "Remerciements", "Errata", "Liste des illustrations",
        "Liste des figures", "Liste des tableaux", "Liste des encadrés",
        "Liste des abréviations et sigles", "Liste des symboles",
        "Table des matières"
    ),
}

def norm(text):
    text = unicodedata.normalize("NFC", text)
    return re.sub(r"\s+", " ", text).strip().casefold()

def get_pages(pdf):
    raw = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    match = re.search(r"^Pages:\s+(\d+)", raw, re.MULTILINE)
    if not match:
        raise SystemExit("PDF page count unavailable")
    return int(match.group(1))

baseline = None
receipts = []
for lang in ("default", "pt", "en", "es", "fr"):
    pdf = work / f"ufc-labels-{lang}.pdf"
    txt = norm((work / f"ufc-labels-{lang}.txt").read_text(encoding="utf-8"))
    selected = "pt" if lang == "default" else lang
    expected = languages[selected]
    missing = [label for label in expected if norm(label) not in txt]
    if missing:
        raise SystemExit(f"I18N-LABELS-EVIDENCE language={lang} missing={missing}")
    for invariant in ("resumo", "abstract", "ufc i18n section"):
        if invariant not in txt:
            raise SystemExit(f"I18N-LABELS-EVIDENCE language={lang} lost={invariant}")
    if lang == "default":
        baseline = txt
    if lang == "pt" and txt != baseline:
        raise SystemExit("Explicit PT differs from implicit PT default")
    # A non-PT locale may still share terms such as Errata, but must not
    # accidentally show the *Portuguese-only* acknowledgments heading.
    if selected != "pt" and "agradecimentos" in txt:
        raise SystemExit(f"Non-Portuguese headings leaked PT at {lang}")
    receipt = {
        "locale": lang,
        "profile": "doctoral-thesis",
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "pdf_pages": get_pages(pdf),
        "headings_checked": list(names),
        "portuguese_summary_preserved": True,
        "english_abstract_preserved": True,
        "proof_state": "experimental-display-only",
    }
    receipts.append(receipt)
    print(
        f"I18N-LABELS-EVIDENCE status=PASS language={lang} "
        f"headings=9 summary=PT abstract=EN pdf_pages={receipt['pdf_pages']}"
    )

report = {
    "component": "frontmatter-display-heading-i18n",
    "source_commit_sha": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip(),
    "default_legacy_pt_unchanged": True,
    "locale_coverage": list(languages),
    "full_manuscript_translation_certified": False,
    "normative_rule_promotion": False,
    "receipts": receipts,
}
output = Path("artifacts/frontmatter/labels-i18n.json")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

# l3keys choice validator is the negative control for unsupported locales.
sed 's/@UFC_LABELS_LANGUAGE@/labels-language = de,/' "$fixture" > "$work/labels-invalid.tex"
if pdflatex -jobname=ufc-labels-invalid -output-directory="$work" $flags \
    "$work/labels-invalid.tex" > "$work/invalid.stdout" 2>&1; then
  echo "I18N-LABELS-EVIDENCE status=FAIL unsupported_language_accepted=true" >&2
  exit 1
fi
grep -F 'labels-language' "$work/invalid.stdout" >/dev/null || {
  cat "$work/invalid.stdout"
  echo "I18N-LABELS-EVIDENCE status=FAIL wrong_invalid_error=true" >&2
  exit 1
}
echo 'I18N-LABELS-EVIDENCE status=PASS languages=pt,en,es,fr default=pt invalid=REJECTED scope=display-only'
