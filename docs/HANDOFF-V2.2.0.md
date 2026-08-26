# abntexto-ufc v2.2.0 — Canonical Handoff

Updated: 2026-08-26

This file is the canonical continuation point for the v2.2.0 audit/release plan. Future work must read this file before relying on chat history. Git history, PR bodies/comments and exact GitHub Actions runs remain authoritative for detailed evidence.

## Current stable checkpoint

- Repository: `tiagosombrra/modelo-latex-ufc`
- Default branch: `main`
- Stable main after documentation PR `#105`: `557a4559fff2b88d17e9b5a3541c12f3e866659d`
- PR `#105` records the citation-family checkpoint after `#104`.
- Latest published release: `v2.1.0`
- Future release under audit: `v2.2.0`
- Canonical class/package identity: `abntexto-ufc`
- Legacy class entry point: deprecated compatibility shim only; outside the canonical CTAN package.
- UFC institutional mark: externalized from public/CTAN bundles; users may supply an official local asset through the supported class option.

## Roadmap identity and correction of phase-label drift

The canonical normative roadmap is N0–N15 with distinct phase meanings. During the bounded final-PDF evidence campaign, the label `N6` was temporarily reused in scripts, fixture names, structured log prefixes and handoff prose as a generic evidence namespace. That execution-label drift did **not** redefine the roadmap.

The correct phase mapping is:

- N0 — freeze/baseline;
- N1 — normative sources and locators;
- N2 — UFC/current-ABNT reconciliation;
- N3 — atomicity gaps;
- N4 — atomic coverage / false-coverage control;
- N5 — final-PDF oracle construction and calibration;
- N6 — pre-textual elements;
- N7 — layout, pagination, sections and footnotes;
- N8 — citations and references;
- N9 — objects, tables, equations and code;
- N10 — post-textual elements and multivolume;
- N11 — research-project profile / NBR 15287;
- N12 — profile, engine and font matrix;
- N13 — negative fixtures / negative-path validation;
- N14 — Web/Lite and CLI/Deep unification;
- N15 — full normative certification and release decision.

Historical filenames such as `n6-*` and log strings such as `N6-EVIDENCE` remain valid evidence identifiers and must not be rewritten merely to relabel history. New work must use the canonical roadmap phase in PR titles, handoff status and new structured evidence identifiers.

## Governing method

The audit must not equate green CI with normative proof. Conservative policy remains in force:

- no rule is promoted to `PROVEN` merely because an aggregate check passes;
- unavailable authoritative/licensed clause text remains unavailable or partial;
- measured final-PDF conformance does not change proof-state;
- evidence-only PRs do not change normative values, locators, N5 tolerances or compatibility mappings;
- implementation defects exposed by evidence are corrected separately while the evidence predicate remains unchanged;
- fixture observations must not strengthen stored predicates;
- broad regression checks do not count as phase-specific bounded evidence unless the exact phase predicate is explicitly measured;
- merge evidence only on the exact audited head with `behind_by=0`;
- after each bounded evidence merge, update this handoff before creating the next evidence branch.

## Operational progress metric

Progress percentages below are **execution-planning metrics**, not percentages of legal/normative conformity and not proof-state scores.

The N0–N15 roadmap is assigned fixed planning weights totaling 100 points:

| Phase | Weight |
| --- | ---: |
| N0 | 3 |
| N1 | 8 |
| N2 | 5 |
| N3 | 6 |
| N4 | 6 |
| N5 | 8 |
| N6 | 10 |
| N7 | 10 |
| N8 | 10 |
| N9 | 10 |
| N10 | 6 |
| N11 | 4 |
| N12 | 5 |
| N13 | 4 |
| N14 | 2 |
| N15 | 3 |
| **Total** | **100** |

Rules for the percentage:

1. a DONE phase contributes 100% of its weight;
2. an active/partially executed phase is calculated from explicitly mapped atomic phase scope with bounded evidence closed / total mapped scope;
3. generic pre-existing regression tests do not increase the percentage until re-audited against the phase predicate;
4. PENDING phases remain 0% even if supporting infrastructure already exists;
5. weights are frozen for v2.2.0 unless an explicit roadmap rebaseline PR changes them.

Current weighted progress:

