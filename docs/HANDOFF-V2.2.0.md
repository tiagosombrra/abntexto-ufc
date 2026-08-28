# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B1 closure candidate — PR #144 (`audit/n15-b1-source-authority`)**.

Certified stable main before N15-B1: `ab61d20c03f9b79e8d01b7913a721c85cd695491`.

Post-N15-A stable-main receipts:

- Normative source contract #340 — SUCCESS;
- LaTeX preflight push #999 — SUCCESS;
- LaTeX preflight exact/manual #1000 — SUCCESS;
- Distribution #236 — SUCCESS.

Current N15-B1 branch receipts:

- Normative source contract #342 — SUCCESS on `58a061bcac779191e79f04eab759a35f94c8f803`;
- N15-B1 source-authority ledger step — SUCCESS;
- LaTeX preflight #1002 — must be green again on the final exact PR head before merge.

This is the single dynamic continuation document for the v2.2.0 audit and release. Detailed historical evidence belongs in `normativa/`, `release/`, `tests/`, Git history, pull requests, GitHub Actions logs and `docs/history/`.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable normative sources, rules, locators, precedence and proof policy.
2. `tests/` + GitHub Actions — executable evidence and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. `release/*.json` — technical audit/release ledgers; these files are not normative sources.
6. this handoff — roadmap state and immediate continuation point.
7. Git/PR/Actions history — detailed historical evidence.

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
- physical bulk branch cleanup remains deferred until final certification/tag and evidence reconciliation.

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
| N15-B1 | source completeness and authority reconciliation | CLOSURE CANDIDATE — PR #144 |
| N15-B2 | UFC scientific-article profile | NEXT |
| N15-B3 | remaining pre-release corrections | BLOCKED by B1/B2 |
| N15-C | v2.2.0 release candidate | BLOCKED by B1/B2/B3 |
| N15-D | exact-head certification and release decision | BLOCKED by N15-C |

N15 remains ACTIVE; the release is not ready while B1–D remain open.

## Frozen N0–N14 baseline

Historical certified baseline, unchanged by B1:

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

The 181/170 counts are the frozen pre-article baseline. N15-B2 may deliberately add source-backed `article.*` predicates. Such growth must be explicit, atomically inventoried, initialized conservatively in proof state and validated independently; it does not retroactively change N0–N14 evidence.

## N15-A — closed

PR #143 established the unrestricted audit and identified seven release blockers. Its substantive findings remain the release agenda:

