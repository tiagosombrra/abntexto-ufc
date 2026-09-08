# V3.0.0 Release Readiness

Updated: 2026-09-08  
Status: ACTIVE — RELEASE EXECUTION

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE** | branch synchronized from merged `main`; execute final release checklist and own phase-end regression |

## Accepted Release entry

| Surface | Accepted state |
|---|---|
| Final Certification candidate | `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final complete Linux | `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final release matrix | `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Transition commit | `d3679f2caa35403887d2dc75f9b2486e5a3b7ba6` |
| Transition Static | `34249182526` SUCCESS |
| Transition Linux | `34249182417` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| PR #289 | merged |
| New `main` / Release branch base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active Release branch | `release/v3.0.0` |
| Literal fonts / Unicode / embedding / PDF/A | ACCEPTED |
| Scientific Article PDF/A-2b | PASS |
| Distribution baseline | 4 artifacts; checksums and archive integrity PASS |
| Deterministic release reference PDF | PASS; permanent gate retained |
| Issue #18 | CLOSED |
| Librarian item 33 | explicit authority gap; not speculative release work |

## Release execution order

| Order | Action | Gate | State |
|---:|---|---|---|
| 1 | Synchronize Release branch/control documents | Static contract green | ACTIVE |
| 2 | Re-read and reconcile `docs/CTAN-RELEASE.md` and repository release tooling | no stale/invented procedure | QUEUED |
| 3 | Build final public/distribution artifacts and checksums | reproducibility/integrity PASS | QUEUED |
| 4 | Extract CTAN candidate and compile shipped example using external `abntexto` | package/example validation PASS | QUEUED |
| 5 | Run current CTAN `pkgcheck` when executable in the release environment | no blocking diagnostics | QUEUED |
| 6 | Freeze one immutable Release candidate | no mutation after final gates begin | QUEUED |
| 7 | Run Static + complete Linux + Linux release check + release-specific verification on candidate | mandatory Release **phase-end regression** | QUEUED |
| 8 | Only after acceptance create/verify `v3.0.0` tag and GitHub Release | published assets/checksums match candidate | QUEUED |
| 9 | Perform any external CTAN submission only as an explicit documented action | submission/acceptance receipt retained | QUEUED |
| 10 | Record final verification and close Release | no unresolved release blocker | QUEUED |

## Current blockers

| Blocker | Exit condition |
|---|---|
| Release branch synchronization not yet accepted by CI | synchronized control-plane checkpoint Static green |
| Final release artifacts not yet rebuilt from Release candidate | artifact/reproducibility/integrity checks PASS |
| Release phase-end regression not yet executed | one immutable candidate passes all required release checks |
| Tag/GitHub Release/publication not yet verified | accepted candidate published and assets checked against SHA-256 metadata |
| External CTAN submission, if performed | explicit release action and receipt verification; candidate preparation alone is not acceptance |

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without its own complete **phase-end regression**.
