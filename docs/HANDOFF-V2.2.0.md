# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-27
Checkpoint: PR #137 binds N13 strict configuration rejection; pre-documentation exact-head validation green
Stable main: `4944d98fd4dd35d9df45fb5764e360324a72b741`
Stable-main LaTeX preflight: #965 / run `33111409990` — SUCCESS
Stable-main Distribution preflight: #229 / run `33111409974` — SUCCESS

This is the single dynamic continuation document for the v2.2.0 normative audit and release. Read it before relying on chat history. Detailed historical evidence belongs in `normativa/`, `tests/`, Git history, pull requests and GitHub Actions logs.

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
- in N13, compile failure is not evidence that a validator rejected a normative violation;
- negative fixtures and validator receipts are instrumentation, not new normative requirements;
- do not modify the N12-certified `.github/workflows/latex-preflight.yml` during N13 unless N12 is explicitly reopened.

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
| N13 | negative fixtures / negative-path validation | ACTIVE — PR #137 strict/config receipt validated; PDF/PDF-A negative mechanism remains |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure remains **13/16 phases = 81.25%**. This is a phase-gate metric, not a normative-conformity or proof percentage.

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

Core N5 tools remain `pdftotext -bbox-layout`, `pdftohtml -xml -zoom 1.0`, `pdfinfo` and `pdffonts`. N9 added calibrated vector-rule geometry with `pdftocairo -svg`; no rasterization or tolerance change.

## Closed-phase certification notes

### N11 — research-project profile

N11 covers exactly five `project.*` predicates and remains **5/5 bounded positive coverage**. NBR 15287 locator limitations remain explicit and proof-state is unchanged.

### N12 — compatibility matrix

N12 is closed as a factorized 20-cell certification:

- six profiles × two engines = 12 cells;
- portable `times`/`arial` × pdfLaTeX/LuaLaTeX = 4 cells;
- literal Windows Times New Roman/Arial × pdfLaTeX/LuaLaTeX = 4 cells.

Literal Windows identity is certified only on the Windows route, never inferred from Linux fallback fonts.

