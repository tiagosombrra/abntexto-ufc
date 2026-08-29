#!/bin/sh
set -eu

fixture="tests/smoke/perfil-artigo.tex"
canonical_pdflatex="artigo-canonical-pdflatex"
legacy_pdflatex="artigo-legacy-pdflatex"

cleanup_job() {
  job="$1"
  rm -f "$job".tex "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
    "$job".out "$job".toc "$job".run.xml "$job".pdf
}

cleanup_aux() {
  job="$1"
  rm -f "$job".tex "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
    "$job".out "$job".toc "$job".run.xml
}

cleanup() {
  # Preserve the generated PDFs for the host-side veraPDF gate that follows
  # the TeX Live container step in latex-preflight.yml.
  cleanup_aux "$canonical_pdflatex"
  cleanup_aux "artigo-canonical-lualatex"
  cleanup_aux "$legacy_pdflatex"
  rm -f /tmp/artigo-*.txt /tmp/artigo-*.html /tmp/artigo-*.info /tmp/abntexto-ufc-v2-article.log
}
trap cleanup EXIT INT TERM

python3 tests/checks/article_runtime_contract.py

for engine in pdflatex lualatex; do
  job="artigo-canonical-$engine"
  cleanup_job "$job"
  cp "$fixture" "$job.tex"

  echo "Validando artigo científico canônico com $engine..."
  make filename="$job" ENGINE="$engine" compile > /tmp/abntexto-ufc-v2-article.log 2>&1 || {
    cat /tmp/abntexto-ufc-v2-article.log
    exit 1
  }

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Artigo V2 falhou: $engine contém warning ou overflow não reconhecido."
    exit 1
  fi

  if [ -f "$job.blg" ] && grep -Eq 'WARN|ERROR' "$job.blg"; then
    cat "$job.blg"
    echo "Artigo V2 falhou: Biber reportou warning/error em $engine."
    exit 1
  fi

  [ -s "$job.pdf" ] || {
    echo "Artigo V2 falhou: PDF canônico ausente para $engine."
    exit 1
  }

  sh tests/v2-font-embedding-check.sh "$job.pdf"
  pdfinfo "$job.pdf" > "/tmp/$job.info"
  pdftotext -layout "$job.pdf" "/tmp/$job.txt"
  pdftotext -bbox "$job.pdf" "/tmp/$job.html"
done

# Portuguese compatibility must exercise the same runtime behavior without
# expanding the frozen B2R public surface.
cleanup_job "$legacy_pdflatex"
sed 's/type = article,/tipo = artigo,/' "$fixture" > "$legacy_pdflatex.tex"
make filename="$legacy_pdflatex" ENGINE=pdflatex compile > /tmp/abntexto-ufc-v2-article.log 2>&1 || {
  cat /tmp/abntexto-ufc-v2-article.log
  exit 1
}

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$legacy_pdflatex.log" || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo "Artigo V2 falhou: compatibilidade tipo=artigo contém warning ou overflow."
  exit 1
fi

sh tests/v2-font-embedding-check.sh "$legacy_pdflatex.pdf"
pdftotext -layout "$legacy_pdflatex.pdf" "/tmp/$legacy_pdflatex.txt"
pdftotext -bbox "$legacy_pdflatex.pdf" "/tmp/$legacy_pdflatex.html"

cmp -s "/tmp/$canonical_pdflatex.txt" "/tmp/$legacy_pdflatex.txt" || {
  diff -u "/tmp/$canonical_pdflatex.txt" "/tmp/$legacy_pdflatex.txt" || true
  echo "Artigo V2 falhou: type=article e tipo=artigo divergiram em texto observável."
  exit 1
}

python3 - "$canonical_pdflatex" "$legacy_pdflatex" <<'PY'
from __future__ import annotations

import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

canonical, legacy = sys.argv[1:3]
PT_PER_CM = 72.0 / 2.54
A4_W = 21.0 * PT_PER_CM
A4_H = 29.7 * PT_PER_CM
M2 = 2.0 * PT_PER_CM
M3 = 3.0 * PT_PER_CM
TEXT_CENTER_X = (M3 + (A4_W - M2)) / 2.0


def normalize(path: str) -> str:
    raw = Path(path).read_text(encoding='utf-8')
    raw = re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', raw)
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', raw)).strip().casefold()


def pages(path: str):
    root = ET.parse(path).getroot()
    result = []
    for elem in root.iter():
        if elem.tag.rsplit('}', 1)[-1] != 'page':
            continue
        words = []
        for word in elem.iter():
            if word.tag.rsplit('}', 1)[-1] != 'word':
                continue
            words.append({
                'text': ''.join(word.itertext()),
                'xMin': float(word.attrib['xMin']),
                'yMin': float(word.attrib['yMin']),
                'xMax': float(word.attrib['xMax']),
                'yMax': float(word.attrib['yMax']),
            })
        result.append({
            'width': float(elem.attrib['width']),
            'height': float(elem.attrib['height']),
            'words': words,
        })
    return result


def find_word(page, token: str):
    target = token.casefold()
    matches = [
        word for word in page['words']
        if word['text'].strip('.,:;').casefold() == target
    ]
    if not matches:
        raise SystemExit(f'artigo: marcador bbox ausente: {token}')
    return matches[0]


