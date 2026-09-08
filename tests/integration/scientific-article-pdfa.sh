#!/bin/sh
set -eu

job="scientific-article"
pdf="template/$job.pdf"
evidence_dir="artifacts/final-certification"
source_sha="${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-local}}"

cleanup() {
  make DOCUMENT="$job" clean >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

make DOCUMENT="$job" ENGINE=pdflatex compile

[ -s "$pdf" ] || {
  echo "Scientific Article PDF/A certification failed: canonical PDF was not generated."
  exit 1
}

sh tests/integration/font-embedding.sh "$pdf"
sh tests/integration/pdfa.sh "$pdf"

mkdir -p "$evidence_dir"
cat > "$evidence_dir/scientific-article-pdfa.json" <<EOF
{
  "status": "PASS",
  "profile": "scientific-article",
  "engine": "pdflatex",
  "pdfa": "2b",
  "font_embedding": "PASS",
  "source_sha": "$source_sha"
}
EOF

echo 'FINAL-CERTIFICATION-EVIDENCE surface=scientific-article-pdfa status=PASS profile=scientific-article engine=pdflatex pdfa=2b font_embedding=PASS'
echo 'Scientific Article PDF/A-2b certification gate completed.'
