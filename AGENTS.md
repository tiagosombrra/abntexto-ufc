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
- Step 2: ACCEPTED at `0947669c2c096dca93991e042d8ae245754688ba`; Static `34026680871`, Linux `34026680882`, `PASS=31 FAIL=0 SKIP=0`.
- Step 3 implementation checkpoint: `81e08321222efb03626ac421fc645bd66edd5ae8`.
- Synchronized Step 3 head `567a5b2d21a16b653d7704639bdd5012d7c2f99b`: Static `34028373064` SUCCESS; full Linux `34028373060` failed only in the article foreign-elements evidence path after all preceding shared checks and all six non-article profile builds had passed.
- Failure classification: `scientific-article-foreign-elements.sh` inspected expected first-pass cross-reference/Biber rerun warnings after only one LaTeX pass. This is an evidence-orchestration defect, not an article runtime, authority or modality failure.
- Current batch: **Scientific Article — Step 3 evidence correction + scoped Linux integration orchestration**.
- Shared librarian-review state remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**; item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Linux integration scopes

`docs/LINUX-INTEGRATION-SCOPES.md` is the orchestration contract.

- PR `auto` uses the incremental pushed range on `synchronize` and the full PR diff on opened/reopened/ready events.
- Available bounded scopes include `article`, `profiles`, `reference-document`, `reference-pdf`, `frontmatter`, `layout`, `objects`, `bibliography`, `backmatter`, `research-project` and `smoke`.
- Multiple known domains run the union of their checks without duplicates.
- Documentation-only changes skip heavy Linux integration.
- Shared/core, standards/integration infrastructure and unknown technical paths fail closed to `complete`.
- Manual `workflow_dispatch` exposes the same named scopes; manual `auto` fails closed to `complete`.
- Article gates are first-class coordinated checks, not recursively hidden inside `profiles` or another article gate.
- During Scientific Article, the `article` scope must include `validator-source`, `scientific-article-profile`, `scientific-article-front-block` and `scientific-article-foreign-elements`; later article-specific executable gates must join the suite in the same material advance.
- Scoped runs are intermediate evidence only. Every phase-end regression still requires `complete` Linux integration on the immutable candidate.

## Scientific Article rules

- Implement only one canonical type: `scientific-article`; no runtime aliases.
- Preserve the retained 18-rule article source contract.
- Required, optional, recommended and required-when-applicable semantics remain distinct.
- Reuse shared citation, reference, section, object and summary machinery rather than fork it.
- Shared mechanisms, source implementation, profile registration and green non-article tests do not by themselves prove article rules.
- Step 3 foreign title and foreign summary remain independently optional; absence must compile cleanly and must not become a validation failure.
- Do not infer foreign-title semantics from shared `title-variant`; the Step 3 route is explicit and article-only.
- Step 3 presentation is deliberately minimally asserted; optionality/routing evidence must not invent unsupported typography requirements.
- Article body typography remains owned by Step 4.
- Recommendations remain advisory and never become hard compilation/validation failures.
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

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, integration-scope behavior, canonical content, phase status, acceptance status, or release/certification state.

For every material advance, update the relevant execution document and canonical handoff in the same work cycle; synchronize roadmap and machine state whenever phase, acceptance, evidence, integration scope, batch, or branch facts change.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded.

The machine contract intentionally keeps `phase_end_regression.candidate = one-immutable-sha`. Targeted/scoped Step checks never replace the Scientific Article phase-end regression. The Linux scope for phase-end regression is `complete`.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement. Do not infer closure from naming, memory, historical intent, or partial evidence.
