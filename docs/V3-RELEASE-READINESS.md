# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — ARTIFACT DELIVERY IMPLEMENTATION / CI PENDING

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE** | transport accepted; artifact-delivery implementation pending CI; immutable candidate regression/publication remain |

## Release branch facts

| Fact | Value |
|---|---|
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch / PR | `release/v3-release` / #293 |
| Transport preparation checkpoint | `6a257f35b65266a1120826b816404116082b1e5c` |
| Transport Static | `34265429699` SUCCESS |
| Transport Linux | `34265429551` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Control reconciliation | `eededce34d81df6b50206cdf11dc8707dde20152`; Static `34300202909` SUCCESS; Linux docs-only heavy skip |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Artifact-delivery implementation

The permanent `Linux release check` implementation now pending CI is designed to ensure final publication assets come from the exact immutable candidate SHA.

| Predicate | Implemented behavior | Acceptance |
|---|---|---|
| Candidate checkout | explicit PR head / `github.sha` fallback | pending Static + complete Linux |
| Source provenance | `SOURCE_COMMIT_SHA` equals checkout SHA | pending |
| Reproducible timestamp | `SOURCE_DATE_EPOCH` from candidate commit | pending |
| Release validation | `make release-check` | pending |
| Final archive generation | `make distribution-bundles` | pending |
| Checksum verification | `sha256sum -c SHA256SUMS` | pending |
| Exact output set | four v3.0.0 ZIPs + `SHA256SUMS` only | pending |
| Workflow retention | pinned upload-artifact, 30-day retention | pending |

No runtime/normative behavior is changed by this transport implementation.

## Release execution order

| Order | Action | Gate |
|---:|---|---|
| 1 | Validate artifact-delivery implementation | Static + complete Linux |
| 2 | Synchronize accepted implementation SHA/run IDs | documentation + machine state |
| 3 | Publish one immutable Release candidate containing `release/v3-release-candidate.json` | no candidate amendment after CI starts |
| 4 | Run complete Release phase-end regression | Static + complete Linux + Linux release check |
| 5 | Download/verify candidate-retained distribution artifact | exact five-file set + checksums/integrity PASS |
| 6 | Only after acceptance, create `v3.0.0` tag/GitHub Release using exact candidate files | published hashes match candidate |
| 7 | Perform explicit external publication only when checklist/tooling and required metadata are available | preserve receipt/evidence |
| 8 | Record final verification and close Release | no unresolved release blocker |

## Current blockers

| Blocker | Exit condition |
|---|---|
| Artifact-delivery implementation not yet accepted | Static + complete Linux green on implementation SHA |
| Release phase-end candidate not yet published | marker commit created after tooling acceptance |
| Release phase-end regression not yet completed | immutable candidate passes all required gates |
| Tag/GitHub Release/publication assets not yet verified | published assets match candidate checksums |

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without its own complete **phase-end regression**.
