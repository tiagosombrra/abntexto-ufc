# V3.0.0 Release Readiness

Updated: 2026-09-07
Status: ACTIVE — RELEASE READINESS TRACKING

## Purpose

Keep repository structure, active plans, issues, branches and release blockers explicit while V3 advances. This document is operational inventory; normative authority remains in the dedicated standards/contracts.

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | green phase-end regression; 34-point librarian contract established |
| Core Corrections | CLOSED | candidate `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | candidate `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | ACTIVE | Step 1 accepted on `08b878a...`; scoped Linux orchestration current; Steps 2–8 remain |
| Final Certification | QUEUED | literal-font/Unicode/embedding/PDF-A/distribution matrix plus release-PDF reproducibility proof |
| Release | QUEUED | release assets, checksums, tag/release publication and final verification |

## Open issue inventory

| Issue | Classification | Release impact | Treatment |
|---|---|---|---|
| #280 Scientific Article | active implementation | BLOCKS Final Certification | keep open until article phase-end regression closes |
| #18 deterministic release reference PDF | release-quality defect | **BLOCKS v3.0.0 Release** | pin release epoch/`SOURCE_DATE_EPOCH`; rebuild from controlled contexts; compare PDF hash and retain evidence |
| #217 historical Linux orchestration | superseded | none | CLOSED; current readable scoped orchestration contract supersedes old opaque work model |

## Active branch model

| Branch | State | Rule |
|---|---|---|
| `main` | canonical and current through PR #285 merge `e6833ed...` | foundation + Scientific Article Step 1 accepted |
| `ci/scoped-linux-integration` | **ACTIVE** | infrastructure-only branch for bounded Linux orchestration; no article Step 2 runtime |
| `feat/v3-scientific-article` | NEXT | create from updated `main` after orchestration merge; continue Step 2 |
| `plan/v3-regression-reset` | historical provenance | no new work |
| older `audit/`, `docs/`, `r3-`, `refactor/`, old `feat/`/`fix/` branches | provenance only | not active authority |

Repository policy remains `main` plus one short-lived active task branch. Historical remote branch cleanup is hygiene and does not override immutable commits, tags, issues, PRs or recorded evidence.

## Active documentation authority

| Surface | Role |
|---|---|
| `release/v3-roadmap.json` | machine state |
| `docs/HANDOFF-V3.0.0.md` | canonical execution handoff |
| `docs/ROADMAP-V3.0.0.md` | readable phase roadmap |
| `docs/V3-SCIENTIFIC-ARTICLE.md` | active phase implementation plan |
| `docs/LINUX-INTEGRATION-SCOPES.md` | bounded Linux orchestration contract |
| `docs/ARTICLE-NORMATIVE-CONTRACT.md` | article source/authority contract |
| `standards/coverage-rules-article.json` | machine article rule contract |
| `docs/UFC-LIBRARIAN-REVIEW.md` | protected 34-point review contract |
| `docs/V3-REFERENCE-PDF-VALIDATION.md` / visual review | accepted academic-work presentation evidence |
| this file | release-readiness inventory |

## Current release blockers

| Blocker | Severity | Exit condition |
|---|---|---|
| Scientific Article incomplete | P0 for v3 feature completeness | Steps 2–8 complete; canonical article PDF visually accepted; phase-end regression green |
| Issue #18 reference-PDF reproducibility | P0 for release reproducibility | deterministic build policy implemented and stable PDF digest demonstrated |
| Final Certification not run on final candidate | P0 | heavy platform/font/PDF-A/distribution matrix green on one immutable SHA |
| Release phase not executed | P0 | bundles/checksums/assets/tag/release verification complete |
| Librarian item 33 authority gap | explicit NORMATIVE-REVIEW | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained |

## Current infrastructure checkpoint

Scoped Linux orchestration is an intermediate engineering optimization, not a release feature and not phase-transition evidence. Acceptance requires a dedicated PR from current `main`, Static contract green, and the technical synchronize event selecting the bounded `smoke` suite for orchestration-only changes. The orchestration PR must merge before `feat/v3-scientific-article` is created.

## Non-blocking repository hygiene

| Finding | State | Decision |
|---|---|---|
| many historical remote branches | open hygiene | provenance-only; active branch policy prevents influence on current state |
| old opaque R2/R3 documents | classified historical | excluded from active authority list |
| old issue #217 | resolved | closed as superseded |
| PR #285 | merged | no longer an integration blocker |

## Mandatory closeout rule

Every phase ends with a complete regression on one immutable SHA. Scoped intermediate Linux runs never close a phase. Final Certification and Release additionally must account for issue #18 so the published V3 reference artifact is reproducible, not merely visually/normatively correct.
