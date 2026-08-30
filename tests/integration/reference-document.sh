#!/bin/sh
set -eu

sh tests/integration/reference-guide-contract.sh

make clean
make compile

log="template/main.log"
pdf="template/main.pdf"
toc="template/main.toc"

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Underfull \\hbox|Overfull \\vbox' "$log" || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Reference document failed: review the warnings above.'
  exit 1
fi

sh tests/integration/font-embedding.sh "$pdf"

if command -v pdfinfo >/dev/null 2>&1; then
  metadata="/tmp/abntexto-ufc-reference-pdfa-meta.xml"
  pdfinfo -meta "$pdf" > "$metadata"
  grep -Eq '<pdfaid:part>2</pdfaid:part>' "$metadata" || {
    echo 'Reference document failed: PDF/A part 2 declaration is missing.'
    exit 1
  }
  grep -Eq '<pdfaid:conformance>[Bb]</pdfaid:conformance>' "$metadata" || {
    echo 'Reference document failed: PDF/A-2b conformance declaration is missing.'
    exit 1
  }
fi

python3 <<'PY'
import re
from pathlib import Path

cases = (
    ('template/frontmatter/summary.tex', r'\\palavraschave', 'Summary'),
    ('template/frontmatter/abstract.tex', r'\\keywords', 'Abstract'),
)

for path, marker, label in cases:
    source = Path(path).read_text(encoding='utf-8')
    body = re.split(marker, source, maxsplit=1)[0]
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*", body)
    if not 150 <= len(words) <= 500:
        raise SystemExit(f'{label} reference text outside the UFC 150–500 word range: {len(words)}')
PY

if command -v pdftotext >/dev/null 2>&1; then
  text="/tmp/abntexto-ufc-reference.txt"
  pdftotext "$pdf" "$text"
  for marker in 'RESUMO' 'ABSTRACT' 'LISTA DE ILUSTRAÇÕES' 'SUMÁRIO' 'INTRODUÇÃO' 'REFERÊNCIAS' 'GLOSSÁRIO' 'ÍNDICE'; do
    grep -Fq "$marker" "$text" || {
      echo "Reference document failed: rendered marker is missing: $marker"
      exit 1
    }
  done
fi

grep -Eiq 'Introdu' "$toc" || {
  echo 'Reference document failed: the textual section is missing from the table of contents.'
  exit 1
}

python3 <<'PY'
import re
from pathlib import Path

toc = Path('template/main.toc').read_text(encoding='utf-8', errors='replace')
for title in ('RESUMO', 'ABSTRACT', 'LISTA DE ILUSTRAÇÕES'):
    pattern = re.compile(
        r'\\contentsline\s*\{[^}]+\}\s*\{' + re.escape(title) + r'\}\s*\{',
        re.IGNORECASE,
    )
    if pattern.search(toc):
        raise SystemExit(f'Reference document failed: front-matter element entered the table of contents: {title}')
PY

echo 'Reference document validated.'
