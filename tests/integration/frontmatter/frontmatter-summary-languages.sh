#!/bin/sh
set -eu

# Opt-in multilingual abstracts: real PDF positive/negative controls.
# The nine front-matter display headings and canonical normative rules are separate.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT INT TERM
flags='-interaction=nonstopmode -halt-on-error -file-line-error'

python3 - "$work" <<'PY'
import sys
from pathlib import Path

work = Path(sys.argv[1])
langs = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
for main, pdf_lang in langs.items():
    complement = "en" if main == "pt" else "pt"
    for lang in set(langs):
        (work / f"{main}-{lang}.tex").write_text(
            f"LANGUAGE-CONTENT-{main.upper()}-{lang.upper()}."
            f"\\ufcSummaryKeywordsInLanguage{{{lang}}}{{meshing; research.}}",
            encoding="utf-8",
        )
    base = rf"""
\DocumentMetadata{{lang={pdf_lang},pdfstandard=A-2b,pdfversion=1.7}}
\documentclass{{abntexto-ufc}}
\ufcsetup{{
  type=doctoral-thesis,
  document-language={main},
  labels-language=pt,
  coat-of-arms=false,
  cover=false,
  catalog-card=false
}}
\begin{{document}}
\pretextual
\ufcPrintRequiredSummaries{{{work / (main + '-' + main + '.tex')}}}{{{work / (main + '-' + complement + '.tex')}}}
"""
    if main in {"es", "fr"}:
        base += rf"\ufcPrintOptionalEnglishSummary{{{work / (main + '-en.tex')}}}" + "\n"
    base += r"\textual" + "\n" + rf"\section{{BODY-{main.upper()}}}" + "\n"
    base += r"\end{document}" + "\n"
    (work / f"academic-{main}.tex").write_text(base, encoding="utf-8")
    # Article: main-language summary, then Portuguese or English complement.
    article = rf"""
\DocumentMetadata{{lang={pdf_lang},pdfstandard=A-2b,pdfversion=1.7}}
\documentclass{{abntexto-ufc}}
\ufcsetup{{
  type=scientific-article,
  document-language={main},
  title={{Policy Article}},
  author={{Academic Test Author}},
  article-author-note={{Testing Institution}},
  submission-date={{20 October 2026}},
  approval-date={{21 October 2026}},
  coat-of-arms=false,
  cover=false
}}
\begin{{document}}
\ufcPrintArticleFrontMatter{{ARTICLE-PRIMARY-{main.upper()}. \ufcSummaryKeywordsInLanguage{{{main}}}{{meshing; research.}}}}
\ufcPrintArticleTranslatedSummary{{{complement}}}{{ARTICLE-SECONDARY-{complement.upper()}. \ufcSummaryKeywordsInLanguage{{{complement}}}{{meshing; research.}}}}
"""
    if main in {"es", "fr"}:
        article += rf"\ufcPrintArticleTranslatedSummary{{en}}{{ARTICLE-OPTIONAL-EN. \ufcSummaryKeywordsInLanguage{{en}}{{meshing; research.}}}}" + "\n"
    article += r"\textual" + "\n" + rf"\section{{ARTICLEBODY-{main.upper()}}}" + "\n"
    article += r"\end{document}" + "\n"
    (work / f"article-{main}.tex").write_text(article, encoding="utf-8")

(work / "academic-duplicate.tex").write_text(
    (work / "academic-pt.tex").read_text(encoding="utf-8").replace(
        r"\textual",
        rf"\ufcPrintSummaryInLanguage{{en}}{{{work / 'pt-en.tex'}}}" + "\n" + r"\textual"
    ),
    encoding="utf-8",
)
(work / "academic-invalid.tex").write_text(
    (work / "academic-pt.tex").read_text(encoding="utf-8").replace(
        "document-language=pt", "document-language=de"
    ),
    encoding="utf-8",
)
(work / "academic-keyword-invalid.tex").write_text(
    (work / "academic-pt.tex").read_text(encoding="utf-8").replace(
        r"\textual", r"\ufcSummaryKeywordsInLanguage{de}{invalid.}" + "\n" + r"\textual"
    ),
    encoding="utf-8",
)
(work / "article-duplicate.tex").write_text(
    (work / "article-en.tex").read_text(encoding="utf-8").replace(
        rf"\ufcPrintArticleTranslatedSummary{{pt}}",
        rf"\ufcPrintArticleTranslatedSummary{{en}}", 1
    ),
    encoding="utf-8",
)
PY

