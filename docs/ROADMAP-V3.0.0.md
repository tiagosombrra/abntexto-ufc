# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-09

## Current status

**Release is ACTIVE on PR #293. The immutable Release phase-end regression is accepted; publication and post-publication verification remain.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | immutable certification candidate and heavy matrix accepted |
| Release | **ACTIVE — PUBLICATION CLOSEOUT** | merge accepted Release work; publish exact retained assets; verify tag/GitHub Release and any explicit external publication; final closeout verification |

## Release facts

| Predicate | Current result |
|---|---|
| Canonical `main` before Release merge | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch / PR | `release/v3-release` / #293 |
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **ACCEPTED** |
| Candidate Static | `34303586782` — SUCCESS |
| Candidate Linux | `34303586778` — SUCCESS, complete scope |
| Candidate Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Reproducible reference PDF | PASS; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`; 450652 bytes |
| Retained distribution artifact | ID `10086299397`; digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |
| Independent retained-artifact verification | exact five files + `SHA256SUMS` PASS + four ZIP integrity checks PASS |
| Librarian matrix | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Release plan

| Step | State | Gate |
|---:|---|---|
| Final Certification → Release transition | DONE | PR #289 merged |
| Release branch + PR synchronization | DONE | PR #293 open |
| Candidate transport + artifact retention tooling | DONE | bounded Static + complete Linux PASS |
| Publish immutable Release phase-end candidate marker | DONE | `release/v3-release-candidate.json` present in `75ead435...` |
| Release phase-end regression | **DONE / ACCEPTED** | Static `34303586782`; complete Linux `34303586778`; release check `34303586773` |
| Verify candidate artifacts/checksums | **DONE / ACCEPTED** | artifact `10086299397`; exact candidate provenance; SHA256SUMS and archive integrity PASS |
| Record candidate acceptance | **ACTIVE — THIS DOCUMENTATION CYCLE** | candidate SHA + runs + artifact identity/checksums synchronized |
| Merge PR #293 | QUEUED | post-acceptance documentation Static remains green |
| Tag/GitHub Release | QUEUED | use exact retained candidate-produced bytes; no rebuild |
| Verify published assets | QUEUED | hashes match accepted candidate checksums |
| CTAN publication step | QUEUED / EXTERNAL | current `pkgcheck`; explicit upload only with receipt/evidence |
| Release closeout | QUEUED | no unresolved publication blocker + final verification recorded |

## Accepted publication checksums

| Asset | SHA-256 |
|---|---|
| `abntexto-ufc-3.0.0.zip` | `c38fe32bc6b51ff3b7723b4ef118574d130cea97f29d443c1fc4d08b24e0b207` |
| `abntexto-ufc-ctan-3.0.0.zip` | `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60` |
| `abntexto-ufc-overleaf-3.0.0.zip` | `6c099a8510a3deb267da1b383df88a8fce310ba41ae5d58a2a4b80c26100d41b` |
| `abntexto-ufc-template-3.0.0.zip` | `4d8ebea5e97317823d05202dfa52c8f40b2b09dd993e8379c220eedf64aef791` |

## Candidate policy

The accepted candidate `75ead435...` remains immutable. The post-CI documentation commit does not replace the candidate and does not authorize rebuilding release archives. The GitHub Release must use the exact retained bytes from Linux release check `34303586773`.

## Frozen remaining scope

Only **Release** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked Release implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Release still requires final publication verification before closure even though its immutable **phase-end regression** candidate is now accepted.
