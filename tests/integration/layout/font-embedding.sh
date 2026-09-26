#!/bin/sh
set -eu

pdf="${1:?usage: font-embedding.sh file.pdf}"

[ -s "$pdf" ] || {
  echo "Font embedding: PDF not found: $pdf"
  exit 1
}

command -v pdffonts >/dev/null 2>&1 || {
  echo 'Font embedding: pdffonts is not available.'
  exit 1
}

if ! pdffonts "$pdf" | tail -n +3 | awk '
  NF {
    count++
    found = 0
    for (i = 1; i <= NF; i++) {
      if ($i == "yes" || $i == "no") {
        found = 1
        if ($i != "yes") bad = 1
        break
      }
    }
    if (!found) bad = 1
  }
  END {
    if (count == 0) bad = 1
    exit bad
  }
'; then
  pdffonts "$pdf"
  echo "Font embedding: an unembedded font, no detected fonts, or an unrecognized pdffonts row was found in $pdf."
  exit 1
fi

echo "Font embedding complete (emb=yes): $pdf"
