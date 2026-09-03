#!/bin/sh
set -eu

source_fixture="tests/documents/backmatter.tex"
tmp_fixture=".abntexto-ufc-posttextual-duplex.tex"
job="postextuais-duplex"

cleanup() {
  rm -f "$tmp_fixture" "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".glg \
        "$job".glo "$job".gls "$job".idx "$job".ilg "$job".ind "$job".ist \
        "$job".log "$job".out "$job".pdf "$job".run.xml "$job".toc
}
trap cleanup EXIT INT TERM

sed 's/print-mode = single-sided/print-mode = double-sided/' "$source_fixture" > "$tmp_fixture"

pdflatex -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$tmp_fixture" > /tmp/abntexto-ufc-post-duplex.log 2>&1 || {
  cat /tmp/abntexto-ufc-post-duplex.log
  exit 1
}
biber "$job" > /tmp/abntexto-ufc-post-duplex-biber.log 2>&1 || {
  cat /tmp/abntexto-ufc-post-duplex-biber.log
  exit 1
}
makeglossaries "$job" > /tmp/abntexto-ufc-post-duplex-glossary.log 2>&1 || {
  cat /tmp/abntexto-ufc-post-duplex-glossary.log
  exit 1
}
makeindex "$job" > /tmp/abntexto-ufc-post-duplex-index.log 2>&1 || {
  cat /tmp/abntexto-ufc-post-duplex-index.log
  exit 1
}
for pass in 1 2 3; do
  pdflatex -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$tmp_fixture" > /tmp/abntexto-ufc-post-duplex.log 2>&1 || {
    cat /tmp/abntexto-ufc-post-duplex.log
    exit 1
  }
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Pós-textuais duplex contêm warning ou overflow não reconhecido.'
  exit 1
fi

pdftotext -layout "$job.pdf" "/tmp/$job.txt"
python3 - "$job" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

job = sys.argv[1]
raw = Path(f'/tmp/{job}.txt').read_text(encoding='utf-8')
pages = raw.split('\f')
if pages and not pages[-1].strip():
    pages.pop()

normalized = []
for page in pages:
    page = re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', page)
    page = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', page)).strip().casefold()
    normalized.append(page)

checks = (
    ('silva, joão carlos', 'Referências'),
    ('discretização de um domínio geométrico', 'Glossário'),
    ('conteúdo do apêndice de validação', 'Apêndice'),
    ('conteúdo do anexo de validação', 'Anexo'),
)

for marker, label in checks:
    matches = [i + 1 for i, page in enumerate(normalized) if marker in page]
    if not matches:
        raise SystemExit(f'{job}: marker pós-textual missing: {label}')
    if matches[0] % 2 == 0:
        raise SystemExit(f'{job}: {label} iniciou in the verso, page física {matches[0]}')

index_pages = [i + 1 for i, page in enumerate(normalized) if 'índice' in page]
if not index_pages:
    raise SystemExit(f'{job}: index missing')
if index_pages[-1] % 2 == 0:
    raise SystemExit(f'{job}: index iniciou in the verso, page física {index_pages[-1]}')

print(f'{job}: pós-textuais auditados iniciam no anverso.')
PY

echo 'Pós-textuais duplex gate completed.'
