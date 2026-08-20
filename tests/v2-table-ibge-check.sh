#!/bin/sh
set -eu

fixture="tests/normativa/tabela-ibge.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f tabela-ibge-*.aux tabela-ibge-*.log tabela-ibge-*.out tabela-ibge-*.pdf tabela-ibge-*.lot
}
trap cleanup EXIT INT TERM

for token in '\\toprule' '\\midrule' '\\bottomrule' 'row{even}' 'remark{Fonte}' 'tabelas = tabularray'; do
  grep -Fq "$token" "$fixture" || {
    echo "Tabela IBGE: estrutura obrigatória ausente no fixture: $token"
    exit 1
  }
done

if grep -Eq '(^|[^[:alpha:]])(vlines|hlines)([^[:alpha:]]|$)' "$fixture"; then
  echo 'Tabela IBGE: tabela numérica não pode usar fechamento lateral ou grade no corpo.'
  exit 1
fi

for engine in pdflatex lualatex; do
  job="tabela-ibge-$engine"
  echo "Validando tabela IBGE com $engine..."

  for pass in 1 2; do
    "$engine" -jobname="$job" $flags "$fixture" > "/tmp/$job.out" 2>&1 || {
      cat "/tmp/$job.out"
      exit 1
    }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "$job: warning ou overflow não reconhecido."
    exit 1
  fi

  grep -Eq 'UFC-IBGE-FONTSIZE=12([.]0+)?$' "$job.log" || {
    grep 'UFC-IBGE-FONTSIZE' "$job.log" || true
    echo "$job: corpo da tabela não está em tamanho 12."
    exit 1
  }

  grep -Fq 'Indicadores numéricos de teste' "$job.lot" || {
    echo "$job: tabela ausente da lista de tabelas."
    exit 1
  }

  sh tests/v2-font-embedding-check.sh "$job.pdf"

  pdftotext -layout "$job.pdf" "/tmp/$job.txt"
  for marker in 'Indicadores numéricos de teste' 'Ano' '2024' '2025' '2026' 'Fonte:' 'Elaboração própria'; do
    grep -Fq "$marker" "/tmp/$job.txt" || {
      echo "$job: conteúdo tabular ausente: $marker"
      exit 1
    }
  done

done

echo 'Gate V2 do subconjunto tabular IBGE concluído.'
