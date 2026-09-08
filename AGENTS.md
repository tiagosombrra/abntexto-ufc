# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. identify actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md` and `docs/ROADMAP-V3.0.0.md`;
4. during **Final Certification**, also read `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and permanent/temporary certification workflow definitions;
5. reconcile Git facts, machine state, handoff, roadmap, release blockers and temporary-executor lifecycle before work.

Memory, prior chats, historical branches and old workflow names never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Final Certification** |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Scientific Article | CLOSED — `923d11ef...`; complete Linux + 5/5 visual PASS |
| Linux release baseline | ACCEPTED — `34168471371`; cleanup `0609f929...` Static/Linux green |
| Profile/engine matrix | ACCEPTED |
| Current batch | **Step 6 canonical-checkout runner correction** |
| First bounded failure | `21455c3344...` / `34172047786`: release 38/38 + Step 5 PASS, then Git ownership failure during epoch read |
| Second bounded failure | `247e31398...` / `34173496336`: release 38/38 + Step 5 PASS, then canonical-checkout failure during `git ls-files`; Static `34173496318` and Linux `34173496285` remained green |
| Second failure artifact | `10036808737`, SHA-256 `c56e1c651ce990ddd5a301c5cf60691b1081a06b7eebe66b27503e256e28e273` |
| Temporary executor | `.github/workflows/final-cert-bounded-matrix.yml` — transport only, active for corrected rerun; removal required before bounded acceptance |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 |

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — active
6. Release — queued

## Closure-scope freeze

Remaining certification scope is fixed to: literal-font/Unicode/embedding proof; explicit Scientific Article PDF/A proof; distribution/public-bundle integrity; issue #18 deterministic reference-PDF proof; one immutable Final Certification phase-end regression; then Release.

Do not create a new roadmap workstream merely because a validator exposes a defect. Classify the defect inside the existing acceptance predicate it violates. A new step/phase is allowed only if current repository authority proves none of the frozen predicates can represent the blocker.

## Current transport rule

Both bounded transports proved the permanent release suite at 38/38 and the Scientific Article PDF/A/embedding gate PASS. The first failed during Step 6 epoch derivation because Git rejected container ownership. The second progressed past that read and then failed when distribution tooling used `git ls-files` to establish the canonical tracked-file set.

The current correction is runner-scoped: temporary and permanent Linux release workflows register only the current mounted checkout as a container-local Git `safe.directory` before `make release-check`. This preserves the distribution predicate and avoids embedding runner ownership assumptions into the product runtime. Do not mark Steps 5-6 accepted until the corrected release transport is green, the temporary workflow is removed, and cleanup Static/Linux pass.

## Engineering rules

- Project-owned technical surfaces are English.
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

If a required fact cannot be established from current Git state, canonical state files, current evidence, or reviewed source material, record ambiguity and stop advancement. Uncertainty does not create a new roadmap item unless it blocks an existing frozen acceptance predicate.
