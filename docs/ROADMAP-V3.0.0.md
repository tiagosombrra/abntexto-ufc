# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE at the Step 8 immutable candidate retry gate.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 8 CANDIDATE RETRY** | same retry candidate passes Static + **complete** Linux + full release/certification matrix |
| Release | QUEUED | only after certification |

## Final Certification steps

| Step | State | Evidence / next gate |
|---:|---|---|
| 1-6 | ACCEPTED | retained certification evidence |
| 7 | ACCEPTED | deterministic proof `34231038578`; cleanup `34e6bf8...`; Static `34232017286`; complete Linux `34232017359`; issue #18 closed |
| 8 preparation | ACCEPTED | `4d94e9c...`; Static `34235990523`; complete Linux `34235990383`, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| 8 candidate `fc907856...` | **REJECTED** | Static `34239113996` SUCCESS; Linux `34239114066` workflow SUCCESS but heavy integration skipped as documentation-only; required complete scope not satisfied |
| 8 candidate retry | **RUNNING** | updated marker + explicit complete-scope guard; await Static + complete Linux + Linux release check on same immutable retry SHA |

## Step 8 retry decision

The permanent Linux release PR route remains unchanged and executes `make release-check` when `release/final-certification-candidate.json` is present. The defect was in Linux integration auto-scope on the incremental synchronize window: the prior candidate commit did not itself change the marker, so only documentation changes were observed and heavy integration was skipped.

The correction is fail-closed and orchestration-only:

- candidate marker is explicitly a `complete` path in `tests/integration_suites.py`;
- self-test covers marker-only and marker+orchestration cases;
- the retry commit updates the marker so the incremental window necessarily sees it.

No runtime, normative rule, tolerance, article/shared semantics or release predicate is changed.

The machine sentinel remains `phase_end_regression.candidate = one-immutable-sha`; the actual retry SHA is recorded after commit creation in PR/evidence metadata. The retry is not amended after CI begins.

## Frozen remaining scope

**Step 8 phase-end regression → Release.** No additional phase/workstream is created. Librarian item 33 remains explicit `NORMATIVE-REVIEW` and fail-closed.

## Operating discipline

Every **material advance** must update roadmap, handoff and machine state in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Workflow success without the required execution scope does not satisfy a phase predicate.
