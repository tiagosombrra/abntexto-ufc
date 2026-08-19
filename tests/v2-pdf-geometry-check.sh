#!/bin/sh
set -eu

fixture="tests/normativa/geometria-pdf.tex"
tmp_fixture=".ufctex-v2-geometry.tex"

cleanup() {
  rm -f "$tmp_fixture" geometry-anverso.* geometry-frente-verso.*
}
trap cleanup EXIT INT TERM

for mode in anverso frente-verso; do
  job="geometry-$mode"
  sed "s/@UFC_PRINT@/$mode/g" "$fixture" > "$tmp_fixture"

  echo "Validando geometria PDF: $mode..."
  for pass in 1 2; do
    pdflatex -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$tmp_fixture" > /tmp/ufctex-v2-geometry.log 2>&1 || {
      cat /tmp/ufctex-v2-geometry.log
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Geometria V2 falhou: $mode contém warning ou overflow não reconhecido."
    exit 1
  fi

  pdfinfo "$job.pdf" > "$job.info"
  pdftotext -bbox "$job.pdf" "$job.html"
done

python3 <<'PY'
import math
import xml.etree.ElementTree as ET
from pathlib import Path

PT_PER_CM = 72.0 / 2.54
A4_W = 21.0 * PT_PER_CM
A4_H = 29.7 * PT_PER_CM
M2 = 2.0 * PT_PER_CM
M3 = 3.0 * PT_PER_CM
POS_TOL = 5.0
SIZE_TOL = 1.0


def pages_from(path):
    root = ET.parse(path).getroot()
    pages = []
    for elem in root.iter():
        if elem.tag.rsplit('}', 1)[-1] != 'page':
            continue
        words = []
        for word in elem.iter():
            if word.tag.rsplit('}', 1)[-1] == 'word':
                words.append({
                    'text': ''.join(word.itertext()),
                    'xMin': float(word.attrib['xMin']),
                    'yMin': float(word.attrib['yMin']),
                    'xMax': float(word.attrib['xMax']),
                    'yMax': float(word.attrib['yMax']),
                })
        pages.append({
            'width': float(elem.attrib['width']),
            'height': float(elem.attrib['height']),
            'words': words,
        })
    return pages


def close(actual, expected, tol, label):
    if abs(actual - expected) > tol:
        raise SystemExit(f'{label}: esperado {expected:.2f} pt, obtido {actual:.2f} pt')


def find(page, text):
    matches = [w for w in page['words'] if w['text'] == text]
    if len(matches) != 1:
        raise SystemExit(f"Marcador {text}: esperado 1 ocorrência, obtido {len(matches)}")
    return matches[0]


def page_number(page, expected):
    matches = [
        w for w in page['words']
        if w['text'] == str(expected) and w['yMin'] < 80.0
    ]
    if len(matches) != 1:
        raise SystemExit(
            f'Paginação da página {expected}: esperado 1 número no cabeçalho, obtido {len(matches)}'
        )
    return matches[0]


def validate(mode):
    pages = pages_from(f'geometry-{mode}.html')
    if len(pages) != 3:
        raise SystemExit(f'{mode}: esperado PDF de 3 páginas, obtido {len(pages)}')

    for i, page in enumerate(pages, 1):
        close(page['width'], A4_W, SIZE_TOL, f'{mode}/p{i} largura A4')
        close(page['height'], A4_H, SIZE_TOL, f'{mode}/p{i} altura A4')

    # Markers are normal-flow text anchored to the text block itself.
    p1 = pages[0]
    left1 = find(p1, 'UFCLEFTONE')
    right1 = find(p1, 'UFCRIGHTONE')
    close(left1['xMin'], M3, POS_TOL, f'{mode}/p1 margem esquerda')
    close(right1['xMax'], A4_W - M2, POS_TOL, f'{mode}/p1 margem direita')
    if not (78.0 <= left1['yMin'] <= 105.0):
        raise SystemExit(f'{mode}/p1 margem superior fora da faixa: y={left1["yMin"]:.2f} pt')

    p2 = pages[1]
    left2 = find(p2, 'UFCLEFTTWO')
    right2 = find(p2, 'UFCRIGHTTWO')
    if mode == 'anverso':
        close(left2['xMin'], M3, POS_TOL, 'anverso/p2 margem esquerda')
        close(right2['xMax'], A4_W - M2, POS_TOL, 'anverso/p2 margem direita')
    else:
        close(left2['xMin'], M2, POS_TOL, 'frente-verso/p2 margem externa esquerda')
        close(right2['xMax'], A4_W - M3, POS_TOL, 'frente-verso/p2 margem interna direita')

    # Page numbers are measured from the rendered PDF header, not TeX dimensions.
    n2 = page_number(pages[1], 2)
    n3 = page_number(pages[2], 3)
    for page_idx, n in ((2, n2), (3, n3)):
        if not (42.0 <= n['yMin'] <= 72.0):
            raise SystemExit(f'{mode}/p{page_idx} paginação vertical fora da faixa: y={n["yMin"]:.2f} pt')

    if mode == 'anverso':
        close(n2['xMax'], A4_W - M2, 7.0, 'anverso/p2 paginação direita')
        close(n3['xMax'], A4_W - M2, 7.0, 'anverso/p3 paginação direita')
    else:
        close(n2['xMin'], M2, 7.0, 'frente-verso/p2 paginação esquerda')
        close(n3['xMax'], A4_W - M2, 7.0, 'frente-verso/p3 paginação direita')

for mode in ('anverso', 'frente-verso'):
    validate(mode)

print('Gate V2 de geometria PDF concluído.')
PY
