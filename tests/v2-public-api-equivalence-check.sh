#!/bin/sh
set -eu

fixture="tests/normativa/public-api-equivalence.tex"
engine="pdflatex"
pt_job="public-api-equivalence-pt"
en_job="public-api-equivalence-en"

cleanup_job() {
  job="$1"
  rm -f "$job".tex "$job".pdf "$job".aux "$job".bbl "$job".bcf \
    "$job".blg "$job".log "$job".out "$job".toc "$job".run.xml \
    "$job".lof "$job".lot "$job".loi "$job".logr "$job".loq \
    "$job".loc "$job".loa "$job".idx "$job".ind "$job".ilg \
    "$job".glo "$job".gls "$job".glg
}

build_mode() {
  mode="$1"
  job="$2"

  cleanup_job "$job"
  sed -e "s/@UFC_API_MODE@/$mode/g" \
      -e "s#tests/fixtures/exemplo.py#tests/fixtures/public-api-equivalence-example.py#g" \
      "$fixture" > "$job.tex"

  echo "Validando equivalência da API pública: mode=$mode engine=$engine..."
  make filename="$job" ENGINE="$engine" compile > "/tmp/$job-build.log" 2>&1 || {
    cat "/tmp/$job-build.log"
    exit 1
  }

  [ -s "$job.pdf" ] || {
    echo "B2R-B4: PDF ausente para $mode."
    exit 1
  }

  grep -Fq "N15-EVIDENCE B2R-B4-FIXTURE mode=$mode PASS" "$job.log" || {
    echo "B2R-B4: marcador de fixture ausente para $mode."
    exit 1
  }

  grep '^N15-B4-STATE|' "$job.log" > "/tmp/$job.state"
  state_lines=$(wc -l < "/tmp/$job.state" | tr -d ' ')
  [ "$state_lines" -ge 55 ] || {
    echo "B2R-B4: estado interno incompleto para $mode ($state_lines linhas)."
    cat "/tmp/$job.state"
    exit 1
  }

  pdftotext -layout "$job.pdf" "/tmp/$job.txt"
  pdfinfo "$job.pdf" | awk '/^Pages:/ || /^Page size:/' > "/tmp/$job.geometry"
  pdfinfo -meta "$job.pdf" > "/tmp/$job-meta.xml"
  grep -Fq '<pdfaid:part>2</pdfaid:part>' "/tmp/$job-meta.xml" || {
    echo "B2R-B4: declaração PDF/A part 2 ausente para $mode."
    exit 1
  }
  grep -Eq '<pdfaid:conformance>[Bb]</pdfaid:conformance>' "/tmp/$job-meta.xml" || {
    echo "B2R-B4: declaração PDF/A-2b ausente para $mode."
    exit 1
  }
}

build_mode pt "$pt_job"
build_mode en "$en_job"

cmp -s "/tmp/$pt_job.state" "/tmp/$en_job.state" || {
  echo 'B2R-B4: API EN/PT produziu estados internos diferentes.'
  diff -u "/tmp/$pt_job.state" "/tmp/$en_job.state" || true
  exit 1
}

cmp -s "/tmp/$pt_job.txt" "/tmp/$en_job.txt" || {
  echo 'B2R-B4: API EN/PT produziu texto renderizado diferente.'
  diff -u "/tmp/$pt_job.txt" "/tmp/$en_job.txt" | head -200 || true
  exit 1
}

cmp -s "/tmp/$pt_job.geometry" "/tmp/$en_job.geometry" || {
  echo 'B2R-B4: API EN/PT produziu paginação/geometria diferente.'
  diff -u "/tmp/$pt_job.geometry" "/tmp/$en_job.geometry" || true
  exit 1
}

for ext in toc lof lot loi logr loq loc loa bbl; do
  pt_file="$pt_job.$ext"
  en_file="$en_job.$ext"
  if [ -f "$pt_file" ] || [ -f "$en_file" ]; then
    [ -f "$pt_file" ] && [ -f "$en_file" ] || {
      echo "B2R-B4: artefato auxiliar .$ext existe em apenas uma variante."
      exit 1
    }
    cmp -s "$pt_file" "$en_file" || {
      echo "B2R-B4: artefato auxiliar .$ext divergiu entre EN/PT."
      diff -u "$pt_file" "$en_file" | head -160 || true
      exit 1
    }
  fi
done

rm -f /tmp/b4-raster-pt-*.png /tmp/b4-raster-en-*.png
pdftoppm -png -r 72 "$pt_job.pdf" /tmp/b4-raster-pt >/dev/null 2>&1
pdftoppm -png -r 72 "$en_job.pdf" /tmp/b4-raster-en >/dev/null 2>&1

python3 - <<'PY'
from __future__ import annotations

import hashlib
import re
from pathlib import Path


def page_key(path: Path) -> int:
    match = re.search(r'-(\d+)\.png$', path.name)
    if not match:
        raise SystemExit(f'B2R-B4: raster inesperado: {path}')
    return int(match.group(1))


def hashes(prefix: str) -> list[str]:
    pages = sorted(Path('/tmp').glob(f'{prefix}-*.png'), key=page_key)
    if not pages:
        raise SystemExit(f'B2R-B4: nenhum raster produzido para {prefix}')
    return [hashlib.sha256(page.read_bytes()).hexdigest() for page in pages]

pt = hashes('b4-raster-pt')
en = hashes('b4-raster-en')
if pt != en:
    raise SystemExit(
        'B2R-B4: raster EN/PT divergiu; '
        f'pt_pages={len(pt)} en_pages={len(en)}'
    )
print(f'N15-EVIDENCE B2R-B4-RASTER pages={len(pt)} sha256_equal=true')
PY

pages=$(pdfinfo "$pt_job.pdf" | awk '/^Pages:/ {print $2}')
state_lines=$(wc -l < "/tmp/$pt_job.state" | tr -d ' ')

echo "N15-EVIDENCE B2R-B4-EQUIVALENCE engine=$engine state_lines=$state_lines pages=$pages state=true text=true geometry=true aux=true raster=true pdfa=true"
