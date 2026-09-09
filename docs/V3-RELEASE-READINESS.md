# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — IMMUTABLE CANDIDATE PREPARATION

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE** | transport and artifact delivery accepted; immutable candidate regression/publication remain |

## Release branch facts

| Fact | Value |
|---|---|
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch / PR | `release/v3-release` / #293 |
| Transport preparation checkpoint | `6a257f35b65266a1120826b816404116082b1e5c` |
| Transport Static / Linux | `34265429699` SUCCESS / `34265429551` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Artifact-delivery checkpoint | `b55210acdb614fc3178e3ebf5b3a595bed8508c1` |
| Artifact-delivery Static | `34300561597` SUCCESS |
| Artifact-delivery Linux | `34300561605` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Artifact-delivery acceptance

The permanent `Linux release check` implementation is accepted as Release tooling. It ensures final publication assets can be retained from the exact immutable candidate SHA.

| Predicate | Accepted behavior | Evidence |
|---|---|---|
| Candidate checkout | explicit PR head / `github.sha` fallback | `b55210ac...` |
| Source provenance | `SOURCE_COMMIT_SHA` equals checkout SHA | implementation + complete Linux PASS |
| Reproducible timestamp | `SOURCE_DATE_EPOCH` from candidate commit | implementation + complete Linux PASS |
| Release validation | `make release-check` | preserved |
| Final archive generation | `make distribution-bundles` | preserved |
| Checksum verification | `sha256sum -c SHA256SUMS` | preserved |
| Exact output set | four v3.0.0 ZIPs + `SHA256SUMS` only | workflow contract |
| Workflow retention | pinned upload-artifact, 30-day retention | workflow contract |

No runtime/normative behavior changed by this transport implementation.

## Release execution order

| Order | Action | Gate |
|---:|---|---|
| 1 | Publish one immutable Release candidate containing `release/v3-release-candidate.json` | no candidate amendment after CI starts |
| 2 | Run complete Release phase-end regression | Static + complete Linux + Linux release check |
| 3 | Download/verify candidate-retained distribution artifact | exact five-file set + checksums/integrity PASS |
| 4 | Synchronize accepted candidate SHA/run IDs/artifact identity | documentation + machine state |
| 5 | Only after acceptance, create `v3.0.0` tag/GitHub Release using exact candidate files | published hashes match candidate |
| 6 | Perform explicit external publication only when checklist/tooling and required metadata are available | preserve receipt/evidence |
| 7 | Record final verification and close Release | no unresolved release blocker |

## Current blockers

| Blocker | Exit condition |
|---|---|
| Release phase-end candidate not yet published | marker commit created after accepted artifact tooling |
| Release phase-end regression not yet completed | immutable candidate passes all required gates |
| Tag/GitHub Release/publication assets not yet verified | published assets match candidate checksums |

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without its own complete **phase-end regression**.
