#!/bin/sh
set -eu

pdf="${1:?uso: v2-font-embedding-check.sh arquivo.pdf}"

[ -s "$pdf" ] || {
  echo "Fontes V2: PDF não encontrado: $pdf"
  exit 1
}

command -v pdffonts >/dev/null 2>&1 || {
  echo 'Fontes V2: pdffonts não disponível.'
  exit 1
}

if ! pdffonts "$pdf" | tail -n +3 | awk '
  NF {
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
  END { exit bad }
'; then
  pdffonts "$pdf"
  echo "Fontes V2: há fonte não incorporada ou linha não reconhecida em $pdf."
  exit 1
fi

echo "Fontes V2 incorporadas: $pdf"
