#!/bin/sh
set -eu

make compile

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Underfull \\hbox|Overfull \\vbox' documento.log | \
  grep -vF -e "Package babel Warning: Name 'brazil' is deprecated." \
            -e 'Class memoir Warning: \settocpreprocessor is marked deprecated and will be' || true)

if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Regressão 1.x falhou: revise os avisos acima.'
  exit 1
fi

if command -v pdffonts >/dev/null 2>&1; then
  if ! pdffonts documento.pdf | tail -n +3 | awk 'NF && $6 != "yes" {bad=1} END{exit bad}'; then
    echo 'Regressão 1.x falhou: há fonte não incorporada.'
    exit 1
  fi
fi

echo 'Gate de regressão da linha 1.x concluído.'
