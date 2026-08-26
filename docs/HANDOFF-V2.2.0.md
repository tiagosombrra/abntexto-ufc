# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-26
Checkpoint PR: #120
Stable base before this PR: `082bc033b86465cb375ca3c90b6ed812de430b7c`

This is the single dynamic continuation document for the v2.2.0 normative audit and release. Future work must read this file before relying on chat history. Detailed evidence belongs in `normativa/`, `tests/`, Git history, pull requests and Actions logs.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable requirements, locators, precedence and proof policy.
2. `tests/` + GitHub Actions — executable evidence and regressions.
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

A green CI job, positive fixture or closed phase does not by itself promote a rule to `PROVEN`.

Guardrails:

- unavailable authoritative/licensed text stays unavailable or partial;
- evidence-only work does not silently change normative values, locators, tolerances or compatibility mappings;
- fixture observations do not strengthen stored predicates;
- broad regressions are support-only until mapped to exact predicates;
- implementation defects exposed by evidence are fixed separately while preserving the predicate;
- evidence merges require the exact audited head and `behind_by=0`;
- no closed scope is reopened without changed source, changed predicate or regression.

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
| N10 | post-textual elements and multivolume | ACTIVE — 2/20 bounded positive, 18 support-only after reconciliation |
| N11 | research-project profile / NBR 15287 | PENDING |
| N12 | profile, engine and font matrix | PENDING |
| N13 | negative fixtures / negative-path validation | PENDING |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure is **10/16 phases = 62.5%**. N10 remains active, so this percentage does not advance until N10 closes. This is a phase-gate metric, not a conformity or proof percentage.

## Frozen baseline and oracle policy

- full atomic rules: 181;
- normative rules: 170;
- N1 locator coverage: 170/170;
- N2 unknown-review relationships: 0;
- N3 explicit gaps resolved/classified: 46/46;
- N4 unsafe `PROVEN`: 0;
- proof-state baseline: `PARTIAL=113`, `NOT_PROVEN=51`, `CONDITIONAL=10`, `MANUAL=6`, `NOT_APPLICABLE=1`, `PROVEN=0`.

Core N5 tools remain:

- `pdftotext -bbox-layout`;
- `pdftohtml -xml -zoom 1.0`;
- `pdfinfo`;
- `pdffonts`.

Frozen N5 tolerances remain unchanged:

- page size: 1 pt;
- horizontal position: 5 pt;
- vertical position: 5 pt;
- font size: 1 pt.

N9 added one calibrated N5 extension without changing those tolerances:

- capability: `vector-rule-geometry`;
- tool: `pdftocairo -svg`;
- no rasterization;
- same-run calibration required before predicate evidence.

## Closed phase notes

### N6 — pre-textuals — DONE

The pre-textual work map is reconciled. Manual/conditional boundaries remain explicit, including catalog-card font sizing, approval signatures and CAPES applicability. Research-project observations remain support-only for N11.

### N7 — layout, pagination, sections and footnotes — DONE

Closed at **39/39 bounded positive coverage**. Literal Arial/Times New Roman identity is certified by the Windows path rather than inferred from Linux fallback fonts.

### N8 — citations and references — DONE

Closed at **19/19 bounded positive coverage**. DOI and online-access evidence remains positive-applicability evidence; unavailable licensed NBR 6023:2025 clause text was not promoted to `PROVEN`. General DOI/URL formatting remains delegated to `biblatex-abnt`.

### N9 — objects, tables, equations and code — DONE

N9 was rederived from the 181-rule contract as an exact **23-predicate** work map and closed at **23/23 bounded positive coverage**.

Progression:

- PR #116: scope reconciliation — `7/23 bounded + 16/23 support-only`;
- PR #117: illustration final-PDF evidence — `15/23`;
- PR #118: table typography + `equation.display` — `18/23`;
- PR #119: five residual `table.ibge.*` predicates — `23/23`.

PR #119 final audited head `3b5ae944fec35015dab7cef4877b072582817a97` passed Normative source contract #238 and LaTeX preflight #846 with `behind_by=0`, then squash-merged as `082bc033b86465cb375ca3c90b6ed812de430b7c`.

The calibrated vector campaign identified exactly three logical horizontal IBGE rules and no vertical rules; open sides, absent body grid, top rule, header rule and bottom rule all passed. Proof-state remained unchanged.

## N10 — post-textual elements and multivolume — ACTIVE

PR #120 machine-rederived N10 from the current full contract and locator manifests as exactly **20 predicates**:

- 17 post-textual predicates covering appendix, annex, index, glossary and appendix/annex identification;
- `pagination.multivolume.continuous`;
- `pagination.appendix-annex.continuous`;
- `volume.number.cover-title-page`.

The conservative baseline is **2/20 bounded positive + 18/20 support-only**:

- `volume.number.cover-title-page`: existing final-PDF oracle explicitly requires the volume marker on both cover and title page;
- `pagination.multivolume.continuous`: existing multivolume gate explicitly checks logical progression `101 → 102 → 102` and rejects invalid `pagina-inicial=0`.

Broad post-textual presence/order and duplex-start regressions remain support-only. They are not promoted merely because CI is green.

PR #120 structured reconciliation evidence requires and currently reports:

- `total=20`;
- `existing_bounded_positive=2`;
- `support_only=18`;
- two disjoint residual campaigns covering exactly `13 + 5` rules;
- post-textual and pagination locator states remain `PARTIAL_WITH_REASON`;
- proof-state unchanged.

Residual campaigns:

1. `appendix-annex-final-pdf` — 13 rules: five appendix heading/page predicates, five annex heading/page predicates, both identification patterns, and appendix→annex pagination continuity.
2. `index-glossary-final-pdf` — 5 rules: four index-heading predicates plus glossary optionality using controlled present/absent routes.

Do not promote locator proof-state while closing these campaigns; the current authoritative-text limitations remain in force.

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

The UFC institutional mark remains in the source repository but is **externalized from public/CTAN bundles**; do not describe it as removed from the repository.

## PR discipline

For roadmap PRs:

1. branch from exact stable `main`;
2. derive exact bounded rule IDs from the current contract;
3. add only required scenario/fixture/checker/gate changes;
4. validate source contract and CI;
5. require final head unchanged and `behind_by=0`;
6. squash merge using `expected_head_sha`;
7. update this handoff only when roadmap state or next action materially changes.

## Next action

Finish PR #120 on its final documentation-updated head. Require exact-head Normative source and LaTeX preflight success, the structured N10 reconciliation line `total=20 existing_bounded_positive=2 support_only=18`, and `behind_by=0`; then squash merge.

After #120 merges, create `audit/n10-appendix-annex-final-pdf-evidence` from the new stable `main` and execute only the 13-rule `appendix-annex-final-pdf` campaign. Use an isolated controlled final-PDF fixture and existing N5 bbox/typography tooling. Derive every expected value from the current contract before implementing assertions; do not infer or strengthen unstored formatting details.

After that campaign, execute the 5-rule `index-glossary-final-pdf` campaign. Only when N10 reaches 20/20 bounded positive coverage may N10 be marked DONE and N11 become active.
