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

Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c` passed Static `33969505681` and full Linux `33969505614`, `PASS=31 FAIL=0 SKIP=0`, closing items 11, 16 and 28. Current librarian-review state is **28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

Engineering-language checkpoint `fd3727d89848eb52a9c79021cd9765ad9e1806db` failed Static `33970711005` after the stronger detector exposed another project-owned Portuguese diagnostic in `tests/integration/algorithm-numbering.sh`. Correction `5c5b9593cd12f3b6fa3108b579514c3c25edcb54` translates that gate's complete diagnostic surface and expands detector/self-test coverage.

The first synchronized correction checkpoint `6c23a49a86944d646db35b56af877d3bb351c0ec` then failed Static `33970988780` because a documentation rewrite had omitted the required `material advance` governance concept from the roadmap. The phase-governance checker stops at the first missing document concept, so this correction restores both required concepts (`material advance` and `phase-end regression`) in this correction plan and the roadmap before rerun.

## Priority model

- **P0:** contract/control blocker.
- **P1:** normative or canonical-output correctness defect.
- **P2:** reference/documentation defect.
- **P3:** evidence hardening.

## Work order

### 1. Control Plane and Regression Harness — VALIDATED / GOVERNANCE DRIFT CORRECTED

Readable six-phase model, machine-protected 34-item contract, semantic phase governance, documentation-on-material-advance policy, and mandatory phase-end regression are retained. Static `33970988780` demonstrated that the permanent governance checker correctly rejects documentation rewrites that drop those contracts; the missing language is restored before further feature work.

### 2. Front Matter and Institutional Metadata — PARTIAL

Covers items 1-10. Remaining: canonical blank/filled department confirmation, complete-author-name guidance confirmation, final approval-page `Instituição (sigla)` confirmation, and final canonical-PDF front-matter inspection.

### 3. Body Structure, Headings, Citations and Lists — VALIDATED

Items 11-20 and 24-29 have their current automated/source/PDF contracts accepted. Items 11, 16 and 28 closed at `c4c59...` with explicit generated-PDF evidence.

### 4. Figures, Tables and Documentary Objects — VALIDATED

Items 21-23 are PASS. Accepted contract is 12 pt single-spaced upper identification/title, 10 pt single-spaced lower source/legend/note where applicable, all constrained to object width.

### 5. Engineering-language evidence hardening — ACTIVE

Initial implementation `5d74c0c...` strengthened mixed-language detection and translated known diagnostics in `multivolume.sh` and `references-6023.sh`.

Static `33970711005` on synchronized checkpoint `fd3727...` correctly exposed `tests/integration/algorithm-numbering.sh:66`. Inspection showed multiple project-owned Portuguese/mixed diagnostics in the same script. Correction `5c5b9593...` therefore:

1. translates the entire diagnostic surface of `algorithm-numbering.sh` to English rather than patching only the first failing line;
2. expands high-confidence mixed-language detection for line-numbering diagnostic phrases;
3. expands self-test coverage from 11 to 13 cases;
4. preserves academic/rendered Portuguese and bibliography data.

The subsequent Static failure `33970988780` is classified separately as documentation-governance drift, not a language/runtime failure.

Acceptance:

1. publish the synchronized governance-corrected checkpoint containing implementation `5c5b9593...`;
2. run Static contract and full Linux integration;
3. correct any further project-owned diagnostics exposed by the stronger detector instead of weakening it;
4. close only when the permanent language audit truthfully reports zero violations, governance contracts are intact, and full Linux remains green.

### 6. References and NBR 6023:2025 — PARTIAL / FAIL-CLOSED

Safe work after the language gate batch:

- item 30: expand reviewer-specific electronic-resource coverage around unknown place/publisher behavior already supported by the current compatibility layer;
- item 31: add explicit thesis/dissertation duplicate-year negative regression;
- item 32: add clear standard and multivolume bibliography fixture/evidence cases supported by current authority.

Item 33 remains `NORMATIVE-REVIEW` until authoritative current NBR 6023:2025 text is available. Do not encode older review examples as current runtime law without current-edition authority.

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
| 30 | PASS/PARTIAL | P1/P3 | Expand reviewer-case electronic-resource fixtures. |
| 31 | PASS | P3 | Add duplicate-year negative fixture. |
| 32 | PARTIAL | P1/P2 | Add current-authority standard/multivolume cases. |
| 33 | NORMATIVE-REVIEW | P1 | Wait for authoritative NBR 6023:2025 edge-case text. |
| 34 | PARTIAL | P1/P2 | Final canonical annex source/heading/TOC confirmation. |

## Additional regression findings

| Finding | State | Next action |
|---|---|---|
| Hidden historical phase-name coupling | CLOSED | Keep semantic phase governance regression. |
| Documentation can drift from implementation | ACTIVE GUARD / LATEST DRIFT CORRECTED | Static `33970988780` rejected missing governance wording; preserve required concepts in active control docs. |
| Phase closure can rely on targeted tests only | CLOSED/POLICY | Require phase-end regression on one SHA. |
| Stale V2 wording/current API vocabulary in V3 reference | CORRECTED/PROTECTED | Keep negative reference hygiene. |
| Object typography tests certified wrong upper-title size | CLOSED | Preserve current authority decision/evidence. |
| Reviewed reference-content requirements lacked source/PDF guards | CLOSED | Preserve `3ae9dd...` + `c4c59...` evidence. |
| Engineering-language gate had mixed-diagnostic false negatives | CORRECTION IN PROGRESS | Static `33970711005` exposed another case; validate `5c5b9593...` after governance-doc correction. |

## Phase transition gates

Core Corrections -> Reference PDF Validation requires all blocking shared P0/P1 corrections implemented, affected normative mappings/tests updated atomically, executable checks green, no shared runtime FAIL, authority gaps explicit/fail-closed, documentation synchronized, and one immutable Core Corrections candidate passing Static plus full Linux.

Reference PDF Validation -> Scientific Article additionally requires the corrected canonical V3 PDF to pass page-level review and reproducible presentation evidence.
