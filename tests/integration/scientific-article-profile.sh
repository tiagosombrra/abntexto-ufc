#!/bin/sh
set -eu

fixture="tests/documents/scientific-article-profile.tex"

cleanup_job() {
  job="$1"
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc"
}

for engine in pdflatex lualatex; do
  job="scientific-article-profile-$engine"
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
    echo "Scientific article profile preflight failed: unrecognized warning or overflow with $engine."
    exit 1
  fi

  grep -Fq 'ARTICLE-PROFILE-TYPE=scientific-article' "$job.log" || {
    echo "Scientific article profile preflight failed: canonical document type was not selected with $engine."
    exit 1
  }
  grep -Fq 'ARTICLE-PROFILE-SUBMISSION=2026-09-01' "$job.log" || {
    echo "Scientific article profile preflight failed: submission-date metadata was not preserved with $engine."
    exit 1
  }
  grep -Fq 'ARTICLE-PROFILE-APPROVAL=2026-09-05' "$job.log" || {
    echo "Scientific article profile preflight failed: approval-date metadata was not preserved with $engine."
    exit 1
  }
  grep -Fq 'ARTICLE-PROFILE-AUTHOR-NOTE=ArticleAuthorNoteMarker' "$job.log" || {
    echo "Scientific article profile preflight failed: article-author-note metadata was not preserved with $engine."
    exit 1
  }

  [ -s "$job.pdf" ] || {
    echo "Scientific article profile preflight failed: PDF was not generated with $engine."
    exit 1
  }

  pdftotext -layout "$job.pdf" "/tmp/$job.txt"
  grep -Fq 'ARTICLEPROFILEBODY' "/tmp/$job.txt" || {
    echo "Scientific article profile preflight failed: controlled body marker is missing with $engine."
    exit 1
  }
done

cleanup_job scientific-article-profile-pdflatex
cleanup_job scientific-article-profile-lualatex

echo 'ARTICLE-PROFILE-EVIDENCE status=PASS engines=2 canonical_type=scientific-article metadata=submission-date,approval-date,article-author-note presentation_rules_promoted=0'

# Step 2 adds rendered evidence without promoting contract modality or proof state.
sh tests/integration/scientific-article-front-block.sh

echo 'Scientific article profile gate completed.'
