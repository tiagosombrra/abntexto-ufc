# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-3 and 5-6 are accepted. The temporary Steps 5-6 transport was removed and its cleanup checkpoint `7307164...` passed Static `34208318971` and Linux `34208318754`. The active certification batch is Step 4: fresh current-candidate literal-font/Unicode/embedding proof.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 4** | Steps 4 and 7 accepted + immutable phase-end regression |
| Release | QUEUED | final release actions after certification |

## Final Certification roadmap

| Step | Work | State |
|---:|---|---|
| 1 | Entry synchronization | ACCEPTED |
| 2 | Linux release baseline | ACCEPTED |
| 3 | Profile and engine certification | ACCEPTED |
| 4 | Literal Times New Roman/Arial, Unicode and embedding | **ACTIVE** |
| 5 | Scientific Article PDF/A-2b | **ACCEPTED** |
| 6 | Distribution/public bundle integrity | **ACCEPTED** |
| 7 | Issue #18 deterministic reference PDF | QUEUED |
| 8 | Final Certification phase-end regression | QUEUED |

## Steps 5-6 accepted evidence

| Surface | Evidence |
|---|---|
| Bounded candidate | `13e491d18d46a86835b4ab1d7f331f6f09f38849` |
| Static / Linux | `34175388673` PASS / `34175388665` PASS |
| Release transport | `34175388675`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Step 5 | PDF/A-2b + embedding PASS |
| Step 6 | 4 bundles + SHA256SUMS + archive integrity PASS |
| Cleanup checkpoint | `7307164ba4cf924beecb6678c7af5b79d551d513` |
| Cleanup Static / Linux | `34208318971` PASS / `34208318754` PASS |

The proof-only workflow is absent after the accepted cleanup. Permanent certification behavior remains in the permanent release/integration contracts.

## Frozen remaining scope

The finite path is:

**Step 4 literal-font/Unicode/embedding proof → issue #18 deterministic reference PDF → Final Certification phase-end regression → Release.**

A temporary Step 4 executor, if required for the Windows runner, must be removed after evidence capture and followed by cleanup Static/Linux before Step 4 acceptance.

No new phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 4-8.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
