#!/bin/sh
set -eu

fixture="tests/documents/frontmatter-dedication-epigraph-test.tex"
job="frontmatter-validation-dedication-epigraph"
evidence="artifacts/frontmatter/dedication-epigraph.json"

cleanup() {
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc"
}
trap cleanup EXIT INT TERM

for pass in 1 2; do
  pdflatex \
    -jobname="$job" \
    -interaction=nonstopmode \
    -halt-on-error \
    -file-line-error \
    "$fixture" > /tmp/abntexto-ufc-frontmatter-evidence.log 2>&1 || {
      cat /tmp/abntexto-ufc-frontmatter-evidence.log
      exit 1
    }
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Front matter audit failed: unrecognized warning or overflow.'
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/frontmatter_evidence.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}" \
  --enforce

test -s "$evidence" || {
  echo 'Front matter audit failed: JSON evidence was not generated.'
  exit 1
}

python3 - "$evidence" <<'PY'
import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
print(
    'FRONTMATTER-EVIDENCE summary '
    + ' '.join(f'{key}={value}' for key, value in sorted(payload['status_counts'].items()))
    + f" distinct_pages={payload['target_pages_are_distinct']}"
)
for scenario in payload['scenarios']:
    print(
        f"FRONTMATTER-EVIDENCE scenario={scenario['scenario_id']} page={scenario['page']} "
        f"lines={scenario['line_count_measured']}/{scenario['line_count_expected']}"
    )
    for item in scenario['evidence']:
        print(
            f"FRONTMATTER-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
PY

echo 'Evidence front matter for dedication and epigraphs gate completed.'
