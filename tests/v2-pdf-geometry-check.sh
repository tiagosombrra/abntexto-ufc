#!/bin/sh
set -eu

fixture="tests/normativa/geometria-pdf.tex"
tmp_fixture=".abntexto-ufc-v2-geometry.tex"

cleanup() {
  rm -f "$tmp_fixture" geometry-anverso.* geometry-frente-verso.*
}
trap cleanup EXIT INT TERM

for mode in anverso frente-verso; do
  job="geometry-$mode"
  sed "s/@UFC_PRINT@/$mode/g" "$fixture" > "$tmp_fixture"

  echo "Validando geometria PDF: $mode..."
  for pass in 1 2; do
    pdflatex -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$tmp_fixture" > /tmp/abntexto-ufc-v2-geometry.log 2>&1 || {
      cat /tmp/abntexto-ufc-v2-geometry.log
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Geometria V2 falhou: $mode contém warning ou overflow não reconhecido."
    exit 1
  fi

  pdfinfo "$job.pdf" > "$job.info"
  pdftotext -bbox "$job.pdf" "$job.html"
done

python3 <<'PY'
import xml.etree.ElementTree as ET

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


def validate_page_margins(mode, page, page_idx, left_marker, right_marker):
    left = find(page, left_marker)
    right = find(page, right_marker)

    if mode == 'anverso' or page_idx % 2 == 1:
        close(left['xMin'], M3, POS_TOL, f'{mode}/p{page_idx} margem esquerda')
        close(right['xMax'], A4_W - M2, POS_TOL, f'{mode}/p{page_idx} margem direita')
    else:
        close(left['xMin'], M2, POS_TOL, f'{mode}/p{page_idx} margem esquerda externa')
        close(right['xMax'], A4_W - M3, POS_TOL, f'{mode}/p{page_idx} margem direita interna')

    if not (78.0 <= left['yMin'] <= 105.0):
        raise SystemExit(f'{mode}/p{page_idx} margem superior fora da faixa: y={left["yMin"]:.2f} pt')


def validate(mode):
    pages = pages_from(f'geometry-{mode}.html')
    if len(pages) != 4:
        raise SystemExit(f'{mode}: esperado PDF de 4 páginas, obtido {len(pages)}')

    for i, page in enumerate(pages, 1):
        close(page['width'], A4_W, SIZE_TOL, f'{mode}/p{i} largura A4')
        close(page['height'], A4_H, SIZE_TOL, f'{mode}/p{i} altura A4')

    validate_page_margins(mode, pages[0], 1, 'UFCLEFTPREONE', 'UFCRIGHTPREONE')
    validate_page_margins(mode, pages[1], 2, 'UFCLEFTPRETWO', 'UFCRIGHTPRETWO')
    validate_page_margins(mode, pages[2], 3, 'UFCLEFTTEXTONE', 'UFCRIGHTTEXTONE')
    validate_page_margins(mode, pages[3], 4, 'UFCLEFTTEXTTWO', 'UFCRIGHTTEXTTWO')

    n3 = page_number(pages[2], 3)
    n4 = page_number(pages[3], 4)
    for page_idx, n in ((3, n3), (4, n4)):
        if not (42.0 <= n['yMin'] <= 72.0):
            raise SystemExit(f'{mode}/p{page_idx} paginação vertical fora da faixa: y={n["yMin"]:.2f} pt')

    close(n3['xMax'], A4_W - M2, 7.0, f'{mode}/p3 paginação direita')
    if mode == 'anverso':
        close(n4['xMax'], A4_W - M2, 7.0, 'anverso/p4 paginação direita')
    else:
        close(n4['xMin'], M2, 7.0, 'frente-verso/p4 paginação esquerda')

for mode in ('anverso', 'frente-verso'):
    validate(mode)

print('Gate V2 de geometria PDF concluído.')
PY

sh tests/v2-page-margins-evidence-check.sh
