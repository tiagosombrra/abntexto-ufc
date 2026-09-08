# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Release is ACTIVE on `release/v3-release` through PR #293. Final Certification is CLOSED.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE — PR #293** | release checklist complete, publication verified, and Release phase-end regression green on one immutable candidate |

## Release entry facts

| Predicate | Current result |
|---|---|
| Merged `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Final Certification PR | #289 — MERGED |
| Release branch | `release/v3-release`, based on `e34037f...` |
| Release PR | #293 — OPEN |
| Librarian matrix | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |
| Item 33 | explicit authority gap; fail-closed |
| Temporary certification executor | absent |

## Release plan

| Step | State | Gate |
|---:|---|---|
| Final Certification → Release transition | DONE | PR #289 merged |
| Create short-lived Release branch from updated `main` | DONE | branch created from `e34037f...` |
| Synchronize branch facts | DONE | control plane consistent |
| Create Release PR | DONE | PR #293 open |
| Read/execute repository release checklist | ACTIVE | `docs/CTAN-RELEASE.md` and release tooling are authority |
| Build final artifacts/checksums | QUEUED | integrity/reproducibility PASS |
| Immutable Release phase-end candidate | QUEUED | Static + complete Linux + Linux release check |
| Tag/GitHub Release/publication | QUEUED | accepted Release candidate; verify published artifacts afterwards |
| Release closeout | QUEUED | no blocker + final verification recorded |

## Frozen remaining scope

Only **Release** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked release implementation task.

## Operating discipline

Every **material advance** must update roadmap, handoff and machine state in the same work cycle. Release ends with a complete **phase-end regression** on one immutable SHA; intermediate green checks do not substitute for it.
