# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-07  
Status: SHARED CORRECTIONS AND SCIENTIFIC ARTICLE CLOSED — FINAL CERTIFICATION ACTIVE

## Purpose

This document preserves the correction history produced by Regression Audit and the phase boundaries built on that corrected foundation. Active certification execution is now defined in `docs/V3-FINAL-CERTIFICATION.md`.

## Execution discipline

Every **material advance** updates the relevant implementation/review/certification state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks and visual review never replace that gate.

## Closed shared work

Core Corrections closed on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, full Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.

Reference PDF Validation closed on `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790`, Linux `33985595798`, complete 55-page visual PASS.

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Items 1–32 and 34 are PASS. Item 33 remains a fail-closed current-authority gap.

## Scientific Article closeout

Scientific Article closed on immutable candidate `923d11ef668b02ec4de3cad4906ad5ac1f527eaf`:

- Static `34154045481`: SUCCESS;
- Linux `34154045509`: SUCCESS;
- scope: `complete`;
- summary: `PASS=36 FAIL=0 SKIP=0`;
- canonical article PDF: provenance-bound build `f62ac703...`, 5/5 visual PASS;
- temporary PDF-build executor: absent from accepted candidate;
- 18-rule source contract preserved without recommendation/journal-modality strengthening.

The same immutable checkpoint satisfied Step 7 cleanup and Step 8 phase-end requirements. Detailed record: `docs/V3-SCIENTIFIC-ARTICLE-PHASE-END.md`.

## Active work — Final Certification

Final Certification is proof/certification/reproducibility work over the accepted V3 runtime. It does not authorize reopening normative behavior without a real defect or new authority.

Execution sequence:

1. merge PR #286 and create `cert/v3-final-certification` from updated main;
2. run Linux release baseline;
3. certify supported profiles and required engines;
4. certify literal Times New Roman/Arial identities, Unicode extraction and embedding where applicable;
5. certify PDF/A-2b;
6. certify public/distribution bundles;
7. resolve issue #18 with deterministic release-reference-PDF rebuild/hash evidence;
8. close Final Certification only after one immutable candidate passes its complete phase-end regression.

## Remaining authority boundary

Review item 33 remains fail-closed pending authoritative current NBR 6023:2025 text for disputed edge cases. Certification and reproducibility work must not be used to resolve it speculatively.

## Phase transition gate

Final Certification -> Release requires the complete certification matrix, issue #18 acceptance, synchronized documentation and one immutable Final Certification candidate passing Static, complete Linux, release/certification evidence and all applicable phase-specific checks.
