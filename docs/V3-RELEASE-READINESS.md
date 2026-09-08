# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEP 4

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 4** | Steps 1-3 and 5-6 accepted; Step 4, issue #18 and phase-end remain |
| Release | QUEUED | tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED |
| Profile/engine matrix | ACCEPTED |
| Steps 5-6 bounded candidate | `13e491d18d46a86835b4ab1d7f331f6f09f38849` |
| Bounded release transport | `34175388675` SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Steps 5-6 cleanup | `7307164ba4cf924beecb6678c7af5b79d551d513`; Static `34208318971` / Linux `34208318754` SUCCESS |
| Scientific Article PDF/A-2b | **ACCEPTED** |
| Distribution/public bundles | **ACCEPTED** — 4 ZIP artifacts, checksums PASS, archive integrity PASS |
| Temporary validation transport | none active |
| Literal Times New Roman/Arial + Unicode + embedding | **ACTIVE — fresh current-candidate Step 4 proof** |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Literal-font/Unicode/embedding | fresh current-candidate Times New Roman/Arial identity, Unicode extraction and embedding evidence; temporary executor cleanup accepted if used |
| Issue #18 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 with existing validation preserved |
| Final Certification phase-end | one immutable candidate passes complete gate |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
