# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Release is ACTIVE. Final Certification is CLOSED.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | **CLOSED** | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE — ENTRY TRANSITION** | release checklist complete, publication verified, and Release phase-end regression green on one immutable candidate |

## Final Certification closure

| Predicate | Accepted result |
|---|---|
| Candidate | `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Static | `34239890649` SUCCESS |
| Linux integration | `34239890614` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Linux release check | `34239890548` SUCCESS; `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Distribution / PDF-A / deterministic reference | PASS |
| Temporary executor | absent |
| Item 33 | explicit `NORMATIVE-REVIEW`, fail-closed |

The prior candidate `fc907856...` remains rejected because heavy Linux integration was skipped. The accepted retry corrected orchestration scope only and changed no product/normative semantics.

## Release plan

| Step | State | Gate |
|---:|---|---|
| Transition from Final Certification | IN PROGRESS | synchronized transition commit green |
| Merge PR #289 | QUEUED | transition checks green |
| Create short-lived Release branch from updated `main` | QUEUED | machine/handoff branch facts synchronized |
| Read/execute repository release checklist | QUEUED | `docs/CTAN-RELEASE.md` and release tooling are authority |
| Build final artifacts/checksums | QUEUED | integrity/reproducibility PASS |
| Immutable Release phase-end candidate | QUEUED | Static + complete applicable Linux/release verification |
| Tag/GitHub Release/publication | QUEUED | accepted Release candidate; verify published artifacts afterwards |
| Release closeout | QUEUED | no blocker + final verification recorded |

## Frozen remaining scope

Only **Release** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked release implementation task.

## Operating discipline

Every **material advance** must update roadmap, handoff and machine state in the same work cycle. Release ends with a complete **phase-end regression** on one immutable SHA; intermediate green checks do not substitute for it.
