# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE; scoped Linux orchestration is ACCEPTED and PR #287 is ready to merge.**

Accepted foundation:

- Regression Audit — CLOSED;
- Core Corrections — CLOSED on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, Static `33982156041`, Linux `33982156042`;
- Reference PDF Validation — CLOSED on `b64074c64941895f97fbe0f795ce826c798d17ce`, Static `33985595790`, Linux `33985595798`, complete 55/55 visual PASS;
- Scientific Article Step 1 — ACCEPTED on merged foundation at `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`, Static `34001350884`, Linux `34001350953`;
- PR #285 — MERGED into `main` as `e6833ed5cf07aaf1021c690260cecfacec1a119a`;
- Scoped Linux orchestration technical checkpoint `47ac2e27c5c2f6797269ccc4e1c07caafea1c643` — Static `34139608322` SUCCESS; Linux `34139608364` SUCCESS, `SCOPE=smoke PASS=4 FAIL=0 SKIP=0`.

The librarian-review matrix remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed.

Current integration branch: `ci/scoped-linux-integration`, PR #287. Existing Scientific Article PR #286 is preserved but paused for advancement until orchestration is merged and its branch is reconciled with updated `main`.

Machine authority: `release/v3-roadmap.json`.  
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.  
Active phase plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.  
Linux scope contract: `docs/LINUX-INTEGRATION-SCOPES.md`.  
Release readiness: `docs/V3-RELEASE-READINESS.md`.

## Operating discipline

Every **material advance** updates the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, article proof/evidence state, integration-scope policy, acceptance state, current work, artifact provenance, release blockers, temporary-executor lifecycle or branch/checkpoint facts also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Scoped or targeted checks are intermediate evidence and never replace the complete closeout regression.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and findings. | Green phase-end regression and stable 34-item contract. |
| **Core Corrections** | CLOSED | Correct shared runtime, template, normative mapping, documentation and tests. | `5f67560a...` passed Static/full Linux. |
| **Reference PDF Validation** | CLOSED | Validate corrected canonical academic-work PDF page by page. | `b64074c...` passed Static/full Linux after provenance + 55/55 visual PASS. |
| **Scientific Article** | **ACTIVE — ORCHESTRATION ACCEPTED / MERGE NEXT** | Implement one canonical article profile using the retained 18-rule contract. | Article runtime, article-specific evidence, canonical article rendering and phase-end regression pass on one immutable SHA. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification and release reproducibility proof. | Heavy certification matrix plus deterministic reference-PDF evidence green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Issue #18 resolved; release checklist complete; final regression recorded. |

## Scoped Linux orchestration result

The first technical synchronize `d089215e...` correctly selected `smoke` but was rejected by Static `34137588226` and Linux `34137588237` because file-spec loading of `tests/run.py` could not resolve sibling `integration_suites`.

The bounded correction `47ac2e27...` made the runner location-independent and added a Static isolated import probe. It passed Static `34139608322` and Linux `34139608364`. Static emitted `runner_file_spec_import=true`; Linux ran exactly the intended `smoke` suite and finished `PASS=4 FAIL=0 SKIP=0`.

The accepted change modifies orchestration robustness only. Suite membership, normative validation, article semantics and runtime behavior are unchanged.

## Scientific Article execution state

| Step | Work | State | Acceptance gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED ON MAIN** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| Infrastructure | Scoped Linux orchestration | **ACCEPTED — PR #287 MERGE NEXT** | `47ac2e27...`; Static `34139608322`; Linux `34139608364` |
| 2–4 | Existing PR #286 feature work | **PRESERVED / PAUSED FOR RECONCILIATION** | reconcile with updated `main`; then obtain executable article-scope evidence for pending structural-checker state |
| 5 | Recommendations and conditional boundary | BLOCKED | resume only after reconciled Step 4 acceptance |
| 6 | Evidence hardening | QUEUED | positive/negative evidence rule-specific and proof state truthful |
| 7 | Canonical article PDF | QUEUED | real provenance-bound TeX Live 2026 artifact + complete visual review |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Linux integration policy

Named bounded suites are permitted only for intermediate work. `auto` chooses the narrowest safe suite from changed paths; documentation-only changes skip heavy Linux; unknown/shared/core/standards paths fail closed to `complete`; manual `auto` also resolves to `complete`. The `article` suite contains executable article evidence plus the source/validator contract. Multiple known domains run the union of their checks without duplicates.

`tests/run.py` must remain executable as the CLI runner and importable by file spec because normative traceability consumes its `CHECKS` registry. Static permanently protects that boundary.

The phase-end regression scope is always `complete`.

## Branch plan

| Branch / PR | State | Purpose |
|---|---|---|
| `main` | current at `e6833ed...` | canonical merged foundation + article Step 1 |
| `ci/scoped-linux-integration` / #287 | **ACCEPTED / READY TO MERGE** | land bounded Linux orchestration |
| `feat/v3-scientific-article` / #286 | **PAUSED / PRESERVED** | existing article work; reconcile with new `main` after #287 |
| `plan/v3-regression-reset` | HISTORICAL | provenance only; no new work |

## Known v3.0.0 blockers

| Item | State | Owner / treatment |
|---|---|---|
| PR #287 orchestration | ACCEPTED / MERGE NEXT | merge, then reconcile PR #286 |
| Scientific Article / #280 and PR #286 | ACTIVE / PAUSED DURING INFRASTRUCTURE | reconcile after #287, validate pending Step 4 executable evidence, then continue |
| Reference PDF bit reproducibility / #18 | OPEN — RELEASE BLOCKER | Final Certification/Release must pin release epoch/`SOURCE_DATE_EPOCH` and prove stable digest |
| Librarian item 33 | NORMATIVE-REVIEW | explicit authority gap; no speculative runtime change |

## Next sequence

1. merge PR #287 after acceptance-document Static remains green;
2. reconcile existing PR #286 with updated `main`;
3. validate the pending Step 4 structure-checker state with executable `article` scope;
4. synchronize accepted article step/proof state;
5. continue Step 5 onward;
6. end Scientific Article only after canonical article visual review and `complete` phase-end regression.

## Gate before Final Certification

Scientific Article must close with article runtime/evidence complete, accepted canonical article rendering, synchronized documentation, no temporary executor, and one immutable candidate green on Static + `complete` Linux + phase-specific evidence.

## Gate before Release

Final Certification must prove the heavy platform/font/PDF-A/distribution matrix and resolve issue #18. Release then owns final bundles, checksums, tag/release assets and publication verification.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
