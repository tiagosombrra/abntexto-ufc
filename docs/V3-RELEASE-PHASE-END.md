# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-08
Status: ACTIVE — ARTIFACT DELIVERY / CANDIDATE PREPARATION

## Purpose

This document defines the immutable Release phase-end candidate and the exact evidence required before `v3.0.0` tag/GitHub Release/publication actions can be finalized.

## Accepted candidate transport

Release uses the tracked marker `release/v3-release-candidate.json` only to make candidate intent explicit to permanent CI orchestration. The marker does not change product runtime or normative semantics.

Transport preparation was accepted on `6a257f35b65266a1120826b816404116082b1e5c`:

| Gate | Result |
|---|---|
| Static contract | `34265429699` — SUCCESS |
| Linux integration | `34265429551` — SUCCESS |
| Linux scope | `complete` |
| Linux summary | `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Release marker scope selector | PASS |
| Release-check PR trigger contract | PASS |

The historical `release/final-certification-candidate.json` remains a Final Certification provenance mechanism and must not be reused as the Release marker.

## Immutable candidate and artifact rule

The Release candidate is the first commit that contains the completed release tooling/checklist state plus the Release candidate marker. After CI starts, that commit is immutable. CI-result documentation is recorded in a later commit and never rewrites the accepted candidate.

The permanent `Linux release check` must generate and retain the final publication bytes from that exact candidate. It already executes `make release-check`; its release-candidate run must also expose `dist/` as a downloadable Actions artifact containing exactly:

- `abntexto-ufc-3.0.0.zip`
- `abntexto-ufc-ctan-3.0.0.zip`
- `abntexto-ufc-template-3.0.0.zip`
- `abntexto-ufc-overleaf-3.0.0.zip`
- `SHA256SUMS`

Pre-candidate builds are diagnostic only. The GitHub Release must use the exact candidate-produced bytes; rebuilding archives after acceptance is not permitted release evidence.

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

A workflow conclusion of `success` does not satisfy the gate if required heavy scope was skipped.

## Publication boundary

Tag `v3.0.0`, GitHub Release assets and any external publication occur only after the immutable Release candidate satisfies every required gate above. Published assets/checksums are verified afterwards before Release closes.

Actual CTAN submission remains an explicit action and must not be reported as acceptance without submission/acceptance evidence.

## Regression discipline

Every **material Release advance** updates roadmap, handoff, readiness and machine state in the same work cycle. Targeted checks are useful intermediate evidence but never replace this **phase-end regression**.
