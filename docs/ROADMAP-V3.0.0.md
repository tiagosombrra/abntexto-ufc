# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-3 are accepted. The persistent article-PDF/A and distribution-integrity gates for Steps 5-6 are implemented and are being validated through a temporary release transport. Remaining scope is frozen.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — BOUNDED MATRIX VALIDATION** | Steps 4-7 accepted + immutable phase-end regression |
| Release | QUEUED | final release actions after certification |

## Final Certification roadmap

| Step | Work | State |
|---:|---|---|
| 1 | Entry synchronization | ACCEPTED |
| 2 | Linux release baseline | ACCEPTED — release `34168471371`; cleanup `0609f929...` Static/Linux green |
| 3 | Profile and engine certification | ACCEPTED |
| 4 | Literal Times New Roman/Arial, Unicode and embedding | ACTIVE |
| 5 | Scientific Article PDF/A-2b | **IMPLEMENTED — RELEASE VALIDATION PENDING** |
| 6 | Distribution/public bundle integrity | **IMPLEMENTED — RELEASE VALIDATION PENDING** |
| 7 | Issue #18 deterministic reference PDF | QUEUED |
| 8 | Final Certification phase-end regression | QUEUED |

`make release-check` now contains the persistent Step 5/6 gates. `.github/workflows/final-cert-bounded-matrix.yml` is temporary transport only and must be removed after classification before bounded acceptance.

## Closure-scope freeze

No new roadmap phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 4-8. Accepted shared, librarian-review, Reference PDF and Scientific Article semantics remain closed absent a concrete regression.

The finite path is: complete Step 4; validate and clean up Steps 5-6; resolve issue #18; execute Final Certification phase-end regression; then Release.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase or create a new workstream by themselves.
