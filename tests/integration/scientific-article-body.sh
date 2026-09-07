#!/bin/sh
set -eu

fixture="tests/documents/scientific-article-body.tex"
negative_fixture="tests/documents/scientific-article-body-missing-development.tex"
module="abntexto-ufc/articles.def"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup_job() {
  job="$1"
  rm -f "$job.aux" "$job.bbl" "$job.bcf" "$job.blg" "$job.log" "$job.out" \
    "$job.pdf" "$job.run.xml" "$job.toc" "$job.body.txt"
}

for token in \
  '\cs_new_protected:Npn \ufc_article_apply_body_typography:' \
  '\str_if_eq:VnT \g_ufc_document_type_tl {scientific-article}' \
  '\setlength{\parindent}{2cm}' \
  '\setlength{\parskip}{0pt}' \
  '\justifying'
do
  grep -Fq "$token" "$module" || {
    echo "Scientific article body gate failed: required profile-specific body token is missing: $token"
    exit 1
  }
done

# The body function must contain an explicit single-spacing route. Restrict the
# check to the function's source range rather than accepting singlesp used by
# the title or summary blocks.
body_source=$(sed -n '/\\cs_new_protected:Npn \\ufc_article_apply_body_typography:/,/^  }$/p' "$module")
printf '%s\n' "$body_source" | grep -Fq '\singlesp' || {
  echo 'Scientific article body gate failed: article-only body activation does not select single spacing.'
  exit 1
}

# Body activation belongs to the required article front-block completion
# boundary. This runs inside the document after shared startup initialization,
# without freezing an ineffective begin-document hook spelling.
front_source=$(sed -n '/\\NewDocumentCommand \\ufcPrintArticleFrontMatter/,/^  }$/p' "$module")
summary_line=$(printf '%s\n' "$front_source" | grep -nF '\ufc_article_primary_summary:n {#1}' | head -n 1 | cut -d: -f1 || true)
body_line=$(printf '%s\n' "$front_source" | grep -nF '\ufc_article_apply_body_typography:' | head -n 1 | cut -d: -f1 || true)
if [ -z "$summary_line" ] || [ -z "$body_line" ] || [ "$body_line" -le "$summary_line" ]; then
  echo 'Scientific article body gate failed: body typography is not activated after the required primary summary in the article front block.'
  exit 1
fi

if grep -Fq '\AddToHook{begindocument/end}{\ufc_article_apply_body_typography:}' "$module"; then
  echo 'Scientific article body gate failed: obsolete begin-document body activation route is still present.'
  exit 1
fi

compile_positive() {
  engine="$1"
  job="scientific-article-body-$engine"
  cleanup_job "$job"

  "$engine" -jobname="$job" $flags "$fixture" > "/tmp/$job.out" 2>&1 || {
    cat "/tmp/$job.out"
    exit 1
  }
  biber "$job" > "/tmp/$job-biber.out" 2>&1 || {
    cat "/tmp/$job-biber.out"
    exit 1
  }
  for pass in 1 2; do
    "$engine" -jobname="$job" $flags "$fixture" > "/tmp/$job.out" 2>&1 || {
      cat "/tmp/$job.out"
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Scientific article body gate failed: unrecognized warning or overflow with $engine."
    exit 1
  fi

  if grep -Eq 'WARN|ERROR' "$job.blg"; then
    cat "$job.blg"
    echo "Scientific article body gate failed: Biber reported a warning/error with $engine."
    exit 1
  fi

  [ -s "$job.pdf" ] || {
    echo "Scientific article body gate failed: PDF was not generated with $engine."
    exit 1
  }

  python3 tests/checks/scientific_article_body.py "$job.pdf"
}

for engine in pdflatex lualatex; do
  compile_positive "$engine"
done

negative_job="scientific-article-body-negative-pdflatex"
cleanup_job "$negative_job"
pdflatex -jobname="$negative_job" $flags "$negative_fixture" > "/tmp/$negative_job.out" 2>&1 || {
  cat "/tmp/$negative_job.out"
  exit 1
}
biber "$negative_job" > "/tmp/$negative_job-biber.out" 2>&1 || {
  cat "/tmp/$negative_job-biber.out"
  exit 1
}
for pass in 1 2; do
  pdflatex -jobname="$negative_job" $flags "$negative_fixture" > "/tmp/$negative_job.out" 2>&1 || {
    cat "/tmp/$negative_job.out"
    exit 1
  }
done

if python3 tests/checks/scientific_article_body.py "$negative_job.pdf" > "/tmp/$negative_job-check.out" 2>&1; then
  cat "/tmp/$negative_job-check.out"
  echo 'Scientific article body gate failed: missing-development negative fixture was accepted unexpectedly.'
  exit 1
fi
grep -Fq 'required article structure element is missing: desenvolvimento' "/tmp/$negative_job-check.out" || {
  cat "/tmp/$negative_job-check.out"
  echo 'Scientific article body gate failed: negative fixture was rejected for an unexpected reason.'
  exit 1
}

cleanup_job scientific-article-body-pdflatex
cleanup_job scientific-article-body-lualatex
cleanup_job "$negative_job"

echo 'ARTICLE-BODY-GATE-EVIDENCE status=PASS engines=2 required_structure=introduction,development,final-considerations,references body_typography=12pt,justified,2cm,single activation=required-front-block-completion negative_structure_rejected=true non_article_runtime_changed=false proof_state_promoted=0'
echo 'Scientific article body gate completed.'
