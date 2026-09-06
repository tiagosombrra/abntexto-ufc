# V3.0.0 Release Readiness

Updated: 2026-09-05
Status: ACTIVE — SCIENTIFIC ARTICLE IN PROGRESS

## Purpose

Keep repository structure, active plans, issues, branches and release blockers explicit while V3 advances. This document is operational inventory; normative authority remains in the dedicated standards/contracts.

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | green phase-end regression; 34-point librarian contract established |
| Core Corrections | CLOSED | candidate `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | candidate `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | ACTIVE | Step 1 accepted on `08b878a...`; Required article front block active; Steps 3–8 remain |
| Final Certification | QUEUED | literal-font/Unicode/embedding/PDF-A/distribution matrix plus release-PDF reproducibility proof |
| Release | QUEUED | release assets, checksums, tag/release publication and final verification |

## Integration state

PR #285 is merged into canonical `main` as `e6833ed5cf07aaf1021c690260cecfacec1a119a`. The fresh active branch is `feat/v3-scientific-article`, created from that SHA. This resolves the prior condition in which all new work depended on a large unmerged regression branch.

## Open issue inventory

| Issue | Classification | Release impact | Treatment |
|---|---|---|---|
| #280 Scientific Article | active implementation | BLOCKS Final Certification | keep open until article phase-end regression closes |
| #18 deterministic release reference PDF | release-quality defect | **BLOCKS v3.0.0 Release** | implement pinned release epoch/`SOURCE_DATE_EPOCH`; rebuild in controlled contexts; compare PDF hashes and retain evidence |
| #217 historical Linux orchestration | superseded | none | CLOSED as `not_planned`; current permanent workflows/readable phase model supersede old opaque design |

## Active branch model

| Branch class | State | Rule |
|---|---|---|
| `main` | canonical and updated | contains PR #285 integration; all new task branches start here |
| `feat/v3-scientific-article` | **ACTIVE** | only current branch for Scientific Article work |
| `plan/v3-regression-reset` | historical | no new work; deletion is hygiene only |
| historical `audit/`, `docs/`, `r3-*`, `refactor/`, old `feat/`/`fix/` branches | provenance only | not active authority; do not branch new work from them |

Repository policy remains `main` plus one short-lived active task branch. Historical remote branch cleanup is hygiene and should be performed when repository-maintenance deletion access is available; it does not override immutable commits, tags, issues, PRs or recorded evidence.

## Active documentation authority

| Surface | Role |
|---|---|
| `release/v3-roadmap.json` | machine state |
| `docs/HANDOFF-V3.0.0.md` | canonical execution handoff |
| `docs/ROADMAP-V3.0.0.md` | readable phase roadmap |
| `docs/V3-SCIENTIFIC-ARTICLE.md` | active phase implementation plan |
| `docs/ARTICLE-NORMATIVE-CONTRACT.md` | article source/authority contract |
| `standards/coverage-rules-article.json` | machine article rule contract |
| `docs/UFC-LIBRARIAN-REVIEW.md` | protected 34-point review contract |
| `docs/V3-REFERENCE-PDF-VALIDATION.md` / visual review | accepted academic-work presentation evidence |
| this file | release-readiness inventory |

Historical opaque files such as `docs/R2-API-OWNERSHIP.md`, `docs/R3-*` and `release/v3-r3-*` are provenance artifacts, not active roadmap authority. They must not be edited as if they controlled current work. Deletion is not required for release unless an active test/document proves they are dead conflicting surfaces; Git history already preserves provenance.

## Current release blockers

| Blocker | Severity | Exit condition |
|---|---|---|
| Scientific Article incomplete | P0 for v3 feature completeness | Steps 2–8 complete; canonical article PDF visually accepted; phase-end regression green |
| Issue #18 reference-PDF reproducibility | P0 for release reproducibility | deterministic build policy implemented and stable PDF digest demonstrated |
| Final Certification not run on final candidate | P0 | heavy platform/font/PDF-A/distribution matrix green on one immutable SHA |
| Release phase not executed | P0 | bundles/checksums/assets/tag/release verification complete |
| Librarian item 33 authority gap | explicit NORMATIVE-REVIEW | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained; do not fabricate closure |

## Non-blocking repository hygiene

| Finding | State | Decision |
|---|---|---|
| many historical remote branches | open hygiene | provenance-only; no effect on current machine state or release acceptance |
| old opaque R2/R3 documents | classified historical | excluded from active authority list |
| old issue #217 | resolved | closed as superseded |
| old integration branch `plan/v3-regression-reset` | historical after PR #285 | no new work; remove later when branch-delete maintenance access is available |

## Mandatory closeout rule

Every phase ends with a complete regression on one immutable SHA. Final Certification and Release additionally must account for issue #18 so that the published V3 reference artifact is reproducible, not merely visually/normatively correct.
