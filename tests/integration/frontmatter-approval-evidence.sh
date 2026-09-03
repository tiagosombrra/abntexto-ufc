#!/bin/sh
set -eu

fixture="tests/documents/frontmatter-approval-test.tex"
evidence="artifacts/frontmatter/approval-page.json"
academic_profiles="tccgraduacao tccespecializacao dissertacao tese"
suppressed_profiles="projeto projetoanonimizado"
all_profiles="$academic_profiles $suppressed_profiles"

cleanup() {
  for profile in $all_profiles; do
    job="frontmatter-validation-approval-$profile"
    rm -f "$job.aux" "$job.log" "$job.out" "$job.pdf" "$job.toc"
    rm -f "/tmp/abntexto-ufc-approval-$profile.tex"
  done
}
trap cleanup EXIT INT TERM

profile_args=""
for profile in $all_profiles; do
  job="frontmatter-validation-approval-$profile"
  generated="/tmp/abntexto-ufc-approval-$profile.tex"
  log="/tmp/abntexto-ufc-approval-$profile.log"

  case "$profile" in
    tccgraduacao) document_type="undergraduate-capstone" ;;
    tccespecializacao) document_type="specialization-capstone" ;;
    dissertacao) document_type="masters-thesis" ;;
    tese) document_type="doctoral-thesis" ;;
    projeto) document_type="research-project" ;;
    projetoanonimizado) document_type="anonymized-research-project" ;;
    *)
      echo "Unknown approval profile label: $profile"
      exit 1
      ;;
  esac

  sed "s/type = doctoral-thesis,/type = $document_type,/" "$fixture" > "$generated"

  type_lines=$(grep -Ec '^[[:space:]]*type[[:space:]]*=' "$generated" || true)
  if [ "$type_lines" -ne 1 ] || ! grep -Fq "type = $document_type," "$generated"; then
    echo "Approval profile generation failed for $profile -> $document_type."
    cat "$generated"
    exit 1
  fi

  for pass in 1 2; do
    pdflatex \
      -jobname="$job" \
      -interaction=nonstopmode \
      -halt-on-error \
      -file-line-error \
      "$generated" > "$log" 2>&1 || {
        cat "$log"
        exit 1
      }
  done

  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$job.log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Auditoria de folha de aprovação falhou: warning ou overflow não reconhecido no perfil $profile."
    exit 1
  fi

  profile_args="$profile_args $profile=$job.pdf"
done

mkdir -p "$(dirname "$evidence")"
# shellcheck disable=SC2086
python3 tests/checks/normative_frontmatter_approval.py \
  $profile_args \
  --json "$evidence" \
  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}" \
  --enforce

test -s "$evidence" || {
  echo 'Auditoria de folha de aprovação falhou: evidência JSON não foi gerada.'
  exit 1
}

echo 'Gate de evidência front matter para folha de aprovação concluído.'
