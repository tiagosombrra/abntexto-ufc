#!/bin/sh
set -eu

fixture="tests/normativa/build-minimo.tex"
job="ufctex-build-minimo"
stubdir="/tmp/ufctex-v2-build-stubs"

cleanup() {
  rm -rf "$stubdir"
  rm -f "$job".tex "$job".aux "$job".bbl "$job".bcf "$job".blg "$job".log \
    "$job".out "$job".pdf "$job".run.xml "$job".toc "$job".glo "$job".gls \
    "$job".glg "$job".idx "$job".ind "$job".ilg
}
trap cleanup EXIT INT TERM

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

  cp "$fixture" "$job.tex"
  echo "Validando fluxo make modular com $engine..."
  PATH="$stubdir:$PATH" make filename="$job" ENGINE="$engine" compile > /tmp/ufctex-v2-build.log 2>&1 || {
    cat /tmp/ufctex-v2-build.log
    exit 1
  }

  [ -f "$job.pdf" ] || {
    echo "$engine: make compile não gerou PDF."
    exit 1
  }

  if [ -s "$job.glo" ] || [ -s "$job.idx" ]; then
    echo "$engine: módulos desativados geraram entrada de glossário ou índice."
    exit 1
  fi

  if [ -s "$job.bcf" ] && grep -q '<bcf:datasource' "$job.bcf"; then
    echo "$engine: documento sem bibliografia declarou datasource inesperada."
    exit 1
  fi

  pdftotext -layout "$job.pdf" /tmp/ufctex-v2-build.txt
  grep -Fqi 'Marcador do build modular' /tmp/ufctex-v2-build.txt || {
    echo "$engine: conteúdo esperado ausente do PDF."
    exit 1
  }
done

echo 'Gate V2 do fluxo make modular concluído.'
