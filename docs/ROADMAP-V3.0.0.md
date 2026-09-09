# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Release is ACTIVE on PR #293. Candidate transport is accepted; candidate artifact-delivery implementation is CI-pending.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE — ARTIFACT DELIVERY IMPLEMENTATION** | immutable candidate passes Static + complete Linux + release check; exact certified assets published and verified |

## Release facts

| Predicate | Current result |
|---|---|
| Merged `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch / PR | `release/v3-release` / #293 |
| Transport preparation | `6a257f35...` — **ACCEPTED** |
| Transport Static | `34265429699` — SUCCESS |
| Transport Linux | `34265429551` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Control reconciliation | `eededce34...`; Static `34300202909` SUCCESS; Linux docs-only skip |
| Librarian matrix | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Release plan

| Step | State | Gate |
|---:|---|---|
| Final Certification → Release transition | DONE | PR #289 merged |
| Release branch + PR synchronization | DONE | PR #293 open |
| Prepare Release-specific phase-end marker transport | DONE | `6a257f35...`; Static + complete Linux PASS |
| Implement exact-candidate distribution artifact retention | **IMPLEMENTED — CI PENDING** | workflow + static orchestration contract must pass Static + complete Linux |
| Record artifact-delivery acceptance | QUEUED | implementation SHA/run IDs synchronized |
| Publish immutable Release phase-end candidate marker | QUEUED | `release/v3-release-candidate.json` on candidate SHA |
| Release phase-end regression | QUEUED | Static + `SCOPE=complete` Linux + Linux release check |
| Verify candidate artifacts/checksums | QUEUED | four ZIPs + `SHA256SUMS`, exact candidate provenance |
| Tag/GitHub Release/publication | QUEUED | accepted candidate; published assets match certified hashes |
| Release closeout | QUEUED | no blocker + final verification recorded |

## Artifact provenance implementation

The permanent `Linux release check` now has an implementation pending CI that:

- checks out `${{ github.event.pull_request.head.sha || github.sha }}` explicitly;
- binds `SOURCE_COMMIT_SHA` to that same SHA;
- derives `SOURCE_DATE_EPOCH` from that candidate commit;
- executes `make release-check` and `make distribution-bundles`;
- verifies `SHA256SUMS` and the exact five-file distribution set;
- retains the four ZIPs plus `SHA256SUMS` through the pinned upload-artifact action.

The implementation is not accepted until Static and complete Linux pass. No product or normative semantics are changed.

## Candidate policy

`release/v3-release-candidate.json` is the Release-specific force-complete/PR-release-check marker. It must not be confused with the historical `release/final-certification-candidate.json`. `docs/V3-RELEASE-PHASE-END.md` is the acceptance contract.

## Frozen remaining scope

Only **Release** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked Release implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Release ends with a complete **phase-end regression** on one immutable SHA; intermediate green checks do not substitute for it.
