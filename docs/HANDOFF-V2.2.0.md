# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-27
Checkpoint PR: #134 — Overleaf/TeX Live 2025 hotfix in progress
Stable main before the current hotfix: `2cbd6d00318ba906e225fa37a4efb724300c3b4e`

This is the single dynamic continuation document for the v2.2.0 normative audit and release. Future work must read this file before relying on chat history. Detailed historical evidence belongs in `normativa/`, `tests/`, Git history, pull requests and GitHub Actions logs.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable requirements, locators, precedence, proof policy and phase manifests.
2. `tests/` + GitHub Actions — executable evidence, negative-path sensitivity and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. this handoff — roadmap state, audit decisions and next action.
6. Git/PR/Actions history — detailed historical evidence.

Do not create generic progress/checkpoint Markdown files. Historical release audits belong under `docs/history/`.

## Governing audit policy

Keep three states separate:

- **positive coverage**: an exact predicate was exercised/measured;
- **phase gate**: all exit criteria of a roadmap phase were reconciled;
- **proof-state**: normative confidence under `normativa/proof-policy.json`.

A green CI job, positive fixture, negative fixture or closed phase does not by itself promote a rule to `PROVEN`.

Guardrails:

- unavailable authoritative/licensed text stays unavailable or partial;
- evidence-only work does not silently change normative values, locators, tolerances or compatibility mappings;
- fixture observations do not strengthen stored predicates;
- implementation defects exposed by evidence are fixed separately while preserving the predicate;
- evidence merges require the exact audited head and `behind_by=0`;
- no closed scope is reopened without changed source, changed predicate or regression;
- in N13, a rendered-PDF fixture that fails to compile is not evidence that an oracle rejected a normative violation;
- negative fixtures are instrumentation, not new normative requirements;
- do not modify the N12-certified `.github/workflows/latex-preflight.yml` during N13 evidence work unless N12 is explicitly reopened.

## Canonical N0–N15 roadmap

| Phase | Scope | Gate status |
| --- | --- | --- |
| N0 | freeze / baseline | DONE |
| N1 | normative sources and exact locators | DONE |
| N2 | UFC × current-ABNT reconciliation | DONE |
| N3 | classify/resolve 46 explicit atomicity gaps | DONE |
| N4 | false-coverage audit and safe proof policy | DONE |
| N5 | final-PDF oracle construction/calibration | DONE |
| N6 | pre-textual elements | DONE |
| N7 | layout, pagination, sections and footnotes | DONE — 39/39 bounded positive coverage |
| N8 | citations and references | DONE — 19/19 bounded positive coverage |
| N9 | objects, tables, equations and code | DONE — 23/23 bounded positive coverage |
| N10 | post-textual elements and multivolume | DONE — 20/20 bounded positive coverage |
| N11 | research-project profile / NBR 15287 | DONE — 5/5 bounded positive coverage |
| N12 | profile, engine and font matrix | DONE — 20-cell factorized certification + orthogonality gate |
| N13 | negative fixtures / negative-path validation | ACTIVE |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure remains **13/16 phases = 81.25%**. The remaining three gates are **18.75%** of the roadmap. This is a phase-gate metric, not a normative-conformity or proof percentage.

## Frozen baseline and oracle policy

- full atomic rules: 181;
- normative rules: 170;
- N1 locator coverage: 170/170;
- N2 unknown-review relationships: 0;
- N3 explicit gaps resolved/classified: 46/46;
- N4 unsafe `PROVEN`: 0;
- proof-state baseline: `PARTIAL=113`, `NOT_PROVEN=51`, `CONDITIONAL=10`, `MANUAL=6`, `NOT_APPLICABLE=1`, `PROVEN=0`.

Frozen N5 tolerances remain unchanged:

- page size: 1 pt;
- horizontal position: 5 pt;
- vertical position: 5 pt;
- font size: 1 pt.

Core N5 tools remain `pdftotext -bbox-layout`, `pdftohtml -xml -zoom 1.0`, `pdfinfo` and `pdffonts`.

N9 added the calibrated `vector-rule-geometry` extension using `pdftocairo -svg`, no rasterization and same-run calibration. It did not change the N5 tolerances.

