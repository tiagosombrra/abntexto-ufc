#!/bin/sh
set -eu

# Render every public document type with all four optional front-matter
# display-heading choices. This is NOT full manuscript translation, official
# ABNT/UFC approval, PDF/UA proof or human visual sign-off.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT INT TERM
fixture=tests/documents/profile-locale-matrix.tex
flags='-interaction=nonstopmode -halt-on-error -file-line-error'
source_sha=$(git rev-parse HEAD)

python3 - "$work" "$fixture" <<'PY'
import json
import sys
from pathlib import Path

work = Path(sys.argv[1])
fixture = Path(sys.argv[2]).read_text(encoding="utf-8")
canonical = json.loads(
    Path("release/history/v3/v3-api-migration.json").read_text(encoding="utf-8")
)["setup_values"]["type"]
profiles = [*canonical, "scientific-article"]
locales = ("pt", "en", "es", "fr")
if len(profiles) != 7 or len(set(profiles)) != 7 or len(locales) != 4:
    raise SystemExit("PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL canonical_matrix_changed")
for marker in ("@UFC_TYPE@", "@UFC_LOCALE@", "@UFC_BODY@"):
    if fixture.count(marker) != 1:
        raise SystemExit(f"PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL placeholder={marker}")

academic_body = r"""
\pretextual
\ufcPrintTableOfContents
\textual
\section{MATRIX BODY SECTION}
Conteúdo de teste em português; somente o rótulo do sumário é traduzido.
"""
article_body = r"""
\ufcPrintArticleFrontMatter{Texto de controle de artigo científico.
\ufcSummaryKeywords{artigo; teste; idioma.}}
\section{MATRIX ARTICLE SECTION}
Conteúdo do artigo em português, independente do idioma dos rótulos.
"""
for profile in profiles:
    for locale in locales:
        body = article_body if profile == "scientific-article" else academic_body
        text = (fixture.replace("@UFC_TYPE@", profile)
                       .replace("@UFC_LOCALE@", locale)
                       .replace("@UFC_BODY@", body))
        if "@UFC_" in text:
            raise SystemExit("PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL unresolved_placeholder")
        (work / f"matrix-{profile}-{locale}.tex").write_text(text, encoding="utf-8")
PY

for profile in $(python3 - <<'PY'
import json
from pathlib import Path
print(*json.loads(Path("release/history/v3/v3-api-migration.json").read_text())["setup_values"]["type"], "scientific-article")
PY
); do
  for locale in pt en es fr; do
    job="matrix-$profile-$locale"
    for pass in 1 2 3; do
      pdflatex -jobname="$job" -output-directory="$work" $flags \
        "$work/$job.tex" > "$work/$job.stdout" 2>&1 || {
          cat "$work/$job.stdout"
          echo "PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL profile=$profile locale=$locale pass=$pass compilation=FAIL" >&2
          exit 1
        }
    done
    test -s "$work/$job.pdf" || {
      echo "PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL profile=$profile locale=$locale missing_pdf=true" >&2
      exit 1
    }
    warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$work/$job.log" |
      grep -vF 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
    if [ -n "$warnings" ]; then
      printf '%s\n' "$warnings"
      echo "PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL profile=$profile locale=$locale warnings=true" >&2
      exit 1
    fi
    pdftotext -layout "$work/$job.pdf" "$work/$job.txt"
  done
done

python3 - "$work" "$source_sha" <<'PY'
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

work = Path(sys.argv[1])
source_sha = sys.argv[2]
canonical = json.loads(
    Path("release/history/v3/v3-api-migration.json").read_text(encoding="utf-8")
)["setup_values"]["type"]
profiles = [*canonical, "scientific-article"]
locales = ("pt", "en", "es", "fr")
headings = {
    "pt": "Sumário",
    "en": "Contents",
    "es": "Índice general",
    "fr": "Table des matières",
}
def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip().casefold()

receipts = []
for profile in profiles:
    for locale in locales:
        key = f"matrix-{profile}-{locale}"
        pdf = work / f"{key}.pdf"
        source = work / f"{key}.tex"
        content = normalize((work / f"{key}.txt").read_text(encoding="utf-8"))
        assignments = re.findall(
            r"^\s*(type|labels-language)\s*=\s*([^,\n]+),",
            source.read_text(encoding="utf-8"), flags=re.MULTILINE,
        )
        if assignments != [("type", profile), ("labels-language", locale)]:
            raise SystemExit(f"PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL malformed_setup={key}")
        info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
        pages = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
        page_size = re.search(r"^Page size:\s+([\d.]+)\s+x\s+([\d.]+)\s+pts\b", info, re.MULTILINE)
        if not pages or int(pages.group(1)) < 1 or not page_size:
            raise SystemExit(f"PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL pdfinfo={key}")
        width, height = map(float, page_size.groups())
        if not (594.5 <= width <= 596.0 and 841.0 <= height <= 842.8):
            raise SystemExit(f"PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL not_a4={key}")
        if profile == "scientific-article":
            if "matrix article section" not in content or "matrix pdf profile locale smoke" not in content:
                raise SystemExit(f"PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL article_body={key}")
            if "sumário" in content or "table des matières" in content:
                raise SystemExit(f"PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL article_toc_leak={key}")
            heading_proof = "not-applicable-article-no-toc"
        else:
            if "matrix body section" not in content or normalize(headings[locale]) not in content:
                raise SystemExit(f"PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL missing_heading_or_body={key}")
            heading_proof = "rendered-toc-display-heading"
        receipt = {
            "profile": profile,
            "display_locale": locale,
            "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "pages": int(pages.group(1)),
            "page_size": "A4",
            "heading_proof": heading_proof,
            "source_content_language": "pt-BR",
            "pdf_metadata_language": "pt-BR",
        }
        receipts.append(receipt)
        print(
            f"PROFILE-LOCALE-MATRIX-EVIDENCE status=PASS profile={profile} "
            f"locale={locale} pages={receipt['pages']} a4=PASS "
            f"heading={heading_proof}"
        )
if len(receipts) != 28 or len({(r["profile"], r["display_locale"]) for r in receipts}) != 28:
    raise SystemExit("PROFILE-LOCALE-MATRIX-EVIDENCE status=FAIL incomplete_28_case_matrix")
manifest = {
    "status": "AUTOMATED_DISPLAY_SMOKE_ONLY",
    "source_sha": source_sha,
    "profiles": profiles,
    "display_locales": locales,
    "case_count": 28,
    "frontmatter_labels_scope": "display-headings-only",
    "full_document_translation_certified": False,
    "pdf_ua_compliant": False,
    "human_visual_approval": "PENDING",
    "normative_rule_promotion": False,
    "receipts": receipts,
}
out = Path("artifacts/frontmatter/profile-locale-matrix.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("PROFILE-LOCALE-MATRIX-EVIDENCE status=PASS real_pdfs=28 profiles=7 locales=4 compilation=PASS pdf_a4=PASS display_scope=partial human_visual_approval=PENDING")
PY
