#!/bin/sh
set -eu

python3 -m py_compile \
  tests/checks/governance/normative_negative_paths.py \
  tests/checks/governance/normative_configuration.py

python3 tests/checks/governance/normative_negative_paths.py \
  --json artifacts/negative-paths/negative-paths.json

test -s artifacts/negative-paths/negative-paths.json || {
  echo 'Negative-path validation failed: aggregate evidence JSON was not generated.'
  exit 1
}

python3 tests/checks/governance/normative_configuration.py \
  --json artifacts/negative-paths/configuration-strict-rejection.json

test -s artifacts/negative-paths/configuration-strict-rejection.json || {
  echo 'Negative-path validation failed: strict configuration evidence was not generated.'
  exit 1
}

echo 'NEGATIVE-PATH-GATE status=PASS'
