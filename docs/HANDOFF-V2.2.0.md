# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28
Checkpoint: N15-A final unrestricted audit closure candidate in PR #143 (`audit/n15-final-unrestricted-audit`)
Certified stable main: `0a13f4388479f63b9af2d898d3cc0410a4a57c0f`
Stable-main source contract: #334 — SUCCESS
Stable-main PDF validator: #133 — source check and Pages deploy SUCCESS
Stable-main push LaTeX preflight: #992 — SUCCESS
Stable-main exact Gate T: #993 / run `33130543594` — SUCCESS
Stable-main Distribution: #235 / run `33130538175` — SUCCESS

This is the single dynamic continuation document for the v2.2.0 audit and release. Detailed historical evidence belongs in `normativa/`, `tests/`, Git history, pull requests, GitHub Actions logs and `docs/history/`.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable normative requirements, locators, precedence and proof policy.
2. `tests/` + GitHub Actions — executable evidence, validator sensitivity and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. `release/final-audit.json` — N15 technical audit/release-decision ledger; it is not a normative source.
6. this handoff — roadmap state, audit decisions and immediate next action.
7. Git/PR/Actions history — detailed historical evidence.

Technical validator/release contracts are not normative requirements. They consume normative content but do not create new UFC/ABNT predicates.

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
- PDF.js and Poppler/veraPDF remain different measurement backends; numerical backend identity is not required;
- no final release may claim official UFC/SiBi approval unless such approval/publication actually exists;
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
| N13 | negative fixtures / negative-path validation | DONE — 7/7 mechanisms represented and sensitivity-tested |
| N14 | Web/Lite and CLI/Deep contract unification | DONE — 6/6 closure criteria; cross-surface vectors certified |
| N15 | final unrestricted audit, correction, release candidate and release decision | ACTIVE |

Formal roadmap closure is **15/16 = 93.75%**. This is a phase-gate metric, not normative-conformity or proof percentage.

## Frozen normative baseline

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

