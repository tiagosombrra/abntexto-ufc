# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-04
Status: ACTIVE — CORE CORRECTIONS

## Purpose

This is the executable correction plan produced by **Regression Audit**. It combines:

1. defects and control-plane risks found by regressing the current v3 implementation and tests;
2. all 34 requirements recovered from the two librarian-reviewed PDFs;
3. the authority/evidence work required before a disputed rule can change runtime behavior;
4. the acceptance evidence required to prevent the same regression from returning.

The detailed review provenance remains in `docs/UFC-LIBRARIAN-REVIEW.md`. The investigation narrative remains in `docs/V3-REGRESSION-AUDIT.md`. This document is the implementation queue.

## Execution discipline

Every material advance must update the relevant implementation/review state and `docs/HANDOFF-V3.0.0.md` in the same work cycle. If the advance changes phase state, acceptance state, current batch, evidence state, or branch/checkpoint facts, `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json` must be updated in the same checkpoint. Documentation reconciliation is part of implementation, not end-of-phase cleanup.

Every phase has a mandatory phase-end regression. A phase cannot be marked `CLOSED` and the next phase cannot become `ACTIVE` until one immutable candidate SHA has passed the full relevant regression and the result has been recorded. Targeted checks used to close individual corrections do not replace this gate.

The phase-end regression includes, as applicable:

- `Static contract`;
- full relevant `Linux integration`;
- all phase-specific acceptance checks;
- canonical-PDF rendering and visual inspection when presentation is in scope;
- the heavy literal-font/Windows/PDF-A/distribution matrix when closing Final Certification;
- synchronized documentation, review matrices, and machine state after the result is known.

Any unexplained regression failure blocks transition and reopens the affected phase work.

## Priority model

- **P0 — Contract/control blocker:** the repository cannot safely advance while unresolved.
- **P1 — Normative or canonical-output defect:** affects the correctness of academic output or institutional compliance.
- **P2 — Reference/documentation defect:** runtime may already be correct, but the canonical example teaches or demonstrates the wrong contract.
- **P3 — Evidence hardening:** behavior may be correct, but regression evidence is insufficient.

## Work order

### Correction Group 1 — Control Plane and Regression Harness

**Priority:** P0

