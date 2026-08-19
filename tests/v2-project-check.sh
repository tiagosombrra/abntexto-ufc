#!/bin/sh
set -eu

compile_project_with_biber() {
  engine="$1"
  job="projeto-15287"
  fixture="tests/normativa/projeto-15287.tex"

  rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
        "$job".out "$job".pdf "$job".run.xml "$job".toc

  echo "Validando $fixture com $engine + Biber..."
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/ufctex-v2-project.log 2>&1 || {
    cat /tmp/ufctex-v2-project.log
    exit 1
  }
  biber "$job" > /tmp/ufctex-v2-project-biber.log 2>&1 || {
    cat /tmp/ufctex-v2-project-biber.log
    exit 1
  }
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/ufctex-v2-project.log 2>&1 || {
    cat /tmp/ufctex-v2-project.log
    exit 1
  }
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/ufctex-v2-project.log 2>&1 || {
    cat /tmp/ufctex-v2-project.log
    exit 1
  }
}

compile_plain_project() {
  engine="$1"
  fixture="$2"
  job="$3"

  rm -f "$job".aux "$job".log "$job".out "$job".pdf "$job".toc
  echo "Validando $fixture com $engine..."
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/ufctex-v2-project.log 2>&1 || {
    cat /tmp/ufctex-v2-project.log
    exit 1
  }
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/ufctex-v2-project.log 2>&1 || {
    cat /tmp/ufctex-v2-project.log
    exit 1
  }
}

check_log() {
  log="$1"
  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$log" | \
    grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Preflight V2 falhou: fixture de projeto contém warning ou overflow não reconhecido."
    exit 1
  fi
}

for engine in pdflatex lualatex; do
  compile_project_with_biber "$engine"
  check_log projeto-15287.log

done

for engine in pdflatex lualatex; do
  compile_plain_project "$engine" tests/normativa/projeto-sem-capa.tex projeto-sem-capa
  check_log projeto-sem-capa.log

done

for engine in pdflatex lualatex; do
  compile_plain_project "$engine" tests/normativa/pretextuais-projeto-anonimo.tex pretextuais-projeto-anonimo
  check_log pretextuais-projeto-anonimo.log

done

if grep -Eq 'brasao-ufc\.pdf|logo-ufc\.PNG' projeto-15287.log; then
  echo 'NBR 15287/UFC: brasão foi carregado por padrão na capa de projeto.'
  exit 1
fi

if grep -Eq 'brasao-ufc\.pdf|logo-ufc\.PNG' pretextuais-projeto-anonimo.log; then
  echo 'NBR 15287/UFC: brasão foi carregado por padrão no projeto anonimizado.'
  exit 1
fi

if command -v pdftotext >/dev/null 2>&1; then
  pdftotext -layout projeto-15287.pdf /tmp/ufctex-v2-project.txt
  pdftotext -layout projeto-sem-capa.pdf /tmp/ufctex-v2-project-no-cover.txt
  pdftotext -layout pretextuais-projeto-anonimo.pdf /tmp/ufctex-v2-project-anon.txt

  python3 - <<'PY'
import re
import unicodedata
from pathlib import Path


def normalize(path):
    text = Path(path).read_text(encoding='utf-8')
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text)).strip()

project = normalize('/tmp/ufctex-v2-project.txt')
no_cover = normalize('/tmp/ufctex-v2-project-no-cover.txt')
anon = normalize('/tmp/ufctex-v2-project-anon.txt')

for expected in (
    'UNIVERSIDADE FEDERAL DO CEARÁ',
    'AUTOR PROJETO TESTE',
    'PROJETO DE PESQUISA NORMATIVO',
    'VALIDAÇÃO DA NBR 15287',
    'PROJECT RESEARCH NORMATIVE TEST',
    'VOLUME 2',
    'INTRODUÇÃO',
    'REFERENCIAL TEÓRICO',
    'METODOLOGIA',
    'RECURSOS',
    'CRONOGRAMA',
    'REFERÊNCIAS',
):
    if expected.casefold() not in project.casefold():
        raise SystemExit(f'NBR 15287:2025: conteúdo obrigatório da fixture ausente: {expected}')

if 'INSTITUIÇÃO DE ORIGEM TESTE'.casefold() in project.casefold():
    raise SystemExit('NBR 15287:2025: capa de projeto usou a IES no lugar da entidade de submissão.')

for forbidden in ('RESUMO', 'ABSTRACT', 'BANCA EXAMINADORA', 'APROVADA EM'):
    if forbidden.casefold() in project.casefold():
        raise SystemExit(f'NBR 15287:2025: elemento de trabalho final apareceu no projeto: {forbidden}')

if 'MARCADOR CAPA OPCIONAL'.casefold() in no_cover.casefold():
    raise SystemExit('NBR 15287:2025: capa opcional foi impressa apesar de capa=nao.')
if 'AUTOR SEM CAPA TESTE'.casefold() not in no_cover.casefold():
    raise SystemExit('NBR 15287:2025: folha de rosto obrigatória ausente no projeto sem capa.')

if 'AUTOR SIGILOSO TESTE'.casefold() in anon.casefold():
    raise SystemExit('Projeto anonimizado: autor vazou no PDF.')
if 'ORIENTADOR SIGILOSO TESTE'.casefold() in anon.casefold():
    raise SystemExit('Projeto anonimizado: orientador vazou no PDF.')
if 'PROJETO-ANONIMO-001'.casefold() not in anon.casefold():
    raise SystemExit('Projeto anonimizado: identificador público ausente.')
PY
fi

for expected in 'Introdução' 'Referencial teórico' 'Metodologia' 'Recursos' 'Cronograma' 'Referências'; do
  grep -Fqi "$expected" projeto-15287.toc || {
    echo "NBR 15287:2025: item ausente do Sumário: $expected"
    cat projeto-15287.toc
    exit 1
  }
done

if grep -Eiq 'resumo|abstract|agradecimentos|dedicat[oó]ria|folha de aprova' projeto-15287.toc; then
  echo 'NBR 15287:2025: elemento pré-textual indevido entrou no Sumário do projeto.'
  cat projeto-15287.toc
  exit 1
fi

echo 'Gate V2 NBR 15287:2025 concluído.'
