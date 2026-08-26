# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-26
Checkpoint PR: #118
Audited stable base: `d8b16041d6273933459e01ec88bdd1276efe85c6`

Key closure/evidence merges:

- N6 technical closure head: `5d1d9ba4aecba5519b600bfba4114009f551ea52`
- N7 technical closure merge: `555b538d7ef05eebfde88a3a3f1e92961f605019`
- N8 reduced-size mapping merge: `61738858d32ab1aea677832e9063fd01ad2b1d1a`
- N8 reference-layout merge: `81d1f42296c1b52222c53f273520475e5d162ba8`
- N8 semantic-closure merge: `2881b88ce1c0d334ecaaab1d4c7b884343f3a313`
- N9 scope-reconciliation merge: `803dba0ebfe3450a5ccf77a6cf14e87cdd16b6a6`
- N9 illustration-evidence merge: `d8b16041d6273933459e01ec88bdd1276efe85c6`

This is the single dynamic continuation document for the v2.2.0 audit and release. Future work must read this file before relying on chat history. Detailed implementation evidence remains in Git history, pull requests, Actions runs, `normativa/` and `tests/`.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable requirements, source status, locators, precedence and proof policy.
2. `tests/` and GitHub Actions — executable evidence and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. this handoff — roadmap state, audit decisions and next action.
6. Git/PR/Actions history — detailed historical evidence.

Historical release audits live under `docs/history/`. Distribution-only documents remain `docs/README-CTAN.md`, `docs/CHANGELOG-CTAN.md` and `docs/ctan-example.tex`.

## Governing audit policy

Keep three states separate:

- **positive coverage**: an exact predicate was exercised/measured;
- **phase gate**: all exit criteria of that roadmap phase were reconciled;
- **proof-state**: normative confidence classification under `normativa/proof-policy.json`.

A green CI job, positive fixture or closed phase does not by itself promote a rule to `PROVEN`.

Mandatory guardrails:

- unavailable authoritative/licensed text stays unavailable or partial;
- evidence-only work does not silently change normative values, locators, N5 tolerances or compatibility mappings;
- fixture observations do not strengthen stored predicates;
- broad regressions are support-only until mapped to the exact predicate;
- implementation defects exposed by evidence are fixed separately while preserving the evidence predicate;
- evidence is merged only on the exact audited head with `behind_by=0`;
- no closed scope is reopened without a changed source, changed predicate or regression.

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
| N9 | objects, tables, equations and code | ACTIVE — 18/23 bounded positive coverage on PR #118 evidence branch |
| N10 | post-textual elements and multivolume | PENDING |
| N11 | research-project profile / NBR 15287 | PENDING |
| N12 | profile, engine and font matrix | PENDING |
| N13 | negative fixtures / negative-path validation | PENDING |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure remains **9/16 phases = 56.25%** while N9 is active. This is a gate-count metric, not a conformity or proof percentage.

Historical fixture/log names containing `n6` / `N6-EVIDENCE` remain valid evidence identifiers and are not renamed merely to repair roadmap labels.

## Frozen baseline and N5 policy

- full atomic rules: 181;
- normative rules: 170;
- N1 locator coverage: 170/170;
- N2 unknown-review relationships: 0;
- N3 explicit gaps resolved/classified: 46/46;
- N4 unsafe `PROVEN`: 0;
- proof-state baseline: `PARTIAL=113`, `NOT_PROVEN=51`, `CONDITIONAL=10`, `MANUAL=6`, `NOT_APPLICABLE=1`, `PROVEN=0`;
- evidence origins: `atomic-parent=8`, `parent-inherited=91`, `rule-local-override=1`, `rule-local-promotion=81`;
- the sole `rule-local-override` remains `font.size.reduced.catalog-card`, normatively 10 pt but manually validated because the catalog card is an external PDF.

Frozen N5 tools:

- `pdftotext -bbox-layout`;
- `pdftohtml -xml -zoom 1.0`;
- `pdfinfo`;
- `pdffonts`.

Frozen N5 tolerances:

- page size: 1 pt;
- horizontal position: 5 pt;
- vertical position: 5 pt;
- font size: 1 pt.

A later vector/rule-geometry capability must be introduced as an explicit, calibrated N5 oracle extension. Do not silently treat `pdftocairo`, SVG/raster extraction or another tool as already frozen N5 capability.

