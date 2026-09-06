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

Step 3 owns:

- `article.title.foreign.optional`;
- `article.summary.foreign.optional`.

Runtime checkpoint `81e08321222efb03626ac421fc645bd66edd5ae8` provides the explicit article-only route:

`\ufcPrintArticleForeignElements{foreign-title}{foreign-summary}`

The arguments are independently blank-safe and do not reuse shared `title-variant` semantics.

The synchronized acceptance checkpoint is `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba`:

| Gate | Result |
|---|---|
| Static | `34031144114` — SUCCESS |
| Linux | `34031144269` — SUCCESS |
| Foreign title absent / summary absent | PASS |
| Foreign title present / summary absent | PASS |
| Foreign title absent / summary present | PASS |
| Foreign title present / summary present | PASS |
| Engines | pdfLaTeX and LuaLaTeX evidence accepted |
| Non-article profile boundary | exactly six non-article profiles retained; article excluded from compatibility matrix |
| Scope robustness | missing synchronize endpoint falls back fail-closed to full PR diff |

Earlier Step 3 failures are retained as history in Git/Actions but no longer represent the current execution state. No article rule authority, modality or proof state was changed merely to obtain Step 3 acceptance.

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

Step 4 must not infer compliance from the existing academic-work body. Reuse of shared section, bibliography and paragraph mechanisms is preferred, but the article profile needs article-specific executable evidence proving the required structure and typography.

### Step 4 implementation sequence

| Order | Work | Acceptance intent |
|---:|---|---|
| 1 | Inspect `articles.def`, shared layout/section hooks and current article fixtures before changing runtime. | Avoid duplicate/forked infrastructure. |
| 2 | Define the smallest article-only activation needed for body presentation. | No cross-profile drift. |
| 3 | Add a controlled article fixture containing introduction, development, final considerations and references. | Positive structural evidence. |
| 4 | Measure 12 pt, justification, 2 cm indent and single spacing from the rendered article PDF. | Physical presentation evidence. |
| 5 | Add a safe negative structural/typographic case where the validator can deterministically reject a violation. | Fail-closed evidence. |
| 6 | Register the new Step 4 executable gate in the `article` Linux scope in the same material advance. | Scoped CI cannot omit Step 4. |
| 7 | Synchronize this plan, handoff, roadmap and machine state. | Documentation matches code/evidence. |
| 8 | Require Static and bounded article/profile Linux PASS on one synchronized Step 4 checkpoint. | Step 4 acceptance. |

## Scoped Linux integration

Intermediate article work uses bounded scope where safe. `article` currently includes:

- `validator-source`;
- `scientific-article-profile`;
- `scientific-article-front-block`;
- `scientific-article-foreign-elements`.

The Step 4 implementation must add its new executable gate to this list in the same material advance. `profiles` remains a separate six-profile compatibility suite. Multiple applicable domains run as a deduplicated union.

A complete repository run is not required for intermediate Step acceptance. The **Scientific Article phase-end regression** remains stricter: `complete` Linux on one immutable candidate, plus Static and all article-specific acceptance evidence.

## README boundary and current correction

The root `README.md` is end-user documentation. It should teach users how to obtain and use the stable release, while detailed Scientific Article execution state remains in this file, the handoff, roadmap, machine state, PR and Actions. Until v3.0.0 is released, the README must not present this in-progress article profile as stable functionality.

README checkpoint `3e3ece5a3607303dd31aee35c67ce4140fb90d94` was rejected by Static `34053874788` because stable-release explanation reintroduced three unclassified references to the retired class identity. Linux `34053874750` succeeded for that documentation-only checkpoint. The correction removes the retired identity from active README text while preserving the stable v2.1.0 download and usage path. `canonical_identity.py` remains unchanged.

This README correction does not alter Step 4 runtime, authority, modality or proof state.

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

Next: validate the corrected user-facing README under Static, then inspect the current article/shared layout implementation, design the bounded Step 4 fixture/checker/runtime activation, synchronize its new executable gate with `article` scope, and require Static plus bounded Linux acceptance before advancing to Step 5.
