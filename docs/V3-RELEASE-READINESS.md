# V3.0.0 Release Readiness

Updated: 2026-09-07
Status: ACTIVE — FINAL CERTIFICATION BOUNDED MATRIX VALIDATION

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — BOUNDED MATRIX VALIDATION** | Steps 1-3 accepted; Steps 5-6 persistent gates implemented and awaiting release execution; Step 4, issue #18 and phase-end remain |
| Release | QUEUED | checksums/tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED — `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup `0609f929...` green |
| Profile/engine matrix | ACCEPTED |
| Literal Times New Roman/Arial + Unicode + embedding | PENDING — bounded Step 4 |
| Scientific Article PDF/A-2b | **IMPLEMENTED — release validation pending** |
| Distribution/public bundles | **IMPLEMENTED — release validation pending** |
| Temporary validation transport | `.github/workflows/final-cert-bounded-matrix.yml` active only for current release execution; must be removed before bounded acceptance |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## Frozen remaining scope

There are no open-ended roadmap additions. Any failure in the current transport is classified under Scientific Article PDF/A or distribution integrity. The finite path remains: Step 4 literal-font proof; accept Steps 5-6 after release CI and transport cleanup; issue #18; Final Certification phase-end; Release.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Literal-font/Unicode/embedding | final-candidate Times New Roman/Arial identity, Unicode extraction and embedding evidence |
| Steps 5-6 validation | permanent `make release-check` passes with new article-PDF/A and distribution gates, then temporary workflow is removed and cleanup CI is green |
| Issue #18 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 with existing validation preserved |
| Final Certification phase-end | one immutable candidate passes complete gate |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. A failing check stays inside the frozen acceptance predicate it violates and does not automatically create a new workstream.
