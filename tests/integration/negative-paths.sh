#!/bin/sh
set -eu

python3 -m py_compile \
  tests/checks/normative_n13_negative_paths.py \
  tests/checks/normative_n13_campaign.py \
  tests/checks/normative_n13_configuration.py

python3 tests/checks/normative_n13_campaign.py \
  --json artifacts/n13-negative/negative-paths.json

test -s artifacts/n13-negative/negative-paths.json || {
  echo 'N13 negative-path gate failed: aggregate evidence JSON was not generated.'
  exit 1
}

python3 tests/checks/normative_n13_configuration.py \
  --json artifacts/n13-negative/configuration-strict-rejection.json

test -s artifacts/n13-negative/configuration-strict-rejection.json || {
  echo 'N13 negative-path gate failed: strict configuration receipt was not generated.'
  exit 1
}

echo 'N13 negative-path campaign gate completed.'
