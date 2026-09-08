# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-3 are accepted. The corrected bounded candidate `13e491d18...` passed Static, Linux, complete `make release-check`, Scientific Article PDF/A-2b/font embedding, and distribution bundle integrity. The temporary bounded transport is now being removed; Steps 5-6 require cleanup Static/Linux before acceptance.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEPS 5-6 CLEANUP** | Steps 4-7 accepted + immutable phase-end regression |
| Release | QUEUED | final release actions after certification |

## Final Certification roadmap

| Step | Work | State |
|---:|---|---|
| 1 | Entry synchronization | ACCEPTED |
| 2 | Linux release baseline | ACCEPTED |
| 3 | Profile and engine certification | ACCEPTED |
| 4 | Literal Times New Roman/Arial, Unicode and embedding | NEXT AFTER CLEANUP |
| 5 | Scientific Article PDF/A-2b | **PASS OBSERVED — cleanup acceptance pending** |
| 6 | Distribution/public bundle integrity | **PASS OBSERVED — cleanup acceptance pending** |
| 7 | Issue #18 deterministic reference PDF | QUEUED |
| 8 | Final Certification phase-end regression | QUEUED |

## Bounded transport result

| Checkpoint / run | Release contract | Step 5 | Step 6 | Artifact |
|---|---|---|---|---|
| `13e491d18...` / `34175388675` | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` | PDF/A-2b + embedding PASS | 4 bundles + checksums + archive integrity PASS | `10037419414`, SHA-256 `e0420e72...` |

Static `34175388673` and Linux `34175388665` also passed on the same bounded candidate.

The temporary `.github/workflows/final-cert-bounded-matrix.yml` is removed in the current cleanup advance. Permanent Step 5/6 behavior remains in `make release-check` and the permanent Linux release workflow.

## Frozen remaining scope

The finite path is:

**cleanup Static/Linux → Step 4 current-candidate literal-font/Unicode/embedding proof → issue #18 deterministic reference PDF → Final Certification phase-end regression → Release.**

No new phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 4-8.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
