# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-05
Status: ACTIVE — CORE CORRECTIONS

## Purpose

This is the executable correction queue produced by Regression Audit. It combines the 34 librarian-review requirements, additional regression findings, authority decisions, implementation order and phase gates.

Canonical companions:

- `docs/UFC-LIBRARIAN-REVIEW.md`
- `docs/V3-REGRESSION-AUDIT.md`
- `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`
- `docs/HANDOFF-V3.0.0.md`
- `docs/ROADMAP-V3.0.0.md`
- `release/v3-roadmap.json`

## Execution discipline

Every material advance updates the relevant implementation/review state and `docs/HANDOFF-V3.0.0.md` in the same work cycle. If phase state, acceptance state, current batch, evidence state or branch/checkpoint facts change, update `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json` in the same checkpoint.

Every phase has a mandatory phase-end regression. Targeted green checks do not replace it.

## Current evidence state

Validated Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`:

- Static contract `33965794475`: success;
- full Linux integration `33965794519`: success;
- Linux summary: `PASS=31 FAIL=0 SKIP=0`.

This closes the object-typography correction. Review item 21 is now `PASS`; final-PDF evidence confirms 12 pt upper illustration/table identification/title and 10 pt lower source, and the IBGE table subset is green under the same contract.

Current implementation checkpoint `c464a1bc2ca04a4ce398878f25e9521f5840d48e` adds source-level canonical-reference regressions for review items 11, 16 and 28. The synchronized branch acceptance run is the next gate.

Current librarian-review state: **25 PASS / 8 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

## Priority model

- **P0:** contract/control blocker.
- **P1:** normative or canonical-output correctness defect.
- **P2:** reference/documentation defect.
- **P3:** evidence hardening.

## Work order

### 1. Control Plane and Regression Harness — VALIDATED

Completed and protected: readable six-phase model, machine-protected 34-item contract, semantic phase governance, documentation-on-material-advance policy, phase-end regression requirement, and baseline Static/Linux validation.

### 2. Front Matter and Institutional Metadata — PARTIAL

Covers items 1-10.

Implemented/validated core behavior includes subtitle propagation, co-advisor optionality, concentration area, variable committee size, CAPES guidance, advisor/co-advisor final punctuation, complete-name placeholder and institution/acronym examples.

Still required before Core Corrections closes:

- canonical blank/filled confirmation for optional department;
- canonical complete-author-name guidance confirmation;
- final approval-page `Instituição (sigla)` confirmation;
- final corrected canonical-PDF confirmation for summary/front-matter placement.

### 3. Body Structure, Headings, Citations and Lists — ACTIVE REFERENCE-CONTENT BATCH

Covers items 11-20 and 24-29.

Already validated: list alignment, TOC exclusion, appendix/annex direct flow, current NBR 10520 capitalization, reviewer long-quotation locator/punctuation, alínea/subalínea rules, paragraph indentation, and code/body typography.

Current implementation `c464a1b...` adds source-level guards for:

- item 11: reviewed object-title sentence case and absence of legacy title casing;
- item 16: first body-text UFC occurrence as `Universidade Federal do Ceará (UFC)`;
- item 28: reviewed heading sentence case and correct `etc.` punctuation.

Next acceptance:

1. synchronized branch Static/full Linux green;
2. extend `tests/integration/reference-corpus.sh` with PDF-text assertions for those three reviewed-content requirements;
3. reclassify items only after generated-PDF evidence is green.

### 4. Figures, Tables and Documentary Objects — VALIDATED

Covers items 21-23.

- item 21: PASS;
- item 22: PASS;
- item 23: PASS.

Accepted contract:

- upper illustration/table/object identification/title: **12 pt**, single spacing;
- lower source/legend/note: **10 pt**, single spacing where applicable;
- object text constrained to object width.

Acceptance evidence: Static `33965794475`, Linux `33965794519`, final-PDF illustration/table typography green, IBGE subset green.

### 5. References and NBR 6023:2025 — PARTIAL / FAIL-CLOSED

Covers items 30-33.

Safe work after the reference-content batch:

- item 30: expand reviewer-case electronic-resource coverage around unknown place/publisher behavior already supported by the current compatibility layer;
- item 31: add explicit duplicate-year negative regression for thesis/dissertation references;
- item 32: add clear standard and multivolume fixture/evidence cases supported by current authority.

Blocked authority work:

- item 33 DOI/availability/repeated-author/corporate-author edge cases remain `NORMATIVE-REVIEW` until authoritative current NBR 6023:2025 text is available.

Do not encode older review examples as current runtime law without current-edition authority.

### 6. Appendices, Annexes and External Source Attribution — PARTIAL

Covers item 34 and reinforces 14-15. Automated heading/pagination behavior is green and the canonical annex source example exists. Final closure requires canonical-PDF confirmation of source attribution, heading and TOC presentation.

### 7. Canonical V3 Reference Corpus Cleanup — ACTIVE

Keep rejecting/removing stale V2 wording, retired profile/API vocabulary, obsolete placeholders, and implementation-history prose presented as current user instruction. The current source-level batch also protects reviewed sentence-case/acronym content.

## Complete 34-item implementation matrix

| # | State | Priority | Remaining action / acceptance |
|---:|---|---|---|
| 1 | PARTIAL | P2 | Canonical blank/filled department confirmation. |
| 2 | PARTIAL | P2 | Canonical complete-name guidance confirmation. |
| 3 | PASS | P3 | Preserve subtitle propagation regression. |
| 4 | PASS | P1 | Preserve advisor/co-advisor punctuation regression. |
| 5 | PASS | P3 | Preserve conditional co-advisor rendering. |
| 6 | PASS | P3 | Preserve master's/doctoral concentration behavior. |
| 7 | PARTIAL | P2 | Final canonical `Instituição (sigla)` approval-page confirmation. |
| 8 | PASS | P3 | Preserve variable committee size. |
| 9 | PASS | P3 | Preserve CAPES guidance. |
| 10 | PASS | P3 | Reconfirm in corrected canonical PDF. |
| 11 | PARTIAL | P2 | `c464a1b...` source guard added; add generated-PDF text evidence. |
| 12 | PASS | P3 | Preserve 3 cm list alignment. |
| 13 | PASS | P3 | Preserve pre-textual TOC exclusion. |
| 14 | PASS | P3 | Preserve direct appendix/annex flow. |
| 15 | PASS | P3 | Final visual TOC confirmation. |
| 16 | PARTIAL | P2 | `c464a1b...` source guard added; confirm first-use phrase in generated PDF. |
| 17 | PASS | P1/P3 | Preserve code/body typography regression. |
| 18 | PASS | P3 | Preserve current NBR 10520 capitalization. |
| 19 | PASS | P1 | Preserve reviewer long-quotation locator fixture. |
| 20 | PASS | P1 | Preserve punctuation positive/negative reviewer gate. |
| 21 | PASS | P1 | Preserve 12 pt upper / 10 pt lower final-PDF and IBGE evidence. |
| 22 | PASS | P3 | Preserve object single spacing. |
| 23 | PASS | P1 | Preserve external-source locator evidence (`p. 42`). |
| 24 | PASS | P3 | Preserve lowercase alínea starts. |
| 25 | PASS | P3 | Preserve intermediate/final punctuation. |
| 26 | PASS | P3 | Preserve colon/subalínea punctuation. |
| 27 | PASS | P3 | Preserve alphabetic alínea ordering. |
| 28 | PARTIAL | P2 | `c464a1b...` source guard added; add generated-PDF heading evidence. |
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
| Object typography tests certified wrong upper-title size | CLOSED | Preserve current authority decision and final-PDF evidence. |
| Independent `tabularray-abnt` adapter retained 10 pt table caption | CLOSED | Preserve 12 pt upper / 10 pt lower regression. |
| Legacy IBGE observer retained retired 10 pt caption expectation | CLOSED | `33965794519` confirms corrected observer. |
| Mixed-language engineering diagnostics | CORRECTED IN TOUCHED GATES | Continue language sweep when adjacent files are modified. |
| Reviewed reference-content requirements lacked explicit source guards | ACTIVE | `c464a1b...` adds source guards; add PDF-level evidence next. |

## Phase transition gates

### Core Corrections -> Reference PDF Validation

Required: all blocking shared P0/P1 corrections implemented; affected normative mappings/tests updated atomically; executable checks green; no shared runtime FAIL; authority gaps explicit/fail-closed; documentation synchronized; one immutable Core Corrections candidate passes Static plus full Linux.

### Reference PDF Validation -> Scientific Article

Required: corrected canonical V3 PDF compiled with the actual class; page-level review of cover, title page, approval, lists, TOC, body, figures/tables, references, appendices and annexes; accepted preservation differences versus V2.1 documented; no unexplained visual regression; phase-end regression green.

### Scientific Article -> Final Certification

Required: article runtime/modality complete; positive/negative article evidence green; canonical article rendering accepted; shared profiles non-regressed; phase-end regression green.

### Final Certification -> Release

Required: complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix green on one immutable candidate; no unresolved certification exception; phase-end regression green and recorded.

### Release closeout

Required: documentation, bundles, assets, checksums and publication metadata finalized; no unresolved roadmap/normative item; final release regression/verification recorded.
