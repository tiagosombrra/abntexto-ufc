#!/bin/sh
set -eu

fixture="tests/normativa/pretextual-oracle-dedication-epigraph.tex"
job="pretextual-oracle-dedication-epigraph"
evidence="artifacts/normative-pretextual/dedication-epigraph.json"

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
    "$fixture" > /tmp/abntexto-ufc-v2-pretextual-evidence.log 2>&1 || {
      cat /tmp/abntexto-ufc-v2-pretextual-evidence.log
      exit 1
    }
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Auditoria pré-textual falhou: warning ou overflow não reconhecido.'
  exit 1
fi

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/pretextual_oracle.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"

test -s "$evidence" || {
  echo 'Auditoria pré-textual falhou: evidência JSON não foi gerada.'
  exit 1
}

python3 - "$evidence" <<'PY'
import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
print(
    'N6-EVIDENCE summary '
    + ' '.join(f'{key}={value}' for key, value in sorted(payload['status_counts'].items()))
    + f" distinct_pages={payload['target_pages_are_distinct']}"
)
for scenario in payload['scenarios']:
    print(
        f"N6-EVIDENCE scenario={scenario['scenario_id']} page={scenario['page']} "
        f"lines={scenario['line_count_measured']}/{scenario['line_count_expected']}"
    )
    for item in scenario['evidence']:
        print(
            f"N6-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
PY

echo 'Gate de evidência N6 para dedicatória e epígrafes concluído.'
