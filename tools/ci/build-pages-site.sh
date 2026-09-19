#!/bin/sh
set -eu

rm -rf _site
mkdir -p _site/validator
cp site/index.html _site/index.html
cp -a validator/. _site/validator/
touch _site/.nojekyll

test -s _site/index.html
test -s _site/validator/index.html
test -s _site/validator/app.js
test -s _site/validator/normative-catalog.js
grep -Fq 'href="./validator/"' _site/index.html
grep -Fq 'is not sent to a server' _site/validator/index.html

echo "PAGES-BUILD-EVIDENCE status=PASS root=_site validator=_site/validator"
