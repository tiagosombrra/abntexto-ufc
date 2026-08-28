# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B2A closure candidate — PR #145 (`audit/n15-b2a-article-contract`)**.

Certified stable `main` before N15-B2A: `bc7b3bbe0e7ac21aa16efb1f0bab9a4dfb8e912e`.

The current PR `head_sha` is the merge/certification authority. Do not use a prose SHA in this document as a substitute for reading the live PR state.

Canonical receipts already obtained for the B2A implementation head:

- Source Contract #351 — SUCCESS;
- LaTeX preflight #1012 — SUCCESS;
- all Linux regression jobs in #1012 — SUCCESS;
- Windows/Overleaf jobs in the PR event — intentionally skipped by workflow conditions and reserved for post-merge/main certification.

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
| N0 | freeze / baseline | DONE |
| N1 | normative sources and exact locators | DONE |
| N2 | UFC × current-ABNT reconciliation | DONE |
| N3 | explicit atomicity gaps | DONE |
| N4 | false-coverage audit / proof policy | DONE |
| N5 | final-PDF oracle calibration | DONE |
| N6 | pre-textual elements | DONE |
| N7 | layout, pagination, sections, footnotes | DONE |
| N8 | citations and references | DONE |
| N9 | objects, tables, equations and code | DONE |
| N10 | post-textual elements and multivolume | DONE |
| N11 | research-project profile / NBR 15287 | DONE |
| N12 | profile, engine and font matrix | DONE |
| N13 | negative-path validation | DONE |
| N14 | Web/Lite and CLI/Deep contract unification | DONE |
| N15-A | unrestricted final audit | DONE — PR #143 merged and main re-certified |
| N15-B1 | source completeness and authority reconciliation | DONE — PR #144 merged; main `bc7b3bbe...` re-certified |
| N15-B2A | scientific-article source + normative contract | CLOSURE CANDIDATE — PR #145 |
| N15-B2R-A | repository/internal English naming normalization | BLOCKED by B2A merge + main certification |
| N15-B2R-B | canonical English public API + Portuguese compatibility aliases | BLOCKED by B2R-A |
| N15-B2B | scientific-article runtime implementation | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | exact-head certification and release decision | BLOCKED by N15-C |

N15 remains ACTIVE; the release is not ready while B2A/B2R/B2B/B2C/B3/C/D remain open.

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

The 181/170 counts are the frozen pre-article baseline. N15-B2A deliberately adds source-backed `article.*` predicates. Such growth is explicit and does not retroactively change N0–N14 evidence.

## N15-B1 — closed

PR #144 completed source completeness and authority reconciliation without article runtime behavior.

Resulting certified `main`:

- SHA `bc7b3bbe0e7ac21aa16efb1f0bab9a4dfb8e912e`;
- Source Contract #345 — SUCCESS;
- PDF Validator #134 — SUCCESS;
- LaTeX preflight #1005 — SUCCESS;
- exact Gate T #1006 — SUCCESS;
- Distribution #237 — SUCCESS.

B1 preserved source history and established the authority model needed for B2A. The previous article-guide identity is retained as reviewed superseded history rather than silently rewritten.

## N15-B2A — current closure candidate

PR #145 promotes the scientific-article authority set and machine-readable contract while deliberately leaving LaTeX runtime behavior unchanged.

### Corrected current article source identity

The active UFC source is:

- `ufc-guia-artigos-2022`;
- bibliographic edition/year: 2022;
- corrected file date: 2023-04-27;
- current corrected SiBi/UFC PDF;
- role: institutional guide, not technical-standard authority.

The earlier `ufc-guia-artigos-2021` identity remains only as reviewed superseded history.

The current technical article source is `abnt-nbr-6022-2018` under the conservative evidence model already recorded in the source/reconciliation ledgers.

### Article normative contract

B2A adds 13 `article.*` predicates with dedicated locators and phase metadata. The contract distinguishes mandatory requirements from recommendations.

In particular, the UFC guide's recommendation wording is preserved:

- 150–250 abstract words is a recommendation, not a hard mandatory predicate;
- a minimum of three keywords is a recommendation, not a hard mandatory predicate;
- Arial/Times recommendations are not silently promoted into mandatory technical rules.

B2A also records article-specific requirements needed by the later runtime, including continuous primary-section flow and first-page-visible pagination.

### Deliberate runtime boundary

B2A must close with all of the following still true:

- no `type=article` / `tipo=artigo` runtime surface;
- no article runtime module loaded by the class;
- no article-specific formatting mutation;
- all pre-existing profiles remain regression-equivalent;
- N12 `latex-preflight.yml` remains byte-identical to its frozen blob.

### B2A evidence

Canonical B2A artifacts include:

