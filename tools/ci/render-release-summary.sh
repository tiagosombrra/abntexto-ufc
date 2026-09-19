#!/bin/sh
set -eu

echo '## Linux release validation'
echo
echo '> This Linux gate is engineering evidence. The retained Windows/literal-font proof remains separately scope-controlled.'
echo

if [ -f artifacts/validation/validation-report.md ]; then
  cat artifacts/validation/validation-report.md
else
  echo 'No repository validation report was produced.'
fi

echo
echo '### Canonical reference PDF'
if [ -f artifacts/validation/release-reference-reproducibility.json ]; then
  echo 'The full template/main.tex reference was built twice from this exact candidate, validated and retained as a dedicated artifact with source/hash provenance.'
else
  echo 'Canonical reference PDF provenance was not produced.'
fi

echo
echo '### CTAN pkgcheck'
if [ -f artifacts/validation/pkgcheck-version.txt ]; then
  printf '%s\n' '```text'
  cat artifacts/validation/pkgcheck-version.txt
  printf '%s\n' '```'
else
  echo 'pkgcheck version evidence was not produced.'
fi
if [ -f artifacts/validation/pkgcheck.log ]; then
  printf '%s\n' '```text'
  cat artifacts/validation/pkgcheck.log
  printf '%s\n' '```'
else
  echo 'pkgcheck output was not produced.'
fi

echo
echo '### Maintainer visual review'
if [ -f artifacts/release-review-pairs/manifest.json ]; then
  echo 'Seven PDF/TeX profile pairs were generated from this exact candidate and passed automated preflight. Explicit maintainer visual approval remains pending.'
else
  echo 'The seven-profile review-pair artifact was not produced.'
fi
