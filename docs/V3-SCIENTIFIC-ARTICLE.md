# V3 Scientific Article — Execution Plan

Updated: 2026-09-05  
Status: ACTIVE — STEP 1 ACCEPTED / REQUIRED ARTICLE FRONT BLOCK ACTIVE

## Purpose

Implement and validate one canonical `scientific-article` profile on top of the corrected, visually accepted shared V3 foundation. This phase realizes the retained 18-rule source-backed article contract without forking cross-cutting infrastructure or weakening accepted non-article behavior.

Authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.

## Accepted entry evidence

| Entry requirement | Evidence | State |
|---|---|---|
| Regression Audit closed | `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2` + green audit regression | PASS |
| Core Corrections closed | `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Static `33982156041`; Linux `33982156042` | PASS |
| Reference PDF Validation closed | `b64074c64941895f97fbe0f795ce826c798d17ce`; Static `33985595790`; Linux `33985595798` | PASS |
| Canonical shared PDF visually accepted | 55/55 pages, 0 unexplained visual FAIL | PASS |
| Article authority contract retained | 18 source-backed `article.*` rules | PASS |
| Shared librarian review state | 33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW | PASS / EXPLICIT AUTHORITY GAP |
| Temporary executors | none active | PASS |
| Shared foundation integrated into canonical main | PR #285 squash merge `e6833ed5cf07aaf1021c690260cecfacec1a119a` | PASS |

## Step 1 — Profile and metadata surface — ACCEPTED

Technical implementation checkpoint: `b46ba2051f8c9c712a7b5d25748b81baa52b920a`.
Synchronized acceptance checkpoint: `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`.

Acceptance evidence:

- Static contract `34001350884`: SUCCESS;
- full Linux integration `34001350953`: SUCCESS, `PASS=31 FAIL=0 SKIP=0`;
- article profile evidence: `ARTICLE-PROFILE-EVIDENCE status=PASS engines=2 canonical_type=scientific-article metadata=submission-date,approval-date,article-author-note presentation_rules_promoted=0`;
- all six accepted non-article profiles remained green in the full profile matrix.

Implemented changes:

- single canonical runtime choice `type = scientific-article`;
- no article compatibility aliases;
- existing generic metadata `author`, `title` and `approval-date` reused;
- only new article metadata surfaces `submission-date` and `article-author-note` added;
- foreign-title semantics deliberately deferred rather than silently repurposing `title-variant`;
- static canonical-name/metadata-ownership contract added;
- dedicated pdfLaTeX + LuaLaTeX profile/metadata compile evidence added;
- non-article profile matrix preserved.

No article presentation rule or proof state is promoted by Step 1. `standards/coverage-rules-article.json` remains source-reviewed/manual or conditional-manual until rule-specific article evidence is implemented.

## Step 2 — Required article front block — ACTIVE

Work now occurs on `feat/v3-scientific-article`, created from canonical `main` after PR #285.

Required implementation scope is bounded to source-backed article presentation:

| Surface | Requirement for this step | Evidence requirement |
|---|---|---|
| Primary title | render through the scientific-article route with the contract-prescribed presentation | article-specific final-PDF/source evidence |
| Authorship metadata note | render `article-author-note` as the article authorship/complementary-information note required by the retained contract | positive rendered evidence; no leakage into non-article profiles |
| Submission date | render `submission-date` in the required article front block | positive rendered evidence |
| Approval date | reuse `approval-date` and render it in the article front block | positive rendered evidence |
| Primary summary | provide the required vernacular summary surface through article-specific presentation while reusing shared summary machinery where semantically valid | positive rendered evidence; recommended length/keyword properties remain advisory unless contract modality says otherwise |

This step must not:

- alter accepted academic-work cover/title/approval pages;
- make a foreign title or foreign summary mandatory;
- promote recommended summary length, keyword count, authorship alignment, or paragraph-count guidance into hard compilation failures unless the retained rule modality explicitly requires it;
- fork citation, bibliography, section, summary or object engines solely for the article profile;
- promote proof state before article-specific evidence exists.

## Metadata decision

| Contract need | Current surface | Decision |
|---|---|---|
| Primary authorship | `author` | reuse |
| Primary title | `title` | reuse |
| Approval date | `approval-date` | reuse |
| Submission date | `submission-date` | article-specific core metadata |
| Complementary author note | `article-author-note` | article-specific core metadata |
| Foreign title | not yet bound | defer to optional foreign elements; do not infer from `title-variant` |
| Primary/foreign summary | document content/shared summary primitives where semantically valid | primary in Step 2; foreign optional in Step 3 |

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no compatibility aliases or retired Portuguese machine identifiers.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse bibliography, citation, section, summary and object machinery rather than fork it.
- Do not change article rule IDs, authority, modality, expected values, locators or applicability without new current source evidence and a separately documented source correction.
- Required, optional, recommended and conditional rules remain distinguishable in runtime and evidence.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain a conditional applicability boundary.
- Item 33 of the librarian review remains fail-closed.
- Issue #18 is a v3 release blocker owned by Final Certification/Release, not a reason to alter article normative semantics.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Implementation sequence

| Step | Work | Current state | Acceptance |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953`, 31/31 PASS |
| 2 | Required article front block | **ACTIVE** | Required title/authorship/date/primary-summary elements have article-specific rendered evidence and non-article regressions remain green |
| 3 | Optional foreign elements | QUEUED | Foreign title/summary may be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | QUEUED | Required article structure and 12 pt/justified/2 cm/single-spaced body are validated |
| 5 | Recommendations and conditional applicability | QUEUED | Advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | Rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | Provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + full Linux + article-specific acceptance on one immutable SHA |

## Current branch and next action

- Canonical base: `main` with merge `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Historical integration branch `plan/v3-regression-reset`: no new work.

Next: inspect the retained article rule contract for the exact Step 2 presentation predicates, implement only those predicates, add rule-specific positive evidence, synchronize all control documents, then run Static and full Linux before marking Step 2 accepted.
