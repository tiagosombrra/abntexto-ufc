#!/bin/sh
set -eu

fixture="tests/normativa/objetos-minted.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

if ! command -v latexminted >/dev/null 2>&1; then
  echo 'latexminted não disponível; rota minted não executada neste ambiente.'
  exit 0
fi

cleanup() {
  rm -f objetos-minted-*.aux objetos-minted-*.log objetos-minted-*.out objetos-minted-*.pdf objetos-minted-*.loc
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  job="objetos-minted-$engine"
  echo "Validando $fixture com $engine..."
  for pass in 1 2; do
    "$engine" -jobname="$job" -shell-escape $flags "$fixture" > /tmp/ufctex-v2-minted.log 2>&1 || {
      cat /tmp/ufctex-v2-minted.log
      exit 1
    }
  done

  overflow=$(grep -E 'Overfull \\hbox|Overfull \\vbox' "$job.log" || true)
  if [ -n "$overflow" ]; then
    printf '%s\n' "$overflow"
    echo "$job: fixture minted contém overflow."
    exit 1
  fi

  grep -Fq 'Arquivo Python com minted' "$job.loc" || {
    echo "$job: minted ausente da lista de códigos."
    exit 1
  }

  python3 - "$job.log" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')


def marker(name):
    match = re.search(rf'{re.escape(name)}=([^\r\n]+)', text)
    if not match:
        raise SystemExit(f'marcador ausente: {name}')
    return match.group(1).strip()

text_family = marker('UFC-MINTED-TEXT-FAMILY')
minted_family = marker('UFC-MINTED-FAMILY')
if minted_family != text_family:
    raise SystemExit(f'minted mudou de família: texto={text_family}, minted={minted_family}')

pt_per_bp = 72.27 / 72.0
expected = 12.0 * pt_per_bp
for name in ('UFC-MINTED-TEXT-FONTSIZE', 'UFC-MINTED-FONTSIZE'):
    actual = float(marker(name))
    if abs(actual - expected) > 0.06:
        raise SystemExit(f'{name}: esperado {expected:.4f}, obtido {actual:.4f}')
PY

  sh tests/v2-font-embedding-check.sh "$job.pdf"
done

echo 'Gate V2 de minted concluído.'
