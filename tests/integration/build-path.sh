#!/bin/sh
set -eu

fixture="tests/documents/minimal-build.tex"
job="abntexto-ufc-minimal-build"
template_job="template/$job"
stubdir="/tmp/abntexto-ufc-build-stubs"

cleanup() {
  rm -rf "$stubdir"
  target="$template_job"
  rm -f "$target".tex "$target".aux "$target".bbl "$target".bcf "$target".blg "$target".log \
    "$target".out "$target".pdf "$target".run.xml "$target".toc "$target".glo "$target".gls \
    "$target".glg "$target".idx "$target".ind "$target".ilg
}
trap cleanup EXIT INT TERM

MAKE_CMD=""
for candidate in make mingw32-make gmake; do
  if command -v "$candidate" >/dev/null 2>&1; then
    MAKE_CMD="$candidate"
    break
  fi
done

if [ -z "$MAKE_CMD" ]; then
  echo "SKIP: no compatible make implementation found (make/mingw32-make/gmake)."
  exit 77
fi

for engine in pdflatex lualatex; do
  cleanup
  mkdir -p "$stubdir"
  for tool in biber makeglossaries makeindex; do
    cat > "$stubdir/$tool" <<'SH'
#!/bin/sh
echo "Processador auxiliar não deveria ter sido chamado: $0" >&2
exit 99
SH
    chmod +x "$stubdir/$tool"
  done

  cp "$fixture" "$template_job.tex"
  echo "Validating canonical modular Makefile flow with $engine..."
  PATH="$stubdir:$PATH" "$MAKE_CMD" DOCUMENT="$job" ENGINE="$engine" compile > /tmp/abntexto-ufc-build.log 2>&1 || {
    cat /tmp/abntexto-ufc-build.log
    exit 1
  }

  [ -f "$template_job.pdf" ] || {
    echo "$engine: make compile did not produce the expected PDF."
    exit 1
  }

  if [ -s "$template_job.glo" ] || [ -s "$template_job.idx" ]; then
    echo "$engine: disabled modules generated glossary or index input."
    exit 1
  fi

  if [ -s "$template_job.bcf" ] && grep -q '<bcf:datasource' "$template_job.bcf"; then
    echo "$engine: bibliography-free document declared an unexpected datasource."
    exit 1
  fi

  pdftotext -layout "$template_job.pdf" /tmp/abntexto-ufc-build.txt
  grep -Fqi 'Marcador do build modular' /tmp/abntexto-ufc-build.txt || {
    echo "$engine: expected content is missing from the generated PDF."
    exit 1
  }
done

cleanup

echo 'Canonical modular build-path gate completed.'
