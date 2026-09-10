# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-10
Status: RELEASE — R1 canonical TCC reconstruction in progress; publication blocked

This is the shortest safe entry point for a new ChatGPT/Codex conversation or a maintainer returning to the repository. Do not reconstruct the current plan from chat history.

## Start here

1. Resolve branch, HEAD and `origin/main` from Git.
2. Read this file.
3. Read `release/v3.0.1-final-corrections.json`.
4. Read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md`.
5. Continue from `current_next_action` in the machine state.

`AGENTS.md` defines the fail-closed precedence and audit rules. Older v3 phase-end/recovery documents remain evidence, but they do not override this handoff or the active correction state.

## Canonical state

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; resolve current SHA dynamically |
| Historical certified main baseline | `111680cd934a4ea55b02f6ffe730ff5260077565` |
| Baseline status | technically certified historical evidence, superseded as the final publication candidate |
| Active branch | `release/v3.0.1-final-corrections` |
| Tracking issue | #304 |
| Draft PR | #305 |
| Target | `v3.0.1` |
| Publication | BLOCKED |
| Public `v3.0.0` | exists on old SHA and must not be retargeted |

Why the previously certified SHA is no longer the final candidate: after exact-main certification, the maintainer identified user-facing release defects in canonical-reference packaging/identity and the Web/Lite validator deployment/E2E path. Those defects must be corrected before a new exact candidate is certified.

## R0–R6 execution state

### R0 — DONE: auditable control plane

Issue #304, PR #305, the execution plan and machine state define the correction cycle. Broad repository cleanup remains deferred.

### R1.1 — DONE: source identity normalization

The TCC source now uses seven sequential semantic chapter paths:

1. `1-introduction.tex`
2. `2-academic-work-structure.tex`
3. `3-front-matter.tex`
4. `4-general-formatting.tex`
5. `5-citations-notes-references.tex`
6. `6-academic-objects.tex`
7. `7-abntexto-ufc-resources-and-final-review.tex`

The first Static run #474 failed closed because the guide trace/checker still encoded old paths. Those consumers were corrected without weakening their semantics. Static #475 then passed on `5394d2caa3c12ec69c87c38c01302df73c9e59c9`. The failure and rerun remain documented in `docs/V3.0.1-R1.1-EVIDENCE.md`.

### R1.2 — DONE: pedagogical coverage and retention inventory

The baseline coverage matrix is `docs/V3.0.1-R1.2-TCC-COVERAGE-MATRIX.md` and the closure evidence is `docs/V3.0.1-R1.2-EVIDENCE.md`.

Important historical result: commit `2cbd6d00318ba906e225fa37a4efb724300c3b4e` introduced the commented UFC reference guide. Comparing that commit with the pre-R1.3 branch state shows the seven current chapter files as renames with **zero additions and zero deletions**. The previously reviewed pedagogical chapter bodies were therefore not deleted; they survived path migrations. R1.3 must preserve and extend them rather than replace them wholesale.

The matrix also found release-reference gaps that R1.3 must close: font embedding, bounded accessibility guidance, CLI/Deep user workflow, Web/Lite user workflow (final wording waits for R4), coherent `\ufcsetup` explanation, list/profile behavior, citation examples/evidence, code/algorithm authority separation, and consolidated pagination/duplex guidance.

Static #476 passed on the initial R1.2 inventory commit `1fcc023c50955f6cd62d84a8f03bd7d91ff58932`.

### R1.3 — NEXT: coherent TCC rewrite

R1.3 may now edit the canonical guide. It must:

- retain the reviewer-corrected material proven above;
- close the missing/partial topics in the R1.2 matrix;
- add explicit project/API and validation-route guidance instead of only prose about rules;
- preserve normative/institutional/project/example separation;
- keep the undergraduate TCC as the canonical full pedagogical reference and treat scientific article/research-project variations as profiles, not duplicate full guides;
- avoid claiming Web/Lite capabilities that R4 has not yet proved.

After R1.3, a fresh Static + reference/integration run must prove that the source compiles and the guide contracts still hold before R2 starts.

### R2 — PENDING: full canonical PDF

Generate `template/main.pdf` deterministically from the exact candidate source; validate convergence, warnings/overflow, A4/geometry, embedded fonts, PDF/A-2b where claimed, CLI/Deep, provenance/hash and page-by-page visual quality.

### R3 — PENDING: distribution repair

Keep the minimal CTAN example separate from the full canonical TCC. Make the full reference PDF/source a first-class user-facing release artifact in the appropriate GitHub/template distribution. Do not redistribute Microsoft fonts or UFC marks where policy forbids them.

### R4 — PENDING: Web/Lite closure

Confirmed defect: `validator/app.js` imports `./normative-catalog.js`, but the tracked static validator tree lacks that module. Existing cross-surface synthetic vectors also do not run the actual canonical PDF through the browser analysis path. R4 must fix deterministic catalog generation/deployment, verify module closure and add real-PDF E2E with a negative case while preserving Deep-only REVIEW boundaries.

### R5 — PENDING: final exact-SHA regression

One final SHA must pass Static, complete Linux Integration, complete Linux Release Check, current CTAN `pkgcheck`, canonical full-reference gates, seven profile fixtures, CLI/Deep, Web/Lite E2E and deterministic distribution hash checks.

### R6 — PENDING: human acceptance/publication

Maintainer visually reviews the full canonical TCC plus seven profile pairs generated from the exact R5 SHA. After explicit acceptance, no source change or rebuild is allowed. Tag `v3.0.1`, GitHub Release bytes and CTAN source must remain bound to that same SHA/artifact set.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

## Deferred after v3.0.1

Do not allow the current release correction to expand into general cleanup. The >100 branch cleanup, lifecycle classification of the full repository, consolidation of historical/transient docs, and review/removal of uncertain utility scripts belong to the separate post-v3.0.1 regression plan unless a direct release blocker is demonstrated.

## Documentation rule

Every material advance must update `release/v3.0.1-final-corrections.json` and this handoff in the same work cycle. Lot-specific evidence must remain in `docs/`. Issue #304 may mirror completed CI receipts without forcing a source commit solely to record the result of the immediately preceding commit.
