# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-3 are accepted. Step 5 passed its explicit gate in the first bounded transport, while Step 6 exposed a runner-ownership integration defect before bundle validation could complete. The correction is bounded to Step 6 and is being rerun through the same temporary release transport. Remaining scope stays frozen.**

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
| 4 | Literal Times New Roman/Arial, Unicode and embedding | ACTIVE / queued immediately after current bounded cleanup |
| 5 | Scientific Article PDF/A-2b | **GATE PASS OBSERVED — bounded acceptance waits for corrected full transport + temporary executor cleanup** |
| 6 | Distribution/public bundle integrity | **CORRECTION ACTIVE — Git safe-directory runner integration** |
| 7 | Issue #18 deterministic reference PDF | QUEUED |
| 8 | Final Certification phase-end regression | QUEUED |

## First bounded transport classification

Checkpoint `21455c3344bfe0413dbe44f29b9cfae5bee58521` produced:

| Gate | Result |
|---|---|
| Static `34172047639` | PASS |
| Linux `34172047586` | PASS |
| Temporary release transport `34172047786` | FAIL |
| Existing release suite inside transport | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Step 5 Scientific Article PDF/A/embedding | PASS |
| Step 6 distribution bundles | stopped before construction because Git rejected the Docker-mounted checkout as a dubious-ownership directory while deriving the deterministic epoch |
| Uploaded diagnostic artifact | ID `10036350950`, SHA-256 `5dd4d212bafa16702947065ef0848c9387e63e16d7d7523fee14d1d529a96432` |

This failure belongs to Step 6. It does not create a new roadmap item and does not authorize a runtime/normative change. The corrected gate uses an explicit safe-directory setting for the provenance Git query and the temporary workflow uses full history to resolve the exact `SOURCE_COMMIT_SHA`.

`make release-check` remains the permanent Step 5/6 contract. `.github/workflows/final-cert-bounded-matrix.yml` remains temporary transport only and must be removed after a successful corrected run before Steps 5-6 can be accepted.

## Closure-scope freeze

No new roadmap phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 4-8. Accepted shared, librarian-review, Reference PDF and Scientific Article semantics remain closed absent a concrete regression.

The finite path is: rerun corrected Step 6; remove transport and pass cleanup CI; complete Step 4; resolve issue #18; execute Final Certification phase-end regression; then Release.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase or create a new workstream by themselves.
