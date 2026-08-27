# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-27
Checkpoint: N14-B validator report-contract adoption on `audit/n14-validator-adoption`
Stable main: `6ead459e9fcaa3d5154fef5883dccc8d06ec5a78`
Stable-main source contract: #329 / run `33124342072` — SUCCESS
Stable-main PDF validator: #131 / run `33124342083` — source check and Pages deploy SUCCESS
Stable-main LaTeX preflight: #985 / run `33124342103` — SUCCESS
Stable-main Gate T: #986 / run `33124347158` — SUCCESS
Stable-main Distribution preflight: #233 / run `33124342067` — SUCCESS

This is the single dynamic continuation document for the v2.2.0 normative audit and release. Detailed historical evidence belongs in `normativa/`, `tests/`, Git history, pull requests and GitHub Actions logs.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable normative requirements, locators, precedence and proof policy.
2. `tests/` + GitHub Actions — executable evidence, validator sensitivity and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. this handoff — roadmap state, audit decisions and immediate next action.
6. Git/PR/Actions history — detailed historical evidence.

Technical validator-interface contracts are not normative requirements. N14 uses `validator/validation-contract.json` as a technical interface contract and continues to consume normative content from `normativa/catalog.json` + `normativa/precedence.json`.

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
- no closed scope is reopened without changed source, changed predicate or reproducible regression;
- compile failure is not evidence that a validator rejected a normative violation;
- negative fixtures and validator receipts are instrumentation, not new normative requirements;
- the N12-certified `.github/workflows/latex-preflight.yml` remains untouched unless N12 is explicitly reopened;
- Web/Lite remains private-by-design and does not upload PDF bytes;
- unsupported deep capabilities in Web/Lite remain review/manual and are never presumed approved;
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
| N14 | Web/Lite and CLI/Deep unification | ACTIVE — N14-A merged; N14-B adoption candidate active |
| N15 | full normative certification and release decision | PENDING |

Stable `main` has **14/16 completed phase gates = 87.5%**. N14 remains active and therefore does not increase this metric. This percentage is not a normative-conformity or proof percentage.

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

## N13 — closed

PR #139 closed N13 and squash-merged as `04cc137f6b0930c2f2a32aa4c299005432959f3b` after exact-head validation. Its stable closure remains:

- controlled rendered-PDF negative cases: 5/5;
- mechanism inventory: 7/7 represented, `phase_status=DONE`;
- strict configuration rejection: strict `REPROVADO`, portable `ALERTA` for the same observation;
- PDF/A controlled mutation: readable PDF with unchanged extracted text and veraPDF-specific rejection;
- N11: 5/5;
- structural suite: `PASS=14 FAIL=0 SKIP=0`;
- no proof-state change.

N13 is closed. Do not reopen it without a changed predicate/source or reproducible regression.

## N14-A — contract baseline merged

PR #140, `audit: establish N14 validator contract baseline`, was validated on exact head `224ab8f7d124c283e801e6bb466efcb7b2c29f64`, `behind_by=0`, with exactly five expected files. Its pull-request synthetic merge tree had zero file differences from the audited head.

N14-A evidence:

- Normative source contract #328 — SUCCESS;
- LaTeX preflight #984 / `33123641766` — SUCCESS;
- structural suite — `PASS=14 FAIL=0 SKIP=0`;
- N13 remained 7/7 `DONE`;
- N11 remained 5/5;
- `proof_state_changed=false`.

PR #140 squash-merged as stable main `6ead459e9fcaa3d5154fef5883dccc8d06ec5a78`.

Post-merge stable-main certification is fully green:

- Normative source contract #329 / `33124342072` — SUCCESS;
- PDF validator #131 / `33124342083` — source check and GitHub Pages deploy SUCCESS;
- push LaTeX preflight #985 / `33124342103` — SUCCESS including reference/PDF-A, 12-profile matrix/PDF-A, objects/bibliography, post-textuals, structural `PASS=14 FAIL=0 SKIP=0`, Overleaf/TeX Live 2025, Windows literal build and independent Unicode/embedding/PDF-A certification;
- Gate T #986 / `33124347158` — SUCCESS with the complete required suite;
- Distribution #233 / `33124342067` — SUCCESS through Gate T prerequisite, release preflight, PDF/A-2b, deterministic bundles, Overleaf import proxy, release-candidate upload and aggregate `distribution-preflight`.

