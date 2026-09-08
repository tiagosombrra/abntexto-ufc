# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. identify actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md` and `docs/ROADMAP-V3.0.0.md`;
4. during **Final Certification**, also read `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, and `docs/UFC-LIBRARIAN-REVIEW.md`;
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
| Step 7 deterministic proof | ACCEPTED — run `34231038578` |
| Step 7 cleanup | ACCEPTED — `34e6bf8299e582803d1726e8dd699271c356fda5`; Static `34232017286`; complete Linux `34232017359`, `PASS=36 FAIL=0 SKIP=0` |
| Issue #18 | CLOSED — deterministic release reference PDF accepted |
| Permanent gate | `make release-reference-reproducibility` remains inside `make release-check` |
| Temporary executor | absent; must remain absent |
| Current batch | **Step 8 — Final Certification phase-end regression preparation** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — active
6. Release — queued

## Closure-scope freeze

Remaining certification scope is fixed to one immutable Final Certification **phase-end regression**, followed by Release. Do not create a new roadmap workstream merely because a validator exposes a defect; classify it inside the existing acceptance predicate.

## Step 7 accepted boundary

The permanent release-reference reproducibility gate pins deterministic provenance time, performs two independent clean builds from one immutable tracked source state, requires exact PDF SHA-256 equality, and validates the deterministic artifact for font embedding, portable PDF structure, Unicode extraction and PDF/A-2b. Run `34231038578` proved the product predicate. Cleanup checkpoint `34e6bf8...` removed the temporary executor and passed Static plus complete Linux, so Step 7 and issue #18 are closed.

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

No phase closes until one immutable candidate SHA passes the complete **phase-end regression** and the result is recorded. Final Certification requires Static, complete Linux and the full applicable release/certification matrix on the accepted candidate. The machine sentinel remains `phase_end_regression.candidate = one-immutable-sha`; the real SHA is recorded only after the immutable commit exists.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record ambiguity and stop advancement.
