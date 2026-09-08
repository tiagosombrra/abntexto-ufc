# V3.0.0 Release — Phase-end Regression

Updated: 2026-09-08
Status: ACTIVE — TRANSPORT PREPARATION

## Purpose

This document defines the immutable Release phase-end candidate and the exact evidence required before `v3.0.0` tag/GitHub Release/publication actions can be finalized.

## Candidate transport

Release uses the tracked marker `release/v3-release-candidate.json` only to make candidate intent explicit to permanent CI orchestration. The marker does not change product runtime or normative semantics.

When the marker is introduced or changed on PR #293:

- `tests/integration_suites.py` must infer `complete`;
- `Linux integration` must execute the complete PR suite;
- `Linux release check` must be triggered on the PR and execute `make release-check`;
- `Static contract` must remain green.

The historical `release/final-certification-candidate.json` remains a Final Certification provenance mechanism and must not be reused as the Release marker.

## Immutable candidate rule

The Release candidate is the first commit that contains the completed release artifacts/checklist state plus the Release candidate marker. After CI starts, that commit is immutable. CI-result documentation is recorded in a later commit and never rewrites the accepted candidate.

## Required phase-end gates

| Gate | Required result |
|---|---|
| Static contract | SUCCESS |
| Linux integration | SUCCESS with `SCOPE=complete` and no failed/skipped required check |
| Linux release check | SUCCESS with complete release contract |
| Distribution artifacts/checksums | reproducible, integrity PASS, exact v3.0.0 artifact set |
| Deterministic reference PDF | permanent reproducibility gate PASS |
| PDF/A / Unicode / embedding | accepted Final Certification proof remains applicable or is re-established if affected |
| Librarian review | remains `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`; item 33 stays fail-closed |
| Temporary executors/assets | absent from candidate/public bundles |

A workflow conclusion of `success` does not satisfy the gate if required heavy scope was skipped.

## Publication boundary

Tag `v3.0.0`, GitHub Release assets and any external publication occur only after the immutable Release candidate satisfies every required gate above. Published assets/checksums are verified afterwards before Release closes.

Actual CTAN submission remains an explicit action and must not be reported as acceptance without submission/acceptance evidence.

## Regression discipline

Every material Release advance updates roadmap, handoff, readiness and machine state in the same work cycle. Targeted checks are useful intermediate evidence but never replace this phase-end regression.