- N0–N6 DONE contribution: `46.0` points;
- N7: `15/34 = 44.1%` → `4.4` weighted points;
- N8: `12/18 = 66.7%` → `6.7` weighted points;
- N9–N15: `0.0` weighted points until formally entered and mapped;
- **total normative-roadmap execution: 57.1% complete**;
- **remaining normative-roadmap execution: 42.9%**.

This metric must be updated in every canonical handoff checkpoint when the mapped phase numerator changes.

## Phase status and percentages

| Phase | Canonical scope | Status | Progress | Remaining |
| --- | --- | --- | ---: | ---: |
| N0 | freeze / baseline | DONE | 100% | 0% |
| N1 | sources + locators | DONE | 100% | 0% |
| N2 | UFC × current ABNT reconciliation | DONE | 100% | 0% |
| N3 | atomicity gaps | DONE | 100% | 0% |
| N4 | atomic coverage / false-coverage control | DONE | 100% | 0% |
| N5 | final-PDF oracle | DONE | 100% | 0% |
| N6 | pre-textual elements | DONE | 100% | 0% |
| **N7** | **layout + pagination + sections + footnotes** | **IN PROGRESS / ACTIVE** | **44.1%** | **55.9%** |
| N8 | citations + references | PARTIALLY EXECUTED / PAUSED UNTIL N7 CLOSES | 66.7% | 33.3% |
| N9 | objects + tables + equations + code | PENDING | 0% | 100% |
| N10 | post-textual + multivolume | PENDING | 0% | 100% |
| N11 | projects / NBR 15287 | PENDING | 0% | 100% |
| N12 | profiles + engines + fonts | PENDING | 0% | 100% |
| N13 | negative fixtures | PENDING | 0% | 100% |
| N14 | Web/Lite + CLI/Deep unification | PENDING | 0% | 100% |
| N15 | full certification + release decision | PENDING | 0% | 100% |

## Normative baseline after N5

Historical baseline; do not recompute or rewrite without an explicit proof-state phase/change.

- full atomic rules: 181
- normative rules: 170
- N1 locator coverage: 170/170
- N2 unknown review relationships: 0
- N3 gaps resolved: 46/46
- N4 unsafe `PROVEN`: 0
- historical proof-state baseline: `PARTIAL=114`, `NOT_PROVEN=51`, `CONDITIONAL=10`, `MANUAL=5`, `NOT_APPLICABLE=1`, `PROVEN=0`

## N5 final-PDF oracle policy

Tools: `pdftotext -bbox-layout`, `pdftohtml -xml -zoom 1.0`, `pdfinfo`, `pdffonts`.

Tolerances remain unchanged:

- page size: `1 pt`
- horizontal position: `5 pt`
- vertical position: `5 pt`
- font size: `1 pt`

Major checkpoints:

- N1: PR `#55` — 170/170 locator coverage.
- N2: PR `#56` — reconciliation complete.
- N4: PR `#57` — parent/local promotion policy and `unsafe-proven=0`.
- N5: PR `#58` — final-PDF oracle calibrated and integrated.

## N6 — pre-textual elements — DONE

The bounded evidence increments that close the canonical N6 phase are:

| Scope | PR / result |
| --- | --- |
| Dedication + epigraph | `#59/#60/#61`; real class divergences fixed in #60; final evidence passed |
| Acknowledgements | `#62`, `PASS=8` |
| Summary / abstract / keywords | `#63`, `PASS=14` |
| Cover | `#64`, `PASS=4` |
| Title page + nature block/project surfaces | `#65`, `PASS=7` |
| Approval | `#67`, `PASS=2` |
| Errata | `#69`, `PASS=3` |
| Optional lists | `#71`, `PASS=4` |
| TOC | `#73`, `PASS=5` |
| Pre-textual pagination/start-side transition | `#75`, `PASS=4` |

The title-page scenario explicitly includes `nature.line-spacing` and `nature.block.alignment`; they are therefore not residual N7 work.

## N7 — layout, pagination, sections and footnotes — ACTIVE

Mapped N7 atomic scope: **34 rules**. Closed with dedicated bounded evidence: **15 rules**. Current phase completion: **44.1%**.

### N7 sub-scope map

