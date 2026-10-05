#!/bin/sh
set -eu

fixture="tests/documents/tagged-pdf-graphics.tex"
job="tagged-pdf-graphics"
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

for cmd in lualatex kpsewhich show-pdf-tags pdfinfo; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Tagged PDF graphics probe failed: required command not found: $cmd"
    exit 1
  }
done

image_path=$(kpsewhich example-image.pdf || true)
[ -n "$image_path" ] && [ -f "$image_path" ] || {
  echo "Tagged PDF graphics probe failed: example-image.pdf is not available in the TeX installation."
  exit 1
}

cleanup
cp "$fixture" "$source"

make DOCUMENT="$job" ENGINE=lualatex compile >"$compile_log" 2>&1 || {
  cat "$compile_log"
  echo "Tagged PDF graphics probe failed: LuaLaTeX compilation failed."
  exit 1
}

[ -s "$pdf" ] || {
  cat "$compile_log"
  echo "Tagged PDF graphics probe failed: PDF was not generated."
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
  echo "Tagged PDF graphics probe failed: Poppler does not report Tagged: yes."
  exit 1
}

show-pdf-tags --xml --map "$pdf" > "$structure"
[ -s "$structure" ] || {
  echo "Tagged PDF graphics probe failed: show-pdf-tags produced no structure output."
  exit 1
}

figure_count=$(grep -c '<Figure' "$structure" || true)
[ "$figure_count" -eq 1 ] || {
  cat "$structure"
  echo "Tagged PDF graphics probe failed: expected exactly one structural Figure; measured $figure_count."
  exit 1
}

grep -F 'alt="Quadrado de teste com a palavra EXAMPLE"' "$structure" >/dev/null || {
  cat "$structure"
  echo "Tagged PDF graphics probe failed: the meaningful graphic alt text is missing from the structure tree."
  exit 1
}

tool_version=$(show-pdf-tags --version 2>&1 | tr '\n' ' ' | sed 's/[[:space:]][[:space:]]*/ /g; s/[[:space:]]$//')
printf 'TAGGED-PDF-GRAPHICS-EVIDENCE contract=PASS accessibility_status=PARTIAL engine=lualatex tagged=yes figure_count=%s alt=present artifact=excluded image=%s inspector="%s" blocker=abntex2-memoir-sectioning\n' "$figure_count" "$image_path" "$tool_version"
echo "Tagged PDF graphics diagnostic completed without exercising memoir float/caption paths."
