#!/bin/sh
set -eu

fixture="tests/normativa/build-minimo.tex"
job="abntexto-ufc-build-minimo"
legacy_job="ufctex-compat-minimo"
stubdir="/tmp/abntexto-ufc-v2-build-stubs"

cleanup() {
  rm -rf "$stubdir"
  for target in "$job" "$legacy_job"; do
    rm -f "$target".tex "$target".aux "$target".bbl "$target".bcf "$target".blg "$target".log \
      "$target".out "$target".pdf "$target".run.xml "$target".toc "$target".glo "$target".gls \
      "$target".glg "$target".idx "$target".ind "$target".ilg
  done
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
  echo "Validando fluxo make modular canônico com $engine..."
  PATH="$stubdir:$PATH" make filename="$job" ENGINE="$engine" compile > /tmp/abntexto-ufc-v2-build.log 2>&1 || {
    cat /tmp/abntexto-ufc-v2-build.log
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

  pdftotext -layout "$job.pdf" /tmp/abntexto-ufc-v2-build.txt
  grep -Fqi 'Marcador do build modular' /tmp/abntexto-ufc-v2-build.txt || {
    echo "$engine: conteúdo esperado ausente do PDF."
    exit 1
  }
done

cleanup
sed 's/\\documentclass{abntexto-ufc}/\\documentclass{ufctex}/' "$fixture" > "$legacy_job.tex"
echo 'Validando shim de compatibilidade ufctex com pdflatex...'
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error "$legacy_job.tex" > /tmp/ufctex-compat-build.log 2>&1 || {
  cat /tmp/ufctex-compat-build.log
  exit 1
}
[ -f "$legacy_job.pdf" ] || {
  echo 'Shim ufctex não gerou PDF.'
  exit 1
}
grep -Fqi 'deprecated' "$legacy_job.log" || {
  echo 'Shim ufctex não emitiu aviso de depreciação.'
  exit 1
}
pdftotext -layout "$legacy_job.pdf" /tmp/ufctex-compat-build.txt
grep -Fqi 'Marcador do build modular' /tmp/ufctex-compat-build.txt || {
  echo 'Conteúdo esperado ausente do PDF gerado pelo shim ufctex.'
  exit 1
}

echo 'Gate V2 do fluxo make modular e compatibilidade de classe concluído.'
