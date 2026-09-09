# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-09

## Current status

**Release is ACTIVE. Release implementation and certification are accepted; only publication closeout remains.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | immutable certification candidate and heavy matrix accepted |
| Release | **ACTIVE — PUBLICATION CLOSEOUT** | publish exact retained assets; verify tag/GitHub Release; record any explicit CTAN action; final closeout verification |

## Release facts

| Predicate | Current result |
|---|---|
| Canonical branch | `main`; resolve current HEAD dynamically from Git |
| Release integration PR #293 | **MERGED** by squash as `add52f2183f18d6cea3e9477f2a45416a13cfc36` |
| Publication-closeout PR #294 | **MERGED** as `c39af06e236b6b61fcf6d11bc383ac5752093cec` |
| Continuation synchronization PR #295 | **MERGED**; canonical post-merge Static `34335044265` PASS |
| Release work branch | `release/v3-release`, aligned to canonical `main` after PR #295 |
| Superseded PR #292 | **CLOSED**; historical evidence only |
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **ACCEPTED** |
| Candidate Static | `34303586782` — SUCCESS |
| Candidate Linux | `34303586778` — SUCCESS, complete scope |
| Candidate Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Reproducible reference PDF | PASS; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`; 450652 bytes |
| Retained distribution artifact | ID `10086299397`; digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |
| Librarian matrix | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Release plan

| Step | State | Gate |
|---:|---|---|
| Final Certification → Release transition | DONE | PR #289 merged |
| Release branch + PR #293 | DONE | squash merge |
| Candidate transport + artifact retention tooling | DONE | bounded Static + complete Linux PASS |
| Release phase-end regression | DONE / ACCEPTED | Static + complete Linux + release check |
| Verify candidate artifacts/checksums | DONE / ACCEPTED | retained candidate artifact independently verified |
| Record candidate acceptance | DONE | merged through PR #293 |
| Record publication-closeout control state | DONE | PR #294 merged |
| Create durable continuation handoff | DONE | PR #295 merged; Static PASS |
| Close superseded Release PR | DONE | PR #292 closed as historical evidence |
| Tag/GitHub Release | **NEXT** | exact retained candidate-produced bytes; no rebuild |
| Verify published assets | QUEUED | hashes match accepted candidate checksums |
| CTAN `pkgcheck` / optional submission | QUEUED / EXTERNAL | explicit evidence only |
| Release closeout | QUEUED | no unresolved publication blocker + final verification recorded |

## Candidate and publication policy

The accepted candidate `75ead435...` remains immutable. Later merges and documentation synchronization do not replace it and do not authorize rebuilding publication archives.

## Frozen remaining scope

Only **Release publication closeout** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked Release implementation task.

## Continuation

Start from the latest `origin/main` and read `docs/V3-CONTINUATION.md`. Do not resume superseded PR #292 or historical task branches. Do not treat any hardcoded current-main SHA as a continuing invariant.

## Operating discipline

Every **material advance** must update roadmap, handoff, readiness and machine state in the same work cycle. Release still requires final publication verification before closure even though its immutable **phase-end regression** candidate is accepted.
