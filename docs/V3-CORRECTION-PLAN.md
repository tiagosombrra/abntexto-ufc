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

Every material advance must update the relevant implementation/review state and `docs/HANDOFF-V3.0.0.md` in the same work cycle. If phase state, acceptance state, current batch, evidence state or branch/checkpoint facts change, update `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json` in the same checkpoint.

Every phase has a mandatory phase-end regression. A phase cannot close and the next phase cannot become active until one immutable candidate SHA has passed the full relevant regression and the result has been recorded. Targeted green checks do not replace the phase-end regression.

## Current evidence state

Latest fully validated Core Corrections/control checkpoint remains `f6ca012164273e67480dca127fe17b392e8a8a21`:

- Static contract `33939512055`: success;
- full Linux integration `33939512019`: success;
- Linux summary: `PASS=31 FAIL=0 SKIP=0`.

Object-typography implementation progressed through three bounded checkpoints:

1. `f2f5124c4adcb34069a667f1ef80c76fb17728bd` migrated the normative rule IDs, shared object runtime, locators and final-PDF expectations.
2. Full Linux run `33963240297` exposed an independent `tabularray-abnt` compatibility adapter that still forced table identification to 10 pt; runtime commit `7ec385ebecf21ba17e59db1e7ec16d3336f4bf4c` corrected that residual.
3. Checkpoint `faa487ed38ca130c9eb9da597d2902603f269a0a` passed Static run `33964421654`. Full Linux run `33964421597` then confirmed the corrected final-PDF object split — illustration title 12 pt, illustration source 10 pt, table title 12 pt, table source 10 pt — but failed one independent legacy assertion in `tests/integration/table-ibge.sh` that still expected a 10 pt table caption. Commit `a3ce2d82899162d12b06c7335b149dc2b44ecfa3` aligns that stale observer with the accepted contract.

Current librarian-review state remains **24 PASS / 8 PARTIAL / 1 FAIL / 1 NORMATIVE-REVIEW** until a normal branch checkpoint containing `a3ce2d8...` passes Static contract and full Linux integration.

Confirmed closures already retained in this cycle:

- item 4 — advisor/co-advisor punctuation;
- item 17 — academic/code typography consistency in the exercised contract;
- item 19 — long-quotation locator;
- item 20 — no extraneous full stop before parenthetical long-quote citation;
- item 23 — page locator in external illustration source when applicable.

## Priority model

- **P0:** contract/control blocker.
- **P1:** normative or canonical-output correctness defect.
- **P2:** reference/documentation defect.
- **P3:** evidence hardening.

## Work order

### 1. Control Plane and Regression Harness — VALIDATED

Completed:

- readable six-phase model;
- machine-protected 34-item review contract;
- removal of historical phase-name coupling;
- synchronized progress-documentation requirement;
- mandatory phase-end regression requirement;
- full static/Linux validation.

Keep these protections active throughout the remaining work.

### 2. Front Matter and Institutional Metadata — PARTIAL

Covers items 1-10.

Implemented/validated core behavior includes subtitle propagation, co-advisor optionality, concentration area, variable committee size, CAPES guidance and advisor/co-advisor final punctuation.

Still required before Core Corrections close:

- canonical blank/filled confirmation for optional department;
- canonical complete-author-name guidance confirmation;
- final approval-page `Instituição (sigla)` visual confirmation;
- final corrected canonical-PDF confirmation for summary/front-matter placement.

### 3. Body Structure, Headings, Citations and Lists — PARTIAL

Covers items 11-20 and 24-29.

Validated:

- list alignment and TOC exclusion;
- appendix/annex direct flow;
- current citation capitalization behavior;
- long-quotation locator and punctuation reviewer cases;
- alínea/subalínea rules;
- paragraph indentation;
- body/code typography contract exercised by integration.

Remaining:

