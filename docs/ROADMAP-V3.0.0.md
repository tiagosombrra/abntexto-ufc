# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-6 are accepted. Step 7 deterministic proof is accepted at the bounded-proof level; temporary-executor cleanup validation is now active.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 7 CLEANUP VALIDATION** | cleanup accepted + immutable phase-end regression |
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
| 7 | Issue #18 deterministic reference PDF | **PROOF ACCEPTED — CLEANUP ACTIVE** | clean proof run `34231038578`; executor removed in cleanup candidate |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate after Step 7 acceptance |

## Step 7 accepted bounded proof

Run `34231038578` on source `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` completed successfully. It used deterministic epoch `1788873426` (`git-commit-time`), performed two independent clean builds and produced identical PDF SHA-256 `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf`. The 450652-byte output passed font embedding, portable UFC PDF validation, Unicode extraction and PDF/A-2b. Artifact `10057880627` contains six bounded evidence files.

The temporary executor is no longer needed and is removed in the current cleanup candidate. The permanent gate remains in `make release-check`.

## Step 7 cleanup requirement

The cleanup candidate must pass Static and Linux with `.github/workflows/final-cert-step7-repro.yml` absent and the permanent reproducibility gate retained. Only then may Step 7 be marked ACCEPTED and issue #18 closed.

## Frozen remaining scope

**Step 7 cleanup validation / issue #18 closure → Final Certification phase-end regression → Release.**

No new phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 7-8.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