N14-A established a technical baseline of 25 Web checks, 27 CLI checks, 28 canonical identities, 24 shared identities, two observed aliases, one Web-only identity and three CLI-only identities. The two baseline aliases were:

- `font.family` → canonical `font.literal`;
- `font.embedding` → canonical `font.embedded`.

That observed baseline remains historical evidence and must not be rewritten away.

## N14-B — report-contract adoption candidate

N14-B normalizes the emitted machine-readable report contract without changing measurement or decision behavior.

Planned/current adoption on `audit/n14-validator-adoption`:

- Web/Lite keeps its existing PDF.js measurement logic and internal check construction;
- Web/Lite normalizes report output at the boundary to canonical IDs and snake_case fields;
- emitted Web aliases become zero while the N14-A alias baseline remains recorded separately;
- Web/Lite emits `normative_catalog`, `normative_rule`, `generated_at` and `mode="web-lite-local"`;
- CLI/Deep retains its existing Poppler/veraPDF measurement logic and canonical IDs;
- CLI/Deep adds the missing report field `mode="cli-deep-local"`;
- both surfaces therefore satisfy the shared target report schema without requiring measurement-backend identity;
- `font.embedded` and `pdfa.deep` remain review-only on Web/Lite and automatic/deep on CLI;
- Web-only `security.javascript` and CLI-only `security.encrypted`, `pdfa.claim`, `access.pdfua` remain explicit capability differences;
- no normative predicate, locator, N5 tolerance, compatibility mapping or proof-state changes;
- no change to `.github/workflows/latex-preflight.yml`.

Expected N14-B receipts:

`N14-EVIDENCE validator-baseline status=PASS web_checks=25 cli_checks=27 canonical_checks=28 shared=24 baseline_aliases=2 web_only=1 cli_only=3 phase_status=ACTIVE normative_contract_changed=false proof_state_changed=false`

`N14-EVIDENCE schema-adoption status=PASS web_case=snake_case cli_case=snake_case emitted_aliases=0 web_mode=web-lite-local cli_mode=cli-deep-local phase_status=ACTIVE normative_contract_changed=false proof_state_changed=false`

`N14-EVIDENCE capability-boundary status=PASS web_lite_upload=false deep_review_only=font.embedded,pdfa.deep measurement_backend_equivalence_required=false proof_state_changed=false`

N14 remains `ACTIVE` after N14-B. Adoption is not phase closure.

## N14-C — remaining closure work

N14-C must independently test semantic contract equivalence across the two surfaces using synthetic vectors. It must require:

- zero unresolved emitted aliases/schema drift;
- the canonical report fields and status/verdict vocabularies on both surfaces;
- consistent normative metadata binding for shared normative checks;
- preserved Web/Lite privacy and deep-capability boundaries;
- explicit treatment of Web-only and CLI-only checks;
- no requirement that PDF.js and Poppler numerical measurements be identical;
- no normative or proof-state change.

Only after N14-C passes and its exact audited head is independently validated may N14 be marked `DONE`.

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

1. validate the N14-B adoption branch against stable main `6ead459e9fcaa3d5154fef5883dccc8d06ec5a78`;
2. require exactly five changed files: `validator/app.js`, `tools/validate-ufc-pdf.py`, `validator/validation-contract.json`, `tests/checks/normative_n14_validator_contract.py`, and this handoff;
3. require `behind_by=0` and the three N14-B receipts above;
4. require PDF-validator/source checks and LaTeX preflight green, with N13 still 7/7 `DONE`, N11 still 5/5 and structural `PASS=14 FAIL=0 SKIP=0`;
5. verify PR merge-ref tree equivalence to the exact branch head when `behind_by=0`;
6. merge N14-B only with the exact audited head;
7. re-certify stable main before beginning N14-C;
8. implement N14-C synthetic cross-surface vectors and close N14 only if every exit criterion remains satisfied;
9. leave bulk branch deletion for final repository cleanup.
