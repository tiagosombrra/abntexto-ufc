# V3.0.0 Release Readiness

Updated: 2026-09-08
Status: ACTIVE — IMMUTABLE CANDIDATE REGRESSION

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | accepted |
| Reference PDF Validation | CLOSED | 55/55 visual PASS |
| Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
| Final Certification | CLOSED | candidate `22f7ba845...`; complete certification accepted |
| Release | **ACTIVE** | immutable candidate published; Static/complete Linux/release check and artifact verification remain |

## Release branch facts

| Fact | Value |
|---|---|
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Release branch / PR | `release/v3-release` / #293 |
| Artifact-delivery checkpoint | `b55210acdb614fc3178e3ebf5b3a595bed8508c1` |
| Artifact-delivery Static / Linux | `34300561597` SUCCESS / `34300561605` SUCCESS; `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Acceptance sync | `6ab4768662aa51842cf745afbf846e89b6bd466a`; Static `34303128975` SUCCESS |
| Release candidate marker | present in current immutable candidate |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

## Candidate execution order

| Order | Action | Gate |
|---:|---|---|
| 1 | Run candidate Static contract | SUCCESS |
| 2 | Run candidate Linux integration | SUCCESS with `SCOPE=complete` |
| 3 | Run candidate Linux release check | SUCCESS; exact candidate checkout/provenance |
| 4 | Download/verify retained distribution artifact | four ZIPs + `SHA256SUMS`; checksums/integrity PASS |
| 5 | Record exact candidate SHA/run IDs/artifact ID | later documentation-only synchronization |
| 6 | Create `v3.0.0` tag/GitHub Release from accepted candidate and retained bytes | published hashes match candidate |
| 7 | Record final verification and close Release | no unresolved release blocker |

## Current blockers

| Blocker | Exit condition |
|---|---|
| Candidate regression not yet accepted | Static + complete Linux + Linux release check green on same SHA |
| Candidate artifact not yet independently verified | retained exact five-file artifact checked |
| Tag/GitHub Release not yet verified | published assets match candidate checksums |

No runtime/normative behavior is being changed in this candidate. Librarian item 33 remains fail-closed.

Every **material advance** updates operational documentation in the same work cycle. Release cannot close without this complete **phase-end regression**.
