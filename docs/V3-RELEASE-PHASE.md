# V3 Release Phase

Updated: 2026-09-08  
Status: ACTIVE — RELEASE EXECUTION

## Purpose

This document is the execution record for the final roadmap phase. It begins after PR #289 merged Final Certification into `main` and after the short-lived `release/v3.0.0` branch was created from that merged main state.

Every **material advance** in Release updates this record, the canonical handoff, roadmap, release readiness and machine state in the same work cycle. Release closes only after a complete **phase-end regression** on one immutable candidate SHA.

## Entry evidence

| Predicate | Accepted evidence |
|---|---|
| Final Certification candidate | `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final Static | `34239890649` — SUCCESS |
| Final complete Linux | `34239890614` — SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Linux release check | `34239890548` — SUCCESS; `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Transition commit | `d3679f2caa35403887d2dc75f9b2486e5a3b7ba6` |
| Transition Static | `34249182526` — SUCCESS |
| Transition Linux | `34249182417` — SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| PR #289 merge / Release base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active Release branch | `release/v3.0.0` |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Release execution queue

| Order | Work | Acceptance gate | State |
|---:|---|---|---|
| 1 | Synchronize Release branch facts and current documentation | Static contract green on synchronized checkpoint | ACTIVE |
| 2 | Revalidate repository release checklist and current tooling | no stale/invented release procedure | QUEUED |
| 3 | Build public/distribution release artifacts and SHA-256 metadata | archive/integrity/reproducibility checks PASS | QUEUED |
| 4 | Validate extracted CTAN candidate and shipped example | external `abntexto` semantics and package checks PASS | QUEUED |
| 5 | Run current CTAN `pkgcheck` when executable in the release environment | no unresolved error/warning that blocks submission | QUEUED |
| 6 | Establish immutable Release candidate | candidate frozen before final gates | QUEUED |
| 7 | Run Release phase-end regression | Static + complete Linux + Linux release check + release-specific acceptance PASS | QUEUED |
| 8 | Create/verify `v3.0.0` tag and GitHub Release only after candidate acceptance | published assets match accepted checksums | QUEUED |
| 9 | Perform any external CTAN submission only as an explicit final release action | submission/acceptance receipt preserved | QUEUED |
| 10 | Record final verification and close Release | no unresolved release blocker | QUEUED |

## Hard boundaries

- Item 33 remains a current-authority gap and is not converted into speculative release work.
- Do not redistribute proprietary Microsoft fonts or UFC institutional mark assets.
- Do not weaken validation predicates to obtain a green release.
- Do not publish/tag from an unrecorded local or intermediate state.
- Do not describe candidate preparation as CTAN acceptance.
