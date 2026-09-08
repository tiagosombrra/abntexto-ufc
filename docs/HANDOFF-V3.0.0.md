# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` / Release base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch | `release/v3.0.0` |
| Final Certification transition PR | #289 — merged |
| Active phase | **Release** |
| Transition Static | `34249182526` SUCCESS |
| Transition complete Linux | `34249182417` SUCCESS — `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Certification | **CLOSED** on candidate `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final Static | `34239890649` SUCCESS |
| Final complete Linux | `34239890614` SUCCESS — `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Linux release check | `34239890548` SUCCESS — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Release-reference reproducibility | PASS; SHA-256 `ae4d7755d18e05abd572a0ad95e5696e54302f9ac236b1efc004d46f57216479` for two accepted builds |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Current batch | **Release execution — branch synchronization and release candidate preparation** |

Canonical Release control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-PHASE.md`, `docs/V3-RELEASE-READINESS.md`, `docs/CTAN-RELEASE.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Accepted entry to Release

The Final Certification → Release transition is accepted. Commit `d3679f2caa35403887d2dc75f9b2486e5a3b7ba6` passed Static `34249182526` and Linux `34249182417`; the Linux log confirms `SCOPE=complete PASS=36 FAIL=0 SKIP=0`. PR #289 was then squash-merged into `main` as `e34037f3241aab013b80645b338f38954e02bcda`, and `release/v3.0.0` was created from that exact main SHA.

No runtime, normative predicate, accepted tolerance or librarian classification changed in this transition.

## Immediate Release action

| Order | Action | Gate | State |
|---:|---|---|---|
| 1 | Synchronize branch facts, roadmap, handoff, readiness and machine state | Static contract on synchronized checkpoint | ACTIVE |
| 2 | Re-read and reconcile `docs/CTAN-RELEASE.md` with current Release state/tooling | no stale or invented release procedure | QUEUED |
| 3 | Build and verify public/distribution artifacts and SHA-256 metadata | integrity/reproducibility PASS | QUEUED |
| 4 | Validate extracted CTAN candidate and shipped example | external dependency/package checks PASS | QUEUED |
| 5 | Establish one immutable Release candidate | candidate frozen before final checks | QUEUED |
| 6 | Run Release **phase-end regression** | Static + complete Linux + Linux release check + release-specific acceptance PASS | QUEUED |
| 7 | Create/verify `v3.0.0` tag and GitHub Release only after candidate acceptance | published assets match accepted checksums | QUEUED |
| 8 | Perform any external CTAN submission only if explicitly authorized by the final checklist | submission/acceptance evidence preserved | QUEUED |
| 9 | Record final verification and close Release | no unresolved release blocker | QUEUED |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts or UFC institutional mark assets.
- Librarian item 33 remains fail-closed.
- Release publication actions must follow the repository release checklist; do not invent external publication steps.
- Candidate preparation is not CTAN acceptance.
