#!/bin/sh
set -eu

fixture="tests/normativa/objetos-minted.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

if ! command -v latexminted >/dev/null 2>&1; then
  echo 'latexminted não disponível; rota minted não executada neste ambiente.'
  exit 0
fi

for engine in pdflatex lualatex; do
  echo "Validando $fixture com $engine..."
  for pass in 1 2; do
    "$engine" -shell-escape $flags "$fixture" > /tmp/ufctex-v2-minted.log 2>&1 || {
      cat /tmp/ufctex-v2-minted.log
      exit 1
    }
  done
done

overflow=$(grep -E 'Overfull \\hbox|Overfull \\vbox' objetos-minted.log || true)
if [ -n "$overflow" ]; then
  printf '%s\n' "$overflow"
  echo 'Preflight V2 falhou: fixture minted contém overflow.'
  exit 1
fi

grep -Fq 'Arquivo Python com minted' objetos-minted.loc || {
  echo 'Preflight V2 falhou: minted ausente da lista de códigos.'
  exit 1
}

echo 'Gate V2 de minted concluído.'
