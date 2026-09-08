# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEP 8 PREPARATION

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 8 PREPARATION** | Steps 1-7 accepted; immutable phase-end candidate remains |
| Release | QUEUED | tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Steps 1-7 | **ACCEPTED** |
| Step 7 permanent gate | IMPLEMENTED — `make release-reference-reproducibility` in `make release-check` |
| Step 7 clean proof | PASS — `34231038578` on `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` |
| Deterministic digest | `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` |
| Cleanup checkpoint | `34e6bf8299e582803d1726e8dd699271c356fda5` |
| Cleanup Static | `34232017286` — SUCCESS |
| Cleanup Linux | `34232017359` — SUCCESS, complete, `PASS=36 FAIL=0 SKIP=0` |
| Temporary executor | absent |
| Issue #18 deterministic reference PDF | **CLOSED — COMPLETED** |
| Final Certification phase-end regression | Step 8 preparation |

## Step 7 acceptance evidence

The clean proof `34231038578` established deterministic provenance, two independent clean builds and exact PDF SHA-256 equality. The resulting PDF passed font embedding, portable UFC validation, Unicode extraction and PDF/A-2b. Cleanup checkpoint `34e6bf8...` removed the temporary executor and passed Static plus complete Linux while retaining the permanent reproducibility gate. Issue #18 is therefore closed.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Final Certification phase-end | one immutable candidate passes Static, complete Linux and full release/certification matrix |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Release cannot start until Final Certification is closed.
