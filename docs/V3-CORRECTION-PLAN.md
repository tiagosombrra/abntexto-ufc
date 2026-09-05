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

Object/Core checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`: Static `33965794475`, Linux `33965794519`, item 21 closed.

Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c`: Static `33969505681`, Linux `33969505614`, `PASS=31 FAIL=0 SKIP=0`, items 11, 16 and 28 closed.

Engineering-language hardening checkpoint `edeb14b7a96d1cab3ad9551701087ddf4dff059a`: Static `33972111694`, Linux `33972111696`, permanent audit `portuguese_technical_diagnostics=0`.

Reference evidence checkpoint `bcd851b3176b516091a254bc57b5ae4e8add9358`: Static `33974062993`, Linux `33974063103`, `PASS=31 FAIL=0 SKIP=0`; bounded evidence for items 30, 31 and 32 passed and item 32 closed.

Current librarian-review state is **29 PASS / 4 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

## Priority model

- **P0:** contract/control blocker.
- **P1:** normative or canonical-output correctness defect.
- **P2:** reference/documentation defect.
- **P3:** evidence hardening.

## Work order

### 1. Control Plane and Regression Harness — VALIDATED

Readable six-phase model, machine-protected 34-item contract, semantic phase governance, documentation-on-material-advance policy, and mandatory phase-end regression are retained.

### 2. Front Matter and Institutional Metadata — ACTIVE / CORRECTED IMPLEMENTATION, CI PENDING

Initial implementation `33bdd0bd5f9360c645b4166071c32dbba6c647f0` added bounded evidence for items 1, 2 and 7 without changing runtime:

- item 1: blank department omitted / filled department rendered;
- item 2: canonical complete-author-name placeholder rendered in generated output;
- item 7: approval page renders `Instituição Externa de Teste (IET)`.

Synchronized checkpoint `48e7e6841b63ea62d6811e734dde09931b8f608c` failed Static `33980486317` because the item-2 failure diagnostic itself contained a project-prohibited Portuguese technical term. The evidence predicate and runtime were not implicated. Correction `dc381d4517341062d53ae5e93082c7856fc4af17` changes only that diagnostic to engineering English. Corrected synchronized Static/full Linux acceptance is pending.

### 3. Body Structure, Headings, Citations and Lists — VALIDATED

Items 11-20 and 24-29 retain accepted automated/source/PDF contracts.

### 4. Figures, Tables and Documentary Objects — VALIDATED

Items 21-23 are PASS. Accepted contract is 12 pt single-spaced upper identification/title and 10 pt single-spaced lower source/legend/note where applicable.

### 5. Engineering-language evidence hardening — VALIDATED/PERMANENT GUARD

Accepted at `edeb14...`. The current `33980486317` failure demonstrates the permanent guard is working: new project-owned technical diagnostics must remain English.

### 6. References and NBR 6023:2025 — VALIDATED BOUNDED BATCH

`bcd851b...` accepted reviewer-specific items 30-32 evidence without runtime changes. Item 33 remains `NORMATIVE-REVIEW`; no disputed DOI/availability/repeated-author/corporate-author runtime change is authorized without current authoritative text.

### 7. Appendices, Annexes and External Source Attribution — ACTIVE / CORRECTED IMPLEMENTATION, CI PENDING

Implementation `33bdd0bd...` extends the canonical reference-document gate for item 34: generated canonical PDF must contain the annex heading/source attribution and generated TOC must contain the annex entry. Existing independent final-PDF evidence continues to prove uppercase/bold/12 pt/centered annex heading behavior. The `dc381d45...` correction does not alter item-34 evidence.

### 8. Canonical V3 Reference Corpus Cleanup — VALIDATED/PROTECTED

Keep rejecting stale V2 wording, retired profile/API vocabulary, obsolete placeholders, reviewed legacy title casing, malformed UFC first-use and legacy heading/`etc.` forms.

