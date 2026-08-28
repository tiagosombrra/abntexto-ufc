# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B2R-A2 read-only inventory — branch `refactor/n15-b2r-a2-user-layout`**.

Certified stable `main`: `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`.

The live branch/PR head and GitHub Actions receipts are the certification authority. A SHA written in this document is contextual evidence, not a substitute for reading live Git state.

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
| N15-B2A | scientific-article source + normative contract | DONE — PR #145 merged and main re-certified |
| N15-B2R-A1 | internal module English naming | DONE — PR #146 merged; main `eefa0659...` re-certified |
| N15-B2R-A2 | user example / distribution-facing repository naming | ACTIVE — read-only consumer inventory |
| N15-B2R-B | canonical English public API + Portuguese compatibility aliases | BLOCKED by A2 |
| N15-B2B | scientific-article runtime implementation | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | exact-head certification and release decision | BLOCKED by N15-C |

N15 remains ACTIVE. The release is not ready while A2/B2R-B/B2B/B2C/B3/C/D remain open.

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

## N15-B2A — closed

PR #145 promoted the scientific-article authority set and machine-readable contract while deliberately leaving LaTeX runtime behavior unchanged.

The active UFC article source is `ufc-guia-artigos-2022`, bibliographic edition/year 2022, corrected file date 2023-04-27. The previous `ufc-guia-artigos-2021` remains reviewed superseded history. The technical article source is `abnt-nbr-6022-2018` under the conservative evidence model recorded in the source/reconciliation ledgers.

B2A adds 13 `article.*` predicates with dedicated locators and phase metadata. Recommendation wording remains recommendation wording: 150–250 abstract words, minimum three keywords and Arial/Times guidance are not silently promoted into hard mandatory predicates.

Post-merge certified `main`:

- SHA `7699ed205d4554df28fc46908fff3be0b92a38f7`;
- Source Contract #361 — SUCCESS;
- PDF Validator #135 — SUCCESS;
- LaTeX preflight push #1022 — SUCCESS;
- exact Gate T #1023 — SUCCESS;
- Distribution #238 — SUCCESS.

B2A closed with no article runtime surface and with the N12 workflow byte-identical to the frozen blob.

## N15-B2R-A1 — closed

PR #146 normalized only internal package-module paths:

- `fontes.def` → `fonts.def`;
- `modulos.def` → `modules.def`;
- `pretextuais.def` → `frontmatter.def`;
- `institucional.def` → `institutional.def`;
- `trabalhos.def` → `academic-works.def`;
- `projetos.def` → `research-projects.def`;
- `objetos.def` → `objects.def`;
- `bibliografia.def` → `bibliography.def`;
- `postextuais.def` → `backmatter.def`.

The relative load order was preserved, especially `academic-works.def` before `research-projects.def`. Public `\ufcsetup` keys/values, document content, normative IDs, example layout and article runtime were not changed.

The first exact-head CI exposed two legitimate stale path consumers. They were corrected without weakening the evidence model:

1. `tests/v2-distribution-check.sh` was synchronized to the canonical internal paths;
2. `tests/checks/normative_n12_matrix.py` gained an explicit rename bridge so the historical N12 manifest/hashes remain unchanged. The bridge reconstructs only the historical `\ProvidesFile` identity before checking the certified blob, so non-rename functional drift still fails certification.

Merged and certified result:

- PR #146 — squash-merged;
- certified `main`: `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`;
- Source Contract #367 — SUCCESS;
- LaTeX preflight push #1030 — SUCCESS;
- exact Gate T / workflow_dispatch #1031 — SUCCESS;
- Distribution #239 — SUCCESS.

Both preflight paths certified reference + PDF/A, structure, objects/bibliography, twelve-profile matrix + PDF/A, post-textuals, public TeX Live 2025 Overleaf proxy, literal Times New Roman/Arial Windows builds, Unicode extraction, embedding and PDF/A-2b.

Distribution #239 additionally passed release preflight, release PDF/A-2b, deterministic bundles, Overleaf import-bundle proxy and candidate upload. GitHub Release publication was skipped as expected for a non-tag `main` push.

No new PDF Validator/Pages run was expected for A1: `.github/workflows/validator-pages.yml` is path-filtered to validator/normative surfaces, and A1 changed none of those paths. The prior B2A PDF Validator #135 remains the relevant unchanged validator-surface certification.

