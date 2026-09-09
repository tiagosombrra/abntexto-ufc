# V3.0.0 Release Readiness

Updated: 2026-09-09
Status: ACTIVE — PUBLICATION CLOSEOUT

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | immutable certification candidate and heavy matrix accepted |
| Release | **ACTIVE** | candidate accepted, PR #293 and PR #294 merged; tag/GitHub Release and post-publication verification remain |

## Canonical Release facts

| Fact | Value |
|---|---|
| Canonical branch | `main` |
| Last merged publication-closeout synchronization checkpoint | `c39af06e236b6b61fcf6d11bc383ac5752093cec` |
| Release work branch | `release/v3-release`, synchronized to that canonical checkpoint |
| Release PR #293 | **MERGED** as squash commit `add52f2183f18d6cea3e9477f2a45416a13cfc36` |
| Publication-closeout PR #294 | **MERGED** as `c39af06e236b6b61fcf6d11bc383ac5752093cec` |
| Superseded PR #292 | **CLOSED** |
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` |
| Candidate Static | `34303586782` — SUCCESS |
| Candidate Linux | `34303586778` — SUCCESS, complete scope |
| Candidate Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Canonical post-merge Static | `34333350711` — SUCCESS |
| Distribution artifact | ID `10086299397`, `abntexto-ufc-v3.0.0-distribution-34303586773` |
| Distribution artifact digest | `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Candidate acceptance evidence

| Gate | Result |
|---|---|
| Static contract | PASS |
| Complete Linux integration | PASS |
| Linux release check | PASS, 38/38 required checks |
| Reference PDF reproducibility | PASS; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`; 450652 bytes |
| Distribution checksums / archive integrity | PASS |
| Independent retained-artifact verification | PASS; no rebuild |

## Remaining publication sequence

| Order | Action | Gate |
|---:|---|---|
| 1 | Create `v3.0.0` tag and GitHub Release | canonical `main` + exact retained candidate-produced bytes only |
| 2 | Verify published GitHub assets | published SHA-256 values match accepted checksums |
| 3 | Run current CTAN `pkgcheck` | retained CTAN ZIP only |
| 4 | If actual CTAN submission is performed, preserve submission/acceptance evidence | no claim without explicit evidence |
| 5 | Record final publication verification and close Release | no unresolved release blocker |

## Current blockers

| Blocker | Exit condition |
|---|---|
| `v3.0.0` tag/GitHub Release not yet published and hash-verified | tag/release exists and exact asset hashes match accepted candidate |
| Final publication verification not yet synchronized | canonical state records the publication result |

PR #293 merge, PR #294 synchronization, candidate regression and retained-artifact verification are no longer blockers. PR #292 is closed and must not be resumed.

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without final publication verification even though the immutable **phase-end regression** is accepted.