## Closed phase notes

### N6 — pre-textuals — DONE

The full pre-textual work map is reconciled. Important validation boundaries remain conservative:

- `deposit.catalog-card`: enabled/disabled routes have bounded positive evidence across engines/layout modes;
- `font.size.reduced.catalog-card`: **MANUAL / external-pdf**;
- `deposit.approval-signatures`: **MANUAL** deposit evidence;
- `deposit.capes`: **CONDITIONAL** on CAPES funding;
- research-project-specific observations are support-only for N11 and did not close N11.

N6 closing changed the phase gate only and did not promote any rule to `PROVEN`.

### N7 — layout, pagination, sections and footnotes — DONE

N7 is formally closed at **39/39 bounded positive coverage**. Final campaigns include page/margin geometry, footnotes, typography and six remaining recto/verso pagination predicates. Literal Arial/Times New Roman identity remains certified by the Windows path rather than inferred from Linux TeX Gyre fallback.

PR #112 final validation used LaTeX preflight run `32968822105`; structural job `98177477428` closed `PASS=14 FAIL=0 SKIP=0` and the branch was `behind_by=0` before squash merge `555b538d7ef05eebfde88a3a3f1e92961f605019`.

### N8 — citations and references — DONE

N8 is formally closed at **19/19 bounded positive coverage**. The final semantic block covers DOI-when-present and online URL/access-date positive applicability while keeping exact licensed NBR 6023:2025 clause-text limitations conservative. `abntexto-ufc/compat-nbr6023-2025.def` remains explicitly audited: general DOI/URL formatting is delegated to `biblatex-abnt`; no global formatter override is inferred from the local jurisprudence driver.

The N8 semantic closure was squash-merged as `2881b88ce1c0d334ecaaab1d4c7b884343f3a313`. Rendered evidence closes implementation coverage and the N8 phase gate; it does not independently promote `references.layout`, `references.doi` or `references.online-access` to `PROVEN`.

## N9 — objects, tables, equations and code — ACTIVE

PR #116 rederived N9 from the full 181-rule contract and froze an exact **23-predicate** work map. The immutable baseline is **7/23 existing-bounded-positive + 16/23 support-only**. Project-policy code/algorithm capabilities remain non-normative, and TeX-log/source-structure checks do not close visual predicates.

`normativa/n9-campaign-plan.json` partitions the 16 initial residuals into:

- `illustration-final-pdf`: 8 predicates measurable with existing N5 tools;
- `table-final-pdf`: 7 predicates — 2 reduced-font predicates measurable with N5 plus 5 `table.ibge.*` vector/rule-geometry predicates requiring oracle extension;
- `equation-display-final-pdf`: 1 predicate measurable with existing N5 bbox capability.

PR #117 added bounded final-PDF evidence for all eight illustration residuals and was squash-merged as `d8b16041d6273933459e01ec88bdd1276efe85c6`. The campaign measured caption/source at exactly 10 pt, controlled 60 mm object bounds and required relative caption/source/note positions, promoting N9 to **15/23** without changing proof-state.

PR #118 adds exactly three more existing-N5 predicates:

- `font.size.reduced.table-caption`;
- `font.size.reduced.table-source`;
- `equation.display`.

First successful exact implementation head: `4ec6d202c8f1ac9fc0f50910e0637bc361fb602d`.

Validation on that head:

- Normative source contract run `32998519354`: **SUCCESS**;
- LaTeX preflight run `32998519348`: **SUCCESS**;
- object/bibliography job `98273922090`: **SUCCESS**, overall `PASS=8 FAIL=0 SKIP=0`;
- structural job `98273922031`: **SUCCESS**;
- aggregate `latex-preflight`: **SUCCESS**;
- table caption: exactly `10.0 pt`;
- table source: exactly `10.0 pt`;
- `equation.display`: **PASS**, with the equation in a distinct non-overlapping vertical band; measured positive gaps were `30.540 pt` before and `16.316 pt` after;
- equation horizontal alignment and exact vertical gaps remain observational and are not frozen into stronger predicates;
- `N9-EVIDENCE bounded-progress`: baseline 7 + promoted 11 = **18/23 current bounded-positive**, **5/23 support-only**.

