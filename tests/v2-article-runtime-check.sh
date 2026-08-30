#!/bin/sh
set -eu

python3 tests/checks/normative_n15_b2b_article_runtime.py

compile_article() {
  engine="$1"
  mode="$2"
  job="article-${mode}-${engine}"

  if [ "$mode" = "compat" ]; then
    source='\def\UFCArticleCompatibilitySetup{1}\input{tests/smoke/article-base.tex}'
  else
    source='\input{tests/smoke/article-base.tex}'
  fi

  rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
        "$job".out "$job".pdf "$job".run.xml "$job".toc

  echo "Validando perfil artigo ($mode) com $engine + Biber..."
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error \
    -jobname="$job" "$source" > "/tmp/abntexto-ufc-${job}.log" 2>&1 || {
      cat "/tmp/abntexto-ufc-${job}.log"
      exit 1
    }

  biber "$job" > "/tmp/abntexto-ufc-${job}-biber.log" 2>&1 || {
    cat "/tmp/abntexto-ufc-${job}-biber.log"
    exit 1
  }

  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error \
    -jobname="$job" "$source" > "/tmp/abntexto-ufc-${job}.log" 2>&1 || {
      cat "/tmp/abntexto-ufc-${job}.log"
      exit 1
    }
  "$engine" -interaction=nonstopmode -halt-on-error -file-line-error \
    -jobname="$job" "$source" > "/tmp/abntexto-ufc-${job}.log" 2>&1 || {
      cat "/tmp/abntexto-ufc-${job}.log"
      exit 1
    }

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "N15-B2B: fixture de artigo contém warning ou overflow não reconhecido."
    exit 1
  fi

  if [ ! -s "$job.pdf" ]; then
    echo "N15-B2B: PDF do artigo não foi gerado: $job.pdf"
    exit 1
  fi

  if command -v pdftotext >/dev/null 2>&1; then
    pdftotext -layout "$job.pdf" "/tmp/${job}.txt"
  fi
}

for engine in pdflatex lualatex; do
  compile_article "$engine" canonical
  compile_article "$engine" compat

done

if command -v pdftotext >/dev/null 2>&1; then
  python3 - <<'PY'
import re
import unicodedata
from pathlib import Path


def normalize(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()

expected = (
    "PERFIL NORMATIVO DE ARTIGO CIENTÍFICO: FIXTURE DE VALIDAÇÃO",
    "Maria Silva",
    "Pesquisadora na área de normalização acadêmica",
    "Universidade Federal do Ceará",
    "maria.silva@example.org",
    "RESUMO",
    "Palavras-chave:",
    "Artigo científico; Normalização; Universidade Federal do Ceará.",
    "ABSTRACT",
    "Keywords:",
    "Data de submissão: 15 de agosto de 2026",
    "Data de aprovação: 29 de agosto de 2026",
    "1 INTRODUÇÃO",
    "2 DESENVOLVIMENTO",
    "3 CONSIDERAÇÕES FINAIS",
    "REFERÊNCIAS",
)

for engine in ("pdflatex", "lualatex"):
    canonical = normalize(f"/tmp/article-canonical-{engine}.txt")
    compat = normalize(f"/tmp/article-compat-{engine}.txt")
    for item in expected:
        if item.casefold() not in canonical.casefold():
            raise SystemExit(f"N15-B2B: conteúdo canônico ausente ({engine}): {item}")
        if item.casefold() not in compat.casefold():
            raise SystemExit(f"N15-B2B: conteúdo de compatibilidade ausente ({engine}): {item}")
    if canonical != compat:
        raise SystemExit(f"N15-B2B: formas EN/PT divergem no texto extraído ({engine}).")
PY
fi

for engine in pdflatex lualatex; do
  for mode in canonical compat; do
    job="article-${mode}-${engine}"
    rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
          "$job".out "$job".pdf "$job".run.xml "$job".toc
  done
done

echo 'N15-EVIDENCE article-runtime-smoke engines=2 api_forms=2 status=PASS'
echo 'Gate N15-B2B artigo científico concluído.'
