# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-05  
Status: SHARED CORRECTIONS CLOSED — SCIENTIFIC ARTICLE ACTIVE

## Purpose

This document preserves the executable correction queue produced by Regression Audit, records the closure of shared corrections and the accepted academic-work reference PDF, and identifies the boundary into the active **Scientific Article** phase.

Active article execution is defined in `docs/V3-SCIENTIFIC-ARTICLE.md` and `docs/ARTICLE-NORMATIVE-CONTRACT.md`.

Canonical companions: `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REGRESSION-AUDIT.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/ENGINEERING-LANGUAGE.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`, `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `release/v3-roadmap.json`.

## Execution discipline

Every **material advance** updates the relevant implementation/review state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks and visual review never replace the phase-end regression.

## Shared correction closeout

Core Corrections closed on immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`.

- Static `33982156041`: SUCCESS.
- Full Linux `33982156042`: SUCCESS.
- Linux summary: `PASS=31 FAIL=0 SKIP=0`.
- Librarian review: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Shared runtime FAIL: none.
- Item 33: explicit fail-closed authority gap.

Items 1-32 and 34 are PASS. Item 33 remains `NORMATIVE-REVIEW` and is not an authorization to guess current NBR 6023:2025 behavior.

## Reference PDF Validation closeout

Canonical artifact provenance is accepted from SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, run `33983729996`, artifact `9974546873`, PDF SHA-256 `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`.

The PDF was rendered fully at 200 DPI and all 55 pages were inspected: **55/55 PASS, 0 unexplained visual failures**.

Reference PDF Validation closed on immutable candidate `b64074c64941895f97fbe0f795ce826c798d17ce`:

- Static `33985595790`: SUCCESS.
- Full Linux `33985595798`: SUCCESS.
- Temporary build executor: absent.
- Visual review record: `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`.

No shared runtime/reference correction queue was reopened.

## Active work — Scientific Article

The article phase is not a continuation of the librarian correction queue. It is a bounded new profile built on the corrected shared foundation.

The retained article authority contract contains 18 rules. Current inspection confirms that `abntexto-ufc/core.def` has no `scientific-article` type yet, so article runtime has not been silently pre-implemented by the regression work.

Required execution sequence:

1. add one canonical `scientific-article` profile and only the metadata/public API required by the source-backed contract;
2. add article-specific positive evidence before proof-state promotion;
3. implement required title/authorship/dates/summary presentation and optional foreign-title/foreign-summary routes;
4. reuse current shared citation/reference/section/summary/object machinery for textual content;
5. preserve recommendations as advisory evidence and journal-specific instructions as a conditional boundary;
6. add controlled negative paths for enforceable rules where safe;
7. build and visually inspect a provenance-bound canonical article PDF;
8. synchronize documentation and close the phase only after a Scientific Article phase-end regression on one immutable SHA.

## Remaining authority boundary

Review item 33 remains fail-closed pending authoritative current NBR 6023:2025 text for disputed DOI/availability/repeated-author/corporate-author edge cases. Scientific Article reuses the current shared bibliography contract and must not use article work as a pretext to resolve item 33 speculatively.

## Phase transition gates

Scientific Article -> Final Certification requires article runtime/evidence/rendering accepted, shared non-article foundation still green, item 33 still explicitly classified unless new authority resolves it, synchronized documentation, and one immutable Scientific Article candidate passing Static, full Linux and article-specific acceptance checks.
