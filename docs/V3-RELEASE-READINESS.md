# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — FINAL CERTIFICATION STEP 8 IMMUTABLE CANDIDATE

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 8 CANDIDATE** | Steps 1-7 accepted; Step 8 transport preparation accepted; immutable final matrix running |
| Release | QUEUED | tag/GitHub Release/publication only after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Steps 1-7 | ACCEPTED |
| Step 7 cleanup | `34e6bf8...`; Static `34232017286`; complete Linux `34232017359` |
| Issue #18 | CLOSED — completed |
| Temporary Step 7 executor | absent |
| Permanent deterministic gate | retained in `make release-check` |
| Step 8 PR transport preparation | ACCEPTED — `4d94e9c...`; Static `34235990523`; complete Linux `34235990383`, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Candidate marker | `release/final-certification-candidate.json` present |
| Final Certification phase-end regression | RUNNING — Static + complete Linux + Linux release check required on same synchronized candidate |

## Remaining blockers

| Blocker | Exit condition |
|---|---|
| Final Certification phase-end | synchronized immutable candidate passes Static + complete Linux + full release/certification matrix |
| Release activation | accepted candidate evidence recorded; marker removed in synchronized transition commit |
| Release execution | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Release cannot start until Final Certification is closed.
