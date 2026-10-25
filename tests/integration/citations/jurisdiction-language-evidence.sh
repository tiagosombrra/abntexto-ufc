#!/bin/sh
set -eu
# Compile real biblatex-abnt jurisdiction references with Biber in four
# selected document languages, not merely a catalog/source string grep.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT INT TERM
mkdir -p artifacts/bibliography
for locale in pt en es fr; do
  case "$locale" in
    pt) code=pt-BR ;;
    en) code=en-US ;;
    es) code=es-ES ;;
    fr) code=fr-FR ;;
  esac
  job="ufc-legal-date-$locale"
  cat > "$work/$job.tex" <<EOF
\\DocumentMetadata{lang=$code,pdfstandard=A-2b,pdfversion=1.7}
\\documentclass{abntexto-ufc}
\\ufcsetup{document-language=$locale,title={UFC legal locale fixture},author={UFC Test},location={Fortaleza},year={2026},coat-of-arms=false}
\\ufcAddBibliographyResource{tests/fixtures/i18n-jurisdiction.bib}
\\begin{document}
\\textual
\\section{UFC LEGAL LOCALE $locale}
\\nocite{ufc-jurisdiction-date}
\\ufcPrintReferences
\\end{document}
EOF
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -jobname="$job" -output-directory="$work" "$work/$job.tex" >"$work/$job.stdout" 2>&1 || {
      cat "$work/$job.stdout"
      echo "LEGAL-I18N-EVIDENCE status=FAIL phase=pdflatex-initial locale=$locale" >&2
      exit 1
    }
  biber --input-directory "$work" --output-directory "$work" "$job" >"$work/$job.biber-stdout" 2>&1 || {
    cat "$work/$job.biber-stdout"
    echo "LEGAL-I18N-EVIDENCE status=FAIL phase=biber locale=$locale" >&2
    exit 1
  }
  for pass in 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
      -jobname="$job" -output-directory="$work" "$work/$job.tex" >"$work/$job.stdout" 2>&1 || {
        cat "$work/$job.stdout"
        echo "LEGAL-I18N-EVIDENCE status=FAIL phase=pdflatex-$pass locale=$locale" >&2
        exit 1
      }
  done
  pdftotext -layout "$work/$job.pdf" "$work/$job.txt"
done
# Unmatched event date: suppress label rather than printing a fake judgment.
cat > "$work/ufc-legal-date-undated.tex" <<'EOF'
\DocumentMetadata{lang=pt-BR,pdfstandard=A-2b,pdfversion=1.7}
\documentclass{abntexto-ufc}
\ufcsetup{title={UFC undated fixture},author={UFC Test},location={Fortaleza},year={2026},coat-of-arms=false}
\ufcAddBibliographyResource{tests/fixtures/i18n-jurisdiction.bib}
\begin{document}
\textual
\section{UFC LEGAL NEGATIVE}
\nocite{ufc-jurisdiction-undated}
\ufcPrintReferences
\end{document}
EOF
job="ufc-legal-date-undated"
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname="$job" -output-directory="$work" "$work/$job.tex" >"$work/$job.stdout" 2>&1 || { cat "$work/$job.stdout"; exit 1; }
biber --input-directory "$work" --output-directory "$work" "$job" >"$work/$job.biber-stdout" 2>&1 || { cat "$work/$job.biber-stdout"; exit 1; }
for pass in 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname="$job" -output-directory="$work" "$work/$job.tex" >"$work/$job.stdout" 2>&1 || { cat "$work/$job.stdout"; exit 1; }
done
pdftotext -layout "$work/$job.pdf" "$work/$job.txt"
python3 - "$work" <<'PY'
import hashlib,json,re,sys,unicodedata
from pathlib import Path
root=Path(sys.argv[1])
labels={"pt":"julgado em","en":"judged on","es":"juzgado el","fr":"juge le"}
def fold(x):
    return re.sub(r"\s+"," ",''.join(ch for ch in unicodedata.normalize("NFKD",x.lower()) if not unicodedata.combining(ch))).strip()
results=[]
for locale,label in labels.items():
    p=root/f"ufc-legal-date-{locale}.pdf"
    text=fold((root/f"ufc-legal-date-{locale}.txt").read_text(encoding="utf-8"))
    if fold(label) not in text or "ufc legal date test decision" not in text:
        raise SystemExit(f"LEGAL-I18N-EVIDENCE status=FAIL locale={locale} missing_legal_date_label=true sample={text[:750]}")
    wrong={fold(v) for k,v in labels.items() if k!=locale}
    if any(w in text for w in wrong):
        raise SystemExit(f"LEGAL-I18N-EVIDENCE status=FAIL locale={locale} foreign_locale_leak=true")
    results.append({"locale":locale,"label":label,"pdf_sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
    print(f"LEGAL-I18N-EVIDENCE status=PASS locale={locale} label={label}",flush=True)
undated=fold((root/"ufc-legal-date-undated.txt").read_text(encoding="utf-8"))
if "ufc legal undated control" not in undated or "julgado em" in undated:
    raise SystemExit("LEGAL-I18N-EVIDENCE status=FAIL undated_negative")
manifest={"status":"AUTOMATED_PARTIAL","bibliography_driver":"jurisdiction","locales":results,"undated_negative":"PASS","human_terminology_review":"PENDING"}
Path("artifacts/bibliography/jurisdiction-language-evidence.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("LEGAL-I18N-EVIDENCE status=PASS languages=4 real_pdfs=5 biber=PASS undated_negative=PASS")
PY
