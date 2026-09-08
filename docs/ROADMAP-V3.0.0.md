# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Final Certification is ACTIVE. Steps 1-7 are accepted. Step 8 release-matrix PR transport preparation is active.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | **ACTIVE — STEP 8 PREPARATION** | immutable candidate passes Static + complete Linux + full release/certification matrix |
| Release | QUEUED | only after certification |

## Final Certification steps

| Step | State | Evidence / next gate |
|---:|---|---|
| 1-6 | ACCEPTED | prior certification evidence retained |
| 7 | **ACCEPTED** | proof `34231038578`; cleanup `34e6bf8...`; Static `34232017286`; complete Linux `34232017359`; issue #18 closed |
| 8 | **PREPARATION** | validate permanent PR transport, then create immutable candidate |

## Step 8 transport decision

The permanent `.github/workflows/linux-release-check.yml` keeps normal `main` push and manual-dispatch routes and adds a PR route restricted to `release/final-certification-candidate.json`. The route runs the same repository-owned `make release-check`; it does not create a second validation contract. This preparation checkpoint must pass Static and complete Linux before the immutable candidate marker is added.

The final candidate must then pass Static, complete Linux and Linux release check on the same immutable candidate. After acceptance, the marker is removed in the phase-transition commit and Release becomes active.

## Frozen remaining scope

**Step 8 phase-end regression → Release.** No additional phase/workstream is created. Librarian item 33 remains explicit `NORMATIVE-REVIEW` and fail-closed.

## Operating discipline

Every **material advance** updates roadmap, handoff and machine state in the same cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Targeted checks never close a phase by themselves.
