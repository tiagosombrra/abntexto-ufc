#!/bin/sh
set -eu

sh tests/integration/capes-guidance.sh
sh tests/integration/frontmatter-evidence.sh
sh tests/integration/frontmatter-alignment-evidence.sh
sh tests/integration/frontmatter-enforcement-negative.sh
sh tests/integration/frontmatter-acknowledgments-evidence.sh
sh tests/integration/frontmatter-summary-evidence.sh
sh tests/integration/frontmatter-cover-evidence.sh
sh tests/integration/frontmatter-title-page-evidence.sh
sh tests/integration/frontmatter-approval-evidence.sh
sh tests/integration/frontmatter-errata-evidence.sh
sh tests/integration/frontmatter-lists-evidence.sh
sh tests/integration/frontmatter-toc-evidence.sh
sh tests/integration/frontmatter-pagination-evidence.sh

fixtures="tests/documents/frontmatter-academic-work.tex tests/documents/frontmatter-anonymized-project.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

for engine in pdflatex lualatex; do
  for fixture in $fixtures; do
    echo "Validating $fixture with $engine..."
    for pass in 1 2; do
      "$engine" $flags "$fixture" > /tmp/abntexto-ufc-frontmatter.log 2>&1 || {
        cat /tmp/abntexto-ufc-frontmatter.log
        exit 1
      }
    done
    if [ "$fixture" = "tests/documents/frontmatter-academic-work.tex" ] && command -v pdftotext >/dev/null 2>&1; then
      python3 tests/checks/frontmatter_definition_alignment.py frontmatter-academic-work.pdf
    fi
  done
done

if grep -Eiq 'dedicat[oó]ria|agradecimentos|resumo|abstract|lista de' frontmatter-academic-work.toc; then
  echo 'Front matter validation failed: element front matter leaked into the table of contents.'
  cat frontmatter-academic-work.toc
  exit 1
fi

grep -Eiq 'Introdu' frontmatter-academic-work.toc || {
  echo 'Front matter validation failed: section textual missing from the table of contents.'
  exit 1
}

if command -v pdftotext >/dev/null 2>&1; then
  pdftotext frontmatter-academic-work.pdf /tmp/abntexto-ufc-frontmatter.txt
  for heading in 'AGRADECIMENTOS' 'RESUMO' 'ABSTRACT' 'LISTA DE FIGURAS' 'LISTA DE TABELAS' 'LISTA DE ABREVIATURAS E SIGLAS' 'LISTA DE SÍMBOLOS' 'SUMÁRIO'; do
    grep -Fq "$heading" /tmp/abntexto-ufc-frontmatter.txt || {
      echo "Front matter validation failed: heading front matter missing or incorrect: $heading"
      exit 1
    }
  done

  if grep -Eiq '^Dedicat[oó]ria$' /tmp/abntexto-ufc-frontmatter.txt; then
    echo 'Front matter validation failed: dedication received a heading.'
    exit 1
  fi

  pdftotext -bbox-layout frontmatter-academic-work.pdf /tmp/abntexto-ufc-frontmatter-bbox.html
  python3 - <<'PY'
import re
import xml.etree.ElementTree as ET

root = ET.parse('/tmp/abntexto-ufc-frontmatter-bbox.html').getroot()
local = lambda tag: tag.rsplit('}', 1)[-1]


def check_below_midpoint(label, marker):
    marker = marker.upper()
    for page in (node for node in root.iter() if local(node.tag) == 'page'):
        midpoint = float(page.attrib['height']) / 2
        for line in (node for node in page.iter() if local(node.tag) == 'line'):
            words = [node for node in line if local(node.tag) == 'word']
            if not words:
                continue
            text = re.sub(
                r'\s+',
                ' ',
                ' '.join(''.join(word.itertext()) for word in words),
            ).upper()
            if marker not in text:
                continue
            first_y = min(float(word.attrib['yMin']) for word in words)
            if first_y <= midpoint:
                raise SystemExit(
                    f'Front matter validation falhou: {label} inicia antes do meio da página: '
                    f'y={first_y:.2f}, meio={midpoint:.2f}'
                )
            return
    raise SystemExit(f'Front matter validation failed: page of {label} not found.')


check_below_midpoint('dedicatória', 'FAMÍLIA')
check_below_midpoint('epígrafe', 'CITAÇÃO DE EXEMPLO')
PY

  pdftotext frontmatter-anonymized-project.pdf /tmp/abntexto-ufc-anonimo.txt
  if grep -Fq 'AUTOR SIGILOSO TESTE' /tmp/abntexto-ufc-anonimo.txt; then
    echo 'Front matter validation failed: author leaked into the anonymized research project.'
    exit 1
  fi
  if grep -Fq 'ORIENTADOR SIGILOSO TESTE' /tmp/abntexto-ufc-anonimo.txt; then
    echo 'Front matter validation failed: advisor leaked into the anonymized research project.'
    exit 1
  fi
  grep -Fq 'PROJETO-ANONIMO-001' /tmp/abntexto-ufc-anonimo.txt || {
    echo 'Front matter validation failed: identifier anonymized missing.'
    exit 1
  }
fi

echo 'Front matter gate completed.'
