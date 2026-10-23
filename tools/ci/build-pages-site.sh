#!/bin/sh
set -eu

rm -rf _site
mkdir -p _site/validator
cp site/index.html _site/index.html
cp site/homepage-locales.js _site/homepage-locales.js
cp -a validator/. _site/validator/
touch _site/.nojekyll

test -s _site/index.html
test -s _site/homepage-locales.js
node --check _site/homepage-locales.js
grep -Fq 'src="./homepage-locales.js"' _site/index.html
grep -Fq 'id="home-locale"' _site/index.html
test -s _site/validator/index.html
test -s _site/validator/app.js
test -s _site/validator/normative-catalog.js
test -s _site/validator/vendor/pdfjs/pdf.mjs
test -s _site/validator/vendor/pdfjs/pdf.worker.mjs
test -s _site/validator/vendor/pdfjs/LICENSE
test -s _site/validator/vendor/pdfjs/PROVENANCE.json
grep -Fq 'from "./vendor/pdfjs/pdf.mjs"' _site/validator/app.js
grep -Fq 'workerSrc="./vendor/pdfjs/pdf.worker.mjs"' _site/validator/app.js
if grep -Eq 'cdn\.jsdelivr\.net|unpkg\.com' _site/validator/app.js; then
  echo "Pages validator must not depend on a runtime JavaScript CDN." >&2
  exit 1
fi
grep -Fq 'http-equiv="Content-Security-Policy"' _site/validator/index.html
grep -Fq "script-src 'self'" _site/validator/index.html
grep -Fq "worker-src 'self'" _site/validator/index.html
grep -Fq "connect-src 'self'" _site/validator/index.html
grep -Fq 'href="./validator/"' _site/index.html
grep -Fq '<html lang="pt-BR">' _site/validator/index.html
grep -Fq 'o arquivo não é enviado a um servidor' _site/validator/index.html

echo "PAGES-BUILD-EVIDENCE status=PASS root=_site validator=_site/validator"
