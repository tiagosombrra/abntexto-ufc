# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Release is ACTIVE. All previous phases are CLOSED.**

| Phase | Status | Accepted / exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted phase-end regression |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE — CANDIDATE TRANSPORT REPAIR** | release checklist complete, immutable Release candidate accepted, publication verified, and Release phase-end regression green |

## Release transport probe result

| Predicate | Result | Gate status |
|---|---|---|
| Probe SHA | `d1f86db10f1458ed75078239916f0de857671348` | classified |
| Static | `34253455083` SUCCESS | PASS |
| Linux integration | `34253455068` SUCCESS, but `SCOPE=smoke PASS=4 FAIL=0 SKIP=0` | **NOT ACCEPTABLE for phase-end** |
| Linux release check | `34253454993` SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` | bounded PASS |
| Release-check artifact | ID `10067709957`, digest `2fc9a5f1dcadf330e2fb832c47e88fe00a6b0ffa2f7f5963291984f0de1f8c6e` | bounded PASS |
| Deterministic reference PDF | 2 builds; SHA-256 `1acd4c47a1485d16c1b0cf92d074c6dc194dc8952c8f2c61709acbc6a9a503a7` | bounded PASS |
| Release-check checkout provenance | PR merge ref, not exact PR head | repair required |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` | unchanged |

A workflow conclusion of `success` is insufficient when the required scope was not executed. Therefore `d1f86db...` is **rejected as a Release phase-end candidate**. It remains useful as a transport-probe checkpoint.

## Root cause

The Release marker had already been introduced before `d1f86db...`. On a `synchronize` event, automatic Linux selection examined only the incremental `before → after` changed paths, which contained orchestration code but not the persistent marker. That produced `smoke`. A force-complete path rule alone cannot protect a persistent candidate marker that is absent from the incremental diff.

The permanent Linux release workflow also used the default pull-request merge checkout. Final Release artifact provenance must instead be bound to the exact PR head candidate.

## Current repair

The next synchronized checkpoint must make candidate state at HEAD part of scope selection: an active non-temporary `release/v3-release-candidate.json` overrides incremental path inference to `complete`, including documentation-only and orchestration-only pushes. Normal scoped behavior remains unchanged when no active Release candidate is present.

The same checkpoint must make `Linux release check` checkout the exact PR head with `fetch-depth: 0` and add static contract coverage for both transport properties.

## Release plan

| Step | State | Gate |
|---:|---|---|
| Synchronize Release branch/control plane | PASS | Static `34252314666` |
| Establish readable non-temporary candidate marker and release-check PR trigger | PASS — transport probe | marker and permanent workflow route exist |
| Repair persistent-marker complete scope + exact-head release checkout | **ACTIVE** | Static + `SCOPE=complete` Linux + exact-head Linux release check |
| Build final public/distribution artifacts and checksums from accepted exact-head route | QUEUED | archive/integrity/reproducibility PASS |
| Validate extracted CTAN candidate and shipped example | QUEUED | external dependency/package checks PASS |
| Run current CTAN `pkgcheck` when executable | QUEUED | no blocking diagnostics; actual version recorded |
| Freeze immutable Release candidate | QUEUED | no candidate mutation after final gates begin |
| Release phase-end regression | QUEUED | Static + complete Linux + Linux release check + release-specific acceptance PASS |
| Tag / GitHub Release / documented publication | QUEUED | only after accepted candidate; published artifacts match checksums |
| Release closeout | QUEUED | final verification recorded; no unresolved release blocker |

## Frozen remaining scope

Only **Release** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked release implementation task.

## Operating discipline

Every **material advance** must update roadmap, handoff, Release execution record, Release readiness and machine state in the same work cycle. Release ends with a complete **phase-end regression** on one immutable SHA; intermediate green checks do not substitute for it.
