#!/bin/sh
set -eu

fixture="tests/documents/tagged-pdf-baseline.tex"
job="tagged-pdf-baseline"
source="template/$job.tex"
pdf="template/$job.pdf"
compile_log="/tmp/$job-compile.log"
metadata="/tmp/$job-meta.xml"
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

for cmd in lualatex kpsewhich show-pdf-tags pdfinfo; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Tagged PDF baseline failed: required command not found: $cmd"
    exit 1
  }
done

tagpdf_path=$(kpsewhich tagpdf.sty || true)
[ -n "$tagpdf_path" ] && [ -f "$tagpdf_path" ] || {
  echo "Tagged PDF baseline failed: tagpdf.sty is not available in the TeX installation."
  exit 1
}

cleanup
cp "$fixture" "$source"

make DOCUMENT="$job" ENGINE=lualatex compile >"$compile_log" 2>&1 || {
  cat "$compile_log"
  echo "Tagged PDF baseline failed: LuaLaTeX compilation failed."
  exit 1
}

[ -s "$pdf" ] || {
  cat "$compile_log"
  echo "Tagged PDF baseline failed: PDF was not generated."
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
  echo "Tagged PDF baseline failed: Poppler does not report Tagged: yes."
  exit 1
}

pdfinfo -meta "$pdf" > "$metadata"
grep -Eiq '<pdfuaid:part>[[:space:]]*2[[:space:]]*</pdfuaid:part>' "$metadata" || {
  cat "$metadata"
  echo "Tagged PDF baseline failed: PDF/UA-2 XMP declaration is missing."
  exit 1
}
grep -Eiq '<pdfaid:part>[[:space:]]*4[[:space:]]*</pdfaid:part>' "$metadata" || {
  cat "$metadata"
  echo "Tagged PDF baseline failed: PDF/A part 4 XMP declaration is missing."
  exit 1
}
grep -Eiq '<pdfaid:conformance>[[:space:]]*[Ff][[:space:]]*</pdfaid:conformance>' "$metadata" || {
  cat "$metadata"
  echo "Tagged PDF baseline failed: PDF/A-4f XMP declaration is missing."
  exit 1
}

show-pdf-tags --xml --map "$pdf" > "$structure"
[ -s "$structure" ] || {
  echo "Tagged PDF baseline failed: show-pdf-tags produced no structure output."
  exit 1
}

require_role() {
  role=$1
  if ! grep -Eq "<$role([[:space:]>])|rolemaps-to=\"$role\"" "$structure"; then
    cat "$structure"
    echo "Tagged PDF baseline failed: expected structure role $role is missing."
    exit 1
  fi
}

for role in Document Sect P L LI; do
  require_role "$role"
done

tool_version=$(show-pdf-tags --version 2>&1 | tr '\n' ' ' | sed 's/[[:space:]][[:space:]]*/ /g; s/[[:space:]]$//')
printf 'TAGGED-PDF-BASELINE-EVIDENCE status=PASS engine=lualatex tagged=yes pdfua_declared=2 pdfa_declared=4f structure=Document,Sect,P,L,LI inspector="%s" tagpdf=%s\n' "$tool_version" "$tagpdf_path"
echo "Tagged PDF baseline experiment completed."
