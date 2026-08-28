#!/bin/sh
set -eu

[ -f abntexto.cls ] || {
  echo 'Overleaf proxy: runtime local abntexto.cls ausente.'
  exit 1
}

runtime=$(kpsewhich abntexto.cls || true)
[ -n "$runtime" ] || {
  echo 'Overleaf proxy: abntexto.cls não localizado pelo Kpathsea.'
  exit 1
}

cmp -s "$runtime" abntexto.cls || {
  echo "Overleaf proxy: Kpathsea não priorizou o runtime pinado: $runtime"
  exit 1
}

grep -Fq '[2026-05-08 1.1 Preparation of works in ABNT standards]' abntexto.cls || {
  echo 'Overleaf proxy: runtime local não corresponde ao abntexto 1.1 esperado.'
  exit 1
}

[ -f tests/fixtures/overleaf-latexmkrc ] || {
  echo 'Overleaf proxy: regras latexmk do proxy ausentes.'
  exit 1
}
cp tests/fixtures/overleaf-latexmkrc latexmkrc

for cmd in latexmk pdffonts pdftotext pdfinfo biber makeglossaries makeindex; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Overleaf proxy: comando ausente: $cmd"
    exit 1
  }
done

cleanup() {
  latexmk -C main.tex >/dev/null 2>&1 || true
  rm -f latexmkrc
  rm -f main.acn main.acr main.alg main.bbl main.bcf main.blg
  rm -f main.glg main.glo main.gls main.idx main.ilg main.ind
  rm -f main.ist main.nlo main.nls main.run.xml main.xdy
}
trap cleanup EXIT INT TERM

flags='LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Underfull \\hbox|Overfull \\vbox'

for engine in pdflatex lualatex; do
  echo "Overleaf proxy: validando documento completo com $engine / TeX Live 2025 público..."
  latexmk -C main.tex >/dev/null 2>&1 || true

  case "$engine" in
    pdflatex) latexmk_mode='-pdf' ;;
    lualatex) latexmk_mode='-lualatex' ;;
  esac

  latexmk "$latexmk_mode" -interaction=nonstopmode -halt-on-error main.tex \
    > "/tmp/abntexto-ufc-overleaf-$engine.out" 2>&1 || {
      cat "/tmp/abntexto-ufc-overleaf-$engine.out"
      exit 1
    }

  warnings=$(grep -E "$flags" main.log || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Overleaf proxy: $engine produziu warning ou overflow."
    exit 1
  fi

  sh tests/v2-font-embedding-check.sh main.pdf

  pdfinfo -meta main.pdf > "/tmp/abntexto-ufc-overleaf-$engine-meta.xml"
  grep -Eq '<pdfaid:part>2</pdfaid:part>' "/tmp/abntexto-ufc-overleaf-$engine-meta.xml" || {
    echo "Overleaf proxy: $engine sem declaração PDF/A parte 2."
    exit 1
  }
  grep -Eq '<pdfaid:conformance>[Bb]</pdfaid:conformance>' "/tmp/abntexto-ufc-overleaf-$engine-meta.xml" || {
    echo "Overleaf proxy: $engine sem declaração PDF/A-2b."
    exit 1
  }

  pdftotext main.pdf "/tmp/abntexto-ufc-overleaf-$engine.txt"
  for marker in 'RESUMO' 'ABSTRACT' 'LISTA DE ILUSTRAÇÕES' 'SUMÁRIO' 'INTRODUÇÃO' 'REFERÊNCIAS' 'GLOSSÁRIO' 'ÍNDICE'; do
    grep -Fq "$marker" "/tmp/abntexto-ufc-overleaf-$engine.txt" || {
      echo "Overleaf proxy: $engine sem marcador esperado: $marker"
      exit 1
    }
  done
done

echo 'Gate proxy V2 para Overleaf estável concluído.'
