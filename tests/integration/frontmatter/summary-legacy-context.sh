#!/bin/sh
set -eu
# Positive + negative PDF evidence for the two legacy keyword macros INSIDE
# the opt-in multilingual summary. PT/EN legacy methods outside remain intact.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT INT TERM
mkdir -p artifacts/frontmatter
python3 - "$work" <<'PY'
from pathlib import Path
import sys
w = Path(sys.argv[1])
langs = {"pt":"pt-BR","en":"en-US","es":"es-ES","fr":"fr-FR"}
for locale, bcp in langs.items():
    for helper in ("ufcSummaryKeywords","keywords"):
        job = f"summary-legacy-{locale}-{helper}"
        content = w / (job+"-body.tex")
        content.write_text(
            f"KEYWORD-CONTEXT-CONTENT-{locale.upper()}-{helper.upper()}. "
            + "\\" + helper + "{keyword-" + locale + "-" + helper + ".}",
            encoding="utf-8"
        )
        tex = rf"""
\DocumentMetadata{{lang={bcp},pdfstandard=A-2b,pdfversion=1.7}}
\documentclass{{abntexto-ufc}}
\ufcsetup{{
  type=doctoral-thesis,document-language={locale},cover=false,
  catalog-card=false,coat-of-arms=false,title={{Test Summary Context}},
  author={{Test Author}},institution={{Universidade Federal do Ceará}},
  doctoral-graduate-program={{Test Program}},doctoral-degree-field={{Computing}}
}}
\begin{{document}}
\pretextual
\ufcPrintSummaryInLanguage{{{locale}}}{{{content}}}
\textual
\section{{CONTEXT-BODY-{locale.upper()}}}
\end{{document}}
"""
        (w/(job+".tex")).write_text(tex, encoding="utf-8")
# Non-opt-in legacy macros keep their semantic labels, irrespective of any
# later opt-in summary helper definition elsewhere in the class source.
legacy = r"""
\DocumentMetadata{lang=pt-BR,pdfstandard=A-2b,pdfversion=1.7}
\documentclass{abntexto-ufc}
\ufcsetup{type=doctoral-thesis,cover=false,coat-of-arms=false,title={Legacy},author={Test}}
\begin{document}
\pretextual
\ufcPrintSummary{TEST/legacy-pt-body.tex}
\ufcPrintAbstract{TEST/legacy-en-body.tex}
\textual
\section{LEGACY-CONTEXT}
\end{document}
"""
(w/"legacy-pt-body.tex").write_text(r"LEGACY-PT-CONTENT. \ufcSummaryKeywords{original.}",encoding="utf-8")
(w/"legacy-en-body.tex").write_text(r"LEGACY-EN-CONTENT. \keywords{original.}",encoding="utf-8")
(w/"summary-legacy-default.tex").write_text(legacy.replace("TEST/legacy",str(w)+"/legacy"),encoding="utf-8")
PY
for locale in pt en es fr; do
  for helper in ufcSummaryKeywords keywords; do
    job="summary-legacy-$locale-$helper"
    for pass in 1 2; do
      pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
        -jobname="$job" -output-directory="$work" "$work/$job.tex" > "$work/$job.stdout" 2>&1 || {
          cat "$work/$job.stdout"
          echo "SUMMARY-LEGACY-CONTEXT status=FAIL case=$job pass=$pass" >&2
          exit 1
        }
    done
    pdftotext -layout "$work/$job.pdf" "$work/$job.txt"
  done
done
job=summary-legacy-default
for pass in 1 2; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -jobname="$job" -output-directory="$work" "$work/$job.tex" > "$work/$job.stdout" 2>&1 || {
      cat "$work/$job.stdout"
      echo "SUMMARY-LEGACY-CONTEXT status=FAIL legacy_baseline pass=$pass" >&2
      exit 1
    }
done
pdftotext -layout "$work/$job.pdf" "$work/$job.txt"
python3 - "$work" <<'PY'
import hashlib,json,re,sys,unicodedata
from pathlib import Path
w=Path(sys.argv[1])
labels={"pt":"Palavras-chave:","en":"Keywords:","es":"Palabras clave:","fr":"Mots-clés:"}
titles={"pt":"RESUMO","en":"ABSTRACT","es":"RESUMEN","fr":"RÉSUMÉ"}
def fold(x):
    return re.sub(r"\s+"," ",''.join(c for c in unicodedata.normalize("NFKD",x).casefold() if not unicodedata.combining(c))).strip()
data=[]
for locale in labels:
    for helper in ("ufcSummaryKeywords","keywords"):
        job=f"summary-legacy-{locale}-{helper}"
        t=fold((w/(job+".txt")).read_text(encoding="utf-8"))
        expected=fold(labels[locale])
        marker=f"keyword-{locale}-{helper}".lower()
        if expected not in t or marker not in t or fold(titles[locale]) not in t:
            raise SystemExit(f"SUMMARY-LEGACY-CONTEXT status=FAIL locale={locale} helper={helper} expected={expected} excerpt={t[:400]}")
        forbidden={fold(lab) for lang,lab in labels.items() if lang!=locale}
        if any(lab in t for lab in forbidden):
            raise SystemExit(f"SUMMARY-LEGACY-CONTEXT status=FAIL wrong_locale={locale} helper={helper}")
        pdf=w/(job+".pdf")
        data.append({"locale":locale,"legacy_helper":helper,"pdf_sha256":hashlib.sha256(pdf.read_bytes()).hexdigest()})
        print(f"SUMMARY-LEGACY-CONTEXT status=PASS locale={locale} helper={helper} pdf=true",flush=True)
legacy=fold((w/"summary-legacy-default.txt").read_text(encoding="utf-8"))
for needed in ("resumo","abstract","palavras-chave:","keywords:","legacy-pt-content","legacy-en-content"):
    if fold(needed) not in legacy:
        raise SystemExit(f"SUMMARY-LEGACY-CONTEXT status=FAIL pt_en_baseline={needed}")
Path("artifacts/frontmatter/summary-legacy-context.json").write_text(json.dumps({
 "status":"AUTOMATED_PARTIAL","positive_count":len(data),"legacy_default":"PASS",
 "old_commands_outside_explicit_locale":"UNCHANGED","examples":data,
 "scope":"summary keyword label only; author wording not translated"
},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("SUMMARY-LEGACY-CONTEXT status=PASS locales=4 helpers=2 real_pdfs=9 legacy_pt_en=PASS")
PY