- sentence-case cleanup for reviewed headings/object examples;
- final canonical confirmation of first-use `Universidade Federal do Ceará (UFC)`;
- final reference-corpus sweep for stale V2/current-state wording.

### 4. Figures, Tables and Documentary Objects — IMPLEMENTED / FINAL REGRESSION PENDING

Covers items 21-23.

Item 23 is PASS. Item 22 is PASS. Item 21 remains the only recorded FAIL until branch-level regression confirms the complete implementation plus observer migration.

Authority decision is recorded in `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`:

- upper illustration/table/object identification/title: **12 pt**, single spacing;
- lower source/legend/note: **10 pt**, single spacing where applicable;
- object text remains constrained to the object width.

Implementation chain:

1. `f2f5124c...` removed upper identification/title from the reduced-font rule group, introduced semantically correct body-size title rules, preserved historical rule provenance in `standards/rule-migrations.json`, updated `objects.def`, split illustration/table locator ownership and updated final-PDF scenarios/checkers.
2. Linux run `33963240297` exposed the separate table-theme adapter; `7ec385e...` changed `caption,lasthead,capcont` to `\normalsize` while retaining reduced lower auxiliary styles.
3. Linux run `33964421597` proved both final-PDF title/source splits correct but exposed a stale independent IBGE gate still asserting 10 pt for the table caption.
4. `a3ce2d8...` updates the IBGE caption observer to 12 pt while preserving source/note at 10 pt and converts its project-owned technical diagnostics to English.

Acceptance still required:

1. normal Static contract on a branch checkpoint containing `a3ce2d8...` plus synchronized documentation;
2. full Linux integration on that same checkpoint;
3. confirm illustration and table final-PDF evidence remain 12 pt upper identification/title and 10 pt lower source;
4. confirm the IBGE subset gate passes with the same contract;
5. only after green evidence, move item 21 from FAIL to PASS and synchronize all control documents.

### 5. References and NBR 6023:2025 — PARTIAL / FAIL-CLOSED

Covers items 30-33.

Safe work:

- expand current-edition fixtures for electronic resources with unknown publication data;
- add thesis/dissertation duplicate-year negative case;
- add standard/multivolume cases where current authority is clear.

Blocked authority work:

- item 33 DOI/availability/repeated-author/corporate-author edge cases remain NORMATIVE-REVIEW until authoritative current NBR 6023:2025 text is available.

Do not encode older review examples as current runtime law without current-edition authority.

### 6. Appendices, Annexes and External Source Attribution — PARTIAL

Covers item 34 and reinforces 14-15.

Automated heading/pagination behavior is green and the canonical annex source example has been introduced. Final closure requires corrected canonical-PDF visual confirmation of source attribution, heading and TOC presentation.

### 7. Canonical V3 Reference Corpus Cleanup — PARTIAL

Continue rejecting/removing:

