# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-6 are accepted. Step 7 — deterministic release reference PDF / issue #18 — is now active.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 7** | deterministic reference PDF accepted + immutable phase-end regression |
| Release | QUEUED | final release actions after certification |

## Final Certification roadmap

| Step | Work | State |
|---:|---|---|
| 1 | Entry synchronization | ACCEPTED |
| 2 | Linux release baseline | ACCEPTED |
| 3 | Profile and engine certification | ACCEPTED |
| 4 | Literal Times New Roman/Arial, Unicode and embedding | ACCEPTED — proof `34219229025`; cleanup `35671aef...`, Static `34224224990`, Linux `34224225080` |
| 5 | Scientific Article PDF/A-2b | ACCEPTED |
| 6 | Distribution/public bundle integrity | ACCEPTED |
| 7 | Issue #18 deterministic reference PDF | **ACTIVE** |
| 8 | Final Certification phase-end regression | QUEUED |

## Step 7 acceptance requirement

The canonical release reference PDF must be reproducible under an explicit deterministic build contract. Acceptance requires at least two independent clean builds from the same controlled source/input state, a pinned provenance time, exact equality of resulting PDF SHA-256 values, and preservation of the existing canonical PDF validation/font/Unicode/embedding/applicable PDF-A checks.

The gate must detect genuine byte-level nondeterminism. It must not obtain equality by copying one build output, comparing post-normalized documents, or weakening metadata/PDF checks.

## Frozen remaining scope

**Issue #18 deterministic reference PDF → Final Certification phase-end regression → Release.**

No new phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 7-8.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
