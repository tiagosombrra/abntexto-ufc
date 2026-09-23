#!/bin/sh
set -eu

python3 -m py_compile tests/checks/governance/reference_guide_contract.py
python3 tests/checks/governance/reference_guide_contract.py

echo 'Reference guide traceability contract validated.'
