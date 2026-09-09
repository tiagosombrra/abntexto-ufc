# V3.0.0 Release Readiness

Updated: 2026-09-09
Status: ACTIVE — MERGED / PUBLICATION PENDING

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | immutable certification candidate and heavy matrix accepted |
| Release | **ACTIVE** | candidate accepted and PR #293 merged; tag/GitHub Release/post-publication verification remain |

## Canonical Release facts

| Fact | Value |
|---|---|
| Canonical `main` | `add52f2183f18d6cea3e9477f2a45416a13cfc36` |
| Release PR #293 | **MERGED** as squash commit `add52f2183f18d6cea3e9477f2a45416a13cfc36` |
| Publication-closeout work branch | `release/v3-release`, reset to merged `main` |
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` |
| Candidate Static | `34303586782` — SUCCESS |
| Candidate Linux | `34303586778` — SUCCESS, complete scope |
| Candidate Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Distribution artifact | ID `10086299397`, `abntexto-ufc-v3.0.0-distribution-34303586773` |
| Distribution artifact digest | `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Candidate acceptance evidence

| Gate | Result |
|---|---|
| Static contract | PASS |
| Complete Linux integration | PASS |
| Linux release check | PASS, 38/38 required checks |
| Reference PDF reproducibility | PASS; 2 builds; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`; 450652 bytes |
| Distribution checksums in CI | PASS |
| Distribution archive integrity in CI | PASS |
| Independent artifact download digest | matches GitHub artifact digest |
| Independent exact file-set verification | PASS; four ZIPs + `SHA256SUMS` only |
| Independent `sha256sum -c SHA256SUMS` | PASS for all four ZIPs |
| Independent ZIP integrity | PASS for all four ZIPs |

## Accepted asset checksums

| Asset | SHA-256 |
|---|---|
| `abntexto-ufc-3.0.0.zip` | `c38fe32bc6b51ff3b7723b4ef118574d130cea97f29d443c1fc4d08b24e0b207` |
| `abntexto-ufc-ctan-3.0.0.zip` | `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60` |
| `abntexto-ufc-overleaf-3.0.0.zip` | `6c099a8510a3deb267da1b383df88a8fce310ba41ae5d58a2a4b80c26100d41b` |
| `abntexto-ufc-template-3.0.0.zip` | `4d8ebea5e97317823d05202dfa52c8f40b2b09dd993e8379c220eedf64aef791` |

## Remaining publication sequence

| Order | Action | Gate |
|---:|---|---|
| 1 | Synchronize PR #293 merge facts in repository docs | Static contract on post-merge documentation sync |
| 2 | Create `v3.0.0` tag and GitHub Release | canonical merged state + exact candidate-produced bytes only |
| 3 | Verify published GitHub assets | published SHA-256 values match accepted checksums |
| 4 | Run current CTAN `pkgcheck` and, if actual submission is performed, preserve submission/acceptance evidence | no claim without receipt/evidence |
| 5 | Record final publication verification and close Release | no unresolved release blocker |

## Current blockers

| Blocker | Exit condition |
|---|---|
| `v3.0.0` tag/GitHub Release not yet published and hash-verified | tag/release exists and exact asset hashes match accepted candidate |
| Final publication verification not yet synchronized | canonical state records publication result |
| External CTAN state not yet recorded | run current `pkgcheck`; record actual upload/acceptance only if performed |

Candidate regression, retained-artifact verification and PR #293 merge are no longer blockers. No runtime/normative behavior is being changed in this documentation synchronization. Librarian item 33 remains fail-closed.

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without final publication verification even though the immutable **phase-end regression** is accepted.
