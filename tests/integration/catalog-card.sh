#!/bin/sh
set -eu

source_fixture="tests/documents/catalog-card.tex"
tmp_fixture="abntexto-ufc-catalog-main.tex"
card_source="abntexto-ufc-catalog-card.tex"
card_base="abntexto-ufc-catalog-card"

cleanup() {
  rm -f "$tmp_fixture" "$card_source" "$card_base".aux "$card_base".log "$card_base".pdf \
        ficha-catalografica-*.aux ficha-catalografica-*.log \
        ficha-catalografica-*.out ficha-catalografica-*.pdf ficha-catalografica-*.toc \
        ficha-catalografica-*.txt
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

pdflatex -interaction=nonstopmode -halt-on-error -file-line-error "$card_source" > /tmp/abntexto-ufc-card-source.log 2>&1 || {
  cat /tmp/abntexto-ufc-card-source.log
  exit 1
}

for engine in pdflatex lualatex; do
  for mode in single-sided double-sided; do
    for card_mode in true false; do
      job="ficha-catalografica-$mode-$card_mode-$engine"
      sed -e "s/@UFC_PRINT@/$mode/g" \
          -e "s/@UFC_CARD@/$card_mode/g" \
          -e "s/\.abntexto-ufc-catalog-card/$card_base/g" \
          "$source_fixture" > "$tmp_fixture"

      echo "Validando ficha catalográfica: $mode/$card_mode/$engine..."
      for pass in 1 2 3; do
        "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$tmp_fixture" > /tmp/abntexto-ufc-card.log 2>&1 || {
          cat /tmp/abntexto-ufc-card.log
          exit 1
        }
      done

      warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
        grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
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
        echo "$job: rota da ficha alterou indevidamente a contagem lógica."
        exit 1
      }

      expected_text_page=2
      if [ "$mode" = "double-sided" ] && [ "$card_mode" = "false" ]; then
        expected_text_page=3
      fi
      grep -Fq "UFC-TEXT-PAGE=$expected_text_page" "$job.log" || {
        echo "$job: página lógica textual inesperada; esperado $expected_text_page."
        exit 1
      }

      pdftotext -layout "$job.pdf" "$job.txt"
      python3 - "$job" "$mode" "$card_mode" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

job, mode, card_mode = sys.argv[1:]
raw = Path(f'{job}.txt').read_text(encoding='utf-8')
pages = raw.split('\f')
if pages and not pages[-1].strip():
    pages.pop()
norm = [re.sub(r'\s+', ' ', unicodedata.normalize('NFC', p)).strip().casefold() for p in pages]
card_marker = 'ficha-catalografica-teste'
text_marker = 'marcador textual após a ficha catalográfica'

if card_mode == 'true':
    if len(norm) != 3:
        raise SystemExit(f'{job}: esperado folha de rosto, ficha e texto em 3 páginas físicas; obtido {len(norm)}.')
    if card_marker not in norm[1]:
        raise SystemExit(f'{job}: ficha habilitada não ocupa o verso físico da folha de rosto.')
    if text_marker not in norm[2]:
        raise SystemExit(f'{job}: texto posterior à ficha não iniciou no anverso físico seguinte.')
else:
    if any(card_marker in page for page in norm):
        raise SystemExit(f'{job}: ficha externa foi incluída although catalog-card=false.')
    text_pages = [index for index, page in enumerate(norm) if text_marker in page]
    if len(text_pages) != 1:
        raise SystemExit(f'{job}: marcador textual ausente ou duplicado com ficha desabilitada.')
    expected_physical_index = 1 if mode == 'single-sided' else 2
    if text_pages[0] != expected_physical_index:
        raise SystemExit(
            f'{job}: texto em página física inesperada com ficha desabilitada; '
            f'esperado índice {expected_physical_index}, obtido {text_pages[0]}.'
        )
    if mode == 'double-sided' and (len(norm) != 3 or norm[1]):
        raise SystemExit(f'{job}: double-sided mode without a catalog card deve preservar verso físico em branco antes do texto.')
PY
    done
  done
done

echo 'VALIDATION-EVIDENCE rule=deposit.catalog-card status=PASS measured=enabled-and-disabled-routes'
echo 'VALIDATION-BOUNDARY rule=font.size.reduced.catalog-card status=MANUAL scope=external-pdf'
echo 'Gate da ficha catalográfica concluído.'
