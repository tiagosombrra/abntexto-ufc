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
\legend{{figure}}{{PLAINCAPTION{locale.upper()}}}
\ufcSource{{OBJSOURCE{locale.upper()}}}
\ufcNote{{OBJNOTE{locale.upper()}}}
\begin{{ufcobject}}[here]
\rule{{5cm}}{{1cm}}
\end{{ufcobject}}
% Separate objects avoid column interleaving in extracted PDF text.
\legend{{figure}}{{MULTINORMAL{locale.upper()}}}
\begin{{multiplace}}[here]
\sublegend{{NORMALSUB{locale.upper()}}}
\begin{{subplace}}[3cm]
\rule{{2cm}}{{1cm}}
\end{{subplace}}
\end{{multiplace}}
\legend{{figure}}{{MULTIALT{locale.upper()}}}
\begin{{multiplace}}[here]
\sublegend[figure]{{ALTSUB{locale.upper()}}}
\begin{{subplace}}[3cm]
\rule{{2cm}}{{1cm}}
\end{{subplace}}
\end{{multiplace}}
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
    def fail(label, pattern):
        # Keep extracted observations visible even when PDFs are absent from
        # uploaded workflow artifacts. Do not silently relax the assertions.
        print(f"INHERITED-LOCALE-DEBUG locale={lang} label={label} pattern={pattern!r} extracted={data[:1400]!r}",flush=True)
        raise SystemExit(f"INHERITED-LOCALE-EVIDENCE status=FAIL locale={lang} label={label}")
    for prefix,marker in ((app,"APPENDIX"),(ann,"ANNEX")):
        pattern=re.escape(prefix)+r"\s+a\b"
        if not re.search(pattern,data) or f"{marker.lower()}-object-{lang}" not in data:
            fail(marker,pattern)
    for prefix,marker in ((source,"OBJSOURCE"),(note,"OBJNOTE")):
        pattern=re.escape(prefix)+r"\s*"+marker.lower()+lang
        if not re.search(pattern,data):
            fail(marker,pattern)
    for marker in ("plaincaption","multinormal","multialt","normalsub","altsub"):
        if marker+lang not in data:
            fail(marker,marker+lang)
    # A normal sublegend must carry the inherited '(a)' identifier; the
    # alternate path uses the inherited object number before its title.
    if not re.search(r"\(a\)\s*normalsub"+lang,data):
        fail("normal_sub_number","(a) before caption")
    if not re.search(r"\b\d+\s*(?:—|---|–)\s*altsub"+lang,data):
        fail("alternative_sub_number","object number and separator before caption")
    if lang=="fr" and len(re.findall(r"annexe\s+a\b",data))<2:
        fail("fr_dual_annexe","two annex labels")
    if lang in ("en","es","fr") and "fonte:" in data:
        fail("pt_source_leak","fonte:")
    print(f"INHERITED-LOCALE-EVIDENCE status=PASS locale={lang} paths=plain,normal-sub,alternative-sub real_pdf=true")
PY
