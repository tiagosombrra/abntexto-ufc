# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28
Checkpoint: N14-C cross-surface closure candidate in PR #142 (`audit/n14-cross-surface-closure`)
Stable main before PR #142: `678cb4d776fe24f4ccdb300f36486bfb70c2461e`
Stable-main source contract: #331 / run `33128000046` — SUCCESS
Stable-main PDF validator: #132 / run `33127999931` — source check and Pages deploy SUCCESS
Stable-main LaTeX preflight: #988 / run `33127999949` — SUCCESS
Stable-main Gate T: #989 / run `33128007869` — SUCCESS
Stable-main Distribution preflight: #234 / run `33127999952` — SUCCESS

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
| N14 | Web/Lite and CLI/Deep unification | CLOSURE CANDIDATE — PR #142; contract records 6/6 exit criteria and requires exact-head merge before stable-main closure |
| N15 | full normative certification and release decision | PENDING |

Stable `main` before PR #142 has **14/16 completed phase gates = 87.5%**. Merging the exact validated N14-C head raises the formal roadmap to **15/16 = 93.75%**. These percentages are roadmap-gate metrics, not normative-conformity or proof percentages.

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

## N14-A — baseline merged

PR #140 established the technical validator baseline and squash-merged as `6ead459e9fcaa3d5154fef5883dccc8d06ec5a78` after exact-head validation. The baseline records 25 Web checks, 27 CLI checks, 28 canonical identities, 24 shared identities, two historical aliases, one Web-only identity and three CLI-only identities.

Historical aliases remain evidence and are not rewritten away:

- `font.family` → canonical `font.literal`;
- `font.embedding` → canonical `font.embedded`.

## N14-B — report-contract adoption merged

PR #141, `audit: adopt N14 validator report contract`, normalized the emitted machine-readable report contract without changing measurement or decision behavior and squash-merged as stable main `678cb4d776fe24f4ccdb300f36486bfb70c2461e`.

N14-B preserves the existing measurement backends and adds boundary normalization only:

- Web/Lite keeps PDF.js measurement logic and normalizes emitted IDs/fields to canonical snake_case;
- emitted aliases are zero while the N14-A historical alias baseline remains two;
- Web/Lite emits `normative_catalog`, `normative_rule`, `generated_at` and `mode="web-lite-local"`;
- CLI/Deep keeps Poppler/veraPDF measurement logic and canonical IDs and emits `mode="cli-deep-local"`;
- `font.embedded` and `pdfa.deep` remain review-only on Web/Lite and automatic/deep on CLI;
- Web-only `security.javascript` and CLI-only `security.encrypted`, `pdfa.claim`, `access.pdfua` remain explicit capability differences;
- no normative predicate, locator, N5 tolerance, compatibility mapping or proof-state changed;
- `.github/workflows/latex-preflight.yml` was not changed.

Post-merge stable-main certification is fully green:

- Normative source contract #331 / `33128000046` — SUCCESS with proof-state baseline unchanged and all three N14-B receipts;
- PDF validator #132 / `33127999931` — source check and GitHub Pages deploy SUCCESS;
- push LaTeX preflight #988 / `33127999949` — SUCCESS including reference/PDF-A, 12-profile matrix/PDF-A, objects/bibliography, post-textuals, structural suite, Overleaf/TeX Live 2025, Windows literal build and independent Unicode/embedding/PDF-A certification;
- exact Gate T #989 / `33128007869` — SUCCESS with the complete required suite for `678cb4d...`;
- Distribution #234 / `33127999952` — SUCCESS through Gate T prerequisite, release preflight, PDF/A-2b, deterministic bundles, Overleaf import proxy, release-candidate upload and aggregate `distribution-preflight`.

N14-B adoption remained a phase intermediate; it did not by itself close N14.

## N14-C — closure candidate in PR #142

PR #142 adds no new validator predicate and does not change `validator/app.js`, `tools/validate-ufc-pdf.py`, `normativa/` or `.github/`.

The closure candidate is limited to five files:

1. `validator/validation-vectors.json` — synthetic cross-surface contract vectors;
2. `tests/checks/normative_n14_cross_surface.py` — executes the current Web/Lite contract expressions through Node and the current CLI/Deep `Check`/`verdict()` implementation through Python;
3. `validator/validation-contract.json` — records the N14 closure candidate and six of six exit criteria;
4. `tests/checks/normative_n14_validator_contract.py` — binds N14-C to the existing source contract gate;
5. this handoff.

N14-C requires and emits evidence for:

- five verdict vectors with identical Web/Lite and CLI/Deep semantic outcomes;
- 24 shared canonical identities across 28 canonical checks;
- two historical aliases normalized at the Web report boundary and zero emitted aliases;
- canonical check schema equivalence using the current Web `reportCheck()` output and CLI `Check` serialization;
- zero post-adoption schema drift;
- explicit deep boundaries for `font.embedded` and `pdfa.deep`;
- no requirement for numerical identity between PDF.js and Poppler/veraPDF measurements;
- no change to normative contract, locator policy, N5 tolerances or proof state.

Expected N14-C receipts:

`N14-EVIDENCE cross-surface-vectors status=PASS verdict_vectors=5 shared_checks=24 canonical_checks=28 baseline_aliases=2 emitted_aliases=0 schema_drift=0 deep_boundaries=2 backend_equivalence_required=false proof_state_changed=false`

`N14-EVIDENCE n14-closure status=PASS exit_criteria=6/6 phase_status=DONE normative_contract_changed=false locator_policy_changed=false oracle_tolerances_changed=false proof_state_changed=false`

The technical contract records `status=DONE` inside the candidate so the closure checker can validate the intended terminal state. Formal stable-main closure still requires PR #142 to satisfy `behind_by=0`, exact-head CI, exact file scope and exact-head merge. Until then, N14 is not closed on stable main.

## N15 — pending final certification and release decision

N15 begins only after N14-C is merged and the resulting stable main is re-certified. N15 must not reinterpret prior phase closure as `PROVEN` normative state. Its first action is to derive the final certification/release-decision inventory from the existing normative/proof/distribution contracts and unresolved release blockers, including issue #18.

No N15 implementation should reopen N0–N14 without changed source, changed predicate or reproducible regression.

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

1. validate PR #142 on its final exact head after this handoff update;
2. require exactly the five N14-C files listed above and `behind_by=0`;
3. require the baseline/adoption/capability receipts plus both N14-C receipts;
4. require N13 still 7/7 `DONE`, N11 still 5/5 and structural `PASS=14 FAIL=0 SKIP=0`;
5. verify no changes to normative predicates, locators, frozen N5 tolerances, proof state, `validator/app.js`, CLI implementation or the N12 workflow;
6. verify pull-request merge-ref tree equivalence to the exact audited head when possible;
7. mark PR #142 ready and squash-merge only with the exact audited head;
8. re-certify the resulting stable main with source contract, PDF validator, push preflight, exact Gate T and Distribution;
9. then begin N15 inventory and final release-decision work;
10. leave bulk branch deletion for final repository cleanup.
