# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — RELEASE ENTRY

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | **CLOSED** | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE** | merge certified PR, synchronize a short-lived release branch, execute release checklist, then phase-end regression |

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
| One-shot Final Certification marker | removed by phase-transition commit |
| Librarian item 33 | explicit authority gap; not a speculative release task |

## Release execution order

| Order | Action | Gate |
|---:|---|---|
| 1 | Validate this Final Certification → Release transition checkpoint | Static and triggered Linux remain green |
| 2 | Merge PR #289 into `main` | PR mergeable and transition checks green |
| 3 | Read new `main` SHA and create one short-lived Release branch | machine/handoff/roadmap synchronized to branch facts |
| 4 | Re-read `docs/CTAN-RELEASE.md` and repository release tooling | no invented publication step |
| 5 | Build final public/distribution artifacts and checksums from the Release candidate | reproducible/integrity gates green |
| 6 | Run complete release verification on one immutable Release candidate | mandatory Release **phase-end regression** |
| 7 | Only after acceptance, create `v3.0.0` tag/GitHub Release and perform publication actions explicitly required by the release checklist | verify published assets/checksums afterwards |
| 8 | Record final publication/verification evidence and close Release | no unresolved release blocker |

## Current blockers

| Blocker | Exit condition |
|---|---|
| PR #289 transition not yet merged | transition checkpoint green and PR merged |
| Release task branch not yet synchronized from new `main` | create branch after merge and update control plane |
| Release phase-end regression not yet executed | one immutable Release candidate passes all required release checks |
| Publication not yet verified | tag/Release/publication assets verified against accepted checksums |

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without its own complete **phase-end regression**.
