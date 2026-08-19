#!/bin/sh
set -eu

fixture="tests/normativa/citacoes-referencias.tex"
job="citacoes-referencias"

cleanup_job() {
  rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
        "$job".out "$job".pdf "$job".run.xml "$job".toc
}

fail_semantic() {
  cat /tmp/ufctex-v2-bib.txt
  echo "$1"
  exit 1
}

normalize_pdf_text() {
  pdftotext -layout "$job.pdf" /tmp/ufctex-v2-bib.raw
  python3 - <<'PY'
import re
import unicodedata
from pathlib import Path

text = Path('/tmp/ufctex-v2-bib.raw').read_text(encoding='utf-8')
text = unicodedata.normalize('NFC', text)
text = re.sub(r'\s+', ' ', text)
Path('/tmp/ufctex-v2-bib.txt').write_text(text, encoding='utf-8')
PY
}

check_apud_italic() {
  pdftohtml -xml -hidden -nodrm "$job.pdf" /tmp/ufctex-v2-bib-visual >/dev/null 2>&1
  python3 - <<'PY'
import xml.etree.ElementTree as ET

root = ET.parse('/tmp/ufctex-v2-bib-visual.xml').getroot()
fonts = {
    node.attrib['id']: node.attrib.get('family', '').lower()
    for node in root.iter('fontspec')
}
apud_nodes = [node for node in root.iter('text') if ''.join(node.itertext()).strip() == 'apud']
if len(apud_nodes) < 2:
    raise SystemExit('Preflight V2 falhou: apud não foi isolado tipograficamente no PDF.')
for node in apud_nodes:
    family = fonts.get(node.attrib.get('font', ''), '')
    if not any(marker in family for marker in ('italic', 'oblique', 'cmti')):
        raise SystemExit(f'Preflight V2 falhou: apud não está em itálico ({family}).')
PY
}

for engine in pdflatex lualatex; do
  cleanup_job
  echo "Validando $fixture com $engine + Biber..."

  if ! "$engine" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/ufctex-v2-bib.log 2>&1; then
    cat /tmp/ufctex-v2-bib.log
    exit 1
  fi

  if ! biber "$job" > /tmp/ufctex-v2-biber.log 2>&1; then
    cat /tmp/ufctex-v2-biber.log
    exit 1
  fi

  if ! "$engine" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/ufctex-v2-bib.log 2>&1; then
    cat /tmp/ufctex-v2-bib.log
    exit 1
  fi

  if ! "$engine" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/ufctex-v2-bib.log 2>&1; then
    cat /tmp/ufctex-v2-bib.log
    exit 1
  fi

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Preflight V2 falhou: fixture bibliográfica contém warnings ou overflow não reconhecidos."
    exit 1
  fi

  if command -v pdftotext >/dev/null 2>&1; then
    normalize_pdf_text

    grep -Fq 'Silva, 2020' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação autor-data simples incorreta.'
    if grep -Fq 'SILVA, 2020' /tmp/ufctex-v2-bib.txt; then
      fail_semantic 'Citação em caixa alta incompatível com NBR 10520:2023.'
    fi
    grep -Fq 'Oliveira; Nunes, 2011, p. 103' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação parentética de dois autores incorreta.'
    grep -Fq 'Oliveira e Nunes (2011, p. 103)' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação textual de dois autores incorreta.'
    grep -Fq 'Cruz; Perota; Mendes, 2000' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação de três autores incorreta.'
    grep -Fq 'Rocha et al., 2021, p. 198' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação com et al. incorreta.'
    grep -Fq 'Chiavenato, 2008a, 2008b' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Desambiguação de mesmo autor/ano incorreta.'
    grep -Fq 'Ferreira, 2006; Silva, 2020' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Ordenação de autores simultâneos incorreta.'
    grep -Fq 'Universidade Federal do Ceará, 2025' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação de pessoa jurídica incorreta.'
    grep -Fq 'Acrefino, 1993' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação de título de uma palavra incorreta.'
    grep -Eq 'Tribunal \[(…|\. ?\. ?\.) ?\], 2011' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação de título sem autoria incorreta.'
    grep -Eq 'O túnel \[(…|\. ?\. ?\.) ?\], 2005, p\. 5' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação de título iniciado por artigo incorreta.'
    grep -Fq 'Eco, 1983, p. 121 apud Koche, 2009, p. 147' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação de citação incorreta.'
    grep -Fq 'Eco (1983 apud Koche, 2009)' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Citação de citação textual incorreta.'
    grep -Fq 'REFERÊNCIAS' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Título de referências ausente.'
    grep -Fq 'SILVA, João Carlos' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Entrada bibliográfica não preserva sobrenome em caixa alta.'
    grep -Fq 'KOCHE, José Carlos' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'Fonte consultada no apud ausente das referências.'
    if grep -Fq 'ECO, Umberto' /tmp/ufctex-v2-bib.txt; then
      fail_semantic 'Fonte original do apud entrou indevidamente nas referências.'
    fi
    grep -Fq '10.0000/ufctex.2025.1234' /tmp/ufctex-v2-bib.txt || \
      fail_semantic 'DOI ausente da referência eletrônica.'

    if command -v pdftohtml >/dev/null 2>&1; then
      check_apud_italic
    fi
  fi

done

grep -Fq 'Referências' "$job.toc" || \
  (echo 'Referências ausentes do Sumário.'; exit 1)

echo 'Gate V2 de citações e referências concluído.'
