#!/bin/sh
set -eu

pdf="${1:-documento.pdf}"
report="/tmp/ufctex-v2-verapdf.xml"

[ -f "$pdf" ] || {
  echo "PDF/A V2 falhou: arquivo não encontrado: $pdf"
  exit 1
}

status=0
if command -v verapdf >/dev/null 2>&1; then
  verapdf -f 2b "$pdf" > "$report" || status=$?
elif command -v docker >/dev/null 2>&1; then
  docker run --rm \
    -v "$PWD:/data:ro" \
    verapdf/cli:v1.30.2 \
    -f 2b "/data/$pdf" > "$report" || status=$?
else
  echo 'PDF/A V2 falhou: instale veraPDF ou Docker para a validação de release.'
  exit 1
fi

if [ -s "$report" ] && grep -Fq 'isCompliant="true"' "$report"; then
  echo 'Gate V2 PDF/A-2b concluído.'
  exit 0
fi

[ -s "$report" ] && cat "$report"
echo "PDF/A V2 falhou: veraPDF rejeitou o documento como PDF/A-2b (exit $status)."
exit 1
