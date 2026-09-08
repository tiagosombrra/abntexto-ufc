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

## Release entry and branch synchronization accepted

| Predicate | Accepted result |
|---|---|
| Final Certification → Release transition | `d3679f2caa35403887d2dc75f9b2486e5a3b7ba6` |
| Transition Static | `34249182526` SUCCESS |
| Transition Linux | `34249182417` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| PR #289 | merged |
| New `main` / Release base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active Release branch / PR | `release/v3.0.0` / #292 |
| Synchronization checkpoint | `3fad68d953b1264148431d7d1046666674b1a240` |
| Synchronization Static | `34252314666` SUCCESS |
| Synchronization Linux | `34252314932` SUCCESS; heavy integration skipped because the checkpoint was documentation-only |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

The transition and synchronization changed control-plane state only. Accepted runtime, normative predicates, validation tolerances and librarian classifications remain frozen unless a concrete Release regression proves a defect.

## Release plan

| Step | State | Gate |
|---:|---|---|
| Synchronize Release branch/control plane | **PASS** | Static `34252314666` |
| Reconcile current release checklist/tooling and final candidate transport | **ACTIVE** | current CTAN/repository procedure represented without stale phase assumptions; exact candidate can run complete Linux and Linux release check |
| Build final public/distribution artifacts and checksums | QUEUED | archive/integrity/reproducibility PASS |
| Validate extracted CTAN candidate and shipped example | QUEUED | external dependency/package checks PASS |
| Run current CTAN `pkgcheck` when executable | QUEUED | no blocking diagnostics; actual version recorded |
| Freeze immutable Release candidate | QUEUED | no candidate mutation after final gates begin |
| Release phase-end regression | QUEUED | Static + complete Linux + Linux release check + release-specific acceptance PASS |
| Tag / GitHub Release / documented publication | QUEUED | only after accepted candidate; published artifacts match checksums |
| Release closeout | QUEUED | final verification recorded; no unresolved release blocker |

## Current tooling findings

- `make release-check` already includes release-mode validation, Scientific Article PDF/A, distribution-bundle verification and deterministic release-reference reproducibility.
- Distribution validation already verifies four archives and SHA-256 integrity with institutional/proprietary asset exclusions.
- CTAN currently reports `pkgcheck` 4.0.3 (2026-05-28); final execution must record the version actually used.
- The remaining orchestration gap is Release-specific PR transport: the permanent `Linux release check` still triggers on the old Final Certification candidate path, so Release needs an explicit, readable non-temporary candidate surface.

## Frozen remaining scope

Only **Release** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked release implementation task.

## Operating discipline

Every **material advance** must update roadmap, handoff, Release execution record and machine state in the same work cycle. Release ends with a complete **phase-end regression** on one immutable SHA; intermediate green checks do not substitute for it.