1. Keep the readable phase model authoritative in `release/v3-roadmap.json`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md`.
2. Remove hidden test/validator coupling to retired opaque phase names while preserving the semantic gates those checks were enforcing.
3. Keep the 34-point librarian contract machine-protected.
4. Run the full PR integration contract after the control-plane migration.
5. Classify any failure as either an actual product regression or an obsolete phase-name coupling before modifying tests.
6. Keep progress documentation synchronized with every material advance and enforce a phase-end regression before every phase transition.

**Acceptance:** static contract green; full Linux PR integration green; no unknown phase consumers; article source rules remain source-review-only before the Scientific Article phase; phase-transition regression policy is machine/documentation protected.

### Correction Group 2 — Front Matter and Institutional Metadata

**Priority:** P1/P2

Covers review items 1-10.

- optional department/unit rendering and placeholder guidance;
- complete author-name guidance;
- subtitle propagation;
- advisor/co-advisor punctuation;
- co-advisor optionality;
- master's/doctoral concentration area;
- committee institution/acronym presentation;
- variable committee size;
- CAPES acknowledgment guidance;
- summary vertical placement.

**Primary surfaces:** `abntexto-ufc/core.def`, `abntexto-ufc/academic-works.def`, `abntexto-ufc/frontmatter.def`, `template/main.tex`, front-matter fixtures/checks.

**Acceptance:** profile fixtures cover blank/filled optional fields; title and approval pages contain correct punctuation/labels; canonical PDF confirms placement; no blank phantom lines.

### Correction Group 3 — Body Structure, Headings, Citations and Lists

**Priority:** P1/P2/P3

Covers review items 11-20 and 24-29.

- sentence case for object/example headings where applicable;
- pre-textual list alignment and TOC exclusion;
- no aggregate appendix/annex entry pages;
- appendix/annex TOC styling;
- first-use UFC acronym presentation;
- academic body font consistency versus documentation/code notation;
- current NBR 10520 citation capitalization;
- page locator and terminal punctuation for long direct quotations;
- alínea/subalínea alphabetical ordering, lowercase starts, semicolons and colon transition;
- first-line indentation;
- removal of stale V2 wording and retired public-profile vocabulary from the V3 reference corpus.

Checkpoint `1eab2539e418224e2a6ce85ef09065941b719ef7` adds reviewer-specific evidence for item 19 (available locator in a long direct quotation) and item 20 (no extraneous full stop before the following parenthetical citation). Static contract is green; full Linux confirmation is still required before the matrix rows are closed.

**Primary surfaces:** `abntexto-ufc/layout.def`, `abntexto-ufc/integrations/abntexto.def`, `template/chapters/*.tex`, back-matter integration, citation fixtures/checks.

**Acceptance:** positive/negative fixtures for automatable rules; reference corpus no longer teaches V2 vocabulary; canonical PDF confirms heading/list/indent presentation.

### Correction Group 4 — Figures, Tables and Documentary Objects

**Priority:** P1

Covers review items 21-23 and the regression-discovered object-typography conflict.

Current evidence must distinguish three different concepts that the existing implementation partly conflates:

1. upper object **identification/title**;
2. lower **source**;
3. optional lower **legend/note/other information**.

The current UFC academic-work guide states that body text is size 12 and lists legends and illustration/table sources among the smaller uniform exceptions. Its illustration section separately defines the upper identification/title, then the lower source, then optional legend/notes. The current implementation applies `\abntsmall` to the complete upper title block as well as the source/note blocks. The recovered librarian review repeatedly marks the upper figure/table title as size 12.

**Planned correction decision:** do not preserve the existing `caption = 10 pt` mapping merely because its tests are green. Reconcile the current ABNT clause if licensed access is available; absent contrary current technical text, split the machine contract so that the upper identification/title follows body size while source/legend/note retain the reduced uniform size required by the UFC guide.

Other object corrections:

- preserve single spacing for title/source/note blocks;
- preserve width binding to the object rather than page width;
- demonstrate source page locators when the object is not author-produced and a page exists;
- update figure/table fixtures and final-PDF typography measurements atomically with the normative catalog.

Checkpoint `1eab2539e418224e2a6ce85ef09065941b719ef7` adds an external-illustration source with locator `p. 42` and explicit regression evidence for review item 23. Full Linux confirmation is still required before the matrix row is closed.

**Primary surfaces:** `abntexto-ufc/objects.def`, `standards/catalog.json`, typography locator/coverage manifests, illustration/table final-PDF scenarios, object fixtures/checks, canonical reference examples.

**Acceptance:** the semantic contract no longer conflates upper identification/title with lower legend/source/note typography; final-PDF measurement proves the accepted title/source/legend sizes and single spacing; review examples match the accepted contract. Existing public rule IDs must not be silently changed; any unavoidable identifier migration requires explicit compatibility/provenance handling.

### Correction Group 5 — References and NBR 6023:2025

**Priority:** P1/P3

Covers review items 30-33.

Do not translate old-review examples directly into 2026 runtime rules. The current project correctly treats NBR 6023:2025 as higher technical authority than the UFC reference guide that still cites the 2018 edition.

Regression cases to close:

- online resources with unknown place/publisher data;
- thesis/dissertation work type, program/institution and year without duplication;
- standards and multivolume physical-description cases;
- DOI, URL, `Disponível em:` and access-date behavior by documentary type;
- repeated personal/corporate authors;
- state/government corporate author cases such as `São Paulo (Estado)`;
- UFC electronic-resource examples.

The existing locator audit explicitly marks the exact current NBR 6023:2025 DOI and online-access clauses as unavailable without authoritative/licensed access. Those items therefore remain fail-closed until authoritative text is supplied or a current source-backed project classification is recorded.

**Primary surfaces:** `abntexto-ufc/bibliography.def`, `abntexto-ufc/standards/nbr6023-2025.def`, `template/backmatter/references.bib`, reference fixtures/checks, normative locator/coverage manifests.

**Acceptance:** each disputed review case has a current-edition decision with provenance; positive and negative bibliography fixtures pass; no superseded 2018 rule silently overrides NBR 6023:2025.

### Correction Group 6 — Appendices, Annexes and External Source Attribution

**Priority:** P1/P2

Covers review item 34 and reinforces items 14-15.

- preserve direct `APÊNDICE A` / `ANEXO A` flow without aggregate pages;
- preserve required primary-heading styling;
- make the annex example explicitly demonstrate the source of external attached material;
- verify TOC presentation and continuous pagination in the canonical PDF.

**Primary surfaces:** `abntexto-ufc/backmatter.def`, `template/backmatter/appendices/*`, `template/backmatter/annexes/*`, back-matter checks.

**Acceptance:** canonical annex demonstrates source attribution; automated back-matter checks remain green; rendered TOC and heading styling pass visual inspection.

### Correction Group 7 — Canonical V3 Reference Corpus Cleanup

**Priority:** P2

Additional regression findings not limited to the 34 librarian items:

- remove rendered phrases such as `Na V2` / `A V2` from the current V3 guide;
- replace retired profile term `tccgraduacao` with `undergraduate-capstone`;
- ensure placeholders teach the current V3 public API and optionality rules;
- do not describe implementation history as current user guidance;
- preserve technical examples without allowing them to redefine academic body typography.

**Primary surfaces:** `template/main.tex`, `template/chapters/*.tex`, reference-corpus checks.

**Acceptance:** reference-corpus checks explicitly reject stale V2 profile vocabulary/current-state wording; canonical V3 PDF contains only current API terminology except clearly labelled migration/history material.

## Complete 34-item implementation matrix

| # | Audit state | Priority | Correction / validation action | Acceptance evidence |
|---:|---|---|---|---|
| 1 | PARTIAL | P2 | Make department placeholder explicitly optional and preserve blank-line suppression. | Blank/filled front-matter fixture + canonical cover. |
| 2 | PARTIAL | P2 | Change canonical author placeholder/guidance to complete name. | Reference-corpus assertion + canonical PDF. |
| 3 | PASS | P3 | Retain subtitle propagation; add explicit regression coverage across cover/title/approval. | Front-matter fixture. |
| 4 | FAIL | P1 | Add reviewed final punctuation to advisor/co-advisor identification where required. | Exact-text fixture + canonical title page. |
| 5 | PASS | P3 | Retain conditional co-advisor rendering. | Blank/filled fixture. |
| 6 | PASS | P3 | Retain concentration area for master's/doctoral nature blocks. | Profile fixtures. |
| 7 | PARTIAL | P2 | Standardize/demonstrate `Instituição (sigla)` for committee members; decide helper versus author-supplied string. | Approval-page fixture + canonical example. |
| 8 | PASS | P3 | Retain variable committee members through examiner 6. | Multi-member fixture. |
| 9 | PASS | P3 | Retain CAPES Portaria 206/2018 guidance and keep it discoverable. | Reference-corpus check. |
| 10 | PASS | P3 | Re-measure summary heading position in the corrected canonical PDF. | Final-PDF geometry/visual check. |
| 11 | PARTIAL | P2 | Correct example/object titles to sentence case where applicable. | Reference-corpus check. |
| 12 | PASS | P3 | Retain 3 cm list alignment. | Front-matter geometry check. |
| 13 | PASS | P3 | Retain exclusion of pre-textual elements from TOC. | TOC fixture. |
| 14 | PASS | P3 | Retain direct appendix/annex flow without aggregate entries. | Back-matter fixture. |
| 15 | PASS | P3 | Reconfirm appendix/annex TOC uppercase/bold presentation visually. | Canonical PDF visual check. |
| 16 | PARTIAL | P2 | Make first body use of UFC demonstrate full name + acronym. | Reference-corpus assertion. |
| 17 | NORMATIVE-REVIEW | P1 | Separate academic font policy from code/documentation notation and define permitted exceptions. | Source-backed decision + typography fixture. |
| 18 | PASS | P3 | Retain current NBR 10520 capitalization behavior. | Citation checks. |
| 19 | PARTIAL — IMPLEMENTED, CI PENDING | P1 | Validate an available page/locator in a long direct-quote example. | `mainmatter-long-quotation-citation-test.tex` + full Linux confirmation. |
| 20 | PARTIAL — IMPLEMENTED, CI PENDING | P1 | Reject extraneous punctuation immediately before a parenthetical long-quote citation. | Positive/negative punctuation gate + full Linux confirmation. |
| 21 | NORMATIVE-REVIEW | P1 | Split upper object identification/title from lower legend/source/note; re-evaluate current 10 pt title implementation against current authority. | Updated normative contract + final-PDF typography measurements. |
| 22 | PASS | P3 | Retain single spacing for required object text blocks. | Object final-PDF measurement. |
| 23 | PARTIAL — IMPLEMENTED, CI PENDING | P1 | Demonstrate/validate source page locator when applicable. | Documentary-source fixture with `p. 42` + full Linux confirmation. |
| 24 | PASS | P3 | Retain lowercase alínea starts. | Layout fixture. |
| 25 | PASS | P3 | Retain semicolon/intermediate and final punctuation rules. | Layout fixture. |
| 26 | PASS | P3 | Retain colon transition and subordinate punctuation for subalíneas. | Layout fixture. |
| 27 | PASS | P3 | Retain alphabetic alínea ordering. | Layout fixture. |
| 28 | PARTIAL | P2 | Correct sentence-case example headings and `etc.` punctuation. | Reference-corpus check. |
| 29 | PASS | P3 | Retain 2 cm first-line indent and no extra inter-paragraph space. | Layout/final-PDF measurement. |
| 30 | PASS/PARTIAL | P1/P3 | Expand NBR 6023:2025 fixtures for electronic unknown-publication-data cases. | Bibliography positive/negative fixtures. |
| 31 | PASS | P3 | Retain corrected thesis/dissertation structure and add duplicate-year negative case. | Bibliography fixture. |
| 32 | PARTIAL | P1/P2 | Add current-edition standard and multivolume examples, including physical-description convention when applicable. | Bibliography fixture + reference example. |
| 33 | NORMATIVE-REVIEW | P1 | Resolve DOI/availability/repeated-author/corporate-author edge cases from authoritative NBR 6023:2025 text before changing runtime. | Locator status + bibliography fixtures. |
| 34 | PARTIAL | P1/P2 | Add explicit source to annexed external material and revalidate bold heading/TOC presentation. | Annex fixture + canonical PDF. |

## Additional regression findings outside the 34 review items

| Finding | Priority | Action | Acceptance |
|---|---|---|---|
| Hidden phase-name coupling in normative validator | P0 | Bind semantics to readable phase states, not historical labels. | Static + full integration green. |
| Control files can drift after material implementation advances | P0 | Update handoff/execution state in the same work cycle as each advance. | Git/machine/docs reconciliation check. |
| Phase closure can otherwise rely on accumulated targeted checks | P0 | Require a full phase-end regression on one immutable candidate before every transition. | Recorded phase regression SHA/run IDs and green results. |
| Stale V2 wording in V3 reference corpus | P2 | Rewrite/remove as current guidance. | Reference-corpus negative check. |
| Retired `tccgraduacao` term in V3 introduction | P2 | Replace with current `undergraduate-capstone`. | Reference-corpus negative check. |
| Existing object typography tests may certify the wrong title-size mapping | P1 | Change source contract, implementation and final-PDF fixtures atomically after authority decision. | Normative + object checks green on corrected semantics. |
| Current roadmap previously duplicated too much history | P0 | Keep active control files concise; rely on Git/PR/release history. | Control-plane static check. |
| Scientific-article runtime would build on unresolved shared behavior | P0 | Keep it deferred through Regression Audit, Core Corrections and Reference PDF Validation. | Roadmap semantic gate. |

## Phase transitions

### Universal transition rule

Before **any** phase transitions to the next one:

- finish and document the phase work;
- freeze one candidate SHA;
- run the mandatory phase-end regression on that SHA;
- record Static contract, full relevant Linux integration, phase-specific evidence, and required manual/visual acceptance;
- update the handoff, roadmap, machine state, and relevant matrix with the results;
- keep the phase open if any unexplained failure remains.

### Regression Audit -> Core Corrections

Required:

- control-plane/static contracts green;
- full current integration result recorded;
- all 34 items protected and classified;
- every additional regression finding recorded;
- object typography and NBR 6023 disputes have explicit source/availability status;
- no unclassified test failure;
- Regression Audit phase-end regression green and recorded.

### Core Corrections -> Reference PDF Validation

Required:

- all shared P0/P1 corrections implemented;
- affected normative catalog/rule IDs and tests updated atomically;
- all executable positive/negative checks green;
- no shared `FAIL` or unexplained `NORMATIVE-REVIEW` remains;
- documentation and review matrices synchronized with the candidate;
- Core Corrections phase-end regression green on that immutable candidate.

### Reference PDF Validation -> Scientific Article

Required:

- canonical corrected V3 PDF compiled with the actual class;
- page-level review of cover, title page, approval, lists, TOC, body, figures/tables, references, appendices and annexes;
- accepted preservation differences versus the V2.1 baseline documented;
- no unexplained visual regression;
- Reference PDF Validation phase-end regression green on the accepted canonical-PDF checkpoint.

### Scientific Article -> Final Certification

Required:

- article runtime and modality behavior complete;
- positive/negative article evidence green;
- canonical article rendering accepted;
- shared profiles remain non-regressed;
- Scientific Article phase-end regression green on one immutable SHA.

### Final Certification -> Release

Required:

- complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix green on one immutable candidate;
- no unresolved certification exception;
- Final Certification phase-end regression, including heavy platform/font/PDF-A coverage, green and recorded.

### Release closeout

Required:

- documentation, bundles, assets, checksums and publication metadata finalized;
- no unresolved roadmap/normative item;
- final release regression/verification on the release candidate recorded before the release is considered closed.
