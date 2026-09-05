# abntexto-ufc v3 — Regression Audit

Updated: 2026-09-05
Status: CLOSED
Baseline SHA: `c4bf51b574647226ee488440579ec2a204c16c79`
Closeout checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`

## Closeout

Regression Audit closed after the shared V3 foundation was rechecked before scientific-article runtime work. The two reviewed PDFs are represented by exactly 34 tracked requirements; the correction queue and readable phase model were established; Static `33937439818` and full Linux `33937439846` passed; scientific-article runtime had not started before the reset.

The project therefore advanced to **Core Corrections**. This historical closeout does not imply that the 34 review items were already corrected.

## Initial 34-item baseline

- `PASS`: 19
- `PARTIAL`: 11
- `FAIL`: 1
- `NORMATIVE-REVIEW`: 3

These counts are historical Regression Audit facts.

## Post-audit disposition in Core Corrections

Object-title typography was resolved and accepted at checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`, with Static `33965794475` and full Linux `33965794519` green. Review item 21 is PASS under the accepted 12 pt upper identification/title and reduced 10 pt lower source/legend/note split.

Canonical-reference source and PDF evidence subsequently closed items 11, 16 and 28. Generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c` passed Static `33969505681` and full Linux `33969505614`, with Linux summary `PASS=31 FAIL=0 SKIP=0` and explicit canonical-PDF evidence for those three items.

Current review state in Core Corrections is **28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

The engineering-language false-negative finding remains active. Initial hardening implementation `5d74c0c5b85ec501b04c5050af81180ad7e3f2ee` was synchronized at `fd3727d89848eb52a9c79021cd9765ad9e1806db`. Static `33970711005` then failed because the stronger detector exposed another project-owned Portuguese diagnostic in `tests/integration/algorithm-numbering.sh`. This validated the fail-closed strategy rather than invalidating it.

Correction implementation `5c5b9593cd12f3b6fa3108b579514c3c25edcb54` translates all diagnostics in the newly exposed algorithm-numbering gate and extends detector/self-test coverage for the discovered line-numbering phrase family. The finding remains open until a synchronized Static/full Linux acceptance run is green. Any further exposed project-owned diagnostic must be corrected rather than hidden by weakening detection.

Item 33 remains fail-closed because current authoritative NBR 6023:2025 text for the disputed edge cases is not available in the evidence corpus.

Scientific Article remains deferred until Core Corrections and Reference PDF Validation close.
