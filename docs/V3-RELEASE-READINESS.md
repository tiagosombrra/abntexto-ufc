# V3.0.0 Release Readiness

Updated: 2026-09-07
Status: ACTIVE — FINAL CERTIFICATION ENTRY

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **CLOSED** | `923d11ef...`; Static `34154045481`; complete Linux `34154045509`, `PASS=36 FAIL=0 SKIP=0`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — ENTRY SYNCHRONIZATION** | merge PR #286, fresh certification branch, then full certification matrix |
| Release | QUEUED | bundles, checksums, tag/GitHub Release and publication verification |

## Current Final Certification entry

| Surface | State |
|---|---|
| Article transition PR | #286 — open until synchronized transition checkpoint is green |
| Transition branch | `feat/v3-scientific-article` |
| Planned certification branch | `cert/v3-final-certification` from updated main |
| Linux release baseline | not yet executed for final certification candidate |
| Profile/engine matrix | queued |
| Literal fonts / Unicode / embedding | queued |
| PDF/A-2b | queued |
| Distribution bundles | queued |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## What still blocks v3.0.0

| Blocker | Severity | Exit condition |
|---|---|---|
| Final Certification branch entry | P0 | PR #286 merged and fresh certification branch synchronized from updated main |
| Linux release/certification matrix | P0 | all applicable profile/engine/certification gates green |
| Literal font and PDF/A evidence | P0 | accepted certification evidence without proprietary-font redistribution |
| Issue #18 reproducibility | P0 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 while existing validation remains green |
| Final Certification phase-end regression | P0 | one immutable candidate passes complete phase-end gate |
| Release | P0 | final documentation, bundles/checksums, `v3.0.0` tag/GitHub Release and publication verification |
| Librarian item 33 | explicit authority gap | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained |

## Active documentation authority

| Surface | Role |
|---|---|
| `release/v3-roadmap.json` | machine state |
| `docs/HANDOFF-V3.0.0.md` | canonical execution handoff |
| `docs/ROADMAP-V3.0.0.md` | readable phase roadmap |
| `docs/V3-SCIENTIFIC-ARTICLE-PHASE-END.md` | accepted article phase-end evidence |
| `docs/V3-FINAL-CERTIFICATION.md` | active certification execution plan |
| `docs/V3-RELEASE-READINESS.md` | release blocker/readiness inventory |
| `docs/UFC-LIBRARIAN-REVIEW.md` | protected 34-point shared review contract |

## Mandatory closeout rule

Every **material advance** updates the relevant operational documents in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Intermediate/scoped checks never close Final Certification. Temporary executors must be removed before bounded checkpoint acceptance.
