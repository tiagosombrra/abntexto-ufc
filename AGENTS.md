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

| Fact | Current state |
|---|---|
| Target version | `3.0.0` |
| Active phase | **Scientific Article** |
| Canonical base | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active task branch | `feat/v3-scientific-article`, PR #286 |
| Steps 1–3 | ACCEPTED |
| Latest fully validated checkpoint | `a99f1e19eac1294eac35fb1da85196a1b8295d1a` |
| Latest synchronized Step 4 result | `05194675f7d41d8c4f35227e67e8ee303d1ea79a`; Static `34115345674` PASS; Linux `34115345586` FAIL, `SCOPE=article PASS=4 FAIL=1 SKIP=0` |
| Positive Step 4 body evidence | PASS under pdfLaTeX and LuaLaTeX: 12 pt, justified, 2 cm first-line indent, 13.800 pt single-spacing calibration |
| Current Step 4 checker correction | `4039fa011b7f54f4f0be6d004131fc0e06567e2e` — required structure is matched as rendered headings, not arbitrary prose tokens |
| Current batch | **Step 4 — repair negative structural evidence classification; synchronized CI pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

Linux `34115345586` materially changed the diagnosis. The supported `\\singlesp` plus `cmd/textual/after` runtime route now passes the physical body predicates under both engines. The sole failure is the negative structural fixture: the checker previously searched the entire extracted PDF for the word `desenvolvimento`, so prose mentioning that word falsely satisfied the required-heading check and the validator later failed on intentionally absent physical markers.

The current checker correction preserves the negative fixture prose and strengthens `validate_structure()` to require one rendered heading line for each required structural element, allowing an optional progressive section number. The physical typography predicates, tolerances, runtime implementation and 18-rule authority contract are unchanged.

Step 5 remains blocked until the synchronized checker correction passes Static and all five article checks, including rejection of the missing-Development fixture for the intended structural reason.

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
- Step 4 must prove 12 pt, justification, 2 cm first-line indent and true single spacing under both engines, plus the missing-Development negative case.
- The article body contract must survive the upstream `\\textual` transition by reapplying the supported single-spacing route after that transition.
- Required structural evidence must identify rendered headings, not incidental occurrences of heading words in prose.
- Step 2 and Step 3 gates must not be coupled to Step 4 implementation syntax. Step 4 owns its own source and physical evidence.
- Recommendations remain advisory; journal instructions remain conditional.
- Step 6 owns later proof-state hardening/promotion.

## Engineering rules

- Project-owned technical surfaces are English.
- Preserve the accepted shared V3 public API unless current authority explicitly authorizes change.
- Do not silently change normative IDs, expected values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only the contract encoded by that test.
- Reviewer comments are evidence, not automatic normative authority.
- Do not weaken tests to recover green CI. Physical PDF predicates remain authoritative for Step 4.
- Negative evidence must fail for the intended predicate; an unrelated later failure does not satisfy the negative contract.
- Deprecated upstream APIs must not be allowlisted merely to bypass warnings when a supported route exists.
- Temporary executors must be removed before checkpoint acceptance.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, integration-scope behavior, canonical content, phase status, acceptance status, or release/certification state.

For every material advance, update the relevant execution document and canonical handoff in the same work cycle; synchronize roadmap and machine state whenever phase, acceptance, evidence, integration scope, batch, or branch/checkpoint facts change.

## Mandatory phase-end regression

No phase may transition to `CLOSED`, and no subsequent phase may become `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded.

The machine contract keeps `phase_end_regression.candidate = one-immutable-sha`. Scoped Step checks never replace the Scientific Article phase-end regression; phase-end Linux uses `complete`.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement. Do not infer closure from naming, memory, historical intent, or partial evidence.
