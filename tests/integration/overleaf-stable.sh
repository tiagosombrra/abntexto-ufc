#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
project="${1:-.}"
project=$(CDPATH= cd -- "$project" && pwd)

[ -f "$project/abntexto.cls" ] || {
  echo 'Overleaf staging: local abntexto.cls is missing.'
  exit 1
}

runtime=$(TEXINPUTS="$project//:" kpsewhich abntexto.cls || true)
[ -n "$runtime" ] || {
  echo 'Overleaf staging: abntexto.cls was not found by Kpathsea.'
  exit 1
}

cmp -s "$runtime" "$project/abntexto.cls" || {
  echo "Overleaf staging: Kpathsea did not prioritize the pinned runtime: $runtime"
  exit 1
}

grep -Fq '[2026-05-08 1.1 Preparation of works in ABNT standards]' "$project/abntexto.cls" || {
  echo 'Overleaf staging: local runtime does not match the expected abntexto 1.1 pin.'
  exit 1
}

fixture="$repo_root/tests/fixtures/overleaf-latexmkrc"
[ -f "$fixture" ] || {
  echo 'Overleaf staging: latexmk fixture is missing.'
  exit 1
}
cp "$fixture" "$project/latexmkrc"

for cmd in latexmk pdffonts pdftotext pdfinfo biber makeglossaries makeindex; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Overleaf staging: required command is missing: $cmd"
    exit 1
  }
done

cleanup() {
  (cd "$project" && latexmk -C main.tex >/dev/null 2>&1) || true
  rm -f "$project/latexmkrc"
  rm -f "$project/main.acn" "$project/main.acr" "$project/main.alg" "$project/main.bbl" "$project/main.bcf" "$project/main.blg"
  rm -f "$project/main.glg" "$project/main.glo" "$project/main.gls" "$project/main.idx" "$project/main.ilg" "$project/main.ind"
  rm -f "$project/main.ist" "$project/main.nlo" "$project/main.nls" "$project/main.run.xml" "$project/main.xdy"
}
trap cleanup EXIT INT TERM

flags='LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Underfull \\hbox|Overfull \\vbox'

for engine in pdflatex lualatex; do
  echo "Overleaf staging: validating the flattened project with $engine..."
  (cd "$project" && latexmk -C main.tex >/dev/null 2>&1) || true

  case "$engine" in
    pdflatex) latexmk_mode='-pdf' ;;
    lualatex) latexmk_mode='-lualatex' ;;
  esac

  (cd "$project" && latexmk "$latexmk_mode" -interaction=nonstopmode -halt-on-error main.tex) \
    > "/tmp/abntexto-ufc-overleaf-$engine.out" 2>&1 || {
      cat "/tmp/abntexto-ufc-overleaf-$engine.out"
      exit 1
    }

  warnings=$(grep -E "$flags" "$project/main.log" || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Overleaf staging: $engine produced a warning or overflow."
    exit 1
  fi

  sh "$repo_root/tests/integration/font-embedding.sh" "$project/main.pdf"

  pdfinfo -meta "$project/main.pdf" > "/tmp/abntexto-ufc-overleaf-$engine-meta.xml"
  grep -Eq '<pdfaid:part>2</pdfaid:part>' "/tmp/abntexto-ufc-overleaf-$engine-meta.xml" || {
    echo "Overleaf staging: $engine PDF does not declare PDF/A part 2."
    exit 1
  }
  grep -Eq '<pdfaid:conformance>[Bb]</pdfaid:conformance>' "/tmp/abntexto-ufc-overleaf-$engine-meta.xml" || {
    echo "Overleaf staging: $engine PDF does not declare PDF/A-2b conformance."
    exit 1
  }

  pdftotext "$project/main.pdf" "/tmp/abntexto-ufc-overleaf-$engine.txt"
  for marker in 'RESUMO' 'ABSTRACT' 'LISTA DE ILUSTRAÇÕES' 'SUMÁRIO' 'INTRODUÇÃO' 'REFERÊNCIAS' 'GLOSSÁRIO' 'ÍNDICE'; do
    grep -Fq "$marker" "/tmp/abntexto-ufc-overleaf-$engine.txt" || {
      echo "Overleaf staging: $engine output is missing expected marker: $marker"
      exit 1
    }
  done
done

echo 'Overleaf flattened staging gate completed.'
