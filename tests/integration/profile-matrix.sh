#!/bin/sh
set -eu

fixture="tests/smoke/base-profile.tex"
template_dir="template"
profiles="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project"

cleanup_job() {
  job="$1"
  rm -f "$template_dir/$job".tex "$template_dir/$job".aux "$template_dir/$job".bbl \
    "$template_dir/$job".bcf "$template_dir/$job".blg "$template_dir/$job".log \
    "$template_dir/$job".out "$template_dir/$job".toc "$template_dir/$job".run.xml \
    "$template_dir/$job".pdf
}

for engine in pdflatex lualatex; do
  for profile in $profiles; do
    job="perfil-${profile}-${engine}"
    output="$template_dir/$job"
    cleanup_job "$job"
    sed \
      -e "s/@UFC_TYPE@/$profile/g" \
      -e 's#tests/fixtures/references.bib#../tests/fixtures/references.bib#g' \
      "$fixture" > "$output.tex"

    echo "Validando perfil completo $profile com $engine..."
    make DOCUMENT="$job" ENGINE="$engine" compile > /tmp/abntexto-ufc-profile.log 2>&1 || {
      cat /tmp/abntexto-ufc-profile.log
      exit 1
    }
    rm -f "$output.tex"

    warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$output.log" || true)
    if [ -n "$warnings" ]; then
      printf '%s\n' "$warnings"
      echo "Preflight falhou: perfil $profile/$engine contém warning ou overflow não reconhecido."
      exit 1
    fi

    if [ -f "$output.blg" ] && grep -Eq 'WARN|ERROR' "$output.blg"; then
      cat "$output.blg"
      echo "Preflight falhou: Biber reportou warning/error em $profile/$engine."
      exit 1
    fi

    [ -s "$output.pdf" ] || {
      echo "Perfil $profile/$engine: PDF não foi gerado."
      exit 1
    }

    meta="/tmp/$job-meta.xml"
    pdfinfo -meta "$output.pdf" > "$meta"
    grep -Fq '<pdfaid:part>2</pdfaid:part>' "$meta" || {
      echo "Perfil $profile/$engine: declaração PDF/A part 2 ausente."
      exit 1
    }
    grep -Eq '<pdfaid:conformance>[Bb]</pdfaid:conformance>' "$meta" || {
      echo "Perfil $profile/$engine: declaração PDF/A-2b ausente."
      exit 1
    }

    if ! pdfinfo "$output.pdf" | awk '
      /^Page size:/ {
        width = $3 + 0
        height = $5 + 0
        if (width < 594.5 || width > 596.0 || height < 841.0 || height > 842.8)
          exit 1
        found = 1
      }
      END { if (!found) exit 1 }
    '; then
      pdfinfo "$output.pdf"
      echo "Perfil $profile/$engine: página não é A4."
      exit 1
    fi

    pages=$(pdfinfo "$output.pdf" | awk '/^Pages:/ {print $2}')
    [ "${pages:-0}" -ge 6 ] || {
      echo "Perfil $profile/$engine: documento completo gerou apenas ${pages:-0} páginas."
      exit 1
    }

    sh tests/integration/font-embedding.sh "$output.pdf"

    pdftotext -layout "$output.pdf" "/tmp/$job.txt"
    python3 - "$profile" "$job" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

profile, job = sys.argv[1:3]
raw = Path(f'/tmp/{job}.txt').read_text(encoding='utf-8')
raw = re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', raw)
text = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', raw)).strip().casefold()

expected = {
    'undergraduate-capstone': (
        'curso de graduação em ciência da computação',
        'trabalho de conclusão de curso',
        'banca examinadora',
        'resumo',
        'abstract',
    ),
    'specialization-capstone': (
        'curso de especialização em computação aplicada',
        'trabalho de conclusão de curso',
        'especialista em computação aplicada',
        'banca examinadora',
    ),
    'masters-thesis': (
        'dissertação apresentada',
        'mestre em ciência da computação',
        'área de concentração: computação gráfica',
        'banca examinadora',
    ),
    'doctoral-thesis': (
        'tese apresentada',
        'doutor em ciência da computação',
        'área de concentração: computação gráfica',
        'banca examinadora',
    ),
    'research-project': (
        'projeto de pesquisa apresentado',
        'processo seletivo de teste',
        'referencial teórico',
        'recursos',
        'cronograma',
    ),
    'anonymized-research-project': (
        'projeto de pesquisa apresentado',
        'perfil-anonimo-001',
        'referencial teórico',
        'recursos',
        'cronograma',
    ),
}

for marker in expected[profile]:
    if marker not in text:
        raise SystemExit(f'Perfil {profile}: conteúdo semântico ausente: {marker}')

for marker in ('introdução', 'metodologia', 'referências', 'fundamentos de metodologia acadêmica'):
    if marker not in text:
        raise SystemExit(f'Perfil {profile}: conteúdo estrutural ausente: {marker}')

if 'capítulo' in text or 'capitulo' in text:
    raise SystemExit(f'Perfil {profile}: estrutura de capítulo reapareceu.')

if profile == 'anonymized-research-project':
    for secret in ('autor matriz teste', 'prof. orientador matriz teste', 'prof. membro matriz teste'):
        if secret in text:
            raise SystemExit(f'Perfil anonimizado vazou dado protegido: {secret}')
else:
    if 'autor matriz teste' not in text:
        raise SystemExit(f'Perfil {profile}: autor esperado ausente.')

if profile in {'research-project', 'anonymized-research-project'}:
    for forbidden in ('banca examinadora', 'abstract'):
        if forbidden in text:
            raise SystemExit(f'Perfil {profile}: elemento de trabalho acadêmico apareceu indevidamente: {forbidden}')
PY

    grep -Fqi 'Introdu' "$output.toc" || {
      echo "Perfil $profile/$engine: Introdução ausente do Sumário."
      cat "$output.toc"
      exit 1
    }
    grep -Fqi 'Metodologia' "$output.toc" || {
      echo "Perfil $profile/$engine: Metodologia ausente do Sumário."
      cat "$output.toc"
      exit 1
    }
    if grep -Eq '\\contentsline \{section\}\{[^}]*\*' "$output.toc"; then
      echo "Perfil $profile/$engine: entrada anômala com asterisco no Sumário."
      cat "$output.toc"
      exit 1
    fi
  done
done

echo 'Gate da matriz completa de perfis concluído.'
