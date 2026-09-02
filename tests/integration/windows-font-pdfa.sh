#!/bin/sh
set -eu

root="${1:-windows-font-pdfs}"

[ -d "$root" ] || {
  echo "Windows font/PDF-A gate: directory not found: $root"
  exit 1
}

for cmd in pdffonts pdftotext; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Windows font/PDF-A gate: required command not found: $cmd"
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
      echo "Windows font/PDF-A gate: $pdf does not contain $pattern"
      pdffonts "$pdf"
      return 1
    }
  done
}

assert_no_text_fallback() {
  pdf=$1
  names=$(font_names "$pdf")

  if printf '%s\n' "$names" | grep -Eiq 'TeXGyreTermesX|TeXGyreTermes|TeXGyreHeros|NimbusSans'; then
    echo "Windows font/PDF-A gate: $pdf contains an unexpected text-font fallback."
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
      echo "Windows font/PDF-A gate: text extraction missing/incorrect in $pdf: $marker"
      cat "$txt"
      return 1
    }
  done
}

for engine in pdflatex lualatex; do
  for family in times arial; do
    pdf="$root/abntexto-ufc-${family}-${engine}-strict-poc.pdf"
    [ -s "$pdf" ] || {
      echo "Windows font/PDF-A gate: file not found: $pdf"
      exit 1
    }

    echo "Windows font/PDF-A gate: certifying $family/$engine..."
    assert_names "$pdf" "$family"
    assert_no_text_fallback "$pdf"
    assert_text_extraction "$pdf"
    sh tests/integration/font-embedding.sh "$pdf"
    sh tests/integration/pdfa.sh "$pdf"
  done
done

echo 'Windows gate: literal font identity, Unicode extraction, embedding, and PDF/A-2b completed.'
