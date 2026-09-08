# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEP 7 BOUNDED PROOF

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 7 BOUNDED PROOF** | Steps 1-6 accepted; deterministic reference-PDF proof and phase-end remain |
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
| Step 7 permanent gate | IMPLEMENTED — parent `775dfdd6f6fa18475344409ac0bdc491c4435754` |
| Step 7 temporary proof executor | ACTIVE — `.github/workflows/final-cert-step7-repro.yml`, one-day retention |
| Issue #18 deterministic reference PDF | **ACTIVE — P0 release blocker** |
| Final Certification phase-end regression | queued after Step 7 proof + cleanup |

## Step 7 acceptance boundary

The permanent release gate now performs two independent clean builds of the canonical `template/main.pdf`, pins deterministic provenance time, requires exact SHA-256 equality and validates the deterministic output for embedding, portable UFC PDF structure, Unicode extraction and PDF/A-2b. A bounded temporary workflow is active only to execute and transport this proof before merge.

Step 7 is accepted only after the bounded run is green, source SHA/epoch/digest are recorded, the proof artifact is inspected, the temporary workflow is removed, and the cleanup checkpoint remains green. Hash equality alone is insufficient if another PDF acceptance predicate fails.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Issue #18 | bounded deterministic proof PASS + temporary-executor cleanup PASS + permanent gate retained |
| Final Certification phase-end | one immutable candidate passes Static, complete Linux and full release/certification matrix |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
