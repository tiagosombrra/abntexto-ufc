# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` / Release base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch / PR | `release/v3.0.0` / #292 |
| Active phase | **Release** |
| Release synchronization checkpoint | `3fad68d953b1264148431d7d1046666674b1a240` |
| Synchronization Static | `34252314666` SUCCESS |
| Synchronization Linux | `34252314932` SUCCESS — heavy integration skipped because the checkpoint was documentation-only |
| Transition Static | `34249182526` SUCCESS |
| Transition complete Linux | `34249182417` SUCCESS — `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Certification | **CLOSED** on candidate `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final Static | `34239890649` SUCCESS |
| Final complete Linux | `34239890614` SUCCESS — `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Linux release check | `34239890548` SUCCESS — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Release-reference reproducibility | PASS; SHA-256 `ae4d7755d18e05abd572a0ad95e5696e54302f9ac236b1efc004d46f57216479` for two accepted builds |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Current batch | **Release tooling reconciliation and final candidate transport** |

Canonical Release control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-PHASE.md`, `docs/V3-RELEASE-READINESS.md`, `docs/CTAN-RELEASE.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Accepted entry and synchronization

The Final Certification → Release transition is accepted. Commit `d3679f2caa35403887d2dc75f9b2486e5a3b7ba6` passed Static `34249182526` and complete Linux `34249182417`. PR #289 was squash-merged into `main` as `e34037f3241aab013b80645b338f38954e02bcda`, and `release/v3.0.0` was created from that exact main SHA.

The first synchronized Release checkpoint `3fad68d...` then passed Static `34252314666`. Linux run `34252314932` also concluded successfully and explicitly skipped heavy integration because only documentation/control-plane surfaces changed; this is an intermediate synchronization result, not the Release phase-end regression.

No runtime, normative predicate, accepted tolerance or librarian classification changed in these steps.

## Release tooling review

| Surface | Current finding |
|---|---|
| `make release-check` | already includes full release-mode validation, Scientific Article PDF/A, distribution bundles and deterministic reference-PDF reproducibility |
| Distribution bundle gate | already validates four archives, SHA-256 metadata, safe paths, integrity and proprietary/institutional asset exclusion |
| CTAN `pkgcheck` | CTAN currently reports version 4.0.3 (2026-05-28); final candidate must record the version actually run |
| Extracted CTAN candidate example | still needs an explicit final-candidate execution record |
| Final Release PR transport | current `Linux release check` PR trigger is Final-Certification-specific; Release needs a readable, non-temporary candidate transport |

## Immediate Release action

| Order | Action | Gate | State |
|---:|---|---|---|
| 1 | Synchronize branch facts, roadmap, handoff, readiness and machine state | Static `34252314666` | **PASS** |
| 2 | Reconcile Release candidate transport with permanent Linux workflows | complete Linux + release check can execute on exact Release candidate | **ACTIVE** |
| 3 | Build and verify public/distribution artifacts and SHA-256 metadata | integrity/reproducibility PASS | QUEUED |
| 4 | Validate extracted CTAN candidate and shipped example | external dependency/package checks PASS | QUEUED |
| 5 | Run current CTAN `pkgcheck` when executable | no blocking diagnostics | QUEUED |
| 6 | Establish one immutable Release candidate | candidate frozen before final checks | QUEUED |
| 7 | Run Release **phase-end regression** | Static + complete Linux + Linux release check + release-specific acceptance PASS | QUEUED |
| 8 | Create/verify `v3.0.0` tag and GitHub Release only after candidate acceptance | published assets match accepted checksums | QUEUED |
| 9 | Perform any external CTAN submission only as an explicit final checklist action | submission/acceptance evidence preserved | QUEUED |
| 10 | Record final verification and close Release | no unresolved release blocker | QUEUED |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts or UFC institutional mark assets.
- Librarian item 33 remains fail-closed.
- Release publication actions must follow the repository release checklist; do not invent external publication steps.
- Candidate preparation is not CTAN acceptance.
