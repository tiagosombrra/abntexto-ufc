# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE — Step 1 ACCEPTED; bounded Linux orchestration is the current infrastructure checkpoint before Step 2.**

Accepted foundation:

- Regression Audit — CLOSED;
- Core Corrections — CLOSED on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, Static `33982156041`, Linux `33982156042`;
- Reference PDF Validation — CLOSED on `b64074c64941895f97fbe0f795ce826c798d17ce`, Static `33985595790`, Linux `33985595798`, with complete 55/55 visual PASS;
- Scientific Article Step 1 — ACCEPTED on synchronized checkpoint `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`, Static `34001350884`, Linux `34001350953`, `PASS=31 FAIL=0 SKIP=0`;
- PR #285 — MERGED into `main` as `e6833ed5cf07aaf1021c690260cecfacec1a119a`.

The librarian-review matrix remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed.

Current task branch: `ci/scoped-linux-integration`, created from the merged `main`. This branch is infrastructure-only; Step 2 article runtime begins later on `feat/v3-scientific-article` from the then-current `main`.

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
| **Scientific Article** | **ACTIVE — STEP 1 ACCEPTED / ORCHESTRATION STABILIZATION** | Implement one canonical article profile using the retained 18-rule contract. | Article runtime, article-specific evidence, canonical article rendering and phase-end regression pass on one immutable SHA. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification and release reproducibility proof. | Heavy certification matrix plus deterministic reference-PDF evidence green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Issue #18 resolved; release checklist complete; final regression recorded. |

## Scientific Article execution state

| Step | Work | State | Acceptance gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| Infrastructure | Scoped Linux orchestration | **CURRENT** | documentation-only PR entry, then technical synchronize must select bounded `smoke`; Static and bounded Linux green |
| 2 | Required article front block | NEXT AFTER ORCHESTRATION MERGE | primary title, authorship metadata footnote, submission/approval dates and primary summary have article-specific rendered evidence |
| 3 | Optional foreign elements | QUEUED | foreign title/summary can be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | QUEUED | required article sections and article body typography validated |
| 5 | Recommendations and conditional boundary | QUEUED | recommendations advisory; journal instructions conditional |
| 6 | Evidence hardening | QUEUED | positive/negative evidence rule-specific and proof state truthful |
| 7 | Canonical article PDF | QUEUED | real provenance-bound TeX Live 2026 artifact + complete visual review |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Linux integration policy

Named bounded suites are permitted only for intermediate work. `auto` chooses the narrowest safe suite from changed paths; documentation-only changes skip heavy Linux; unknown/shared/core/standards paths fail closed to `complete`; manual `auto` also resolves to `complete`. The `article` suite must always contain executable article evidence plus the source/validator contract. Multiple known domains run the union of their checks without duplicates.

The phase-end regression scope is always `complete`.

## Branch plan

| Branch | State | Purpose |
|---|---|---|
| `main` | current at `e6833ed...` | canonical merged foundation + article Step 1 |
| `ci/scoped-linux-integration` | ACTIVE | land bounded Linux orchestration only |
| `plan/v3-regression-reset` | HISTORICAL | provenance only; no new work |
| `feat/v3-scientific-article` | NEXT | create from updated `main` after orchestration merge; continue Step 2 |

## Known v3.0.0 blockers

| Item | State | Owner / treatment |
|---|---|---|
| Scientific Article / #280 | ACTIVE | complete Steps 2–8 and phase-end regression |
| Reference PDF bit reproducibility / #18 | OPEN — RELEASE BLOCKER | Final Certification/Release must pin release epoch/`SOURCE_DATE_EPOCH` and prove stable digest |
| Librarian item 33 | NORMATIVE-REVIEW | explicit authority gap; no speculative runtime change |

## Gate before Final Certification

Scientific Article must close with article runtime/evidence complete, accepted canonical article rendering, synchronized documentation, no temporary executor, and one immutable candidate green on Static + `complete` Linux + phase-specific evidence.

## Gate before Release

Final Certification must prove the heavy platform/font/PDF-A/distribution matrix and resolve issue #18. Release then owns final bundles, checksums, tag/release assets and publication verification.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
