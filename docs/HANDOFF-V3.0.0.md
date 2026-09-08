# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch / PR | `release/v3-release` / #293 |
| Active phase | **Release** |
| Release entry sync | `4fbd56930e4025da1a5463150c3cfd23005f6df4`; Static `34264486539` SUCCESS; Linux `34264486462` SUCCESS with heavy integration skipped as documentation-only |
| Final Certification | **CLOSED** on candidate `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final complete Linux | `34239890614` SUCCESS — `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Linux release check | `34239890548` SUCCESS — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Current batch | **Release phase-end candidate transport preparation** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-RELEASE-PHASE-END.md`, `docs/CTAN-RELEASE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Current Release advance

The permanent CI orchestration is being extended with the Release-specific marker `release/v3-release-candidate.json`. It is separate from the historical Final Certification marker and exists only to force the required phase-end execution contract.

| Predicate | Required behavior |
|---|---|
| Release marker in scoped Linux selector | forces `complete` |
| Release marker in `Linux release check` PR paths | triggers `make release-check` |
| Static self-test | verifies both properties |
| Product/normative semantics | unchanged |

This transport-preparation commit must pass Static and complete Linux before the immutable Release candidate marker is published.

## Immediate Release action

| Order | Action | Gate |
|---:|---|---|
| 1 | Validate Release candidate-transport preparation | Static + complete Linux green |
| 2 | Build/verify final distribution artifacts and checksums | reproducibility/integrity PASS |
| 3 | Publish one immutable Release candidate with `release/v3-release-candidate.json` | candidate not amended after CI starts |
| 4 | Run Release **phase-end regression** | Static + `SCOPE=complete` Linux + `Linux release check` |
| 5 | Only after candidate acceptance, create/verify `v3.0.0` tag and GitHub Release | assets/checksums verified |
| 6 | Perform external publication only when explicit checklist/tooling and required metadata are available | preserve submission/acceptance evidence |
| 7 | Record final verification and close Release | no unresolved release blocker |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. A workflow conclusion of `success` never substitutes for required scope.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not reuse the Final Certification marker as Release identity.
- Do not claim CTAN acceptance without submission/acceptance evidence.
