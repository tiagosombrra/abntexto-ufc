# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch / PR | `release/v3-release` / #293 |
| Active phase | **Release** |
| Release branch base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release entry sync | `4fbd56930e4025da1a5463150c3cfd23005f6df4` |
| Release transport preparation | **ACCEPTED** on `6a257f35b65266a1120826b816404116082b1e5c` |
| Transport Static | `34265429699` — SUCCESS |
| Transport complete Linux | `34265429551` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Certification | **CLOSED** on candidate `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final release check | `34239890548` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Current batch | **Release artifact delivery and immutable candidate preparation** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-RELEASE-PHASE-END.md`, `docs/CTAN-RELEASE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Accepted Release transport

The Release-specific CI transport is now accepted. On `6a257f35...`, Static `34265429699` passed and Linux `34265429551` actually ran the complete suite, finishing `SCOPE=complete PASS=36 FAIL=0 SKIP=0`.

| Predicate | Accepted result |
|---|---|
| Release marker recognized by Linux scope selector | PASS — forces `complete` |
| Release marker recognized by `Linux release check` PR trigger | PASS |
| Static orchestration self-test | PASS |
| Complete Linux integration | PASS |
| Product/normative semantics changed | No |
| Temporary executor introduced | No |

## Artifact provenance decision

The release checklist is tightened so publication bytes originate from the immutable Release candidate itself. The permanent `Linux release check` already executes `make release-check`, which builds and validates the distribution set. It must also retain `dist/` as a downloadable workflow artifact. Therefore:

- pre-candidate bundle builds are diagnostic only;
- the certified four ZIPs and `SHA256SUMS` are generated on the immutable candidate;
- those exact bytes are later attached to the GitHub Release;
- no separately rebuilt local ZIP is accepted as publication evidence.

This is a Release transport/provenance refinement only; it does not alter LaTeX runtime, normative rules or accepted review evidence.

## Immediate Release action

| Order | Action | Gate |
|---:|---|---|
| 1 | Add durable upload of the generated `dist/` set to permanent `Linux release check` | workflow/static review + complete Linux on the technical change |
| 2 | Synchronize acceptance of that workflow change in roadmap/handoff/readiness/machine state | same work cycle |
| 3 | Publish one immutable Release candidate containing `release/v3-release-candidate.json` | no candidate amendment after CI starts |
| 4 | Run Release **phase-end regression** | Static + `SCOPE=complete` Linux + `Linux release check` |
| 5 | Verify/download the candidate's four ZIPs and `SHA256SUMS` | exact candidate provenance + checksum/integrity PASS |
| 6 | Only after candidate acceptance, create/verify `v3.0.0` tag and GitHub Release with those exact assets | published hashes match candidate |
| 7 | Perform external publication only when explicit checklist/tooling and required metadata are available | preserve submission/acceptance evidence |
| 8 | Record final verification and close Release | no unresolved release blocker |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. A workflow conclusion of `success` never substitutes for required scope.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not reuse the Final Certification marker as Release identity.
- Do not claim CTAN acceptance without submission/acceptance evidence.
- Do not rebuild publication ZIPs after the accepted Release candidate; use the workflow-retained certified bytes.
