# V3.0.0 Release Readiness

Updated: 2026-09-07
Status: ACTIVE — SCIENTIFIC ARTICLE STEP 6

## Purpose

Keep repository structure, active plans, issues, branches and release blockers explicit while V3 advances. This document is operational inventory; normative authority remains in the dedicated standards/contracts.

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | green phase-end regression; 34-point librarian contract established |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 6** | Steps 1–5 accepted; branch reconciled with current `main`; evidence hardening active; Steps 7–8 remain |
| Final Certification | QUEUED | literal-font/Unicode/embedding/PDF-A/distribution matrix plus release-PDF reproducibility proof |
| Release | QUEUED | release assets, checksums, tag/release publication and final verification |

## Scientific Article current checkpoint

| Surface | State |
|---|---|
| Step 1 | ACCEPTED — `08b878a...`; Static `34001350884`; Linux `34001350953` |
| Step 2 | ACCEPTED — `0947669...`; Static `34026680871`; Linux `34026680882` |
| Step 3 | ACCEPTED — `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| Step 4 | ACCEPTED — `005956bd...`; Static `34119007413`; Linux `34119007425` |
| Step 5 | ACCEPTED — `55fa1c8...`; Static `34132291198`; Linux `34132291304`; `SCOPE=article PASS=6 FAIL=0 SKIP=0` |
| Step 6 | **ACTIVE** — exact 18-rule evidence map and truthful ownership/proof disposition |
| Article proof policy | conservative; executable validation does not by itself mean `PROVEN` |

## Integration state

| Fact | State |
|---|---|
| Canonical `main` | `789c6f3f4669ae36c3d4fe831ae939a340592568` |
| Shared-foundation integration checkpoint | `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active branch / PR | `feat/v3-scientific-article` / #286 |
| Current-main reconciliation | merge `ae7e2cf2484e0b4329cc30ea80a95d0788e0e9f4` |
| Previous PR mergeability | dirty before reconciliation |
| Reconciliation semantics | preserve branch's newer fail-closed orchestration while recording current-main ancestry |

## Open issue inventory

| Issue | Classification | Release impact | Treatment |
|---|---|---|---|
| #280 Scientific Article | active implementation | BLOCKS Final Certification | keep open until article phase-end regression closes |
| #18 deterministic release reference PDF | release-quality defect | **BLOCKS v3.0.0 Release** | implement pinned release epoch/`SOURCE_DATE_EPOCH`; rebuild in controlled contexts; compare PDF hashes and retain evidence |
| #217 historical Linux orchestration | superseded | none | current scoped workflow supersedes it |

## Active branch model

| Branch class | State | Rule |
|---|---|---|
| `main` | canonical | current accepted integration base |
| `feat/v3-scientific-article` | **ACTIVE** | only current Scientific Article work branch |
| `plan/v3-regression-reset` | historical | no new work |
| other historical branches | provenance only | not active authority |

## Current release blockers

| Blocker | Severity | Exit condition |
|---|---|---|
| Scientific Article incomplete | P0 feature completeness | Steps 6–8 complete; canonical article PDF visually accepted; phase-end regression green |
| Issue #18 reference-PDF reproducibility | P0 release reproducibility | deterministic build policy and stable digest evidence |
| Final Certification not run on final candidate | P0 | heavy platform/font/PDF-A/distribution matrix green on one immutable SHA |
| Release phase not executed | P0 | bundles/checksums/assets/tag/release verification complete |
| Librarian item 33 authority gap | explicit NORMATIVE-REVIEW | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained |

## Step 6 release-safety boundary

Step 6 may harden evidence ownership and validation modes only where direct article-specific executable evidence exists. It may not rewrite source-backed requirement text, modality, locators or applicability without new authority. Recommended rules stay non-enforcing, optional foreign elements stay optional, and target-journal precedence stays conditional-manual.

## Active documentation authority

| Surface | Role |
|---|---|
| `release/v3-roadmap.json` | machine state |
| `docs/HANDOFF-V3.0.0.md` | canonical execution handoff |
| `docs/ROADMAP-V3.0.0.md` | readable phase roadmap |
| `docs/V3-SCIENTIFIC-ARTICLE.md` | active implementation/evidence plan |
| `docs/ARTICLE-NORMATIVE-CONTRACT.md` | article source/authority/modality contract |
| `standards/coverage-rules-article.json` | machine article rule contract |
| `docs/LINUX-INTEGRATION-SCOPES.md` | scoped Linux execution policy |
| `docs/UFC-LIBRARIAN-REVIEW.md` | protected 34-point shared review contract |
| accepted Reference PDF documents | academic-work presentation evidence |
| this file | release-readiness inventory |

## Mandatory closeout rule

Every **material advance** updates the relevant operational documents in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Scoped intermediate Linux runs never close a phase. Final Certification and Release additionally must account for issue #18 so the published V3 reference artifact is reproducible, not merely visually/normatively correct.
