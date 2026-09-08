# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Release is ACTIVE in execution. All previous phases are CLOSED.**

| Phase | Status | Accepted / exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted phase-end regression |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE — EXECUTION** | release checklist complete, immutable Release candidate accepted, publication verified, and Release phase-end regression green |

## Release entry accepted

| Predicate | Accepted result |
|---|---|
| Final Certification → Release transition | `d3679f2caa35403887d2dc75f9b2486e5a3b7ba6` |
| Transition Static | `34249182526` SUCCESS |
| Transition Linux | `34249182417` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| PR #289 | merged |
| New `main` / Release base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active Release branch | `release/v3.0.0` |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

The transition changed control-plane phase state only. Accepted runtime, normative predicates, validation tolerances and librarian classifications remain frozen unless a concrete Release regression proves a defect.

## Release plan

| Step | State | Gate |
|---:|---|---|
| Synchronize Release branch/control plane | **ACTIVE** | Static contract green on synchronized checkpoint |
| Reconcile current release checklist/tooling | QUEUED | `docs/CTAN-RELEASE.md` and repository tooling agree; stale history removed |
| Build final public/distribution artifacts and checksums | QUEUED | archive/integrity/reproducibility PASS |
| Validate extracted CTAN candidate and shipped example | QUEUED | external dependency/package checks PASS |
| Run current CTAN `pkgcheck` when executable | QUEUED | no blocking diagnostics |
| Freeze immutable Release candidate | QUEUED | no candidate mutation after final gates begin |
| Release phase-end regression | QUEUED | Static + complete Linux + Linux release check + release-specific acceptance PASS |
| Tag / GitHub Release / documented publication | QUEUED | only after accepted candidate; published artifacts match checksums |
| Release closeout | QUEUED | final verification recorded; no unresolved release blocker |

## Frozen remaining scope

Only **Release** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked release implementation task.

## Operating discipline

Every **material advance** must update roadmap, handoff, Release execution record and machine state in the same work cycle. Release ends with a complete **phase-end regression** on one immutable SHA; intermediate green checks do not substitute for it.
