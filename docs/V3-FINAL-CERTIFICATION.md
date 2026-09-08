# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 7 PROOF PASS / EXECUTOR REPORTING RERUN

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
| 7 | Deterministic release reference PDF / issue #18 | **ACTIVE — CORE PROOF PASS, CLEAN EXECUTOR RERUN REQUIRED** | run `34229431523`: proof step PASS; reporting-only step failed; artifact uploaded |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate after Step 7 cleanup |

## Step 7 permanent gate

The permanent implementation is repository-owned and part of normal release verification:

- `tests/integration/release-reference-reproducibility.sh` performs the proof;
- `make release-reference-reproducibility` exposes the bounded entry point;
- `make release-check` invokes the reproducibility gate after the established release checks.

The proof performs two independent clean builds from one immutable Git archive, pins deterministic provenance using `SOURCE_DATE_EPOCH`, `FORCE_SOURCE_DATE=1` and `TZ=UTC`, requires exact SHA-256 equality, then validates the accepted output for font embedding, portable UFC PDF structure, Unicode extraction and PDF/A-2b. No post-build PDF normalization or output reuse is permitted.

## Bounded proof classification — run 34229431523

The temporary executor ran on source `0040ed413df7bd9126ff1dcb34c23582bfd68403`. The product/evidence step **passed** and emitted:

| Predicate | Measured result | State |
|---|---|---|
| Source SHA | `0040ed413df7bd9126ff1dcb34c23582bfd68403` | PASS |
| Deterministic epoch | `1788872450` (`git-commit-time`) | PASS |
| Independent clean builds | `2` | PASS |
| Exact PDF SHA-256 | `cf00b4ba784d0e0cd774b080d9cb88cc23b19c4ecc17ace6dc6aa7fc17c5ac7f` | PASS |
| PDF bytes | `450652` | recorded |
| Font embedding | PASS | PASS |
| Portable UFC PDF validator | PASS | PASS |
| Unicode extraction | PASS | PASS |
| PDF/A-2b | PASS | PASS |
| Post-build normalization | false by gate contract | PASS |
| Evidence artifact | ID `10057223731`, 6 files, one-day retention | uploaded |

The workflow conclusion was `failure` only because the **Publish proof summary** shell here-document was malformed after the proof had completed. `Run bounded reproducibility proof` succeeded, and `Upload bounded evidence` also succeeded. This is classified as a temporary-executor reporting defect, not a reproducibility, PDF, runtime, normative or product failure.

Because the Step 7 acceptance contract also requires a clean bounded executor result, the temporary workflow summary is simplified to direct JSON output and must rerun green. The permanent gate and its predicates are unchanged.

## Step 7 cleanup boundary

After the corrected temporary executor completes green:

1. record the clean run and confirm the same proof predicates;
2. remove `.github/workflows/final-cert-step7-repro.yml`;
3. synchronize roadmap, handoff, readiness and machine state;
4. require cleanup Static and Linux to pass;
5. only then accept Step 7 / issue #18 and prepare Step 8.

## Issue #18 boundary

Issue #18 remains a P0 v3.0.0 release blocker until the clean bounded executor result is recorded, the temporary executor is removed and cleanup validation is green. The successful core proof from `34229431523` is retained as evidence but does not by itself close the issue.

## Phase-end rule

Final Certification closes only when Step 7 is accepted, temporary executors are absent, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
