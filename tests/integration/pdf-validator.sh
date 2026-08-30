#!/bin/sh
set -eu

pdf="${1:-template/main.pdf}"
report="/tmp/abntexto-ufc-pdf-validator.json"

[ -f "$pdf" ] || {
  echo "PDF validator failed: file not found: $pdf"
  exit 1
}

python3 -m py_compile tools/validate-ufc-pdf.py
python3 - <<'PY'
import runpy
import sys

sys.path.insert(0, 'tools')
module = runpy.run_path('tools/validate-ufc-pdf.py', run_name='ufc_pdf_validator')


def font_status(names, profile):
    rows = [{'name': name, 'emb': 'yes', 'uni': 'yes'} for name in names]
    return module['check_fonts'](rows, profile)[-1].status


for names in (
    ['TimesNewRomanPSMT', 'NewTXMI', 'txsys'],
    ['ArialMT', 'TeXGyreTermesMath-Regular'],
):
    status = font_status(names, 'strict')
    if status != module['PASS']:
        raise SystemExit(f'literal text font with complementary math font should pass: {names}: {status}')

fallback = ['TeXGyreTermesX-Regular', 'NewTXMI']
if font_status(fallback, 'strict') != module['FAIL']:
    raise SystemExit('textual fallback should fail in the strict profile')
if font_status(fallback, 'portable') != module['WARN']:
    raise SystemExit('textual fallback should warn in the portable profile')
PY

set +e
python3 tools/validate-ufc-pdf.py "$pdf" --profile portable --format json --output "$report"
validator_status=$?
set -e

python3 - "$report" <<'PY'
import json
import sys

with open(sys.argv[1], encoding='utf-8') as handle:
    report = json.load(handle)
checks = {item['id']: item for item in report['checks']}
required = {
    'pdf.open',
    'layout.a4',
    'layout.margins',
    'font.embedded',
    'font.literal',
    'structure.cover',
    'structure.approval',
    'structure.resumo',
    'structure.abstract',
    'structure.toc',
    'structure.refs',
    'pdfa.claim',
}
missing = sorted(required - checks.keys())
if missing:
    raise SystemExit(f'missing validator checks: {missing}')
failed = [item for item in report['checks'] if item['mandatory'] and item['status'] == 'REPROVADO']
if failed:
    raise SystemExit('; '.join(f"{item['id']}: {item['evidence']}" for item in failed))
if checks['layout.margins']['status'] != 'APROVADO':
    raise SystemExit(checks['layout.margins']['evidence'])
if checks['font.literal']['status'] not in {'APROVADO', 'ALERTA'}:
    raise SystemExit('portable profile must not fail only because a textual fallback is used')
PY

if [ "$validator_status" -ne 0 ]; then
  echo "PDF validator failed with exit status $validator_status without a mandatory failure in the report."
  exit "$validator_status"
fi

echo 'PDF validator gate completed.'
