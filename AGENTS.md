# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. During **Core Corrections**, also read `docs/V3-CORRECTION-PLAN.md`, `docs/V3-REGRESSION-AUDIT.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, and `docs/ENGINEERING-LANGUAGE.md`.
6. Compare Git facts, machine state, handoff, and roadmap.
7. If phase, checkpoint, acceptance state, or temporary-artifact state disagrees, reconcile the control plane before feature work.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Core Corrections**.
- Front Matter and Annex Closeout checkpoint `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8`: Static `33980847191` and Linux `33980847189` success, `PASS=31 FAIL=0 SKIP=0`.
- Current 34-item state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Rejected phase-end candidate `3b2476371e1df5180d8ee25ea53aed6a13fa2da2`: Static `33981960024` failed only because the machine candidate sentinel did not equal `one-immutable-sha`.
- Current batch: **Core Corrections — Corrected Phase-end Regression Candidate**.
- Candidate contract: `docs/V3-CORE-CORRECTIONS-PHASE-END.md`.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred until Core Corrections and Reference PDF Validation are complete.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — active, corrected phase-end candidate gate
3. **Reference PDF Validation** — queued
4. **Scientific Article** — queued
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers such as nested letter/number codes. GitHub issue/PR numbers and immutable SHAs provide traceability. Historical labels may appear only to identify old evidence.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- Treat an engineering-language gate that misses known project-owned Portuguese diagnostics as a false-negative defect. Fix the detector and diagnostics; do not weaken the policy or flag legitimate academic Portuguese.
- Preserve the closed v3 public API unless a current requirement explicitly authorizes a change.
- Do not silently change normative rule IDs, expected values, tolerances, locators, applicability, source precedence, or proof-state semantics.
- A green test proves only the contract encoded by that test. Current authority and presentation acceptance remain separate obligations.
- Reviewer comments are evidence, not automatic normative authority.
- Presentation requirements require canonical PDF evidence in addition to source-level checks.
- Do not weaken tests merely to recover green CI.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before checkpoint closeout.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Heavy Windows/literal-font/PDF-A/distribution checks belong to Final Certification or an explicitly justified correction task.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, canonical reference content, phase status, acceptance status, or release/certification state.

For every material advance, update the relevant execution document/review matrix and canonical handoff in the same work cycle; synchronize roadmap/machine state whenever phase, acceptance, evidence, batch, or branch facts change.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded.

The machine contract intentionally represents this invariant with `phase_end_regression.candidate = one-immutable-sha`. Do not replace that sentinel with prose or an actual self-referential SHA. The exact Git candidate SHA is recorded in evidence after the immutable commit exists.

Candidate `3b247637...` was rejected because it violated this representation invariant. The corrected candidate restores the sentinel; `tests/checks/phase_governance.py` remains unchanged.

## Core Corrections acceptance model

All currently resolvable librarian-review corrections are accepted. Item 33 remains a fail-closed authority gap and must not be converted into speculative runtime behavior merely to obtain a fully-PASS matrix.

## Branch governance and fail-closed rule

The steady state is `main` plus short-lived task branches. Releases are preserved by immutable tags and GitHub Releases, not permanent audit branches.

If a required fact cannot be established from the current Git repository, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement to the next phase. Do not infer closure from naming, memory, historical intent, or partial certification evidence.
