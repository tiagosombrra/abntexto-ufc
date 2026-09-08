# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. identify actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md` and `docs/ROADMAP-V3.0.0.md`;
4. during **Final Certification**, also read `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, and `docs/UFC-LIBRARIAN-REVIEW.md`;
5. reconcile Git facts, machine state, handoff, roadmap, release blockers and temporary-executor lifecycle before work.

Memory, prior chats and historical branches never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Final Certification** |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Scientific Article | CLOSED — `923d11ef...`; complete Linux + 5/5 visual PASS |
| Steps 1-3 | ACCEPTED |
| Steps 5-6 | ACCEPTED — cleanup `7307164...`; Static `34208318971`; Linux `34208318754` |
| Steps 5-6 acceptance sync | `237cb53b65c91052a469ab67991ea78e71ade283`; Static `34218086750`; Linux `34218086734` |
| Current batch | **Step 4 — fresh current-candidate literal-font/Unicode/embedding proof** |
| Temporary executor | `.github/workflows/final-cert-literal-fonts.yml` active only for bounded Step 4 evidence |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 deterministic reference PDF |

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — active
6. Release — queued

## Closure-scope freeze

Remaining certification scope is fixed to: fresh current-candidate literal Times New Roman/Arial identity, Unicode extraction and embedding proof; issue #18 deterministic reference-PDF proof; one immutable Final Certification **phase-end regression**; then Release.

Do not create a new roadmap workstream merely because a validator exposes a defect. Classify it inside the existing acceptance predicate.

## Temporary workflow lifecycle

Steps 5-6 proof transport is closed. Step 4 uses `.github/workflows/final-cert-literal-fonts.yml` as a bounded proof-only executor. It must be removed after evidence capture, and the cleanup checkpoint must pass Static and Linux before Step 4 becomes ACCEPTED. No bounded-only orchestration is promoted into permanent product runtime.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- Preserve accepted v3 public API and shared/article semantics unless a concrete regression or current authority requires change.
- Do not silently change normative IDs, values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only its encoded contract.
- Do not weaken tests merely to recover green CI.
- Temporary workflow lifecycle is atomic: create -> execute -> validate -> remove -> cleanup validation.
- Do not redistribute proprietary Microsoft fonts.
- Item 33 remains fail-closed and is not a hidden implementation task.
- Do not perform CTAN/external publication before **Release**.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification result/scope, phase/acceptance state, artifact provenance, reproducibility state or release readiness. Update relevant execution documents and handoff in the same work cycle; synchronize roadmap/machine state whenever those facts change.

## Mandatory phase-end regression

No phase closes until one immutable candidate SHA passes the complete **phase-end regression** and the result is recorded. Final Certification requires complete Linux plus the full applicable certification/release evidence matrix.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record ambiguity and stop advancement.
