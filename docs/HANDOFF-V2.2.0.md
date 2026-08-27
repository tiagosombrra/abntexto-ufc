# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-26
Checkpoint PR: #123
Stable base before this PR: `dc964740e0200483c3327c760f820e6f30f12d6a`

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
| N11 | research-project profile / NBR 15287 | ACTIVE — 3/5 bounded positive, 2 support-only |
| N12 | profile, engine and font matrix | PENDING |
| N13 | negative fixtures / negative-path validation | PENDING |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure is **11/16 phases = 68.75%**. The remaining five gates are **31.25%** of the roadmap. N11 remains active, so this phase-gate percentage does not advance until N11 closes. This is not a conformity or proof percentage.

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

The pre-textual work map is reconciled. Manual/conditional boundaries remain explicit, including catalog-card font sizing, approval signatures and CAPES applicability. N11 reconciliation has now mapped three existing structured N6 project measurements to exact `project.*` predicates; this mapping changes bounded-coverage classification only and does not promote proof-state.

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
- PR #122: final 5-rule `index-glossary-final-pdf` campaign — `20/20`; technical evidence head `9f648ab676800d0e9cf5c0e76c23e3eab7494458`, final audited documentation head `de172c297594ded28b2833d95065b45377dbfd33`, Normative source contract #251 and LaTeX preflight #862 successful with `behind_by=0`, then squash-merged as `dc964740e0200483c3327c760f820e6f30f12d6a`.

The PR #122 final-PDF campaign reported `PASS=5 FAIL=0` and `current_bounded_positive=20 current_support_only=0`:

- observed index heading: `ÍNDICE REMISSIVO`; this lexical text is observational and is **not** frozen as an additional predicate;
- index heading is uppercase, bold against same-document calibration, exactly 12 pt, and centered within the frozen N5 tolerance;
- `glossary.element.optional` passes with controlled present and absent routes while an independent index is still generated.

The absent-route fixture and marker observer were corrected during audit without changing the class implementation, any normative value, locator or N5 tolerance. N10 closure did **not** promote proof-state.

## N11 — research-project profile / NBR 15287 — ACTIVE

PR #123 machine-rederives N11 from the current 181-rule full contract as exactly **5 `project.*` predicates**, partitioned by authority:

Normative NBR 15287:2025 rules — 3:

- `project.cover.optional`;
- `project.title-page.required`;
- `project.textual.required-sections`.

Internal technical/profile rules — 2:

- `project.final-work-elements.excluded` — authority `technical-profile`;
- `project.anonymization.policy` — authority `project-policy`.

The NBR 15287:2025 locator ruleset `project.structure-nbr15287` covers exactly the three normative rules and remains `UNAVAILABLE_WITH_REASON`: exact authoritative/licensed clause text is not available in the repository evidence corpus. Positive rendered evidence therefore remains separate from normative proof-state.

The conservative N11 baseline is **3/5 bounded positive + 2/5 support-only**.

Existing bounded-positive rules, mapped from live structured N6 evidence:

- `project.cover.optional` — the cover oracle measures both `projeto` and `projetoanonimizado` with `required=false` and suppressed cover routes;
- `project.title-page.required` — the title-page oracle measures title-page presence for both project profiles with `required=true`;
- `project.anonymization.policy` — the title-page oracle verifies hidden author/advisor and the required public identifier.

PR #123 does not count these merely because checker files exist. `normativa/n11-scope-reconciliation.json` and `tests/checks/normative_n11_scope.py` also require each historical checker to remain invoked by its evidence gate, and each evidence gate to remain invoked by the mandatory `pretextual` CI host. Orphaned evidence therefore cannot silently remain in the bounded baseline.

Residual support-only rules:

- `project.textual.required-sections` with exact semantic values `introduction`, `theoretical-framework`, `methodology`, `resources`, `schedule`, `references`;
- `project.final-work-elements.excluded` with exact semantic values `summary`, `abstract`, `approval-page`.

The existing `tests/v2-project-check.sh` already exercises these behaviors broadly in `tests/normativa/projeto-15287.tex`, but those observations remain support-only until the exact two rule IDs are mapped by the residual `project-structure-final-pdf` campaign.

On PR #123 head `c1ddfefe80fe67049d51f79c3bc0fa8c33a4f04c`, the structural job of LaTeX preflight #867 reported:

- `N11-EVIDENCE scope-reconciliation total=5 existing_bounded_positive=3 support_only=2`;
- exact authority lists: 3 normative, 1 technical-profile, 1 project-policy;
- one residual campaign with exactly two rules;
- `nbr15287=UNAVAILABLE_WITH_REASON`;
- `proof_state_changed=false`;
- structural validation summary `PASS=14 FAIL=0 SKIP=0`.

This is bounded-coverage reconciliation, not a proof-state promotion.

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

Finish PR #123 on its final documentation-updated head. Require exact-head Normative source and full LaTeX preflight success, including structural `N11-EVIDENCE scope-reconciliation total=5 existing_bounded_positive=3 support_only=2`, structural validation `PASS=14 FAIL=0 SKIP=0`, aggregate `latex-preflight` success and `behind_by=0`; then squash merge with the expected head SHA.

After #123 merges, create `audit/n11-project-structure-evidence` from the new stable `main`. Reuse the controlled `projeto-15287.pdf` generated by the project gate and add structured final-PDF evidence for exactly the two residual predicates. Map the six contract semantic section IDs to the controlled project headings and verify their presence without inventing an order predicate. For final-work exclusions, verify the exact semantic exclusions while treating concrete detection strings such as `RESUMO`, `ABSTRACT`, `BANCA EXAMINADORA` and `APROVADA EM` as observer tokens rather than new normative lexical requirements.

If that residual campaign reports `PASS=2 FAIL=0`, promote N11 bounded coverage to **5/5** while keeping the NBR 15287 locator `UNAVAILABLE_WITH_REASON` and proof-state unchanged. Only then may N11 be marked DONE, formal roadmap closure advance to **12/16 = 75%**, and N12 become active for a fresh exact-scope rederivation.
