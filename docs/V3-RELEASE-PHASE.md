# V3 Release Phase

Updated: 2026-09-08  
Status: ACTIVE — CANDIDATE TRANSPORT REPAIR

## Purpose

This document is the execution record for the final roadmap phase. Every **material advance** in Release updates this record, the canonical handoff, roadmap, release readiness and machine state in the same work cycle. Release closes only after a complete **phase-end regression** on one immutable candidate SHA.

## Entry evidence

| Predicate | Accepted evidence |
|---|---|
| Final Certification candidate | `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final Static | `34239890649` — SUCCESS |
| Final complete Linux | `34239890614` — SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Linux release check | `34239890548` — SUCCESS; `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| PR #289 merge / Release base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active Release branch / PR | `release/v3.0.0` / #292 |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Candidate transport probe

Checkpoint `d1f86db10f1458ed75078239916f0de857671348` tested the first permanent Release transport route.

| Surface | Evidence | Result |
|---|---|---|
| Static | `34253455083` | PASS |
| Linux integration | `34253455068`; `SCOPE=smoke PASS=4 FAIL=0 SKIP=0` | **REJECTED for phase-end** |
| Linux release check | `34253454993`; `SCOPE=complete PASS=38 FAIL=0 SKIP=0` | bounded PASS |
| Validation artifact | ID `10067709957`; digest `2fc9a5f1dcadf330e2fb832c47e88fe00a6b0ffa2f7f5963291984f0de1f8c6e` | PASS |
| Distribution gate | 4 artifacts; SHA-256 and archive integrity PASS | bounded PASS |
| Deterministic reference PDF | 2 builds; SHA-256 `1acd4c47a1485d16c1b0cf92d074c6dc194dc8952c8f2c61709acbc6a9a503a7`; 450652 bytes; PDF/A/Unicode/font embedding PASS | bounded PASS |
| Release-check source provenance | pull-request merge checkout | **not exact-head acceptance evidence** |

This checkpoint is not an immutable Release phase-end candidate. The Linux workflow conclusion was green, but the required `complete` scope was not executed. Machine policy therefore rejects it fail-closed.

## Root-cause classification

The Release marker was already present before the `d1f86db...` synchronize event. The workflow correctly chose an incremental `before → after` diff, but that diff contained only orchestration changes. Because `release/v3-release-candidate.json` was absent from that incremental changed-path list, path-only inference selected `smoke` even though the checked-out HEAD still contained an active Release marker.

A second provenance gap was identified in the permanent Linux release workflow: default pull-request checkout uses the merge ref. Final Release artifacts/reproducibility must be produced from the exact PR head candidate.

Neither defect changes product runtime or normative behavior; both are Release orchestration/provenance defects.

## Current repair contract

The next synchronized technical checkpoint must satisfy all of the following:

1. active candidate state is read from `release/v3-release-candidate.json` in the checked-out HEAD;
2. states `transport-probe`, `candidate-active` and `candidate-frozen` force `complete` Linux even when the incremental diff contains only documentation or orchestration files;
3. when no active Release candidate exists, existing bounded auto scopes remain unchanged;
4. the permanent Linux release workflow checks out `${{ github.event.pull_request.head.sha || github.sha }}` with `fetch-depth: 0`;
5. a permanent static contract verifies marker schema/base/non-temporary state, complete-scope forcing and exact-head release checkout;
6. no test is weakened to obtain green status.

## Release execution queue

| Order | Work | Acceptance gate | State |
|---:|---|---|---|
| 1 | Synchronize Release branch facts and current documentation | Static green | PASS |
| 2 | Establish non-temporary candidate marker and permanent release-check trigger | route exists | PASS — transport probe |
| 3 | Repair persistent candidate complete-scope selection and exact-head checkout | Static + complete Linux + exact-head Linux release check | **ACTIVE** |
| 4 | Build public/distribution release artifacts and SHA-256 metadata from accepted exact-head route | archive/integrity/reproducibility checks PASS | QUEUED |
| 5 | Validate extracted CTAN candidate and shipped example | external `abntexto` semantics and package checks PASS | QUEUED |
| 6 | Run current CTAN `pkgcheck` when executable in the release environment | no unresolved blocking diagnostics | QUEUED |
| 7 | Establish immutable Release candidate | candidate frozen before final gates | QUEUED |
| 8 | Run Release phase-end regression | Static + complete Linux + Linux release check + release-specific acceptance PASS | QUEUED |
| 9 | Create/verify `v3.0.0` tag and GitHub Release only after candidate acceptance | published assets match accepted checksums | QUEUED |
| 10 | Perform any external CTAN submission only as explicit final action and record closeout | no unresolved release blocker | QUEUED |

## Hard boundaries

- Item 33 remains a current-authority gap and is not converted into speculative release work.
- Do not redistribute proprietary Microsoft fonts or UFC institutional mark assets.
- Do not weaken validation predicates to obtain a green release.
- Do not publish/tag from an unrecorded local or intermediate state.
- Do not describe candidate preparation as CTAN acceptance.
