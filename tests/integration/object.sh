#!/bin/sh
set -eu

fixture="tests/documents/advanced-objects.tex"
job="objetos-avancados"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

for engine in pdflatex lualatex; do
  echo "Validando $fixture com $engine..."
  for pass in 1 2; do
    "$engine" -jobname="$job" $flags "$fixture" > /tmp/abntexto-ufc-objects.log 2>&1 || {
      cat /tmp/abntexto-ufc-objects.log
      exit 1
    }
  done
done

warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
  grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
if [ -n "$warnings" ]; then
  printf '%s\n' "$warnings"
  echo 'Contexto das caixas excedentes:'
  grep -n -A4 -B1 -E 'Overfull \\hbox|Overfull \\vbox' "$job.log" || true
  echo 'Preflight falhou: fixture de objetos contém warnings ou overflow não reconhecidos.'
  exit 1
fi

grep -Fq 'Figura normativa de teste' "$job.lof" || { echo 'Figura ausente da lista de figuras.'; exit 1; }
grep -Fq 'Tabela acadêmica de teste' "$job.lot" || { echo 'Tabela ausente da lista de tabelas.'; exit 1; }
grep -Fq 'Quadro multipágina de teste' "$job.loq" || { echo 'Quadro ausente da lista de quadros.'; exit 1; }
grep -Fq 'Gráfico normativo de teste' "$job.logr" || { echo 'Gráfico ausente da lista de gráficos.'; exit 1; }
grep -Fq 'Trecho C++ embutido' "$job.loc" || { echo 'Código embutido ausente da lista de códigos.'; exit 1; }
grep -Fq 'Arquivo C++ externo' "$job.loc" || { echo 'Código externo ausente da lista de códigos.'; exit 1; }
grep -Fq 'Busca linear' "$job.loa" || { echo 'Algoritmo ausente da lista de algoritmos.'; exit 1; }
grep -Fq 'Figura normativa de teste' "$job.loi" || { echo 'Figura ausente da lista unificada.'; exit 1; }
grep -Fq 'Gráfico normativo de teste' "$job.loi" || { echo 'Gráfico ausente da lista unificada.'; exit 1; }
grep -Fq 'Quadro multipágina de teste' "$job.loi" || { echo 'Quadro ausente da lista unificada.'; exit 1; }
if grep -Fq 'Tabela acadêmica de teste' "$job.loi"; then
  echo 'Preflight falhou: tabela entrou indevidamente na lista de ilustrações.'
  exit 1
fi

if command -v pdftotext >/dev/null 2>&1; then
  pdftotext -layout "$job.pdf" /tmp/abntexto-ufc-objects.txt
  for heading in 'LISTA DE ILUSTRAÇÕES' 'LISTA DE FIGURAS' 'LISTA DE TABELAS' 'LISTA DE QUADROS' 'LISTA DE GRÁFICOS' 'LISTA DE CÓDIGOS' 'LISTA DE ALGORITMOS'; do
    grep -Fq "$heading" /tmp/abntexto-ufc-objects.txt || {
      echo "Preflight falhou: lista de objeto ausente: $heading"
      exit 1
    }
  done

  python3 <<'PY'
import re
from pathlib import Path

text = Path('/tmp/abntexto-ufc-objects.txt').read_text(encoding='utf-8', errors='replace')

markers = (
    'Figura normativa de teste',
    'Gráfico normativo de teste',
    'Quadro multipágina de teste',
    'Tabela acadêmica de teste',
    'Trecho C++ embutido',
    'Arquivo C++ externo',
    'Busca linear',
)

for marker in markers:
    pattern = re.compile(re.escape(marker) + r'[^\n]*\.\s*(?:\.\s*)*\d+\s*$', re.M)
    if not pattern.search(text):
        raise SystemExit(
            f'Preflight falhou: líder pontilhado ausente na lista de objeto: {marker}'
        )
PY

  grep -Fq 'Fonte:' /tmp/abntexto-ufc-objects.txt || { echo 'Fonte de objeto ausente.'; exit 1; }
  grep -Fq 'Nota:' /tmp/abntexto-ufc-objects.txt || { echo 'Nota de objeto ausente.'; exit 1; }
  echo 'VALIDATION-EVIDENCE rule=illustration.source.required status=PASS expected=source-required measured=rendered-source-marker-present'
fi

echo 'Gate de objetos concluído.'
