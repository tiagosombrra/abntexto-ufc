# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEP 7 CLEANUP VALIDATION

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 7 CLEANUP VALIDATION** | Steps 1-6 accepted; deterministic proof green; cleanup and phase-end remain |
| Release | QUEUED | tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Steps 1-6 | ACCEPTED |
| Step 7 permanent gate | IMPLEMENTED — `make release-reference-reproducibility` in `make release-check` |
| Step 7 clean proof | **PASS** — run `34231038578` on `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` |
| Deterministic digest | `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` |
| Proof predicates | 2 clean builds; embedding/validator/Unicode/PDF-A all PASS |
| Proof artifact | `10057880627`, 6 files, one-day retention |
| Temporary executor | removed in current cleanup candidate |
| Issue #18 deterministic reference PDF | **ACTIVE — cleanup validation only** |
| Final Certification phase-end regression | queued after Step 7 acceptance |

## Step 7 acceptance evidence

The corrected bounded executor run `34231038578` is fully green. It established source SHA `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522`, deterministic epoch `1788873426` from Git commit time, two independent clean builds and exact SHA-256 equality at `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf`. The 450652-byte output passed font embedding, the portable UFC PDF validator, Unicode extraction and PDF/A-2b.

The temporary proof transport has completed its purpose and is removed in the current cleanup candidate. Step 7 is accepted only after this cleanup candidate passes Static and Linux. This retains the permanent release gate and the original fail-closed boundary.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Issue #18 | cleanup candidate Static/Linux PASS with temporary executor absent and permanent gate retained |
| Final Certification phase-end | one immutable candidate passes Static, complete Linux and full release/certification matrix |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
