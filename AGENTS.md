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
| Steps 1–4 | **ACCEPTED** |
| Step 4 accepted checkpoint | `005956bd615042a12fb0393fddd4941b635f6ce3`; Static `34119007413` PASS; Linux `34119007425` PASS, `SCOPE=article PASS=5 FAIL=0 SKIP=0` |
| Step 4 body evidence | pdfLaTeX and LuaLaTeX: 12 pt, justified, 2 cm first-line indent, `13.800 pt` single-spacing calibration |
| Step 4 negative evidence | missing Development rejected by heading-based structural predicate; adversarial prose token no longer satisfies the requirement |
| Current batch | **Step 5 — recommendations and conditional applicability** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

Step 4 is closed. The accepted runtime uses supported `\singlesp` plus the article-only `cmd/textual/after` route; physical evidence proves the body contract under both engines. The structure checker requires rendered headings rather than arbitrary prose tokens, and the negative fixture is rejected for the intended missing-Development condition.

Step 5 owns modality preservation for the retained recommendation and conditional rules. It must prove that recommended values remain advisory rather than compilation/validation requirements and that journal-specific precedence remains conditional/manual when a target journal applies.

## Readable phase model

1. **Regression Audit** — closed
2. **Core Corrections** — closed
3. **Reference PDF Validation** — closed
4. **Scientific Article** — active, Step 5
5. **Final Certification** — queued
6. **Release** — queued

Do not create new opaque work identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Scientific Article rules

- One canonical type: `scientific-article`; no aliases.
- Preserve the retained 18-rule article source contract.
- Keep required, optional, recommended and required-when-applicable semantics distinct.
- Reuse shared bibliography, citation, section, object and summary mechanisms rather than fork them.
- Shared implementation is not article proof.
- Step 4 body contract is accepted at `005956bd...`; do not weaken its physical predicates.
- Step 5 recommendations must remain advisory: author alignment, 150–250-word summary interval, minimum three keywords and single-paragraph summary must not become hard compile/validation failures.
- Journal instructions remain `required-when-applicable` and conditional-manual; the generic UFC profile is a fallback, not proof of compliance with a specific journal.
- Step 6 owns later proof-state hardening/promotion.

## Engineering rules

- Project-owned technical surfaces are English.
- Preserve the accepted shared V3 public API unless current authority explicitly authorizes change.
- Do not silently change normative IDs, expected values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only the contract encoded by that test.
- Reviewer comments are evidence, not automatic normative authority.
- Do not weaken tests to recover green CI.
- Negative evidence must fail for the intended predicate.
- Recommended rules may influence defaults/documentation but must not be converted into mandatory rejection predicates.
- Conditional journal rules require applicability context; do not hard-code one journal into the generic UFC profile.
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

The machine contract keeps `phase_end_regression.candidate = one-immutable-sha`. Scoped Step checks never replace the Scientific Article phase-end regression; Step 8 requires `complete` Linux.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement. Do not infer closure from naming, memory, historical intent, or partial evidence.
