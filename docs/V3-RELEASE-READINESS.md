# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEPS 5-6 CLEANUP

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEPS 5-6 CLEANUP** | bounded Step 5/6 technical evidence green; cleanup Static/Linux, Step 4, issue #18 and phase-end remain |
| Release | QUEUED | tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED |
| Profile/engine matrix | ACCEPTED |
| Successful bounded candidate | `13e491d18d46a86835b4ab1d7f331f6f09f38849` |
| Candidate Static/Linux | `34175388673` PASS / `34175388665` PASS |
| Bounded release transport | `34175388675` **SUCCESS**, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Scientific Article PDF/A-2b | **PASS observed**, font embedding PASS |
| Distribution/public bundles | **PASS observed** — 4 ZIP artifacts, checksums PASS, archive integrity PASS |
| Bounded artifact | ID `10037419414`, SHA-256 `e0420e72c4f9afc0d58792ddb1c83df6b3bcdbc8d2db493b53d1b22e0c589da6` |
| Temporary validation transport | removed in current cleanup checkpoint; cleanup CI pending |
| Literal Times New Roman/Arial + Unicode + embedding | PENDING current-candidate Step 4 proof |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## Step 5/6 acceptance boundary

Run `34175388675` proves the bounded technical predicates. It emitted explicit PASS evidence for article PDF/A-2b/font embedding and for distribution bundles with four artifacts, verified SHA256SUMS, archive integrity, deterministic provenance epoch and no proprietary-font redistribution.

Per the temporary-executor lifecycle, Steps 5-6 are not marked ACCEPTED until the temporary workflow is removed and the cleanup checkpoint passes Static and Linux.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Steps 5-6 cleanup | temporary executor absent + cleanup Static/Linux green |
| Literal-font/Unicode/embedding | fresh current-candidate Times New Roman/Arial identity, Unicode extraction and embedding evidence |
| Issue #18 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 with existing validation preserved |
| Final Certification phase-end | one immutable candidate passes complete gate |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