def line_bounds(page, anchor, tolerance: float = 1.5):
    words = [
        word for word in page['words']
        if abs(word['yMin'] - anchor['yMin']) <= tolerance
    ]
    if not words:
        raise SystemExit('artigo: linha do título não pôde ser reconstruída')
    return min(word['xMin'] for word in words), max(word['xMax'] for word in words)


def page_index_for_token(all_pages, token: str) -> int:
    for index, page in enumerate(all_pages, 1):
        if any(word['text'].strip('.,:;').casefold() == token.casefold() for word in page['words']):
            return index
    raise SystemExit(f'artigo: marcador sem página: {token}')

text = normalize(f'/tmp/{canonical}.txt')
legacy_text = normalize(f'/tmp/{legacy}.txt')
if text != legacy_text:
    raise SystemExit('artigo: aliases canônico e português não são semanticamente equivalentes')

required = (
    'ufcarticletitlemarker',
    'ufcarticleauthormarker',
    'data de submissão: 18 de agosto de 2026',
    'data de aprovação: 20 de agosto de 2026',
    'resumo',
    'ufcarticlesummarymarker',
    'palavras-chave: malhamento adaptativo; geometria computacional; compatibilidade.',
    'abstract',
    'ufcarticleabstractmarker',
    'keywords: adaptive meshing; computational geometry; compatibility.',
    'introdução',
    'desenvolvimento',
    'considerações finais',
    'referências',
    'fundamentos de metodologia acadêmica',
)
for marker in required:
    if marker not in text:
        raise SystemExit(f'artigo: conteúdo obrigatório ausente: {marker}')

for forbidden in ('sumário', 'banca examinadora', 'trabalho de conclusão de curso', 'tese apresentada', 'dissertação apresentada'):
    if forbidden in text:
        raise SystemExit(f'artigo: elemento de outro perfil apareceu indevidamente: {forbidden}')

article_pages = pages(f'/tmp/{canonical}.html')
legacy_pages = pages(f'/tmp/{legacy}.html')
if len(article_pages) < 2:
    raise SystemExit(f'artigo: esperado documento multipágina, obtido {len(article_pages)}')
if len(article_pages) != len(legacy_pages):
    raise SystemExit('artigo: aliases canônico/português divergiram em número de páginas')

for index, page in enumerate(article_pages, 1):
    if abs(page['width'] - A4_W) > 1.0 or abs(page['height'] - A4_H) > 1.0:
        raise SystemExit(f'artigo/p{index}: página não é A4')
    numbers = [
        word for word in page['words']
        if word['text'] == str(index) and word['yMin'] < 80.0
    ]
    if len(numbers) != 1:
        raise SystemExit(f'artigo/p{index}: paginação visível esperada desde a primeira página')
    number = numbers[0]
    if not 42.0 <= number['yMin'] <= 72.0:
        raise SystemExit(f'artigo/p{index}: paginação vertical fora da faixa: {number["yMin"]:.2f}')
    if abs(number['xMax'] - (A4_W - M2)) > 7.0:
        raise SystemExit(f'artigo/p{index}: paginação não está a 2 cm da borda direita')

first = article_pages[0]
title = find_word(first, 'UFCARTICLETITLEMARKER')
summary = find_word(first, 'UFCARTICLESUMMARYMARKER')
if not 78.0 <= title['yMin'] <= 115.0:
    raise SystemExit(f'artigo: título não inicia junto à margem superior: y={title["yMin"]:.2f}')
title_x_min, title_x_max = line_bounds(first, title)
if abs(((title_x_min + title_x_max) / 2.0) - TEXT_CENTER_X) > 7.0:
    raise SystemExit(
        'artigo: linha do título principal não está centralizada na área de texto: '
        f'xMin={title_x_min:.2f} xMax={title_x_max:.2f} center={TEXT_CENTER_X:.2f}'
    )
if summary['yMin'] <= title['yMin']:
    raise SystemExit('artigo: resumo não aparece após título/autoria/datas')

intro_page = page_index_for_token(article_pages, 'UFCARTICLEINTROMARKER')
flow_dev_page = page_index_for_token(article_pages, 'UFCARTICLEFLOWMARKERBEFOREDEVELOPMENT')
development_page = page_index_for_token(article_pages, 'UFCARTICLEDEVELOPMENTMARKER')
flow_final_page = page_index_for_token(article_pages, 'UFCARTICLEFLOWMARKERBEFOREFINAL')
final_page = page_index_for_token(article_pages, 'UFCARTICLEFINALMARKER')
if flow_dev_page != development_page:
    raise SystemExit('artigo: seção Desenvolvimento forçou nova página')
if flow_final_page != final_page:
    raise SystemExit('artigo: seção Considerações finais forçou nova página')

intro_marker = find_word(article_pages[intro_page - 1], 'UFCARTICLEINTROMARKER')
expected_indent_x = M3 + M2
if abs(intro_marker['xMin'] - expected_indent_x) > 8.0:
    raise SystemExit(
        f'artigo: recuo de primeira linha diferente de 2 cm: x={intro_marker["xMin"]:.2f}'
    )

print(
    'N15-EVIDENCE article-runtime '
    f'pages={len(article_pages)} a4=true margins=3-3-2-2 pagination=first-page-upper-right '
    'single-sided=true section-flow=continuous title-text-area-centered=true canonical-pt-equivalent=true '
    'pdfa=deferred-to-host-gate status=PASS'
)
PY

echo 'Gate V2 do runtime de artigo científico concluído.'
