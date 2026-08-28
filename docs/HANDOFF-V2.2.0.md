# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28
Checkpoint: N15-A final unrestricted audit closure candidate in PR #143 (`audit/n15-final-unrestricted-audit`)
Certified stable main before PR #143: `0a13f4388479f63b9af2d898d3cc0410a4a57c0f`
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
| N15 | final unrestricted audit, source/profile completion, correction, release candidate and release decision | ACTIVE |

Formal roadmap closure remains **15/16 = 93.75%**. This is a phase-gate metric, not normative-conformity or proof percentage.

## Frozen N0–N14 normative baseline

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

The 181/170 counts above are the certified historical N0–N14 baseline. Because N15-A deliberately expands v2.2.0 scope to include the official UFC scientific-article profile, N15-B may intentionally add new `article.*` rules. Any such growth must be explicit, source-backed, atomically inventoried, conservatively initialized in proof-state and independently validated; it is not a retroactive change to the N0–N14 evidence.

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

N15 is intentionally broader than a version bump. The final release is blocked until the official source surface, supported document profiles, reproducibility and release metadata are reconciled together.

### N15-A — final unrestricted audit

PR #143 records the audit as an executable technical ledger without changing runtime, normative predicates, proof state or version. It now also records the deliberate scope decision that the official UFC scientific-article guide will be implemented for v2.2.0 rather than merely listed as out-of-scope.

Candidate file scope remains exactly four files:

1. `release/final-audit.json` — audit dimensions, findings, passes, limitations, article-scope decision and deferred cleanup;
2. `tests/checks/normative_n15_final_audit.py` — machine-checks the ledger against the current source tree and frozen baselines;
3. `.github/workflows/normative-source.yml` — observes the ledger and runs the N15 checker; the N12 preflight workflow is untouched;
4. this handoff.

N15-A records **13 audit dimensions, 13 findings, seven explicit release blockers and six PASS observations**.

Release-blocking findings:

1. the official UFC normalization page lists five institutional guides, but the current active source inventory/checker explicitly models four; the fifth scientific-article guide must be added and reconciled against current technical editions;
2. related UFC graduate-program acts are incompletely classified: CEPE Resolution 17/2015 contains applicable authority for program-level presentation directives and must be reconciled with the general CEPE Resolution 17/2017 regime; the related MEC/CAPES acts must be classified by actual scope;
3. `normativa/source-audit.json` and its checker still carry a v2.1.0-specific scope identifier;
4. `docs/NORMAS.md` still describes the prior v2.1.0/Gate-F release state;
5. issue #18, bit-reproducible reference PDF metadata/ID, remains unresolved and needs an exact two-build SHA-256 proof on the production reference path;
6. version-bearing release surfaces deliberately remain at 2.1.0 and must be promoted atomically only in N15-C;
7. the official UFC scientific-article profile is not implemented even though its requirements materially differ from the existing academic-work and research-project profiles.

The article-profile finding is intentionally separate from the missing-source finding. Source completeness does not prove runtime support, and runtime support cannot be built safely until source authority, current technical editions and exact locators are reconciled.

Non-blocking review/cleanup findings include the older `reference-validation.yml` branch strategy, 131 accumulated remote branches, historical release/N13 branches, `tmp-noop`, and the highly divergent planning branch. Physical deletion is not part of N15-A.

Positive findings include current GitHub protection/immutable-tag rules, explicit reference-image licensing and public-bundle asset restrictions, current N12 Windows helper consumption, conservative proof-state behavior and fully green Distribution #235.

The previous PR #143 preflight #995 had one documentation-only failure: the distribution-identity detector interpreted a sentence in this handoff as a legacy public artifact identity. All 13 other structural checks passed, including N13 7/7, N11 5/5, profile/PDF-A, reference/PDF-A, objects/bibliography and post-textual regressions. The sentence has been rewritten here without changing any runtime or distribution policy; the updated head must be fully revalidated.

### N15-B1 — source completeness and authority reconciliation

Start only after N15-A is merged and stable main is re-certified.

Required work:

