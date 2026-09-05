# abntexto-ufc v3 — Regression Audit

Updated: 2026-09-05
Status: CLOSED
Baseline SHA: `c4bf51b574647226ee488440579ec2a204c16c79`
Closeout checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`

## Closeout

Regression Audit closed after the shared V3 foundation was rechecked before scientific-article runtime work.

Evidence at closeout: the two reviewed PDFs are represented by exactly 34 tracked requirements in `docs/UFC-LIBRARIAN-REVIEW.md`; `docs/V3-CORRECTION-PLAN.md` contains the executable correction queue; the active roadmap uses readable phase names; object typography and selected NBR 6023:2025 disputes had explicit unresolved authority status at audit closeout; Static `33937439818` passed; full Linux `33937439846` passed; scientific-article runtime had not started before the regression reset.

The project therefore advanced to **Core Corrections**. This closeout does not mean the 34 review items were already corrected.

## Initial 34-item baseline

- `PASS`: 19
- `PARTIAL`: 11
- `FAIL`: 1
- `NORMATIVE-REVIEW`: 3

These are historical audit closeout facts.

## Post-audit disposition in Core Corrections

The object-title authority conflict is resolved and accepted. Checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` passed Static `33965794475` and full Linux `33965794519`; review item 21 is PASS.

Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c` passed Static `33969505681` and full Linux `33969505614`, closing review items 11, 16 and 28. Current librarian-review state is therefore **28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

The engineering-language false-negative finding is being exercised fail-closed. Successive Static runs exposed `algorithm-numbering.sh`, a temporary documentation-governance drift, catalog-card/duplex/vector diagnostic surfaces, and most recently five technical diagnostics in `tests/integration/backmatter.sh` at synchronized checkpoint `0818bc2c5f50f6f1c60d4cef98d1c85031cb2fcd` / Static `33971849196`.

Current implementation `a1c139a6efa8bacefcd3294f01b1f7ed3447a8dd` translates the complete back-matter engineering diagnostic surface and normalizes its technical job identifier while preserving academic Portuguese literals. This hardening is not accepted until a synchronized Static/full Linux checkpoint is green.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence. Scientific Article remains deferred until Core Corrections and Reference PDF Validation close.
