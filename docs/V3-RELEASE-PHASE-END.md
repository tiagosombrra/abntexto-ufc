# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-08
Status: ACTIVE — IMMUTABLE CANDIDATE PUBLISHED / REGRESSION PENDING

## Purpose

This document defines the immutable Release phase-end candidate and the exact evidence required before `v3.0.0` tag/GitHub Release/publication actions can be finalized.

## Accepted preparation

| Preparation | Checkpoint | Evidence |
|---|---|---|
| Release candidate transport | `6a257f35b65266a1120826b816404116082b1e5c` | Static `34265429699`; Linux `34265429551`, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Artifact-delivery tooling | `b55210acdb614fc3178e3ebf5b3a595bed8508c1` | Static `34300561597`; Linux `34300561605`, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Acceptance control sync | `6ab4768662aa51842cf745afbf846e89b6bd466a` | Static `34303128975`; Linux documentation-only skip |

## Immutable candidate

The current commit contains the tracked Release marker `release/v3-release-candidate.json` and the synchronized control-plane state. This commit is the immutable Release phase-end candidate. Its exact Git SHA is obtained after commit creation and is not self-recorded by amending the candidate.

After CI starts, the candidate is immutable. CI-result documentation is recorded only in a later commit.

The historical `release/final-certification-candidate.json` remains a Final Certification provenance mechanism and is not reused.

## Required phase-end gates

| Gate | Required result |
|---|---|
| Static contract | SUCCESS |
| Linux integration | SUCCESS with `SCOPE=complete` and no failed/skipped required check |
| Linux release check | SUCCESS with complete release contract |
| Distribution artifacts/checksums | exact five-file set retained from candidate; reproducibility and integrity PASS |
| Deterministic reference PDF | permanent reproducibility gate PASS |
| PDF/A / Unicode / embedding | accepted Final Certification proof remains applicable or is re-established if affected |
| Librarian review | remains `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`; item 33 stays fail-closed |
| Temporary executors/assets | absent from candidate/public bundles |

The permanent `Linux release check` must retain exactly:

- `abntexto-ufc-3.0.0.zip`
- `abntexto-ufc-ctan-3.0.0.zip`
- `abntexto-ufc-template-3.0.0.zip`
- `abntexto-ufc-overleaf-3.0.0.zip`
- `SHA256SUMS`

A workflow conclusion of `success` does not satisfy the gate if required heavy scope was skipped.

## Artifact provenance rule

The GitHub Release must use the exact candidate-produced bytes retained by the candidate's `Linux release check`. Rebuilding archives after candidate acceptance is not permitted release evidence.

## Publication boundary

Tag `v3.0.0`, GitHub Release assets and any external publication occur only after the immutable Release candidate satisfies every required gate above. Published assets/checksums are verified afterwards before Release closes.

Actual CTAN submission remains an explicit action and must not be reported as acceptance without submission/acceptance evidence.

## Regression discipline

Every **material advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Targeted checks never replace this **phase-end regression**.
