#!/bin/sh
set -eu

fixture="tests/documents/minted-objects.tex"
tmp="abntexto-ufc-minted-check.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

if ! command -v latexminted >/dev/null 2>&1; then
  echo 'latexminted não disponível; rota minted não executada neste ambiente.'
  exit 0
fi

cleanup() {
  rm -f "$tmp" objetos-minted-*.aux objetos-minted-*.log objetos-minted-*.out objetos-minted-*.pdf objetos-minted-*.loc
}
trap cleanup EXIT INT TERM

expected_family() {
  engine=$1
  family=$2
  log=$3

  case "$family/$engine" in
    times/pdflatex)
      if grep -Fq 'Using literal Times New Roman with pdfLaTeX' "$log"; then
        echo 'TimesNewRoman'
      else
        echo 'TeXGyreTermesX'
      fi
      ;;
    arial/pdflatex)
      if grep -Fq 'Using literal Arial with pdfLaTeX' "$log"; then
        echo 'Arial'
      else
        echo 'TeXGyreHeros'
      fi
      ;;
    times/lualatex)
      if grep -Fq 'Using literal Times New Roman with LuaLaTeX' "$log"; then
        echo 'TimesNewRoman'
      else
        echo 'TeXGyreTermes'
      fi
      ;;
    arial/lualatex)
      if grep -Fq 'Using literal Arial with LuaLaTeX' "$log"; then
        echo 'Arial'
      else
        echo 'TeXGyreHeros'
      fi
      ;;
  esac
}

for engine in pdflatex lualatex; do
  for family in times arial; do
    sed "s/@UFC_FONT@/$family/g" "$fixture" > "$tmp"
    job="objetos-minted-$family-$engine"
    echo "Validating minted $family com $engine..."

    for pass in 1 2; do
      "$engine" -jobname="$job" -shell-escape $flags "$tmp" > /tmp/abntexto-ufc-minted.log 2>&1 || {
        cat /tmp/abntexto-ufc-minted.log
        exit 1
      }
    done

    overflow=$(grep -E 'Overfull \\hbox|Overfull \\vbox' "$job.log" || true)
    if [ -n "$overflow" ]; then
      printf '%s\n' "$overflow"
      echo "$job: fixture minted contains overflow."
      exit 1
    fi

    grep -Fq 'Arquivo Python com minted' "$job.loc" || {
      echo "$job: minted missing da list of code listings."
      exit 1
    }

    sh tests/integration/font-embedding.sh "$job.pdf"

    pages=$(pdfinfo "$job.pdf" | awk '/^Pages:/ {print $2}')
    [ "${pages:-0}" -ge 2 ] || {
      echo "$job: page isolada de code was not generated."
      exit 1
    }

    expected=$(expected_family "$engine" "$family" "$job.log")
    pdffonts -f "$pages" -l "$pages" "$job.pdf" | tail -n +3 | awk 'NF {print $1}' | grep -Fq "$expected" || {
      echo "$job: page isolada de minted não usa a família expected: $expected"
      pdffonts -f "$pages" -l "$pages" "$job.pdf"
      exit 1
    }
  done
done

echo 'Gate for minted completed.'
