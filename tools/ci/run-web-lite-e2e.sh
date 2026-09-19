#!/bin/sh
set -eu

: "${WEB_LITE_EVIDENCE_DIR:?WEB_LITE_EVIDENCE_DIR is required}"

test -s artifacts/validation/web-lite-positive.pdf
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
python3 tests/integration/web-lite-e2e.py \
  --pdf artifacts/validation/web-lite-positive.pdf \
  --profile portable \
  --evidence "$WEB_LITE_EVIDENCE_DIR/web-lite-e2e.json"
