# V3.0.0 Release Readiness

Updated: 2026-09-07
Status: ACTIVE — FINAL CERTIFICATION BASELINE ENTRY

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; Static `34154045481`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — BASELINE ENTRY** | branch `cert/v3-final-certification` from main `22e3c192...`; certification matrix remains |
| Release | QUEUED | bundles, checksums, tag/GitHub Release and publication verification |

## Current certification entry

| Surface | State |
|---|---|
| Scientific Article PR #286 | MERGED |
| Canonical main | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch | `cert/v3-final-certification` |
| Linux release baseline | queued |
| Profile/engine matrix | queued |
| Literal fonts / Unicode / embedding | queued |
| PDF/A-2b | queued |
| Distribution bundles | queued |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## What still blocks v3.0.0

| Blocker | Severity | Exit condition |
|---|---|---|
| Final Certification baseline | P0 | current main-derived branch passes/establishes existing release baseline |
| Complete certification matrix | P0 | all applicable profile/engine/font/Unicode/embedding/PDF-A/distribution gates green |
| Issue #18 reproducibility | P0 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 while existing validation remains green |
| Final Certification phase-end regression | P0 | one immutable candidate passes complete phase-end gate |
| Release | P0 | final documentation, bundles/checksums, `v3.0.0` tag/GitHub Release and publication verification |
| Librarian item 33 | explicit authority gap | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained |

## Mandatory closeout rule

Every **material advance** updates the relevant operational documents in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Intermediate/scoped checks never close Final Certification. Temporary executors must be removed before bounded checkpoint acceptance.
