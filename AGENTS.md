# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. Identify the actual Git branch and HEAD.
2. Read `release/v3-roadmap.json`.
3. Read `docs/HANDOFF-V3.0.0.md`.
4. Read `docs/ROADMAP-V3.0.0.md`.
5. During **Scientific Article**, also read `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `standards/coverage-rules-article.json`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, and `docs/ENGINEERING-LANGUAGE.md`.
6. Compare Git facts, machine state, handoff, roadmap and the active phase documents.
7. If phase, checkpoint, acceptance state, article authority, proof state, artifact provenance, or temporary-artifact state disagrees, reconcile the control plane before feature work.

Memory, prior chats, historical branch names, old pull requests, and workflow names never override current repository state.

## Current state

- Target version: `3.0.0`.
- Active phase: **Scientific Article**.
- Core Corrections phase-end candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Reference PDF Validation phase-end candidate `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790` and Linux `33985595798` success.
- Canonical reference artifact: build SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, run `33983729996`, artifact `9974546873`, 55 A4 pages, PDF 1.7, TeX Live 2026/pdfLaTeX.
- Complete reference-PDF visual review: **PASS, 55/55 pages, 0 unexplained visual FAIL**.
- Current 34-item librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Article authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` / `standards/coverage-rules-article.json`.
- Article rules: 18 source-backed rules; pre-implementation validation remains manual/conditional-manual until article-specific executable evidence exists.
- Current runtime inspection: `abntexto-ufc/core.def` does not yet expose `type = scientific-article`; implementation starts in this phase.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers such as nested letter/number codes. Historical labels such as `V3-A1` or `V3-A2` may appear only when identifying old evidence, issues or SHAs. Current work names must be descriptive.

## Scientific Article boundaries

- Implement one canonical `scientific-article` profile; do not add compatibility aliases.
- Reuse current citation, bibliography, section, summary and object infrastructure rather than fork it.
- Preserve the 18-rule source contract unless new current authority requires a separately documented source correction.
- Keep required, optional, recommended and conditional semantics distinct.
- Do not promote an article rule to executable/proven merely because shared non-article machinery is green.
- Add rule-specific positive evidence before proof-state promotion; add controlled negative evidence where a safe rejectable case exists.
- Journal-specific instructions remain an applicability boundary; the generic UFC article profile does not supersede a target journal.
- Preserve the validated non-article foundation and the accepted reference PDF presentation.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal Portuguese output under test, or explicit upstream/current-runtime boundaries.
- Treat an engineering-language gate that misses known project-owned Portuguese diagnostics as a false-negative defect. Fix the detector and diagnostics; do not weaken the policy or flag legitimate academic Portuguese.
- Preserve the closed v3 public API except for the bounded new public article profile/API explicitly required by the Scientific Article contract.
- Do not silently change normative rule IDs, expected values, tolerances, locators, applicability, source precedence, or proof-state semantics.
- A green test proves only the contract encoded by that test. Current authority and presentation acceptance remain separate obligations.
- Reviewer comments are evidence, not automatic normative authority.
- Presentation requirements require canonical PDF evidence in addition to source-level checks.
- Do not weaken tests merely to recover green CI.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before checkpoint closeout.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Heavy Windows/literal-font/PDF-A/distribution checks belong to Final Certification unless a bounded article change directly requires them.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, canonical reference content, article proof state, phase status, acceptance status, artifact provenance, temporary-executor lifecycle, or release/certification state.

For every material advance, update the relevant execution document/review matrix and canonical handoff in the same work cycle; synchronize roadmap/machine state whenever phase, acceptance, evidence, batch, branch, article-rule, artifact, or temporary-executor facts change.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded.

The machine contract intentionally represents this invariant with `phase_end_regression.candidate = one-immutable-sha`. Do not replace that sentinel with prose or an actual self-referential SHA. Exact Git candidate SHAs are recorded in evidence after immutable commits exist.

Reference PDF Validation satisfied this rule with candidate `b64074c64941895f97fbe0f795ce826c798d17ce`, Static `33985595790`, full Linux `33985595798`, accepted canonical provenance and complete visual PASS.

Scientific Article must end with its own immutable candidate containing article runtime, rule-specific evidence, canonical article rendering and synchronized documentation. Targeted article checks do not replace that phase-end regression.

## Branch governance and fail-closed rule

The steady state is `main` plus short-lived task branches. Releases are preserved by immutable tags and GitHub Releases, not permanent audit branches.

If a required fact cannot be established from the current Git repository, canonical state files, current normative evidence, reviewed source material, or a provenance-bound canonical artifact, record the ambiguity and stop advancement to the next phase. Do not infer closure from naming, memory, historical intent, old PDFs, or partial certification evidence.
