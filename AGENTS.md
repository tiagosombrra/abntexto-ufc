# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. During **Scientific Article**, also read `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `standards/coverage-rules-article.json`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-RELEASE-READINESS.md`, and `docs/ENGINEERING-LANGUAGE.md`.
6. Compare Git facts, machine state, handoff, roadmap and the active phase documents.
7. If phase, checkpoint, acceptance state, article authority, proof state, artifact provenance, release-blocker state, or temporary-artifact state disagrees, reconcile the control plane before feature work.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Scientific Article**.
- Canonical `main` now contains the validated shared foundation and accepted Scientific Article Step 1 at squash merge `e6833ed5cf07aaf1021c690260cecfacec1a119a` (PR #285).
- Active task branch: `feat/v3-scientific-article`, created from that updated `main`.
- Core Corrections phase-end candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Reference PDF Validation phase-end candidate `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790` and Linux `33985595798` success.
- Canonical reference artifact: 55 A4 pages, TeX Live 2026/pdfLaTeX, complete visual review PASS 55/55.
- Current 34-item librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Article authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` / `standards/coverage-rules-article.json`.
- Article rules: 18 source-backed rules; profile registration does not promote presentation/proof state.
- Step 1 implementation checkpoint: `b46ba2051f8c9c712a7b5d25748b81baa52b920a`.
- Step 1 synchronized checkpoint `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`: Static `34001350884` SUCCESS; full Linux `34001350953` SUCCESS, `PASS=31 FAIL=0 SKIP=0`.
- Step 1 state: **ACCEPTED**.
- Current implementation step: **Required article front block**.
- Release blocker #18 is explicit and owned by Final Certification/Release: the release reference PDF must become bit-reproducible using a pinned release epoch/`SOURCE_DATE_EPOCH` and hash comparison.
- Historical orchestration issue #217 is closed as superseded by the readable permanent workflow model.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active; Step 1 accepted; Required article front block active
5. **Final Certification** — queued; owns release reproducibility proof together with Release
6. **Release** — queued

Do not create new opaque work identifiers such as nested letter/number codes. Historical labels may appear only when identifying old evidence. Current work names must be descriptive.

## Scientific Article boundaries

- Implement one canonical `scientific-article` profile; do not add compatibility aliases.
- Step 1 reuses `author`, `title`, `approval-date`; adds only `submission-date` and `article-author-note`.
- Required article front block must add article-specific rendering/evidence for primary title, authorship metadata note, submission/approval dates and primary summary without contaminating accepted academic-work front matter.
- Do not infer foreign-title semantics from `title-variant`; bind that behavior explicitly in the optional-foreign-elements step.
- Reuse current citation, bibliography, section, summary and object infrastructure rather than fork it.
- Preserve the 18-rule source contract unless new current authority requires a separately documented source correction.
- Keep required, optional, recommended and conditional semantics distinct.
- Do not promote an article rule to executable/proven merely because shared non-article machinery or the profile-selection gate is green.
- Add rule-specific positive evidence before proof-state promotion; add controlled negative evidence where a safe rejectable case exists.
- Journal-specific instructions remain an applicability boundary.
- Preserve the validated non-article foundation and accepted reference PDF presentation.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- Preserve the closed v3 public API except for the bounded new article profile/API explicitly required by the Scientific Article contract.
- Do not silently change normative rule IDs, expected values, tolerances, locators, applicability, source precedence, or proof-state semantics.
- A green test proves only the contract encoded by that test. Current authority and presentation acceptance remain separate obligations.
- Reviewer comments are evidence, not automatic normative authority.
- Presentation requirements require canonical PDF evidence in addition to source-level checks.
- Do not weaken tests merely to recover green CI.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before checkpoint closeout.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Heavy Windows/literal-font/PDF-A/distribution checks belong to Final Certification unless a bounded article change directly requires them.
- Release reproducibility issue #18 must be resolved before v3.0.0 publication; it does not block current Scientific Article implementation.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, canonical reference content, article proof state, phase status, acceptance status, artifact provenance, release-blocker state, temporary-executor lifecycle, or release/certification state.

For every material advance, update the relevant execution document and canonical handoff in the same work cycle; synchronize roadmap/machine state whenever phase, acceptance, evidence, batch, branch, article-rule, artifact, blocker, or temporary-executor facts change.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded.

The machine contract intentionally represents this invariant with `phase_end_regression.candidate = one-immutable-sha`. Do not replace that sentinel with prose or an actual self-referential SHA.

Scientific Article must end with its own immutable candidate containing article runtime, rule-specific evidence, canonical article rendering and synchronized documentation. Targeted article checks do not replace that phase-end regression.

## Branch governance and fail-closed rule

The steady state is `main` plus one short-lived active task branch. PR #285 is merged. New article work belongs only on `feat/v3-scientific-article`, based on updated `main`. The old `plan/v3-regression-reset` and other historical remote branches are provenance only and must not receive new work.

Historical opaque R2/R3 evidence files are provenance only, not active control authority. Their presence does not authorize work from them.

If a required fact cannot be established from the current Git repository, canonical state files, current normative evidence, reviewed source material, or a provenance-bound canonical artifact, record the ambiguity and stop advancement to the next phase.