- rendered current guidance such as `Na V2` / `A V2`;
- retired profile `tccgraduacao` in current V3 guidance;
- obsolete API vocabulary/placeholders;
- implementation-history prose presented as current user instruction.

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
| 11 | PARTIAL | P2 | Correct/confirm sentence case in reviewed examples. |
| 12 | PASS | P3 | Preserve 3 cm list alignment. |
| 13 | PASS | P3 | Preserve pre-textual TOC exclusion. |
| 14 | PASS | P3 | Preserve direct appendix/annex flow. |
| 15 | PASS | P3 | Final visual TOC confirmation. |
| 16 | PARTIAL | P2 | Final canonical first-use UFC acronym confirmation. |
| 17 | PASS | P1/P3 | Preserve code/body typography regression. |
| 18 | PASS | P3 | Preserve current NBR 10520 capitalization. |
| 19 | PASS | P1 | Preserve reviewer long-quotation locator fixture. |
| 20 | PASS | P1 | Preserve punctuation positive/negative reviewer gate. |
| 21 | FAIL | P1 | Runtime and final-PDF contract are aligned; `a3ce2d8...` fixes the stale IBGE 10 pt observer. Close only after normal Static + full Linux are green on the synchronized branch checkpoint. |
| 22 | PASS | P3 | Preserve object single spacing. |
| 23 | PASS | P1 | Preserve external-source locator evidence (`p. 42`). |
| 24 | PASS | P3 | Preserve lowercase alínea starts. |
| 25 | PASS | P3 | Preserve intermediate/final punctuation. |
| 26 | PASS | P3 | Preserve colon/subalínea punctuation. |
| 27 | PASS | P3 | Preserve alphabetic alínea ordering. |
| 28 | PARTIAL | P2 | Finish sentence-case/`etc.` reference cleanup. |
| 29 | PASS | P3 | Preserve 2 cm first-line indent/no extra paragraph spacing. |
| 30 | PASS/PARTIAL | P1/P3 | Expand reviewer-case electronic-resource fixtures. |
| 31 | PASS | P3 | Add duplicate-year negative fixture. |
| 32 | PARTIAL | P1/P2 | Add current-edition standard/multivolume cases. |
| 33 | NORMATIVE-REVIEW | P1 | Wait for authoritative NBR 6023:2025 edge-case text. |
| 34 | PARTIAL | P1/P2 | Final canonical annex source/heading/TOC visual confirmation. |

## Additional regression findings

| Finding | State | Next action |
|---|---|---|
| Hidden historical phase-name coupling | CLOSED | Keep semantic phase governance regression. |
| Documentation can drift from implementation | CLOSED/POLICY | Update docs with every material advance. |
| Phase closure can rely on targeted tests only | CLOSED/POLICY | Require phase-end regression on one SHA. |
| Stale V2 wording in current V3 reference | PARTIAL | Complete reference-corpus sweep. |
| Retired `tccgraduacao` in V3 current guidance | CORRECTED/PROTECTED | Preserve negative regression. |
| Object typography tests certified wrong upper-title size | RUNTIME/CONTRACT CORRECTED; ACCEPTANCE PENDING | Confirm synchronized branch Static/full Linux after `a3ce2d8...`. |
| Independent `tabularray-abnt` adapter retained 10 pt table caption | CORRECTED | Preserve 12 pt upper / 10 pt lower regression. |
| Legacy IBGE integration observer retained retired 10 pt caption expectation | CORRECTED; CI PENDING | Rerun full Linux on synchronized checkpoint. |
| Mixed-language engineering diagnostics | CORRECTED IN TOUCHED GATES | Continue language sweep when adjacent files are modified. |

## Phase transition gates

### Core Corrections -> Reference PDF Validation

Required:

- all blocking shared P0/P1 corrections implemented;
- affected normative catalog/rule IDs and tests updated atomically;
- all executable positive/negative checks green;
- no shared runtime FAIL remains;
- remaining authority gaps explicit and fail-closed;
- documentation/review matrices synchronized with the candidate;
- Core Corrections phase-end regression green on one immutable candidate SHA.

### Reference PDF Validation -> Scientific Article

Required:

- corrected canonical V3 PDF compiled with the actual class;
- page-level review of cover, title page, approval, lists, TOC, body, figures/tables, references, appendices and annexes;
- accepted preservation differences versus V2.1 documented;
- no unexplained visual regression;
- Reference PDF Validation phase-end regression green on the accepted canonical checkpoint.

### Scientific Article -> Final Certification

Required:

- article runtime/modality complete;
- positive/negative article evidence green;
- canonical article rendering accepted;
- shared profiles remain non-regressed;
- Scientific Article phase-end regression green on one immutable SHA.

### Final Certification -> Release

Required:

- complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix green on one immutable candidate;
- no unresolved certification exception;
- Final Certification phase-end regression green and recorded.

### Release closeout

Required:

- documentation, bundles, assets, checksums and publication metadata finalized;
- no unresolved roadmap/normative item;
- final release regression/verification recorded.