## Complete 34-item implementation matrix

| # | State | Priority | Remaining action / acceptance |
|---:|---|---|---|
| 1 | PARTIAL | P2 | Blank/filled department evidence implemented; corrected synchronized CI pending. |
| 2 | PARTIAL | P2 | Complete-name canonical output evidence implemented; diagnostic corrected at `dc381d45...`; CI pending. |
| 3 | PASS | P3 | Preserve subtitle propagation. |
| 4 | PASS | P1 | Preserve advisor/co-advisor punctuation. |
| 5 | PASS | P3 | Preserve conditional co-advisor rendering. |
| 6 | PASS | P3 | Preserve concentration behavior. |
| 7 | PARTIAL | P2 | Approval-page institution/acronym evidence implemented; corrected synchronized CI pending. |
| 8 | PASS | P3 | Preserve variable committee size. |
| 9 | PASS | P3 | Preserve CAPES guidance. |
| 10 | PASS | P3 | Reconfirm in corrected canonical PDF. |
| 11 | PASS | P2 | Source/PDF evidence accepted at `c4c59...`. |
| 12 | PASS | P3 | Preserve 3 cm list alignment. |
| 13 | PASS | P3 | Preserve pre-textual TOC exclusion. |
| 14 | PASS | P3 | Preserve direct appendix/annex flow. |
| 15 | PASS | P3 | Final visual TOC confirmation remains a presentation-phase check. |
| 16 | PASS | P2 | Source/PDF first-use evidence accepted. |
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
| 28 | PASS | P2 | Source/PDF sentence-case and `etc.` evidence accepted. |
| 29 | PASS | P3 | Preserve body paragraph indentation/spacing. |
| 30 | PASS | P1/P3 | Reviewer-specific electronic evidence accepted at `bcd851b...`. |
| 31 | PASS | P3 | Single-year thesis/dissertation evidence accepted at `bcd851b...`. |
| 32 | PASS | P1/P2 | Standard/multivolume evidence accepted at `bcd851b...`. |
| 33 | NORMATIVE-REVIEW | P1 | Wait for authoritative NBR 6023:2025 edge-case text. |
| 34 | PARTIAL | P1/P2 | Canonical annex source/heading/TOC evidence implemented; corrected synchronized CI pending. |

## Additional regression findings

| Finding | State | Next action |
|---|---|---|
| Hidden historical phase-name coupling | CLOSED | Keep semantic phase governance. |
| Documentation can drift from implementation | ACTIVE GUARD | Keep mandatory reconciliation on every material advance. |
| Phase closure can rely on targeted tests only | CLOSED/POLICY | Require phase-end regression on one SHA. |
| Stale V2/current API wording | CORRECTED/PROTECTED | Keep negative reference hygiene. |
| Object typography test encoded wrong upper size | CLOSED | Preserve accepted authority/evidence. |
| Engineering-language false negatives | CLOSED/PERMANENT GUARD | Keep stronger detector; `33980486317` is a successful fail-closed discovery. |
| Current closeout diagnostic used prohibited engineering wording | CORRECTED, CI PENDING | `dc381d45...`; synchronize and re-run Static/full Linux. |

## Current batch acceptance

If the corrected synchronized checkpoint passes Static and full Linux and emits PASS evidence for items 1, 2, 7 and 34, promote the matrix to **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Then prepare a separate immutable Core Corrections phase-end regression candidate. Do not transition phases on the targeted batch result alone.

## Phase transition gates

Core Corrections -> Reference PDF Validation requires all blocking shared P0/P1 corrections implemented, no shared runtime FAIL, authority gaps explicit/fail-closed, documentation synchronized, and one immutable Core Corrections candidate passing Static plus full Linux and phase-specific acceptance checks.

Reference PDF Validation -> Scientific Article additionally requires the corrected canonical V3 PDF to pass page-level review and reproducible presentation evidence.
