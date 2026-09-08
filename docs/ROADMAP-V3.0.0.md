# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE at the Step 8 immutable phase-end candidate gate.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 8 IMMUTABLE CANDIDATE** | same candidate passes Static + complete Linux + full release/certification matrix |
| Release | QUEUED | only after certification |

## Final Certification steps

| Step | State | Evidence / next gate |
|---:|---|---|
| 1-6 | ACCEPTED | retained certification evidence |
| 7 | ACCEPTED | deterministic proof `34231038578`; cleanup `34e6bf8...`; Static `34232017286`; complete Linux `34232017359`; issue #18 closed |
| 8 preparation | ACCEPTED | `4d94e9c...`; Static `34235990523`; complete Linux `34235990383`, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| 8 candidate | **RUNNING** | one-shot marker present; await Static + complete Linux + Linux release check on same immutable candidate |

## Step 8 candidate decision

The permanent `.github/workflows/linux-release-check.yml` retains normal `main` push and manual-dispatch routes and exposes the accepted PR route only when `release/final-certification-candidate.json` is present. That route runs the same repository-owned `make release-check`; it is transport, not a second validation contract.

The synchronized candidate is the first commit that contains the marker and synchronized candidate-running control state. Earlier marker-only/intermediate commits are not accepted candidates. The candidate is not amended after CI begins.

The machine sentinel remains `phase_end_regression.candidate = one-immutable-sha`; the actual candidate SHA is recorded after commit creation in evidence/PR metadata.

## Frozen remaining scope

**Step 8 phase-end regression → Release.** No additional phase/workstream is created. Librarian item 33 remains explicit `NORMATIVE-REVIEW` and fail-closed.

## Operating discipline

Every **material advance** must update roadmap, handoff and machine state in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
