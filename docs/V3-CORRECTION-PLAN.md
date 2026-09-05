# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-05  
Status: CORE CORRECTIONS CLOSED — REFERENCE PDF VALIDATION PHASE-END GATE

## Purpose

This document preserves the executable correction queue produced by Regression Audit and records its closure state. Active presentation validation is defined in `docs/V3-REFERENCE-PDF-VALIDATION.md` and `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`.

Canonical companions: `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REGRESSION-AUDIT.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/ENGINEERING-LANGUAGE.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `release/v3-roadmap.json`.

## Execution discipline

Every **material advance** updates the relevant implementation/review state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks and visual review never replace the phase-end regression.

## Core Corrections final state

Core Corrections closed on immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`.

- Static `33982156041`: SUCCESS.
- Full Linux `33982156042`: SUCCESS.
- Linux summary: `PASS=31 FAIL=0 SKIP=0`.
- Librarian review: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Shared runtime FAIL: none.
- Item 33: explicit fail-closed authority gap.

Items 1-32 and 34 are PASS; item 33 remains NORMATIVE-REVIEW.

## Reference PDF Validation state

Canonical artifact provenance is accepted from SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, run `33983729996`, artifact `9974546873`, PDF SHA-256 `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`.

The PDF was rendered fully at 200 DPI and all 55 pages were inspected. Result: **PASS, 0 unexplained visual failures**. No runtime/reference correction queue was reopened.

The reference-source fallback boxes for optional licensed photographs are intentional when `make reference-assets` has not been run and do not constitute a missing-artifact defect in the normal canonical build.

## Current batch — Reference PDF Validation phase-end candidate

The final synchronized state that includes accepted provenance and `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md` is frozen as one immutable candidate. Its exact SHA is recorded after Git creation and, if Static/full Linux are green, is written into the later phase-transition evidence.

Required gate:

1. Static contract;
2. full Linux integration;
3. no regression of the 34-item evidence state;
4. canonical PDF provenance remains bound and visual-review result remains PASS;
5. temporary executor remains absent.

## Remaining authority boundary

Review item 33 remains fail-closed pending authoritative current NBR 6023:2025 text for the disputed DOI/availability/repeated-author/corporate-author cases. Visual observation does not promote those edge cases into normative runtime requirements.

## Phase transition gates

Reference PDF Validation -> Scientific Article requires accepted artifact provenance, complete 55-page visual PASS, synchronized documentation, and one immutable Reference PDF Validation phase-end candidate passing Static plus full Linux.

Scientific Article remains blocked until that result is recorded.
