#!/bin/sh
set -eu

fixtures="tests/normativa/pretextuais-trabalho.tex tests/normativa/pretextuais-projeto-anonimo.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

for engine in pdflatex lualatex; do
  for fixture in $fixtures; do
    echo "Validando $fixture com $engine..."
    for pass in 1 2; do
      "$engine" $flags "$fixture" > /tmp/ufctex-v2-pretextual.log 2>&1 || {
        cat /tmp/ufctex-v2-pretextual.log
        exit 1
      }
    done
  done
done

if grep -Eiq 'dedicat[oó]ria|agradecimentos|resumo|abstract|lista de' pretextuais-trabalho.toc; then
  echo 'Preflight V2 falhou: elemento pré-textual entrou no Sumário.'
  cat pretextuais-trabalho.toc
  exit 1
fi

grep -Eiq 'Introdu' pretextuais-trabalho.toc || {
  echo 'Preflight V2 falhou: seção textual ausente do Sumário.'
  exit 1
}

if command -v pdftotext >/dev/null 2>&1; then
  pdftotext pretextuais-trabalho.pdf /tmp/ufctex-v2-pretextual.txt
  for heading in 'AGRADECIMENTOS' 'RESUMO' 'ABSTRACT' 'LISTA DE FIGURAS' 'LISTA DE TABELAS' 'LISTA DE ABREVIATURAS E SIGLAS' 'LISTA DE SÍMBOLOS' 'SUMÁRIO'; do
    grep -Fq "$heading" /tmp/ufctex-v2-pretextual.txt || {
      echo "Preflight V2 falhou: título pré-textual ausente ou incorreto: $heading"
      exit 1
    }
  done

  if grep -Eiq '^Dedicat[oó]ria$' /tmp/ufctex-v2-pretextual.txt; then
    echo 'Preflight V2 falhou: dedicatória recebeu título.'
    exit 1
  fi

  pdftotext pretextuais-projeto-anonimo.pdf /tmp/ufctex-v2-anonimo.txt
  if grep -Fq 'AUTOR SIGILOSO TESTE' /tmp/ufctex-v2-anonimo.txt; then
    echo 'Preflight V2 falhou: autor vazou no projeto anonimizado.'
    exit 1
  fi
  if grep -Fq 'ORIENTADOR SIGILOSO TESTE' /tmp/ufctex-v2-anonimo.txt; then
    echo 'Preflight V2 falhou: orientador vazou no projeto anonimizado.'
    exit 1
  fi
  grep -Fq 'PROJETO-ANONIMO-001' /tmp/ufctex-v2-anonimo.txt || {
    echo 'Preflight V2 falhou: identificador anonimizado ausente.'
    exit 1
  }
fi

echo 'Gate V2 de pré-textuais concluído.'
