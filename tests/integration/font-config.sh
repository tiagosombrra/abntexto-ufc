#!/bin/sh
set -eu

fixture="tests/documents/font-configuration.tex"
tmp=".abntexto-ufc-font-config.tex"
flags="-interaction=nonstopmode -halt-on-error -file-line-error"

cleanup() {
  rm -f "$tmp" font-config-*.aux font-config-*.log font-config-*.out font-config-*.pdf
}
trap cleanup EXIT INT TERM

render_fixture() {
  family=$1
  strict=$2
  slot=$3
  sed \
    -e "s/@UFC_FONT@/$family/g" \
    -e "s/@UFC_STRICT@/$strict/g" \
    -e "s/@UFC_SLOT@/$slot/g" \
    "$fixture" > "$tmp"
}

expected_family() {
  engine=$1
  family=$2
  log=$3

  case "$family/$engine" in
    times/pdflatex)
      if grep -Fq 'Using literal Times New Roman with pdfLaTeX' "$log"; then echo 'TimesNewRoman'; else echo 'TeXGyreTermesX'; fi
      ;;
    arial/pdflatex)
      if grep -Fq 'Using literal Arial with pdfLaTeX' "$log"; then echo 'Arial'; else echo 'TeXGyreHeros'; fi
      ;;
    times/lualatex)
      if grep -Fq 'Using literal Times New Roman with LuaLaTeX' "$log"; then echo 'TimesNewRoman'; else echo 'TeXGyreTermes'; fi
      ;;
    arial/lualatex)
      if grep -Fq 'Using literal Arial with LuaLaTeX' "$log"; then echo 'Arial'; else echo 'TeXGyreHeros'; fi
      ;;
  esac
}

literal_available() {
  engine=$1
  family=$2
  log=$3
  case "$family/$engine" in
    times/pdflatex) grep -Fq 'Using literal Times New Roman with pdfLaTeX' "$log" ;;
    arial/pdflatex) grep -Fq 'Using literal Arial with pdfLaTeX' "$log" ;;
    times/lualatex) grep -Fq 'Using literal Times New Roman with LuaLaTeX' "$log" ;;
    arial/lualatex) grep -Fq 'Using literal Arial with LuaLaTeX' "$log" ;;
  esac
}

for engine in pdflatex lualatex; do
  for family in times arial; do
    baseline_log=''

    for slot in rm sf tt; do
      render_fixture "$family" nao "$slot"
      job="font-config-$family-$slot-$engine"
      echo "Validating $family/$slot in portable mode with $engine..."
      "$engine" -jobname="$job" $flags "$tmp" > "/tmp/$job.out" 2>&1 || {
        cat "/tmp/$job.out"
        exit 1
      }

      sh tests/integration/font-embedding.sh "$job.pdf"
      expected=$(expected_family "$engine" "$family" "$job.log")
      pdffonts "$job.pdf" | tail -n +3 | awk 'NF {print $1}' | grep -Fq "$expected" || {
        echo "$job: expected font family not found: $expected"
        pdffonts "$job.pdf"
        exit 1
      }

      if [ "$slot" = rm ]; then baseline_log="$job.log"; fi
    done

    render_fixture "$family" sim rm
    strict_job="font-config-$family-$engine-strict"
    if literal_available "$engine" "$family" "$baseline_log"; then
      echo "Validating literal $family in strict mode with $engine..."
      "$engine" -jobname="$strict_job" $flags "$tmp" > "/tmp/$strict_job.out" 2>&1 || {
        cat "/tmp/$strict_job.out"
        exit 1
      }
      sh tests/integration/font-embedding.sh "$strict_job.pdf"
    else
      echo "Validating strict rejection for unavailable literal $family with $engine..."
      if "$engine" -jobname="$strict_job" $flags "$tmp" > "/tmp/$strict_job.out" 2>&1; then
        echo "$strict_job: strict mode accepted an unavailable literal font."
        exit 1
      fi
      case "$family" in
        times) grep -Fq 'Times New Roman' "/tmp/$strict_job.out" ;;
        arial) grep -Fq 'Arial' "/tmp/$strict_job.out" ;;
      esac || {
        cat "/tmp/$strict_job.out"
        echo "$strict_job: failure did not identify the requested font."
        exit 1
      }
    fi
  done
done

echo 'Font configuration gate completed.'
