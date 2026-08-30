#!/bin/sh
set -eu

file="frontmatter/agradecimentos.tex"

for token in 'CAPES' 'Ordinance 206/2018' 'Código de Financiamento 001'; do
  grep -Fq "$token" "$file" || {
    echo "CAPES guidance: required marker missing: $token"
    exit 1
  }
done

echo 'Gate de orientação CAPES concluído.'
