# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. identify the actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md` and `docs/ROADMAP-V3.0.0.md`;
4. during **Scientific Article**, also read `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `standards/coverage-rules-article.json`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/V3-RELEASE-READINESS.md`, and `docs/ENGINEERING-LANGUAGE.md`;
5. reconcile Git facts, machine state, handoff, roadmap, article authority, proof state, Linux-scope state and release blockers before feature work.

Memory, prior chats, historical branches and old workflow names never override the current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Scientific Article** |
| Canonical base | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active branch / PR | `feat/v3-scientific-article` / #286 |
| Steps 1–4 | **ACCEPTED** |
| Step 5 implementation | `6507da00275d8a69093541d6e6cb119a1b6f6cb3` |
| Step 5 Linux | `34126602083` **PASS**, `SCOPE=complete PASS=36 FAIL=0 SKIP=0`; all six article gates and both recommendation scenarios passed |
| Step 5 Static | `34126602062` **FAIL** only on mixed orchestration + article scope inference |
| Current batch | **Step 5 — correct scoped orchestration inference and harden rendered keyword evidence** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

The Step 5 runtime/evidence surface is green under the complete Linux regression. The checkpoint is not accepted yet because the Static contract correctly found an independent orchestration defect: `tests/run.py` plus an article path incorrectly forced `complete` instead of selecting `article`. Fix the inference algorithm; do not weaken `tests/checks/linux_integration_suites.py`.

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — active, Step 5 correction/acceptance gate
5. Final Certification — queued
6. Release — queued

Do not create new opaque work identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Scientific Article rules

- One canonical type: `scientific-article`; no aliases.
- Preserve the retained 18-rule article source contract.
- Keep required, optional, recommended and required-when-applicable semantics distinct.
- Reuse shared bibliography, citation, section, object and summary mechanisms rather than fork them.
- Shared implementation is not article proof.
- Step 4 physical predicates remain accepted and must not be weakened.
- Step 5 recommendations remain advisory; short summaries, multiple summary paragraphs and fewer than three keywords must not become hard failures.
- Journal precedence remains `required-when-applicable`, `conditional-manual`, applicability `target-journal-submission`.
- Step 5 proof state remains unpromoted.
- Step 6 begins only after Step 5 acceptance is recorded.

## Linux scope rule

Orchestration-only changes select `smoke`. When orchestration files accompany recognized domain-specific technical files, orchestration paths are neutral for domain selection and the known domain suite must win. Unknown non-orchestration technical paths and force-complete surfaces still fail closed to `complete`.

## Engineering rules

- Project-owned technical surfaces are English.
- Preserve the accepted shared V3 public API unless current authority explicitly authorizes a change.
- Do not silently change normative IDs, expected values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only the encoded contract.
- Reviewer comments are evidence, not automatic normative authority.
- Do not weaken tests merely to recover green CI.
- Negative evidence must fail for the intended predicate.
- Recommended rules may influence defaults/documentation but must not become mandatory rejection predicates.
- Temporary executors must be removed before checkpoint acceptance.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, integration-scope behavior, canonical content, phase status, acceptance status, or release/certification state. Update the relevant execution document and canonical handoff in the same work cycle; synchronize roadmap and machine state whenever those facts change.

## Mandatory phase-end regression

No phase transitions to `CLOSED`, and no later phase becomes `ACTIVE`, until one immutable candidate SHA passes the complete relevant **phase-end regression** and the result is recorded. The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`. Scientific Article Step 8 requires `complete` Linux.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement. Do not infer closure from naming, memory, historical intent, or partial evidence.