- add the fifth official UFC guide, **Guia para Elaboração de Artigo em Publicação Periódica Científica**, to the audited institutional source inventory;
- verify and register the current applicable ABNT article-presentation standard before creating article predicates; current evidence points to ABNT NBR 6022:2018, but current-edition verification is a mandatory gate, not an assumption;
- classify the UFC article guide so embedded superseded technical references cannot choose the governing edition;
- explicitly reconcile its stale references to older citation/reference standards with the already adopted current NBR 10520:2023 and NBR 6023:2025 policy;
- add CEPE Resolution 17/2015 as an applicable institutional source for graduate-program presentation directives and reconcile that authority with the general CEPE Resolution 17/2017 normalization/model-exception framework;
- classify MEC Portaria 1.224/2013 and CAPES Portaria 59/2017 according to their actual operational, deposit or regulatory scope without granting technical formatting authority by implication;
- replace the v2.1.0-specific source-audit scope identifier with a release-independent current-source scope;
- update `docs/VIGENCIA-NORMATIVA.md` and related source/currentness checks to explain the article source set and program-specific exception boundary;
- preserve existing N0–N14 predicates unless the new source reconciliation identifies a genuine conflict that requires explicit review.

Exit criteria for N15-B1:

- five of five official UFC guides present in the audited source registry;
- current article technical standard explicitly verified;
- no stale embedded guide citation can govern technical edition selection;
- CEPE 17/2015 and CEPE 17/2017 authority relationship explicitly modeled;
- no new article runtime predicate yet unless its governing source/locator has been reconciled;
- source contract fully green.

### N15-B2 — UFC scientific-article profile

After B1 establishes source authority, define a bounded article contract and implement a dedicated `artigo` profile without altering the defaults of existing academic-work or research-project profiles.

The official guide review already identified material article-specific behavior that must be modeled instead of inherited blindly:

- article-specific required structure and front matter, including title, authorship and submission/approval-date elements;
- abstract range of **150–250 words** rather than the academic-work 150–500 range;
- article body using **single line spacing** rather than the academic-work 1.5 baseline;
- pagination visible **from the first page**;
- primary article sections continuing on the same page flow instead of forcing each primary section to a new page;
- article-specific title/authorship/presentation layout;
- references as a required post-textual element, with other article post-textual elements classified according to the guide;
- existing current citation/reference rules reused only where their applicability is actually shared.

B2 requirements:

- create source-backed atomic `article.*` rules with exact locators and applicability;
- initialize all new proof-state entries conservatively; no rule starts `PROVEN` by construction;
- implement the profile in a dedicated modular runtime surface rather than scattering article conditionals through unrelated modules where avoidable;
- add positive fixtures and final-PDF measurements for article-only behavior;
- add negative/sensitivity cases for predicates whose validator sensitivity can be demonstrated safely;
- extend the profile/engine test matrix to include the article profile and PDF/A route as applicable;
- update human documentation and the commented reference material so the new profile is discoverable without confusing it with TCC/dissertation/thesis/project profiles;
- extend Web/Lite and CLI/Deep contracts only for article checks that genuinely belong in PDF validation, preserving the N14 semantic-contract rules;
- run the complete pre-existing regression suite to prove that academic-work and research-project behavior did not drift.

The UFC guide itself notes that a target journal may impose different author instructions. Therefore the template's article profile is a **UFC baseline**, not a claim to override journal-specific submission rules. Journal-specific instructions must remain an explicit applicability/override boundary documented for users.

B2 closes only when the article source→rule→implementation→test→documentation chain is complete and the full old profile suite plus the new article profile are green.

### N15-B3 — remaining pre-release corrections

After B1/B2:

- resolve issue #18 by building the production reference path twice under a controlled `SOURCE_DATE_EPOCH` and requiring exact SHA-256 identity; change PDF metadata generation only if the controlled experiment demonstrates it is necessary;
- update stale v2.1.0 audit/release-state wording in current documentation while retaining the v2.1.0 historical audit under `docs/history/`;
- decide whether `reference-validation.yml` still has a unique supported role under the current main + Gate T + Distribution strategy; remove or modernize it only with evidence;
- resolve any additional release-blocking finding exposed by B1/B2 or their exact-head CI;
- keep physical branch deletion deferred;
- do not promote the release version yet.

### N15-C — v2.2.0 release candidate

Only after all release blockers are resolved:

- promote `Makefile`, `abntexto-ufc.cls`, compatibility metadata, CTAN README/changelog and other version-bearing release surfaces atomically to 2.2.0;
- require the canonical `abntexto-ufc` distribution identity and prevent historical public artifact names based on the deprecated compatibility-class identity from returning;
- build the production reference twice under the controlled release epoch and require exact SHA-256 identity;
- build class/template/Overleaf/CTAN candidates, verify checksums, licensing, package allowlists and Overleaf import;
- include the new article-profile runtime/docs/tests in release-package allowlists where appropriate;
- keep the UFC institutional mark externalized from public/CTAN bundles and Microsoft font files undistributed.

