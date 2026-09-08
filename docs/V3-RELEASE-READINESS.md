# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEP 4 BOUNDED PROOF

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 4** | Steps 1-3 and 5-6 accepted; Step 4 bounded proof active; issue #18 and phase-end remain |
| Release | QUEUED | tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED |
| Profile/engine matrix | ACCEPTED |
| Steps 5-6 | ACCEPTED; cleanup `7307164...`, Static `34208318971`, Linux `34208318754` |
| Steps 5-6 sync | `237cb53b65c91052a469ab67991ea78e71ade283`; Static `34218086750`, Linux `34218086734` |
| Temporary Step 4 executor | `.github/workflows/final-cert-literal-fonts.yml` ACTIVE |
| Literal Times New Roman/Arial + Unicode + embedding | **BOUNDED PROOF IN PROGRESS** |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## Step 4 acceptance boundary

The temporary workflow must produce fresh current-candidate proof for Times New Roman and Arial under pdfLaTeX and LuaLaTeX, with literal identity, Unicode extraction, embedding and PDF/A-2b all green. It must upload no raw proprietary font files. After proof capture, the workflow must be removed and cleanup Static/Linux must pass before Step 4 is accepted.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Step 4 literal-font proof | bounded matrix PASS + workflow removed + cleanup Static/Linux green |
| Issue #18 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 with existing validation preserved |
| Final Certification phase-end | one immutable candidate passes complete gate |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
