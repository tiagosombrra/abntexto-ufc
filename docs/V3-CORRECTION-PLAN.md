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

## Current validated state

Checkpoint `f6ca012164273e67480dca127fe17b392e8a8a21`:

- Static contract `33939512055`: success;
- full Linux integration `33939512019`: success;
- Linux summary: `PASS=31 FAIL=0 SKIP=0`.

Current librarian-review state: **24 PASS / 8 PARTIAL / 1 FAIL / 1 NORMATIVE-REVIEW**.

Confirmed closures in this cycle:

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

### 4. Figures, Tables and Documentary Objects — ACTIVE P1 BATCH

Covers items 21-23.

Item 23 is PASS. Item 22 is PASS. Item 21 is the current shared runtime FAIL.

Authority decision is recorded in `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`:

- upper illustration/table/object identification/title: **12 pt**, single spacing;
- lower source/legend/note: **10 pt**, single spacing where applicable;
- object text remains constrained to the object width.

Implementation candidate: `abntexto-ufc/objects.def`, the active normative contract, locator ownership and final-PDF rules have been migrated to the accepted 12 pt upper-title semantics. Item 21 intentionally remains FAIL until Static/full Linux evidence is green.

Required atomic migration:

1. remove upper identification/title from the reduced-font rule group;
2. introduce semantically correct body-size title rules;
3. preserve provenance for historical rule IDs instead of silently changing their meaning;
4. update `objects.def` to render upper identification/title at 12 pt and single spacing;
5. retain reduced 10 pt source/legend/note behavior;
6. update locator audits, scenarios/checkers and expected evidence;
7. run Static contract + full Linux integration;
8. only after green final-PDF measurements, move item 21 from FAIL to PASS and synchronize all documents.

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
| 21 | FAIL | P1 | Migrate upper object title to 12 pt and update normative/final-PDF evidence atomically. |
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
| Object typography tests certify wrong upper-title size | ACTIVE FAIL | Perform atomic object contract/runtime/evidence migration. |
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
