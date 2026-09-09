# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch / PR | `release/v3-release` / #293 |
| Active phase | **Release** |
| Release transport preparation | **ACCEPTED** on `6a257f35b65266a1120826b816404116082b1e5c` |
| Transport Static / Linux | `34265429699` SUCCESS / `34265429551` SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Control-plane reconciliation | `eededce34d81df6b50206cdf11dc8707dde20152`; Static `34300202909` SUCCESS; Linux docs-only heavy skip |
| Current batch | **Release artifact delivery implementation — CI pending** |
| Final Certification | **CLOSED** on `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-RELEASE-PHASE-END.md`, `docs/CTAN-RELEASE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Current material advance

The permanent `Linux release check` is being changed so the final publication bytes have exact candidate provenance:

| Surface | Implemented behavior | Acceptance state |
|---|---|---|
| Checkout | explicit PR head / candidate SHA | CI pending |
| Provenance | `SOURCE_COMMIT_SHA` bound to checkout SHA | CI pending |
| Determinism | `SOURCE_DATE_EPOCH` from candidate commit time | CI pending |
| Release contract | `make release-check` remains mandatory | CI pending |
| Final package build | `make distribution-bundles` after release contract | CI pending |
| Integrity | `sha256sum -c SHA256SUMS` + exact file-set check | CI pending |
| Artifact retention | four ZIPs + `SHA256SUMS` uploaded by permanent workflow | CI pending |

No LaTeX runtime or normative rule is changed by this Release transport work.

## Acceptance rule for this advance

The implementation commit must pass Static contract and **complete** Linux integration. A green workflow with heavy integration skipped is insufficient. The exact implementation SHA and run IDs are recorded in a later documentation-only acceptance synchronization after CI finishes.

## Immediate Release action

| Order | Action | Gate |
|---:|---|---|
| 1 | Validate artifact-delivery implementation | Static + complete Linux green |
| 2 | Record implementation SHA/run IDs | documentation + machine-state synchronization |
| 3 | Publish one immutable Release candidate containing `release/v3-release-candidate.json` | candidate not amended after CI starts |
| 4 | Run Release **phase-end regression** | Static + `SCOPE=complete` Linux + `Linux release check` |
| 5 | Verify/download the candidate's four ZIPs and `SHA256SUMS` | exact candidate provenance + checksum/integrity PASS |
| 6 | Only after candidate acceptance, create/verify `v3.0.0` tag and GitHub Release with those exact assets | published hashes match candidate |
| 7 | Perform external publication only when explicit checklist/tooling and required metadata are available | preserve submission/acceptance evidence |
| 8 | Record final verification and close Release | no unresolved release blocker |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Release ends with its own complete **phase-end regression** on one immutable SHA.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not reuse the Final Certification marker as Release identity.
- Do not claim CTAN acceptance without submission/acceptance evidence.
- Do not rebuild publication ZIPs after the accepted candidate; publish the workflow-retained candidate bytes.
