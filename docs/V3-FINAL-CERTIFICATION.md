# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 7 BOUNDED DETERMINISTIC PROOF

## Purpose

Final Certification proves the accepted V3 product across the remaining bounded release surfaces without reopening closed shared or Scientific Article semantics. Every **material advance** is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable **phase-end regression** candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | branch/PR and control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup Static/Linux green |
| 3 | Profile/engine matrix | ACCEPTED | current complete release evidence |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | ACCEPTED | proof `34219229025`; cleanup `35671aef...`, Static `34224224990`, Linux `34224225080` PASS |
| 5 | Scientific Article PDF/A-2b | ACCEPTED | bounded `34175388675` PASS; cleanup accepted |
| 6 | Distribution/public bundle integrity | ACCEPTED | 4 bundles, checksums and archive integrity PASS; cleanup accepted |
| 7 | Deterministic release reference PDF / issue #18 | **ACTIVE — BOUNDED PROOF** | permanent gate implemented at parent `775dfdd6...`; bounded executor active |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate with complete matrix after Step 7 cleanup |

## Step 7 permanent gate

The permanent implementation is repository-owned and part of normal release verification:

- `tests/integration/release-reference-reproducibility.sh` performs the proof;
- `make release-reference-reproducibility` exposes the bounded entry point;
- `make release-check` invokes the reproducibility gate after the established release checks.

For each proof the script:

1. identifies the immutable Git source SHA;
2. obtains deterministic provenance time from explicit `SOURCE_DATE_EPOCH` or the source commit time;
3. exports `SOURCE_DATE_EPOCH`, `FORCE_SOURCE_DATE=1` and `TZ=UTC`;
4. creates one Git archive of that immutable source and extracts it independently into two clean build directories;
5. runs `make clean` + `make compile` separately in both directories;
6. computes and requires exact SHA-256 equality of the two independently generated `template/main.pdf` files;
7. validates the deterministic output for embedded fonts, the existing portable UFC PDF contract, Unicode text extraction and PDF/A-2b;
8. records structured evidence under `artifacts/validation/release-reference-reproducibility.json` during normal release verification.

No post-build PDF normalization, rewriting or output reuse is permitted.

## Step 7 bounded proof executor

`.github/workflows/final-cert-step7-repro.yml` is temporarily active on `cert/v3-final-certification`. It exists only to execute the bounded proof before merge and uploads one-day evidence including both independently generated PDFs/logs when available. The temporary executor must be removed after the run is classified; Step 7 cannot be accepted while it remains active.

The bounded proof must establish all of the following on one source checkpoint:

| Predicate | Required result |
|---|---|
| Independent clean builds | 2 |
| Deterministic epoch | explicit and recorded |
| PDF SHA-256 equality | exact PASS |
| Font embedding | PASS |
| Portable UFC PDF validator | PASS |
| Unicode extraction | PASS |
| PDF/A-2b | PASS |
| Post-build normalization | false |

## Issue #18 boundary

Issue #18 remains a P0 v3.0.0 release blocker until the bounded proof passes, the temporary executor is removed, cleanup validation is green and the accepted digest/provenance are recorded. This reproducibility work must not change accepted shared or Scientific Article normative semantics.

## Phase-end rule

Final Certification closes only when Step 7 is accepted, temporary executors are absent, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
