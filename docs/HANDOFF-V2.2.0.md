# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-26
Checkpoint PR: #124
Stable base before this PR: `0888b4bf3f5cd367a70efd1ad82d25aa73aea235`

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
| N10 | post-textual elements and multivolume | DONE — 20/20 bounded positive coverage |
| N11 | research-project profile / NBR 15287 | DONE — 5/5 bounded positive coverage |
| N12 | profile, engine and font matrix | ACTIVE — exact matrix reconciliation pending |
| N13 | negative fixtures / negative-path validation | PENDING |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure is **12/16 phases = 75%**. The remaining four gates are **25%** of the roadmap. This is a phase-gate metric, not a conformity or proof percentage.

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

The pre-textual work map is reconciled. Manual/conditional boundaries remain explicit, including catalog-card font sizing, approval signatures and CAPES applicability. Structured cover/title-page evidence is reused by N11 only through machine-checked live evidence chains.

### N7 — layout, pagination, sections and footnotes — DONE

Closed at **39/39 bounded positive coverage**. Literal Arial/Times New Roman identity is certified by the Windows path rather than inferred from Linux fallback fonts.

### N8 — citations and references — DONE

Closed at **19/19 bounded positive coverage**. DOI and online-access evidence remains positive-applicability evidence; unavailable licensed NBR 6023:2025 clause text was not promoted to `PROVEN`. General DOI/URL formatting remains delegated to `biblatex-abnt`.

### N9 — objects, tables, equations and code — DONE

Closed at **23/23 bounded positive coverage** through PRs #116–#119. PR #119 final audited head `3b5ae944fec35015dab7cef4877b072582817a97` passed Normative source contract #238 and LaTeX preflight #846 with `behind_by=0`, then squash-merged as `082bc033b86465cb375ca3c90b6ed812de430b7c`.

### N10 — post-textual elements and multivolume — DONE

Machine-rederived as exactly **20 predicates** and closed at **20/20 bounded positive coverage**:

- PR #120: baseline `2/20 bounded + 18/20 support-only`, merge `17c8e22337f861127bf6bb07efa8bf9602010a49`;
- PR #121: 13-rule appendix/annex final-PDF campaign → `15/20`, merge `509b04c08d0fa3be469d32c0ed5a856f76e5422c`;
- PR #122: 5-rule index/glossary final-PDF campaign → `20/20`; final head `de172c297594ded28b2833d95065b45377dbfd33`, Normative source #251 and LaTeX preflight #862 successful with `behind_by=0`, merge `dc964740e0200483c3327c760f820e6f30f12d6a`.

The observed index title `ÍNDICE REMISSIVO` remains observational only; it is not a new lexical predicate. Glossary optionality is exercised with clean present and absent routes. Proof-state remains unchanged.

### N11 — research-project profile / NBR 15287 — DONE

PR #123 machine-rederived the exact N11 scope as **5 `project.*` predicates**:

Normative NBR 15287:2025 rules:

- `project.cover.optional`;
- `project.title-page.required`;
- `project.textual.required-sections`.

Internal profile/policy rules:

- `project.final-work-elements.excluded` — `technical-profile`;
- `project.anonymization.policy` — `project-policy`.

The NBR 15287 locator `project.structure-nbr15287` remains `UNAVAILABLE_WITH_REASON` because exact authoritative/licensed clause text is unavailable in the repository evidence corpus. Positive coverage therefore remains separate from proof-state.

PR #123 fixed the conservative baseline at **3/5 bounded + 2/5 support-only**. The three bounded rules are sustained by live structured N6 cover/title-page evidence, with checker → evidence-shell → mandatory `pretextual` host linkage verified by `tests/checks/normative_n11_scope.py`. Final audited head `a0a223a55d9cc11e805d199a01ad581207ecc423` passed exact-head CI with `behind_by=0` and squash-merged as `0888b4bf3f5cd367a70efd1ad82d25aa73aea235`.

PR #124 executes the sole residual `project-structure-final-pdf` campaign against the existing controlled `projeto-15287.pdf`:

