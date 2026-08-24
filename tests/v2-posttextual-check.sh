#!/bin/sh
set -eu

modern="tests/normativa/postextuais.tex"

cleanup_job() {
  job="$1"
  rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".glg "$job".glo \
        "$job".gls "$job".idx "$job".ilg "$job".ind "$job".ist "$job".log \
        "$job".out "$job".pdf "$job".run.xml "$job".toc
}

check_log() {
  job="$1"
  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Gate V2 falhou: $job contém warning ou overflow não reconhecido."
    exit 1
  fi
}

for engine in pdflatex lualatex; do
  job="postextuais-$engine"
  cleanup_job "$job"
  echo "Validando pós-textuais com $engine..."

  "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$modern" > /tmp/abntexto-ufc-v2-post.log 2>&1 || {
    cat /tmp/abntexto-ufc-v2-post.log
    exit 1
  }
  biber "$job" > /tmp/abntexto-ufc-v2-post-biber.log 2>&1 || {
    cat /tmp/abntexto-ufc-v2-post-biber.log
    exit 1
  }
  makeglossaries "$job" > /tmp/abntexto-ufc-v2-post-glossary.log 2>&1 || {
    cat /tmp/abntexto-ufc-v2-post-glossary.log
    exit 1
  }
  makeindex "$job" > /tmp/abntexto-ufc-v2-post-index.log 2>&1 || {
    cat /tmp/abntexto-ufc-v2-post-index.log
    exit 1
  }
  for pass in 1 2 3; do
    "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$modern" > /tmp/abntexto-ufc-v2-post.log 2>&1 || {
      cat /tmp/abntexto-ufc-v2-post.log
      exit 1
    }
  done
  check_log "$job"

  pdftotext -layout "$job.pdf" "/tmp/$job.txt"
  python3 - "$job" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

job = sys.argv[1]
raw = Path(f'/tmp/{job}.txt').read_text(encoding='utf-8')
raw = re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', raw)
text = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', raw)).strip()
fold = text.casefold()

markers = [
    'referências',
    'glossário',
    'apêndice a',
    'anexo a',
    'índice',
]
positions = []
for marker in markers:
    pos = fold.find(marker)
    if pos < 0:
        raise SystemExit(f'{job}: elemento pós-textual ausente: {marker}')
    positions.append(pos)
if positions != sorted(positions):
    raise SystemExit(f'{job}: ordem pós-textual incorreta: {list(zip(markers, positions))}')

for content in (
    'discretização de um domínio geométrico',
    'questionário produzido pelo autor',
    'documento institucional externo',
):
    if content.casefold() not in fold:
        raise SystemExit(f'{job}: conteúdo pós-textual ausente: {content}')

if 'capítulo' in fold or 'capitulo' in fold:
    raise SystemExit(f'{job}: estrutura baseada em capítulo reapareceu.')
PY

  for marker in 'Referências' 'Glossário' 'Questionário produzido pelo autor' 'Documento institucional externo' 'Remissivo'; do
    grep -Fqi "$marker" "$job.toc" || {
      echo "$job: item pós-textual ausente do Sumário: $marker"
      cat "$job.toc"
      exit 1
    }
  done

done

echo 'Gate V2 de pós-textuais concluído.'
