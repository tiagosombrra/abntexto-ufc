#!/bin/sh
set -eu

fixture="tests/normativa/fontes-config.tex"
tmp="ufctex-font-config.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f "$tmp" font-config-*.aux font-config-*.log font-config-*.out font-config-*.pdf
}
trap cleanup EXIT INT TERM

render_fixture() {
  family=$1
  strict=$2
  sed -e "s/@UFC_FONT@/$family/g" -e "s/@UFC_STRICT@/$strict/g" "$fixture" > "$tmp"
}

expected_family() {
  engine=$1
  family=$2
  log=$3

  case "$family/$engine" in
    times/pdflatex)
      if grep -Fq 'Using literal Times New Roman with pdfLaTeX' "$log"; then
        echo 'TimesNewRoman'
      else
        echo 'NewTX'
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

literal_available() {
  engine=$1
  family=$2
  log=$3
  case "$family/$engine" in
    times/pdflatex) grep -Fq 'Using literal Times New Roman with pdfLaTeX' "$log" ;;
    arial/pdflatex) grep -Fq 'Using literal Arial with pdfLaTeX' "$log" ;;
    times/lualatex) grep -Fq 'Using literal Times New Roman with LuaLaTeX' "$log" ;;
    arial/lualatex) grep -Fq 'Using literal Arial with LuaLaTeX' "$log" ;;
  esac
}

for engine in pdflatex lualatex; do
  for family in times arial; do
    render_fixture "$family" nao
    job="font-config-$family-$engine"
    echo "Validando fonte $family em modo compatível com $engine..."
    "$engine" -jobname="$job" $flags "$tmp" > "/tmp/$job.out" 2>&1 || {
      cat "/tmp/$job.out"
      exit 1
    }

    sh tests/v2-font-embedding-check.sh "$job.pdf"
    expected=$(expected_family "$engine" "$family" "$job.log")
    pdffonts "$job.pdf" | tail -n +3 | awk 'NF {print $1}' | grep -Fq "$expected" || {
      echo "$job: família esperada não encontrada: $expected"
      pdffonts "$job.pdf"
      exit 1
    }

    render_fixture "$family" sim
    strict_job="font-config-$family-$engine-strict"
    if literal_available "$engine" "$family" "$job.log"; then
      echo "Validando fonte literal $family em modo estrito com $engine..."
      "$engine" -jobname="$strict_job" $flags "$tmp" > "/tmp/$strict_job.out" 2>&1 || {
        cat "/tmp/$strict_job.out"
        exit 1
      }
      sh tests/v2-font-embedding-check.sh "$strict_job.pdf"
    else
      echo "Validando rejeição estrita de $family com $engine..."
      if "$engine" -jobname="$strict_job" $flags "$tmp" > "/tmp/$strict_job.out" 2>&1; then
        echo "$strict_job: modo estrito aceitou fonte literal ausente."
        exit 1
      fi
      case "$family" in
        times) grep -Fq 'Times New Roman' "/tmp/$strict_job.out" ;;
        arial) grep -Fq 'Arial' "/tmp/$strict_job.out" ;;
      esac || {
        cat "/tmp/$strict_job.out"
        echo "$strict_job: falhou sem diagnóstico da fonte solicitada."
        exit 1
      }
    fi
  done
done

echo 'Gate V2 de configuração tipográfica concluído.'
