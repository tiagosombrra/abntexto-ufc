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
| Steps 1-6 | ACCEPTED |
| Step 7 core proof | **PASS** in run `34229431523` on `0040ed413df7bd9126ff1dcb34c23582bfd68403` |
| Step 7 digest | `cf00b4ba784d0e0cd774b080d9cb88cc23b19c4ecc17ace6dc6aa7fc17c5ac7f` from 2 clean builds |
| Step 7 validation | embedding/portable PDF/Unicode/PDF-A all PASS |
| Step 7 workflow result | reporting-only failure after proof; clean executor rerun required |
| Permanent gate | `make release-reference-reproducibility` is part of `make release-check` |
| Temporary executor | `.github/workflows/final-cert-step7-repro.yml` remains active only for the clean rerun; remove immediately after classification |
| Current batch | **Step 7 — repair executor summary, rerun, then cleanup** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — active
6. Release — queued

## Closure-scope freeze

Remaining certification scope is fixed to: Step 7 clean executor rerun and cleanup; issue #18 acceptance; one immutable Final Certification **phase-end regression**; then Release.

Do not create a new roadmap workstream merely because a validator or executor exposes a defect. Classify it inside the existing acceptance predicate.

## Step 7 deterministic-build boundary

The permanent release-reference reproducibility gate pins deterministic provenance time, performs two independent clean builds from one immutable tracked source state, requires exact PDF SHA-256 equality, and validates the deterministic artifact for font embedding, portable PDF structure, Unicode extraction and PDF/A-2b. It does not post-normalize PDF bytes or reuse one output twice.

Run `34229431523` proved these product predicates. The overall workflow failed only in a later reporting shell here-document while the proof and artifact upload were green. This is a temporary executor defect. Correct only the reporting surface, rerun it clean, then remove the workflow. Do not change the permanent gate predicates to address a reporting failure.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- Preserve accepted v3 public API and shared/article semantics unless a concrete regression or current authority requires change.
- Do not silently change normative IDs, values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only its encoded contract.
- Do not weaken tests merely to recover green CI.
- Temporary workflow lifecycle is atomic: create -> execute -> classify -> correct executor-only defects if needed -> rerun -> remove -> cleanup validation.
- Do not redistribute proprietary Microsoft fonts.
- Item 33 remains fail-closed and is not a hidden implementation task.
- Do not perform CTAN/external publication before **Release**.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification result/scope, phase/acceptance state, artifact provenance, reproducibility state or release readiness. Update relevant execution documents and handoff in the same work cycle; synchronize roadmap/machine state whenever those facts change.

## Mandatory phase-end regression

No phase closes until one immutable candidate SHA passes the complete **phase-end regression** and the result is recorded. Final Certification requires complete Linux plus the full applicable certification/release evidence matrix.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record ambiguity and stop advancement.
