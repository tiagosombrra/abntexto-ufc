# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 8 PHASE-END REGRESSION PREPARATION

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
| 7 | Deterministic release reference PDF / issue #18 | **ACCEPTED** | clean proof `34231038578`; cleanup `34e6bf8...` Static/Linux green; issue closed |
| 8 | Final Certification phase-end regression | **PREPARATION** | one immutable candidate must pass complete matrix |

## Step 7 permanent gate

The permanent implementation remains repository-owned and part of normal release verification:

- `tests/integration/release-reference-reproducibility.sh` performs the proof;
- `make release-reference-reproducibility` exposes the bounded entry point;
- `make release-check` invokes the reproducibility gate after the established release checks.

The proof performs two independent clean builds from one immutable Git archive, pins deterministic provenance using `SOURCE_DATE_EPOCH`, `FORCE_SOURCE_DATE=1` and `TZ=UTC`, requires exact SHA-256 equality, then validates the accepted output for font embedding, portable UFC PDF structure, Unicode extraction and PDF/A-2b. No post-build PDF normalization or output reuse is permitted.

## Accepted Step 7 evidence

| Predicate | Measured result | State |
|---|---|---|
| Clean proof workflow | `34231038578` | PASS |
| Source SHA | `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` | PASS |
| Deterministic epoch | `1788873426` (`git-commit-time`) | PASS |
| Independent clean builds | `2` | PASS |
| Exact PDF SHA-256 | `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` | PASS |
| PDF bytes | `450652` | recorded |
| Font embedding | PASS | PASS |
| Portable UFC PDF validator | PASS | PASS |
| Unicode extraction | PASS | PASS |
| PDF/A-2b | PASS | PASS |
| Evidence artifact | ID `10057880627`, 6 files | PASS |
| Cleanup checkpoint | `34e6bf8299e582803d1726e8dd699271c356fda5` | PASS |
| Cleanup Static | `34232017286` | PASS |
| Cleanup complete Linux | `34232017359`, `PASS=36 FAIL=0 SKIP=0` | PASS |
| Temporary executor | absent | PASS |
| Issue #18 | CLOSED — completed | PASS |

The historical reporting-only wrapper failure `34229431523` remains classified as such; it does not override the accepted clean proof. No permanent proof predicate changed.

## Step 8 boundary

`docs/V3-FINAL-CERTIFICATION-PHASE-END.md` defines the final certification candidate contract. After this Step 7 acceptance synchronization:

1. prepare one immutable candidate;
2. run Static contract on that SHA;
3. run complete Linux integration on that SHA;
4. run the full applicable release/certification matrix, including `make release-check`, on the accepted candidate;
5. classify any failure before changing code or tests;
6. record candidate SHA and run IDs only after the immutable commit exists;
7. close Final Certification and activate Release only when the complete matrix is green.

## Phase-end rule

Final Certification closes only when all Steps 1-7 are accepted, temporary executors are absent, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
