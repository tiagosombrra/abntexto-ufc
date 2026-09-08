# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEP 7 CLEAN EXECUTOR RERUN

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 7 CLEAN EXECUTOR RERUN** | Steps 1-6 accepted; core deterministic proof PASS; executor cleanup and phase-end remain |
| Release | QUEUED | tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED |
| Profile/engine matrix | ACCEPTED |
| Literal Times New Roman/Arial × pdfLaTeX/LuaLaTeX | ACCEPTED — proof `34219229025`; cleanup `35671aef...` green |
| Scientific Article PDF/A-2b | ACCEPTED |
| Distribution/public bundle integrity | ACCEPTED |
| Step 7 permanent gate | IMPLEMENTED — `make release-reference-reproducibility` in `make release-check` |
| Step 7 core proof | **PASS** — run `34229431523`, source `0040ed413...`, digest `cf00b4ba...c5ac7f` |
| Step 7 wrapper | reporting-only failure after proof; clean rerun required |
| Step 7 temporary executor | ACTIVE until clean rerun; then remove |
| Issue #18 deterministic reference PDF | **ACTIVE — P0 release blocker** |
| Final Certification phase-end regression | queued after Step 7 proof + cleanup |

## Step 7 measured acceptance evidence

The core proof in run `34229431523` established two independent clean builds, deterministic epoch `1788872450` from Git commit time and exact SHA-256 equality at `cf00b4ba784d0e0cd774b080d9cb88cc23b19c4ecc17ace6dc6aa7fc17c5ac7f`. The 450652-byte output passed font embedding, the portable UFC PDF validator, Unicode extraction and PDF/A-2b. Artifact `10057223731` preserved six evidence files for one day.

The run conclusion was `failure` only because the later `Publish proof summary` shell here-document was malformed. The proof step and evidence upload were both successful. This is classified as an executor-reporting defect and does not change any product or proof predicate.

Step 7 is accepted only after the corrected temporary workflow reruns green, the temporary executor is removed, and the cleanup checkpoint passes Static/Linux. This preserves the original fail-closed acceptance boundary.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Issue #18 | clean bounded executor result + temporary-executor cleanup PASS + permanent gate retained |
| Final Certification phase-end | one immutable candidate passes Static, complete Linux and full release/certification matrix |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
