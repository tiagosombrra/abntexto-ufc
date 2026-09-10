# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-10
Status: RELEASE — R1.3 implemented, checks pending; publication blocked

This is the shortest safe entry point for a new ChatGPT/Codex conversation or a maintainer returning to the repository. Do not reconstruct the current plan from chat history.

## Start here

1. Resolve branch, HEAD and `origin/main` from Git.
2. Read this file.
3. Read `release/v3.0.1-final-corrections.json`.
4. Read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md`.
5. Continue from `current_next_action` in the machine state.

`AGENTS.md` defines fail-closed precedence and audit rules. Older v3 phase-end/recovery documents remain evidence but do not override this handoff or the active correction state.

## Canonical state

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; resolve current SHA dynamically |
| Historical certified main baseline | `111680cd934a4ea55b02f6ffe730ff5260077565` |
| Baseline status | certified historical evidence, superseded as final publication candidate |
| Active branch | `release/v3.0.1-final-corrections` |
| Tracking issue | #304 |
| Draft PR | #305 |
| Target | `v3.0.1` |
| Publication | BLOCKED |
| Public `v3.0.0` | historical/superseded and must not be retargeted |

The old exact-main certification is no longer the final candidate because release-blocking canonical-reference/distribution and Web/Lite defects were found afterward.

## Current execution

### R0 — DONE

Auditable control plane is established in issue #304, PR #305, `docs/V3.0.1-FINAL-CORRECTION-PLAN.md` and `release/v3.0.1-final-corrections.json`.

### R1.1 — DONE

Seven canonical TCC chapter paths are sequential and semantic. Static #474 failed closed on stale path consumers; those consumers were corrected and Static #475 passed. Evidence: `docs/V3.0.1-R1.1-EVIDENCE.md`.

### R1.2 — DONE

Coverage baseline: `docs/V3.0.1-R1.2-TCC-COVERAGE-MATRIX.md`. Closure evidence: `docs/V3.0.1-R1.2-EVIDENCE.md`.

Historical comparison anchored at `2cbd6d00318ba906e225fa37a4efb724300c3b4e` proves that all seven commented-guide chapter bodies survived to the R1.3 boundary as renames with zero additions/deletions. The user-facing loss was principally artifact role/distribution, not deletion of those chapter bodies. Static #476 passed on the initial matrix commit `1fcc023c50955f6cd62d84a8f03bd7d91ff58932`.

### R1.3 — IMPLEMENTED_PENDING_CHECKS

Evidence: `docs/V3.0.1-R1.3-EVIDENCE.md`.

The bounded rewrite preserves the reviewed corpus and adds missing user-facing guidance. Main changes:

- two local guide callouts: `Como usar no projeto` and `Validação e evidência`;
- coherent `\ufcsetup` explanation;
- explicit pre-textual command/evidence mapping;
- consolidated pagination/duplex explanation;
- dedicated font-embedding guidance distinct from literal-font identity;
- a physical footnote example and footnote evidence route;
- stronger citation command/localizer/`apud` guidance without fictitious locators;
- all seven profiles now named in prose, including `scientific-article`;
- code/algorithm/equation capability versus normative-authority boundary;
- build flow using `make compile`/conditional Biber, glossaries and index;
- CLI/Deep user workflow;
- bounded Web/Lite workflow and explicit Deep-only/E2E boundaries;
- accessibility/manual-review limits without a false PDF/UA claim;
- expanded final delivery checklist.

`template/chapters/6-academic-objects.tex` remains unchanged in this lot to protect its reviewed visual corpus.

Next action: obtain fresh Static and canonical reference/integration evidence on the R1.3 implementation. Any failure must be fixed without weakening existing contracts. Only then mark R1.3 DONE and start R2.

### R2 — PENDING

Treat the full PDF generated from `template/main.tex` as a first-class canonical release reference. Require deterministic build, warning/overflow preflight, A4/geometry, embedded fonts, PDF/A-2b where claimed, CLI/Deep, hash/provenance and page-by-page visual review.

### R3 — PENDING

Repair distribution so the full canonical TCC PDF/source has an explicit public role while the CTAN minimal example retains its independent small-example role.

### R4 — PENDING

Known defect: `validator/app.js` imports `./normative-catalog.js`, but the tracked static validator tree lacks the module. Existing synthetic cross-surface vectors do not prove the actual canonical PDF through the browser analysis path. Fix deterministic catalog generation/deployment, clean module closure and real-PDF positive/negative E2E.

### R5 — PENDING

Certify one final exact SHA with Static, complete Linux Integration, complete Linux Release Check, current CTAN `pkgcheck`, full canonical reference, seven profiles, CLI/Deep, Web/Lite E2E and frozen distribution hashes.

### R6 — PENDING

Maintainer visually approves the full canonical TCC plus seven profile pairs generated from the R5 SHA. No tracked commit or rebuild after acceptance. Tag, GitHub Release bytes and CTAN archive must remain bound to the same candidate.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

## Deferred after v3.0.1

Whole-repository lifecycle cleanup, >100 branch pruning, broad historical-document consolidation and unrelated utility/runtime cleanup remain outside this release correction unless a direct blocker is demonstrated.

## Documentation discipline

Every material advance updates this handoff and `release/v3.0.1-final-corrections.json` in the same work cycle. Lot-specific evidence remains under `docs/`. Issue #304 may record CI receipts after a commit without creating another source commit solely to echo an external workflow result.