N12 remains the factorized 20-cell certification. Literal Windows identity is certified only on the Windows route. The certified `.github/workflows/latex-preflight.yml` blob remains `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## N13 and N14 — closed

N13 is closed on stable main and remains re-certified with:

- controlled rendered-PDF negative cases: 5/5;
- mechanism inventory: 7/7 represented;
- strict configuration rejection sensitivity;
- PDF/A controlled negative mutation sensitivity;
- N11: 5/5;
- structural suite: `PASS=14 FAIL=0 SKIP=0`;
- no proof-state change.

N14 closed through PRs #140, #141 and #142. Stable main now has:

- 28 canonical validator identities;
- 24 shared identities;
- historical alias baseline retained, but zero aliases emitted after adoption;
- canonical snake_case reports with explicit Web/Lite and CLI/Deep modes;
- five semantic cross-surface verdict vectors;
- six of six N14 closure criteria;
- no change to normative predicates, locators, N5 tolerances or proof state.

The post-N14 stable main `0a13f438...` is fully certified by Source #334, PDF Validator #133, push preflight #992, exact Gate T #993 and Distribution #235. Gate T reconfirmed N13 5/5 + 7/7, N11 5/5 and structural `PASS=14 FAIL=0 SKIP=0`. Distribution reconfirmed release preflight, PDF/A-2b, deterministic bundles, Overleaf import proxy, candidate upload and aggregate.

## N15 — final phase structure

N15 is intentionally broader than a version bump.

### N15-A — final unrestricted audit

PR #143 records the audit as an executable technical ledger without changing runtime, normative rules, proof state or version.

Candidate file scope is exactly four files:

1. `release/final-audit.json` — audit dimensions, findings, passes, limitations and deferred cleanup;
2. `tests/checks/normative_n15_final_audit.py` — machine-checks the ledger against the current source tree and frozen baselines;
3. `.github/workflows/normative-source.yml` — observes the ledger and runs the N15 checker; the N12 preflight workflow is untouched;
4. this handoff.

N15-A currently records 13 audit dimensions, 12 findings, six explicit release blockers and six PASS observations.

Release-blocking findings:

1. the official UFC normalization page lists five guides, while the active registry/checker explicitly models four; the article guide must be recorded as reviewed/out-of-scope unless an article profile is deliberately added;
2. related deposit/academic acts listed by the current UFC receiving page must be explicitly classified as operational/contextual or applicable, without granting technical authority by implication;
3. `normativa/source-audit.json` and its checker still carry a v2.1.0-specific scope identifier;
4. `docs/NORMAS.md` still describes the prior v2.1.0/Gate-F release state;
5. issue #18, bit-reproducible reference PDF metadata/ID, remains unresolved and needs an exact two-build SHA-256 proof on the production reference path;
6. version-bearing release surfaces deliberately remain at 2.1.0 and must be promoted atomically only in N15-C.

Non-blocking review/cleanup findings include the older `reference-validation.yml` branch strategy, 131 accumulated remote branches, historical release/N13 branches, `tmp-noop`, and the highly divergent planning branch. Physical deletion is not part of N15-A.

Positive findings include current GitHub protection/immutable-tag rules, explicit reference-image licensing and public-bundle asset restrictions, current N12 Windows helper consumption, conservative proof-state behavior and fully green Distribution #235.

### N15-B — corrections and reconciliation

After N15-A is accepted:

- add explicit reviewed-out-of-scope/context source classification and reconcile the official five-guide inventory;
- classify related UFC deposit/academic acts without changing technical authority unless a real applicable predicate is found;
- remove stale v2.1.0 scope/status wording from current audit metadata/docs;
- decide whether the legacy reference-validation workflow has a unique supported role;
- implement and prove reference-PDF reproducibility for issue #18;
- fix any additional N15-A finding discovered by exact-head CI or review;
- do not promote the release version yet unless the correction itself requires a candidate-only version context.

### N15-C — v2.2.0 release candidate

Only after all release blockers are resolved:

- promote `Makefile`, `abntexto-ufc.cls`, compatibility metadata, CTAN README/changelog and other version-bearing release surfaces atomically to 2.2.0;
- require the current `abntexto-ufc` distribution identity and prevent historical `ufctex-*` public artifact names from returning;
- build the production reference twice under the controlled release epoch and require exact SHA-256 identity;
- build class/template/Overleaf/CTAN candidates, verify checksums, licensing, package allowlists and Overleaf import;
- keep the UFC institutional mark externalized from public/CTAN bundles and Microsoft font files undistributed.

The historical `release/v2.2.0-certification` branch / closed PR #36 is rehearsal evidence only. It must never be merged into current main; N15-C is derived fresh from the then-certified main.

### N15-D — final exact-head certification and release decision

Require on the exact final candidate:

- source contract;
- PDF validator/Pages;
- complete push/PR preflight;
- exact Gate T including Windows literal-font independent certification and Overleaf;
- Distribution through release preflight, PDF/A-2b, deterministic bundles, Overleaf import and aggregate;
- version/tag metadata consistency;
- no unresolved release-blocking N15 findings;
- `behind_by=0` and exact audited file scope.

Only then may the project make the GO/NO-GO decision for tag `v2.2.0` and subsequent CTAN resubmission.

## Normative/source completeness guardrail

The current UFC Normalização page, reviewed again during N15-A, lists five guides: trabalhos acadêmicos, artigo científico, citações, referências and projetos de pesquisa. The template currently has no article profile. The correct response is explicit classification, not silent omission and not automatic scope expansion.

The current UFC receiving pages also contain operational/context acts beyond the active formatting registry. N15-B must make review completeness visible while preserving `normativa/version-policy.json`: stale/operational acts do not select technical ABNT editions or gain technical authority by mere citation.

The official UFC templates page still marks the Overleaf/LaTeX model as `Em atualização`. Do not describe v2.2.0 as an officially published/approved UFC LaTeX template unless institutional status changes.

## Distribution / CTAN track

- D0–D4: DONE;
- D5 rehearsal: historical PR #36, CLOSED without merge;
- N15-A: ACTIVE in PR #143;
- D5 final / N15-C-D: BLOCKED by the six N15 release findings;
- D6 CTAN resubmission: BLOCKED by final GO decision.

The latest public GitHub release remains v2.1.0. The intended v2.2.0 distribution identity is `abntexto-ufc`; no public CTAN availability for `abntexto-ufc` is assumed before successful submission/publication.

## Repository hygiene and cleanup policy

Current N15-A inventory observed 131 remote branches and no open pull request before PR #143 was created.

Protected long-lived branches remain `main` and `1.x`. Version tags `v*` remain immutable.

Cleanup classes:

- **preserve**: `main`, `1.x`, current N15 work until merged/released;
- **review before deletion**: `planning/v2.2.0-normative-verification` because it is 55 commits ahead and 107 behind main with substantial unique historical material;
- **historical rehearsal/reference until N15-C finishes**: `release/v2.2.0-certification` / PR #36;
- **cleanup candidates after release**: stale audit/docs/fix/preview/maintenance branches whose evidence is already represented by merged/closed PRs and Actions;
- **clear cleanup candidate**: `tmp-noop`, which is behind main with no unique changes.

Do not bulk-delete branches before the v2.2.0 final certification/tag. The final cleanup must explicitly reconcile unique planning/history material first.

## Immediate next action

1. validate PR #143 on its final exact head after this handoff update;
2. require exactly the four N15-A files listed above and `behind_by=0`;
3. require both N15 receipts from `normative_n15_final_audit.py`;
4. require the proof-state baseline unchanged and frozen N12 workflow blob unchanged;
5. require normal LaTeX preflight regression green with N13 7/7, N11 5/5 and structural `PASS=14 FAIL=0 SKIP=0`;
6. prove pull-request merge-ref tree equivalence to the audited head when possible;
7. mark #143 ready and squash-merge only with the exact audited head;
8. re-certify resulting main;
9. begin N15-B from that certified main and resolve the six release blockers without prematurely promoting version 2.2.0;
10. leave physical branch deletion for the final post-release cleanup pass.
