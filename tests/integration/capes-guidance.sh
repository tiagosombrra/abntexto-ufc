#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
file="$ROOT/template/frontmatter/acknowledgments.tex"

for token in 'CAPES' 'Ordinance 206/2018' 'Código de Financiamento 001'; do
  grep -Fq "$token" "$file" || {
    echo "CAPES guidance: required marker missing: $token"
    exit 1
  }
done

echo 'Gate for CAPES guidance completed.'
