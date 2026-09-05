# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-05
Status: ACTIVE — CORE CORRECTIONS PHASE-END REGRESSION

## Purpose

This is the executable correction queue produced by Regression Audit. It combines the 34 librarian-review requirements, additional regression findings, authority decisions, implementation order and phase gates.

Canonical companions: `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REGRESSION-AUDIT.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/ENGINEERING-LANGUAGE.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `release/v3-roadmap.json`.

## Execution discipline

Every **material advance** updates the relevant implementation/review state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks are evidence for bounded corrections but never replace the phase-end regression.

## Current evidence state

Front Matter and Annex Closeout checkpoint `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8` passed Static `33980847191` and full Linux `33980847189`, `PASS=31 FAIL=0 SKIP=0`. Current librarian-review state is **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

## Work status

All correction batches that can be safely resolved with current authority are validated. Items 1-32 and 34 are PASS; item 33 is NORMATIVE-REVIEW. No PARTIAL or FAIL item remains.

## Phase-end candidate history

Candidate `3b2476371e1df5180d8ee25ea53aed6a13fa2da2` is rejected because Static `33981960024` correctly enforced the machine invariant `phase_end_regression.candidate = one-immutable-sha`. The candidate had replaced that sentinel with descriptive text. No runtime or review-evidence failure was observed by Static before the governance stop.

The fix restores the exact governance invariant; `tests/checks/phase_governance.py` remains unchanged.

## Current batch — corrected Core Corrections phase-end candidate

`docs/V3-CORE-CORRECTIONS-PHASE-END.md` defines the corrected immutable-candidate semantics. The commit that first contains the corrected synchronized state is the new candidate. Its SHA is recorded later with CI results; the candidate is not modified after publication.

The candidate must pass Static contract, full Linux integration and the existing phase-specific evidence matrix on the same SHA. No phase transition occurs until those results are recorded.

## Phase transition gates

Core Corrections -> Reference PDF Validation requires no shared runtime FAIL, all blocking correction evidence accepted, item 33 explicit/fail-closed, documentation synchronized, and one immutable Core Corrections candidate passing Static plus full Linux and phase-specific acceptance checks.

Reference PDF Validation -> Scientific Article additionally requires the corrected canonical V3 PDF to pass page-level visual review and reproducible presentation evidence.
