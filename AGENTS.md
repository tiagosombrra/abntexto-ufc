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
| Step 7 clean proof | **PASS** — run `34231038578` on `9ba5905d2325b3cc0cd0b9cd3bef9a2fecb7b522` |
| Step 7 digest | `1c92535fcab2d209396279c0b200d5f21fa989b9a2c2adf8a77f389ffe432dbf` from 2 clean builds |
| Step 7 validation | embedding/portable PDF/Unicode/PDF-A all PASS |
| Permanent gate | `make release-reference-reproducibility` remains part of `make release-check` |
| Temporary executor | removed in current cleanup candidate; do not recreate unless a new bounded proof is explicitly required |
| Current batch | **Step 7 — cleanup validation** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — active
6. Release — queued

## Closure-scope freeze

Remaining certification scope is fixed to: Step 7 cleanup validation and issue #18 acceptance; one immutable Final Certification **phase-end regression**; then Release.

Do not create a new roadmap workstream merely because a validator exposes a defect. Classify it inside the existing acceptance predicate.

## Step 7 deterministic-build boundary

The permanent release-reference reproducibility gate pins deterministic provenance time, performs two independent clean builds from one immutable tracked source state, requires exact PDF SHA-256 equality, and validates the deterministic artifact for font embedding, portable PDF structure, Unicode extraction and PDF/A-2b. It does not post-normalize PDF bytes or reuse one output twice.

Run `34231038578` cleanly proved these predicates. The temporary proof workflow has served its bounded purpose and is removed. Step 7 remains open only until the cleanup candidate passes Static/Linux.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- Preserve accepted v3 public API and shared/article semantics unless a concrete regression or current authority requires change.
- Do not silently change normative IDs, values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only its encoded contract.
- Do not weaken tests merely to recover green CI.
- Temporary workflow lifecycle is atomic: create -> execute -> classify -> remove -> cleanup validation.
- Do not redistribute proprietary Microsoft fonts.
- Item 33 remains fail-closed and is not a hidden implementation task.
- Do not perform CTAN/external publication before **Release**.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification result/scope, phase/acceptance state, artifact provenance, reproducibility state or release readiness. Update relevant execution documents and handoff in the same work cycle; synchronize roadmap/machine state whenever those facts change.

## Mandatory phase-end regression

No phase closes until one immutable candidate SHA passes the complete **phase-end regression** and the result is recorded. Final Certification requires complete Linux plus the full applicable certification/release evidence matrix.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record ambiguity and stop advancement.
