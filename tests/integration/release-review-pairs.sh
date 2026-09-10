#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
cd "$ROOT"

OUTPUT_DIR="${UFC_REVIEW_PAIRS_DIR:-artifacts/release-review-pairs}"
SOURCE_SHA="${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-$(git -c "safe.directory=$ROOT" rev-parse HEAD)}}"
VERSION="$(make version)"
PINNED_UPSTREAM_COMMIT="4c03fd7b5a7af089627dedb547c53cad4eed2a2a"
UPSTREAM_FILE="abntexto.cls"
UPSTREAM_PREEXISTING=false
PROFILES="undergraduate-capstone specialization-capstone masters-thesis doctoral-thesis research-project anonymized-research-project"
FIXTURE="tests/smoke/base-profile.tex"

[ -f "$UPSTREAM_FILE" ] && UPSTREAM_PREEXISTING=true

cleanup_job() {
  job="$1"
  rm -f "template/$job.tex" "template/$job.aux" "template/$job.bbl" \
    "template/$job.bcf" "template/$job.blg" "template/$job.fdb_latexmk" \
    "template/$job.fls" "template/$job.glg" "template/$job.glo" \
    "template/$job.gls" "template/$job.idx" "template/$job.ilg" \
    "template/$job.ind" "template/$job.lof" "template/$job.log" \
    "template/$job.lot" "template/$job.out" "template/$job.pdf" \
    "template/$job.run.xml" "template/$job.synctex.gz" "template/$job.toc"
  rm -rf "template/_minted-$job"
}

cleanup() {
  for profile in $PROFILES; do
    cleanup_job "release-review-$profile"
  done
  make DOCUMENT=scientific-article clean >/dev/null 2>&1 || true
  if [ "$UPSTREAM_PREEXISTING" = false ]; then
    rm -f "$UPSTREAM_FILE"
  fi
}
trap cleanup EXIT INT TERM

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

python3 tools/fetch-abntexto.py --output "$UPSTREAM_FILE"

check_log() {
  log="$1"
  warnings=$(grep -E 'LaTeX Warning:|Package [^ ]+ Warning:|Class [^ ]+ Warning:|Overfull \\hbox|Overfull \\vbox' "$log" | \
    grep -vF -e 'Class abntexto-ufc Warning: Times New Roman not found; using TeX Gyre Termes' || true)
  if [ -n "$warnings" ]; then
    printf '%s\n' "$warnings"
    echo "Release review-pair preflight failed: unrecognized warning or overflow in $log."
    exit 1
  fi
}

check_pdf() {
  pdf="$1"
  profile="$2"

  [ -s "$pdf" ] || {
    echo "Release review-pair preflight failed: missing PDF for $profile: $pdf"
    exit 1
  }

  if ! pdfinfo "$pdf" | awk '
    /^Page size:/ {
      width = $3 + 0
      height = $5 + 0
      if (width < 594.5 || width > 596.0 || height < 841.0 || height > 842.8)
        exit 1
      found = 1
    }
    END { if (!found) exit 1 }
  '; then
    pdfinfo "$pdf"
    echo "Release review-pair preflight failed: $profile is not A4."
    exit 1
  fi

  sh tests/integration/font-embedding.sh "$pdf"
  UFC_PDFA_NEGATIVE_VALIDATION=0 sh tests/integration/pdfa.sh "$pdf"
}

index=1
for profile in $PROFILES; do
  job="release-review-$profile"
  source="template/$job.tex"
  cleanup_job "$job"

  sed \
    -e "s/@UFC_TYPE@/$profile/g" \
    -e 's#tests/fixtures/references.bib#../tests/fixtures/references.bib#g' \
    "$FIXTURE" > "$source"

  if grep -Fq '@UFC_TYPE@' "$source"; then
    echo "Release review-pair generation failed: placeholder survived for $profile."
    exit 1
  fi

  make DOCUMENT="$job" ENGINE=pdflatex compile > "/tmp/$job.log" 2>&1 || {
    cat "/tmp/$job.log"
    exit 1
  }

  check_log "template/$job.log"
  check_pdf "template/$job.pdf" "$profile"

  prefix=$(printf '%02d-%s' "$index" "$profile")
  cp "$source" "$OUTPUT_DIR/$prefix.tex"
  cp "template/$job.pdf" "$OUTPUT_DIR/$prefix.pdf"
  index=$((index + 1))
done

make DOCUMENT=scientific-article ENGINE=pdflatex compile > /tmp/release-review-scientific-article.log 2>&1 || {
  cat /tmp/release-review-scientific-article.log
  exit 1
}
check_log "template/scientific-article.log"
check_pdf "template/scientific-article.pdf" "scientific-article"
cp template/scientific-article.tex "$OUTPUT_DIR/07-scientific-article.tex"
cp template/scientific-article.pdf "$OUTPUT_DIR/07-scientific-article.pdf"

(
  cd "$OUTPUT_DIR"
  sha256sum ./*.tex ./*.pdf > SHA256SUMS
)

python3 - "$OUTPUT_DIR" "$SOURCE_SHA" "$VERSION" "$PINNED_UPSTREAM_COMMIT" <<'PY'
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
source_sha = sys.argv[2]
version = sys.argv[3]
upstream_commit = sys.argv[4]
profiles = [
    "undergraduate-capstone",
    "specialization-capstone",
    "masters-thesis",
    "doctoral-thesis",
    "research-project",
    "anonymized-research-project",
    "scientific-article",
]

pairs = []
for index, profile in enumerate(profiles, 1):
    prefix = f"{index:02d}-{profile}"
    source = root / f"{prefix}.tex"
    pdf = root / f"{prefix}.pdf"
    if not source.is_file() or not pdf.is_file():
        raise SystemExit(f"Release review-pair manifest failed: missing pair for {profile}")
    pairs.append(
        {
            "profile": profile,
            "source": source.name,
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "pdf": pdf.name,
            "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "engine": "pdflatex",
            "preflight": {
                "a4": "PASS",
                "pdfa_2b": "PASS",
                "font_embedding": "PASS",
                "recognized_warning_overflow": "PASS",
            },
        }
    )

payload = {
    "status": "READY_FOR_MAINTAINER_REVIEW",
    "version": version,
    "source_sha": source_sha,
    "pinned_abntexto_commit": upstream_commit,
    "pair_count": len(pairs),
    "maintainer_visual_approval": "PENDING",
    "pairs": pairs,
}
(root / "manifest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
PY

printf '%s\n' \
  "RELEASE-REVIEW-PAIRS-EVIDENCE status=PASS version=$VERSION source_sha=$SOURCE_SHA pairs=7 engine=pdflatex pinned_abntexto=$PINNED_UPSTREAM_COMMIT a4=PASS pdfa_2b=PASS font_embedding=PASS warnings_overflow=PASS maintainer_approval=PENDING"
echo 'Seven-profile release review pairs are ready for explicit maintainer visual approval.'
