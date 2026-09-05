# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. If the active phase is `Regression Audit` or `Core Corrections`, also read `docs/V3-REGRESSION-AUDIT.md` and `docs/UFC-LIBRARIAN-REVIEW.md`.
6. Compare Git facts, machine state, handoff, and roadmap.
7. If the current phase, checkpoint, or temporary-artifact state disagrees, stop feature work and reconcile the control plane first.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override the current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Regression Audit**.
- Scientific-article runtime work is deferred until the shared foundation passes regression, correction, and canonical reference-PDF validation.
- Regression baseline on `main`: `c4bf51b574647226ee488440579ec2a204c16c79`.
- Certified non-article foundation retained for comparison/certification: `c79f3c73f1d51a30175e8259269504d029442a1c`.
- Scientific-article authority reconstruction is retained; its runtime implementation had not started when the regression reset began.
- The two librarian-reviewed PDFs are external evidence. Their union is tracked as the 34-item contract in `docs/UFC-LIBRARIAN-REVIEW.md`.

## Readable phase model

New work uses descriptive phase and work-package names:

1. **Regression Audit**
2. **Core Corrections**
3. **Reference PDF Validation**
4. **Scientific Article**
5. **Final Certification**
6. **Release**

Do not create new opaque work identifiers such as nested letter/number codes. GitHub issue/PR numbers and immutable SHAs provide traceability. Historical stage labels may appear only when needed to identify old evidence; they are not the naming scheme for new work.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- The active repository is not an archive. Historical evidence belongs in Git history, tags, releases, issues, pull requests, certified SHAs, and external verified backups.
- Do not create archive/history branches in the active repository.
- Preserve the closed v3 public API unless a current requirement explicitly authorizes a change.
- Do not silently change normative rule IDs, expected values, tolerances, locators, applicability, source precedence, or proof-state semantics.
- A green test proves only the contract encoded by that test. Regression review must separately establish that the encoded contract is current and correct.
- Reviewer comments are evidence, not automatic normative authority. Reconcile them against current institutional acts, current ABNT editions, compatible UFC requirements, and the project precedence policy before changing normative behavior.
- For every automatically enforceable correction, add positive evidence and a negative case where practical.
- Presentation requirements require canonical PDF inspection in addition to source-level checks.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before checkpoint closeout.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Heavy Windows/literal-font/PDF-A/distribution checks belong to final certification or an explicitly justified regression task, not every small edit.
- Do not rerun completed certification unless current-state validation requires it.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before the explicit **Release** phase is ready.

## Regression acceptance model

The regression is not closed by a plausible-looking PDF or by an all-green test run. A shared rule closes only when its relevant evidence is established:

1. current authority or explicit project-policy classification;
2. runtime/reference behavior consistent with that classification;
3. automated positive evidence or an explicitly manual review contract;
4. negative evidence where the failure is machine-detectable;
5. visual inspection of the canonical V3 PDF when presentation is part of the requirement.

The 34 librarian-review items use `PASS`, `PARTIAL`, `FAIL`, and `NORMATIVE-REVIEW` until their final disposition is proven.

## Branch governance

The steady state is `main` plus short-lived task branches. Merged or abandoned task branches are deleted promptly. Releases are preserved by immutable version tags and GitHub Releases, not permanent release/audit branches.

## Fail-closed rule

If a required fact cannot be established from the current Git repository, canonical state files, current normative evidence, or the reviewed source material, record the ambiguity and stop advancement to the next phase. Do not infer closure from naming, memory, historical intent, or a partial certification milestone.
