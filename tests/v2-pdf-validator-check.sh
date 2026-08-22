#!/bin/sh
set -eu
pdf="${1:-documento.pdf}"
report="/tmp/ufctex-v2-pdf-validator.json"
[ -f "$pdf" ] || { echo "Validador PDF V2 falhou: $pdf não existe."; exit 1; }
python3 -m py_compile tools/validate-ufc-pdf.py
python3 tools/validate-ufc-pdf.py "$pdf" --profile portable --format json --output "$report"
python3 - "$report" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding='utf-8')); c={x['id']:x for x in r['checks']}
needed={'pdf.open','layout.a4','layout.margins','font.embedded','font.literal','structure.cover','structure.approval','structure.resumo','structure.abstract','structure.toc','structure.refs','pdfa.claim'}
missing=sorted(needed-c.keys())
if missing: raise SystemExit(f'checks ausentes: {missing}')
bad=[x for x in r['checks'] if x['mandatory'] and x['status']=='REPROVADO']
if bad: raise SystemExit('; '.join(f"{x['id']}: {x['evidence']}" for x in bad))
if c['layout.margins']['status']!='APROVADO': raise SystemExit(c['layout.margins']['evidence'])
if c['font.literal']['status'] not in {'APROVADO','ALERTA'}: raise SystemExit('perfil portátil não deve reprovar apenas por fallback tipográfico')
PY
echo 'Gate V2 do validador de PDF concluído.'
