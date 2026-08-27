# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-27
Checkpoint PR: #128
Stable main: `a1dfd9a179c768bde63a2bf9055af2c1fd142cad`

This is the single dynamic continuation document for the v2.2.0 normative audit and release. Future work must read this file before relying on chat history. Detailed evidence belongs in `normativa/`, `tests/`, Git history, pull requests and Actions logs.

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
- broad regressions are support-only until mapped to exact predicates;
- implementation defects exposed by evidence are fixed separately while preserving the predicate;
- evidence merges require the exact audited head and `behind_by=0`;
- no closed scope is reopened without changed source, changed predicate or regression;
- in N13, a fixture that fails to compile is **not** evidence that an oracle rejected a normative violation;
- negative fixtures are test instrumentation, not new normative requirements.

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
| N13 | negative fixtures / negative-path validation | ACTIVE — 4 controlled negative cases; residual mechanism reconciliation pending |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure remains **13/16 phases = 81.25%**. The remaining three gates are **18.75%** of the roadmap. N13 activity does not count as phase closure until its mechanism inventory is fully reconciled. This is a phase-gate metric, not a conformity or proof percentage.

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

### N6–N8

- N6 pre-textual work map is reconciled; manual/conditional boundaries remain explicit.
- N7 closed at **39/39 bounded positive coverage**. Literal Arial/Times New Roman identity is certified by the Windows path, not inferred from Linux fallback fonts.
- N8 closed at **19/19 bounded positive coverage**. Unavailable licensed NBR 6023:2025 clause text remains unavailable and no DOI/URL observation was promoted to `PROVEN`.

### N9 — objects, tables, equations and code — DONE

Closed at **23/23 bounded positive coverage** through PRs #116–#119. PR #119 final audited head `3b5ae944fec35015dab7cef4877b072582817a97` passed exact-head source/preflight CI with `behind_by=0`, then squash-merged as `082bc033b86465cb375ca3c90b6ed812de430b7c`.

The calibrated vector-rule extension uses `pdftocairo -svg`, same-run calibration and no rasterization.

### N10 — post-textual elements and multivolume — DONE

Machine-rederived as exactly **20 predicates** and closed at **20/20 bounded positive coverage**:

- PR #120: baseline `2/20 bounded + 18/20 support-only`, merge `17c8e22337f861127bf6bb07efa8bf9602010a49`;
- PR #121: 13-rule appendix/annex final-PDF campaign → `15/20`, merge `509b04c08d0fa3be469d32c0ed5a856f76e5422c`;
- PR #122: 5-rule index/glossary final-PDF campaign → `20/20`, final head `de172c297594ded28b2833d95065b45377dbfd33`, merge `dc964740e0200483c3327c760f820e6f30f12d6a`.

The observed index title remains observational only; glossary optionality is exercised on present/absent routes; proof-state is unchanged.

### N11 — research-project profile / NBR 15287 — DONE

Exact scope is five `project.*` predicates:

Normative NBR 15287:2025:

- `project.cover.optional`;
- `project.title-page.required`;
- `project.textual.required-sections`.

Internal profile/policy:

- `project.final-work-elements.excluded`;
- `project.anonymization.policy`.

The NBR 15287 locator remains `UNAVAILABLE_WITH_REASON`; positive coverage therefore remains separate from proof-state.

PR #123 established the machine-derived scope and live N6 evidence chain. PR #124 closed the two residual final-PDF predicates and squash-merged as `34a723c33d6779fb8a4476c7e4d94f610e19e129`. N11 closure did not change proof-state.

### N12 — profile, engine and font matrix — DONE

N12 is a compatibility/certification phase and did not reopen N7/N11 predicates.

PR #125 introduced:

- `normativa/n12-matrix-reconciliation.json`;
- `tests/checks/normative_n12_matrix.py`;
- mandatory invocation from `tests/v2-normative-complement-check.sh`.

The certified model is deliberately factorized rather than a redundant 24-cell full cross-product:

1. **profile × engine** — six supported profiles × two engines = 12 cells, including PDF/A-2b;
2. **portable font family × engine** — `times`/`arial` × `pdflatex`/`lualatex` = 4 cells;
3. **literal Windows font family × engine** — Times New Roman/Arial × pdfLaTeX/LuaLaTeX = 4 cells.

Total: **20 certification cells**.

The static orthogonality gate verifies that profile selection and font-family selection remain independent implementation axes before the marginal grids are accepted as certification of the cross-product. Literal Windows font identity is never inferred from Linux fallback output.