for case in academic-pt academic-en academic-es academic-fr article-pt article-en article-es article-fr; do
  for pass in 1 2 3; do
    pdflatex $flags -jobname="$case" -output-directory="$work" "$work/$case.tex" > "$work/$case.stdout" 2>&1 || {
      cat "$work/$case.stdout"
      echo "SUMMARY-LOCALE-EVIDENCE status=FAIL case=$case pass=$pass compilation=FAIL" >&2
      exit 1
    }
  done
  test -s "$work/$case.pdf"
  pdftotext -layout "$work/$case.pdf" "$work/$case.txt"
  echo "SUMMARY-LOCALE-EVIDENCE status=PASS case=$case real_pdf=true"
done

for case in academic-duplicate academic-invalid academic-keyword-invalid article-duplicate; do
  if pdflatex $flags -jobname="$case" -output-directory="$work" "$work/$case.tex" > "$work/$case.stdout" 2>&1; then
    echo "SUMMARY-LOCALE-EVIDENCE status=FAIL unexpected_negative_success=$case" >&2
    exit 1
  fi
  case "$case" in
    academic-duplicate|article-duplicate)
      grep -Fq 'Duplicate' "$work/$case.stdout" ||
      grep -Fq 'duplicates' "$work/$case.stdout" || {
        cat "$work/$case.stdout"
        echo "SUMMARY-LOCALE-EVIDENCE status=FAIL missing_duplicate_error=$case" >&2
        exit 1
      }
      ;;
    academic-invalid)
      grep -Fq "document-language" "$work/$case.stdout" || {
        cat "$work/$case.stdout"
        echo "SUMMARY-LOCALE-EVIDENCE status=FAIL missing_invalid_locale_error=true" >&2
        exit 1
      }
      ;;
    academic-keyword-invalid)
      grep -Fq "Unsupported" "$work/$case.stdout" || {
        cat "$work/$case.stdout"
        echo "SUMMARY-LOCALE-EVIDENCE status=FAIL missing_invalid_keyword_locale_error=true" >&2
        exit 1
      }
      ;;
  esac
  echo "SUMMARY-LOCALE-EVIDENCE status=PASS negative=$case rejected=true"
done

python3 - "$work" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

work = Path(sys.argv[1])
titles = {"pt": "RESUMO", "en": "ABSTRACT", "es": "RESUMEN", "fr": "RÉSUMÉ"}
keywords = {"pt": "Palavras-chave:", "en": "Keywords:",
            "es": "Palabras clave:", "fr": "Mots-clés:"}

def norm(value):
    return unicodedata.normalize("NFC", value).casefold()

for kind in ("academic", "article"):
    for main in titles:
        secondary = "en" if main == "pt" else "pt"
        expect = [main, secondary] + (["en"] if main in ("es", "fr") else [])
        raw = (work / f"{kind}-{main}.txt").read_text(encoding="utf-8")
        text = norm(raw)
        # Each version must be on a separate heading/inline heading route.
        found_with_offsets = []
        for language, heading in titles.items():
            if kind == "academic":
                matches = list(re.finditer(
                    r"^\s*" + re.escape(norm(heading)) + r"\s*$",
                    text, flags=re.MULTILINE,
                ))
            else:
                matches = list(re.finditer(
                    r"\b" + re.escape(norm(heading)) + r"\s*:",
                    text,
                ))
            if matches:
                if len(matches) != 1:
                    raise SystemExit(f"SUMMARY-LOCALE-EVIDENCE status=FAIL duplicate={kind}-{main}-{language}")
                found_with_offsets.append((matches[0].start(), language))
        found = [language for _, language in sorted(found_with_offsets)]
        if found != expect:
            raise SystemExit(f"SUMMARY-LOCALE-EVIDENCE status=FAIL headings_or_order={kind}-{main}-{found} expected={expect}")
        expected_markers = (
            [f"language-content-{main}-{l}" for l in expect]
            if kind == "academic"
            else [f"article-primary-{main}", f"article-secondary-{secondary}"]
            + (["article-optional-en"] if main in {"es", "fr"} else [])
        )
        for marker in expected_markers:
            if norm(marker) not in text:
                raise SystemExit(f"SUMMARY-LOCALE-EVIDENCE status=FAIL missing_text={kind}-{main}-{marker}")
        for lang in expect:
            if norm(keywords[lang]) not in text:
                raise SystemExit(f"SUMMARY-LOCALE-EVIDENCE status=FAIL missing_keyword_label={kind}-{main}-{lang}")
        # The last section must still use the manuscript's main language.
        if norm(("body-" if kind == "academic" else "articlebody-") + main) not in text:
            raise SystemExit(f"SUMMARY-LOCALE-EVIDENCE status=FAIL body_missing={kind}-{main}")
        print(f"SUMMARY-LOCALE-EVIDENCE status=PASS kind={kind} main={main} versions={','.join(expect)} headings=PASS keywords=PASS no_duplicates=PASS")
print("SUMMARY-LOCALE-EVIDENCE status=PASS real_pdfs=8 positive=8 negative=4 main_languages=pt,en,es,fr compatibility=OPT_IN")
PY
