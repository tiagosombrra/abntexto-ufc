# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-27
Checkpoint: N14 validator-contract inventory active on `audit/n14-validator-contract`
Stable main: `04cc137f6b0930c2f2a32aa4c299005432959f3b`
Stable-main Gate T: LaTeX preflight #983 / run `33121966942` — SUCCESS
Stable-main Distribution preflight: #232 / run `33121959982` — SUCCESS
Stable-main PDF validator: #130 / run `33121959909` — source check and Pages deploy SUCCESS

This is the single dynamic continuation document for the v2.2.0 normative audit and release. Read it before relying on chat history. Detailed historical evidence belongs in `normativa/`, `tests/`, Git history, pull requests and GitHub Actions logs.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable normative requirements, locators, precedence and proof policy.
2. `tests/` + GitHub Actions — executable evidence, validator sensitivity and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. this handoff — roadmap state, audit decisions and immediate next action.
6. Git/PR/Actions history — detailed historical evidence.

Technical validator-interface contracts are not normative requirements. N14 therefore uses `validator/validation-contract.json` as a technical source of truth and continues to consume normative content from `normativa/catalog.json` + `normativa/precedence.json`.

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
- Web/Lite must remain private-by-design and must not auto-approve capabilities it cannot execute;
- PDF.js and Poppler/veraPDF are different measurement backends; N14 requires semantic contract consistency, not numerical backend identity;
- bulk remote-branch deletion remains deferred until final repository cleanup.

## Canonical N0–N15 roadmap

| Phase | Scope | Status |
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
| N13 | negative fixtures / negative-path validation | DONE — 7/7 validator mechanisms represented and sensitivity-tested |
| N14 | Web/Lite and CLI/Deep unification | ACTIVE |
| N15 | full normative certification and release decision | PENDING |

Stable `main` has **14/16 completed phase gates = 87.5%**. N14 being active does not increase this completion metric until its exit criteria are independently validated and merged. This is not a normative-conformity or proof percentage.

## Frozen normative baseline and oracle policy

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

N11 remains exactly five `project.*` predicates with 5/5 bounded positive coverage and `proof_state_changed=false`.

