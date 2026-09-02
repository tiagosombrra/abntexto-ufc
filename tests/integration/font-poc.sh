#!/bin/sh
set -u

root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
cd "$root" || exit 1

class_fixture="tests/documents/class-font-poc.tex"
class_tmp="abntexto-ufc-font-class-poc.tex"
compile_only=${UFC_FONT_POC_COMPILE_ONLY:-0}
trap 'rm -f "$class_tmp"' EXIT INT TERM

find_tex_bin() {
  if command -v kpsewhich >/dev/null 2>&1; then
    return 0
  fi

  found=''
  for candidate in /c/texlive/*/bin/windows; do
    [ -x "$candidate/kpsewhich.exe" ] && found="$candidate"
  done

  if [ -z "$found" ]; then
    for candidate in \
      '/c/Program Files/MiKTeX/miktex/bin/x64' \
      '/c/Program Files/MiKTeX/miktex/bin' \
      "/c/Users/${USERNAME:-}/AppData/Local/Programs/MiKTeX/miktex/bin/x64" \
      "/c/Users/${USERNAME:-}/AppData/Local/Programs/MiKTeX/miktex/bin"; do
      [ -x "$candidate/kpsewhich.exe" ] && found="$candidate" && break
    done
  fi

  if [ -n "$found" ]; then
    PATH="$found:$PATH"
    export PATH
    echo "POC fontes: toolchain TeX localizada em $found"
  fi
}

normalize_texmfhome() {
  case "$(uname -s 2>/dev/null || echo unknown)" in
    MINGW*|MSYS*|CYGWIN*)
      if [ -n "${TEXMFHOME:-}" ] && command -v cygpath >/dev/null 2>&1; then
        TEXMFHOME=$(cygpath -m "$TEXMFHOME")
        export TEXMFHOME
      fi
      ;;
  esac
}

find_poppler_bin() {
  if command -v pdffonts >/dev/null 2>&1; then
    return 0
  fi

  found=''
  if command -v where.exe >/dev/null 2>&1; then
    found_win=$(where.exe pdffonts.exe 2>/dev/null | tr -d '\r' | head -n 1 || true)
    if [ -n "$found_win" ] && command -v cygpath >/dev/null 2>&1; then
      found=$(cygpath -u "$found_win")
    fi
  fi

  if [ -z "$found" ] && command -v powershell.exe >/dev/null 2>&1; then
    found_win=$(powershell.exe -NoProfile -Command '$p = Get-ChildItem -Path "C:\ProgramData\chocolatey\lib\poppler\tools" -Filter pdffonts.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1; if ($p) { $p.FullName }' 2>/dev/null | tr -d '\r' | head -n 1 || true)
    if [ -n "$found_win" ] && command -v cygpath >/dev/null 2>&1; then
      found=$(cygpath -u "$found_win")
    fi
  fi

  if [ -z "$found" ]; then
    found=$(find /c/ProgramData/chocolatey/lib/poppler/tools -type f -iname pdffonts.exe -print -quit 2>/dev/null || true)
  fi

  if [ -n "$found" ]; then
    PATH="$(dirname "$found"):$PATH"
    export PATH
    echo "POC fontes: Poppler localizado em $(dirname "$found")"
  fi
}

find_tex_bin
normalize_texmfhome
if [ "$compile_only" != 1 ]; then
  find_poppler_bin
fi

missing=''
required='kpsewhich pdflatex lualatex'
if [ "$compile_only" != 1 ]; then
  required="$required pdffonts pdftotext"
fi
for cmd in $required; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    missing="$missing $cmd"
  fi
done

if [ -n "$missing" ]; then
  echo "POC fontes: comandos ausentes:$missing"
  echo 'POC fontes: verifique a instalação/PATH do TeX Live ou MiKTeX.'
  exit 2
fi

printf 'POC fontes: kpsewhich = %s\n' "$(command -v kpsewhich)"
printf 'POC fontes: pdflatex = %s\n' "$(command -v pdflatex)"
printf 'POC fontes: lualatex  = %s\n' "$(command -v lualatex)"
if [ -n "${TEXMFHOME:-}" ]; then
  printf 'POC fontes: TEXMFHOME  = %s\n' "$TEXMFHOME"
fi
if [ "$compile_only" != 1 ]; then
  printf 'POC fontes: pdffonts  = %s\n' "$(command -v pdffonts)"
  printf 'POC fontes: pdftotext = %s\n' "$(command -v pdftotext)"
else
  echo 'POC fontes: modo compile-only; certificação do PDF será executada no gate Linux.'
fi

font_dir=${UFC_WINDOWS_FONTS_DIR:-}
if [ -z "$font_dir" ]; then
  if [ -d /c/Windows/Fonts ]; then
    font_dir='C:/Windows/Fonts'
  elif [ -d /mnt/c/Windows/Fonts ]; then
    font_dir='/mnt/c/Windows/Fonts'
  fi
fi

if [ -n "$font_dir" ]; then
  echo "POC fontes: diretório Windows Fonts = $font_dir"
  case "$(uname -s 2>/dev/null || echo unknown)" in
    MINGW*|MSYS*|CYGWIN*) TTFONTS="${font_dir}//;${TTFONTS:-}" ;;
    *) TTFONTS="${font_dir}//:${TTFONTS:-}" ;;
  esac
  export TTFONTS
fi

cleanup() {
  job=$1
  rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
    "$job".out "$job".pdf "$job".run.xml
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

assert_no_text_fallback() {
  pdf=$1
  names=$(font_names "$pdf")

  if printf '%s\n' "$names" | grep -Eiq 'TeXGyreTermesX|TeXGyreTermes|TeXGyreHeros|NimbusSans'; then
    echo "POC fontes: $pdf contém família textual de fallback inesperada."
    pdffonts "$pdf"
    return 1
  fi
}

assert_text_extraction() {
  pdf=$1
  txt="${TMPDIR:-/tmp}/$(basename "$pdf" .pdf)-text.txt"
  pdftotext "$pdf" "$txt" || return 1

  for marker in 'Texto normal para prova literal da classe.' 'ação' 'ciência' 'computação' 'orientação' 'avaliação' 'João' 'Ceará' 'São Luís'; do
    grep -Fq "$marker" "$txt" || {
      echo "POC fontes: extração de texto ausente ou incorreta em $pdf: $marker"
      cat "$txt"
      return 1
    }
  done
}

compile_case() {
  engine=$1
  family=$2
  fixture="tests/documents/${family}-font-poc.tex"
  job="${family}-font-${engine}-poc"

  cleanup "$job"
  echo "POC fontes: infraestrutura $family com $engine"
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error \
    -jobname="$job" "$fixture" >"${TMPDIR:-/tmp}/$job.log" 2>&1 || {
      cat "${TMPDIR:-/tmp}/$job.log"
      return 1
    }

  if [ "$compile_only" != 1 ]; then
    assert_names "$job.pdf" "$family" || return 1
    echo "POC fontes: identidade de infraestrutura confirmada em $job.pdf"
  fi
}

compile_class_case() {
  engine=$1
  family=$2
  job="abntexto-ufc-${family}-${engine}-strict-poc"

  cleanup "$job"
  sed "s/@UFC_FONT@/$family/g" "$class_fixture" > "$class_tmp"
  echo "POC fontes: abntexto-ufc estrito $family com $engine"
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error \
    -jobname="$job" "$class_tmp" >"${TMPDIR:-/tmp}/$job.log" 2>&1 || {
      cat "${TMPDIR:-/tmp}/$job.log"
      return 1
    }

  if [ "$compile_only" != 1 ]; then
    assert_names "$job.pdf" "$family" || return 1
    assert_no_text_fallback "$job.pdf" || return 1
    assert_text_extraction "$job.pdf" || return 1
    sh tests/integration/font-embedding.sh "$job.pdf" || return 1
    echo "POC fontes: abntexto-ufc estrito confirmado em $job.pdf"
  else
    echo "POC fontes: artefato Windows gerado em $job.pdf"
  fi
}

fail_case() {
  code=$1
  label=$2
  echo "::error title=Windows literal font failure::$label"
  exit "$code"
}

blocked=0
failed=0

if ! kpsewhich t1times-ttf.fd >/dev/null 2>&1 || \
   ! kpsewhich t1arial.fd >/dev/null 2>&1 || \
   ! kpsewhich abntexto-ufc-windows.map >/dev/null 2>&1; then
  echo 'POC fontes: suporte abntexto-ufc Windows não localizado para pdfLaTeX.'
  blocked=1
else
  for ttf in times.ttf timesbd.ttf timesi.ttf timesbi.ttf arial.ttf arialbd.ttf ariali.ttf arialbi.ttf; do
    kpsewhich --format=truetype "$ttf" >/dev/null 2>&1 || {
      echo "POC fontes: TrueType não localizado pelo Kpathsea: $ttf"
      blocked=1
    }
  done

  if [ "$blocked" -eq 0 ]; then
    if [ "$compile_only" = 1 ]; then
      compile_case pdflatex times || fail_case 11 'pdfLaTeX / Times New Roman / infrastructure POC'
      compile_case pdflatex arial || fail_case 12 'pdfLaTeX / Arial / infrastructure POC'
      compile_class_case pdflatex times || fail_case 13 'pdfLaTeX / Times New Roman / abntexto-ufc strict POC'
      compile_class_case pdflatex arial || fail_case 14 'pdfLaTeX / Arial / abntexto-ufc strict POC'
    else
      compile_case pdflatex times || failed=1
      compile_case pdflatex arial || failed=1
      compile_class_case pdflatex times || failed=1
      compile_class_case pdflatex arial || failed=1
    fi
  fi
fi

if [ "$compile_only" = 1 ]; then
  compile_case lualatex times || fail_case 21 'LuaLaTeX / Times New Roman / infrastructure POC'
  compile_case lualatex arial || fail_case 22 'LuaLaTeX / Arial / infrastructure POC'
  compile_class_case lualatex times || fail_case 23 'LuaLaTeX / Times New Roman / abntexto-ufc strict POC'
  compile_class_case lualatex arial || fail_case 24 'LuaLaTeX / Arial / abntexto-ufc strict POC'
else
  compile_case lualatex times || failed=1
  compile_case lualatex arial || failed=1
  compile_class_case lualatex times || failed=1
  compile_class_case lualatex arial || failed=1
fi

if [ "$failed" -ne 0 ]; then
  echo 'POC fontes: houve falha na geração/certificação tipográfica.'
  exit 1
fi

if [ "$blocked" -ne 0 ]; then
  echo 'POC fontes: LuaLaTeX validado; pdfLaTeX bloqueado por infraestrutura local.'
  exit 2
fi

if [ "$compile_only" = 1 ]; then
  echo 'POC fontes: quatro PDFs estritos gerados no Windows; certificação delegada ao gate Linux.'
else
  echo 'POC fontes: Times New Roman e Arial literais validadas na infraestrutura e no abntexto-ufc estrito.'
fi
