#!/bin/sh
set -eu

fixture="tests/normativa/tipografia-codigo.tex"
tmp="ufctex-code-typography.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f "$tmp" tipografia-codigo-*.aux tipografia-codigo-*.log tipografia-codigo-*.out tipografia-codigo-*.pdf
  rm -f tipografia-codigo-*.loa tipografia-codigo-*.loc
}
trap cleanup EXIT INT TERM

for engine in pdflatex lualatex; do
  for family in times arial; do
    sed "s/@UFC_FONT@/$family/g" "$fixture" > "$tmp"
    job="tipografia-codigo-$family-$engine"
    echo "Validando tipografia de código/algoritmo $family com $engine..."

    "$engine" -jobname="$job" $flags "$tmp" > "/tmp/$job.out" 2>&1 || {
      cat "/tmp/$job.out"
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


def scalar(name):
    value = marker(name)
    try:
        return float(value)
    except ValueError as exc:
        raise SystemExit(f'{name}: valor inválido: {value}') from exc


def normalize_family(value):
    return re.sub(r'\([0-9]+\)$', '', value)

text_family = normalize_family(marker('UFC-TEXT-FAMILY'))
code_family = normalize_family(marker('UFC-CODE-FAMILY'))
algorithm_family = normalize_family(marker('UFC-ALGORITHM-FAMILY'))

if code_family != text_family:
    raise SystemExit(f'código mudou de família: texto={text_family}, código={code_family}')
if algorithm_family != text_family:
    raise SystemExit(f'algoritmo mudou de família: texto={text_family}, algoritmo={algorithm_family}')

for name in ('UFC-TEXT-FONTSIZE', 'UFC-CODE-FONTSIZE', 'UFC-ALGORITHM-FONTSIZE'):
    actual = scalar(name)
    if abs(actual - 12.0) > 0.1:
        raise SystemExit(f'{name}: esperado 12 pt nominal, obtido {actual:.4f}')
PY

    pdftotext -bbox-layout "$job.pdf" "/tmp/$job-bbox.html"
    python3 - "/tmp/$job-bbox.html" <<'PY'
import re
import sys
import xml.etree.ElementTree as ET

A4_WIDTH = 595.276
CM = 72.0 / 2.54
LEFT = 3 * CM
RIGHT = 2 * CM
TOL = 1.5

root = ET.parse(sys.argv[1]).getroot()
local = lambda tag: tag.rsplit('}', 1)[-1]


def compact(value):
    return re.sub(r'[^A-Z0-9]', '', value.upper())


def locate(marker):
    target = compact(marker)
    for line in (node for node in root.iter() if local(node.tag) == 'line'):
        words = [node for node in line if local(node.tag) == 'word']
        if not words:
            continue
        text = ''.join(''.join(word.itertext()) for word in words)
        if target in compact(text):
            return (
                min(float(word.attrib['xMin']) for word in words),
                max(float(word.attrib['xMax']) for word in words),
            )
    raise SystemExit(f'marcador geométrico ausente: {marker}')

for marker in ('UFC-CODE-GEOMETRY-MARKER', 'UFC-ALGORITHM-GEOMETRY-MARKER'):
    x0, x1 = locate(marker)
    if x0 < LEFT - TOL:
        raise SystemExit(f'{marker}: conteúdo/numeração invade margem esquerda: x={x0:.2f}, limite={LEFT:.2f}')
    if x1 > A4_WIDTH - RIGHT + TOL:
        raise SystemExit(f'{marker}: conteúdo/numeração invade margem direita: x={x1:.2f}, limite={A4_WIDTH - RIGHT:.2f}')
PY

    sh tests/v2-font-embedding-check.sh "$job.pdf"
  done
done

echo 'Gate V2 de tipografia e geometria de código e algoritmos concluído.'
