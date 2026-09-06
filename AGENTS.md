# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. During **Scientific Article**, also read `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `standards/coverage-rules-article.json`, and `docs/V3-RELEASE-READINESS.md`.
6. Compare Git facts, machine state, handoff, and roadmap.
7. If phase, checkpoint, acceptance state, or temporary-artifact state disagrees, reconcile the control plane before feature work.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Scientific Article**.
- Canonical base: `main` at shared-foundation merge `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active task branch: `feat/v3-scientific-article` through PR #286.
- Scientific Article Step 1 is accepted at `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`.
- Scientific Article Step 2 is accepted at `0947669c2c096dca93991e042d8ae245754688ba`: Static `34026680871` SUCCESS; Linux `34026680882` SUCCESS with `PASS=31 FAIL=0 SKIP=0`.
- Step 2 Linux emitted `ARTICLE-PROFILE-EVIDENCE` and `ARTICLE-FRONT-BLOCK-EVIDENCE` PASS on both engines; no article proof-state promotion occurred.
- Current batch: **Scientific Article — Optional foreign elements (Step 3)**.
- Current librarian-review state remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**; item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains a v3 release blocker owned by Final Certification/Release.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers such as nested letter/number codes. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Scientific Article rules

- Implement only one canonical type: `scientific-article`; no runtime aliases.
- Preserve the retained 18-rule article source contract.
- Required, optional, recommended and required-when-applicable semantics remain distinct.
- Reuse shared citation, reference, section, object and summary machinery rather than fork it.
- Shared mechanisms, source implementation, profile registration and green non-article tests do not by themselves prove article rules.
- Step 3 must keep foreign title and foreign summary independently optional. Their absence must compile cleanly and must not become a validation failure.
- Do not infer article foreign-title semantics from the shared `title-variant` metadata key; bind the article surface explicitly.
- Do not freeze unsupported foreign-element typography merely because an implementation needs a default rendering.
- Article body typography remains owned by Step 4.
- Recommendations remain advisory and must never become hard compilation or validation failures.
- Journal instructions remain a conditional applicability boundary.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- Preserve the closed shared V3 public API unless a current requirement explicitly authorizes a change.
- Do not silently change normative rule IDs, expected values, tolerances, locators, applicability, source precedence, modality, or proof-state semantics.
- A green test proves only the contract encoded by that test. Current authority and presentation acceptance remain separate obligations.
- Reviewer comments are evidence, not automatic normative authority.
- Do not weaken tests merely to recover green CI.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before checkpoint closeout.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, canonical content, phase status, acceptance status, or release/certification state.

For every material advance, update the relevant execution document and canonical handoff in the same work cycle; synchronize roadmap and machine state whenever phase, acceptance, evidence, batch, or branch facts change.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded.

The machine contract intentionally keeps `phase_end_regression.candidate = one-immutable-sha`. Targeted checks never replace the Scientific Article phase-end regression.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement. Do not infer closure from naming, memory, historical intent, or partial evidence.
