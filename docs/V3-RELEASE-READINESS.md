# V3.0.0 Release Readiness

Updated: 2026-09-08  
Status: ACTIVE — RELEASE CANDIDATE TRANSPORT REPAIR

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE** | transport probe exposed scope/provenance defects; repair before final candidate freeze |

## Release transport probe readiness

| Surface | Current state |
|---|---|
| Probe SHA | `d1f86db10f1458ed75078239916f0de857671348` |
| Static | `34253455083` SUCCESS |
| Linux integration | `34253455068` SUCCESS but `SCOPE=smoke PASS=4 FAIL=0 SKIP=0` |
| Complete-Linux predicate | **NOT SATISFIED** |
| Linux release check | `34253454993` SUCCESS; `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Release-check artifact | ID `10067709957`; digest `2fc9a5f1dcadf330e2fb832c47e88fe00a6b0ffa2f7f5963291984f0de1f8c6e` |
| Distribution validation in release check | 4 archives; checksums and integrity PASS |
| Deterministic release reference PDF | 2 builds; SHA-256 `1acd4c47a1485d16c1b0cf92d074c6dc194dc8952c8f2c61709acbc6a9a503a7`; PDF/A/Unicode/font embedding PASS |
| Exact-head artifact provenance | not yet; release check used PR merge checkout |
| Librarian item 33 | explicit authority gap; unchanged |

`d1f86db...` is therefore **not Release-ready as a phase-end candidate**. The repository policy explicitly states that workflow success without the required execution scope does not satisfy the phase gate.

## Current blocker and repair

| Blocker | Root cause | Required exit condition |
|---|---|---|
| Complete Linux not forced by persistent marker | synchronize selector considers incremental changed paths; marker was introduced earlier | checked-out active marker overrides path inference to `complete` |
| Release-check artifacts not bound to exact head | default PR checkout uses merge ref | permanent release workflow explicitly checks out PR head and full Git history |
| No static Release transport contract | transport semantics distributed across path lists/workflows | permanent source check validates marker, scope override and exact-head route |

## Release execution order

| Order | Action | Gate | State |
|---:|---|---|---|
| 1 | Synchronize Release branch/control documents | Static `34252314666` | PASS |
| 2 | Establish readable non-temporary Release marker and permanent release-check trigger | transport route exists | PASS — probe |
| 3 | Repair persistent complete-scope selection and exact-head release checkout | Static + `SCOPE=complete` Linux + exact-head Linux release check | **ACTIVE** |
| 4 | Build final public/distribution artifacts and checksums from accepted route | reproducibility/integrity PASS | QUEUED |
| 5 | Extract CTAN candidate and compile shipped example using external `abntexto` | package/example validation PASS | QUEUED |
| 6 | Run current CTAN `pkgcheck` when executable | no blocking diagnostics; actual version recorded | QUEUED |
| 7 | Freeze one immutable Release candidate | no mutation after final gates begin | QUEUED |
| 8 | Run Static + complete Linux + Linux release check + release-specific verification | mandatory Release **phase-end regression** | QUEUED |
| 9 | Only after acceptance create/verify `v3.0.0` tag and GitHub Release | published assets/checksums match candidate | QUEUED |
| 10 | Perform external CTAN submission only as an explicit action and record final closeout | no unresolved blocker | QUEUED |

## Current tooling facts

| Surface | Finding |
|---|---|
| `make release-check` | covers release-mode suite + Scientific Article PDF/A + distribution bundles + deterministic release-reference reproducibility |
| Distribution bundles | four archives, SHA-256, safe paths, archive integrity and proprietary/institutional asset exclusions enforced |
| Current CTAN `pkgcheck` | project research records CTAN package page version 4.0.3 dated 2026-05-28; final run must record actual executable version |
| Candidate marker | `release/v3-release-candidate.json`, non-temporary, state `transport-probe` |
| Final candidate status | **not frozen** |

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without its own complete **phase-end regression** on an immutable candidate.
