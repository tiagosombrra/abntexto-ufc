# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. During **Core Corrections**, also read `docs/V3-CORRECTION-PLAN.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/UFC-LIBRARIAN-REVIEW.md`.
6. Compare Git facts, machine state, handoff, and roadmap.
7. If phase, checkpoint, acceptance state, or temporary-artifact state disagrees, reconcile the control plane before feature work.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Core Corrections**.
- Regression baseline: `c4bf51b574647226ee488440579ec2a204c16c79`.
- Regression planning checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`.
- Regression baseline Linux run `33937439846`: success.
- Object/Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`: Static `33965794475` success; Linux `33965794519` success with `PASS=31 FAIL=0 SKIP=0`.
- Canonical-reference source checkpoint `3ae9dd698e021a117ba2b64ebf970dc8c507fa8f`: Static `33968579418` success; Linux `33968579449` success with `PASS=31 FAIL=0 SKIP=0`. Source-level librarian evidence for items 11, 16 and 28 is accepted.
- Current implementation checkpoint: `a1149f169f06b2db620bc5df69d0870b60fe583c`, extending the canonical `reference-document` gate with generated-PDF text evidence for items 11, 16 and 28. Branch acceptance is pending.
- Review item 21 is closed: upper illustration/table/object identification/title is 12 pt and lower source/legend/note remains 10 pt where applicable.
- Current 34-item state before generated-PDF acceptance: **25 PASS / 8 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence for disputed edge cases.
- Scientific Article runtime remains deferred until Core Corrections and Reference PDF Validation are complete.
- Every material advance updates the active documentation/control state in the same work cycle.
- Every phase ends with a recorded phase-end regression before the next phase becomes active.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — active
3. **Reference PDF Validation** — queued
4. **Scientific Article** — queued
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers such as nested letter/number codes. GitHub issue/PR numbers and immutable SHAs provide traceability. Historical labels may appear only to identify old evidence.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- Preserve the closed v3 public API unless a current requirement explicitly authorizes a change.
- Do not silently change normative rule IDs, expected values, tolerances, locators, applicability, source precedence, or proof-state semantics.
- A green test proves only the contract encoded by that test. Current authority and presentation acceptance remain separate obligations.
- Reviewer comments are evidence, not automatic normative authority. Reconcile them against current institutional acts, current ABNT editions, compatible UFC requirements, and project precedence before changing normative behavior.
- For every automatically enforceable correction, add positive evidence and a negative case where practical.
- Presentation requirements require canonical PDF evidence in addition to source-level checks.
- Do not weaken tests merely to recover green CI. Correct the rule, generator, observer, or fixture according to the classified finding.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before checkpoint closeout.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Heavy Windows/literal-font/PDF-A/distribution checks belong to Final Certification or an explicitly justified correction task.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A material advance is any change that alters runtime behavior, normative classification, test/evidence coverage, canonical reference content, phase status, acceptance status, or release/certification state.

For every material advance:

1. update the relevant execution document or review matrix in the same work cycle;
2. update `docs/HANDOFF-V3.0.0.md` with the checkpoint, evidence, unresolved blockers, and next action;
3. update `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json` whenever phase state, acceptance state, current batch, or machine-readable evidence changes;
4. keep Git branch/HEAD facts and machine state synchronized;
5. do not defer documentation reconciliation to phase closeout.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant regression and the result is recorded.

At minimum this includes Static contract, full relevant Linux integration, phase-specific acceptance evidence, and canonical-PDF checks when presentation is in scope. Final Certification additionally requires the heavy literal-font/Windows/PDF-A/distribution matrix. Any unexplained failure keeps the phase open.

## Core Corrections acceptance model

A correction closes only when the applicable combination is established: current authority/project classification, correct runtime/reference behavior, automated positive evidence or explicit manual review, negative evidence where practical, and canonical-PDF evidence when presentation is part of the requirement.

The object-title typography authority decision is final for the current evidence state and is recorded in `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`. Item 33 remains fail-closed until current authoritative NBR 6023:2025 text supports any additional runtime change.

## Branch governance and fail-closed rule

The steady state is `main` plus short-lived task branches. Releases are preserved by immutable tags and GitHub Releases, not permanent audit branches.

If a required fact cannot be established from the current Git repository, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement to the next phase. Do not infer closure from naming, memory, historical intent, or partial certification evidence.
