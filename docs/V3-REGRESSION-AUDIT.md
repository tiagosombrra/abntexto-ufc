# abntexto-ufc v3 — Regression Audit

Updated: 2026-09-05
Status: CLOSED
Baseline SHA: `c4bf51b574647226ee488440579ec2a204c16c79`
Closeout checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`

## Closeout

Regression Audit closed after the shared V3 foundation was rechecked before scientific-article runtime work. The two reviewed PDFs are represented by exactly 34 tracked requirements in `docs/UFC-LIBRARIAN-REVIEW.md`; the correction queue is `docs/V3-CORRECTION-PLAN.md`; Static `33937439818` and full Linux `33937439846` passed at audit closeout.

Initial historical state: **19 PASS / 11 PARTIAL / 1 FAIL / 3 NORMATIVE-REVIEW**.

## Post-audit disposition

The audit findings were resolved through the readable downstream phases rather than by reopening the audit itself.

### Core Corrections

- Object-title authority/runtime correction accepted; item 21 PASS.
- Canonical-reference source/PDF evidence accepted; items 11, 16 and 28 PASS.
- Engineering-language hardening accepted; Static `33972111694` and Linux `33972111696`.
- Bounded reference evidence accepted; items 30-32 PASS.
- Front Matter and Annex Closeout accepted at `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8`; items 1, 2, 7 and 34 gained explicit reviewer evidence.
- Core Corrections phase-end candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da` passed Static `33982156041` and Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.

Core Corrections is CLOSED.

### Reference PDF Validation

- Fresh canonical PDF built from SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, run `33983729996`, artifact `9974546873`.
- Canonical PDF: 55 A4 pages, PDF 1.7, TeX Live 2026/pdfLaTeX, fonts embedded, preflight PASS.
- Complete 200 DPI visual review: **55/55 PASS, 0 unexplained visual failures**.
- Phase-end candidate `b64074c64941895f97fbe0f795ce826c798d17ce` passed Static `33985595790` and Linux `33985595798`.

Reference PDF Validation is CLOSED.

## Current review state

The consolidated librarian-review state is **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence. This is an unresolved authority classification, not a shared runtime or visual failure.

The accepted shared foundation now permits the **Scientific Article** phase to proceed from a clean, regression-tested base. Historical article source-contract work remains evidence only; article runtime must be implemented against the current architecture and current readable roadmap.

## Regression discipline retained after audit

Every **material advance** updates the active execution documentation. Every phase requires a **phase-end regression** on one immutable candidate before closure; targeted checks never replace that phase-level regression.
