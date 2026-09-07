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
| Steps 1–5 | **ACCEPTED** |
| Step 5 acceptance checkpoint | `55fa1c8dc1b503c119d564950d04141cf45ad345` |
| Step 5 acceptance Static | `34132291198` **PASS** |
| Step 5 acceptance Linux | `34132291304` **PASS**, bounded `article` scope with all six first-class article checks green |
| Step 5 recommendation evidence | both engines and both controlled scenarios passed; 3/3 recommended keyword sentinels and outside-recommendation sentinel rendered; recommendations remained non-enforcing; journal precedence remained conditional-manual; `proof_state_promoted=0` |
| Current batch | **Step 6 — evidence hardening and truthful article-specific proof-state mapping** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

Step 5 is closed. The shortened controlled sentinels passed under pdfLaTeX and LuaLaTeX without article runtime or normative changes. Step 6 must now classify article-specific evidence rule by rule and may promote proof state only where an article-specific executable predicate actually supports the rule.

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — active, Step 6 evidence hardening
5. Final Certification — queued
6. Release — queued

Do not create new opaque work identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Scientific Article rules

- One canonical type: `scientific-article`; no aliases.
- Preserve the retained 18-rule article source contract.
- Keep required, optional, recommended and required-when-applicable semantics distinct.
- Reuse shared bibliography, citation, section, object and summary mechanisms rather than fork them.
- Shared implementation is not article proof.
- Steps 1–5 are accepted and their executable predicates must not be weakened.
- Recommended rules remain advisory; positive recommendation scenarios are evidence of supported defaults, not rejection predicates.
- Journal precedence remains `required-when-applicable`, `conditional-manual`, applicability `target-journal-submission`.
- Step 5 proof state remains unpromoted.
- Step 6 may promote only rules with direct article-specific evidence and must leave unsupported or conditional rules manual/conditional-manual.
- Step 7 begins only after Step 6 evidence-state changes are accepted and documented.

## Linux scope rule

Orchestration-only changes select `smoke`. When orchestration files accompany recognized domain-specific technical files, orchestration paths are neutral for domain selection and the known domain suite wins. Unknown non-orchestration technical paths and force-complete surfaces still fail closed to `complete`.

This behavior is accepted by Static `34129625390` and was reconfirmed by Step 5 acceptance Linux `34132291304`, which selected the bounded `article` suite and passed all six article checks.

## Engineering rules

- Project-owned technical surfaces are English.
- Preserve the accepted shared V3 public API unless current authority explicitly authorizes a change.
- Do not silently change normative IDs, expected values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only the encoded contract.
- Reviewer comments are evidence, not automatic normative authority.
- Do not weaken tests merely to recover green CI.
- Negative evidence must fail for the intended predicate.
- Recommended rules may influence defaults/documentation but must not become mandatory rejection predicates.
- Evidence sentinels should be short enough to survive deterministic PDF text extraction; a sentinel/extractor failure is not by itself evidence of a runtime normative defect.
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
