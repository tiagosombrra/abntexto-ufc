#!/bin/sh
set -eu

recommended_fixture="tests/documents/scientific-article-recommendations-recommended.tex"
outside_fixture="tests/documents/scientific-article-recommendations-outside.tex"

cleanup_job() {
  job="$1"
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc" "$job.txt"
}

python3 tests/checks/scientific_article_recommendations_contract.py

for engine in pdflatex lualatex; do
  for scenario in recommended outside; do
    case "$scenario" in
      recommended)
        fixture="$recommended_fixture"
        marker="ARTICLEADVISORYSUMMARYOK"
        ;;
      outside)
        fixture="$outside_fixture"
        marker="ARTICLEADVISORYOUTSIDEPARAONE"
        ;;
      *)
        echo "Scientific article recommendation gate failed: unknown scenario $scenario."
        exit 1
        ;;
    esac

    job="scientific-article-recommendations-$scenario-$engine"
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
      echo "Scientific article recommendation gate failed: unrecognized warning or overflow for $scenario with $engine."
      exit 1
    fi

    [ -s "$job.pdf" ] || {
      echo "Scientific article recommendation gate failed: PDF was not generated for $scenario with $engine."
      exit 1
    }

    pdftotext -layout "$job.pdf" "$job.txt"
    grep -Fq "$marker" "$job.txt" || {
      echo "Scientific article recommendation gate failed: rendered marker $marker is missing for $scenario with $engine."
      exit 1
    }
    if [ "$scenario" = "outside" ]; then
      grep -Fq 'ARTICLEADVISORYOUTSIDEPARATWO' "$job.txt" || {
        echo "Scientific article recommendation gate failed: second outside-recommendation paragraph was not rendered with $engine."
        exit 1
      }
    fi
  done
done

for engine in pdflatex lualatex; do
  cleanup_job "scientific-article-recommendations-recommended-$engine"
  cleanup_job "scientific-article-recommendations-outside-$engine"
done

echo 'ARTICLE-RECOMMENDATION-EVIDENCE status=PASS engines=2 scenarios=2 recommended_scenario_compiled=true outside_recommendation_compiled=true short_summary_accepted=true multi_paragraph_summary_accepted=true fewer_than_three_keywords_accepted=true author_alignment_default=right recommendation_hard_failures=0 journal_precedence=conditional-manual proof_state_promoted=0'
echo 'Scientific article recommendation and conditional-applicability gate completed.'
