# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Release is ACTIVE on PR #293. Candidate transport is accepted; durable candidate-artifact delivery is the current work.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE — ARTIFACT DELIVERY / CANDIDATE PREPARATION** | immutable Release candidate passes Static + complete Linux + release check; exact certified assets published and verified |

## Release facts

| Predicate | Current result |
|---|---|
| Merged `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch / PR | `release/v3-release` / #293 |
| Entry sync | `4fbd5693...`; Static green; Linux heavy work correctly skipped because that increment was documentation-only |
| Transport preparation | `6a257f35...` — **ACCEPTED** |
| Transport Static | `34265429699` — SUCCESS |
| Transport Linux | `34265429551` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Librarian matrix | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |
| Item 33 | explicit authority gap; fail-closed |

## Release plan

| Step | State | Gate |
|---:|---|---|
| Final Certification → Release transition | DONE | PR #289 merged |
| Release branch + PR synchronization | DONE | PR #293 open, control plane synchronized |
| Prepare Release-specific phase-end marker transport | **DONE** | `6a257f35...`; Static + complete Linux PASS |
| Retain final distribution artifacts from permanent release workflow | **ACTIVE** | `Linux release check` uploads exact generated `dist/` set |
| Publish immutable Release phase-end candidate marker | QUEUED | `release/v3-release-candidate.json` changes on candidate SHA |
| Release phase-end regression | QUEUED | Static + `SCOPE=complete` Linux + Linux release check |
| Verify candidate artifacts/checksums | QUEUED | four ZIPs + `SHA256SUMS`, exact candidate provenance |
| Tag/GitHub Release/publication | QUEUED | accepted candidate; published assets match certified hashes |
| Release closeout | QUEUED | no blocker + final verification recorded |

## Artifact provenance policy

The permanent `Linux release check` executes `make release-check`, which builds and validates the release distribution. The same workflow must retain the generated `dist/` directory as a downloadable artifact. The final GitHub Release must use those exact candidate-produced bytes, not a later rebuild.

This tightens provenance without changing product or normative semantics. Diagnostic pre-candidate builds do not become publication artifacts.

## Candidate transport policy

`release/v3-release-candidate.json` is the Release-specific force-complete/PR-release-check marker. It must not be confused with or replace the historical `release/final-certification-candidate.json`. The marker changes orchestration/provenance only, never product or normative semantics.

`docs/V3-RELEASE-PHASE-END.md` is the phase-end acceptance contract.

## Frozen remaining scope

Only **Release** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked Release implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Release ends with a complete **phase-end regression** on one immutable SHA; intermediate green checks do not substitute for it.
