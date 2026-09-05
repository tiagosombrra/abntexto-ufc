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
- Engineering-language hardening accepted at `edeb14b7...`; Static `33972111694` and Linux `33972111696`, permanent diagnostics audit zero.
- Bounded reference evidence accepted at `bcd851b...`; Static `33974062993`, Linux `33974063103`; items 30, 31 and 32 reviewer-specific evidence PASS and item 32 closed.

Current review state is **29 PASS / 4 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

Front Matter and Annex Closeout implementation `33bdd0bd5f9360c645b4166071c32dbba6c647f0` adds evidence for the four remaining PARTIAL items 1, 2, 7 and 34. Synchronized checkpoint `48e7e6841b63ea62d6811e734dde09931b8f608c` failed Static `33980486317` because the newly added item-2 failure diagnostic contained the prohibited project-owned technical term `pre-textual`. This is a guardrail discovery, not a runtime/review contradiction. Correction `dc381d4517341062d53ae5e93082c7856fc4af17` changes only that diagnostic wording; corrected synchronized CI remains pending.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence. Scientific Article remains deferred until Core Corrections and Reference PDF Validation close.

## Regression discipline retained after audit

Every **material advance** updates the active execution documentation. Every phase requires a **phase-end regression** on one immutable candidate before closure; targeted correction checks never replace that phase-level regression.
