# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEP 7

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 7** | Steps 1-6 accepted; deterministic reference PDF and phase-end remain |
| Release | QUEUED | tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED |
| Profile/engine matrix | ACCEPTED |
| Literal Times New Roman/Arial × pdfLaTeX/LuaLaTeX | ACCEPTED — proof `34219229025`; cleanup `35671aef...`, Static `34224224990`, Linux `34224225080` |
| Scientific Article PDF/A-2b | ACCEPTED |
| Distribution/public bundle integrity | ACCEPTED |
| Temporary executors | none active |
| Issue #18 deterministic reference PDF | **ACTIVE — P0 release blocker** |
| Final Certification phase-end regression | queued after Step 7 |

## Step 7 acceptance boundary

A permanent release-verification gate must pin deterministic provenance time, execute at least two independent clean builds of the canonical reference PDF from the same controlled inputs, require identical SHA-256 values and preserve existing PDF validity/font/Unicode/embedding/applicable PDF/A validation. Hash equality alone is not sufficient if other acceptance checks regress.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Issue #18 | deterministic provenance + two controlled clean rebuilds + identical reference-PDF SHA-256 + existing validation preserved |
| Final Certification phase-end | one immutable candidate passes complete gate |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