- `normativa/coverage-rules-article.json`;
- `normativa/locator-audit-article.json`;
- corrected `normativa/source-audit.json`;
- promoted `normativa/catalog.json` and `normativa/precedence.json` entries;
- `release/n15-b2a-article-contract.json`;
- `tests/checks/normative_n15_b2a_article_contract.py`;
- phase-aware historical B1 and N4 checkers.

Implementation-head receipts:

- Source Contract #351 — SUCCESS;
- LaTeX preflight #1012 — SUCCESS, including the 12-profile matrix, PDF/A, reference document, post-textuals, objects/bibliography and layout/fonts/pre-textuals/projects.

After the naming-roadmap documentation commits, the final exact PR head must receive fresh green receipts before merge.

## N15-B2R — English naming and public API normalization

B2R is inserted deliberately **before** article runtime implementation so the new article surface is born under the final naming architecture rather than being created in Portuguese and immediately migrated.

B2R is behavior-preserving by default and is governed by `docs/NAMING.md`.

### N15-B2R-A — repository and internal naming

Goals:

1. inventory internal/public identifiers before mutation;
2. normalize internal implementation filenames and new internal identifiers to English;
3. normalize the user example skeleton to conventional LaTeX/editorial English names where distribution behavior permits;
4. keep official Portuguese names and normative IDs intact;
5. update all imports, build scripts, packaging allowlists, tests and documentation atomically;
6. preserve Overleaf bundle usability, including the chosen root entrypoint contract;
7. prove behavior equivalence across all existing profiles;
8. avoid changing normative predicates or formatting semantics.

Target internal vocabulary includes concepts such as `fonts`, `modules`, `frontmatter`, `backmatter`, `academic-works`, `research-projects`, `objects` and `bibliography`.

A repository move into `examples/` is not automatic: it must first prove no degradation of the Overleaf/import/distribution experience. If necessary, source layout and distributed-bundle layout may intentionally differ.

### N15-B2R-B — canonical English public API

Goals:

1. define the public API inventory as a machine-readable contract;
2. introduce canonical English `\ufcsetup` keys and values;
3. introduce canonical English UFC-owned commands/environments where beneficial;
4. retain supported Portuguese keys/values/commands/environments as compatibility aliases in v2.x;
5. distinguish UFC-owned API from upstream compatibility commands;
6. validate canonical-English and Portuguese-compatibility documents against equivalent output/semantics;
7. prevent new unreviewed Portuguese engineering identifiers after migration;
8. document any deprecated aliases explicitly rather than removing them silently.

Likely canonical setup vocabulary includes `type`, `print-mode`, `cover`, `catalog-card`, `coat-of-arms`, `font`, `strict-font`, `tables`, `code`, `algorithms`, `glossary`, `index`, `author`, `title`, `subtitle`, `approval-date`, `advisor` and `coadvisor`.

Canonical booleans should use `true/false`; existing `sim/nao` remains compatibility input where currently supported.

No public Portuguese API removal belongs to v2.2.0.

## N15-B2B — scientific-article runtime

Begin only from B2R-certified `main`.

The profile must be a dedicated UFC scientific-article baseline, not a claim to override a target journal's own author instructions.

The runtime should use the normalized architecture established by B2R. The article module should therefore be created directly under the canonical English naming scheme (for example `articles.def`) rather than as a temporary Portuguese name.

B2B must also address the architectural differences already identified in the current runtime:

- the general academic-work runtime currently uses one-and-a-half line spacing;
- primary sections currently invoke a page-break policy;
- the article profile requires single spacing and continuous primary-section flow.

Do not solve this with scattered `if article` checks. Prefer profile capabilities or an equivalent centralized profile-policy abstraction so future profiles can express behavior such as cover presence, approval-page presence, body spacing, first-page pagination and section-break policy.

B2B requirements:

1. add canonical `type=article` plus Portuguese compatibility alias/value as defined by B2R;
2. create the dedicated article runtime module under canonical naming;
3. implement article metadata and required structure without contaminating academic-work/project modules;
4. implement profile-level layout capabilities rather than ad-hoc conditionals where practical;
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
- update any remaining stale v2.1.0 release-state wording while preserving historical records;
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

1. require Source Contract and full LaTeX preflight green on the final PR #145 exact head after `docs/NAMING.md`/handoff updates;
2. verify PR #145 remains mergeable and `behind_by=0` against current `main`;
3. squash-merge PR #145 only with that exact audited head;
4. re-certify resulting `main`, including full push/manual/Distribution surfaces needed by the existing gate strategy;
5. mark N15-B2A DONE in this handoff on a fresh B2R branch;
6. begin N15-B2R-A with a read-only API/naming inventory before renaming files;
7. complete B2R-A regression proof before introducing canonical-English public API in B2R-B;
8. begin article runtime B2B only after B2R is certified;
9. leave B2C/B3/C/D and physical branch cleanup blocked until their prerequisites are satisfied.
