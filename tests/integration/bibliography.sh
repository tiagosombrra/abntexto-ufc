#!/bin/sh
set -eu

fixture="tests/documents/citations-references.tex"
job="citacoes-referencias"

cleanup_job() {
  rm -f "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
        "$job".out "$job".pdf "$job".run.xml "$job".toc
}

fail_semantic() {
  cat /tmp/abntexto-ufc-bib.txt
  echo "$1"
  exit 1
}

normalize_pdf_text() {
  pdftotext -layout "$job.pdf" /tmp/abntexto-ufc-bib.raw
  python3 - <<'PY'
import re
import unicodedata
from pathlib import Path

text = Path('/tmp/abntexto-ufc-bib.raw').read_text(encoding='utf-8')
text = unicodedata.normalize('NFC', text)
text = re.sub(r'\s+', ' ', text)
Path('/tmp/abntexto-ufc-bib.txt').write_text(text, encoding='utf-8')
PY
}

check_apud_italic() {
  pdftohtml -xml -hidden -nodrm "$job.pdf" /tmp/abntexto-ufc-bib-visual >/dev/null 2>&1
  python3 - <<'PY'
import xml.etree.ElementTree as ET

root = ET.parse('/tmp/abntexto-ufc-bib-visual.xml').getroot()
fonts = {
    node.attrib['id']: node.attrib.get('family', '').lower()
    for node in root.iter('fontspec')
}
apud_nodes = [node for node in root.iter('text') if ''.join(node.itertext()).strip() == 'apud']
if len(apud_nodes) < 2:
    raise SystemExit('Preflight failed: apud was not typographically isolated in the PDF.')
for node in apud_nodes:
    family = fonts.get(node.attrib.get('font', ''), '')
    structural_italic = any(child.tag.lower() == 'i' for child in node.iter())
    named_italic = any(marker in family for marker in ('italic', 'oblique', 'cmti'))
    if not (structural_italic or named_italic):
        raise SystemExit(f'Preflight failed: apud is not italic ({family}).')
PY
}

