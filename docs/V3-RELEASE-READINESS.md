# V3.0.0 Release Readiness

Updated: 2026-09-06
Status: ACTIVE — SCIENTIFIC ARTICLE STEP 3

## Purpose

Keep repository structure, active plans, issues, branches and release blockers explicit while V3 advances. This document is operational inventory; normative authority remains in the dedicated standards/contracts.

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | green phase-end regression; 34-point librarian contract established |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE** | Steps 1–2 accepted; Step 3 optional foreign elements active; Steps 4–8 remain |
| Final Certification | QUEUED | literal-font/Unicode/embedding/PDF-A/distribution matrix plus release-PDF reproducibility proof |
| Release | QUEUED | release assets, checksums, tag/release publication and final verification |

## Scientific Article current checkpoint

| Surface | State |
|---|---|
| Step 1 | ACCEPTED — `08b878a...`; Static `34001350884`; Linux `34001350953` |
| Step 2 runtime | IMPLEMENTED at `90293af760c4063b02a16831196ec3d932f1471d` |
| Step 2 validator correction | `bb52697a0e71b2d6a8bc135196f40dba9497b38f`; runtime unchanged |
| Step 2 synchronized acceptance | `0947669c2c096dca93991e042d8ae245754688ba` |
| Step 2 Static | `34026680871` — SUCCESS |
| Step 2 Linux | `34026680882` — SUCCESS, `PASS=31 FAIL=0 SKIP=0` |
| Article evidence | profile PASS and front-block PASS on both engines; no proof-state promotion |
| Step 3 | **ACTIVE — optional foreign title/summary** |

The earlier Step 2 Linux failure `34003838521` remains a classified validator-predicate defect, not a release blocker independent of Scientific Article completion. The corrected synchronized checkpoint is green.

## Integration state

PR #285 is merged into canonical `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`. The active branch is `feat/v3-scientific-article`, tracked by PR #286.

## Open issue inventory

| Issue | Classification | Release impact | Treatment |
|---|---|---|---|
| #280 Scientific Article | active implementation | BLOCKS Final Certification | keep open until article phase-end regression closes |
| #18 deterministic release reference PDF | release-quality defect | **BLOCKS v3.0.0 Release** | implement pinned release epoch/`SOURCE_DATE_EPOCH`; rebuild in controlled contexts; compare PDF hashes and retain evidence |
| #217 historical Linux orchestration | superseded | none | closed/not planned; current permanent workflows supersede it |

## Active branch model

| Branch class | State | Rule |
|---|---|---|
| `main` | canonical | accepted shared foundation |
| `feat/v3-scientific-article` | **ACTIVE** | only current Scientific Article work branch |
| `plan/v3-regression-reset` | historical | no new work |
| other historical branches | provenance only | not active authority |

Repository policy remains `main` plus one short-lived active task branch.

## Active documentation authority

| Surface | Role |
|---|---|
| `release/v3-roadmap.json` | machine state |
| `docs/HANDOFF-V3.0.0.md` | canonical execution handoff |
| `docs/ROADMAP-V3.0.0.md` | readable phase roadmap |
| `docs/V3-SCIENTIFIC-ARTICLE.md` | active phase implementation plan |
| `docs/ARTICLE-NORMATIVE-CONTRACT.md` | article source/authority/modality contract |
| `standards/coverage-rules-article.json` | machine article rule contract |
| `docs/UFC-LIBRARIAN-REVIEW.md` | protected 34-point shared review contract |
| accepted Reference PDF documents | academic-work presentation evidence |
| this file | release-readiness inventory |

## Current release blockers

| Blocker | Severity | Exit condition |
|---|---|---|
| Scientific Article incomplete | P0 feature completeness | Steps 3–8 complete; canonical article PDF visually accepted; phase-end regression green |
| Issue #18 reference-PDF reproducibility | P0 release reproducibility | deterministic build policy and stable digest evidence |
| Final Certification not run on final candidate | P0 | heavy platform/font/PDF-A/distribution matrix green on one immutable SHA |
| Release phase not executed | P0 | bundles/checksums/assets/tag/release verification complete |
| Librarian item 33 authority gap | explicit NORMATIVE-REVIEW | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained |

## Step 3 release-safety boundary

Optional foreign title/summary work must not create a new mandatory article field, reuse ambiguous shared metadata semantics, change article proof state, or activate body typography early. The accepted non-article profile matrix must remain green.

## Mandatory closeout rule

Every **material advance** updates the relevant operational documents in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Final Certification and Release additionally must account for issue #18 so the published V3 reference artifact is reproducible, not merely visually/normatively correct.
