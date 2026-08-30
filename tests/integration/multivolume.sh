#!/bin/sh
set -eu

fixture="tests/documents/multivolume.tex"
invalid_fixture=".abntexto-ufc-v2-invalid-page.tex"

cleanup_invalid() {
  rm -f "$invalid_fixture" invalid-page.aux invalid-page.log invalid-page.out invalid-page.pdf invalid-page.toc
}
trap cleanup_invalid EXIT INT TERM

for engine in pdflatex lualatex; do
  job="multivolume-$engine"
  rm -f "$job".aux "$job".log "$job".out "$job".pdf "$job".toc

  echo "Validando trabalho multivolume com $engine..."
  for pass in 1 2 3; do
    "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-v2-multivolume.log 2>&1 || {
      cat /tmp/abntexto-ufc-v2-multivolume.log
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Multivolume V2 falhou: $job contém warning ou overflow não reconhecido."
    exit 1
  fi

  grep -Fq 'UFC-PAGE-AFTER-COVER=101' "$job.log" || {
    echo "$job: pagina-inicial não foi preservada após a capa."
    exit 1
  }
  grep -Fq 'UFC-PAGE-AFTER-TITLE=102' "$job.log" || {
    echo "$job: folha de rosto não avançou a sequência 101 → 102."
    exit 1
  }
  grep -Fq 'UFC-TEXT-PAGE=102' "$job.log" || {
    echo "$job: conteúdo textual não continuou na página lógica 102."
    exit 1
  }

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

norm = [
    re.sub(r'\s+', ' ', unicodedata.normalize('NFC', page)).strip().casefold()
    for page in pages
]
text = ' '.join(norm)

if len(norm) < 3:
    raise SystemExit(f'{job}: esperado capa, folha de rosto e conteúdo textual.')
if 'curso de graduação em ciência da computação' not in norm[0]:
    raise SystemExit(f'{job}: identificação completa do curso ausente da capa.')
if text.count('volume 2') < 2:
    raise SystemExit(f'{job}: volume não aparece na capa e na folha de rosto.')
for marker in ('autor multivolume teste', 'trabalho multivolume de teste', 'marcador textual do volume dois'):
    if marker not in text:
        raise SystemExit(f'{job}: conteúdo esperado ausente: {marker}')
PY
done

cleanup_invalid
sed 's/pagina-inicial = 101/pagina-inicial = 0/' "$fixture" > "$invalid_fixture"
if pdflatex -jobname=invalid-page -interaction=nonstopmode -halt-on-error -file-line-error "$invalid_fixture" > /tmp/abntexto-ufc-v2-invalid-page.log 2>&1; then
  echo 'Multivolume V2 falhou: pagina-inicial=0 foi aceita.'
  exit 1
fi
if ! python3 - /tmp/abntexto-ufc-v2-invalid-page.log <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace')
compact = re.sub(r'\s+', '', text)
expected = "Classabntexto-ufcError:Invalidpagina-inicial'0'."
raise SystemExit(0 if expected in compact else 1)
PY
then
  cat /tmp/abntexto-ufc-v2-invalid-page.log
  echo 'Multivolume V2 falhou: pagina-inicial inválida não produziu o erro esperado.'
  exit 1
fi

echo 'Gate V2 de trabalhos multivolume concluído.'