for engine in pdflatex lualatex; do
  cleanup_job
  echo "Validating $fixture with $engine + Biber..."

  if ! "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-bib.log 2>&1; then
    cat /tmp/abntexto-ufc-bib.log
    exit 1
  fi

  if ! biber "$job" > /tmp/abntexto-ufc-biber.log 2>&1; then
    cat /tmp/abntexto-ufc-biber.log
    exit 1
  fi

  if ! "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-bib.log 2>&1; then
    cat /tmp/abntexto-ufc-bib.log
    exit 1
  fi

  if ! "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$fixture" > /tmp/abntexto-ufc-bib.log 2>&1; then
    cat /tmp/abntexto-ufc-bib.log
    exit 1
  fi

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    if printf '%s\n' "$warnings" | grep -q 'Overfull'; then
      echo 'Contexto das caixas excedentes:'
      grep -n -B4 -A40 -E 'Overfull \\hbox|Overfull \\vbox' "$job.log" || true
    fi
    echo "Preflight failed: fixture bibliográfica contains warnings or overflow unrecognized."
    exit 1
  fi

  if command -v pdftotext >/dev/null 2>&1; then
    normalize_pdf_text

    grep -Fq 'Silva, 2020' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation author-date simple incorrect.'
    if grep -Fq 'SILVA, 2020' /tmp/abntexto-ufc-bib.txt; then fail_semantic 'citation in case uppercase incompatível with NBR 10520:2023.'; fi
    grep -Fq 'Oliveira; Nunes, 2011, p. 103' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation parenthetical of two authors incorrect.'
    grep -Fq 'Oliveira e Nunes (2011, p. 103)' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation textual of two authors incorrect.'
    grep -Fq 'Cruz; Perota; Mendes, 2000' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation of three authors incorrect.'
    grep -Fq 'Rocha et al., 2021, p. 198' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation with et al. incorrect.'
    grep -Fq 'Chiavenato, 2008a, 2008b' /tmp/abntexto-ufc-bib.txt || fail_semantic 'Desambiguação of same author/ano incorrect.'
    grep -Fq 'Rudio, 2002, 2003, 2007' /tmp/abntexto-ufc-bib.txt || fail_semantic 'Ordem cronológica of same authorship incorrect.'
    grep -Fq 'Rudio (2002, 2003, 2007)' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation textual of same authorship in years distinct incorrect.'
    grep -Fq 'Ferreira, C., 2007, p. 20' /tmp/abntexto-ufc-bib.txt || fail_semantic 'Desambiguação of the first author same-name incorrect.'
    grep -Fq 'Ferreira, L., 2007, p. 40' /tmp/abntexto-ufc-bib.txt || fail_semantic 'Desambiguação of the second author same-name incorrect.'
    grep -Fq 'C. Ferreira (2007, p. 20)' /tmp/abntexto-ufc-bib.txt || fail_semantic 'form textual of the first author same-name incorrect.'
    grep -Fq 'L. Ferreira (2007, p. 40)' /tmp/abntexto-ufc-bib.txt || fail_semantic 'form textual of the second author same-name incorrect.'
    grep -Fq 'Ferreira, 2006; Silva, 2020' /tmp/abntexto-ufc-bib.txt || fail_semantic 'Ordenação of authors simultaneous incorrect.'
    grep -Fq 'Universidade Federal do Ceará, 2025' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation of person corporate incorrect.'
    grep -Fq 'Acrefino, 1993' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation of heading of a word incorrect.'
    grep -Eq 'Tribunal \[(…|\. ?\. ?\.) ?\], 2011' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation of heading without authorship incorrect.'
    grep -Eq 'O túnel \[(…|\. ?\. ?\.) ?\], 2005, p\. 5' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation of heading iniciado by artigo incorrect.'
    grep -Fq 'Eco, 1983, p. 121 apud Koche, 2009, p. 147' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation of citation incorrect.'
    grep -Fq 'Eco (1983 apud Koche, 2009)' /tmp/abntexto-ufc-bib.txt || fail_semantic 'citation of citation textual incorrect.'
    grep -Fq 'REFERÊNCIAS' /tmp/abntexto-ufc-bib.txt || fail_semantic 'heading of references missing.'
    grep -Fq 'SILVA, João Carlos' /tmp/abntexto-ufc-bib.txt || fail_semantic 'Entrada bibliográfica não preserva sobrenome em caixa alta.'
    grep -Fq 'KOCHE, José Carlos' /tmp/abntexto-ufc-bib.txt || fail_semantic 'source consultada in the apud missing of the references.'
    if grep -Fq 'ECO, Umberto' /tmp/abntexto-ufc-bib.txt; then fail_semantic 'source original of the apud was incorrectly included in the references.'; fi
    grep -Fq 'e1234' /tmp/abntexto-ufc-bib.txt || fail_semantic 'E-location missing of the reference electronic.'
    grep -Fq '10.0000/exemplo.2025.1234' /tmp/abntexto-ufc-bib.txt || fail_semantic 'DOI missing of the reference electronic.'
    grep -Fq 'SIMPÓSIO INTERNACIONAL DE TESTE' /tmp/abntexto-ufc-bib.txt || fail_semantic 'reference of event missing.'
    if grep -Eq 'SIMPÓSIO INTERNACIONAL DE TESTE,? 2025,? \[[Ss]\. ?[Ll]\.\]' /tmp/abntexto-ufc-bib.txt; then fail_semantic 'Evento sem cidade recebeu sine loco indevidamente.'; fi

    if command -v pdftohtml >/dev/null 2>&1; then check_apud_italic; fi
  fi
done

grep -Fq 'Referências' "$job.toc" || (echo 'references missing from the table of contents.'; exit 1)
echo 'Citations and references gate completed.'

sh tests/integration/references-6023.sh
sh tests/integration/short-direct-citation-evidence.sh
sh tests/integration/direct-citation-source-evidence.sh
sh tests/integration/indirect-citation-source-evidence.sh
sh tests/integration/ufc-citation-system-evidence.sh
sh tests/integration/apud-evidence.sh
