#!/bin/sh
set -eu
# Verify actual inherited upstream labels in rendered PDFs, including legacy PT.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT INT TERM
python3 - "$work" <<'PY'
from pathlib import Path
import sys
work = Path(sys.argv[1])
langs = {"legacy":"pt-BR", "pt":"pt-BR", "en":"en-US",
         "es":"es-ES", "fr":"fr-FR"}
for locale, meta in langs.items():
    opt = "" if locale == "legacy" else f"document-language={locale},"
    tex = rf"""
\DocumentMetadata{{lang={meta},pdfstandard=A-2b,pdfversion=1.7}}
\documentclass{{abntexto-ufc}}
\ufcsetup{{type=doctoral-thesis,{opt}author={{Test Author}},
 title={{Object Labels Test}},institution={{Universidade Federal do Ceará}},
 doctoral-graduate-program={{Computing}},doctoral-degree-field={{Computing}},
 coat-of-arms=false,cover=false,catalog-card=false}}
\begin{{document}}
\textual
\section{{BODY-OBJECT-{locale.upper()}}}
\appendix{{APPENDIX-OBJECT-{locale.upper()}}}
\annex{{ANNEX-OBJECT-{locale.upper()}}}
\legend{{figure}}{{OBJECT-CAPTION-{locale.upper()}}}
\ufcSource{{OBJECT-SOURCE-{locale.upper()}}}
\ufcNote{{OBJECT-NOTE-{locale.upper()}}}
\begin{{ufcobject}}[here]
\rule{{5cm}}{{1cm}}
\end{{ufcobject}}
\end{{document}}
"""
    (work/f"inherited-{locale}.tex").write_text(tex, encoding="utf-8")
PY
for locale in legacy pt en es fr; do
  case="inherited-$locale"
  for pass in 1 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname="$case" -output-directory="$work" "$work/$case.tex" > "$work/$case.stdout" 2>&1 || {
      cat "$work/$case.stdout"
      echo "INHERITED-LOCALE-EVIDENCE status=FAIL case=$case pass=$pass" >&2
      exit 1
    }
  done
  test -s "$work/$case.pdf"
  pdftotext -layout "$work/$case.pdf" "$work/$case.txt"
done
python3 - "$work" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path
work=Path(sys.argv[1])
expect={
  "legacy":("apêndice","anexo","fonte:","nota:"),
  "pt":("apêndice","anexo","fonte:","nota:"),
  "en":("appendix","annex","source:","note:"),
  "es":("apéndice","anexo","fuente:","nota:"),
  "fr":("annexe","annexe","source:","note:"),
}
for lang,(app,ann,source,note) in expect.items():
    data=(work/f"inherited-{lang}.txt").read_text(encoding="utf-8")
    data=re.sub(r"\s+"," ",unicodedata.normalize("NFC",data).casefold())
    for prefix,marker in ((app,"APPENDIX"),(ann,"ANNEX")):
        if not re.search(re.escape(prefix)+r"\s+a\b",data) or f"{marker}-object-{lang}" not in data:
            raise SystemExit(f"INHERITED-LOCALE-EVIDENCE status=FAIL locale={lang} label={marker}")
    for prefix,marker in ((source,"SOURCE"),(note,"NOTE")):
        if not re.search(re.escape(prefix)+r"\s*object-"+marker.lower()+"-"+lang,data):
            raise SystemExit(f"INHERITED-LOCALE-EVIDENCE status=FAIL locale={lang} label={marker}")
    if lang=="fr" and len(re.findall(r"annexe\s+a\b",data))<2:
        raise SystemExit("INHERITED-LOCALE-EVIDENCE status=FAIL fr_dual_annexe")
    if lang in ("en","es","fr") and "fonte:" in data:
        raise SystemExit(f"INHERITED-LOCALE-EVIDENCE status=FAIL pt_source_leak={lang}")
    print(f"INHERITED-LOCALE-EVIDENCE status=PASS locale={lang} real_pdf=true")
PY
