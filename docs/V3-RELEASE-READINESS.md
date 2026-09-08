# V3.0.0 Release Readiness

Updated: 2026-09-07
Status: ACTIVE — FINAL CERTIFICATION STEP 6 CANONICAL-CHECKOUT CORRECTION

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 6 CORRECTION** | Steps 1-3 accepted; Step 5 PASS observed twice; Step 6 runner correction active; Steps 4, 7 and phase-end remain |
| Release | QUEUED | checksums/tag/GitHub Release/publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | ACCEPTED |
| Linux release baseline | ACCEPTED — `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup `0609f929...` green |
| Profile/engine matrix | ACCEPTED |
| First bounded transport | `21455c3344...` / `34172047786`: release 38/38, Step 5 PASS, Step 6 Git ownership failure during epoch read |
| Second bounded transport | `247e31398...` / `34173496336`: release 38/38, Step 5 PASS, Step 6 canonical-checkout detection failure during tracked-file discovery |
| Second checkpoint Static/Linux | `34173496318` / `34173496285`: PASS / PASS |
| Second diagnostic artifact | ID `10036808737`, SHA-256 `c56e1c651ce990ddd5a301c5cf60691b1081a06b7eebe66b27503e256e28e273` |
| Scientific Article PDF/A-2b | **PASS observed twice** — bounded acceptance pending Step 6 green + cleanup |
| Distribution/public bundles | **CORRECTION ACTIVE** — configure container-local Git trust before persistent release contract |
| Literal Times New Roman/Arial + Unicode + embedding | PENDING current-candidate Step 4 proof |
| Temporary validation transport | `.github/workflows/final-cert-bounded-matrix.yml` active for corrected rerun; must be removed before Steps 5-6 acceptance |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## Step 6 correction

The first correction fixed exact-source epoch derivation but the second run proved a later Git consumer still failed. `build-distribution-bundles.py` and `build-public-bundles.py` call `git ls-files` to define the canonical tracked-file set. Inside the TeX Live action container, that Git process did not inherit the host runner's safe-directory configuration.

The current runner correction configures only the mounted checkout as a container-local safe directory immediately before `make release-check`. The same configuration is added to the permanent Linux release workflow. No archive-content predicate is removed or weakened.

## Frozen remaining scope

There are no open-ended roadmap additions. The finite path is: rerun corrected Step 6; remove temporary transport and pass cleanup CI; complete Step 4 current-candidate literal-font proof; issue #18; Final Certification phase-end; Release.

## What still blocks v3.0.0

| Blocker | Exit condition |
|---|---|
| Steps 5-6 bounded acceptance | corrected permanent `make release-check` transport passes, temporary workflow removed, cleanup Static/Linux green |
| Literal-font/Unicode/embedding | current final-candidate Times New Roman/Arial identity, Unicode extraction and embedding evidence |
| Issue #18 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 with existing validation preserved |
| Final Certification phase-end | one immutable candidate passes complete gate |
| Release | final documentation/checksums, `v3.0.0` tag/GitHub Release and publication verification |

Librarian item 33 remains an explicit authority gap, not a release implementation task.

## Mandatory closeout rule

Every **material advance** updates operational documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. A failing check stays inside the frozen acceptance predicate it violates and does not automatically create a new workstream.