The certified workflow blob `.github/workflows/latex-preflight.yml` remains SHA `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## Stable-main baseline

Repository-hygiene PR #136 squash-merged as stable main `4944d98fd4dd35d9df45fb5764e360324a72b741` without changing class implementation or the normative contract.

Post-#136 stable-main certification:

- LaTeX preflight #965 / `33111409990` — SUCCESS;
- reference document + PDF/A-2b — SUCCESS;
- 12-profile matrix + PDF/A-2b — SUCCESS;
- objects/bibliography — SUCCESS;
- post-textuals — SUCCESS;
- structural suite — SUCCESS;
- Overleaf/TeX Live 2025 proxy — SUCCESS;
- Windows literal Times New Roman/Arial build — SUCCESS;
- Windows literal Unicode/embedding/PDF-A certification — SUCCESS;
- Distribution #229 / `33111409974` — SUCCESS through Gate T, release preflight, PDF/A-2b, deterministic bundles, Overleaf import proxy and artifact upload.

## N13 — negative fixtures / validator sensitivity — ACTIVE

N13 validates sensitivity of existing oracles/validators and does not create a second normative specification.

### Rendered-PDF controlled cases already merged

1. `page-margins-right` → `margin.recto.right`;
2. `body-font-size` → `font.size.body`;
3. `short-direct-citation-quotes` → `citation.direct-short.quotation-marks`;
4. `ibge-table-open-sides` → `table.ibge.open-sides`;
5. `project-required-resources` → `project.textual.required-sections`.

The generic mutation harness requires a passing positive baseline, successful fixture compilation, target-oracle non-zero rejection, exact predicate signature and matching failed-rule evidence.

### PR #137 — configuration strict rejection

Branch: `audit/n13-configuration-strict-receipt`.

Base: stable main `4944d98fd4dd35d9df45fb5764e360324a72b741`.

Pre-documentation implementation head: `a9040a4e70803ea9f665113bf3202cf7771cba86`.

PR #137 adds one structured validator-mechanism receipt and keeps all five rendered-PDF mutation cases unchanged. The checker reuses `check_fonts()` from `tools/validate-ufc-pdf.py` and binds its result to the existing normative rule `font.family.body`.

The same textual fallback observation must produce:

- profile `strict` → `REPROVADO`, mandatory;
- profile `portable` → `ALERTA`, non-mandatory.

Literal Times New Roman and Arial controls must remain `APROVADO` in `strict`.

Exact pre-documentation evidence:

- Normative source contract #314 / `33112476335` — SUCCESS;
- LaTeX preflight #967 / `33112476333` — SUCCESS;
- five existing negative cases — `PASS=5 FAIL=0 selected=5 proof_state_changed=false`;
- `N13-EVIDENCE mechanism=configuration-strict-rejection status=PASS rule=font.family.body strict=REPROVADO portable=ALERTA same_observation=true compile_failure_counted_as_rejection=false proof_state_changed=false`;
- positive N11 — 5/5 bounded coverage, `proof_state_changed=false`;
- structural suite — `PASS=14 FAIL=0 SKIP=0`;
- reference/PDF-A, profiles/PDF-A, objects/bibliography and post-textual jobs — SUCCESS;
- branch was `behind_by=0` before this handoff synchronization.

This handoff commit changes the PR head. The pre-documentation evidence is historical support only; merge requires the final documented head to reproduce the required CI evidence and remain `behind_by=0`.

### N13 mechanism inventory after PR #137

- `final-pdf-geometry` — REPRESENTED;
- `text-typography-extraction` — REPRESENTED;
- `citation-quotation-presentation` — REPRESENTED;
- `vector-rule-geometry` — REPRESENTED;
- `configuration-strict-rejection` — REPRESENTED on PR #137;
- `semantic-structural-observers` — REPRESENTED;
- `pdf-pdfa-validation` — INVENTORY_PENDING.

N13 remains ACTIVE until `pdf-pdfa-validation` is represented/reconciled and the complete mechanism inventory is rederived.

### PDF/PDF-A negative-path requirement

A corrupt or unreadable PDF is not sufficient negative evidence. The controlled negative document must:

1. originate from a positively valid/readable PDF;
2. remain readable by ordinary PDF tooling such as `pdfinfo` and `pdftotext` after mutation;
3. contain an isolated PDF/A-2b non-conformity that does not depend on LaTeX compile failure;
4. be rejected specifically by veraPDF under flavour `2b`;
5. emit structured N13 evidence identifying the controlled mutation and veraPDF rejection;
6. leave normative values, locators, N5 tolerances and proof-state unchanged.

A promising implementation direction is a same-length in-place mutation of the PDF/A XMP identification metadata on a controlled valid PDF, followed by independent readability checks and veraPDF-specific rejection. Do not freeze a veraPDF clause/signature until an observed validator report confirms the stable failure identifier.

## Repository hygiene and Git policy

The published `main` history is healthy and must not be rewritten for cosmetic compaction. Protected long-lived branches are `main` and `1.x`; roadmap/audit/fix/docs/preview/release-validation branches are disposable working refs after their evidence is safely represented by PR/merge/Actions history.

A 2026-08-27 audit found 123 remote branches. Physical branch deletion is intentionally **deferred until the final cleanup stage**; do not make branch deletion a blocker for N13–N15 work.

Preserve `planning/v2.2.0-normative-verification` until its unique divergent content is explicitly reconciled. Do not delete it solely based on age/name.

Release tags `v*` remain immutable. Do not force-update protected branches or published tags.

## Normative currency

The repository records `ABNT NBR 14724:2024`, corrected version dated 2025-04-01. Current-edition and precedence policy remains governed by `normativa/version-policy.json` and `docs/VIGENCIA-NORMATIVA.md`. No N1/N2 reopening is required at this checkpoint.

## Distribution / CTAN track

- D0–D4: DONE;
- D5 rehearsal: historical PR #36, CLOSED without merge;
- D5 final: BLOCKED by N15;
- D6 CTAN resubmission: BLOCKED by final D5.

Issue #18, bit-reproducible reference PDF metadata/ID, remains open and requires an explicit blocking/non-blocking release decision before final D5.

The UFC institutional mark remains in the source repository but is externalized from public/CTAN bundles; do not describe it as removed from the repository.

## PR discipline

For roadmap PRs:

1. branch from exact stable `main`;
2. derive the exact bounded predicate/mechanism scope from the current contract and implementation;
3. add only required scenario/fixture/checker/gate changes;
4. validate source contract and CI;
5. require final head unchanged and `behind_by=0`;
6. squash merge using `expected_head_sha`;
7. inspect the full stable-main push, including Overleaf and Windows literal fonts when applicable;
8. update this handoff whenever roadmap state, stable-main evidence or immediate next action materially changes;
9. defer bulk remote-ref cleanup until the final cleanup stage unless a branch itself blocks current work.

## Immediate next action

1. validate PR #137 again on the exact post-handoff head;
2. require the five existing negative cases, the strict-configuration receipt and positive N11 to remain green with `proof_state_changed=false`;
3. require `behind_by=0`, mark #137 ready and squash-merge with `expected_head_sha`;
4. inspect the resulting stable-main LaTeX preflight and distribution evidence;
5. branch from that exact stable main for `pdf-pdfa-validation`;
6. prototype a structurally readable controlled PDF/A-2b metadata non-conformity and observe the exact veraPDF rejection before freezing the receipt signature;
7. bind the successful PDF/A negative path into the N13 mechanism inventory;
8. rederive the complete inventory and close N13 only if all declared mechanisms are represented or explicitly reconciled;
9. advance to N14 only after formal N13 closure;
10. leave bulk branch deletion for the final repository-cleanup stage.
