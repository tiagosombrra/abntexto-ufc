#!/bin/sh
set -eu

fixture="tests/normativa/citacoes-referencias.tex"
job="citacoes-referencias"

cleanup_job() {
  rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
        "$job".out "$job".pdf "$job".run.xml "$job".toc
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
    pdftotext -layout "$job.pdf" /tmp/ufctex-v2-bib.txt

    grep -Fq 'Silva, 2020' /tmp/ufctex-v2-bib.txt || \
      (echo 'Citação autor-data simples incorreta.'; exit 1)
    if grep -Fq 'SILVA, 2020' /tmp/ufctex-v2-bib.txt; then
      echo 'Citação em caixa alta incompatível com NBR 10520:2023.'
      exit 1
    fi
    grep -Fq 'Oliveira; Nunes, 2011, p. 103' /tmp/ufctex-v2-bib.txt || \
      (echo 'Citação parentética de dois autores incorreta.'; exit 1)
    grep -Fq 'Oliveira e Nunes (2011, p. 103)' /tmp/ufctex-v2-bib.txt || \
      (echo 'Citação textual de dois autores incorreta.'; exit 1)
    grep -Fq 'Cruz; Perota; Mendes, 2000' /tmp/ufctex-v2-bib.txt || \
      (echo 'Citação de três autores incorreta.'; exit 1)
    grep -Fq 'Rocha et al., 2021, p. 198' /tmp/ufctex-v2-bib.txt || \
      (echo 'Citação com et al. incorreta.'; exit 1)
    grep -Fq 'Chiavenato, 2008a, 2008b' /tmp/ufctex-v2-bib.txt || \
      (echo 'Desambiguação de mesmo autor/ano incorreta.'; exit 1)
    grep -Fq 'Ferreira, 2006; Silva, 2020' /tmp/ufctex-v2-bib.txt || \
      (echo 'Ordenação de autores simultâneos incorreta.'; exit 1)
    grep -Fq 'Universidade Federal do Ceará, 2025' /tmp/ufctex-v2-bib.txt || \
      (echo 'Citação de pessoa jurídica incorreta.'; exit 1)
    grep -Fq 'Acrefino, 1993' /tmp/ufctex-v2-bib.txt || \
      (echo 'Citação de título de uma palavra incorreta.'; exit 1)
    grep -Fq 'Tribunal […], 2011' /tmp/ufctex-v2-bib.txt || \
      (echo 'Citação de título sem autoria incorreta.'; exit 1)
    grep -Fq 'O túnel […], 2005, p. 5' /tmp/ufctex-v2-bib.txt || \
      (echo 'Citação de título iniciado por artigo incorreta.'; exit 1)
    grep -Fq 'REFERÊNCIAS' /tmp/ufctex-v2-bib.txt || \
      (echo 'Título de referências ausente.'; exit 1)
    grep -Fq 'SILVA, João Carlos' /tmp/ufctex-v2-bib.txt || \
      (echo 'Entrada bibliográfica não preserva sobrenome em caixa alta.'; exit 1)
    grep -Fq '10.0000/ufctex.2025.1234' /tmp/ufctex-v2-bib.txt || \
      (echo 'DOI ausente da referência eletrônica.'; exit 1)
  fi

done

grep -Fq 'Referências' "$job.toc" || \
  (echo 'Referências ausentes do Sumário.'; exit 1)

echo 'Gate V2 de citações e referências concluído.'
