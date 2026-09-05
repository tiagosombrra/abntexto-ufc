# abntexto-ufc v3 — Regression Audit

Updated: 2026-09-05
Status: CLOSED
Baseline SHA: `c4bf51b574647226ee488440579ec2a204c16c79`
Closeout checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`

## Closeout

Regression Audit closed after the shared V3 foundation was rechecked before scientific-article runtime work. The two reviewed PDFs are represented by exactly 34 tracked requirements in `docs/UFC-LIBRARIAN-REVIEW.md`; the correction queue is `docs/V3-CORRECTION-PLAN.md`; Static `33937439818` and full Linux `33937439846` passed at audit closeout.

Initial historical state: **19 PASS / 11 PARTIAL / 1 FAIL / 3 NORMATIVE-REVIEW**.

## Post-audit disposition in Core Corrections

- Object-title authority/runtime correction accepted at `3f47081c...`; item 21 PASS.
- Canonical-reference source/PDF evidence accepted at `c4c59f83...`; items 11, 16 and 28 PASS.
- Engineering-language hardening accepted at `edeb14b7...`; Static `33972111694` and Linux `33972111696`.
- Bounded reference evidence accepted at `bcd851b...`; Static `33974062993`, Linux `33974063103`; items 30-32 PASS.
- Front Matter and Annex Closeout accepted at `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8`; Static `33980847191`, Linux `33980847189`, `PASS=31 FAIL=0 SKIP=0`; explicit reviewer evidence PASS for items 1, 2, 7 and 34.

Current review state is **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence. This is an unresolved authority classification, not a shared runtime failure. Scientific Article remains deferred until Core Corrections and Reference PDF Validation close.

## Core Corrections closeout requirement

Targeted correction evidence is complete for all review items that can be safely closed with current authority. Core Corrections still requires a separate immutable phase-end regression candidate passing Static and full Linux on the same SHA before the phase may close.

## Regression discipline retained after audit

Every **material advance** updates the active execution documentation. Every phase requires a **phase-end regression** on one immutable candidate before closure; targeted correction checks never replace that phase-level regression.
