# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B2R-A1 implementation candidate — PR #146 (`refactor/n15-b2r-a-internal-naming`)**.

Certified stable `main`: `7699ed205d4554df28fc46908fff3be0b92a38f7`.

The live PR `head_sha` and GitHub Actions receipts are the merge/certification authority. A SHA written in this document is contextual evidence, not a substitute for reading the live PR state.

This is the single dynamic continuation document for the v2.2.0 audit and release. Detailed historical evidence belongs in `normativa/`, `release/`, `tests/`, Git history, pull requests, GitHub Actions logs and `docs/history/`.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable normative sources, rules, locators, precedence and proof policy.
2. `tests/` + GitHub Actions — executable evidence and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. `docs/NAMING.md` — canonical engineering-language, naming and compatibility policy.
6. `release/*.json` — technical audit/release ledgers; these files are not normative sources.
7. this handoff — roadmap state and immediate continuation point.
8. Git/PR/Actions history — detailed historical evidence.

Technical validators and release contracts consume normative requirements; they do not create UFC/ABNT predicates.

## Guardrails

- unavailable authoritative/licensed text remains unavailable or partial;
- green CI does not by itself promote any normative rule to `PROVEN`;
- evidence-only work does not silently alter normative values, locators or tolerances;
- fixture observations do not strengthen stored predicates;
- closed phases reopen only for changed source, changed predicate or reproducible regression;
- compile failure is not proof that a validator rejected a normative violation;
- N12-certified `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- Web/Lite remains private-by-design and does not upload PDF bytes;
- no release may claim official UFC/SiBi approval unless that institutional status actually exists;
- physical bulk branch cleanup remains deferred until final certification/tag and evidence reconciliation;
- engineering identifiers may be normalized to English only under `docs/NAMING.md` and with compatibility evidence;
- Portuguese UFC/ABNT names, document content and historical normative identifiers are not translated merely for code-style consistency;
- public API renaming is additive in v2.x: canonical English surfaces may be introduced, but supported Portuguese surfaces remain compatibility aliases unless a future major-version policy explicitly says otherwise.

## Canonical roadmap

| Phase | Scope | Status |
| --- | --- | --- |
| N0–N14 | frozen normative/runtime/evidence baseline | DONE |
| N15-A | unrestricted final audit | DONE — PR #143 merged and main re-certified |
| N15-B1 | source completeness and authority reconciliation | DONE — PR #144 merged and main re-certified |
| N15-B2A | scientific-article source + normative contract | DONE — PR #145 merged; main `7699ed20...` re-certified |
| N15-B2R-A1 | internal module English naming | ACTIVE — PR #146 implementation candidate |
| N15-B2R-A2 | user example / distribution-facing repository naming | BLOCKED by A1 merge + main certification |
| N15-B2R-B | canonical English public API + Portuguese compatibility aliases | BLOCKED by B2R-A |
| N15-B2B | scientific-article runtime implementation | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | exact-head certification and release decision | BLOCKED by N15-C |

N15 remains ACTIVE. The release is not ready while B2R/B2B/B2C/B3/C/D remain open.

## Frozen N0–N14 baseline

Historical certified baseline:

- full atomic rules: 181;
- normative rules: 170;
- locator coverage: 170/170;
- explicit gaps classified/resolved: 46/46;
- proof state: `PARTIAL=113`, `NOT_PROVEN=51`, `CONDITIONAL=10`, `MANUAL=6`, `NOT_APPLICABLE=1`, `PROVEN=0`;
- N5 tolerances: page size 1 pt, horizontal 5 pt, vertical 5 pt, font size 1 pt;
- N11: exactly five `project.*` predicates, 5/5 bounded positive coverage;
- N12 LaTeX-preflight workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- N13: seven negative mechanisms represented, five controlled rendered-PDF negative cases;
- N14: six of six closure criteria and cross-surface semantic contract certified.

The 181/170 counts are the frozen pre-article baseline. N15-B2A explicitly added source-backed `article.*` predicates; that growth does not retroactively alter N0–N14 evidence.

## N15-B1 — closed

PR #144 completed source completeness and authority reconciliation without article runtime behavior.

Certified resulting `main`:

- SHA `bc7b3bbe0e7ac21aa16efb1f0bab9a4dfb8e912e`;
- Source Contract #345 — SUCCESS;
- PDF Validator #134 — SUCCESS;
- LaTeX preflight #1005 — SUCCESS;
- exact Gate T #1006 — SUCCESS;
- Distribution #237 — SUCCESS.

B1 preserved source history and established the authority model needed for B2A.

## N15-B2A — closed

PR #145 promoted the scientific-article authority set and machine-readable contract while deliberately leaving LaTeX runtime behavior unchanged.

The active UFC article source is:

- `ufc-guia-artigos-2022`;
- bibliographic edition/year: 2022;
- corrected file date: 2023-04-27;
- role: institutional guide, not technical-standard authority.

The earlier `ufc-guia-artigos-2021` identity remains only as reviewed superseded history. The current technical article source is `abnt-nbr-6022-2018` under the conservative evidence model recorded in the source/reconciliation ledgers.

B2A adds 13 `article.*` predicates with dedicated locators and phase metadata. Recommendation language remains recommendation language: 150–250 abstract words, a minimum of three keywords, and Arial/Times guidance are not silently promoted into hard mandatory predicates.

B2A closed with all runtime boundaries intact:

- no `type=article` / `tipo=artigo` runtime surface;
- no article runtime module loaded by the class;
- no article-specific formatting mutation;
- all pre-existing profiles regression-equivalent;
- N12 `latex-preflight.yml` byte-identical to the frozen blob.

Post-merge certified `main`:

- SHA `7699ed205d4554df28fc46908fff3be0b92a38f7`;
- Source Contract #361 — SUCCESS;
- PDF Validator #135 — SUCCESS;
- LaTeX preflight push #1022 — SUCCESS;
- exact Gate T / LaTeX preflight #1023 — SUCCESS;
- Distribution #238 — SUCCESS.

Distribution #238 also passed release preflight, release PDF/A-2b validation, deterministic bundles, the Overleaf import proxy and candidate upload. GitHub Release publication was skipped as expected because the certification was a `main` push without a release tag.

Canonical B2A artifacts include `normativa/coverage-rules-article.json`, `normativa/locator-audit-article.json`, corrected source/catalog/precedence data, `release/n15-b2a-article-contract.json`, and `tests/checks/normative_n15_b2a_article_contract.py`.

## N15-B2R — English naming and public API normalization

B2R is intentionally before article runtime so the article surface is created directly under the final naming architecture.

B2R is behavior-preserving by default and governed by `docs/NAMING.md`.

### N15-B2R-A1 — internal package module paths

A1 is the current mutation scope. It changes internal paths only and must not change public API, normative predicates, formatting, pagination, example layout or article runtime.

Canonical module renames:

- `fontes.def` → `fonts.def`;
- `modulos.def` → `modules.def`;
- `pretextuais.def` → `frontmatter.def`;
- `institucional.def` → `institutional.def`;
- `trabalhos.def` → `academic-works.def`;
- `projetos.def` → `research-projects.def`;
- `objetos.def` → `objects.def`;
- `bibliografia.def` → `bibliography.def`;
- `postextuais.def` → `backmatter.def`.

Retained canonical internal paths include `core.def`, `layout.def`, `compat-abntexto.def` and `compat-nbr6023-2025.def`.

The relative load order is preserved. In particular, `academic-works.def` must load before `research-projects.def`.

A1 implementation evidence:

- inventory ledger: `release/n15-b2r-a-naming-inventory.json`;
- human inventory: `docs/B2R-NAMING-INVENTORY.md`;
- atomic rename commit: `09ceda01ebbc2427ca3bdf109cdcdec06c3bdc3a`;
- PR: #146;
- class module inputs and each `\ProvidesFile` identity updated atomically;
- repository audit dependency names updated;
- dynamic canonical-identity, CTAN-manifest and recursive bundle consumers remain intentionally generic.

A1 exit criteria on the exact merge candidate:

1. no old internal module path is loaded by `abntexto-ufc.cls`;
2. every canonical module exists exactly once;
3. every `\ProvidesFile` path matches the canonical path;
4. module load order is preserved;
5. repository and canonical-identity audits pass;
6. twelve-profile matrix and PDF/A checks pass;
7. reference, layout, pre-textual, project, object, bibliography and post-textual regressions pass;
8. required Overleaf/Windows certification remains green under the existing gate strategy;
9. N12 workflow remains unchanged;
10. PR is `behind_by=0` before merge.

After A1 merge, recertify `main` before A2 begins.

### N15-B2R-A2 — example and distribution-facing repository layout

A2 is separate because these names are visible to template/Overleaf users and distribution tooling.

Candidates to evaluate, not pre-approved renames:

- `documento.tex` → `main.tex`;
- `1-pre-textuais/` → `frontmatter/`;
- `2-textuais/` → `chapters/`;
- `3-pos-textuais/` → `backmatter/`;
- `figuras/` → `figures/`;
- `assets/institucional/` → `assets/institutional/`;
- the institutional image filename → a lowercase English asset name.

Source layout and generated Overleaf-bundle layout may intentionally differ if that gives the best import experience. No A2 rename belongs to A1.

### N15-B2R-B — canonical English public API

Only after B2R-A is certified:

1. define a machine-readable public API inventory;
2. introduce canonical English `\ufcsetup` keys and values;
3. introduce canonical English UFC-owned commands/environments where beneficial;
4. retain supported Portuguese keys/values/commands/environments as compatibility aliases throughout v2.x;
5. distinguish UFC-owned API from upstream compatibility commands;
6. validate canonical-English and Portuguese-compatibility documents against equivalent output/semantics;
7. prevent new unreviewed Portuguese engineering identifiers after migration;
8. document deprecated aliases explicitly rather than removing them silently.

Likely canonical setup vocabulary includes `type`, `print-mode`, `cover`, `catalog-card`, `coat-of-arms`, `font`, `strict-font`, `tables`, `code`, `algorithms`, `glossary`, `index`, `author`, `title`, `subtitle`, `approval-date`, `advisor` and `coadvisor`.

Canonical booleans should use `true/false`; existing `sim/nao` remains compatibility input where currently supported. No public Portuguese API removal belongs to v2.2.0.

## N15-B2B — scientific-article runtime

Begin only from B2R-certified `main`.

The profile is a UFC scientific-article baseline, not a claim to override a target journal's author instructions.

The article runtime module should be created directly under canonical English naming, for example `articles.def`.

Architectural differences already identified:

- general academic-work runtime uses one-and-a-half line spacing;
- primary sections currently invoke a page-break policy;
- article profile requires single spacing and continuous primary-section flow.

Prefer centralized profile capabilities over scattered `if article` checks. Capabilities should express behavior such as cover presence, approval-page presence, body spacing, first-page pagination and section-break policy.

B2B requirements:

1. add canonical `type=article` plus Portuguese compatibility alias/value defined by B2R;
2. create the dedicated article runtime module under canonical naming;
3. implement article metadata and required structure without contaminating academic-work/project modules;
4. implement profile-level capabilities where practical;
5. preserve all existing profile behavior;
6. keep recommendations distinct from mandatory validation;
7. keep target-journal instructions outside the UFC baseline contract.

## N15-B2C — scientific-article evidence closure

After B2B:

- add positive article fixtures;
- add final-PDF measurements/oracles for mandatory article predicates;
- add bounded negative/sensitivity cases where rejection can be demonstrated safely;
- extend engine/PDF-A/profile coverage as applicable;
- validate first-page-visible pagination and continuous section flow;
- validate canonical English API and Portuguese compatibility API for article documents;
- update user/reference documentation;
- extend Web/Lite and CLI/Deep only for checks that genuinely belong to PDF validation;
- run all pre-existing academic-work/project regressions and prove no drift.

B2 closes only when source → predicate → locator → implementation → evidence → documentation is complete for the article profile.

## N15-B3 — remaining pre-release corrections

After B2C:

- resolve issue #18 using two production-reference builds under controlled `SOURCE_DATE_EPOCH` and require exact SHA-256 identity;
- only if that experiment fails, repair nondeterministic PDF metadata/ID generation and retest;
- update remaining stale v2.1.0 release-state wording while preserving historical records;
- determine whether `reference-validation.yml` still has a unique supported role under the current main + Gate T + Distribution strategy;
- resolve additional release blockers exposed by B2R/B2B/B2C;
- keep branch deletion deferred;
- do not promote version metadata yet.

## N15-C — release candidate

Only after B2/B3 are closed:

- atomically promote all release-bearing surfaces to 2.2.0;
- build the production reference twice and require exact SHA-256 identity;
- build class/template/Overleaf/CTAN candidates;
- verify checksums, licensing, allowlists and Overleaf import;
- include the article profile and canonical API documentation in appropriate distribution surfaces;
- keep the UFC institutional mark out of public/CTAN bundles as already established;
- do not redistribute proprietary Microsoft font files.

Historical `release/v2.2.0-certification` / closed PR #36 remains rehearsal evidence only and must not be merged into current main.

## N15-D — final exact-head certification

Require on the exact final candidate:

- complete source contract with all five UFC guides and final article authority model;
- final public-API compatibility contract;
- article-profile evidence plus all legacy profile regressions;
- PDF validator/Pages;
- complete preflight and exact Gate T;
- Distribution aggregate;
- exact two-build reference-PDF reproducibility receipt;
- version/tag consistency;
- zero unresolved release-blocking N15 findings;
- `behind_by=0` and exact audited scope.

Only then make the GO/NO-GO decision for tag `v2.2.0` and CTAN resubmission.

## Distribution / CTAN state

- public GitHub release remains v2.1.0;
- target release remains v2.2.0;
- canonical distribution identity remains `abntexto-ufc`;
- official UFC templates page status must not be represented as approval unless it actually changes;
- CTAN resubmission remains blocked until N15-D GO.

## Repository cleanup policy

Preserve through final certification:

- `main`;
- `1.x`;
- current N15 work branches until merged/released;
- historical rehearsal evidence that has not yet been reconciled.

Physical branch cleanup remains deferred until final v2.2.0 certification/tag. Naming normalization must not be used as an excuse for unrelated branch deletion or history rewriting.

## Immediate next action

1. finish exact-head PR #146 Source Contract and LaTeX regression checks;
2. verify the A1 diff remains limited to the naming inventory, nine module renames, synchronized identities/loading, repository audit and handoff/ledger state;
3. verify PR #146 is mergeable and `behind_by=0`;
4. squash-merge PR #146 only with that exact audited head;
5. re-certify the resulting `main` through Source Contract, PDF Validator, push/manual LaTeX preflight/Gate T and Distribution;
6. mark B2R-A1 DONE and begin B2R-A2 from that certified `main`;
7. complete A2 distribution/Overleaf evidence before B2R-B public API work;
8. begin article runtime B2B only after B2R is certified;
9. keep B2C/B3/C/D and physical branch cleanup blocked until their prerequisites are satisfied.
