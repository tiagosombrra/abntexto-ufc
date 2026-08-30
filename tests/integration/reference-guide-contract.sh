#!/bin/sh
set -eu

python3 -m py_compile tests/checks/reference_guide_contract.py
python3 tests/checks/reference_guide_contract.py

echo 'Reference guide traceability contract validated.'
