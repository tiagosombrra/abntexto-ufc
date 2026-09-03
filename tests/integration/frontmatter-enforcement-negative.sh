#!/bin/sh
set -eu

fixture="tests/documents/frontmatter-enforcement-negative-test.tex"
job="frontmatter-validation-enforcement-negative"
evidence="/tmp/abntexto-ufc-frontmatter-enforcement-negative.json"
log="/tmp/abntexto-ufc-frontmatter-enforcement-negative.log"

cleanup() {
  rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc" "$evidence" "$log"
}
trap cleanup EXIT INT TERM

for pass in 1 2; do
  pdflatex \
    -jobname="$job" \
    -interaction=nonstopmode \
    -halt-on-error \
    -file-line-error \
    "$fixture" > "$log" 2>&1 || {
      cat "$log"
      exit 1
    }
done

if python3 tests/checks/frontmatter_evidence.py \
  "$job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}" \
  --enforce > "$log" 2>&1; then
  echo 'Front matter enforcement negative path failed: invalid dedication was accepted.'
  cat "$log"
  exit 1
fi

python3 - "$evidence" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.is_file():
    raise SystemExit("negative-path evidence was not generated")
payload = json.loads(path.read_text(encoding="utf-8"))
if payload.get("mode") != "enforce":
    raise SystemExit(f"expected enforce mode, found {payload.get('mode')!r}")
findings = payload.get("findings", [])
if "dedication.position.start" not in findings:
    raise SystemExit(
        "negative path did not fail on dedication.position.start: "
        + ", ".join(findings)
    )
print(
    "FRONTMATTER-NEGATIVE-EVIDENCE status=PASS "
    "rejected_rule=dedication.position.start"
)
PY

echo 'Front matter enforcement negative path completed.'
