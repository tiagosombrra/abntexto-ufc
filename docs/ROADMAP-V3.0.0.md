# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-7 are accepted. Step 8 phase-end regression preparation is active.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 8 PHASE-END PREPARATION** | immutable candidate passes complete certification matrix |
| Release | QUEUED | final release actions after certification |

## Final Certification roadmap

| Step | Work | State | Evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | canonical branch/base reconciled |
| 2 | Linux release baseline | ACCEPTED | complete release matrix green |
| 3 | Profile and engine certification | ACCEPTED | current candidate matrix accepted |
| 4 | Literal Times New Roman/Arial, Unicode and embedding | ACCEPTED | proof `34219229025`; cleanup `35671aef...` green |
| 5 | Scientific Article PDF/A-2b | ACCEPTED | bounded + cleanup accepted |
| 6 | Distribution/public bundle integrity | ACCEPTED | bundles/checksums/archive integrity accepted |
| 7 | Issue #18 deterministic reference PDF | **ACCEPTED** | proof `34231038578`; cleanup `34e6bf8...`; Static `34232017286`; complete Linux `34232017359`; issue closed |
| 8 | Final Certification phase-end regression | **PREPARATION** | one immutable candidate must pass Static + complete Linux + full release/certification matrix |

## Step 7 accepted evidence

Run `34231038578` on source `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` used deterministic epoch `1788873426`, performed two independent clean builds and produced identical PDF SHA-256 `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf`. Font embedding, portable UFC PDF validation, Unicode extraction and PDF/A-2b all passed. Cleanup checkpoint `34e6bf8299e582803d1726e8dd699271c356fda5` removed the temporary executor and passed Static `34232017286` plus complete Linux `34232017359`, `PASS=36 FAIL=0 SKIP=0`. Issue #18 is closed.

## Frozen remaining scope

**Final Certification phase-end regression → Release.**

No new phase or certification step is created merely because a validator finds a defect. New findings are classified inside Step 8.

## Step 8 gate

`docs/V3-FINAL-CERTIFICATION-PHASE-END.md` defines the candidate contract. One immutable candidate must pass Static, complete Linux and the complete applicable release/certification matrix. The candidate is not amended after CI begins. A failure is classified before any code or test change.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
