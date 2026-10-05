#!/bin/sh
set -eu

fixture="tests/documents/tagged-pdf-table.tex"
job="tagged-pdf-table"
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
    echo "Tagged PDF table probe failed: required command not found: $cmd"
    exit 1
  }
done

cleanup
cp "$fixture" "$source"

make DOCUMENT="$job" ENGINE=lualatex compile >"$compile_log" 2>&1 || {
  cat "$compile_log"
  echo "Tagged PDF table probe failed: LuaLaTeX compilation failed."
  exit 1
}

[ -s "$pdf" ] || {
  cat "$compile_log"
  echo "Tagged PDF table probe failed: PDF was not generated."
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
  echo "Tagged PDF table probe failed: Poppler does not report Tagged: yes."
  exit 1
}

show-pdf-tags --xml --map "$pdf" > "$structure"
[ -s "$structure" ] || {
  echo "Tagged PDF table probe failed: show-pdf-tags produced no structure output."
  exit 1
}

table_count=$(grep -c '<Table' "$structure" || true)
row_count=$(grep -c '<TR' "$structure" || true)
header_count=$(grep -c '<TH' "$structure" || true)
data_count=$(grep -c '<TD' "$structure" || true)

[ "$table_count" -eq 1 ] || {
  cat "$structure"
  echo "Tagged PDF table probe failed: expected one Table; measured $table_count."
  exit 1
}
[ "$row_count" -eq 3 ] || {
  cat "$structure"
  echo "Tagged PDF table probe failed: expected three TR rows; measured $row_count."
  exit 1
}
[ "$header_count" -eq 2 ] || {
  cat "$structure"
  echo "Tagged PDF table probe failed: expected two TH cells; measured $header_count."
  exit 1
}
[ "$data_count" -eq 4 ] || {
  cat "$structure"
  echo "Tagged PDF table probe failed: expected four TD cells; measured $data_count."
  exit 1
}

tool_version=$(show-pdf-tags --version 2>&1 | tr '\n' ' ' | sed 's/[[:space:]][[:space:]]*/ /g; s/[[:space:]]$//')
printf 'TAGGED-PDF-TABLE-EVIDENCE contract=PASS accessibility_status=PARTIAL engine=lualatex tagged=yes table=%s rows=%s headers=%s data_cells=%s inspector="%s" blocker=abntex2-memoir-sectioning\n' "$table_count" "$row_count" "$header_count" "$data_count" "$tool_version"
echo "Tagged PDF table-header diagnostic completed without exercising float/caption paths."
