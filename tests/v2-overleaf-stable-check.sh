#!/bin/sh
set -eu

runtime=$(kpsewhich abntexto.cls || true)
[ -n "$runtime" ] || {
  echo 'Overleaf proxy: abntexto.cls não localizado.'
  exit 1
}

grep -Fq '[2026-05-08 1.1 Preparation of works in ABNT standards]' "$runtime" || {
  echo "Overleaf proxy: versão incorreta de abntexto em $runtime"
  exit 1
}

for cmd in pdffonts pdftotext pdfinfo biber makeglossaries makeindex; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Overleaf proxy: comando ausente: $cmd"
    exit 1
  }
done

cleanup() {
  make clean >/dev/null 2>&1 || true
  rm -f overleaf-stable-pdflatex.pdf overleaf-stable-lualatex.pdf
}
trap cleanup EXIT INT TERM

flags='LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Underfull \\hbox|Overfull \\vbox'

for engine in pdflatex lualatex; do
  echo "Overleaf proxy: validando documento completo com $engine / TeX Live 2025..."
  make clean >/dev/null
  make ENGINE="$engine" compile > "/tmp/ufctex-overleaf-$engine.out" 2>&1 || {
    cat "/tmp/ufctex-overleaf-$engine.out"
    exit 1
  }

  warnings=$(grep -E "$flags" documento.log || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Overleaf proxy: $engine produziu warning ou overflow."
    exit 1
  fi

  sh tests/v2-font-embedding-check.sh documento.pdf

  pdfinfo -meta documento.pdf > "/tmp/ufctex-overleaf-$engine-meta.xml"
  grep -Eq '<pdfaid:part>2</pdfaid:part>' "/tmp/ufctex-overleaf-$engine-meta.xml" || {
    echo "Overleaf proxy: $engine sem declaração PDF/A parte 2."
    exit 1
  }
  grep -Eq '<pdfaid:conformance>[Bb]</pdfaid:conformance>' "/tmp/ufctex-overleaf-$engine-meta.xml" || {
    echo "Overleaf proxy: $engine sem declaração PDF/A-2b."
    exit 1
  }

  pdftotext documento.pdf "/tmp/ufctex-overleaf-$engine.txt"
  for marker in 'RESUMO' 'ABSTRACT' 'LISTA DE ILUSTRAÇÕES' 'SUMÁRIO' 'INTRODUÇÃO' 'REFERÊNCIAS' 'GLOSSÁRIO' 'ÍNDICE'; do
    grep -Fq "$marker" "/tmp/ufctex-overleaf-$engine.txt" || {
      echo "Overleaf proxy: $engine sem marcador esperado: $marker"
      exit 1
    }
  done

  cp documento.pdf "overleaf-stable-$engine.pdf"
done

echo 'Gate proxy V2 para Overleaf estável concluído.'
