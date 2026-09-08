# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE on `cert/v3-final-certification`. Steps 1-6 are accepted. Step 7 has entered bounded proof after permanent deterministic reference-PDF gate implementation.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static/Linux green |
| Reference PDF Validation | CLOSED | `b64074c...`; 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | `923d11ef...`; complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 7 BOUNDED PROOF** | deterministic reference PDF accepted + temporary executor removed + immutable phase-end regression |
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
| 7 | Issue #18 deterministic reference PDF | **ACTIVE — BOUNDED PROOF** | permanent gate parent `775dfdd6...`; temporary proof executor active |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate after Step 7 cleanup |

## Step 7 implementation and acceptance requirement

The normal release entry point now includes `make release-reference-reproducibility`. The gate performs two independent clean builds of `template/main.pdf` from one immutable Git source state, pins deterministic build time with `SOURCE_DATE_EPOCH`/`FORCE_SOURCE_DATE`, requires exact PDF SHA-256 equality, and validates the deterministic output for font embedding, portable UFC PDF structure, Unicode extraction and PDF/A-2b.

The bounded executor `.github/workflows/final-cert-step7-repro.yml` is temporary proof transport only. It retains the two generated PDFs and build logs for one day and must be removed after the proof is classified. Step 7 is not accepted merely because the implementation exists.

## Frozen remaining scope

**Step 7 bounded proof → Step 7 executor cleanup/issue #18 closure → Final Certification phase-end regression → Release.**

No new phase or certification step is created merely because a validator finds a defect. New findings are classified inside Steps 7-8.

## Persistent authority gap

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed and is not a hidden implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