The N12 manifest binds certification to stable-main workflow run **#875 / run id 33032198400** at source SHA `34a723c33d6779fb8a4476c7e4d94f610e19e129`, including the required Linux, profile, Overleaf proxy, Windows literal-font and aggregate jobs. PR #125 head `ecb77f6a6e4e69260502087248304f7fc966bf02` passed both Normative source contract and LaTeX preflight with `behind_by=0`, then squash-merged as `b9a827199fea3838bf94d707d43c78523f1475ad`.

No normative values, locators, tolerances, compatibility mappings or proof-state were changed by N12.

## N13 — negative fixtures / negative-path validation — ACTIVE

N13 tests **validator sensitivity** and does not create a second normative specification.

PR #127 established the machine-readable baseline and generic temporary-mutation harness. Its final branch evidence reported **PASS=3 / FAIL=0** for:

1. `page-margins-right` — family `final-pdf-geometry`, expected rejection `margin.recto.right`;
2. `short-direct-citation-quotes` — family `citation-quotation-presentation`, expected rejection `citation.direct-short.quotation-marks`;
3. `ibge-table-open-sides` — family `vector-rule-geometry`, expected rejection `table.ibge.open-sides`.

The initial margin mutation was discarded because it did not change the physical geometry measured by the oracle. The accepted case mutates the actual post-`\textual` geometry while preserving the expected predicate and N5 tolerance. PR #127 squash-merged as stable main `a1dfd9a179c768bde63a2bf9055af2c1fd142cad`.

Post-#127 stable-main LaTeX preflight **#890 / run id 33055886167** is fully green, including profile matrix/PDF-A, reference document/PDF-A, Overleaf proxy, Windows literal Times/Arial build and certification, structural checks and aggregate gate.

PR #128 hardens the N11 structural observer so predicate evidence is serialized/printed before positive-campaign bookkeeping can reject a negative run. The positive project route remains strict at **5/5 bounded positive coverage**; there is no bypass for the N11 closure gate.

PR #128 adds the fourth controlled case:

4. `project-required-resources` — family `semantic-structural-observers`; the required `Recursos` section is temporarily replaced by non-equivalent `Infraestrutura`, the project compiles through pdfLaTeX + Biber, and `normative_n11_project_structure.py --enforce` must reject `project.textual.required-sections`.

Pre-handoff PR #128 head `9bcd7f46063d274af3d31f66877ccea3d1fd416c` passed both source-contract and LaTeX-preflight workflows. Structured evidence recorded **PASS=4 / FAIL=0** for N13 and the positive N11 project route remained **5/5**. This handoff update changes the PR head, so the resulting exact head must be revalidated before merge.

Current mechanism state:

- `final-pdf-geometry` — REPRESENTED;
- `citation-quotation-presentation` — REPRESENTED;
- `vector-rule-geometry` — REPRESENTED;
- `semantic-structural-observers` — REPRESENTED on PR #128;
- `configuration-strict-rejection` — pre-existing negative paths identified, but N13 must bind them to machine-verifiable campaign evidence rather than documentation alone;
- `pdf-pdfa-validation` — still pending a controlled non-destructive negative artifact and exact validator signature;
- text/typography extraction — still requires explicit reconciliation before closure; coverage by another family must not be assumed without machine evidence.

N13 remains open. Do not mark the phase DONE until the mechanism inventory is fully reconciled and every declared negative-path cell is machine-verified.

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
2. derive exact bounded rule IDs, matrix cells or validator-mechanism cells from the current contract/implementation;
3. add only required scenario/fixture/checker/gate changes;
4. validate source contract and CI;
5. require final head unchanged and `behind_by=0`;
6. squash merge using `expected_head_sha`;
7. update this handoff only when roadmap state or next action materially changes.

## Next action

Finish PR #128 on its documentation-final head:

1. require both Normative source contract and LaTeX preflight to pass on the exact new head;
2. confirm `behind_by=0` against stable main `a1dfd9a179c768bde63a2bf9055af2c1fd142cad`;
3. verify the diff remains limited to N13/N11 audit code, manifest and this handoff;
4. mark ready and squash merge with `expected_head_sha` only after those checks.

Then continue N13 from the resulting stable main in isolated units:

1. reconcile and machine-bind the pre-existing `configuration-strict-rejection` negatives;
2. add an explicit text/typography-extraction negative case if the mechanism inventory shows it is not already represented by a predicate-specific path;
3. implement PDF/PDF-A negative validation on the existing veraPDF execution path, using a structurally valid PDF with a controlled non-conformity and requiring a validator-specific rejection signature;
4. rederive the complete mechanism inventory and close N13 only when every declared cell is represented or explicitly reconciled with a justified state;
5. only after N13 closure advance the formal roadmap to N14.
