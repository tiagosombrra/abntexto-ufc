#!/bin/sh
set -eu

academic_fixture="tests/documents/frontmatter-cover-academic-test.tex"
project_fixture="tests/documents/frontmatter-cover-project-optional-test.tex"
anonymized_fixture="tests/documents/frontmatter-cover-project-anonymized-optional-test.tex"
filled_department_fixture="/tmp/abntexto-ufc-frontmatter-cover-department-filled.tex"
academic_job="frontmatter-validation-cover-academic"
filled_department_job="frontmatter-validation-cover-department-filled"
project_job="frontmatter-validation-cover-project-optional"
anonymized_job="frontmatter-validation-cover-project-anonymized-optional"
evidence="artifacts/frontmatter/cover.json"

cleanup() {
  for job in "$academic_job" "$filled_department_job" "$project_job" "$anonymized_job"; do
    rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc"
    rm -f "$job"-*.png "$job"-*.jpg "$job"-*.ppm "$job".xml
  done
  rm -f "$filled_department_fixture"
}
trap cleanup EXIT INT TERM

compile_fixture() {
  fixture="$1"
  job="$2"
  log="/tmp/abntexto-ufc-${job}.log"

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

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Cover audit failed: unrecognized warning or overflow in $fixture."
    exit 1
  fi
}

compile_fixture "$academic_fixture" "$academic_job"

python3 - "$academic_fixture" "$filled_department_fixture" <<'PY'
import sys
from pathlib import Path

source_path = Path(sys.argv[1])
target_path = Path(sys.argv[2])
source = source_path.read_text(encoding='utf-8')
needle = '  institution = {UFCFRONTMATTERCOVINST},\n'
replacement = needle + '  department = {UFCFRONTMATTERCOVDEPT},\n'
if source.count(needle) != 1:
    raise SystemExit('Cover audit failed: academic fixture institution insertion point drifted.')
target_path.write_text(source.replace(needle, replacement), encoding='utf-8')
PY

compile_fixture "$filled_department_fixture" "$filled_department_job"
compile_fixture "$project_fixture" "$project_job"
compile_fixture "$anonymized_fixture" "$anonymized_job"

pdftotext -layout "$academic_job.pdf" /tmp/abntexto-ufc-cover-department-blank.txt
pdftotext -layout "$filled_department_job.pdf" /tmp/abntexto-ufc-cover-department-filled.txt
python3 - <<'PY'
import re
import unicodedata
from pathlib import Path

blank = unicodedata.normalize(
    'NFC', Path('/tmp/abntexto-ufc-cover-department-blank.txt').read_text(encoding='utf-8')
)
filled = unicodedata.normalize(
    'NFC', Path('/tmp/abntexto-ufc-cover-department-filled.txt').read_text(encoding='utf-8')
)
blank = re.sub(r'\s+', ' ', blank)
filled = re.sub(r'\s+', ' ', filled)
marker = 'UFCFRONTMATTERCOVDEPT'
if marker in blank:
    raise SystemExit('Cover audit failed: blank department unexpectedly rendered.')
if marker not in filled:
    raise SystemExit('Cover audit failed: filled department did not render.')
print(
    'LIBRARIAN-REVIEW-EVIDENCE item=1 status=PASS '
    'context=academic-cover blank_department_omitted=true filled_department_rendered=true'
)
PY

mkdir -p "$(dirname "$evidence")"
python3 tests/checks/normative_frontmatter_cover.py \
  "$academic_job.pdf" \
  "$project_job.pdf" \
  "$anonymized_job.pdf" \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}" \
  --enforce

test -s "$evidence" || {
  echo 'Cover audit failed: JSON evidence was not generated.'
  exit 1
}

echo 'Evidence front matter for cover gate completed.'
