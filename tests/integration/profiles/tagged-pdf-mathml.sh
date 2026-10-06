#!/bin/sh
set -eu

fixture="tests/documents/tagged-pdf-mathml.tex"
job="tagged-pdf-mathml"
source="template/$job.tex"
pdf="template/$job.pdf"
compile_log="/tmp/$job-compile.log"
structure="/tmp/$job-structure.xml"

cleanup() {
  rm -f \
    "$source" \
    "template/$job.aux" \
    "template/$job.bbl" \
    "template/$job.bcf" \
    "template/$job.blg" \
    "template/$job.fdb_latexmk" \
    "template/$job.fls" \
    "template/$job.glo" \
    "template/$job.idx" \
    "template/$job.log" \
    "template/$job.out" \
    "template/$job.pdf" \
    "template/$job.run.xml" \
    "template/$job.toc"
}
trap cleanup EXIT INT TERM

for cmd in lualatex show-pdf-tags pdfinfo; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Tagged PDF MathML probe failed: required command not found: $cmd"
    exit 1
  }
done

cleanup
cp "$fixture" "$source"

make DOCUMENT="$job" ENGINE=lualatex compile >"$compile_log" 2>&1 || {
  cat "$compile_log"
  echo "Tagged PDF MathML probe failed: LuaLaTeX compilation failed."
  exit 1
}

[ -s "$pdf" ] || {
  cat "$compile_log"
  echo "Tagged PDF MathML probe failed: PDF was not generated."
  exit 1
}

tagged=$(pdfinfo "$pdf" | awk -F: '
  /^Tagged:/ {
    value=$2
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
    print tolower(value)
  }
')
[ "$tagged" = "yes" ] || {
  pdfinfo "$pdf"
  echo "Tagged PDF MathML probe failed: Poppler does not report Tagged: yes."
  exit 1
}

show-pdf-tags --xml --map "$pdf" > "$structure"
[ -s "$structure" ] || {
  echo "Tagged PDF MathML probe failed: show-pdf-tags produced no structure output."
  exit 1
}

formula_count=$(grep -c '<Formula' "$structure" || true)
[ "$formula_count" -eq 1 ] || {
  cat "$structure"
  echo "Tagged PDF MathML probe failed: expected exactly one Formula; measured $formula_count."
  exit 1
}

grep -F '<math xmlns="http://www.w3.org/1998/Math/MathML"' "$structure" >/dev/null || {
  cat "$structure"
  echo "Tagged PDF MathML probe failed: MathML root element is missing."
  exit 1
}

for element in mi mo mn msup; do
  if ! grep -F "<$element xmlns=\"http://www.w3.org/1998/Math/MathML\"" "$structure" >/dev/null; then
    cat "$structure"
    echo "Tagged PDF MathML probe failed: expected MathML element $element is missing."
    exit 1
  fi
done

tool_version=$(show-pdf-tags --version 2>&1 | tr '\n' ' ' | sed 's/[[:space:]][[:space:]]*/ /g; s/[[:space:]]$//')
printf 'TAGGED-PDF-MATHML-EVIDENCE contract=PASS accessibility_status=PARTIAL engine=lualatex tagged=yes formula=%s mathml=math,mi,mo,mn,msup setup=mathml-SE inspector="%s" blocker=abntex2-memoir-sectioning\n' "$formula_count" "$tool_version"
echo "Tagged PDF MathML diagnostic completed without exercising section, TOC, float or caption paths."
