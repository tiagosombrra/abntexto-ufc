#!/bin/sh
set -eu

source_fixture="tests/normativa/ficha-catalografica.tex"
tmp_fixture="ufctex-v2-catalog-main.tex"
card_source="ufctex-v2-catalog-card.tex"
card_base="ufctex-v2-catalog-card"

cleanup() {
  rm -f "$tmp_fixture" "$card_source" "$card_base".aux "$card_base".log "$card_base".pdf \
        ficha-catalografica-*.aux ficha-catalografica-*.log \
        ficha-catalografica-*.out ficha-catalografica-*.pdf ficha-catalografica-*.toc
}
trap cleanup EXIT INT TERM

cat > "$card_source" <<'TEX'
\documentclass{article}
\usepackage[paperwidth=210mm,paperheight=297mm,margin=2cm]{geometry}
\pagestyle{empty}
\begin{document}
\vfill
\begin{center}
FICHA-CATALOGRAFICA-TESTE
\end{center}
\vfill
\end{document}
TEX

pdflatex -interaction=nonstopmode -halt-on-error -file-line-error "$card_source" > /tmp/ufctex-v2-card-source.log 2>&1 || {
  cat /tmp/ufctex-v2-card-source.log
  exit 1
}

for engine in pdflatex lualatex; do
  for mode in anverso frente-verso; do
    job="ficha-catalografica-$mode-$engine"
    sed -e "s/@UFC_PRINT@/$mode/g" \
        -e "s/\.ufctex-catalog-card/$card_base/g" \
        "$source_fixture" > "$tmp_fixture"

    echo "Validando ficha catalográfica: $mode/$engine..."
    for pass in 1 2 3; do
      "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$tmp_fixture" > /tmp/ufctex-v2-card.log 2>&1 || {
        cat /tmp/ufctex-v2-card.log
        exit 1
      }
    done

    warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
      grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
    if [ -n "$warnings" ]; then
      printf '%s\n' "$warnings"
      echo "$job: warning ou overflow não reconhecido."
      exit 1
    fi

    grep -Fq 'UFC-BEFORE-CARD=2' "$job.log" || {
      echo "$job: contador inesperado antes da ficha."
      exit 1
    }
    grep -Fq 'UFC-AFTER-CARD=2' "$job.log" || {
      echo "$job: ficha catalográfica foi contada indevidamente."
      exit 1
    }
    grep -Fq 'UFC-TEXT-PAGE=2' "$job.log" || {
      echo "$job: texto não preservou a contagem lógica após a ficha."
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
norm = [re.sub(r'\s+', ' ', unicodedata.normalize('NFC', p)).strip().casefold() for p in pages]

if len(norm) != 3:
    raise SystemExit(f'{job}: esperado folha de rosto, ficha e texto em 3 páginas físicas; obtido {len(norm)}.')
if 'ficha-catalografica-teste' not in norm[1]:
    raise SystemExit(f'{job}: ficha não ocupa o verso físico da folha de rosto.')
if 'marcador textual após a ficha catalográfica' not in norm[2]:
    raise SystemExit(f'{job}: texto posterior à ficha não iniciou no anverso físico seguinte.')
PY
  done
done

echo 'Gate V2 da ficha catalográfica concluído.'
