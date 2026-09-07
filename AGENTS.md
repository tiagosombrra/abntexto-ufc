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
- Rejected Step 4 synchronized checkpoint: `8b52ee4b36b23868fecce9bbe9b843f689ccc01e`; Static `34058435312` PASS, Linux `34058435311` FAIL (`article`: PASS=4 FAIL=1).
- Step 4 failure classification: real runtime initialization-order defect. The article body rendered at the shared 1.5-spacing gap (`20.700 pt`) instead of the same-document single-spacing calibration (`13.800 pt`).
- Current batch: **Step 4 — body-spacing initialization-order correction implemented, acceptance rerun pending**.
- Correction strategy: keep the article-only runtime predicate and apply it through `begindocument/end`, after shared begin-document layout initialization. The body checker is unchanged.
- Step 5 remains blocked until the corrected synchronized checkpoint is green and acceptance is documented.
- Shared librarian-review state remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**; item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active, Step 4 correction acceptance gate
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Linux integration scopes

`docs/LINUX-INTEGRATION-SCOPES.md` is the orchestration contract. The `article` scope contains `validator-source`, `scientific-article-profile`, `scientific-article-front-block`, `scientific-article-foreign-elements`, and `scientific-article-body`. `profiles` remains the six non-article profiles. Scoped runs are intermediate evidence only; phase-end regression always uses `complete`.

## Scientific Article rules

- One canonical type: `scientific-article`; no aliases.
- Preserve the retained 18-rule article source contract.
- Keep required, optional, recommended and required-when-applicable semantics distinct.
- Reuse shared bibliography, citation, section, object and summary mechanisms rather than fork them.
- Shared implementation is not article proof.
- Step 4 runtime body activation must remain profile-scoped and must not change the six non-article profiles.
- Step 4 requires article-specific physical PDF evidence for 12 pt, justification, 2 cm first-line indent and single spacing, plus a negative structural case.
- The failed `34058435311` body measurement is a runtime defect; do not weaken or recalibrate the checker to accept 1.5 spacing.
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
