# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch | `release/v3-release` |
| Release PR | pending creation after this synchronization checkpoint |
| Active phase | **Release** |
| Final Certification | **CLOSED** on candidate `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final Static | `34239890649` SUCCESS |
| Final complete Linux | `34239890614` SUCCESS — `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Linux release check | `34239890548` SUCCESS — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Final Certification merge | PR #289 merged to `main` as `e34037f3241aab013b80645b338f38954e02bcda` |
| Release-reference reproducibility | PASS; accepted certification SHA-256 `ae4d7755d18e05abd572a0ad95e5696e54302f9ac236b1efc004d46f57216479` |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Current batch | **Release branch synchronization and repository release-checklist execution** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-READINESS.md`, `docs/CTAN-RELEASE.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Release entry acceptance

PR #289 is merged. The Release branch is based exactly on merged `main` `e34037f...`. Final Certification remains accepted and immutable; Release does not reopen it absent a concrete regression.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence and is not converted into speculative runtime work.

## Immediate Release action

| Order | Action | Gate |
|---:|---|---|
| 1 | Synchronize branch/handoff/roadmap/readiness/machine facts | same work cycle |
| 2 | Create the Release PR | branch and PR facts recorded |
| 3 | Execute `docs/CTAN-RELEASE.md` and repository release tooling | no invented publication step |
| 4 | Build final distribution artifacts and checksums | integrity/reproducibility PASS |
| 5 | Establish one immutable Release candidate | candidate is not amended after CI starts |
| 6 | Run Release **phase-end regression** | Static + complete Linux + Linux release check green |
| 7 | Create/verify `v3.0.0` tag and GitHub Release only after accepted candidate | published assets/checksums verified |
| 8 | Perform any external publication only when explicitly supported by the checklist and available tooling | preserve receipt/evidence |
| 9 | Record final verification and close Release | no unresolved release blocker |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Release publication actions must follow the repository release checklist; do not invent external publication steps.
