#!/bin/sh
set -eu

fixture="tests/normativa/matematica.tex"
tmp="ufctex-matematica.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f "$tmp" matematica-*.aux matematica-*.log matematica-*.out matematica-*.pdf
  rm -f /tmp/matematica-*.html
}
trap cleanup EXIT INT TERM

for cmd in pdffonts pdftotext; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Matemática V2: comando ausente: $cmd"
    exit 1
  }
done

for engine in pdflatex lualatex; do
  for family in times arial; do
    sed "s/@UFC_FONT@/$family/g" "$fixture" > "$tmp"
    job="matematica-$family-$engine"
    echo "Validando política matemática $family com $engine..."

    for pass in 1 2; do
      "$engine" -jobname="$job" $flags "$tmp" > "/tmp/$job.out" 2>&1 || {
        cat "/tmp/$job.out"
        exit 1
      }
    done

    case "$engine" in
      pdflatex)
        grep -Fq 'UFC-MATH-POLICY=NEW-TX-MATH' "$job.log" || {
          echo "$job: política newtxmath não confirmada."
          exit 1
        }
        pdffonts "$job.pdf" | tail -n +3 | awk 'NF {print $1}' | grep -Eiq 'ntx|txmi|txsy' || {
          echo "$job: fonte matemática NewTX não identificada no PDF."
          pdffonts "$job.pdf"
          exit 1
        }
        ;;
      lualatex)
        grep -Fq 'UFC-MATH-POLICY=TEX-GYRE-TERMES-MATH' "$job.log" || {
          echo "$job: política TeX Gyre Termes Math não confirmada."
          exit 1
        }
        pdffonts "$job.pdf" | tail -n +3 | awk 'NF {print $1}' | grep -Fq 'TeXGyreTermesMath' || {
          echo "$job: TeX Gyre Termes Math não identificada no PDF."
          pdffonts "$job.pdf"
          exit 1
        }
        ;;
    esac

    sh tests/v2-font-embedding-check.sh "$job.pdf"

    bbox="/tmp/$job.html"
    pdftotext -bbox-layout "$job.pdf" "$bbox"
    python3 - "$bbox" <<'PY'
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

path = Path(sys.argv[1])
root = ET.parse(path).getroot()

pages = [node for node in root.iter() if node.tag.endswith('page')]
if not pages:
    raise SystemExit('PDF sem página no bbox.')

page = pages[0]
page_width = float(page.attrib['width'])
words = []
for node in page.iter():
    if not node.tag.endswith('word'):
        continue
    text = ''.join(node.itertext()).strip()
    if not text:
        continue
    words.append((text, float(node.attrib['xMin']), float(node.attrib['xMax'])))

if not words:
    raise SystemExit('PDF sem palavras no bbox.')

if not any(text == '1' or '(1)' in text for text, _, _ in words):
    raise SystemExit('número da equação não identificado no bbox.')

rightmost = max(words, key=lambda item: item[2])
expected_right = page_width - 2.0 * 72.0 / 2.54
if abs(rightmost[2] - expected_right) > 4.0:
    raise SystemExit(
        f'número da equação não está alinhado à direita: '
        f'esperado xMax≈{expected_right:.2f}, obtido {rightmost[2]:.2f} ({rightmost[0]!r})'
    )
PY
  done
done

echo 'Gate V2 de matemática e equações concluído.'
