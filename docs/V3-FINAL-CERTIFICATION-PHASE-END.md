# V3 Final Certification — Phase-end Regression

Updated: 2026-09-08
Status: CANDIDATE RETRY — RUNNING

## Purpose

This document binds Final Certification Step 8 to one immutable candidate at a time. Every **material advance** remains synchronized with handoff, roadmap, readiness and `release/v3-roadmap.json`. Targeted checks do not replace the mandatory **phase-end regression**.

## Accepted prerequisites

| Surface | Accepted evidence |
|---|---|
| Steps 1-6 | ACCEPTED |
| Step 7 deterministic proof | `34231038578` — SUCCESS |
| Step 7 cleanup | `34e6bf8299e582803d1726e8dd699271c356fda5`; Static `34232017286`; complete Linux `34232017359` |
| Deterministic PDF | 2 clean builds; SHA-256 `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` |
| Temporary executor | absent |
| Permanent reproducibility gate | `make release-reference-reproducibility` inside `make release-check` |
| Issue #18 | CLOSED — completed |
| Step 8 transport preparation | `4d94e9cd7a565eac2e226360bd2b4a92fee52586`; Static `34235990523` SUCCESS; complete Linux `34235990383` SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |

## Candidate history

| Candidate | Static | Linux integration | Release matrix | Decision |
|---|---|---|---|---|
| `fc907856ac4ba0febf4d44fb408407a0fc2e94d4` | `34239113996` SUCCESS | `34239114066` workflow SUCCESS, but heavy integration **SKIPPED** as documentation-only | not relevant to acceptance after Linux predicate failed | **REJECTED** |
| current retry | pending | must execute `complete`, not scoped skip | permanent Linux release check / `make release-check` | RUNNING |

Workflow conclusion `success` is insufficient when a mandatory phase predicate was not executed. The rejected candidate did not satisfy `complete Linux integration` and cannot close Final Certification.

## Retry scope correction

The permanent `.github/workflows/linux-release-check.yml` remains the accepted release-matrix transport. The retry changes Linux integration scope orchestration only:

1. `release/final-certification-candidate.json` is explicitly listed as force-complete in `tests/integration_suites.py`;
2. self-tests assert marker-only and marker+orchestration paths infer `complete`;
3. the retry changes the marker itself, ensuring the incremental synchronize window contains the force-complete path.

No runtime, normative predicate, tolerance, accepted article/shared behavior or release-check predicate changes.

## Immutable retry gate

The current retry candidate contains the updated marker, scope guard and synchronized retry-running state. It is not amended after CI begins. The exact Git retry SHA is recorded after commit creation; the machine sentinel remains `phase_end_regression.candidate = one-immutable-sha`.

That exact retry must pass:

1. Static contract;
2. **complete** Linux integration, with heavy integration actually executed;
3. Linux release check running the permanent `make release-check` contract;
4. all accepted literal-font/Unicode/embedding/PDF-A/distribution predicates remain intact;
5. deterministic release-reference-PDF gate remains green;
6. no temporary certification executor is present;
7. librarian item 33 remains explicitly fail-closed.

Any failure is classified before code or test changes. A rejected candidate is never amended; a corrected state creates a new candidate commit.

## Exit rule

After one candidate passes the complete matrix, record its SHA/run IDs/conclusions, mark Final Certification `CLOSED`, activate `Release`, remove the one-shot candidate marker, and execute the phase-transition documentation cycle.