1. missing fifth UFC guide and article technical-source reconciliation;
2. incomplete graduate-program authority classification;
3. release-dependent source-audit scope;
4. stale current-documentation release-state wording;
5. unresolved exact reference-PDF bit reproducibility (issue #18);
6. release metadata still correctly fixed at published v2.1.0 until N15-C;
7. missing UFC scientific-article runtime profile.

N15-A also explicitly deferred physical branch cleanup and prohibited merging historical rehearsal branches as release source.

## N15-B1 — current closure candidate

PR #144 starts from the re-certified N15-A main and resolves the source/authority blockers without implementing article runtime behavior.

### Source completeness

The audited registry now contains all five current UFC guides:

1. trabalhos acadêmicos;
2. artigo em publicação periódica científica;
3. citações;
4. referências;
5. projetos de pesquisa.

`normativa/source-audit.json` now uses the release-independent scope `abntexto-ufc-current-sources`.

### Scientific-article authority reconciliation

N15-B1 registers/reconciles:

- `ufc-guia-artigos-2021` as a current institutional guide with `technical_authority=false`;
- `abnt-nbr-6022-2018` as the current article-presentation technical source identified by the current review;
- article-guide stale citation mapping `ABNT NBR 10520:2002 → ABNT NBR 10520:2023`;
- article-guide stale reference mapping `ABNT NBR 6023:2018 → ABNT NBR 6023:2025`.

Verification caveat is explicit in `release/n15-b1-source-authority.json`: the public ABNT catalog search surface did not provide a directly indexable NBR 6022 record during automated review. Current-edition reconciliation instead uses the official current UFC guide/page plus current university standards registries; no later replacement was identified. This is recorded as an evidence chain rather than overstated as a direct ABNT-catalog locator.

Most importantly, B1 maintains a strict boundary:

- the article guide and NBR 6022 are **reconciled profile candidates**;
- they do **not** enter `normativa/catalog.json` or `normativa/precedence.json` in B1;
- no `article.*` predicate is created in B1;
- no article LaTeX profile is implemented in B1;
- runtime promotion belongs only to N15-B2 after exact predicates/locators are derived.

### Graduate-program authority reconciliation

B1 classifies the related acts by actual authority:

- **CEPE Resolution 17/2017** remains the general UFC normalization/model-exception regime;
- **CEPE Resolution 17/2015**, Normas Gerais art. 10, X, is current and gives a PPG collegiate body competence to define presentation directives for dissertation, thesis or equivalent work;
- this PPG competence does not invent an automatic template exception: a specific current program directive must be identified, registered, scoped and reconciled before it changes runtime behavior;
- **MEC Portaria 1.224/2013** is recorded as reviewed but excluded because the MEC identifies it as revoked; it has no technical-formatting authority;
- **CAPES Portaria 59/2017** is recorded as a current contextual regulation for the 2017 Quadrennial Evaluation, with `technical_authority=false`.

### B1 executable evidence

Canonical B1 evidence:

- `release/n15-b1-source-authority.json`;
- `tests/checks/normative_n15_b1_source_authority.py`;
- updated `normativa/source-audit.json`;
- updated `normativa/version-policy.json`;
- updated `normativa/reconciliation.json`;
- updated source/currentness checks;
- updated `docs/VIGENCIA-NORMATIVA.md`.

Source Contract #342 passed after synchronizing the reconciliation ledger with the 28/08 source contracts. The successful run confirms:

- 5/5 UFC guides registered;
- 10 current technical standards in the audited source inventory, including the non-runtime article candidate;
- 9 active runtime technical standards remain unchanged;
- 2 reconciled non-runtime article sources;
- 12 stale UFC technical-reference mappings reconciled;
- no article candidate entered runtime prematurely;
- B1 source-authority ledger passed;
- proof-state/false-coverage snapshot generation remained green.

B1 is not DONE until the final PR head has green source contract + full LaTeX preflight, `behind_by=0`, is squash-merged, and resulting `main` is re-certified.

## N15-B2 — next: UFC scientific-article profile

Begin only from the B1-certified main.

The profile must be a dedicated UFC scientific-article baseline, not a claim to override a target journal's own author instructions.

Known article-specific behavior to derive into exact source-backed predicates includes:

- article-specific title/authorship/submission/approval presentation;
- abstract range 150–250 words;
- single line spacing for article body;
- visible pagination from the first page;
- continuous primary-section flow rather than mandatory new-page starts;
- article-specific required structure;
- references as required post-textual content;
- reuse of current citation/reference predicates only where applicability is genuinely shared.

B2 requirements:

1. derive atomic `article.*` rules with exact locators and applicability;
2. add the reconciled article sources to runtime catalog/precedence only together with their consumed rules;
3. initialize new proof-state rows conservatively; no new rule starts `PROVEN`;
4. implement a modular article runtime surface, avoiding scattered conditionals where possible;
5. add positive fixtures and final-PDF measurements;
6. add bounded negative/sensitivity cases where rejection can be demonstrated safely;
7. extend profile/engine/PDF-A coverage as applicable;
8. update human/reference documentation;
9. extend Web/Lite and CLI/Deep only for checks that genuinely belong to PDF validation;
10. run all pre-existing academic-work/project regressions and prove no drift.

B2 closes only when source → predicate → locator → implementation → evidence → documentation is complete for the article profile.

## N15-B3 — remaining pre-release corrections

After B1/B2:

- resolve issue #18 using two production-reference builds under controlled `SOURCE_DATE_EPOCH` and require exact SHA-256 identity;
- only if that experiment fails, repair nondeterministic PDF metadata/ID generation and retest;
- update stale v2.1.0 release-state wording in current documentation while preserving historical records;
- determine whether `reference-validation.yml` still has a unique supported role under the current main + Gate T + Distribution strategy;
- resolve any additional release blocker exposed by B1/B2;
- keep branch deletion deferred;
- do not promote version metadata yet.

## N15-C — release candidate

Only after B1/B2/B3 are closed:

- atomically promote all release-bearing surfaces to 2.2.0;
- build the production reference twice and require exact SHA-256 identity;
- build class/template/Overleaf/CTAN candidates;
- verify checksums, licensing, allowlists and Overleaf import;
- include the article profile in appropriate distribution surfaces;
- keep the UFC institutional mark out of public/CTAN bundles as already established;
- do not redistribute proprietary Microsoft font files.

Historical `release/v2.2.0-certification` / closed PR #36 remains rehearsal evidence only and must not be merged into current main.

## N15-D — final exact-head certification

Require on the exact final candidate:

- complete source contract with all five UFC guides and final article authority model;
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

Review before deletion:

- `planning/v2.2.0-normative-verification`, because it contains divergent historical planning material.

Final cleanup candidates include stale audit/docs/fix/release branches whose evidence is already represented by canonical docs, PRs and Actions, plus `tmp-noop` if it still has no unique content.

Do not bulk-delete before the v2.2.0 final certification/tag.

## Immediate next action

1. require Source Contract green on the final PR #144 exact head;
2. require full LaTeX preflight green on that same final head, including N13/N11/structural regressions;
3. verify PR #144 `behind_by=0` against current `main`;
4. verify no `article.*` predicate/runtime implementation entered B1;
5. squash-merge PR #144 only with the exact audited head;
6. re-certify resulting stable `main`;
7. mark N15-B1 DONE in this handoff;
8. create N15-B2 fresh from that certified `main` and begin the bounded scientific-article contract;
9. leave N15-B3/C/D and physical branch cleanup blocked until their prerequisites are satisfied.
