#!/bin/sh
set -eu

fixture="tests/documents/scientific-article-front-block.tex"
module="abntexto-ufc/articles.def"

cleanup_job() {
  job="$1"
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc" "$job.front-block.txt"
}

grep -Fq '\normalsize\singlesp\bfseries' "$module" || {
  echo 'Scientific article front-block gate failed: primary title source contract is missing 12 pt/single-spacing/bold composition.'
  exit 1
}
grep -Fq '\footnote{\ufc_meta_use:n {article-author-note}}' "$module" || {
  echo 'Scientific article front-block gate failed: article-author-note is not routed through a footnote.'
  exit 1
}

for engine in pdflatex lualatex; do
  job="scientific-article-front-block-$engine"
  cleanup_job "$job"

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
    echo "Scientific article front-block gate failed: unrecognized warning or overflow with $engine."
    exit 1
  fi

  [ -s "$job.pdf" ] || {
    echo "Scientific article front-block gate failed: PDF was not generated with $engine."
    exit 1
  }

  python3 tests/checks/scientific_article_front_block.py "$job.pdf"
done

cleanup_job scientific-article-front-block-pdflatex
cleanup_job scientific-article-front-block-lualatex

echo 'ARTICLE-FRONT-BLOCK-EVIDENCE status=PASS engines=2 rules=title-required,authorship-required,summary-required,dates-required,title-typography,authorship-footnote presentation_rules_promoted=0 recommendations_promoted=0'
echo 'Scientific article front-block gate completed.'