| Sub-scope | Closed / total | Status | Evidence / remaining |
| --- | ---: | --- | --- |
| Sections | `10/10` | CLOSED | #77, #79/#80, #82, #84, #86, #88, #90 |
| Body paragraph | `2/2` | CLOSED | #92; 20 mm indent and 0 pt extra paragraph spacing measured |
| Pagination core | `3/9` | PARTIAL | #75 closes counted-not-numbered, catalog exception and textual display start; recto/verso position/offset rules remain |
| Page size + recto/verso margins | `0/9` | OPEN | broad geometry regressions exist, but no bounded phase-specific evidence closure yet |
| Body line spacing | `0/1` | OPEN | dedicated final-PDF bounded evidence still required |
| Footnotes | `0/3` | OPEN | line spacing, 5 cm separator and hanging alignment still require bounded phase-specific treatment |
| **Total** | **15/34** | **ACTIVE** | **19 rules remain** |

Rules intentionally assigned to N10 rather than N7: `pagination.multivolume.continuous` and `pagination.appendix-annex.continuous`.

### N7 completed evidence ledger

- section hierarchy — `#77`, `PASS=3`;
- section indicators — `#79/#80`; real separator defect corrected; final 3.0 pt gap matched calibration;
- primary section recto duplex — `#82`; primary pages 1,3,5;
- primary after-spacing — `#84`; 41.55 pt vs 41.40 pt calibration;
- subsection spacing — `#86`, `PASS=1`;
- multiline hanging — `#88`; five levels, 10 continuation lines, max delta 0.9 pt;
- unnumbered heading centering — `#90`; max delta 0.2162 pt;
- body paragraph — `#92`; 20 mm measured 56.6930 pt; extra spacing 0.0 pt.

### N7 remaining work order

Use smallest independently measurable scope first:

1. `footnotes.line-spacing` → `footnote.line-spacing`;
2. `footnotes.separator` → `footnote.separator.length`;
3. `footnotes.hanging-alignment` → `footnote.hanging-alignment`;
4. `layout.body-spacing` → `spacing.body`;
5. `layout.page-a4` → `page.a4`;
6. `layout.margin-recto` → four recto margin rules;
7. `layout.margin-verso` → four verso margin rules;
8. pagination recto position/top/right offsets;
9. pagination verso position/top/left offsets;
10. N7 closure reconciliation/checkpoint.

`footnotes.hanging-alignment` currently has locator status `UNAVAILABLE_WITH_REASON`; measuring implementation behavior must not upgrade that locator or proof-state.

## N8 — citations and references — 66.7%, PAUSED

N8 was partially executed ahead of formal N7 closure because of the phase-label drift. The evidence is valid and retained; execution order is now restored by pausing additional N8 increments until N7 closes.

Mapped N8 atomic scope: **18 rules**.

- citations: `12/12` closed with dedicated bounded evidence;
- references: `0/6` closed with dedicated phase-specific bounded evidence;
- total: `12/18 = 66.7%`.

Citation evidence already closed:

- long direct quotation → `#94`;
- short direct citation → `#96`;
- direct citation source → `#98`;
- indirect citation source → `#100`;
- UFC author-date system → `#102`;
- citation of citation (`apud`) → `#104`.

All six dedicated rulesets in `normativa/locator-audit-citations.json` therefore have bounded evidence. This does not promote proof-state.

Reference residual after N7:

- `references.layout`: 4 atomic rules;
- `references.doi`: 1 atomic rule;
- `references.online-access`: 1 atomic rule.

Broad bibliography/reference regressions already exist, but they do not count as bounded N8 closure until re-audited against these exact predicates.

Latest N8 citation increment: `#104`, squash merge `84e57059795da7927466d6834e733b1d61800631`, exact audited head `c20f1079640fd57329d07e0b9e7b05cb7ff95407`, `apud` result `PASS=1`, 2/2 supported surfaces. Documentation checkpoint `#105` was merged as `557a4559fff2b88d17e9b5a3541c12f3e866659d`.

## N9–N15 remaining roadmap

These phases have not been formally entered under the bounded phase-closure method. Existing supporting tests are prerequisites/regressions and do not by themselves change phase progress from 0%.

### N9 — objects, tables, equations and code

Expected families already visible in the contract/locator graph include illustration presentation/bounds/source, list routing, IBGE table presentation, equation presentation and project-policy code/algorithm capabilities. Re-derive exact N9 scope only after N8 closure.

### N10 — post-textual elements and multivolume

Includes post-textual presentation and the pagination continuity rules intentionally excluded from N7: multivolume continuity and appendix/annex continuity.

### N11 — research projects / NBR 15287

