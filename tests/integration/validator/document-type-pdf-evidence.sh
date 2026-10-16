#!/bin/sh
# Produce real class-rendered documents for cross-surface validator regression.
set -eu

out="artifacts/validation/document-profiles"
mkdir -p "$out"
tmp="$(mktemp -d)"
article_job="validator-article-missing-front"
project_job="validator-project-missing-refs"

cleanup() {
  make DOCUMENT=scientific-article clean >/dev/null 2>&1 || true
  make DOCUMENT="$project_job" clean >/dev/null 2>&1 || true
  rm -f "template/$project_job.tex"
  for ext in aux log out pdf toc bcf bbl blg run.xml; do
    rm -f "$article_job.$ext"
  done
  rm -rf "$tmp"
}
trap cleanup EXIT INT TERM

for type in research-project anonymized-research-project; do
  source="template/perfil-$type-pdflatex.pdf"
  test -s "$source" || {
    echo "Document-type final-PDF evidence: missing profile-matrix PDF: $source" >&2
    exit 1
  }
  cp "$source" "$out/$type.pdf"
done

# The canonical scientific article has primary summary, keywords and references.
make DOCUMENT=scientific-article ENGINE=pdflatex compile > "$tmp/article-build.log" 2>&1 || {
  cat "$tmp/article-build.log"
  exit 1
}
test -s template/scientific-article.pdf
cp template/scientific-article.pdf "$out/scientific-article.pdf"
make DOCUMENT=scientific-article clean >/dev/null

# Existing standalone article fixture intentionally misses required content.
# It must still generate a real PDF under the actual project class.
for pass in 1 2; do
  pdflatex -jobname="$article_job" -interaction=nonstopmode \
    -halt-on-error -file-line-error \
    tests/documents/scientific-article-profile.tex > "$tmp/article-negative.log" 2>&1 || {
    cat "$tmp/article-negative.log"
    exit 1
  }
done
test -s "$article_job.pdf"
cp "$article_job.pdf" "$out/scientific-article-missing.pdf"

# A project whose bibliography is deliberately omitted: negative compiled PDF.
python3 - "tests/smoke/base-profile.tex" "template/$project_job.tex" <<'PY'
from pathlib import Path
import sys

source = Path(sys.argv[1]).read_text(encoding="utf-8")
anchors = {
    "type = @UFC_TYPE@,": "type = research-project,",
    "tests/fixtures/references.bib": "../tests/fixtures/references.bib",
    r"\ufcPrintReferences": "% Deliberately omit required project references",
}
for previous, replacement in anchors.items():
    if source.count(previous) != 1:
        raise SystemExit(f"Document-type negative source drift: {previous}")
    source = source.replace(previous, replacement)
Path(sys.argv[2]).write_text(source, encoding="utf-8")
PY
make DOCUMENT="$project_job" ENGINE=pdflatex compile > "$tmp/project-negative.log" 2>&1 || {
  cat "$tmp/project-negative.log"
  exit 1
}
test -s "template/$project_job.pdf"
cp "template/$project_job.pdf" "$out/research-project-missing-refs.pdf"

python3 tests/checks/validator/document_type_pdf_evidence.py \
  --pdf-dir "$out" \
  --evidence "$out/cli-evidence.json" \
  --source-sha "$(git rev-parse HEAD)"

echo 'DOCUMENT-TYPE-PDF-EVIDENCE status=PASS generated=5 surfaces=cli-deep browser_inputs=READY scope=automatic-partial'
