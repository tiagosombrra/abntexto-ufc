#!/bin/sh
set -eu

file="1-pre-textuais/agradecimentos.tex"

for token in 'CAPES' 'Ordinance 206/2018' 'Código de Financiamento 001'; do
  grep -Fq "$token" "$file" || {
    echo "CAPES guidance: required marker missing: $token"
    exit 1
  }
done

echo 'Gate V2 de orientação CAPES concluído.'
