# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-05
Status: ACTIVE — CORE CORRECTIONS

## Purpose

This is the executable correction queue produced by Regression Audit. It combines the 34 librarian-review requirements, additional regression findings, authority decisions, implementation order and phase gates.

Canonical companions: `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REGRESSION-AUDIT.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `release/v3-roadmap.json`.

## Execution discipline

Every material advance updates the relevant implementation/review state and canonical handoff in the same work cycle. If phase state, acceptance state, current batch, evidence state or branch/checkpoint facts change, update the roadmap and machine state in the same checkpoint. Every phase has a mandatory phase-end regression; targeted green checks do not replace it.

## Current evidence state

Object/Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` passed Static `33965794475` and Linux `33965794519`, closing item 21.

Canonical-reference source checkpoint `3ae9dd698e021a117ba2b64ebf970dc8c507fa8f` passed Static `33968579418` and full Linux `33968579449`, both green; Linux summary is `PASS=31 FAIL=0 SKIP=0`. Source-level PASS evidence for items 11, 16 and 28 is therefore accepted.

Current implementation `a1149f169f06b2db620bc5df69d0870b60fe583c` extends `tests/integration/reference-document.sh` so the compiled canonical PDF must contain the reviewed sentence-case object titles/headings and full-name UFC first-use marker while rejecting reviewed legacy forms. Branch acceptance is pending.

Current librarian-review state before that acceptance: **25 PASS / 8 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

## Priority model

- **P0:** contract/control blocker.
- **P1:** normative or canonical-output correctness defect.
- **P2:** reference/documentation defect.
- **P3:** evidence hardening.

## Work order

### 1. Control Plane and Regression Harness — VALIDATED

Readable six-phase model, machine-protected 34-item contract, semantic phase governance, documentation-on-material-advance policy, phase-end regression requirement, and baseline Static/Linux validation are complete.

### 2. Front Matter and Institutional Metadata — PARTIAL

Covers items 1-10. Core behavior for subtitle propagation, co-advisor optionality, concentration area, variable committee size, CAPES guidance, advisor punctuation, complete-name placeholder and institution/acronym examples is implemented. Remaining: canonical blank/filled department confirmation, complete-author-name guidance confirmation, final approval-page `Instituição (sigla)` confirmation, and final canonical-PDF front-matter inspection.

### 3. Body Structure, Headings, Citations and Lists — ACTIVE CANONICAL-PDF BATCH

Covers items 11-20 and 24-29.

Validated: list alignment, TOC exclusion, appendix/annex direct flow, current NBR 10520 capitalization, reviewer long-quotation locator/punctuation, alínea/subalínea rules, paragraph indentation, code/body typography, and source-level reviewed-content evidence for items 11, 16 and 28.

Current implementation `a1149...` adds generated-PDF checks for:

- item 11: reviewed sentence-case object titles and absence of legacy casing;
- item 16: rendered `Universidade Federal do Ceará (UFC)` plus source first-use guard;
- item 28: reviewed sentence-case headings, absence of legacy headings, and malformed `etc` punctuation rejection.

Acceptance: synchronize branch, run normal Static/full Linux, inspect explicit item 11/16/28 PDF evidence in the Reference document gate, then reclassify only if green.

### 4. Figures, Tables and Documentary Objects — VALIDATED

Items 21-23 are PASS. Accepted contract is 12 pt single-spaced upper identification/title, 10 pt single-spaced lower source/legend/note where applicable, all constrained to object width.

### 5. Engineering-language evidence hardening — QUEUED NEXT

A new regression finding was identified after the source-level reference batch: the permanent engineering-language gate reports zero Portuguese project-owned diagnostics while mixed Portuguese/English diagnostics remain in at least `tests/integration/multivolume.sh` and `tests/integration/references-6023.sh`.

Required bounded correction:

1. strengthen `tests/checks/engineering_language.py` with high-confidence mixed-language phrase detection rather than broad Portuguese stopwords that could flag legitimate academic literals;
2. extend its self-test with known false-negative mixed diagnostics;
3. translate affected project-owned diagnostics to English;
4. run Static contract and relevant integration; document any additional files exposed by the strengthened detector;
5. keep academic/rendered Portuguese explicitly protected.

### 6. References and NBR 6023:2025 — PARTIAL / FAIL-CLOSED

Covers items 30-33.

Safe work after the language gate batch:

- item 30: expand reviewer-specific electronic-resource coverage around unknown place/publisher behavior already supported by the current compatibility layer;
- item 31: add explicit thesis/dissertation duplicate-year negative regression;
- item 32: add clear standard and multivolume bibliography fixture/evidence cases supported by current authority.

Item 33 remains `NORMATIVE-REVIEW` until authoritative current NBR 6023:2025 text is available. Do not encode older review examples as current runtime law without current-edition authority.

### 7. Appendices, Annexes and External Source Attribution — PARTIAL

Automated heading/pagination behavior is green and the canonical annex source example exists. Final closure requires canonical-PDF confirmation of source attribution, heading and TOC presentation.

### 8. Canonical V3 Reference Corpus Cleanup — ACTIVE

Keep rejecting stale V2 wording, retired profile/API vocabulary, obsolete placeholders, and implementation-history prose presented as current user instruction. The source/PDF gates now explicitly protect the reviewed sentence-case/acronym content.

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
| 11 | PARTIAL | P2 | Source evidence green at `3ae9dd...`; PDF evidence implemented at `a1149...`, acceptance pending. |
| 12 | PASS | P3 | Preserve 3 cm list alignment. |
| 13 | PASS | P3 | Preserve pre-textual TOC exclusion. |
| 14 | PASS | P3 | Preserve direct appendix/annex flow. |
| 15 | PASS | P3 | Final visual TOC confirmation. |
| 16 | PARTIAL | P2 | Source evidence green; PDF evidence implemented, acceptance pending. |
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
| 28 | PARTIAL | P2 | Source evidence green; PDF evidence implemented, acceptance pending. |
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
| Documentation can drift from implementation | CLOSED/POLICY | Update docs with every material advance. |
| Phase closure can rely on targeted tests only | CLOSED/POLICY | Require phase-end regression on one SHA. |
| Stale V2 wording/current API vocabulary in V3 reference | CORRECTED/PROTECTED | Keep negative reference hygiene. |
| Object typography tests certified wrong upper-title size | CLOSED | Preserve current authority decision/evidence. |
| Independent table adapter retained 10 pt table caption | CLOSED | Preserve corrected regression. |
| Legacy IBGE observer retained retired 10 pt caption expectation | CLOSED | Preserve corrected observer. |
| Reviewed reference-content requirements lacked source/PDF guards | IN PROGRESS | Source green at `3ae9dd...`; PDF gate `a1149...` pending acceptance. |
| Engineering-language gate has false negatives for mixed diagnostics | OPEN/P3 | Strengthen detector + translate mixed diagnostics after current batch. |

## Phase transition gates

Core Corrections -> Reference PDF Validation requires all blocking shared P0/P1 corrections implemented, affected normative mappings/tests updated atomically, executable checks green, no shared runtime FAIL, authority gaps explicit/fail-closed, documentation synchronized, and one immutable Core Corrections candidate passing Static plus full Linux.

Reference PDF Validation -> Scientific Article additionally requires the corrected canonical V3 PDF to pass page-level review and reproducible presentation evidence. Subsequent phases retain their heavy certification/release gates defined in the roadmap.
