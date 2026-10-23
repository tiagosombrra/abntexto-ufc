#!/bin/sh
set -eu

: "${WEB_LITE_EVIDENCE_DIR:?WEB_LITE_EVIDENCE_DIR is required}"

test -s artifacts/validation/web-lite-positive.pdf
for profile_pdf in scientific-article research-project anonymized-research-project scientific-article-missing research-project-missing-refs; do
  test -s "artifacts/validation/document-profiles/$profile_pdf.pdf" || {
    echo "Web/Lite E2E: required actual-class PDF missing: $profile_pdf" >&2
    exit 1
  }
done
test -s artifacts/validation/document-profiles/cli-evidence.json
for pdf in geometry-single-sided geometry-double-sided; do
  test -s "artifacts/validation/duplex-margins/$pdf.pdf"
done
test -s artifacts/validation/duplex-margins/cli-evidence.json
mkdir -p "$WEB_LITE_EVIDENCE_DIR"
command -v chromedriver
if command -v google-chrome >/dev/null 2>&1; then
  google-chrome --version
elif command -v chromium >/dev/null 2>&1; then
  chromium --version
elif command -v chromium-browser >/dev/null 2>&1; then
  chromium-browser --version
else
  echo 'Web/Lite E2E failed: Chrome/Chromium is not installed on the GitHub runner.'
  exit 1
fi
chromedriver --version
sh tools/ci/build-pages-site.sh
python3 tests/integration/validator/web-lite-e2e.py \
  --pdf artifacts/validation/web-lite-positive.pdf \
  --profile portable \
  --document-pdf-dir artifacts/validation/document-profiles \
  --duplex-pdf-dir artifacts/validation/duplex-margins \
  --site-root _site/validator \
  --evidence "$WEB_LITE_EVIDENCE_DIR/web-lite-e2e.json"
python3 tests/integration/validator/homepage-locale-e2e.py \
  --site-root _site \
  --evidence "$WEB_LITE_EVIDENCE_DIR/homepage-locale-e2e.json"
