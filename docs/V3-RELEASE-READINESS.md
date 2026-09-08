# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — RELEASE BRANCH

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE** | branch synchronized from merged `main`; execute checklist, phase-end regression, tag/Release/publication verification |

## Release branch facts

| Fact | Value |
|---|---|
| Merged Final Certification PR | #289 |
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch | `release/v3-release` |
| Release branch base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release PR | pending creation after synchronization commit |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Final Certification handoff to Release

| Surface | Accepted state |
|---|---|
| Final Certification candidate | `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Linux integration | `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Release matrix | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Literal fonts / Unicode / embedding / PDF/A | ACCEPTED |
| Scientific Article PDF/A-2b | PASS |
| Distribution bundles | 4 artifacts; checksums and archive integrity PASS |
| Deterministic release reference PDF | PASS; permanent gate retained |
| Issue #18 | CLOSED |
| Temporary certification executor | absent |
| Librarian item 33 | explicit authority gap; not a speculative release task |

## Release execution order

| Order | Action | Gate |
|---:|---|---|
| 1 | Synchronize branch facts from merged `main` | DONE by first Release checkpoint |
| 2 | Create Release PR | record PR number in control plane |
| 3 | Re-read `docs/CTAN-RELEASE.md` and repository release tooling | no invented publication step |
| 4 | Build final public/distribution artifacts and checksums | reproducible/integrity gates green |
| 5 | Run complete release verification on one immutable Release candidate | mandatory Release **phase-end regression** |
| 6 | Only after acceptance, create `v3.0.0` tag/GitHub Release and perform explicit documented publication | verify published assets/checksums afterwards |
| 7 | Record final publication/verification evidence and close Release | no unresolved release blocker |

## Current blockers

| Blocker | Exit condition |
|---|---|
| Release PR not yet created | create PR after branch synchronization commit |
| Release execution and phase-end regression not yet completed | one immutable Release candidate passes all required release checks |
| Publication not yet verified | tag/Release/publication assets verified against accepted checksums |

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without its own complete **phase-end regression**.
