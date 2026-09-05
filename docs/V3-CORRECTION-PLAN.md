# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-05
Status: ACTIVE — CORE CORRECTIONS CLOSEOUT

## Purpose

This is the executable correction queue produced by Regression Audit. It combines the 34 librarian-review requirements, additional regression findings, authority decisions, implementation order and phase gates.

Canonical companions: `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REGRESSION-AUDIT.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/ENGINEERING-LANGUAGE.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `release/v3-roadmap.json`.

## Execution discipline

Every **material advance** updates the relevant implementation/review state and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current batch, or branch/checkpoint facts also update the roadmap and machine state.

Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks are evidence for bounded corrections but never replace the phase-end regression.

## Current evidence state

Accepted checkpoints include object typography `3f47081c...`, canonical reference content `c4c59f83...`, engineering-language hardening `edeb14b7...`, and bounded references `bcd851b...`.

Front Matter and Annex Closeout checkpoint `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8` passed Static `33980847191` and full Linux `33980847189`, `PASS=31 FAIL=0 SKIP=0`. Explicit reviewer evidence passed for items 1, 2, 7 and 34.

Current librarian-review state is **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence for disputed edge cases.

## Priority model

- **P0:** contract/control blocker.
- **P1:** normative or canonical-output correctness defect.
- **P2:** reference/documentation defect.
- **P3:** evidence hardening.

## Work order

### 1. Control Plane and Regression Harness — VALIDATED

Readable six-phase model, machine-protected 34-item contract, semantic phase governance, documentation-on-material-advance policy, and mandatory phase-end regression are retained.

### 2. Front Matter and Institutional Metadata — VALIDATED

Items 1-10 are PASS. Items 1, 2 and 7 received explicit generated-output evidence in Linux `33980847189`; existing evidence for items 3-6 and 8-10 remains green.

### 3. Body Structure, Headings, Citations and Lists — VALIDATED

Items 11-20 and 24-29 retain accepted automated/source/PDF contracts.

### 4. Figures, Tables and Documentary Objects — VALIDATED

Items 21-23 are PASS. Accepted contract is 12 pt single-spaced upper identification/title and 10 pt single-spaced lower source/legend/note where applicable.

### 5. Engineering-language evidence hardening — VALIDATED/PERMANENT GUARD

Accepted at `edeb14...`. Historical Static `33980486317` is retained as evidence that the permanent guard rejects newly introduced project-owned Portuguese technical diagnostics. Correction `dc381d45...` changed only diagnostic wording.

### 6. References and NBR 6023:2025 — VALIDATED BOUNDED BATCH / ONE AUTHORITY GAP

Items 30-32 are PASS. Item 33 remains `NORMATIVE-REVIEW`; no disputed DOI/availability/repeated-author/corporate-author runtime change is authorized without current authoritative text.

### 7. Appendices, Annexes and External Source Attribution — VALIDATED

Item 34 is PASS. Canonical source attribution, heading presence and TOC entry are combined with independent final-PDF evidence proving uppercase/bold/12 pt/centered annex headings.

### 8. Canonical V3 Reference Corpus Cleanup — VALIDATED/PROTECTED

Keep rejecting stale V2 wording, retired profile/API vocabulary, obsolete placeholders, reviewed legacy title casing, malformed UFC first-use and legacy heading/`etc.` forms.

## Complete 34-item implementation matrix

| # | State | Priority | Remaining action / acceptance |
|---:|---|---|---|
| 1 | PASS | P2 | Preserve blank/filled department evidence. |
| 2 | PASS | P2 | Preserve complete-name canonical output evidence. |
| 3 | PASS | P3 | Preserve subtitle propagation. |
| 4 | PASS | P1 | Preserve advisor/co-advisor punctuation. |
| 5 | PASS | P3 | Preserve conditional co-advisor rendering. |
| 6 | PASS | P3 | Preserve concentration behavior. |
| 7 | PASS | P2 | Preserve approval-page institution/acronym evidence. |
| 8 | PASS | P3 | Preserve variable committee size. |
| 9 | PASS | P3 | Preserve CAPES guidance. |
| 10 | PASS | P3 | Reconfirm visually during Reference PDF Validation. |
| 11 | PASS | P2 | Preserve sentence-case source/PDF evidence. |
| 12 | PASS | P3 | Preserve 3 cm list alignment. |
| 13 | PASS | P3 | Preserve front-matter TOC exclusion. |
| 14 | PASS | P3 | Preserve direct appendix/annex flow. |
| 15 | PASS | P3 | Reconfirm visually during Reference PDF Validation. |
| 16 | PASS | P2 | Preserve source/PDF first-use evidence. |
| 17 | PASS | P1/P3 | Preserve code/body typography regression. |
| 18 | PASS | P3 | Preserve current NBR 10520 capitalization. |
| 19 | PASS | P1 | Preserve long-quotation locator. |
| 20 | PASS | P1 | Preserve punctuation positive/negative gate. |
| 21 | PASS | P1 | Preserve 12 pt upper / 10 pt lower object evidence. |
| 22 | PASS | P3 | Preserve object single spacing. |
| 23 | PASS | P1 | Preserve external-source locator evidence. |
| 24 | PASS | P3 | Preserve lowercase alínea starts. |
| 25 | PASS | P3 | Preserve intermediate/final punctuation. |
| 26 | PASS | P3 | Preserve colon/subalínea punctuation. |
| 27 | PASS | P3 | Preserve alphabetic alínea ordering. |
| 28 | PASS | P2 | Preserve sentence-case and `etc.` evidence. |
| 29 | PASS | P3 | Preserve body paragraph indentation/spacing. |
| 30 | PASS | P1/P3 | Preserve reviewer-specific electronic evidence. |
| 31 | PASS | P3 | Preserve single-year thesis/dissertation evidence. |
| 32 | PASS | P1/P2 | Preserve standard/multivolume evidence. |
| 33 | NORMATIVE-REVIEW | P1 | Wait for authoritative NBR 6023:2025 edge-case text; remain fail-closed. |
| 34 | PASS | P1/P2 | Preserve canonical annex source/heading/TOC and final-PDF heading evidence. |

## Additional regression findings

| Finding | State | Next action |
|---|---|---|
| Hidden historical phase-name coupling | CLOSED | Keep semantic phase governance. |
| Documentation can drift from implementation | ACTIVE GUARD | Keep mandatory reconciliation on every material advance. |
| Phase closure can rely on targeted tests only | CLOSED/POLICY | Require phase-end regression on one SHA. |
| Stale V2/current API wording | CORRECTED/PROTECTED | Keep negative reference hygiene. |
| Object typography test encoded wrong upper size | CLOSED | Preserve accepted authority/evidence. |
| Engineering-language false negatives | CLOSED/PERMANENT GUARD | Keep stronger detector. |
| Closeout diagnostic used prohibited engineering wording | CLOSED | `dc381d45...`; Static `33980847191` and Linux `33980847189` green afterward. |

## Current batch — Core Corrections phase-end regression preparation

All correction items that can be closed with current authority are accepted. The next action is to create a **separate immutable Core Corrections phase-end regression candidate** with synchronized control documentation and no speculative item-33 runtime change.

The candidate must pass Static contract, full Linux integration and the existing phase-specific evidence matrix on the same SHA. A green targeted closeout alone does not close Core Corrections.

## Phase transition gates

Core Corrections -> Reference PDF Validation requires no shared runtime FAIL, all blocking shared correction evidence accepted, item 33 explicit/fail-closed, documentation synchronized, and one immutable Core Corrections candidate passing Static plus full Linux and phase-specific acceptance checks.

Reference PDF Validation -> Scientific Article additionally requires the corrected canonical V3 PDF to pass page-level visual review and reproducible presentation evidence.
