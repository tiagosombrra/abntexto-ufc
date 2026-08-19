#!/bin/sh
set -eu

fixture="tests/smoke/perfil-base.tex"
tmp_fixture=".ufctex-v2-profile.tex"
profiles="tccgraduacao tccespecializacao dissertacao tese projeto projetoanonimizado"

cleanup_profile() {
  job="$1"
  rm -f "$job".aux "$job".log "$job".out "$job".pdf "$job".toc
}

trap 'rm -f "$tmp_fixture"' EXIT INT TERM

for engine in pdflatex lualatex; do
  for profile in $profiles; do
    job="perfil-${profile}-${engine}"
    cleanup_profile "$job"
    sed "s/@UFC_TYPE@/$profile/g" "$fixture" > "$tmp_fixture"

    echo "Validando perfil $profile com $engine..."
    for pass in 1 2 3; do
      "$engine" -jobname="$job" -interaction=nonstopmode -halt-on-error -file-line-error "$tmp_fixture" > /tmp/ufctex-v2-profile.log 2>&1 || {
        cat /tmp/ufctex-v2-profile.log
        exit 1
      }
    done

    warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
      grep -vF -e 'Class ufctex Warning: Times New Roman not found; using TeX Gyre Termes' || true)
    if [ -n "$warnings" ]; then
      printf '%s\n' "$warnings"
      echo "Preflight V2 falhou: perfil $profile/$engine contém warning ou overflow não reconhecido."
      exit 1
    fi

    if command -v pdftotext >/dev/null 2>&1; then
      pdftotext -layout "$job.pdf" /tmp/ufctex-v2-profile.txt
      python3 - "$profile" <<'PY'
import re
import sys
import unicodedata
from pathlib import Path

profile = sys.argv[1]
raw = Path('/tmp/ufctex-v2-profile.txt').read_text(encoding='utf-8')
# PDF text extraction may preserve visual hyphenation at line breaks.
raw = re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '', raw)
text = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', raw)).strip()
fold = text.casefold()

expected = {
    'tccgraduacao': ('trabalho de conclusão de curso', 'curso de graduação em ciência da computação'),
    'tccespecializacao': ('trabalho de conclusão de curso', 'curso de especialização em computação aplicada'),
    'dissertacao': ('dissertação apresentada', 'mestre em ciência da computação'),
    'tese': ('tese apresentada', 'doutor em ciência da computação'),
    'projeto': ('projeto de pesquisa apresentado', 'universidade federal do ceará'),
    'projetoanonimizado': ('projeto de pesquisa apresentado', 'perfil-anonimo-001'),
}

for marker in expected[profile]:
    if marker.casefold() not in fold:
        raise SystemExit(f'Perfil {profile}: conteúdo semântico ausente: {marker}')

if 'capítulo' in fold or 'capitulo' in fold:
    raise SystemExit(f'Perfil {profile}: estrutura de capítulo reapareceu.')

if profile == 'projetoanonimizado':
    for secret in ('autor matriz teste', 'prof. orientador matriz teste'):
        if secret in fold:
            raise SystemExit(f'Perfil anonimizado vazou dado protegido: {secret}')
else:
    if 'autor matriz teste' not in fold:
        raise SystemExit(f'Perfil {profile}: autor esperado ausente.')
PY
    fi

    grep -Fqi 'Introdu' "$job.toc" || {
      echo "Perfil $profile/$engine: Introdução ausente do Sumário."
      cat "$job.toc"
      exit 1
    }
    grep -Fqi 'Metodologia' "$job.toc" || {
      echo "Perfil $profile/$engine: Metodologia ausente do Sumário."
      cat "$job.toc"
      exit 1
    }
    if grep -Eq '\\contentsline \{section\}\{[^}]*\*' "$job.toc"; then
      echo "Perfil $profile/$engine: entrada anômala com asterisco no Sumário."
      cat "$job.toc"
      exit 1
    fi
  done
done

echo 'Gate V2 da matriz de perfis concluído.'
