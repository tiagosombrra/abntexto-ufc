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
| Artifact-delivery implementation | **ACCEPTED** on `b55210acdb614fc3178e3ebf5b3a595bed8508c1` |
| Artifact-delivery Static | `34300561597` — SUCCESS |
| Artifact-delivery Linux | `34300561605` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Current batch | **Release immutable candidate preparation — publish Release marker next** |
| Final Certification | **CLOSED** on `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-RELEASE-PHASE-END.md`, `docs/CTAN-RELEASE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Artifact-delivery acceptance

The permanent `Linux release check` hardening at `b55210ac...` is accepted as bounded Release tooling work. It changes no LaTeX runtime or normative semantics.

| Predicate | Accepted result |
|---|---|
| Candidate checkout | explicit PR head / candidate SHA |
| Provenance | `SOURCE_COMMIT_SHA` bound to checkout SHA |
| Determinism | `SOURCE_DATE_EPOCH` derived from candidate commit |
| Release contract | `make release-check` retained |
| Final package build | `make distribution-bundles` after release contract |
| Integrity | `sha256sum -c SHA256SUMS` + exact five-file set |
| Artifact retention | four ZIPs + `SHA256SUMS` via pinned upload-artifact |
| Static acceptance | `34300561597` SUCCESS |
| Linux acceptance | `34300561605` SUCCESS, complete scope, 36/36 checks |

This acceptance authorizes candidate publication; it is not itself the Release phase-end regression.

## Immediate Release action

| Order | Action | Gate |
|---:|---|---|
| 1 | Publish one immutable Release candidate containing `release/v3-release-candidate.json` | candidate commit is not amended after CI starts |
| 2 | Run Release **phase-end regression** on that exact SHA | Static + `SCOPE=complete` Linux + `Linux release check` |
| 3 | Verify/download the candidate's four ZIPs and `SHA256SUMS` | exact candidate provenance + checksum/integrity PASS |
| 4 | Record candidate SHA, run IDs and retained artifact identity | documentation + machine-state synchronization after CI |
| 5 | Only after candidate acceptance, create/verify `v3.0.0` tag and GitHub Release using the exact retained files | published hashes match candidate |
| 6 | Perform external publication only when explicit checklist/tooling and required metadata are available | preserve submission/acceptance evidence |
| 7 | Record final verification and close Release | no unresolved release blocker |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not reuse the Final Certification marker as Release identity.
- Do not claim CTAN acceptance without submission/acceptance evidence.
- Do not rebuild publication ZIPs after the accepted candidate; publish the workflow-retained candidate bytes.
