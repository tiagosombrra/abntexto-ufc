#!/bin/sh
set -eu
# Separate from labels-language 28-case matrix. Actual primary document
# language and class-owned nature strings; official names remain user text.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT INT TERM
mkdir -p artifacts/frontmatter
python3 - "$work" <<'PY'
from pathlib import Path
import json,sys
work=Path(sys.argv[1])
fixture=Path("tests/documents/profile-locale-matrix.tex").read_text(encoding="utf-8")
profiles=[*json.loads(Path("release/history/v3/v3-api-migration.json").read_text())["setup_values"]["type"],"scientific-article"]
langs={"pt":"pt-BR","en":"en-US","es":"es-ES","fr":"fr-FR"}
if len(profiles)!=7: raise SystemExit("PRIMARY-LOCALE-MATRIX status=FAIL seven_profiles")
for profile in profiles:
  for locale,code in langs.items():
    if profile=="scientific-article":
      body=rf"\ufcPrintArticleFrontMatter{{PRIMARY-ARTICLE-{locale.upper()}. \ufcSummaryKeywordsInLanguage{{{locale}}}{{research; computing.}}}}"+"\n"
    else:
      body="\\pretextual\n\\ufcPrintTitlePage\n"
    body+=rf"\typeout{{UFC-PRIMARY-BABEL=\languagename}}"+"\n"
    body+="\\textual\n"+rf"\section{{PRIMARY-PROFILE-{locale.upper()}}}"+"\n"+f"PRIMARY-LOCALE-MANUSCRIPT-{locale.upper()}.\n"
    tex=fixture.replace("lang = pt-BR,",f"lang = {code},").replace("labels-language = @UFC_LOCALE@,","document-language = @UFC_LOCALE@,")
    tex=tex.replace("@UFC_TYPE@",profile).replace("@UFC_LOCALE@",locale).replace("@UFC_BODY@",body)
    if "@UFC_" in tex or f"document-language = {locale}," not in tex:
      raise SystemExit("PRIMARY-LOCALE-MATRIX status=FAIL unresolved_setup")
    (work/f"primary-{profile}-{locale}.tex").write_text(tex,encoding="utf-8")
PY
profiles=$(python3 - <<'PY'
import json
from pathlib import Path
print(*json.loads(Path("release/history/v3/v3-api-migration.json").read_text())["setup_values"]["type"],"scientific-article")
PY
)
for profile in $profiles; do
  for locale in pt en es fr; do
    job="primary-$profile-$locale"
    for pass in 1 2; do
      pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname="$job" \
        -output-directory="$work" "$work/$job.tex" > "$work/$job.stdout" 2>&1 || {
        cat "$work/$job.stdout"
        echo "PRIMARY-LOCALE-MATRIX status=FAIL case=$job pass=$pass" >&2
        exit 1
      }
    done
    test -s "$work/$job.pdf"
    pdftotext -layout "$work/$job.pdf" "$work/$job.txt"
  done
done
python3 - "$work" <<'PY'
import hashlib,json,re,sys,unicodedata,os
from pathlib import Path
work=Path(sys.argv[1])
profiles=[*json.loads(Path("release/history/v3/v3-api-migration.json").read_text())["setup_values"]["type"],"scientific-article"]
langs={"pt":("pt-BR","brazilian"),"en":("en-US","english"),"es":("es-ES","spanish"),"fr":("fr-FR","french")}
nature={
"undergraduate-capstone":("trabalho de conclusao de curso","undergraduate capstone","trabajo de fin de grado","memoire de fin de licence"),
"specialization-capstone":("trabalho de conclusao de curso","specialization capstone","trabajo final de especializacion","memoire de specialisation"),
"masters-thesis":("dissertacao apresentada","master's dissertation submitted","disertacion presentada","memoire presente"),
"doctoral-thesis":("tese apresentada","doctoral thesis submitted","tesis presentada","these presente"),
"research-project":("apresentado a","submitted to","presentado a","soumis a"),
"anonymized-research-project":("apresentado a","submitted to","presentado a","soumis a"),
"scientific-article":("submetido em","submitted on","enviado el","soumis le")
}
def fold(x):return re.sub(r"\s+"," ",unicodedata.normalize("NFKD",x).encode("ascii","ignore").decode().lower()).strip()
receipts=[]
for profile in profiles:
  for i,(locale,(code,babel)) in enumerate(langs.items()):
    name=f"primary-{profile}-{locale}"
    pdf=work/f"{name}.pdf"
    source=(work/f"{name}.tex").read_text()
    text=fold((work/f"{name}.txt").read_text())
    log=(work/f"{name}.log").read_text(errors="replace")
    if fold(nature[profile][i]) not in text:
      raise SystemExit(f"PRIMARY-LOCALE-MATRIX status=FAIL nature={name} expected={nature[profile][i]} sample={text[:1100]}")
    if f"UFC-PRIMARY-BABEL={babel}" not in log:
      raise SystemExit(f"PRIMARY-LOCALE-MATRIX status=FAIL babel={name} expected={babel}")
    if fold("PRIMARY-LOCALE-MANUSCRIPT-"+locale.upper()) not in text or f"lang = {code}," not in source:
      raise SystemExit(f"PRIMARY-LOCALE-MATRIX status=FAIL body_or_metadata={name}")
    receipts.append({"profile":profile,"locale":locale,"babel":babel,"author_declared_pdf_lang":code,
     "pdf_sha256":hashlib.sha256(pdf.read_bytes()).hexdigest(),"source_sha256":hashlib.sha256(source.encode()).hexdigest()})
    print(f"PRIMARY-LOCALE-MATRIX status=PASS profile={profile} locale={locale} babel={babel}",flush=True)
if len(receipts)!=28 or len({(x["profile"],x["locale"]) for x in receipts})!=28:
  raise SystemExit("PRIMARY-LOCALE-MATRIX status=FAIL incomplete_matrix")
manifest={"status":"AUTOMATED_PARTIAL","case_count":28,"source_sha":os.environ.get("GITHUB_SHA",""),
 "author_declared_pdf_lang":True,"pdf_catalog_language_independently_verified":False,
 "official_institutional_translation_verified":False,"author_prose_translated":False,
 "human_visual_approval":"PENDING","receipts":receipts}
Path("artifacts/frontmatter/primary-document-locale-matrix.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("PRIMARY-LOCALE-MATRIX status=PASS profiles=7 document_locales=4 real_pdfs=28 pdf_catalog=NOT_CHECKED proof=automatic-partial")
PY
