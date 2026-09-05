# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-05
Status: CORE CORRECTIONS CLOSED — REFERENCE PDF VALIDATION ACTIVE

## Purpose

This document preserves the executable correction queue produced by Regression Audit and records its closure state. The active presentation-validation work is defined in `docs/V3-REFERENCE-PDF-VALIDATION.md`.

Canonical companions: `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REGRESSION-AUDIT.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/ENGINEERING-LANGUAGE.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `release/v3-roadmap.json`.

## Execution discipline

Every **material advance** updates the relevant implementation/review state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks and visual spot checks never replace the phase-end regression.

## Core Corrections final state

Core Corrections closed on immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`.

- Static `33982156041`: SUCCESS.
- Full Linux `33982156042`: SUCCESS.
- Linux summary: `PASS=31 FAIL=0 SKIP=0`.
- Librarian review: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Shared runtime FAIL: none.
- Item 33: explicit fail-closed authority gap.

All correction batches that can be safely resolved with current authority are validated. Items 1-32 and 34 are PASS; item 33 remains NORMATIVE-REVIEW.

## Phase-end candidate history

Candidate `3b2476371e1df5180d8ee25ea53aed6a13fa2da2` was rejected because Static `33981960024` correctly enforced `phase_end_regression.candidate = one-immutable-sha`. The governance test was not weakened.

Corrected candidate `5f67560a...` restored the exact invariant and passed both required workflows on the same immutable SHA. The phase closure record is `docs/V3-CORE-CORRECTIONS-PHASE-END.md`.

## Active work — Reference PDF Validation

The correction queue is not reopened merely to perform visual inspection. The active phase validates the canonical rendered artifact against the accepted shared foundation.

If visual inspection exposes a real defect, add a classified correction entry before changing runtime/reference content, then rebuild, re-render and revalidate. A presentation defect discovered here keeps Reference PDF Validation open; it does not authorize Scientific Article work.

The canonical PDF must be a real LaTeX build tied to a concrete Git SHA. Older PDFs are comparison-only when later changes can affect output. Synthetic PDFs are never acceptance evidence.

## Remaining authority boundary

Review item 33 remains fail-closed pending authoritative current NBR 6023:2025 text for the disputed DOI/availability/repeated-author/corporate-author cases. Observing the current rendered output in the PDF phase does not promote those edge cases into normative runtime requirements.

## Phase transition gates

Reference PDF Validation -> Scientific Article requires accepted artifact provenance, complete page-level visual review with no unexplained FAIL, reproducible presentation evidence, synchronized documentation, and one immutable Reference PDF Validation phase-end candidate passing Static plus full Linux.