- `project.textual.required-sections` — all six semantic sections are observed in the rendered PDF; section order is explicitly **not** asserted;
- `project.final-work-elements.excluded` — summary, abstract and approval-page observer classes are absent; concrete observer strings are instrumentation, not new normative lexical requirements.

Technical evidence on head `99da6cd8e5477906346826df4257c9f2a7b225e9` reported:

- `N11-EVIDENCE project-structure-final-pdf-summary PASS=2`;
- `N11-EVIDENCE bounded-progress total=5 baseline_existing_bounded_positive=3 promoted_bounded_positive=2 current_bounded_positive=5 current_support_only=0 proof_state_changed=false`;
- structural summary `PASS=14 FAIL=0 SKIP=0`;
- full LaTeX preflight #871 success.

The observer was then hardened to normalized case-insensitive section matching so capitalization is not introduced as an unstored requirement. This is an observer-only correction. The documentation-updated final PR head must pass exact-head source/preflight CI before merge.

N11 closure does **not** promote proof-state; `PROVEN=0` and the NBR 15287 locator limitation remain unchanged.

## N12 — profile, engine and font matrix — ACTIVE

N12 is a compatibility/certification phase, not a reopening of N7/N11 normative predicates. Rederive its exact matrix dimensions before declaring closure.

Current physical evidence already provides three complementary grids:

1. **profile × engine** — six supported profiles (`tccgraduacao`, `tccespecializacao`, `dissertacao`, `tese`, `projeto`, `projetoanonimizado`) × two engines (`pdflatex`, `lualatex`) = 12 complete PDFs through `tests/v2-profile-matrix-check.sh`; all 12 are also validated as PDF/A-2b by `tests/v2-profile-pdfa-check.sh`;
2. **font family × engine, portable mode** — `times`/`arial` × `pdflatex`/`lualatex` through `tests/v2-font-config-check.sh`, including rm/sf/tt family consistency, embedding and strict-mode acceptance/rejection behavior;
3. **literal Windows font family × engine** — Times New Roman/Arial × pdfLaTeX/LuaLaTeX, with literal identity, Unicode extraction, no textual fallback, embedding and PDF/A-2b certified by the Windows build/certification jobs on full stable-main runs.

The matrix reconciliation should prove the profile axis and font axis are implementation-orthogonal before using the complete marginal grids instead of adding a permanent 24-cell profile × font × engine job. At minimum, verify the exact supported choice sets, mandatory PR hosts, font/profile source separation and absence of hidden coupling. Do not infer literal Windows identity from Linux fallback PDFs.

A full stable-main workflow run after the final N11 merge must be used for the literal Windows evidence so all matrix evidence is tied to the stable implementation state. The Overleaf proxy may be recorded as supplemental environment evidence but is not automatically part of the N12 core matrix.

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
2. derive exact bounded rule IDs or matrix cells from the current contract/implementation;
3. add only required scenario/fixture/checker/gate changes;
4. validate source contract and CI;
5. require final head unchanged and `behind_by=0`;
6. squash merge using `expected_head_sha`;
7. update this handoff only when roadmap state or next action materially changes.

## Next action

Finish PR #124 on its final documentation-updated head. Require exact-head Normative source and full LaTeX preflight success, including `N11-EVIDENCE project-structure-final-pdf-summary PASS=2`, bounded progress `current_bounded_positive=5 current_support_only=0`, structural validation `PASS=14 FAIL=0 SKIP=0`, aggregate `latex-preflight` success and `behind_by=0`; then squash merge with the expected head SHA.

After #124 merges, inspect the full stable-main LaTeX preflight for that exact merge SHA and require successful profile matrix, profile PDF/A, Windows literal font build/certification and aggregate. Then create `audit/n12-matrix-reconciliation` from that stable main. Build a machine-readable matrix manifest/checker that rederives the exact profile, engine and font axes, binds them to the existing physical gates, verifies profile/font implementation orthogonality and records the exact stable-main Windows artifact/run evidence. Avoid a permanent redundant 24-cell cross-product unless the orthogonality checker finds real coupling. Only close N12 when every declared matrix cell and the orthogonality gate are machine-verified.