Re-audit project structure and project-specific behavior against the current NBR 15287:2025 source state. Exact authoritative clauses currently unavailable remain unavailable unless new authoritative evidence is introduced.

### N12 — profiles, engines and fonts

Certify the profile/engine/font matrix, literal fonts where applicable, embedding and PDF/A behavior. Existing profile matrix/Windows/Overleaf checks are prerequisites and must be mapped explicitly before N12 completion can advance.

### N13 — negative fixtures

Exercise malformed/unsupported/nonconforming cases and verify that validators fail for the intended reason without false positives/false coverage.

### N14 — Web/Lite and CLI/Deep unification

Reconcile rule inventory, semantics and outputs across validator execution surfaces so equivalent predicates do not diverge by interface.

### N15 — full normative certification and release decision

Run the final whole-tree certification, reconcile all phase ledgers, proof-state limits, release blockers and residual manual/conditional items, and make the explicit v2.2.0 release decision. N15 approval is the prerequisite for final D5.

## Weighted remaining work

At this checkpoint, the remaining **42.9 planning points** are distributed as:

| Remaining source | Weighted points remaining |
| --- | ---: |
| N7 residual | 5.6 |
| N8 residual | 3.3 |
| N9 | 10.0 |
| N10 | 6.0 |
| N11 | 4.0 |
| N12 | 5.0 |
| N13 | 4.0 |
| N14 | 2.0 |
| N15 | 3.0 |
| **Total remaining** | **42.9** |

## Required PR discipline

Every bounded audit PR must record:

- canonical roadmap phase;
- stable base SHA;
- exact audited head SHA;
- complete exact rule scope;
- fixture/measurement strategy;
- workflow/job IDs;
- structured phase evidence summary (`N7-EVIDENCE`, `N8-EVIDENCE`, etc. for new work);
- explicit statement about normative values, locators, N5 tolerances, compatibility mappings and proof-state.

Merge only on the unchanged audited head with `behind_by=0`, then update this handoff before starting the next bounded increment.

## CTAN / distribution state

Technical blockers already remediated for v2.2.0:

- canonical package/class identity is `abntexto-ufc`;
- legacy identity remains only through compatibility surface outside the canonical CTAN package;
- UFC coat of arms is externalized from public/CTAN archives;
- CTAN archive is limited to canonical runtime, essential documentation and portable example;
- archive/asset identity guards and allowlists are present;
- D5 distribution rehearsal exists in PR `#36`.

D-track status:

- D0–D4: DONE / 100%;
- D5 rehearsal: VALIDATED / rehearsal complete, not a release decision;
- D5 final: 0% and BLOCKED by N15;
- D6 CTAN resubmission: 0% and BLOCKED by final D5.

Do not tag or publish v2.2.0 from the rehearsal.

## M1 state

Implementation is complete through PR `#19`: Node 24 migration, `configure-pages` v6, `upload-pages-artifact` v5, `deploy-pages` v5, and repository `has_pages=true`.

M1 remains `IMPLEMENTED`, not formally `DONE`, until explicit Pages/runtime/deployment evidence is reviewed and recorded. Track M1 separately from the N0–N15 weighted percentage.

## Open release-adjacent items

- PR `#36` remains D5 distribution rehearsal only.
- Issue `#18` remains open for bit-reproducible PDF differences (`CreationDate`, `ModDate`, PDF `/ID`) although pages/text/fonts/images were identical; reassess release-blocking status under the final public bundle policy.
- D5 final remains blocked by N15.
- D6 CTAN resubmission remains blocked by final D5.

## How to resume

Read, in order:

1. this file;
2. current `main` SHA and open PRs;
3. latest bounded audit PR body/comments and exact-head workflow runs;
4. current full contract, relevant phase locator ruleset and N5 oracle policy for the next scope.

Do not reconstruct state primarily from old chats.

## Immediate next action

1. merge this roadmap/progress correction checkpoint only if CI is green, exact head is unchanged and `behind_by=0`;
2. from the resulting stable `main`, start N7 `footnotes.line-spacing` as the smallest residual bounded scope;
3. preserve the stored predicate `factor=1.0` and locator state; measure final-PDF line spacing only;
4. if the measurement exposes a class/runtime defect, keep the evidence FAIL and correct implementation separately;
5. after evidence merge, update this handoff, increasing N7 from `15/34` to `16/34` and recomputing weighted progress before the next N7 increment.
