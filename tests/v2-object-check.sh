#!/bin/sh
set -eu

fixture="tests/normativa/objetos-avancados.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

for engine in pdflatex lualatex; do
  echo "Validando $fixture com $engine..."
  for pass in 1 2; do
    "$engine" $flags "$fixture" > /tmp/ufctex-v2-objects.log 2>&1 || {
      cat /tmp/ufctex-v2-objects.log
      exit 1
    }
  done
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' objetos-avancados.log | \
  grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Contexto das caixas excedentes:'
  grep -n -A4 -B1 -E 'Overfull \\hbox|Overfull \\vbox' objetos-avancados.log || true
  echo 'Preflight V2 falhou: fixture de objetos contém warnings ou overflow não reconhecidos.'
  exit 1
fi

grep -Fq 'Figura normativa de teste' objetos-avancados.lof || { echo 'Figura ausente da lista de figuras.'; exit 1; }
grep -Fq 'Tabela acadêmica de teste' objetos-avancados.lot || { echo 'Tabela ausente da lista de tabelas.'; exit 1; }
grep -Fq 'Quadro multipágina de teste' objetos-avancados.loq || { echo 'Quadro ausente da lista de quadros.'; exit 1; }
grep -Fq 'Gráfico normativo de teste' objetos-avancados.logr || { echo 'Gráfico ausente da lista de gráficos.'; exit 1; }
grep -Fq 'Trecho C++ embutido' objetos-avancados.loc || { echo 'Código embutido ausente da lista de códigos.'; exit 1; }
grep -Fq 'Arquivo C++ externo' objetos-avancados.loc || { echo 'Código externo ausente da lista de códigos.'; exit 1; }
grep -Fq 'Busca linear' objetos-avancados.loa || { echo 'Algoritmo ausente da lista de algoritmos.'; exit 1; }
grep -Fq 'Figura normativa de teste' objetos-avancados.loi || { echo 'Figura ausente da lista unificada.'; exit 1; }
grep -Fq 'Gráfico normativo de teste' objetos-avancados.loi || { echo 'Gráfico ausente da lista unificada.'; exit 1; }
grep -Fq 'Quadro multipágina de teste' objetos-avancados.loi || { echo 'Quadro ausente da lista unificada.'; exit 1; }
if grep -Fq 'Tabela acadêmica de teste' objetos-avancados.loi; then
  echo 'Preflight V2 falhou: tabela entrou indevidamente na lista de ilustrações.'
  exit 1
fi

if command -v pdftotext >/dev/null 2>&1; then
  pdftotext objetos-avancados.pdf /tmp/ufctex-v2-objects.txt
  for heading in 'LISTA DE ILUSTRAÇÕES' 'LISTA DE FIGURAS' 'LISTA DE TABELAS' 'LISTA DE QUADROS' 'LISTA DE GRÁFICOS' 'LISTA DE CÓDIGOS' 'LISTA DE ALGORITMOS'; do
    grep -Fq "$heading" /tmp/ufctex-v2-objects.txt || {
      echo "Preflight V2 falhou: lista de objeto ausente: $heading"
      exit 1
    }
  done
  grep -Fq 'Fonte:' /tmp/ufctex-v2-objects.txt || { echo 'Fonte de objeto ausente.'; exit 1; }
  grep -Fq 'Nota:' /tmp/ufctex-v2-objects.txt || { echo 'Nota de objeto ausente.'; exit 1; }
fi

echo 'Gate V2 de objetos concluído.'
