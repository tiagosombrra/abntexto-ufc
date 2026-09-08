# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 7 PROOF ACCEPTED / CLEANUP VALIDATION

## Purpose

Final Certification proves the accepted V3 product across the remaining bounded release surfaces without reopening closed shared or Scientific Article semantics. Every **material advance** is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable **phase-end regression** candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | branch/PR and control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | complete release matrix green |
| 3 | Profile/engine matrix | ACCEPTED | current candidate matrix accepted |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | ACCEPTED | proof `34219229025`; cleanup `35671aef...` green |
| 5 | Scientific Article PDF/A-2b | ACCEPTED | bounded + cleanup accepted |
| 6 | Distribution/public bundle integrity | ACCEPTED | bundles/checksums/archive integrity accepted |
| 7 | Deterministic release reference PDF / issue #18 | **PROOF ACCEPTED — CLEANUP VALIDATION ACTIVE** | clean run `34231038578` PASS; temporary executor removed by current cleanup candidate |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate after Step 7 cleanup |

## Step 7 permanent gate

The permanent implementation remains repository-owned and part of normal release verification:

- `tests/integration/release-reference-reproducibility.sh` performs the proof;
- `make release-reference-reproducibility` exposes the bounded entry point;
- `make release-check` invokes the reproducibility gate after the established release checks.

The proof performs two independent clean builds from one immutable Git archive, pins deterministic provenance using `SOURCE_DATE_EPOCH`, `FORCE_SOURCE_DATE=1` and `TZ=UTC`, requires exact SHA-256 equality, then validates the accepted output for font embedding, portable UFC PDF structure, Unicode extraction and PDF/A-2b. No post-build PDF normalization or output reuse is permitted.

## Accepted bounded proof — run 34231038578

The corrected temporary executor ran cleanly on source `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522`.

| Predicate | Measured result | State |
|---|---|---|
| Workflow conclusion | `success` | PASS |
| Source SHA | `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` | PASS |
| Deterministic epoch | `1788873426` (`git-commit-time`) | PASS |
| Independent clean builds | `2` | PASS |
| Exact PDF SHA-256 | `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` | PASS |
| PDF bytes | `450652` | recorded |
| Font embedding | PASS | PASS |
| Portable UFC PDF validator | PASS | PASS |
| Unicode extraction | PASS | PASS |
| PDF/A-2b | PASS | PASS |
| Evidence artifact | ID `10057880627`, 6 files, one-day retention | PASS |
| Artifact archive digest | `8f2fdceae9351eaa9181501ec1fd23f240ab66a26e5814d329240ea4b11b820a` | recorded |

This clean run supersedes the reporting-only wrapper failure of run `34229431523` for executor acceptance while retaining that earlier successful product proof as historical evidence. No permanent proof predicate changed.

## Step 7 cleanup boundary

The temporary workflow `.github/workflows/final-cert-step7-repro.yml` is removed in the current cleanup candidate. Step 7 remains open until that cleanup candidate passes Static and Linux with the permanent reproducibility gate retained.

After cleanup Static/Linux are green:

1. record cleanup SHA and run IDs;
2. accept Step 7 and close issue #18;
3. create the immutable Step 8 Final Certification phase-end candidate;
4. run Static, complete Linux and the full applicable release/certification matrix on that candidate.

## Issue #18 boundary

Issue #18 remains open only until cleanup validation is green. Its product acceptance predicate is now proven by the clean bounded run above; closure additionally requires temporary-executor absence and green cleanup validation.

## Phase-end rule

Final Certification closes only when Step 7 is accepted, temporary executors are absent, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
