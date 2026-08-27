# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-27
Checkpoint: distribution reference-corpus hotfix before N13 typography merge
Stable main: `d10d28607487c5a8d7bca325f48201c6deea8a77`
Stable-main full preflight: #941 / run id `33080352548` — SUCCESS

This is the single dynamic continuation document for the v2.2.0 normative audit and release. Future work must read this file before relying on chat history. Detailed historical evidence belongs in `normativa/`, `tests/`, Git history, pull requests and GitHub Actions logs.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable requirements, locators, precedence, proof policy and phase manifests.
2. `tests/` + GitHub Actions — executable evidence, negative-path sensitivity and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. this handoff — roadmap state, audit decisions and immediate next action.
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
| N13 | negative fixtures / negative-path validation | ACTIVE — typography port prepared in PR #130 |
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

Stable mechanism state before PR #130 merge:

- `final-pdf-geometry` — REPRESENTED;
- `citation-quotation-presentation` — REPRESENTED;
- `vector-rule-geometry` — REPRESENTED;
- `semantic-structural-observers` — REPRESENTED;
- `text-typography-extraction` — represented by the ported PR #130 campaign, pending exact-head validation and merge;
- `configuration-strict-rejection` — pre-existing behavior exists, but still needs machine-bound N13 receipt/evidence;
- `pdf-pdfa-validation` — still requires controlled structurally valid non-conformity and validator-specific rejection evidence.

### PR #130 — typography negative path

The original preserved head before the port was `7e830dd4f5bb732fa98b20a6020a0e1158c50ec6`. It was intentionally not merged on stale ancestry.

After stable-main preflight #941 closed the #134 compatibility blocker, PR #130 was atomically ported onto `d10d28607487c5a8d7bca325f48201c6deea8a77` as head `6a7835b1a89508a7b5854249660a575972fc4901` with `behind_by=0` at port time. The port contains only three N13 functional deltas plus its handoff update:

1. `normativa/n13-negative-paths.json` adds mechanism `text-typography-extraction` and case `body-font-size`;
2. `tests/checks/normative_n13_campaign.py` expands the expected campaign scope without duplicating the generic executor;
3. `tests/v2-negative-paths-check.sh` routes the gate through the campaign adapter.

The fifth controlled negative case temporarily renders `UFCNSevenBodyAlpha` at 14 pt, requires successful pdfLaTeX compilation, and requires `normative_typography.py` to reject `font.size.body` with `N7-EVIDENCE rule=font.size.body status=FAIL`.

Normative source contract #311 / run id `33081569884` is green on the ported head. LaTeX preflight #942 / run id `33081569864` is the exact-head validation run; do not merge #130 until that run is fully reconciled and the distribution blocker below is closed.

No class implementation, normative values, locators, N5 tolerances, compatibility mappings, N12-certified workflow or proof-state are changed by the typography port.

### Remaining N13 sequence

After the typography case is exact-head validated, merged and confirmed on stable main:

1. machine-bind `configuration-strict-rejection` using structured receipt/evidence from the existing strict font checks;
2. implement host-side PDF/A negative validation using a structurally readable PDF with controlled XMP non-conformity and veraPDF-specific rejection evidence;
3. rederive the complete mechanism inventory;
4. close N13 only if every declared mechanism is represented or explicitly reconciled;
5. only then advance to N14.

## Editorial v2.2 reference guide and Overleaf hotfix

PR #133 converted the v2.2 reference PDF into the commented UFC academic-work guide while preserving class behavior and normative values. It squash-merged as `2cbd6d00318ba906e225fa37a4efb724300c3b4e`.

The post-#133 full preflight #933 / run id `33076301572` exposed one LuaLaTeX/TeX Live 2025 overflow in the long direct CAPES Portaria nº 206/2018 URL. All other Linux, PDF/A, structural and Windows surfaces were green.

PR #134 fixed only that compatibility issue:

- final exact head: `05bf4c87ac4a7b711be71015c4b33222b53e67a2`;
- squash merge: `d10d28607487c5a8d7bca325f48201c6deea8a77`;
- the bibliography now uses the shorter official CAPES administrative-act catalog URL;
- no warning suppression or tolerance relaxation was introduced;
- the non-frozen reference-preview workflow now checks TeX Live 2025 on relevant PRs;
- the N12-certified `latex-preflight.yml` was not modified.

Full stable-main preflight #941 / run id `33080352548` is fully green, including reference/PDF-A, 12 profile PDFs/PDF-A, objects/bibliography, post-textuals, structural suite, Overleaf stable proxy, Windows literal-font build/certification and aggregate `latex-preflight`.

## Distribution reference-corpus blocker — ACTIVE HOTFIX

Stable-main Distribution preflight #219 / run id `33080343888` exposed one stale reference-corpus expectation after the #133 guide rewrite:

- Gate T prerequisite — SUCCESS;
- full `make preflight` — 30/31 checks PASS;
- only `Reference corpus` failed;
- exact failure: expected PDF marker `BASE NORMATIVA ADOTADA` was absent;
- the document source defines `\subsection{Base normativa adotada}` and the same corpus checker already expects `Base normativa adotada` in the sumário;
- all PDF, layout, N13 baseline, N11, object, bibliography and post-textual checks in that same release preflight passed.

This is a stale test-contract case expectation, not a class/normative/PDF defect. The hotfix changes only the body marker in `tests/v2-reference-corpus-check.sh` from the obsolete all-uppercase form to the exact subsection title `Base normativa adotada`. It does not remove the marker, weaken the corpus, change heading behavior or alter normative values.

Do not merge PR #130 before this distribution hotfix is validated and merged. After the hotfix changes stable main, port/rebase #130 once more if required so its final audited head is `behind_by=0`.

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

1. validate and merge the isolated distribution reference-corpus hotfix from stable main `d10d28607487c5a8d7bca325f48201c6deea8a77`;
2. require the corrected release/distribution preflight to pass, especially `Reference corpus`, bundle construction and Overleaf import proxy;
3. inspect the resulting stable-main preflight/distribution runs;
4. finish/reconcile PR #130 preflight #942, but re-port #130 onto the resulting new stable main before merge if it becomes behind;
5. on the final #130 head require `body-font-size` PASS, N13 summary 5/5, positive N11 5/5, exact-head green CI and `behind_by=0`;
6. squash-merge #130 and inspect stable main;
7. continue N13 with machine-bound configuration-strict evidence;
8. add host-side PDF/A negative evidence;
9. perform final mechanism inventory reconciliation and close N13 only if all declared cells are represented or explicitly reconciled;
10. advance to N14 only after N13 closure.
