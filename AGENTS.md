# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. identify the actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md` and `docs/ROADMAP-V3.0.0.md`;
4. during **Scientific Article**, also read `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `standards/coverage-rules-article.json`, `standards/article-evidence-map.json`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/V3-RELEASE-READINESS.md`, and `docs/ENGINEERING-LANGUAGE.md`;
5. reconcile Git facts, machine state, handoff, roadmap, article authority, evidence map, Linux-scope state and release blockers before feature work.

Memory, prior chats, historical branches and old workflow names never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Scientific Article** |
| Canonical `main` | `fbf7cc4839ce318024a7d1ed517dd50fab5773ac` |
| Active branch / PR | `feat/v3-scientific-article` / #286 |
| Current-main reconciliation merge | `85cf22b6fe5d117bb2611a2865911e0d20a19363` |
| Steps 1–5 | **ACCEPTED** |
| Step 5 checkpoint | `55fa1c8dc1b503c119d564950d04141cf45ad345`; Static `34132291198`; Linux `34132291304` |
| Step 6 | **IMPLEMENTED — ACCEPTANCE CI PENDING** |
| Step 6 contract | exact 18-rule `standards/article-evidence-map.json` + `tests/checks/scientific_article_evidence_map.py` |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

The root README and canonical control documents on `main` were reconciled through PR #288, merged as `fbf7cc4...`. The article branch then recorded that current-main ancestry in `85cf22b...` before Step 6 implementation.

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — active, Step 6 acceptance pending
5. Final Certification — queued
6. Release — queued

## Scientific Article evidence rules

- Preserve exactly the retained 18-rule source contract.
- `standards/article-evidence-map.json` records current article-specific evidence ownership without rewriting source requirement text, normativity, locators or applicability.
- Executable support is not equivalent to a normative rule becoming `PROVEN`.
- Step 6 currently promotes **zero** validation modes; the map is deliberately conservative.
- Optional foreign title/summary remain optional and use present/absent matrix evidence.
- The four recommendation rules remain manual, advisory and non-enforcing.
- Journal precedence remains `required-when-applicable`, `conditional-manual`, applicability `target-journal-submission`, with no generic executable owner.
- Shared implementation reuse never counts as article-specific proof by itself.
- Step 7 starts only after Step 6 Static and required Linux scope pass on the synchronized technical checkpoint.

## Linux scope rule

Scoped runs are valid intermediate evidence only. Scientific Article Step 8 requires `complete` Linux on one immutable candidate, plus accepted canonical article PDF evidence.

## Engineering rules

- Project-owned technical surfaces are English.
- Preserve the accepted shared V3 public API unless current authority explicitly authorizes a change.
- Do not silently change normative IDs, values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only the encoded contract.
- Reviewer comments are evidence, not automatic normative authority.
- Do not weaken tests merely to recover green CI.
- Negative evidence must fail for the intended predicate.
- Recommended rules must not become rejection predicates.
- Temporary executors must be removed before checkpoint acceptance.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, integration-scope behavior, canonical content, phase status, acceptance status, branch/base reconciliation, or release/certification state. Update the relevant execution documents and handoff in the same work cycle; synchronize roadmap and machine state whenever those facts change.

## Mandatory phase-end regression

No phase closes until one immutable candidate SHA passes the complete phase-end regression and the result is recorded. The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`. Scientific Article Step 8 requires complete Linux.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement.
