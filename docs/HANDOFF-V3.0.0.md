# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch / PR | `release/v3-release` / #293 |
| Active phase | **Release** |
| Artifact-delivery implementation | **ACCEPTED** on `b55210acdb614fc3178e3ebf5b3a595bed8508c1` |
| Artifact-delivery Static / Linux | `34300561597` SUCCESS / `34300561605` SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Acceptance control sync | `6ab4768662aa51842cf745afbf846e89b6bd466a`; Static `34303128975` SUCCESS; Linux docs-only skip |
| Current batch | **Release immutable phase-end candidate — marker published; regression pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-RELEASE-PHASE-END.md`, `docs/CTAN-RELEASE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Candidate state

The tracked marker `release/v3-release-candidate.json` is now part of the immutable Release candidate commit. The candidate SHA is deliberately not self-recorded inside that commit; after Git creates the commit, its exact SHA is the evidence identity and is recorded only in the post-CI synchronization commit.

The candidate is not amended after CI starts.

## Required Release phase-end regression

| Gate | Required result |
|---|---|
| Static contract | SUCCESS on candidate SHA |
| Linux integration | SUCCESS with `SCOPE=complete` and no required skip/failure |
| Linux release check | SUCCESS on candidate SHA |
| Retained distribution artifact | four ZIPs + `SHA256SUMS`, exact file set |
| Checksum/integrity | PASS on candidate-produced bytes |
| Deterministic reference PDF | permanent gate remains PASS |
| Final Certification applicability | remains valid or affected proof re-established |
| Librarian review | remains 33/0/0/1; item 33 fail-closed |

## Next actions

| Order | Action |
|---:|---|
| 1 | Wait for Static, complete Linux and Linux release check on this immutable candidate. |
| 2 | Classify any failure before changing code or tests. |
| 3 | If all gates pass, download and verify the retained candidate artifact. |
| 4 | Record candidate SHA, workflow run IDs, artifact ID and checksum evidence in a later documentation-only commit. |
| 5 | Only after phase-end acceptance create/verify `v3.0.0` tag and GitHub Release with the exact candidate-produced bytes. |
| 6 | Verify published hashes and only then close Release. |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

Do not rebuild publication ZIPs after candidate acceptance, do not weaken tests, do not redistribute proprietary fonts, and do not claim CTAN acceptance without explicit submission/acceptance evidence.
