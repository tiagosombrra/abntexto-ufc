# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. During **Scientific Article**, also read `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `standards/coverage-rules-article.json`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-RELEASE-READINESS.md`, and `docs/ENGINEERING-LANGUAGE.md`.
6. Compare Git facts, machine state, handoff, roadmap and the active phase documents.
7. If phase, checkpoint, acceptance state, article authority, proof state, artifact provenance, integration-scope state, release-blocker state, or temporary-artifact state disagrees, reconcile the control plane before feature work.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Scientific Article**.
- `main` is current at merge `e6833ed5cf07aaf1021c690260cecfacec1a119a`; PR #285 is merged.
- Active task branch: `ci/scoped-linux-integration`, created from current `main` only to land readable bounded Linux orchestration.
- Core Corrections: CLOSED — candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Reference PDF Validation: CLOSED — candidate `b64074c64941895f97fbe0f795ce826c798d17ce`, Static `33985595790`, Linux `33985595798`, canonical 55/55 visual PASS.
- Librarian review: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**; item 33 remains fail-closed.
- Scientific Article Step 1: ACCEPTED — implementation `b46ba2051f8c9c712a7b5d25748b81baa52b920a`, synchronized checkpoint `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`, Static `34001350884`, Linux `34001350953`.
- Current material advance: **Scoped Linux integration orchestration**. No Step 2 article runtime is permitted on this infrastructure branch.
- After orchestration merges, create `feat/v3-scientific-article` from updated `main` and continue with the Required article front block.
- Issue #18 remains a v3.0.0 release blocker owned by Final Certification/Release.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active; Step 1 accepted; orchestration stabilization in progress
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers. GitHub issues/PRs and immutable SHAs provide traceability.

## Linux integration scopes

`docs/LINUX-INTEGRATION-SCOPES.md` is the orchestration contract.

- `auto` infers the narrowest safe suite from the changed surface.
- Documentation-only changes skip heavy Linux integration.
- Known bounded domains may use named suites.
- Multiple known domains run the union of their checks without duplicates.
- Shared/core, standards/integration infrastructure and unknown technical paths fail closed to `complete`.
- Manual `auto` fails closed to `complete`.
- `article` must include executable article evidence plus the article/source contract.
- Scoped runs are intermediate evidence only. Every phase-end regression requires `complete` Linux on one immutable candidate.

## Scientific Article boundaries

- One canonical `scientific-article` profile; no compatibility aliases.
- Reuse shared citation, bibliography, section, summary and object infrastructure rather than fork it.
- Preserve all 18 article rule IDs, authority and modality unless new current source evidence explicitly changes the source contract.
- Keep required, optional, recommended and conditional semantics distinct.
- Shared mechanism reuse and profile selection do not count as rule proof.
- Add article-specific positive evidence before proof promotion and controlled negative evidence where safe.
- Journal-specific instructions remain a conditional applicability boundary.
- Preserve the validated non-article foundation and canonical academic-work PDF presentation.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- Preserve the closed V3 public API except for bounded new article API explicitly required by the Scientific Article contract.
- Do not silently change normative rule IDs, expected values, tolerances, locators, applicability, source precedence, or proof-state semantics.
- A green test proves only the contract encoded by that test.
- Reviewer comments are evidence, not automatic normative authority.
- Presentation requirements require canonical PDF evidence in addition to source-level checks.
- Do not weaken tests merely to recover green CI.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before checkpoint closeout.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Heavy literal-font/PDF-A/distribution checks belong to Final Certification unless a bounded change directly requires them.
- Do not redistribute proprietary Microsoft fonts.
- CTAN submission remains blocked until **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, canonical content, article proof state, integration-scope policy, phase/acceptance status, artifact provenance, release-blocker state, branch/checkpoint facts, or certification state.

For every material advance, update the relevant execution document and canonical handoff in the same work cycle; synchronize roadmap and machine state whenever those facts change.

## Mandatory phase-end regression

No phase transitions to `CLOSED`, and no subsequent phase becomes `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the results are recorded. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel; the concrete SHA belongs in evidence fields after the candidate exists.

## Branch governance and fail-closed rule

The steady state is `main` plus one short-lived active task branch. PR #285 is historical and merged. `plan/v3-regression-reset` is provenance only and must not receive current work. The active infrastructure branch is `ci/scoped-linux-integration`; after it merges, current article work moves to `feat/v3-scientific-article` created from the then-current `main`.

If a required fact cannot be established from Git, canonical state files, current normative evidence, reviewed source material, or a provenance-bound canonical artifact, record the ambiguity and stop advancement.