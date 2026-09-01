#!/bin/sh
set -eu

log="citacoes-referencias.log"
[ -f "$log" ] || {
  echo "Referências falharam: log ausente: $log"
  exit 1
}

python3 - "$log" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')


def metric(name):
    match = re.search(rf'{re.escape(name)}=([0-9.]+)', text)
    if not match:
        raise SystemExit(f'Referências: métrica ausente no log: {name}')
    return float(match.group(1))

itemsep = metric('UFC-BIBITEMSEP')
actual_itemsep = metric('UFC-BIBACTUALITEMSEP')
baseline = metric('UFC-BIBBASELINE')
stretch = metric('UFC-BIBSTRETCH')

if baseline <= 0:
    raise SystemExit('Referências: entrelinha inválida.')

for name, value in (
    ('bibitemsep', itemsep),
    ('itemsep efetivo', actual_itemsep),
):
    ratio = value / baseline
    if not 0.99 <= ratio <= 1.01:
        raise SystemExit(
            f'Referências: {name} deve equivaler a uma linha simples; razão={ratio:.4f}'
        )

if not 0.99 <= stretch <= 1.01:
    raise SystemExit(
        f'Referências: espaçamento interno deve ser simples; baselinestretch={stretch:.4f}'
    )

print('Gate de espaçamento das referências concluído.')
PY

sh tests/integration/reference-layout-evidence.sh
