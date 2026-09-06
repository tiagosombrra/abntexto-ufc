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
- README user-guide correction: ACCEPTED at `a99f1e19eac1294eac35fb1da85196a1b8295d1a`; Static `34054110778`, Linux `34054110738`.
- Step 4 implementation commit: `e5291137d4753b7d776916ca0f08c67929dbb76b`.
- Current batch: **Step 4 — implementation complete, Static/Linux acceptance pending**.
- Step 4 implements required article structure plus 12 pt, justified, 2 cm first-line indent and single-spaced body evidence. It is not accepted until the synchronized checkpoint is green.
- Shared librarian-review state remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**; item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active, Step 4 acceptance gate
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## README ownership

`README.md` is the user-facing entry point for people who want to use the template. Keep it focused on choosing a released version, downloading it, configuring a document, compiling it, understanding the template layout, and solving common user problems.

Do not turn `README.md` into execution history. Detailed phase status, workflow run IDs, implementation SHAs, issue chronology, regression failures, normative disputes and control-plane mechanics belong in `docs/`, GitHub issues/pull requests, Actions and `release/v3-roadmap.json`.

The active README must also respect the canonical-identity contract. Stable-release instructions may identify the supported release and bundle names, but must not casually reintroduce a retired class identity into the active V3 tree.

## Linux integration scopes

`docs/LINUX-INTEGRATION-SCOPES.md` is the orchestration contract.

- PR `auto` normally uses the incremental pushed range on `synchronize` and the full PR diff on opened/reopened/ready events.
- If the synchronize endpoints are unavailable locally, scope selection falls back to the full PR diff and remains fail-closed.
- Documentation-only changes skip heavy Linux integration.
- Multiple known domains run a deduplicated union.
- Workflow/runner orchestration accompanying known domain changes does not force `complete`.
- Unknown technical paths and shared/core/standards surfaces fail closed to `complete`.
- Article gates are first-class checks; `profiles` contains exactly six non-article profiles and excludes `scientific-article`.
- The `article` scope now includes `validator-source`, `scientific-article-profile`, `scientific-article-front-block`, `scientific-article-foreign-elements`, and `scientific-article-body`.
- The Step 4 body gate must remain registered while Scientific Article, Final Certification or Release is active.
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
- Step 4 runtime body activation must remain profile-scoped and must not change the six non-article profiles.
- Step 4 requires article-specific physical PDF evidence for 12 pt, justification, 2 cm first-line indent and single spacing, plus a negative structural case.
- Recommendations remain advisory; journal instructions remain conditional.
- Step 6, not Step 4, owns later proof-state hardening/promotion.

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
