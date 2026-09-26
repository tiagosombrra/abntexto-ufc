#!/bin/sh
set -eu

find_repo_root() {
  current=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
  while [ "$current" != "/" ]; do
    if [ -f "$current/abntexto-ufc.cls" ] && [ -f "$current/tests/path_resolver.py" ]; then
      printf '%s\n' "$current"
      return 0
    fi
    current=$(dirname "$current")
  done
  echo 'Repository root could not be located from integration script.' >&2
  return 1
}

ROOT=$(find_repo_root)
file="$ROOT/template/frontmatter/acknowledgments.tex"

for token in 'CAPES' 'Ordinance 206/2018' 'Código de Financiamento 001'; do
  grep -Fq "$token" "$file" || {
    echo "CAPES guidance: required marker missing: $token"
    exit 1
  }
done

echo 'Capes guidance gate completed.'
