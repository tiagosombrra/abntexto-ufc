# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-05
Status: ACTIVE — CORE CORRECTIONS PHASE-END REGRESSION

## Purpose

This is the executable correction queue produced by Regression Audit. It combines the 34 librarian-review requirements, additional regression findings, authority decisions, implementation order and phase gates.

Canonical companions: `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REGRESSION-AUDIT.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/ENGINEERING-LANGUAGE.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `release/v3-roadmap.json`.

## Execution discipline

Every **material advance** updates the relevant implementation/review state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks are evidence for bounded corrections but never replace the phase-end regression.

## Current evidence state

Front Matter and Annex Closeout checkpoint `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8` passed Static `33980847191` and full Linux `33980847189`, `PASS=31 FAIL=0 SKIP=0`. Explicit reviewer evidence passed for items 1, 2, 7 and 34.

Current librarian-review state is **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Acceptance-state synchronization checkpoint: `c066697691df748a3b24a716ba69d5e4cb168f5d`.

## Work status

All correction batches that can be safely resolved with current authority are validated:

- Control Plane and Regression Harness — VALIDATED;
- Front Matter and Institutional Metadata — VALIDATED;
- Body Structure, Headings, Citations and Lists — VALIDATED;
- Figures, Tables and Documentary Objects — VALIDATED;
- Engineering-language evidence hardening — VALIDATED/PERMANENT GUARD;
- References items 30-32 — VALIDATED;
- Appendices, Annexes and External Source Attribution — VALIDATED;
- Canonical V3 Reference Corpus Cleanup — VALIDATED/PROTECTED.

Item 33 remains `NORMATIVE-REVIEW`, not a runtime FAIL.

## Complete 34-item implementation state

Items 1-32 and 34 are PASS. Item 33 is NORMATIVE-REVIEW. No PARTIAL or FAIL item remains.

## Current batch — Core Corrections phase-end regression

`docs/V3-CORE-CORRECTIONS-PHASE-END.md` defines the immutable candidate semantics and acceptance gate. The commit that first introduces that synchronized document is the candidate.

The candidate must pass Static contract, full Linux integration and the existing phase-specific evidence matrix on the same SHA. No phase transition occurs until the candidate result is recorded.

## Phase transition gates

Core Corrections -> Reference PDF Validation requires no shared runtime FAIL, all blocking correction evidence accepted, item 33 explicit/fail-closed, documentation synchronized, and one immutable Core Corrections candidate passing Static plus full Linux and phase-specific acceptance checks.

Reference PDF Validation -> Scientific Article additionally requires the corrected canonical V3 PDF to pass page-level visual review and reproducible presentation evidence.
