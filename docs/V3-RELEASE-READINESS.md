# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — RELEASE PHASE-END TRANSPORT PREPARATION

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE** | PR #293; prepare Release-specific candidate transport, execute checklist, phase-end regression, then publication verification |

## Release branch facts

| Fact | Value |
|---|---|
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch / PR | `release/v3-release` / #293 |
| Entry synchronization checkpoint | `4fbd56930e4025da1a5463150c3cfd23005f6df4` |
| Entry Static | `34264486539` SUCCESS |
| Entry Linux | `34264486462` SUCCESS; heavy integration skipped because the incremental change was documentation-only; **not phase-end evidence** |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Release phase-end transport

| Surface | Required state |
|---|---|
| Marker | `release/v3-release-candidate.json` |
| Linux suite inference | marker forces `complete` |
| Linux release workflow | marker triggers PR `Linux release check` |
| Static contract | self-tests both orchestration properties |
| Marker semantics | provenance/orchestration only; no runtime/normative change |
| Candidate contract | `docs/V3-RELEASE-PHASE-END.md` |

The transport-preparation implementation must itself pass Static and complete Linux before the candidate marker is introduced.

## Release execution order

| Order | Action | Gate |
|---:|---|---|
| 1 | Validate Release transport preparation | Static + complete Linux |
| 2 | Build final public/distribution artifacts and checksums | reproducible/integrity gates green |
| 3 | Publish one immutable Release candidate containing the Release marker | no candidate amendment after CI starts |
| 4 | Run complete Release phase-end regression | Static + complete Linux + Linux release check |
| 5 | Only after acceptance, create `v3.0.0` tag/GitHub Release | verify published assets/checksums |
| 6 | Perform explicit external publication only when checklist/tooling and required metadata are available | preserve receipt/evidence |
| 7 | Record final verification and close Release | no unresolved release blocker |

## Current blockers

| Blocker | Exit condition |
|---|---|
| Candidate transport not yet accepted | preparation commit passes required CI |
| Release artifacts/checksums not yet built from final candidate | checklist evidence PASS |
| Release phase-end regression not yet completed | immutable candidate passes all required gates |
| Publication not yet verified | tag/Release/publication assets verified against accepted checksums |

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without its own complete **phase-end regression**.
