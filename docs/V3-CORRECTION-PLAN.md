# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-05
Status: ACTIVE — CORE CORRECTIONS

## Purpose

This is the executable correction queue produced by Regression Audit. It combines the 34 librarian-review requirements, additional regression findings, authority decisions, implementation order and phase gates.

Canonical companions: `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REGRESSION-AUDIT.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/ENGINEERING-LANGUAGE.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `release/v3-roadmap.json`.

## Execution discipline

Every **material advance** updates the relevant implementation/review state and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current batch, or branch/checkpoint facts also update the roadmap and machine state.

Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks are evidence for bounded corrections but never replace the phase-end regression.

## Current evidence state

Object/Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` passed Static `33965794475` and Linux `33965794519`, closing item 21.

Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c` passed Static `33969505681` and full Linux `33969505614`, `PASS=31 FAIL=0 SKIP=0`, closing items 11, 16 and 28.

Engineering-language hardening checkpoint `edeb14b7a96d1cab3ad9551701087ddf4dff059a` passed Static `33972111694` and full Linux `33972111696`. The permanent audit reports zero project-owned Portuguese technical diagnostics, so that additional regression finding is closed.

Current librarian-review state is **28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

## Priority model

- **P0:** contract/control blocker.
- **P1:** normative or canonical-output correctness defect.
- **P2:** reference/documentation defect.
- **P3:** evidence hardening.

## Work order

### 1. Control Plane and Regression Harness — VALIDATED

Readable six-phase model, machine-protected 34-item contract, semantic phase governance, documentation-on-material-advance policy, and mandatory phase-end regression are retained. Static failures during the correction cycle demonstrated that the permanent governance checker rejects documentation drift instead of silently accepting it.

### 2. Front Matter and Institutional Metadata — PARTIAL

Covers items 1-10. Remaining: canonical blank/filled department confirmation, complete-author-name guidance confirmation, final approval-page `Instituição (sigla)` confirmation, and final canonical-PDF front-matter inspection.

### 3. Body Structure, Headings, Citations and Lists — VALIDATED

Items 11-20 and 24-29 have their current automated/source/PDF contracts accepted. Items 11, 16 and 28 closed at `c4c59...` with explicit generated-PDF evidence.

### 4. Figures, Tables and Documentary Objects — VALIDATED

Items 21-23 are PASS. Accepted contract is 12 pt single-spaced upper identification/title, 10 pt single-spaced lower source/legend/note where applicable, all constrained to object width.

### 5. Engineering-language evidence hardening — VALIDATED

Accepted at checkpoint `edeb14b7a96d1cab3ad9551701087ddf4dff059a` with Static `33972111694` and full Linux `33972111696` both green. The stronger detector progressively exposed previously missed project-owned Portuguese diagnostics; all discovered engineering surfaces were corrected instead of weakening the detector. Permanent evidence now reports `portuguese_technical_diagnostics=0`.

### 6. References and NBR 6023:2025 — ACTIVE / FAIL-CLOSED BOUNDARY

Safe bounded work:

- item 30: retain current electronic-resource unknown-publication-data behavior and add reviewer-case regression coverage without strengthening unresolved current-edition semantics;
- item 31: add an explicit thesis/dissertation negative regression preventing duplicate or contradictory year output;
- item 32: add bibliography-specific standard and multivolume fixture/evidence cases using current accepted project/source data;
- item 33: remain `NORMATIVE-REVIEW` until authoritative current NBR 6023:2025 text is available for the disputed DOI/availability/repeated-author/corporate-author edge cases.

Important boundary: `tests/integration/multivolume.sh` validates pagination of a multivolume academic document; it is not evidence for a multivolume bibliographic entry. Bibliography evidence must use a separate fixture/reference gate.

Acceptance for this batch:

1. no normative runtime change unless directly supported by current authority already in the evidence corpus;
2. add positive/negative reviewer-specific evidence where bounded behavior is already established;
3. keep item 33 untouched;
4. synchronize affected execution documentation in the same material advance;
5. require Static contract and full Linux integration green before accepting the batch.

### 7. Appendices, Annexes and External Source Attribution — PARTIAL

Automated heading/pagination behavior is green and the canonical annex source example exists. Final closure requires canonical-PDF confirmation of source attribution, heading and TOC presentation.

### 8. Canonical V3 Reference Corpus Cleanup — VALIDATED/PROTECTED

Keep rejecting stale V2 wording, retired profile/API vocabulary, obsolete placeholders, implementation-history prose presented as current user instruction, reviewed legacy object-title casing, malformed UFC first-use, and legacy heading/`etc.` forms.

## Complete 34-item implementation matrix

| # | State | Priority | Remaining action / acceptance |
|---:|---|---|---|
| 1 | PARTIAL | P2 | Canonical blank/filled department confirmation. |
| 2 | PARTIAL | P2 | Canonical complete-name guidance confirmation. |
| 3 | PASS | P3 | Preserve subtitle propagation regression. |
| 4 | PASS | P1 | Preserve advisor/co-advisor punctuation regression. |
| 5 | PASS | P3 | Preserve conditional co-advisor rendering. |
| 6 | PASS | P3 | Preserve concentration behavior. |
| 7 | PARTIAL | P2 | Final canonical `Instituição (sigla)` approval-page confirmation. |
| 8 | PASS | P3 | Preserve variable committee size. |
| 9 | PASS | P3 | Preserve CAPES guidance. |
| 10 | PASS | P3 | Reconfirm in corrected canonical PDF. |
| 11 | PASS | P2 | Source/PDF evidence accepted at `3ae9dd...` / `c4c59...`. |
| 12 | PASS | P3 | Preserve 3 cm list alignment. |
| 13 | PASS | P3 | Preserve pre-textual TOC exclusion. |
| 14 | PASS | P3 | Preserve direct appendix/annex flow. |
| 15 | PASS | P3 | Final visual TOC confirmation remains a presentation-phase check. |
| 16 | PASS | P2 | Source/PDF first-use evidence accepted. |
| 17 | PASS | P1/P3 | Preserve code/body typography regression. |
| 18 | PASS | P3 | Preserve current NBR 10520 capitalization. |
| 19 | PASS | P1 | Preserve long-quotation locator fixture. |
| 20 | PASS | P1 | Preserve punctuation positive/negative reviewer gate. |
| 21 | PASS | P1 | Preserve 12 pt upper / 10 pt lower final-PDF and IBGE evidence. |
| 22 | PASS | P3 | Preserve object single spacing. |
| 23 | PASS | P1 | Preserve external-source locator evidence. |
| 24 | PASS | P3 | Preserve lowercase alínea starts. |
| 25 | PASS | P3 | Preserve intermediate/final punctuation. |
| 26 | PASS | P3 | Preserve colon/subalínea punctuation. |
| 27 | PASS | P3 | Preserve alphabetic alínea ordering. |
| 28 | PASS | P2 | Source/PDF sentence-case and `etc.` evidence accepted. |
| 29 | PASS | P3 | Preserve 2 cm first-line indent/no extra paragraph spacing. |
| 30 | PASS/PARTIAL | P1/P3 | Add reviewer-specific electronic-resource regression while preserving current bounded behavior. |
| 31 | PASS | P3 | Add duplicate/contradictory-year negative fixture. |
| 32 | PARTIAL | P1/P2 | Add bibliography-specific standard/multivolume cases. |
| 33 | NORMATIVE-REVIEW | P1 | Wait for authoritative NBR 6023:2025 edge-case text. |
| 34 | PARTIAL | P1/P2 | Final canonical annex source/heading/TOC confirmation. |

## Additional regression findings

| Finding | State | Next action |
|---|---|---|
| Hidden historical phase-name coupling | CLOSED | Keep semantic phase governance regression. |
| Documentation can drift from implementation | ACTIVE GUARD | Preserve mandatory reconciliation on every material advance. |
| Phase closure can rely on targeted tests only | CLOSED/POLICY | Require phase-end regression on one SHA. |
| Stale V2 wording/current API vocabulary in V3 reference | CORRECTED/PROTECTED | Keep negative reference hygiene. |
| Object typography tests certified wrong upper-title size | CLOSED | Preserve current authority decision/evidence. |
| Reviewed reference-content requirements lacked source/PDF guards | CLOSED | Preserve `3ae9dd...` + `c4c59...` evidence. |
| Engineering-language gate had mixed-diagnostic false negatives | CLOSED | Accepted at `edeb14...`; retain permanent stronger detector and self-tests. |

## Phase transition gates

Core Corrections -> Reference PDF Validation requires all blocking shared P0/P1 corrections implemented, affected normative mappings/tests updated atomically, executable checks green, no shared runtime FAIL, authority gaps explicit/fail-closed, documentation synchronized, and one immutable Core Corrections candidate passing Static plus full Linux.

Reference PDF Validation -> Scientific Article additionally requires the corrected canonical V3 PDF to pass page-level review and reproducible presentation evidence.
