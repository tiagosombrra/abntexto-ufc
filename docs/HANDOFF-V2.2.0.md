# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-26
Checkpoint PR: #122
Stable base before this PR: `509b04c08d0fa3be469d32c0ed5a856f76e5422c`

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
| N11 | research-project profile / NBR 15287 | ACTIVE — exact scope reconciliation pending |
| N12 | profile, engine and font matrix | PENDING |
| N13 | negative fixtures / negative-path validation | PENDING |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure is **11/16 phases = 68.75%**. The remaining five gates are **31.25%** of the roadmap. This is a phase-gate metric, not a conformity or proof percentage.

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

The pre-textual work map is reconciled. Manual/conditional boundaries remain explicit, including catalog-card font sizing, approval signatures and CAPES applicability. Research-project observations remain support-only until N11 maps them to exact project predicates.

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

### N10 — post-textual elements and multivolume — DONE

N10 was machine-rederived from the current full contract and locator manifests as exactly **20 predicates** and closed at **20/20 bounded positive coverage**.

Progression:

- PR #120: exact scope reconciliation — baseline `2/20 bounded + 18/20 support-only`; squash merge `17c8e22337f861127bf6bb07efa8bf9602010a49`.
- PR #121: 13-rule `appendix-annex-final-pdf` campaign — `15/20`; final audited head `2779c86aa08ac979f8cac7f4007c66a2584f6573`; squash merge `509b04c08d0fa3be469d32c0ed5a856f76e5422c`.
- PR #122: final 5-rule `index-glossary-final-pdf` campaign — `20/20` on technical head `9f648ab676800d0e9cf5c0e76c23e3eab7494458`; final documentation-updated head must still pass exact-head CI before merge.

The PR #122 final-PDF campaign reports `PASS=5 FAIL=0` and `current_bounded_positive=20 current_support_only=0`:

- observed index heading: `ÍNDICE REMISSIVO`; this lexical text is observational and is **not** frozen as an additional predicate;
- index heading is uppercase;
- index heading uses the same-document bold calibration and differs from the regular calibration;
- index heading measures exactly 12 pt within the frozen 1 pt tolerance;
- index heading center differs from the recto text-area center by approximately `0.00023 pt`, within the frozen 5 pt tolerance;
- `glossary.element.optional` passes with a controlled present route and a separate clean absent route while an independent index is still generated.

The absent-route fixture was corrected during audit so it truly omits glossary configuration instead of configuring `glossaries` and intentionally not printing it. The observer was also narrowed to detect glossary headings structurally and index entries by normalized page content. These were evidence-fixture/observer corrections only; no class implementation, normative value, locator or N5 tolerance changed.

Post-textual and pagination locator limitations remain in force. N10 closure does **not** promote proof-state; the project-wide proof baseline remains unchanged and `PROVEN=0`.

## N11 — research-project profile / NBR 15287 — ACTIVE

N11 must now be rederived from the **current full contract** before any implementation or evidence campaign is opened. Do not reuse an old count by assumption.

Read-only reconnaissance indicates that `normativa/coverage-rules-project.json`, `normativa/locator-audit-final.json`, `tests/v2-project-check.sh`, `tests/normativa/projeto-15287.tex`, `tests/normativa/projeto-sem-capa.tex` and `tests/normativa/pretextuais-projeto-anonimo.tex` are the principal inputs for reconciliation. Existing broad project regressions must be mapped to exact predicates before being counted as bounded positive coverage.

The NBR 15287:2025 structure rules currently have locator status `UNAVAILABLE_WITH_REASON` because exact authoritative/licensed clause text is not available in the repository evidence corpus. Positive rendered evidence must therefore remain separate from normative proof-state. Technical-profile and project-policy rules, including anonymization behavior, must also remain explicitly separated from ABNT normative claims.

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

Finish PR #122 on its **final documentation-updated head**. Require exact-head Normative source and full LaTeX preflight success, including `N10-EVIDENCE index-glossary-final-pdf-summary PASS=5 FAIL=0`, `current_bounded_positive=20 current_support_only=0`, structural repository audit success, aggregate `latex-preflight` success and `behind_by=0`; then squash merge with the expected head SHA.

After #122 merges, rederive the exact N11 work map from the current full contract, project locator manifests and existing project gates. Build a machine-readable reconciliation that distinguishes normative NBR 15287 predicates from technical-profile/project-policy predicates and classifies existing checks as bounded-positive or support-only. Only after that reconciliation should any residual N11 evidence or implementation work begin.
