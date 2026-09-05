# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. During **Reference PDF Validation**, also read `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, and `docs/ENGINEERING-LANGUAGE.md`.
6. Compare Git facts, machine state, handoff, roadmap and the active phase document.
7. If phase, checkpoint, acceptance state, artifact provenance, or temporary-artifact state disagrees, reconcile the control plane before feature work.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Reference PDF Validation**.
- Core Corrections immutable phase-end candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041` and full Linux `33982156042` success; Linux summary `PASS=31 FAIL=0 SKIP=0`.
- Core Corrections is CLOSED.
- Current 34-item state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Pre-existing 2026-09-04 reference PDF is comparison-only because it predates accepted Core Corrections.
- Current batch: **Reference PDF Validation — fresh provenance-bound canonical build**.
- Temporary executor `.github/workflows/tmp-reference-pdf.yml` is ACTIVE and must be removed immediately after artifact recovery.
- Active phase contract: `docs/V3-REFERENCE-PDF-VALIDATION.md`.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred until Reference PDF Validation closes.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed; phase-end regression accepted at `5f67560a...`
3. **Reference PDF Validation** — active
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

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, canonical reference content, phase status, acceptance status, artifact provenance, visual-validation status, temporary-executor lifecycle, or release/certification state.

For every material advance, update the relevant execution document/review matrix and canonical handoff in the same work cycle; synchronize roadmap/machine state whenever phase, acceptance, evidence, batch, branch, artifact, or temporary-executor facts change.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded.

The machine contract intentionally represents this invariant with `phase_end_regression.candidate = one-immutable-sha`. Do not replace that sentinel with prose or an actual self-referential SHA. Exact Git candidate SHAs are recorded in evidence after immutable commits exist.

Core Corrections satisfied this rule with candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, Static `33982156041`, and Linux `33982156042`.

## Reference PDF Validation acceptance model

- Use only a real LaTeX-generated canonical artifact tied to a concrete repository SHA.
- Do not use a stale, synthetic or recreated PDF as acceptance evidence.
- Render the complete PDF and inspect every page; source checks and automated geometry do not replace visual review.
- Confirm no clipping, overlap, broken glyphs, unexpected page breaks, object overflow, heading drift or pagination anomalies.
- Reconfirm presentation-sensitive librarian-review items and preserve item 33 as an explicit authority gap.
- Any defect must be classified before code/test changes; after a correction, rebuild, re-render and re-inspect.
- Remove the temporary canonical-build workflow immediately after artifact recovery.
- Scientific Article remains blocked until this phase and its own phase-end regression close.

## Branch governance and fail-closed rule

The steady state is `main` plus short-lived task branches. Releases are preserved by immutable tags and GitHub Releases, not permanent audit branches.

If a required fact cannot be established from the current Git repository, canonical state files, current normative evidence, reviewed source material, or a provenance-bound canonical artifact, record the ambiguity and stop advancement to the next phase. Do not infer closure from naming, memory, historical intent, old PDFs, or partial certification evidence.