The historical `release/v2.2.0-certification` branch / closed PR #36 is rehearsal evidence only. It must never be merged into current main; N15-C is derived fresh from the then-certified main.

### N15-D — final exact-head certification and release decision

Require on the exact final candidate:

- source contract including all five UFC guides and the final article source/currentness model;
- complete article-profile contract/evidence plus all legacy profile regressions;
- PDF validator/Pages;
- complete push/PR preflight;
- exact Gate T including Windows literal-font independent certification and Overleaf;
- Distribution through release preflight, PDF/A-2b, deterministic bundles, Overleaf import and aggregate;
- exact reference-PDF two-build reproducibility receipt;
- version/tag metadata consistency;
- no unresolved release-blocking N15 findings;
- `behind_by=0` and exact audited file scope.

Only then may the project make the GO/NO-GO decision for tag `v2.2.0` and subsequent CTAN resubmission.

## Normative/source completeness guardrail

The current UFC Normalização page, reviewed again during N15-A, lists five guides: trabalhos acadêmicos, artigo científico, citações, referências and projetos de pesquisa. The v2.2.0 scope decision is now explicit: **all five guides are to be represented, and the scientific-article guide will receive a supported article profile**.

This does not authorize copying old technical editions embedded in the article guide into the runtime contract. N15-B1 must first reconcile technical currentness and authority. N15-B2 then creates only the article predicates justified by that reconciled source set.

The current UFC receiving pages also contain institutional/operational acts beyond the active formatting registry. In particular, CEPE Resolution 17/2015 has been identified as relevant to program-level presentation directives and must be modeled as applicable authority. Other acts remain review-required until classified. None selects an ABNT edition merely by being cited.

The official UFC templates page still marks the Overleaf/LaTeX model as `Em atualização`. Do not describe v2.2.0 as an officially published/approved UFC LaTeX template unless institutional status changes.

## Distribution / CTAN track

- D0–D4: DONE;
- D5 rehearsal: historical PR #36, CLOSED without merge;
- N15-A: ACTIVE in PR #143;
- N15-B1/B2/B3: BLOCKED until #143 closes, then required before release candidate;
- D5 final / N15-C-D: BLOCKED by the seven N15 release findings;
- D6 CTAN resubmission: BLOCKED by final GO decision.

The latest public GitHub release remains v2.1.0. The intended v2.2.0 distribution identity is `abntexto-ufc`; no public CTAN availability for `abntexto-ufc` is assumed before successful submission/publication.

## Repository hygiene and cleanup policy

Current N15-A inventory observed 131 remote branches.

Protected long-lived branches remain `main` and `1.x`. Version tags `v*` remain immutable.

Cleanup classes:

- **preserve**: `main`, `1.x`, current N15 work until merged/released;
- **review before deletion**: `planning/v2.2.0-normative-verification` because it has substantial unique historical material;
- **historical rehearsal/reference until N15-C finishes**: `release/v2.2.0-certification` / PR #36;
- **cleanup candidates after release**: stale audit/docs/fix/preview/maintenance branches whose evidence is already represented by merged/closed PRs and Actions;
- **clear cleanup candidate**: `tmp-noop`, which is behind main with no unique changes.

Do not bulk-delete branches before the v2.2.0 final certification/tag. The final cleanup must explicitly reconcile unique planning/history material first.

## Immediate next action

1. validate PR #143 on its new exact head after the article-scope and handoff updates;
2. require exactly the four N15-A files listed above and `behind_by=0`;
3. require the updated N15 receipts with `findings=13`, `release_blockers=7` and `article_profile_in_scope=true`;
4. require proof-state baseline unchanged and frozen N12 workflow blob unchanged;
5. require normal LaTeX preflight regression green with N13 7/7, N11 5/5 and structural `PASS=14 FAIL=0 SKIP=0`;
6. prove pull-request merge-ref tree equivalence to the audited head when possible;
7. mark #143 ready and squash-merge only with the exact audited head;
8. re-certify resulting stable main;
9. begin N15-B1 from that certified main, then N15-B2 article-profile work, then N15-B3 remaining corrections;
10. only after B1/B2/B3 are fully green create N15-C; leave physical branch deletion for the final post-release cleanup pass.
