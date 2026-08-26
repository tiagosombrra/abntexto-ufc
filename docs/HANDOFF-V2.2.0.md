# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-26
Checkpoint PR: #119
Audited stable base before this PR: `998289fa3b0bb7961c7b65b992f4f7974df3b432`
N9 closure candidate head: `f12ccb4dea1653a6fc6e3b00c50a842d6bf8485b`

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
| N9 | objects, tables, equations and code | DONE — 23/23 bounded positive coverage on PR #119 closure evidence |
| N10 | post-textual elements and multivolume | ACTIVE |
| N11 | research-project profile / NBR 15287 | PENDING |
| N12 | profile, engine and font matrix | PENDING |
| N13 | negative fixtures / negative-path validation | PENDING |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

After PR #119 merges, formal roadmap closure is **10/16 phases = 62.5%**. This is a phase-gate metric, not a conformity or proof percentage.

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

PR #119 adds one explicit calibrated N5 extension:

- capability: `vector-rule-geometry`;
- tool: `pdftocairo -svg`;
- no rasterization;
- same-run calibration required before predicate evidence;
- existing N5 tolerances unchanged;
- proof-state unchanged.

Calibration on PR #119 measured:

- horizontal 50 mm: expected `141.7323 pt`, measured `141.5586 pt`, delta `0.1737 pt`;
- vertical 30 mm: expected `85.0394 pt`, measured `84.9336 pt`, delta `0.1058 pt`;
- result: `PASS=2 FAIL=0`.

## Closed phase notes

### N6 — pre-textuals — DONE

The pre-textual work map is reconciled. Important conservative boundaries remain:

- `font.size.reduced.catalog-card`: MANUAL / external PDF;
- `deposit.approval-signatures`: MANUAL;
- `deposit.capes`: CONDITIONAL on CAPES funding;
- research-project-specific observations remain support-only for N11.

N6 closure did not promote proof-state.

### N7 — layout, pagination, sections and footnotes — DONE

Closed at **39/39 bounded positive coverage**. Final pagination closure was squash-merged as `555b538d7ef05eebfde88a3a3f1e92961f605019`. Literal Arial/Times New Roman identity remains certified by the Windows path rather than inferred from Linux fallback fonts.

### N8 — citations and references — DONE

Closed at **19/19 bounded positive coverage**. Semantic closure was squash-merged as `2881b88ce1c0d334ecaaab1d4c7b884343f3a313`. DOI and online-access evidence remains positive-applicability evidence; unavailable licensed NBR 6023:2025 clause text is not promoted to `PROVEN`. `compat-nbr6023-2025.def` remains explicitly audited and general DOI/URL formatting remains delegated to `biblatex-abnt`.

### N9 — objects, tables, equations and code — DONE

N9 was rederived from the 181-rule contract as an exact **23-predicate** work map.

Key progression:

- PR #116: scope reconciliation, baseline `7/23 bounded + 16/23 support-only`, squash merge `803dba0ebfe3450a5ccf77a6cf14e87cdd16b6a6`;
- PR #117: 8 illustration final-PDF predicates, reaching `15/23`, squash merge `d8b16041d6273933459e01ec88bdd1276efe85c6`;
- PR #118: table caption/source 10 pt + `equation.display`, reaching `18/23`, squash merge `998289fa3b0bb7961c7b65b992f4f7974df3b432`;
- PR #119: five residual `table.ibge.*` predicates using calibrated vector-rule geometry, reaching `23/23`.

PR #119 exact technical head `f12ccb4dea1653a6fc6e3b00c50a842d6bf8485b` validation:

- Normative source contract run `33001794807` (#236): SUCCESS;
- LaTeX preflight run `33001794787` (#844): SUCCESS;
- all five effective preflight jobs: SUCCESS;
- aggregate `latex-preflight`: SUCCESS;
- object/bibliography job `98285253002`: `PASS=8 FAIL=0 SKIP=0`;
- vector calibration: `PASS=2 FAIL=0`;
- raw IBGE vector inventory: 6 horizontal segments, 0 vertical;
- logical clustering: exactly 3 horizontal table rules, 0 vertical;
- `table.ibge.open-sides`: PASS;
- `table.ibge.body-grid`: PASS;
- `table.ibge.top-rule`: PASS;
- `table.ibge.header-rule`: PASS;
- `table.ibge.bottom-rule`: PASS;
- bounded progress: **23/23 bounded-positive, 0 support-only**;
- proof-state unchanged.

The first PR #119 attempt correctly failed because each logical table rule was emitted as two contiguous SVG segments, one per column. The instrument was fixed by clustering co-linear contiguous segments using already-declared parser limits; normative values, class implementation and N5 tolerances were not changed.

## Normative currency

The repository records `ABNT NBR 14724:2024`, corrected version dated 2025-04-01. Current technical-edition and precedence policy remains governed by `normativa/version-policy.json` and `docs/VIGENCIA-NORMATIVA.md`. No N1/N2 reopening is required at this checkpoint.

## M1 — validator Pages migration

M1 is DONE. The workflow uses Node 24 and the intended Pages actions. Main-branch run `32922391042` completed check/deploy successfully.

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

## Next action — N10

After PR #119 is revalidated and squash-merged on its documentation-updated head, start N10 from the new stable `main`.

Do not inherit an old N10 count. Rederive the exact current N10 work map from the full 181-rule contract and relevant locators/tests. N10 scope is **post-textual elements and multivolume**, including the two continuity predicates deliberately excluded from N7:

- `pagination.multivolume.continuous`;
- `pagination.appendix-annex.continuous`.

The N10 reconciliation must:

1. derive the exact N10 rule set and authority boundaries;
2. map current bounded evidence from post-textual, duplex-posttextual and multivolume gates without counting broad regression as exact predicate evidence;
3. classify residuals as existing-oracle measurable, semantic/structural, manual/conditional or requiring oracle extension;
4. preserve proof-state and N5 tolerances;
5. create the smallest coherent evidence campaigns only after the reconciliation is machine-checked.

Then proceed N11 → N12 → N13 → N14 → N15 → D5 final → D6.
