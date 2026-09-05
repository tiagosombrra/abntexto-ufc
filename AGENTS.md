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
7. If the current phase, checkpoint, or temporary-artifact state disagrees, stop feature work and reconcile the control plane first.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override the current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Core Corrections**.
- Regression baseline: `c4bf51b574647226ee488440579ec2a204c16c79`.
- Regression planning checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`.
- Full regression integration run `33937439846` passed before Core Corrections began.
- Scientific-article runtime remains deferred until shared corrections and canonical reference-PDF validation are complete.
- The union of the two librarian-reviewed PDFs is tracked as exactly 34 requirements in `docs/UFC-LIBRARIAN-REVIEW.md`.
- Every material advance must update the active documentation/control state in the same work cycle.
- Every phase must end with a recorded phase-end regression before the next phase becomes active.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — active
3. **Reference PDF Validation** — queued
4. **Scientific Article** — queued
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers such as nested letter/number codes. GitHub issue/PR numbers and immutable SHAs provide traceability. Historical stage labels may appear only when needed to identify old evidence.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- The active repository is not an archive. Historical evidence belongs in Git history, tags, releases, issues, pull requests, and certified SHAs.
- Preserve the closed v3 public API unless a current requirement explicitly authorizes a change.
- Do not silently change normative rule IDs, expected values, tolerances, locators, applicability, source precedence, or proof-state semantics.
- A green test proves only the contract encoded by that test. Current authority and visual acceptance remain separate obligations.
- Reviewer comments are evidence, not automatic normative authority. Reconcile them against current institutional acts, current ABNT editions, compatible UFC requirements, and project precedence before changing normative behavior.
- For every automatically enforceable correction, add positive evidence and a negative case where practical.
- Presentation requirements require canonical PDF inspection in addition to source-level checks.
- Do not weaken tests merely to recover a green build. Correct the rule, generator, observer, or fixture according to the classified finding.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before checkpoint closeout.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Heavy Windows/literal-font/PDF-A/distribution checks belong to Final Certification or an explicitly justified correction task.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A material advance is any change that alters runtime behavior, normative classification, test/evidence coverage, canonical reference content, phase status, acceptance status, or release/certification state.

For every material advance:

1. update the relevant execution document or review matrix in the same work cycle;
2. update `docs/HANDOFF-V3.0.0.md` with the new checkpoint, evidence, unresolved blockers, and next action;
3. update `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json` whenever phase state, acceptance state, current batch, or machine-readable evidence changes;
4. keep Git branch/HEAD facts and machine state synchronized;
5. do not defer documentation reconciliation to phase closeout.

Pure comment/wording cleanup that changes no project state does not require rewriting every control file, but any claimed project advancement does.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until a phase-end regression has passed and its evidence has been recorded.

The phase-end regression must:

1. run on one immutable candidate SHA after the phase implementation/documentation work is complete;
2. include `Static contract` and the full relevant Linux integration contract, not only targeted tests from the last correction;
3. include every phase-specific acceptance surface, including canonical-PDF checks when presentation is in scope;
4. include the heavy literal-font/Windows/PDF-A/distribution matrix when closing **Final Certification**;
5. record the candidate SHA, workflow run IDs, conclusions, and any manual visual result required by the phase;
6. fail closed: any unexplained failure reopens the phase and blocks transition;
7. update handoff, roadmap, machine state, and the relevant review/correction matrix after the regression result is known.

Targeted green checks during a phase are evidence for individual corrections; they do not replace the phase-end regression.

## Core Corrections acceptance model

A correction closes only when the applicable evidence is established:

1. current authority or explicit project-policy classification;
2. runtime/reference behavior consistent with that classification;
3. automated positive evidence or an explicitly manual review contract;
4. negative evidence where failure is machine-detectable;
5. visual inspection of the canonical V3 PDF when presentation is part of the requirement.

Do not change disputed object-title typography or NBR 6023:2025 edge-case runtime merely to match older review comments. Those remain fail-closed until their current authority decision is explicit.

## Branch governance

The steady state is `main` plus short-lived task branches. Merged or abandoned task branches are deleted promptly. Releases are preserved by immutable version tags and GitHub Releases, not permanent release/audit branches.

## Fail-closed rule

If a required fact cannot be established from the current Git repository, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement to the next phase. Do not infer closure from naming, memory, historical intent, or a partial certification milestone.
