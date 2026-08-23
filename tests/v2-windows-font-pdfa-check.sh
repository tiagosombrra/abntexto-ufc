#!/bin/sh
set -eu

root="${1:-windows-font-pdfs}"

[ -d "$root" ] || {
  echo "Fontes Windows PDF/A: diretório ausente: $root"
  exit 1
}

for cmd in pdffonts pdftotext; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Fontes Windows PDF/A: comando ausente: $cmd"
    exit 2
  }
done

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
      echo "Fontes Windows PDF/A: $pdf não contém $pattern"
      pdffonts "$pdf"
      return 1
    }
  done
}

assert_no_text_fallback() {
  pdf=$1
  names=$(font_names "$pdf")

  if printf '%s\n' "$names" | grep -Eiq 'TeXGyreTermesX|TeXGyreTermes|TeXGyreHeros|NimbusSans'; then
    echo "Fontes Windows PDF/A: $pdf contém fallback textual inesperado."
    pdffonts "$pdf"
    return 1
  fi
}

assert_text_extraction() {
  pdf=$1
  txt="${TMPDIR:-/tmp}/$(basename "$pdf" .pdf)-text.txt"
  pdftotext "$pdf" "$txt"

  for marker in 'Texto normal para prova literal da classe.' 'ação' 'ciência' 'computação' 'orientação' 'avaliação' 'João' 'Ceará' 'São Luís'; do
    grep -Fq "$marker" "$txt" || {
      echo "Fontes Windows PDF/A: extração ausente/incorreta em $pdf: $marker"
      cat "$txt"
      return 1
    }
  done
}

for engine in pdflatex lualatex; do
  for family in times arial; do
    pdf="$root/ufctex-${family}-${engine}-strict-poc.pdf"
    [ -s "$pdf" ] || {
      echo "Fontes Windows PDF/A: arquivo ausente: $pdf"
      exit 1
    }

    echo "Fontes Windows PDF/A: certificando $family/$engine..."
    assert_names "$pdf" "$family"
    assert_no_text_fallback "$pdf"
    assert_text_extraction "$pdf"
    sh tests/v2-font-embedding-check.sh "$pdf"
    sh tests/v2-pdfa-check.sh "$pdf"
  done
done

echo 'Gate Windows: identidade literal, Unicode, embedding e PDF/A-2b concluídos.'
