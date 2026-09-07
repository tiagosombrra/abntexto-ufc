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
- Steps 1–3: ACCEPTED. Step 3 acceptance: `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba`; Static `34031144114`; Linux `34031144269`.
- README user guide: ACCEPTED at `a99f1e19eac1294eac35fb1da85196a1b8295d1a`; Static `34054110778`; Linux `34054110738`.
- Step 4 implementation: `e5291137d4753b7d776916ca0f08c67929dbb76b`.
- Rejected Step 4 checkpoint `8b52ee4b36b23868fecce9bbe9b843f689ccc01e`: Static `34058435312` PASS; Linux `34058435311` FAIL because body spacing remained 1.5 (`20.700 pt`) instead of single (`13.800 pt`).
- Runtime correction checkpoint `177a62115e1dc28b24394ed4061600c3a7386fca`: Static `34070809181` PASS; Linux `34070809177` FAIL before physical body execution because three Step 4 gates still required the retired literal `\AtBeginDocument{...}` registration.
- Current batch: **Step 4 — remove stale implementation-token coupling from article gates and rerun acceptance**.
- The runtime correction remains `\AddToHook{begindocument/end}{\ufc_article_apply_body_typography:}`. The physical body checker is unchanged.
- Step 5 remains blocked until the corrected Step 4 runtime and updated semantic gates pass together.
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

## Scientific Article rules

- One canonical type: `scientific-article`; no aliases.
- Preserve the retained 18-rule article source contract.
- Keep required, optional, recommended and required-when-applicable semantics distinct.
- Reuse shared bibliography, citation, section, object and summary mechanisms rather than fork them.
- Shared implementation is not article proof.
- Step 4 body activation must remain profile-scoped and execute after shared begin-document layout initialization.
- Step 4 must prove 12 pt, justification, 2 cm first-line indent and true single spacing under both engines, plus the missing-Development negative case.
- Tests may protect semantic/runtime boundaries but must not freeze an implementation token when a different hook preserves the required behavior. The `34070809177` failure is classified as stale gate coupling; updating those source guards must not weaken physical PDF evidence.
- Recommendations remain advisory; journal instructions remain conditional.
- Step 6 owns later proof-state hardening/promotion.

## Engineering rules

- Project-owned technical surfaces are English.
- Preserve the accepted shared V3 public API unless current authority explicitly authorizes change.
- Do not silently change normative IDs, expected values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only the contract encoded by that test.
- Reviewer comments are evidence, not automatic normative authority.
- Do not weaken tests to recover green CI. Correct stale implementation coupling only when the semantic/physical predicate remains equally or more strict.
- Temporary executors must be removed before checkpoint acceptance.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, integration-scope behavior, canonical content, phase status, acceptance status, or release/certification state.

For every material advance, update the relevant execution document and canonical handoff in the same work cycle; synchronize roadmap and machine state whenever phase, acceptance, evidence, integration scope, batch, or branch facts change.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded.

The machine contract keeps `phase_end_regression.candidate = one-immutable-sha`. Scoped Step checks never replace the Scientific Article phase-end regression; phase-end Linux uses `complete`.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement. Do not infer closure from naming, memory, historical intent, or partial evidence.
