# V3.0.0 Release Readiness

Updated: 2026-09-07
Status: ACTIVE — FINAL CERTIFICATION BOUNDED MATRIX

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; Static `34154045481`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — BOUNDED MATRIX** | release baseline and profile/engine matrix accepted; literal-font/Unicode, article PDF/A, distribution, issue #18 and phase-end remain |
| Release | QUEUED | bundles/checksums, tag/GitHub Release and publication verification after certification |

## Current certification state

| Surface | State |
|---|---|
| Canonical main | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | **ACCEPTED** — `aa6cc4a...`; Static `34161228915`; Linux `34161228823` |
| Linux release execution | **ACCEPTED** — transport `f8be323...`; release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup `0609f929...`; Static `34170123785`; Linux `34170123765` |
| Release evidence artifact | `10035242168`; `sha256:d5f3f75c29e294728dbc59fe569b2aba8cfc7f7ba23d05eb80bc7abfdf302604` |
| Temporary executor | absent; cleanup acceptance proven |
| Profile/engine matrix | **ACCEPTED** — six non-article profiles × two engines plus scientific article × two engines through current complete release evidence |
| Literal Times New Roman/Arial + Unicode + embedding | **PENDING — bounded certification gap** |
| PDF/A-2b | **PARTIAL — reference/non-article release routes green; explicit scientific-article final-candidate proof pending** |
| Distribution/public bundles | **PENDING — bounded certification gap** |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## Frozen remaining scope

The remaining v3.0.0 path is intentionally finite. Certification may not create new workstreams merely because a check reveals a defect; any defect is assigned to the existing acceptance step it violates. The fixed remaining certification work is: literal-font/Unicode/embedding proof, explicit article PDF/A proof, distribution integrity, issue #18 reproducibility, and one immutable phase-end regression. After that, only Release remains.

## What still blocks v3.0.0

| Blocker | Severity | Exit condition |
|---|---|---|
| Literal-font/Unicode/embedding certification | P0 | final-candidate Times New Roman/Arial identity, Unicode extraction and embedding evidence passes without redistributing fonts |
| Scientific Article PDF/A proof | P0 | explicit article PDF/A-2b validation passes on certification candidate |
| Distribution/public bundles | P0 | package/public-distribution integrity passes from certification candidate |
| Issue #18 reproducibility | P0 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 while existing validation remains green |
| Final Certification phase-end regression | P0 | one immutable candidate passes complete phase-end gate |
| Release | P0 | final documentation, checksums, `v3.0.0` tag/GitHub Release and publication verification |
| Librarian item 33 | explicit authority gap | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained; it does not authorize speculative runtime work |

## Mandatory closeout rule

Every **material advance** updates the relevant operational documents in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Intermediate checks never create a new phase and never reopen accepted semantics unless a concrete regression proves a defect.
