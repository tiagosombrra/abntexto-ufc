# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-08

## Current status

**Release is ACTIVE on PR #293. The immutable Release phase-end candidate marker is published; complete regression is pending.**

| Phase | Status | Exit requirement |
|---|---|---|
| Regression Audit | CLOSED | accepted |
| Core Corrections | CLOSED | accepted phase-end regression |
| Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
| Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |
| Release | **ACTIVE — IMMUTABLE CANDIDATE REGRESSION** | candidate passes Static + complete Linux + release check; exact certified assets published and verified |

## Release facts

| Predicate | Current result |
|---|---|
| Merged `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch / PR | `release/v3-release` / #293 |
| Artifact-delivery implementation | `b55210ac...` — **ACCEPTED** |
| Artifact-delivery Static | `34300561597` — SUCCESS |
| Artifact-delivery Linux | `34300561605` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Acceptance sync | `6ab47686...`; Static `34303128975` SUCCESS; Linux docs-only skip |
| Release candidate marker | **PRESENT in current immutable candidate** |
| Librarian matrix | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Release plan

| Step | State | Gate |
|---:|---|---|
| Final Certification → Release transition | DONE | PR #289 merged |
| Release branch + PR synchronization | DONE | PR #293 open |
| Candidate transport + artifact retention tooling | DONE | bounded Static + complete Linux PASS |
| Publish immutable Release phase-end candidate marker | **DONE IN CURRENT CANDIDATE** | `release/v3-release-candidate.json` present |
| Release phase-end regression | **RUNNING / PENDING RESULTS** | Static + `SCOPE=complete` Linux + Linux release check |
| Verify candidate artifacts/checksums | QUEUED | four ZIPs + `SHA256SUMS`, exact candidate provenance |
| Record candidate acceptance | QUEUED | candidate SHA + runs + artifact ID/checksums in later docs-only commit |
| Tag/GitHub Release/publication | QUEUED | accepted candidate; published assets match certified hashes |
| Release closeout | QUEUED | no blocker + final verification recorded |

## Candidate policy

The current commit contains `release/v3-release-candidate.json`, the Release-specific force-complete and PR release-check marker. The commit is immutable after CI starts. The exact candidate SHA is recorded after CI in the later acceptance synchronization; do not amend this candidate to insert its own SHA.

The GitHub Release must use the exact retained candidate-produced bytes. No archive rebuild is allowed after candidate acceptance.

## Frozen remaining scope

Only **Release** remains. Do not create another roadmap phase. Librarian item 33 remains an explicit authority gap, not an untracked Release implementation task.

## Operating discipline

Every **material advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Release ends with a complete **phase-end regression** on one immutable SHA; intermediate green checks do not substitute for it.
