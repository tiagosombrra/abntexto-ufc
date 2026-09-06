# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 4 TEXTUAL STRUCTURE AND BODY TYPOGRAPHY

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
| 4 | Textual structure and body typography | **ACTIVE** | required structure + 12 pt/justified/2 cm/single-spaced body evidence |
| 5 | Recommendations and conditional applicability | QUEUED | advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Step 3 acceptance — optional foreign elements

Step 3 owns `article.title.foreign.optional` and `article.summary.foreign.optional`. The synchronized acceptance checkpoint `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba` passed Static `34031144114` and Linux `34031144269`. All four title/summary optionality scenarios are accepted under both engines, the six non-article profiles remain separate, and missing synchronize endpoints fall back fail-closed to the full PR diff.

No article authority, modality or proof state was changed merely to obtain Step 3 acceptance.

## README user-guide correction

The README correction is accepted at `a99f1e19eac1294eac35fb1da85196a1b8295d1a`, with Static `34054110778` and Linux `34054110738` both successful.

The first rewrite `3e3ece5...` was rejected because it reintroduced three unclassified references to the retired class identity while explaining the stable release. The accepted correction keeps the v2.1.0 download and usage path without weakening `canonical_identity.py`.

README remains end-user documentation. Scientific Article execution details remain in this plan, handoff, roadmap, machine state, PR and Actions.

## Step 4 contract — textual structure and body typography

Rules owned by this Step:

- `article.introduction.required`;
- `article.development.required`;
- `article.final-considerations.required`;
- `article.references.required`;
- `article.body.typography`.

Accepted presentation values for the article body are:

| Property | Required value |
|---|---|
| Font size | 12 pt |
| Alignment | justified |
| First-line indent | 2 cm |
| Line spacing | single |

The shared academic-work layout currently activates 12 pt, 2 cm indentation and 1.5 spacing globally. Therefore the article requires an explicit profile-specific override to single spacing (while preserving the other accepted properties) and article-specific physical evidence. Reuse of shared layout, section and bibliography mechanisms is preferred but is not itself proof.

### Step 4 implementation sequence

| Order | Work | Acceptance intent |
|---:|---|---|
| 1 | Inspect `articles.def`, shared layout/section hooks and PDF checker patterns. | Avoid duplicate/forked infrastructure. |
| 2 | Define the smallest `scientific-article`-only body activation. | No cross-profile drift. |
| 3 | Add a controlled article fixture containing introduction, development, final considerations and references. | Positive structural evidence. |
| 4 | Measure 12 pt, justification, 2 cm indent and single spacing from the rendered article PDF. | Physical presentation evidence. |
| 5 | Add a safe negative structural case that the checker deterministically rejects. | Fail-closed evidence. |
| 6 | Register the new Step 4 executable gate in `tests/run.py` and in the `article` Linux suite in the same material advance. | Scoped CI cannot omit Step 4. |
| 7 | Replace the obsolete pre-Step4 front-block guard with the new accepted Step4 boundary rather than simply deleting coverage. | Semantic transition without test weakening. |
| 8 | Synchronize this plan, handoff, roadmap and machine state. | Documentation matches code/evidence. |
| 9 | Require Static and bounded article/profile Linux PASS on one synchronized Step 4 checkpoint. | Step 4 acceptance. |

## Scoped Linux integration

Intermediate article work uses bounded scope where safe. `article` currently includes `validator-source`, `scientific-article-profile`, `scientific-article-front-block` and `scientific-article-foreign-elements`. The Step 4 implementation must add its new executable gate to this list in the same material advance. `profiles` remains a separate six-profile compatibility suite.

A complete repository run is not required for intermediate Step acceptance. The **Scientific Article phase-end regression** remains stricter: `complete` Linux on one immutable candidate, plus Static and all article-specific acceptance evidence.

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

Next: implement and validate the bounded Step 4 article body/structure evidence, then only after Static plus bounded Linux acceptance advance to Step 5.
