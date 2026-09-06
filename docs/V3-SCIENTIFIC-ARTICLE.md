# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 4 IMPLEMENTED / ACCEPTANCE PENDING

## Purpose

Implement and validate one canonical `scientific-article` profile on top of the corrected, visually accepted shared V3 foundation. The phase realizes the retained 18-rule source-backed article contract without forking cross-cutting infrastructure or weakening accepted non-article behavior.

Authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.  
Linux orchestration contract: `docs/LINUX-INTEGRATION-SCOPES.md`.

## Accepted entry evidence

| Entry requirement | Evidence | State |
|---|---|---|
| Regression Audit | green audit regression | PASS |
| Core Corrections | `5f67560a...`; Static `33982156041`; Linux `33982156042` | PASS |
| Reference PDF Validation | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS | PASS |
| Article authority contract | exactly 18 retained `article.*` rules | PASS |
| Shared librarian review | 33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW | PASS / EXPLICIT AUTHORITY GAP |
| Shared foundation in `main` | `e6833ed5cf07aaf1021c690260cecfacec1a119a` | PASS |

## Step status

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | **ACCEPTED** | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign elements | **ACCEPTED** | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | **IMPLEMENTED — CI PENDING** | implementation `e5291137d4753b7d776916ca0f08c67929dbb76b`; synchronized acceptance checkpoint must pass Static + bounded Linux |
| 5 | Recommendations and conditional applicability | QUEUED | advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Step 3 acceptance — optional foreign elements

Step 3 owns `article.title.foreign.optional` and `article.summary.foreign.optional`. The synchronized acceptance checkpoint `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba` passed Static `34031144114` and Linux `34031144269`. All four title/summary optionality scenarios are accepted under both engines, the six non-article profiles remain separate, and missing synchronize endpoints fall back fail-closed to the full PR diff.

No article authority, modality or proof state was changed merely to obtain Step 3 acceptance.

## README user-guide correction

The README correction is accepted at `a99f1e19eac1294eac35fb1da85196a1b8295d1a`, with Static `34054110778` and Linux `34054110738` both successful. README remains end-user documentation; Scientific Article execution details remain in engineering documents, PR and Actions.

## Step 4 contract — textual structure and body typography

Step 4 owns:

- `article.introduction.required`;
- `article.development.required`;
- `article.final-considerations.required`;
- `article.references.required`;
- `article.body.typography`.

| Property | Required value |
|---|---|
| Font size | 12 pt |
| Alignment | justified |
| First-line indent | 2 cm |
| Line spacing | single |

The shared academic-work layout activates 12 pt, 2 cm indentation and 1.5 spacing. Step 4 therefore adds only a `scientific-article`-scoped begin-document override to single spacing while reaffirming 12 pt, 2 cm, zero extra paragraph spacing and justified alignment. No non-article route is modified.

## Step 4 implementation checkpoint

Implementation commit `e5291137d4753b7d776916ca0f08c67929dbb76b` completes the bounded implementation before documentation synchronization.

| Requirement | Implementation/evidence surface | State before CI |
|---|---|---|
| Article-only body activation | `abntexto-ufc/articles.def` checks canonical `scientific-article` before applying body typography | IMPLEMENTED |
| Required structure | positive fixture contains Introdução, Desenvolvimento, Considerações finais and Referências | IMPLEMENTED |
| 12 pt body | final-PDF checker measures controlled body typography runs | IMPLEMENTED |
| 2 cm first-line indent | checker compares paragraph start against same-page text-margin control | IMPLEMENTED |
| Justification | checker measures left continuation alignment and right extent of non-final natural lines | IMPLEMENTED |
| Single spacing | checker compares natural body-line gaps to same-document explicit `\singlesp` calibration | IMPLEMENTED |
| Negative structure | separate fixture omits Desenvolvimento; checker must reject for that reason | IMPLEMENTED |
| Step 2/3 regression boundary | obsolete “no AtBeginDocument before Step 4” guards replaced by positive profile-scoped Step 4 route checks | IMPLEMENTED |
| Coordinated runner | new `scientific-article-body` check registered in `tests/run.py` | IMPLEMENTED |
| Linux article suite | `scientific-article-body` added to `article`; static suite contract requires it | IMPLEMENTED |
| Proof-state promotion | none; retained article rules remain source-reviewed until later evidence-hardening Step 6 | PRESERVED |

## Acceptance gate for Step 4

The synchronized checkpoint containing `e5291137...` plus this documentation must pass:

1. Static contract, including Linux-suite registration and existing normative/identity/language guards;
2. bounded Linux `article` acceptance, exercising profile, front block, foreign elements and the new body gate;
3. two-engine positive final-PDF body evidence;
4. deterministic negative rejection for missing Desenvolvimento;
5. no regression in the six-profile non-article compatibility boundary when selected by scope;
6. no article authority/modality/proof-state promotion merely to obtain green CI.

Any failure is classified before changing runtime or tests. Step 5 does not begin until this gate is green and the result is recorded in a later documentation checkpoint.

## Scoped Linux integration

`article` now includes `validator-source`, `scientific-article-profile`, `scientific-article-front-block`, `scientific-article-foreign-elements` and `scientific-article-body`. `profiles` remains a separate six-profile compatibility suite.

A scoped green run never closes the Scientific Article phase. Step 8 still requires Static plus `complete` Linux on one immutable phase-end candidate.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no compatibility aliases.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain conditional.
- Shared implementation is not article proof.
- Do not weaken normative traceability, canonical identity or scope fail-closed behavior.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.
- Step 4 implementation: `e5291137d4753b7d776916ca0f08c67929dbb76b`.

Next: publish the synchronized Step 4 checkpoint, run Static plus bounded Linux, classify any failure fail-closed, and only after green acceptance advance documentation to Step 5.
