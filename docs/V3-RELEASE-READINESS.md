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
| Release | **ACTIVE** | branch synchronization accepted; reconcile final candidate transport/tooling, then execute final checklist and own phase-end regression |

## Accepted Release entry and synchronization

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
| Active Release branch / PR | `release/v3.0.0` / #292 |
| Synchronization checkpoint | `3fad68d953b1264148431d7d1046666674b1a240` |
| Synchronization Static | `34252314666` SUCCESS |
| Synchronization Linux | `34252314932` SUCCESS; docs-only heavy integration skipped as intended |
| Literal fonts / Unicode / embedding / PDF/A | ACCEPTED |
| Scientific Article PDF/A-2b | PASS |
| Distribution baseline | 4 artifacts; checksums and archive integrity PASS |
| Deterministic release reference PDF | PASS; permanent gate retained |
| Issue #18 | CLOSED |
| Librarian item 33 | explicit authority gap; not speculative release work |

## Release execution order

| Order | Action | Gate | State |
|---:|---|---|---|
| 1 | Synchronize Release branch/control documents | Static `34252314666` | **PASS** |
| 2 | Reconcile `docs/CTAN-RELEASE.md`, repository tooling and exact candidate CI transport | no stale/invented procedure; exact candidate can run complete Linux + Linux release check | **ACTIVE** |
| 3 | Build final public/distribution artifacts and checksums | reproducibility/integrity PASS | QUEUED |
| 4 | Extract CTAN candidate and compile shipped example using external `abntexto` | package/example validation PASS | QUEUED |
| 5 | Run current CTAN `pkgcheck` when executable in the release environment | no blocking diagnostics; actual version recorded | QUEUED |
| 6 | Freeze one immutable Release candidate | no mutation after final gates begin | QUEUED |
| 7 | Run Static + complete Linux + Linux release check + release-specific verification on candidate | mandatory Release **phase-end regression** | QUEUED |
| 8 | Only after acceptance create/verify `v3.0.0` tag and GitHub Release | published assets/checksums match candidate | QUEUED |
| 9 | Perform any external CTAN submission only as an explicit documented action | submission/acceptance receipt retained | QUEUED |
| 10 | Record final verification and close Release | no unresolved release blocker | QUEUED |

## Current tooling findings

| Surface | Finding |
|---|---|
| `make release-check` | already covers release-mode suite + Scientific Article PDF/A + distribution bundle validation + deterministic release-reference reproducibility |
| Distribution bundles | four archives, SHA-256, safe paths, archive integrity and proprietary/institutional asset exclusions already enforced |
| Current CTAN `pkgcheck` | CTAN package page reports 4.0.3 dated 2026-05-28 |
| Final candidate PR trigger | still tied to `release/final-certification-candidate.json`; Release needs a readable non-temporary candidate surface |

## Current blockers

| Blocker | Exit condition |
|---|---|
| Exact Release candidate transport not yet established | complete Linux and Linux release check execute on the same final Release SHA without temporary Final-Certification semantics |
| Final release artifacts not yet rebuilt from Release candidate | artifact/reproducibility/integrity checks PASS |
| Extracted CTAN example/current `pkgcheck` not yet recorded for final candidate | release-specific validation PASS |
| Release phase-end regression not yet executed | one immutable candidate passes all required release checks |
| Tag/GitHub Release/publication not yet verified | accepted candidate published and assets checked against SHA-256 metadata |
| External CTAN submission, if performed | explicit release action and receipt verification; candidate preparation alone is not acceptance |

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without its own complete **phase-end regression**.
