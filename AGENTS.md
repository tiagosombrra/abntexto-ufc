# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. During **Scientific Article**, also read `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `standards/coverage-rules-article.json`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/V3-RELEASE-READINESS.md`, and `docs/ENGINEERING-LANGUAGE.md`.
6. Compare Git facts, machine state, handoff, roadmap and active phase documents.
7. If phase, checkpoint, acceptance state, article authority, proof state, integration-scope state, release-blocker state or temporary-artifact state disagrees, reconcile the control plane before feature work.

Memory, prior chats, historical branch names, old pull requests and workflow names never override current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Scientific Article**.
- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active task branch: `feat/v3-scientific-article`, PR #286.
- Step 1: ACCEPTED at `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`.
- Step 2: ACCEPTED at `0947669c2c096dca93991e042d8ae245754688ba`; Static `34026680871`, Linux `34026680882`.
- Step 3: ACCEPTED at `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba`; Static `34031144114`, Linux `34031144269`.
- Step 3 acceptance confirms the missing-incremental-SHA fallback, article/profile scoped execution, optional foreign-element scenarios under both engines, and the six-profile non-article compatibility boundary.
- Current batch: **Step 4 — textual structure and body typography**.
- Step 4 owns required article structure plus the accepted 12 pt, justified, 2 cm first-line indent, single-spaced body contract. It has not been implemented or accepted yet.
- README usability rewrite checkpoint `3e3ece5a3607303dd31aee35c67ce4140fb90d94` was rejected by Static `34053874788` because the user guide reintroduced unclassified legacy class identity while explaining the stable release. The correction keeps stable-release onboarding but removes the retired identity from the active tree; the canonical-identity gate is not weakened.
- Shared librarian-review state remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**; item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active, Step 4
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## README ownership

`README.md` is the user-facing entry point for people who want to use the template. Keep it focused on choosing a released version, downloading it, configuring a document, compiling it, understanding the template layout, and solving common user problems.

Do not turn `README.md` into execution history. Detailed phase status, workflow run IDs, implementation SHAs, issue chronology, regression failures, normative disputes and control-plane mechanics belong in `docs/`, GitHub issues/pull requests, Actions and `release/v3-roadmap.json`. A short unreleased-version notice and links to developer documents are allowed when they help users avoid an unstable branch.

The active README must also respect the canonical-identity contract. Stable-release instructions may identify the supported release, bundle names and historical file layout, but must not casually reintroduce a retired class identity into the active V3 tree. If an exact legacy identity becomes indispensable to user documentation, classify it narrowly in the identity contract rather than globally exempting the README.

## Linux integration scopes

`docs/LINUX-INTEGRATION-SCOPES.md` is the orchestration contract.

- PR `auto` normally uses the incremental pushed range on `synchronize` and the full PR diff on opened/reopened/ready events.
- If the synchronize `before` or `after` commit is unavailable locally, scope selection must not crash; it falls back to the full PR diff and therefore remains fail-closed.
- Documentation-only changes skip heavy Linux integration.
- Multiple known domains run a deduplicated union.
- Workflow/runner orchestration accompanying known domain changes does not force `complete`.
- Unknown technical paths and shared/core/standards surfaces fail closed to `complete`.
- Article gates are first-class checks; `profiles` contains exactly six non-article profiles and excludes `scientific-article`.
- The `article` scope currently includes `validator-source`, `scientific-article-profile`, `scientific-article-front-block` and `scientific-article-foreign-elements`.
- Step 4 must add its article-specific executable gate to `article` in the same material advance that introduces the gate.
- Runner modules must remain importable by direct execution and repository traceability loaders.
- Scoped runs are intermediate evidence only. Phase-end regression always uses `complete`.

## Scientific Article rules

- One canonical type: `scientific-article`; no aliases.
- Preserve the retained 18-rule article source contract.
- Keep required, optional, recommended and required-when-applicable semantics distinct.
- Reuse shared bibliography, citation, section, object and summary mechanisms rather than fork them.
- Shared implementation is not article proof.
- Foreign title and foreign summary are independently optional; Step 3 is accepted and regression-protected.
- Do not repurpose `title-variant` for article foreign-title semantics.
- Step 4 must prove article textual structure and body typography with article-specific executable evidence.
- Recommendations remain advisory; journal instructions remain conditional.

## Engineering rules

- Project-owned technical surfaces are English.
- Preserve the accepted shared V3 public API unless current authority explicitly authorizes change.
- Do not silently change normative IDs, expected values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only the contract encoded by that test.
- Reviewer comments are evidence, not automatic normative authority.
- Do not weaken tests to recover green CI.
- Temporary executors must be removed before checkpoint acceptance.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, integration-scope behavior, canonical content, phase status, acceptance status, or release/certification state.

For every material advance, update the relevant execution document and canonical handoff in the same work cycle; synchronize roadmap and machine state whenever phase, acceptance, evidence, integration scope, batch, or branch facts change.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded.

The machine contract keeps `phase_end_regression.candidate = one-immutable-sha`. Scoped Step checks never replace the Scientific Article phase-end regression; the phase-end Linux scope is `complete`.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement. Do not infer closure from naming, memory, historical intent, or partial evidence.
