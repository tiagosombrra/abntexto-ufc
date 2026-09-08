# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` / Release base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch / PR | `release/v3.0.0` / #292 |
| Active phase | **Release** |
| Final Certification | **CLOSED** on candidate `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Release transport probe | `d1f86db10f1458ed75078239916f0de857671348` |
| Probe Static | `34253455083` SUCCESS |
| Probe Linux | `34253455068` workflow SUCCESS; **`SCOPE=smoke PASS=4 FAIL=0 SKIP=0` — phase-end predicate NOT satisfied** |
| Probe Linux release check | `34253454993` SUCCESS; `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Release-check artifact | `linux-release-validation-34253454993`, ID `10067709957`, digest `2fc9a5f1dcadf330e2fb832c47e88fe00a6b0ffa2f7f5963291984f0de1f8c6e` |
| Probe release-reference reproducibility | PASS; SHA-256 `1acd4c47a1485d16c1b0cf92d074c6dc194dc8952c8f2c61709acbc6a9a503a7`, 450652 bytes |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Current batch | **Release candidate transport repair** |

Canonical Release control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-PHASE.md`, `docs/V3-RELEASE-READINESS.md`, `docs/CTAN-RELEASE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Accepted entry

The Final Certification → Release transition remains accepted. PR #289 was squash-merged into `main` as `e34037f3241aab013b80645b338f38954e02bcda`, and `release/v3.0.0` was created from that exact main SHA. No accepted runtime, normative predicate, tolerance or librarian classification has been reopened.

## Release transport probe classification

The non-temporary Release marker and permanent Linux release-check trigger are present, but `d1f86db...` exposed two transport defects that prevent phase-end acceptance.

| Predicate | Observation | Classification |
|---|---|---|
| Static contract | `34253455083` SUCCESS | PASS |
| Complete Linux required | `34253455068` ran `SCOPE=smoke`, `PASS=4` | **FAIL-CLOSED for phase-end** |
| Linux release check | `34253454993`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` | bounded PASS |
| Distribution bundles | 4 artifacts, checksums/integrity PASS in release check | bounded PASS |
| Deterministic reference PDF | 2 builds, SHA-256 `1acd4c47...`, PDF/A/Unicode/font embedding PASS | bounded PASS |
| Exact-head release provenance | release workflow checked out PR merge ref rather than the immutable PR head | **transport defect** |

The Linux scope failure occurred because synchronize events use the incremental `before → after` diff. The Release marker had been added on an earlier commit, so the later orchestration-only diff selected `smoke`. Merely putting the marker path in `FORCE_COMPLETE_EXACT` is insufficient when the marker is persistent but absent from that incremental diff.

## Current repair

The synchronized repair must:

1. make an active, non-temporary `release/v3-release-candidate.json` in the checked-out HEAD force `complete` regardless of incremental changed paths;
2. preserve bounded auto scopes when no active Release candidate is present;
3. add static/self-test coverage for documentation-only and orchestration-only incremental diffs under an active Release marker;
4. make `Linux release check` checkout `${{ github.event.pull_request.head.sha || github.sha }}` with `fetch-depth: 0` so Release artifacts and reproducibility evidence are tied to the exact head candidate;
5. add a permanent static Release-candidate transport contract.

## Immediate Release action

| Order | Action | Gate | State |
|---:|---|---|---|
| 1 | Synchronize Release branch/control plane | Static `34252314666` | PASS |
| 2 | Establish non-temporary Release marker and trigger release check | marker + release workflow route | PASS — transport probe |
| 3 | Repair persistent-marker complete-scope selection and exact-head release checkout | Static + complete Linux + Linux release check | **ACTIVE** |
| 4 | Build/verify final public/distribution artifacts and checksums from exact-head route | integrity/reproducibility PASS | QUEUED |
| 5 | Validate extracted CTAN candidate and shipped example | external dependency/package checks PASS | QUEUED |
| 6 | Run current CTAN `pkgcheck` when executable | no blocking diagnostics; actual version recorded | QUEUED |
| 7 | Freeze one immutable Release candidate | no candidate mutation after final gates begin | QUEUED |
| 8 | Run Release **phase-end regression** | Static + complete Linux + Linux release check + release-specific acceptance PASS | QUEUED |
| 9 | Create/verify `v3.0.0` tag and GitHub Release only after acceptance | published assets match accepted checksums | QUEUED |
| 10 | Perform external CTAN submission only as explicit final action, then record final verification | no unresolved blocker | QUEUED |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Workflow conclusion `success` without the required execution scope or provenance never satisfies a phase gate. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts or UFC institutional mark assets.
- Librarian item 33 remains fail-closed.
- Release publication actions must follow the repository release checklist; candidate preparation is not CTAN acceptance.
