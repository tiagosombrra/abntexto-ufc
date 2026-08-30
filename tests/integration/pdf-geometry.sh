#!/bin/sh
set -eu

fixture="tests/documents/pdf-geometry.tex"
tmp_fixture=".abntexto-ufc-geometry.tex"
log="/tmp/abntexto-ufc-geometry.log"

cleanup() {
  rm -f "$tmp_fixture" geometry-single-sided.* geometry-double-sided.*
}
trap cleanup EXIT INT TERM

build_mode() {
  label=$1
  runtime_value=$2
  job="geometry-$label"
  sed "s/@UFC_PRINT@/$runtime_value/g" "$fixture" > "$tmp_fixture"

  echo "Validating PDF geometry: $label..."
  for pass in 1 2; do
    pdflatex -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$tmp_fixture" > "$log" 2>&1 || {
      cat "$log"
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "PDF geometry failed: $label contains an unrecognized warning or overflow."
    exit 1
  fi

  pdfinfo "$job.pdf" > "$job.info"
  pdftotext -bbox "$job.pdf" "$job.html"
}

# Portuguese values below are the current runtime contract and are migrated in R2.
build_mode single-sided anverso
build_mode double-sided frente-verso

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
        pages.append({'width': float(elem.attrib['width']), 'height': float(elem.attrib['height']), 'words': words})
    return pages


def close(actual, expected, tolerance, label):
    if abs(actual - expected) > tolerance:
        raise SystemExit(f'{label}: expected {expected:.2f} pt, observed {actual:.2f} pt')


def find(page, text):
    matches = [word for word in page['words'] if word['text'] == text]
    if len(matches) != 1:
        raise SystemExit(f'{text}: expected one marker, observed {len(matches)}')
    return matches[0]


def page_number(page, expected):
    matches = [word for word in page['words'] if word['text'] == str(expected) and word['yMin'] < 80.0]
    if len(matches) != 1:
        raise SystemExit(f'Page {expected}: expected one header page number, observed {len(matches)}')
    return matches[0]


def validate_page_margins(mode, page, page_index, left_marker, right_marker):
    left = find(page, left_marker)
    right = find(page, right_marker)

    if mode == 'single-sided' or page_index % 2 == 1:
        close(left['xMin'], M3, POS_TOL, f'{mode}/p{page_index} left margin')
        close(right['xMax'], A4_W - M2, POS_TOL, f'{mode}/p{page_index} right margin')
    else:
        close(left['xMin'], M2, POS_TOL, f'{mode}/p{page_index} outer left margin')
        close(right['xMax'], A4_W - M3, POS_TOL, f'{mode}/p{page_index} inner right margin')

    if not (78.0 <= left['yMin'] <= 105.0):
        raise SystemExit(f'{mode}/p{page_index} top margin outside expected range: y={left["yMin"]:.2f} pt')


def validate(mode):
    pages = pages_from(f'geometry-{mode}.html')
    if len(pages) != 4:
        raise SystemExit(f'{mode}: expected 4 pages, observed {len(pages)}')

    for index, page in enumerate(pages, 1):
        close(page['width'], A4_W, SIZE_TOL, f'{mode}/p{index} A4 width')
        close(page['height'], A4_H, SIZE_TOL, f'{mode}/p{index} A4 height')

    validate_page_margins(mode, pages[0], 1, 'UFCLEFTPREONE', 'UFCRIGHTPREONE')
    validate_page_margins(mode, pages[1], 2, 'UFCLEFTPRETWO', 'UFCRIGHTPRETWO')
    validate_page_margins(mode, pages[2], 3, 'UFCLEFTTEXTONE', 'UFCRIGHTTEXTONE')
    validate_page_margins(mode, pages[3], 4, 'UFCLEFTTEXTTWO', 'UFCRIGHTTEXTTWO')

    n3 = page_number(pages[2], 3)
    n4 = page_number(pages[3], 4)
    for page_index, number in ((3, n3), (4, n4)):
        if not (42.0 <= number['yMin'] <= 72.0):
            raise SystemExit(f'{mode}/p{page_index} page-number vertical position outside expected range: y={number["yMin"]:.2f} pt')

    close(n3['xMax'], A4_W - M2, 7.0, f'{mode}/p3 right page number')
    if mode == 'single-sided':
        close(n4['xMax'], A4_W - M2, 7.0, 'single-sided/p4 right page number')
    else:
        close(n4['xMin'], M2, 7.0, 'double-sided/p4 left page number')


for mode in ('single-sided', 'double-sided'):
    validate(mode)

print('PDF geometry measurement completed.')
PY

sh tests/integration/page-margins-evidence.sh
sh tests/integration/pagination-geometry-evidence.sh

echo 'PDF geometry gate completed.'
