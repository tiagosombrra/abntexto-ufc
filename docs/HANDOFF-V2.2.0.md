# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-27
Checkpoint: N13 formal-closure candidate prepared on `audit/n13-formal-closure`; exact-head PR validation pending
Stable main: `c27686b9cc0b7dcb6aa40a6e29b49829ed2ea693`
Stable-main LaTeX preflight: #978 / run `33118743279` — SUCCESS
Stable-main Distribution preflight: #231 / run `33118743274` — SUCCESS

This is the single dynamic continuation document for the v2.2.0 normative audit and release. Read it before relying on chat history. Detailed historical evidence belongs in `normativa/`, `tests/`, Git history, pull requests and GitHub Actions logs.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable requirements, locators, precedence, proof policy and phase manifests.
2. `tests/` + GitHub Actions — executable evidence, validator sensitivity and regressions.
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
- compile failure is not evidence that a validator rejected a normative violation;
- negative fixtures and validator receipts are instrumentation, not new normative requirements;
- the N12-certified `.github/workflows/latex-preflight.yml` remains untouched unless N12 is explicitly reopened;
- bulk remote-branch deletion remains deferred until final repository cleanup.

## Canonical N0–N15 roadmap

| Phase | Scope | Gate status on this closure branch |
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
| N13 | negative fixtures / negative-path validation | DONE candidate — 7/7 mechanism inventory represented; exact-head closure validation pending |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

The closure branch represents **14/16 phases = 87.5%**. Stable `main` remains formally at 13/16 until this closure PR is independently validated and merged. This percentage is a phase-gate metric, not a normative-conformity or proof percentage.

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

Core final-PDF tooling remains `pdftotext -bbox-layout`, `pdftohtml -xml -zoom 1.0`, `pdfinfo`, `pdffonts` and calibrated `pdftocairo -svg` vector geometry.

### N11 and N12 closed-state invariants

N11 remains exactly five `project.*` predicates with **5/5 bounded positive coverage** and `proof_state_changed=false`. NBR 15287 locator limitations remain explicit.

N12 remains a factorized 20-cell certification:

- six profiles × two engines = 12 cells;
- portable `times`/`arial` × pdfLaTeX/LuaLaTeX = 4 cells;
- literal Windows Times New Roman/Arial × pdfLaTeX/LuaLaTeX = 4 cells.