## Closed-phase certification notes

### N11 — research-project profile

N11 covers exactly five `project.*` predicates. The positive route remains **5/5 bounded positive coverage**. NBR 15287 locator limitations remain explicit and proof-state was not promoted by the positive campaign.

### N12 — compatibility matrix

N12 is closed as a factorized 20-cell certification:

- six profiles × two engines = 12 cells;
- portable `times`/`arial` × pdfLaTeX/LuaLaTeX = 4 cells;
- literal Windows Times New Roman/Arial × pdfLaTeX/LuaLaTeX = 4 cells.

The static orthogonality gate verifies that profile and font-family selection are independent axes. Literal Windows identity is certified only on the Windows route, never inferred from Linux fallback fonts.

The certified workflow blob `.github/workflows/latex-preflight.yml` remains SHA `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## N13 — negative fixtures / validator sensitivity — ACTIVE

N13 tests validator sensitivity and does not create a second normative specification.

### Stable-main evidence already merged

PR #127 established the generic temporary-mutation harness and three controlled negative cases:

1. `page-margins-right` → `margin.recto.right`;
2. `short-direct-citation-quotes` → `citation.direct-short.quotation-marks`;
3. `ibge-table-open-sides` → `table.ibge.open-sides`.

PR #128 added the fourth controlled case and hardened evidence ordering in the N11 observer:

4. `project-required-resources` → `project.textual.required-sections`.

PR #128 final exact head was `e7c69a4d974779bde5b04f71cf9b97b9f6cdc76c`, squash-merged as `9fee7c4b760bf4aaee5615f63e6b7e5f58e549a2`. Stable-main preflight #895 / run id `33058717022` was fully green, including Overleaf and Windows literal-font certification.

Current stable mechanism state before the pending typography port:

- `final-pdf-geometry` — REPRESENTED;
- `citation-quotation-presentation` — REPRESENTED;
- `vector-rule-geometry` — REPRESENTED;
- `semantic-structural-observers` — REPRESENTED;
- `text-typography-extraction` — prepared in PR #130 but not yet merged;
- `configuration-strict-rejection` — pre-existing behavior exists, but still needs machine-bound N13 receipt/evidence;
- `pdf-pdfa-validation` — pending controlled structurally valid non-conformity and validator-specific rejection evidence.

### PR #130 — typography negative path

PR #130, branch `audit/n13-typography-negative-path`, remains open and draft on stale base. Its preserved head is `7e830dd4f5bb732fa98b20a6020a0e1158c50ec6`.

It adds the fifth controlled negative case:

5. `body-font-size` — temporarily renders `UFCNSevenBodyAlpha` at 14 pt, requires successful pdfLaTeX compilation, and requires `normative_typography.py` to reject `font.size.body` with `N7-EVIDENCE rule=font.size.body status=FAIL`.

The PR also adds the campaign adapter `tests/checks/normative_n13_campaign.py`. Its `runpy` binding was corrected to modify the loaded executor function's actual `__globals__`, not merely the dictionary returned by `runpy.run_path()`.

Do not merge #130 on its stale ancestry. After the current stable-main hotfix is complete, port only its three functional deltas onto the new stable main, rerun exact-head source/preflight CI, require `behind_by=0`, then merge.

### Remaining N13 sequence

After typography is stable-main evidence:

1. machine-bind `configuration-strict-rejection` using structured receipt/evidence from the existing strict font checks;
2. implement host-side PDF/A negative validation using a structurally readable PDF with controlled XMP non-conformity and veraPDF-specific rejection evidence;
3. rederive the complete mechanism inventory;
4. close N13 only if every declared mechanism is represented or explicitly reconciled;
5. only then advance to N14.

## Editorial v2.2 reference guide

PR #133 converted the v2.2 reference PDF into the commented UFC academic-work guide while preserving class behavior and normative values.

Final exact head before merge: `ba3dcc053c10f7ce926348d4c3729d13c478e746`.

Exact-head PR validation:

- Normative source contract run #309 / id `33075329551`: SUCCESS;
- LaTeX preflight #931 / id `33075329213`: SUCCESS;
- reference/PDF-A: SUCCESS;
- 12 profile PDFs/PDF-A: SUCCESS;
- objects/bibliography: SUCCESS;
- post-textuals: SUCCESS;
- structural suite: 14/14 SUCCESS;
- aggregate `latex-preflight`: SUCCESS.

PR #133 squash-merged as stable main `2cbd6d00318ba906e225fa37a4efb724300c3b4e`.

During PR validation, the repository auditor exposed a false positive because `TODO_PATTERN` used case-insensitive matching and therefore interpreted ordinary Portuguese `todo` as technical `TODO`. The auditor was corrected to recognize only explicit uppercase work markers; guide prose was not rewritten to bypass the detector.

## Current compatibility blocker — PR #134

The full stable-main post-#133 preflight #933 / run id `33076301572` isolated one compatibility regression:

- reference document/PDF-A — SUCCESS;
- 12 profile matrix/PDF-A — SUCCESS;
- objects/bibliography — SUCCESS;
- post-textuals — SUCCESS;
- structure — SUCCESS;
- Windows literal Times/Arial build — SUCCESS;
- Windows literal-font certification — SUCCESS;
- Overleaf stable proxy / LuaLaTeX / TeX Live 2025 — FAILURE;
- aggregate gate — FAILURE only because of the Overleaf proxy.

The Overleaf failure is a single `Overfull \\hbox` of **0.21825 pt** while printing the CAPES Portaria nº 206/2018 URL. pdfLaTeX / TeX Live 2025 passes.

PR #134 was opened to diagnose and fix only that issue. A temporary PR-only TeX Live 2025 diagnostic workflow identified the exact offending URL and was then removed from the branch; it must not enter `main`.

The bibliography now points `capes2062018` to the official CAPES administrative-act catalog entry instead of the longer direct-file URL. The permanent N12 workflow remains untouched.

PR #134 is not ready for merge until the final branch head passes its normal PR CI and the exact Overleaf proxy is revalidated on a route that executes TeX Live 2025. After merge, run the full stable-main preflight and require Overleaf + Windows certification to be green before resuming N13.

## Normative currency

The repository records `ABNT NBR 14724:2024`, corrected version dated 2025-04-01. Current-edition and precedence policy remains governed by `normativa/version-policy.json` and `docs/VIGENCIA-NORMATIVA.md`. No N1/N2 reopening is required at this checkpoint.

## M1 — validator Pages migration

M1 is DONE. The workflow uses Node 24 and the intended Pages actions.

## Distribution / CTAN track

- D0–D4: DONE;
- D5 rehearsal: historical PR #36 only;
- D5 final: BLOCKED by N15;
- D6 CTAN resubmission: BLOCKED by final D5.

Issue #18, bit-reproducible reference PDF metadata/ID, remains open and requires an explicit blocking/non-blocking release decision before final D5.

The UFC institutional mark remains in the source repository but is externalized from public/CTAN bundles; do not describe it as removed from the repository.

## PR discipline

For roadmap PRs:

1. branch from exact stable `main`;
2. derive exact bounded rule IDs, matrix cells or validator-mechanism cells from the current contract/implementation;
3. add only required scenario/fixture/checker/gate changes;
4. validate source contract and CI;
5. require final head unchanged and `behind_by=0`;
6. squash merge using `expected_head_sha`;
7. inspect the full stable-main push, including Overleaf and Windows literal fonts when applicable;
8. update this handoff whenever roadmap state, stable-main evidence or the immediate next action materially changes.

## Immediate next action

1. finish PR #134 on its final non-diagnostic head;
2. verify the short official CAPES catalog URL removes the LuaLaTeX / TeX Live 2025 overflow without suppressing warnings;
3. require normal PR source/preflight CI green and `behind_by=0`;
4. squash-merge #134 using the exact expected head;
5. run and inspect the full stable-main preflight, including Overleaf and Windows literal-font certification;
6. only after stable main is fully green, port PR #130's three functional typography-negative deltas onto the new stable main;
7. validate and merge the N13 typography negative path;
8. continue with configuration-strict evidence, PDF/A negative evidence and final N13 reconciliation;
9. advance to N14 only after N13 closure.
