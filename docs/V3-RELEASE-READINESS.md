# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — ARTIFACT DELIVERY / IMMUTABLE CANDIDATE PREPARATION

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE** | transport accepted; durable candidate artifact delivery, immutable candidate regression, publication verification remain |

## Release branch facts

| Fact | Value |
|---|---|
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch / PR | `release/v3-release` / #293 |
| Entry synchronization checkpoint | `4fbd56930e4025da1a5463150c3cfd23005f6df4` |
| Entry Static | `34264486539` SUCCESS |
| Entry Linux | `34264486462` SUCCESS; heavy integration skipped because the incremental change was documentation-only; **not phase-end evidence** |
| Transport preparation checkpoint | `6a257f35b65266a1120826b816404116082b1e5c` |
| Transport Static | `34265429699` SUCCESS |
| Transport Linux | `34265429551` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Transport state | **ACCEPTED** |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Release phase-end transport

| Surface | State |
|---|---|
| Marker | `release/v3-release-candidate.json` |
| Linux suite inference | accepted: marker forces `complete` |
| Linux release workflow trigger | accepted: marker triggers PR `Linux release check` |
| Static self-test | accepted |
| Transport checkpoint | `6a257f35...` accepted on Static + complete Linux |
| Marker semantics | provenance/orchestration only; no runtime/normative change |
| Candidate contract | `docs/V3-RELEASE-PHASE-END.md` |

## Certified artifact provenance

The final distribution set must be produced by `make release-check` on the immutable Release candidate and retained by the permanent `Linux release check` workflow. The required publication set is:

- `dist/abntexto-ufc-3.0.0.zip`
- `dist/abntexto-ufc-ctan-3.0.0.zip`
- `dist/abntexto-ufc-template-3.0.0.zip`
- `dist/abntexto-ufc-overleaf-3.0.0.zip`
- `dist/SHA256SUMS`

A pre-candidate build can diagnose release packaging, but it cannot be substituted for the candidate-produced files attached to the GitHub Release.

## Release execution order

| Order | Action | Gate |
|---:|---|---|
| 1 | Add durable `dist/` upload to permanent `Linux release check` | technical change passes Static + complete Linux |
| 2 | Synchronize workflow acceptance in roadmap/handoff/readiness/machine state | same work cycle |
| 3 | Publish one immutable Release candidate containing `release/v3-release-candidate.json` | no candidate amendment after CI starts |
| 4 | Run complete Release phase-end regression | Static + complete Linux + Linux release check |
| 5 | Download/verify the candidate's retained distribution artifact | exact five-file set + checksums/integrity PASS |
| 6 | Only after acceptance, create `v3.0.0` tag/GitHub Release using the exact candidate files | published hashes match certified hashes |
| 7 | Perform explicit external publication only when checklist/tooling and required metadata are available | preserve receipt/evidence |
| 8 | Record final verification and close Release | no unresolved release blocker |

## Current blockers

| Blocker | Exit condition |
|---|---|
| Candidate distribution bytes are not yet durably retained by the release workflow | permanent artifact upload accepted |
| Release phase-end candidate not yet published | marker commit created after artifact-delivery tooling is accepted |
| Release phase-end regression not yet completed | immutable candidate passes all required gates |
| Tag/GitHub Release/publication assets not yet verified | published assets match candidate checksums |

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without its own complete **phase-end regression**.
