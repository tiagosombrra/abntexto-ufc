# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. During **Scientific Article**, also read `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `standards/coverage-rules-article.json`, `docs/NORMATIVE-CURRENCY.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-RELEASE-READINESS.md`, and `docs/ENGINEERING-LANGUAGE.md`.
6. Compare Git facts, machine state, handoff, roadmap and the active phase documents.
7. If phase, checkpoint, acceptance state, article authority, proof state, artifact provenance, release-blocker state, or temporary-artifact state disagrees, reconcile the control plane before feature work.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Scientific Article**.
- Canonical `main`: `e6833ed5cf07aaf1021c690260cecfacec1a119a`, PR #285 merged.
- Active task branch: `feat/v3-scientific-article`.
- Active pull request: #286.
- Regression Audit, Core Corrections and Reference PDF Validation are closed with their recorded phase-end regressions.
- Current 34-item librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Article authority contract: 18 source-backed rules in `docs/ARTICLE-NORMATIVE-CONTRACT.md` / `standards/coverage-rules-article.json`.
- Scientific Article Step 1: **ACCEPTED** at `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`; Static `34001350884`; Linux `34001350953`, `PASS=31 FAIL=0 SKIP=0`.
- Step 2 runtime implementation: `90293af760c4063b02a16831196ec3d932f1471d`.
- Normative-currency correction: `e29501bd8cae98d6442f08e17bc3a54892fc7e0d`.
- Post-currency synchronized checkpoint `6587636f8550dcd68b3feec5bbd145551775eb4b`: Static `34003838489` SUCCESS; Linux `34003838521` FAILURE, `PASS=29 FAIL=1 SKIP=1`.
- Linux `34003838521` failed only the article front-block evidence because the checker imposed an unsupported fixed physical-page bottom percentage on author-note placement.
- Validator correction: `bb52697a0e71b2d6a8bc135196f40dba9497b38f`.
- Current implementation step: **Required article front block — EVIDENCE CORRECTION / CI PENDING**.
- Runtime `abntexto-ufc/articles.def` is unchanged by the current validator correction.
- Corrected authorship-footnote evidence combines a source-enforced genuine LaTeX `\footnote` route with rendered post-front-block 10 pt footnote typography.
- Optional foreign elements remain deferred to Step 3; article body typography remains deferred to Step 4; recommendations remain advisory.
- Article proof state remains manual/conditional-manual; no article rule is promoted merely by source implementation, runtime activation, shared green checks or this validator correction.
- Release blocker #18 remains owned by Final Certification/Release: deterministic reference PDF via pinned release epoch/`SOURCE_DATE_EPOCH` and rebuilt hash evidence.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active; Step 1 accepted; Step 2 evidence correction/CI pending
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers such as nested letter/number codes. Historical labels may appear only when identifying old evidence. Current work names must be descriptive.

## Scientific Article boundaries

- Implement one canonical `scientific-article` profile; do not add compatibility aliases.
- Step 1 reuses `author`, `title`, `approval-date`; adds only `submission-date` and `article-author-note`.
- Step 2 required front block is implemented through `abntexto-ufc/articles.def` and must be accepted by article-specific rendered evidence on pdfLaTeX and LuaLaTeX before Step 3 activates.
- `\ufcPrintArticleFrontMatter{...}` must remain article-profile-only and require title, author, author note, submission date, approval date and primary summary.
- The authorship-footnote contract requires a genuine footnote. Do not invent a physical-page percentage unless current authority explicitly requires it.
- The source gate must continue to prove `article-author-note` is routed through `\footnote`; the PDF gate must prove the note renders after the front block with shared footnote typography.
- Do not infer foreign-title semantics from `title-variant`; bind that behavior explicitly in the optional-foreign-elements step.
- Do not activate article body typography in the required-front-block step; body behavior belongs to Step 4.
- Reuse current citation, bibliography, section, summary and object infrastructure rather than fork it.
- Preserve the 18-rule source contract unless new current authority requires a separately documented source correction.
- Keep required, optional, recommended and conditional semantics distinct.
- Do not promote an article rule to executable/proven merely because shared non-article machinery, profile selection, source-level implementation, runtime activation or a validator fix is green.
- Add rule-specific positive evidence before proof-state promotion; add controlled negative evidence where a safe rejectable case exists.
- Journal-specific instructions remain an applicability boundary.
- Preserve the validated non-article foundation and accepted reference PDF presentation.

## Failure-classification rule

Before changing runtime or tests after a failed gate, classify whether the failure is:

- runtime behavior;
- source/normative authority;
- evidence predicate;
- control-plane state; or
- infrastructure/transient execution.

A test predicate that exceeds the source-backed requirement is a validator defect. Correct that predicate without weakening the actual requirement. Linux `34003838521` is the current example: the real `\footnote` route remained intact, while the unsupported `65% of physical page height` acceptance predicate was removed and replaced by semantic route + rendered 10 pt footnote evidence.

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

The steady state is `main` plus one short-lived active task branch. PR #285 is merged. New article work belongs only on `feat/v3-scientific-article`, based on updated `main`, and is tracked in PR #286. The old `plan/v3-regression-reset` and other historical remote branches are provenance only and must not receive new work.

Historical opaque R2/R3 evidence files are provenance only, not active control authority. Their presence does not authorize work from them.

If a required fact cannot be established from the current Git repository, canonical state files, current normative evidence, reviewed source material, or a provenance-bound canonical artifact, record the ambiguity and stop advancement to the next phase.
