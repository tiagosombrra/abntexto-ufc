# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEP 4 CLEANUP

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 4 CLEANUP** | Steps 1-3 and 5-6 accepted; Step 4 proof PASS, cleanup Static/Linux pending; issue #18 and phase-end remain |
| Release | QUEUED | tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED |
| Profile/engine matrix | ACCEPTED |
| Steps 5-6 | ACCEPTED |
| Step 4 bounded proof | PASS — `34219229025` on `fae338e16304ad45c353067a0b7982f73a8363c5` |
| Literal Times New Roman/Arial × pdfLaTeX/LuaLaTeX | PASS |
| Unicode extraction / embedding / PDF/A-2b | PASS |
| Proof artifact | generated PDFs only, `10053151610`, one-day retention, digest `sha256:6b0cd0a6ac2543017a8496a1af7feeca70640f2b73862311a4325a981dc5fb60` |
| Temporary Step 4 executor | REMOVED after evidence capture |
| Step 4 acceptance | cleanup Static/Linux pending |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## Step 4 acceptance boundary

The bounded proof satisfied all four family/engine combinations and downstream literal identity, Unicode extraction, embedding and PDF/A-2b checks. No raw proprietary font file was committed or uploaded. The proof-only workflow has been removed. Step 4 becomes ACCEPTED only after the cleanup checkpoint passes Static and Linux.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Step 4 cleanup | Static + Linux green after removal of the temporary workflow |
| Issue #18 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 with existing validation preserved |
| Final Certification phase-end | one immutable candidate passes complete gate |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
