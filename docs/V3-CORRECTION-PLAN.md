# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-07  
Status: SHARED CORRECTIONS AND SCIENTIFIC ARTICLE CLOSED — FINAL CERTIFICATION ACTIVE

## Purpose

This document preserves the correction history produced by Regression Audit and the phase boundaries built on that corrected foundation. Active certification execution is defined in `docs/V3-FINAL-CERTIFICATION.md`.

## Execution discipline

Every **material advance** updates the relevant implementation/review/certification state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks and visual review never replace that gate.

## Accepted shared foundation

Core Corrections closed on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Reference PDF Validation closed on `b64074c64941895f97fbe0f795ce826c798d17ce` with 55/55 page-level visual PASS.

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Items 1–32 and 34 are PASS. Item 33 remains a fail-closed current-authority gap.

## Scientific Article closeout

Scientific Article closed on immutable candidate `923d11ef668b02ec4de3cad4906ad5ac1f527eaf`: Static `34154045481`, complete Linux `34154045509`, `PASS=36 FAIL=0 SKIP=0`, and canonical article PDF 5/5 visual PASS. PR #286 is merged into main as `22e3c19235fa5245505b92d919a09d31eb2bfecb`.

## Active work — Final Certification

Active branch `cert/v3-final-certification` was created from exact canonical main `22e3c192...`.

Execution sequence:

1. validate branch/main entry synchronization and establish the existing Linux release baseline;
2. certify supported profiles and required engines;
3. certify literal Times New Roman/Arial identities, Unicode extraction and embedding where applicable;
4. certify PDF/A-2b;
5. certify public/distribution bundles;
6. resolve issue #18 with deterministic release-reference-PDF rebuild/hash evidence;
7. close Final Certification only after one immutable candidate passes its complete phase-end regression.

Certification and reproducibility work do not authorize speculative normative changes.

## Remaining authority boundary

Review item 33 remains fail-closed pending authoritative current NBR 6023:2025 text for disputed edge cases.

## Phase transition gate

Final Certification -> Release requires the complete certification matrix, issue #18 acceptance, synchronized documentation and one immutable Final Certification candidate passing Static, complete Linux, release/certification evidence and all applicable phase-specific checks.