Two instrumentation defects were exposed and corrected before that green run without changing the normative predicate or class implementation:

1. a JSON marker key named `source` collided with normative-source integrity scanning; it was renamed to an unambiguous marker key;
2. the first synthetic table fixture was too narrow for its marker strings and produced `Overfull \\hbox`; the fixture was widened/bounded rather than suppressing the warning.

`normativa/n9-bounded-promotions.json` keeps promotions separate from the immutable baseline. `tests/checks/normative_n9_progress.py` requires runtime PASS evidence, exact promoted rule IDs, same execution SHA, PR-preflight binding and `proof_state_changed=false` before counting a promotion.

After PR #118, the only N9 support-only predicates are:

- `table.ibge.open-sides`;
- `table.ibge.body-grid`;
- `table.ibge.top-rule`;
- `table.ibge.header-rule`;
- `table.ibge.bottom-rule`.

## Normative currency

The repository records `ABNT NBR 14724:2024`, corrected version dated 2025-04-01. Current technical-edition/precedence policy remains governed by `normativa/version-policy.json` and `docs/VIGENCIA-NORMATIVA.md`. No N1/N2 reopening is required for this point.

## M1 — validator Pages migration

M1 is **DONE**. The workflow uses Node 24 and the intended Pages actions. Main-branch run `32922391042` completed check/deploy successfully.

## Distribution / CTAN track

- D0–D4: DONE.
- D5 rehearsal: historical PR #36 only.
- D5 final: BLOCKED by N15.
- D6 CTAN resubmission: BLOCKED by final D5.

PR #36 is not the final release branch; final D5 must start from the N15-approved SHA.

Issue #18 (bit-reproducible reference PDF metadata/ID) remains open and requires an explicit blocking/non-blocking release decision before final D5.

The UFC institutional mark remains in the source repository but is **externalized from public/CTAN bundles**; do not describe it as removed from the repository.

## Documentation and PR discipline

Keep the active documentation surface small:

- `README.md` — user-facing entry point;
- `docs/NORMAS.md` — normative human map;
- `docs/VIGENCIA-NORMATIVA.md` — normative currency/precedence;
- `docs/HANDOFF-V2.2.0.md` — only dynamic roadmap/audit-state document;
- CTAN-specific docs — distribution artifacts;
- `docs/history/` — immutable archival audits.

Do not add generic progress/checkpoint/status Markdown files. Detailed evidence belongs in machine-readable files, tests, PRs and Actions logs.

For roadmap PRs:

1. branch from exact stable `main`;
2. define exact bounded rule IDs;
3. add only required scenario/fixture/checker/gate changes;
4. validate source contract and CI;
5. require final head unchanged and `behind_by=0`;
6. squash merge using `expected_head_sha`;
7. update this handoff only when roadmap state or next action materially changes.

## Next action

Finish PR #118 on the documentation-updated head. Require exact-head `Normative source contract=SUCCESS`, aggregate `latex-preflight=SUCCESS`, object/bibliography `PASS=8 FAIL=0 SKIP=0`, `N9-EVIDENCE table-typography-final-pdf-summary PASS=2 FAIL=0`, `N9-EVIDENCE equation-display-final-pdf-summary PASS=1`, bounded progress **18/23 + 5/23**, and `behind_by=0` before squash merge.

Then address the last five `table.ibge.*` predicates. Before promoting any of them:

1. define an explicit vector/rule-geometry oracle extension and add it to the N5 measurement policy only after calibration;
2. calibrate the extractor against deterministic known geometry and a retained regression control; the existing N7 footnote-separator vector path may be reused as a calibration precedent, but not silently treated as frozen N5 tooling;
3. create a bounded final-PDF IBGE fixture/checker that distinguishes top/header/bottom horizontal rules and verifies absence of side closures/body grid without inferring unrelated line widths/styles;
4. preserve current N5 positional tolerances unless calibration proves a source-level reason to change policy — do not relax tolerances to make a fixture pass;
5. register the five promotions through `normativa/n9-bounded-promotions.json` only from same-SHA runtime PASS evidence.

If all five pass, N9 reaches **23/23 bounded positive coverage** and can be formally closed. Then proceed N10 → N11 → N12 → N13 → N14 → N15 → D5 final → D6.