Literal Windows identity is certified only on the Windows route. The certified workflow blob `.github/workflows/latex-preflight.yml` remains SHA `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## Stable-main baseline after PR #138

PR #138, `audit: add N13 PDF/A negative validation`, squash-merged as stable main `c27686b9cc0b7dcb6aa40a6e29b49829ed2ea693`.

Its exact functional head was `59911308d4304fc3a54b7513f0691540768ffc9e`, with `behind_by=0` and exactly four changed files. Exact-head evidence included:

- Normative source contract #323 / `33117857209` — SUCCESS;
- LaTeX preflight #977 / `33117857239` — SUCCESS;
- five controlled rendered-PDF negative cases — `PASS=5 FAIL=0 selected=5 proof_state_changed=false`;
- strict-configuration receipt — PASS with the same fallback observation producing `strict=REPROVADO` and `portable=ALERTA`;
- positive N11 — 5/5 bounded coverage, `proof_state_changed=false`;
- structural suite — `PASS=14 FAIL=0 SKIP=0`;
- controlled PDF/A receipt:
  `N13-EVIDENCE mechanism=pdf-pdfa-validation status=PASS mutation=pdfaid-part-2-to-3 readable=true text_unchanged=true verapdf_compliant=false specification=ISO_19005_2 clause=6.6.4 test=2 compile_failure_counted_as_rejection=false proof_state_changed=false`.

The PDF/A receipt uses an already-valid PDF/A-2b reference PDF, mutates exactly one same-length XMP identifier `<pdfaid:part>2</pdfaid:part>` → `<pdfaid:part>3</pdfaid:part>`, preserves `pdfinfo`/`pdftotext` readability and extracted text identity, and is rejected by veraPDF 1.30.2 under PDF/A-2b at ISO 19005-2:2011 clause 6.6.4 test 2. This signature is observed validator evidence, not an inferred identifier.

Post-merge stable-main certification is fully green:

- LaTeX preflight #978 / `33118743279` — SUCCESS;
- reference document + PDF/A-2b — SUCCESS;
- 12-profile matrix + PDF/A-2b — SUCCESS;
- objects/bibliography — SUCCESS;
- post-textuals — SUCCESS;
- structural suite — SUCCESS;
- Overleaf/TeX Live 2025 proxy — SUCCESS;
- Windows literal Times New Roman/Arial build — SUCCESS;
- Windows literal Unicode/embedding/PDF-A certification — SUCCESS;
- aggregate `latex-preflight` — SUCCESS;
- Distribution #231 / `33118743274` — SUCCESS through Gate T, release preflight, PDF/A-2b, deterministic bundles, Overleaf import proxy, artifact upload and aggregate `distribution-preflight`; GitHub Release publication skipped as expected because the ref is not a release tag.

## N13 — formal closure candidate

N13 validates sensitivity of existing oracles/validators and does not create a second normative specification.

The complete mechanism inventory is now:

1. `final-pdf-geometry` — REPRESENTED by `page-margins-right`;
2. `text-typography-extraction` — REPRESENTED by `body-font-size`;
3. `citation-quotation-presentation` — REPRESENTED by `short-direct-citation-quotes`;
4. `vector-rule-geometry` — REPRESENTED by `ibge-table-open-sides`;
5. `configuration-strict-rejection` — REPRESENTED by the machine-bound strict/portable receipt;
6. `semantic-structural-observers` — REPRESENTED by `project-required-resources` and the N11 structural oracle;
7. `pdf-pdfa-validation` — REPRESENTED by the readable same-length XMP mutation and veraPDF-specific rejection.

The formal-closure branch changes phase metadata/instrumentation only:

- `normativa/n13-negative-paths.json`: `status` becomes `DONE`; predicates, cases, mechanism bindings and policy stay unchanged;
- `tests/checks/normative_n13_negative_paths.py`: the generic executor requires `status=DONE`;
- `tests/checks/normative_n13_campaign.py`: after the executor succeeds, it emits
  `N13-EVIDENCE mechanism-inventory-summary PASS=7 FAIL=0 represented=7 phase_status=DONE proof_state_changed=false`;
- this handoff records the closure candidate and stable-main evidence.

No class/runtime code, normative value, source locator, N5 tolerance, compatibility mapping, proof-state or N12 workflow is changed by formal closure.

N13 is not considered merged/closed on stable `main` until the final closure head independently reproduces the five negative cases, configuration receipt, PDF/A receipt, 7/7 inventory receipt, N11 5/5 and structural 14/14 with `behind_by=0`.

## Repository hygiene and Git policy

The published `main` history must not be rewritten for cosmetic compaction. Protected long-lived branches are `main` and `1.x`. Audit/fix/docs/preview/release-validation branches remain disposable working refs after their evidence is safely represented by PR/merge/Actions history, but physical branch deletion is intentionally deferred until the final cleanup stage.

Preserve `planning/v2.2.0-normative-verification` until its unique divergent content is explicitly reconciled. Release tags `v*` remain immutable.

## Normative currency

The repository records `ABNT NBR 14724:2024`, corrected version dated 2025-04-01. Current-edition and precedence policy remains governed by `normativa/version-policy.json` and `docs/VIGENCIA-NORMATIVA.md`. No N1/N2 reopening is required at this checkpoint.

## Distribution / CTAN track

- D0–D4: DONE;
- D5 rehearsal: historical PR #36, CLOSED without merge;
- D5 final: BLOCKED by N15;
- D6 CTAN resubmission: BLOCKED by final D5.

Issue #18, bit-reproducible reference PDF metadata/ID, remains open and requires an explicit blocking/non-blocking release decision before final D5.

The UFC institutional mark remains in the source repository but is externalized from public/CTAN bundles; do not describe it as removed from the repository.

## Immediate next action

1. open the formal N13 closure PR from `audit/n13-formal-closure` onto exact stable main `c27686b9cc0b7dcb6aa40a6e29b49829ed2ea693`;
2. require the PR diff to remain limited to the N13 status/executor/campaign and this handoff;
3. require exact-head Normative source contract and LaTeX preflight SUCCESS;
4. require `N13-EVIDENCE negative-path-summary PASS=5 FAIL=0 selected=5 proof_state_changed=false`;
5. require the strict-configuration and PDF/A-specific N13 receipts to remain PASS;
6. require `N13-EVIDENCE mechanism-inventory-summary PASS=7 FAIL=0 represented=7 phase_status=DONE proof_state_changed=false`;
7. require N11 5/5, structural `PASS=14 FAIL=0 SKIP=0`, final head unchanged and `behind_by=0`;
8. mark the closure PR ready and squash-merge with `expected_head_sha`;
9. certify the resulting stable main with full LaTeX preflight and Distribution, including Overleaf and Windows literal fonts;
10. only then begin N14 Web/Lite and CLI/Deep unification from that exact stable main;
11. leave bulk branch deletion for the final repository-cleanup stage.