N12 remains the factorized 20-cell certification: 12 profile×engine cells, four portable font×engine cells and four literal Windows font×engine cells. Literal Windows identity is certified only on the Windows route. The certified `.github/workflows/latex-preflight.yml` blob remains `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## N13 — closed on stable main

PR #139, `audit: close N13 negative-path validation`, was validated on exact head `7cb391bb649648300ed1f407151f5840564b7169`, `behind_by=0`, then squash-merged as `04cc137f6b0930c2f2a32aa4c299005432959f3b`.

Exact-head closure evidence:

- Normative source contract #326 / `33121159620` — SUCCESS;
- LaTeX preflight #981 / `33121159587` — SUCCESS;
- controlled rendered-PDF negative cases — `PASS=5 FAIL=0 selected=5 proof_state_changed=false`;
- mechanism inventory — `PASS=7 FAIL=0 represented=7 phase_status=DONE proof_state_changed=false`;
- strict configuration rejection — `strict=REPROVADO`, `portable=ALERTA`, same observation, no compile-failure shortcut;
- PDF/A controlled mutation — readable PDF, identical extracted text, veraPDF rejection at ISO 19005-2:2011 clause 6.6.4 test 2;
- positive N11 — 5/5, proof state unchanged;
- structural suite — `PASS=14 FAIL=0 SKIP=0`.

Post-merge stable-main certification:

- Gate T LaTeX preflight #983 / `33121966942` — SUCCESS including reference/PDF-A, 12-profile matrix/PDF-A, objects/bibliography, post-textuals, structural suite, Overleaf/TeX Live 2025, Windows literal build and Windows literal Unicode/embedding/PDF-A certification;
- PDF validator #130 / `33121959909` — source contract and GitHub Pages deploy SUCCESS;
- Distribution #232 / `33121959982` — SUCCESS through Gate T, release preflight, PDF/A-2b, deterministic bundles, Overleaf import proxy, release-candidate upload and aggregate `distribution-preflight`.

N13 is closed. Do not reopen it without a changed predicate/source or a reproducible regression.

## N14 — Web/Lite and CLI/Deep unification

Original product intent, preserved from the v2.1.0 validator work:

- Web/Lite processes the PDF locally in the browser and does not upload file bytes;
- CLI/Deep uses local Poppler/veraPDF tooling for checks unavailable or inappropriate in the browser;
- unavailable deep capabilities in Web/Lite remain review/manual rather than receiving presumed approval.

Current stable baseline already shares the generated normative catalog, but the validation interface still drifts:

- Web/Lite emits camelCase report metadata (`normativeCatalog`, `normativeRule`), while CLI/Deep uses snake_case (`normative_catalog`, `normative_rule`);
- Web/Lite and CLI/Deep expose 25 and 27 current check IDs respectively;
- after canonical aliasing there are 28 check identities: 24 shared, one Web-only and three CLI-only;
- two current aliases require reconciliation: `font.family` → `font.literal` and `font.embedding` → `font.embedded`;
- `font.embedded` and `pdfa.deep` are explicit capability-boundary checks: review-only in Web/Lite, automatic/deep in CLI;
- Web-only baseline: `security.javascript`;
- CLI-only baseline: `security.encrypted`, `pdfa.claim`, `access.pdfua`.

The N14 contract is technical, not normative. `validator/validation-contract.json` is `ACTIVE` and records:

- canonical profiles, states, verdicts and target report schema;
- current IDs and required aliases;
- per-surface capability mode;
- explicit non-equivalence of PDF.js and Poppler measurement backends;
- `normative_contract_changed=false`, `locator_policy_changed=false`, `oracle_tolerances_changed=false`, `proof_state_changed=false`.

N14 is staged to avoid a broad validator rewrite:

1. **N14-A — inventory/contract:** machine-bind the current two surfaces and capability boundaries without behavior changes;
2. **N14-B — adoption:** make both surfaces consume the canonical technical contract, normalize emitted schema/IDs and retain explicit Lite/Deep differences;
3. **N14-C — equivalence/closure:** exercise synthetic cross-surface contract vectors, require zero unresolved aliases/schema drift, revalidate privacy/deep boundaries, then mark N14 `DONE`.

The first N14 receipt must report the observed baseline without claiming closure:

`N14-EVIDENCE validator-inventory status=PASS web_checks=25 cli_checks=27 canonical_checks=28 shared=24 aliases=2 web_only=1 cli_only=3 phase_status=ACTIVE normative_contract_changed=false proof_state_changed=false`

## Repository hygiene and Git policy

The published `main` history must not be rewritten for cosmetic compaction. Protected long-lived branches are `main` and `1.x`. Audit/fix/docs/preview/release-validation branches remain disposable after evidence is represented by PR/merge/Actions history, but physical deletion stays deferred until final cleanup.

Preserve `planning/v2.2.0-normative-verification` until its unique divergent content is explicitly reconciled. Release tags `v*` remain immutable.

## Normative currency

The repository records `ABNT NBR 14724:2024`, corrected version dated 2025-04-01. Current-edition and precedence policy remains governed by `normativa/version-policy.json` and `docs/VIGENCIA-NORMATIVA.md`. N14 does not reopen N1/N2.

## Distribution / CTAN track

- D0–D4: DONE;
- D5 rehearsal: historical PR #36, CLOSED without merge;
- D5 final: BLOCKED by N15;
- D6 CTAN resubmission: BLOCKED by final D5.

Issue #18, bit-reproducible reference PDF metadata/ID, remains open and requires an explicit blocking/non-blocking release decision before final D5.

The UFC institutional mark remains in the source repository but is externalized from public/CTAN bundles.

## Immediate next action

1. validate N14-A on `audit/n14-validator-contract` with `tests/checks/normative_n14_validator_contract.py` through the PDF-validator source gate;
2. require the baseline receipts for 25 Web IDs, 27 CLI IDs, 28 canonical identities, 24 shared identities, two aliases, one Web-only and three CLI-only checks;
3. require browser upload APIs to remain absent and `font.embedded`/`pdfa.deep` to stay review-only on Web/Lite;
4. require the diff to contain no class/runtime formatting changes, no normative predicate/value/locator/tolerance/proof-state changes and no change to `.github/workflows/latex-preflight.yml`;
5. require exact branch comparison against stable main with `behind_by=0` and green PDF-validator/source checks;
6. open the N14-A PR and merge only after the exact audited head is green;
7. re-certify stable main, then begin N14-B adoption from that exact main;
8. leave bulk branch deletion for final repository cleanup.
