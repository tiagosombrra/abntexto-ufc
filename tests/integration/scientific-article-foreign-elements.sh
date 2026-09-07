#!/bin/sh
set -eu

module="abntexto-ufc/articles.def"

title_marker="ARTICLEFOREIGNTITLEMARKER"
summary_marker="ARTICLEFOREIGNSUMMARYMARKER"
control_marker="ARTICLEFOREIGNCONTROL"

cleanup_job() {
  job="$1"
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc" "/tmp/$job.txt"
}

grep -Fq '\NewDocumentCommand \ufcPrintArticleForeignElements { +m +m }' "$module" || {
  echo 'Scientific article foreign-elements gate failed: explicit article foreign-elements route is missing.'
  exit 1
}

blank_guard_count=$(grep -Fc '\tl_if_blank:nF {#1}' "$module" || true)
[ "$blank_guard_count" -ge 2 ] || {
  echo 'Scientific article foreign-elements gate failed: foreign title and summary are not independently blank-safe.'
  exit 1
}

if grep -Fq 'title-variant' "$module"; then
  echo 'Scientific article foreign-elements gate failed: shared title-variant metadata was repurposed for article foreign-title semantics.'
  exit 1
fi

grep -Fq '\cs_new_protected:Npn \ufc_article_apply_body_typography:' "$module" || {
  echo 'Scientific article foreign-elements gate failed: accepted Step 4 body activation is missing.'
  exit 1
}
grep -Fq '\str_if_eq:VnT \g_ufc_document_type_tl {scientific-article}' "$module" || {
  echo 'Scientific article foreign-elements gate failed: Step 4 body activation is not profile-scoped.'
  exit 1
}
grep -Fq '\AddToHook{begindocument/end}{\ufc_article_apply_body_typography:}' "$module" || {
  echo 'Scientific article foreign-elements gate failed: Step 4 body activation is not registered after shared begin-document initialization.'
  exit 1
}

run_case() {
  engine="$1"
  scenario="$2"
  fixture="$3"
  expect_title="$4"
  expect_summary="$5"
  job="scientific-article-foreign-${scenario}-${engine}"

  cleanup_job "$job"

  # Two passes are required before warning inspection because the shared class
  # uses cross-reference infrastructure even in this minimal article fixture.
  for pass in 1 2; do
    "$engine" \
      -jobname="$job" \
      -interaction=nonstopmode \
      -halt-on-error \
      -file-line-error \
      "$fixture" > "/tmp/$job.out" 2>&1 || {
        cat "/tmp/$job.out"
        exit 1
      }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Scientific article foreign-elements gate failed: unrecognized warning or overflow in $scenario with $engine."
    exit 1
  fi

  [ -s "$job.pdf" ] || {
    echo "Scientific article foreign-elements gate failed: PDF was not generated in $scenario with $engine."
    exit 1
  }

  pdftotext -layout "$job.pdf" "/tmp/$job.txt"
  grep -Fq "$control_marker" "/tmp/$job.txt" || {
    echo "Scientific article foreign-elements gate failed: control marker is missing in $scenario with $engine."
    exit 1
  }

  if [ "$expect_title" = "present" ]; then
    grep -Fq "$title_marker" "/tmp/$job.txt" || {
      echo "Scientific article foreign-elements gate failed: foreign title is missing in $scenario with $engine."
      exit 1
    }
  elif grep -Fq "$title_marker" "/tmp/$job.txt"; then
    echo "Scientific article foreign-elements gate failed: foreign title rendered unexpectedly in $scenario with $engine."
    exit 1
  fi

  if [ "$expect_summary" = "present" ]; then
    grep -Fq "$summary_marker" "/tmp/$job.txt" || {
      echo "Scientific article foreign-elements gate failed: foreign summary is missing in $scenario with $engine."
      exit 1
    }
  elif grep -Fq "$summary_marker" "/tmp/$job.txt"; then
    echo "Scientific article foreign-elements gate failed: foreign summary rendered unexpectedly in $scenario with $engine."
    exit 1
  fi

  cleanup_job "$job"
}

for engine in pdflatex lualatex; do
  run_case "$engine" both \
    tests/documents/scientific-article-foreign-both.tex present present
  run_case "$engine" title-only \
    tests/documents/scientific-article-foreign-title-only.tex present absent
  run_case "$engine" summary-only \
    tests/documents/scientific-article-foreign-summary-only.tex absent present
  run_case "$engine" absent \
    tests/documents/scientific-article-foreign-absent.tex absent absent
done

echo 'ARTICLE-FOREIGN-ELEMENTS-EVIDENCE status=PASS engines=2 scenarios=4 convergence_passes=2 warnings_checked_after_final_pass=true title_optional=true summary_optional=true independent=true title_variant_reused=false step4_body_route=profile-scoped-post-shared-initialization presentation_rules_promoted=0 recommendations_promoted=0'
echo 'Scientific article foreign-elements gate completed.'