A1 ledger: `release/n15-b2r-a-naming-inventory.json`.

## N15-B2R-A2 — active read-only inventory

A2 starts from certified `main` `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1` on branch `refactor/n15-b2r-a2-user-layout`.

A2 is separate from A1 because its candidate names are visible to template users, Overleaf users, documentation, tooling and distribution bundles. No visible rename is approved merely because an English name looks cleaner.

Candidates to evaluate:

- `documento.tex` → `main.tex`;
- `1-pre-textuais/` → `frontmatter/`;
- `2-textuais/` → `chapters/`;
- `3-pos-textuais/` → `backmatter/`;
- `figuras/` → `figures/`;
- `assets/institucional/` → `assets/institutional/`;
- `brasao-ufc.PNG` → a lowercase canonical asset name.

For every candidate, A2 must inventory:

1. source-document references;
2. Makefile/build/check consumers;
3. test/fixture consumers;
4. README/user documentation consumers;
5. release/CTAN/template/Overleaf packaging behavior;
6. licensing/institutional-mark constraints;
7. import-root expectations and default entrypoint behavior;
8. compatibility cost versus actual user benefit.

Possible outcomes are deliberately broader than “rename everything”:

- rename source and distribution layout together;
- keep source path but translate only generated bundle layout;
- preserve an established user-facing path when migration cost outweighs value;
- defer a candidate if it couples to a later public-API decision.

A2 must not change public setup keys/values, normative predicates, formatting semantics or article runtime.

A2 implementation begins only after a read-only decision matrix is recorded. Once mutations begin, all approved path moves and direct consumers must be updated atomically, followed by exact-head reference/profile/PDF-A/Overleaf/distribution regression proof and post-merge recertification.

## N15-B2R-B — canonical English public API

Only after B2R-A is certified:

1. define a machine-readable public API inventory;
2. introduce canonical English `\ufcsetup` keys and values;
3. introduce canonical English UFC-owned commands/environments where beneficial;
4. retain supported Portuguese keys/values/commands/environments as compatibility aliases throughout v2.x;
5. distinguish UFC-owned API from upstream compatibility commands;
6. validate canonical-English and Portuguese-compatibility documents against equivalent output/semantics;
7. prevent new unreviewed Portuguese engineering identifiers after migration;
8. document deprecated aliases explicitly rather than removing them silently.

Canonical booleans should use `true/false`; existing `sim/nao` remains compatibility input where currently supported. No public Portuguese API removal belongs to v2.2.0.

## N15-B2B — scientific-article runtime

Begin only from B2R-certified `main`.

The profile is a UFC scientific-article baseline, not a claim to override a target journal's author instructions. The article runtime module should be created directly under canonical English naming, for example `articles.def`.

Architectural differences already identified:

- general academic-work runtime uses one-and-a-half line spacing;
- primary sections currently invoke a page-break policy;
- article profile requires single spacing and continuous primary-section flow.

Prefer centralized profile capabilities over scattered `if article` checks.

## N15-B2C — scientific-article evidence closure

After B2B:

- add positive article fixtures;
- add final-PDF measurements/oracles for mandatory article predicates;
- add bounded negative/sensitivity cases where rejection can be demonstrated safely;
- extend engine/PDF-A/profile coverage as applicable;
- validate first-page-visible pagination and continuous section flow;
- validate canonical English API and Portuguese compatibility API for article documents;
- update user/reference documentation;
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
- PDF validator/Pages when relevant surfaces changed;
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

Physical branch cleanup remains deferred until final v2.2.0 certification/tag.

## Immediate next action

1. complete the A2 read-only consumer inventory for every candidate visible path/name;
2. record a decision matrix with compatibility/distribution/Overleaf impact and one recommendation per candidate;
3. approve only the bounded A2 mutation set justified by that matrix;
4. implement approved path moves and direct consumers atomically;
5. run exact-head repository/reference/profile/PDF-A/Overleaf/distribution regressions;
6. merge and re-certify resulting `main` before B2R-B;
7. keep B2R-B/B2B/B2C/B3/C/D and physical branch cleanup blocked until prerequisites are satisfied.
