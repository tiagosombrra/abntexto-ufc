#!/bin/sh
set -u

root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
cd "$root" || exit 1

for cmd in kpsewhich pdffonts pdflatex lualatex; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "POC fontes: comando ausente: $cmd"
    exit 2
  }
done

font_dir=${UFC_WINDOWS_FONTS_DIR:-}
if [ -z "$font_dir" ]; then
  if [ -d /c/Windows/Fonts ]; then
    font_dir='C:/Windows/Fonts'
  elif [ -d /mnt/c/Windows/Fonts ]; then
    font_dir='/mnt/c/Windows/Fonts'
  fi
fi

if [ -n "$font_dir" ]; then
  case "$(uname -s 2>/dev/null || echo unknown)" in
    MINGW*|MSYS*|CYGWIN*) TTFONTS="${font_dir}//;${TTFONTS:-}" ;;
    *) TTFONTS="${font_dir}//:${TTFONTS:-}" ;;
  esac
  export TTFONTS
fi

cleanup() {
  job=$1
  rm -f "$job".aux "$job".log "$job".out "$job".pdf
}

font_names() {
  pdffonts "$1" | tail -n +3 | awk 'NF {print $1}'
}

assert_names() {
  pdf=$1
  family=$2
  names=$(font_names "$pdf")

  case "$family" in
    times)
      patterns='TimesNewRomanPSMT TimesNewRomanPS-BoldMT TimesNewRomanPS-ItalicMT TimesNewRomanPS-BoldItalicMT'
      ;;
    arial)
      patterns='ArialMT Arial-BoldMT Arial-ItalicMT Arial-BoldItalicMT'
      ;;
    *) return 1 ;;
  esac

  for pattern in $patterns; do
    printf '%s\n' "$names" | grep -Fq "$pattern" || {
      echo "POC fontes: $pdf não contém $pattern"
      pdffonts "$pdf"
      return 1
    }
  done
}

compile_case() {
  engine=$1
  family=$2
  fixture="tests/normativa/fontes-${family}-poc.tex"
  job="fontes-${family}-${engine}-poc"

  cleanup "$job"
  echo "POC fontes: $family com $engine"
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error \
    -jobname="$job" "$fixture" >"/tmp/$job.log" 2>&1 || {
      cat "/tmp/$job.log"
      return 1
    }

  assert_names "$job.pdf" "$family" || return 1
  echo "POC fontes: identidade confirmada em $job.pdf"
}

blocked=0
failed=0

if ! kpsewhich t1times-ttf.fd >/dev/null 2>&1 || \
   ! kpsewhich t1arial.fd >/dev/null 2>&1 || \
   ! kpsewhich winfonts.map >/dev/null 2>&1; then
  echo 'POC fontes: suporte winfonts não localizado para pdfLaTeX.'
  blocked=1
else
  for ttf in times.ttf timesbd.ttf timesi.ttf timesbi.ttf arial.ttf arialbd.ttf ariali.ttf arialbi.ttf; do
    kpsewhich --format=truetype "$ttf" >/dev/null 2>&1 || {
      echo "POC fontes: TrueType não localizado pelo Kpathsea: $ttf"
      blocked=1
    }
  done

  if [ "$blocked" -eq 0 ]; then
    compile_case pdflatex times || failed=1
    compile_case pdflatex arial || failed=1
  fi
fi

compile_case lualatex times || failed=1
compile_case lualatex arial || failed=1

if [ "$failed" -ne 0 ]; then
  echo 'POC fontes: houve falha de identidade tipográfica.'
  exit 1
fi

if [ "$blocked" -ne 0 ]; then
  echo 'POC fontes: LuaLaTeX validado; pdfLaTeX bloqueado por infraestrutura local.'
  exit 2
fi

echo 'POC fontes: Times New Roman e Arial literais validadas nos dois motores.'
