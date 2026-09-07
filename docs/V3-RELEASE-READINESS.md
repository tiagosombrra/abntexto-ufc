# V3.0.0 Release Readiness

Updated: 2026-09-07
Status: ACTIVE — FINAL CERTIFICATION RELEASE BASELINE EXECUTOR

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | CLOSED | `923d11ef...`; Static `34154045481`; complete Linux `34154045509`; article PDF 5/5 visual PASS |
| Final Certification | **ACTIVE — RELEASE BASELINE EXECUTOR** | entry accepted; exact permanent release contract currently being exercised |
| Release | QUEUED | bundles, checksums, tag/GitHub Release and publication verification |

## Current certification state

| Surface | State |
|---|---|
| Scientific Article PR #286 | MERGED |
| Canonical main | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | **ACCEPTED** — `aa6cc4a...`; Static `34161228915`; Linux `34161228823` SUCCESS, docs-only heavy skip |
| Linux release baseline | **ACTIVE — temporary transport executor** |
| Temporary executor | `.github/workflows/final-cert-release-baseline.yml`; must be removed before baseline acceptance |
| Profile/engine matrix | queued |
| Literal fonts / Unicode / embedding | queued |
| PDF/A-2b | queued |
| Distribution bundles | queued |
| Issue #18 deterministic reference PDF | OPEN — P0 release blocker |
| Final Certification phase-end regression | not started |

## Baseline transport boundary

The temporary executor runs the existing permanent `make release-check` contract under the same TeX Live 2026 environment and dependency set because direct workflow dispatch is unavailable through the current automation surface. It is not a new release rule and must be removed before baseline acceptance.

## What still blocks v3.0.0

| Blocker | Severity | Exit condition |
|---|---|---|
| Linux release baseline | P0 | current main-derived certification branch passes the existing release contract and temporary executor is removed |
| Complete certification matrix | P0 | all applicable profile/engine/font/Unicode/embedding/PDF-A/distribution gates green |
| Issue #18 reproducibility | P0 | deterministic epoch + two controlled clean rebuilds + identical reference-PDF SHA-256 while existing validation remains green |
| Final Certification phase-end regression | P0 | one immutable candidate passes complete phase-end gate |
| Release | P0 | final documentation, bundles/checksums, `v3.0.0` tag/GitHub Release and publication verification |
| Librarian item 33 | explicit authority gap | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained |

## Mandatory closeout rule

Every **material advance** updates the relevant operational documents in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Intermediate/scoped checks never close Final Certification. Temporary executors must be removed before bounded checkpoint acceptance.
