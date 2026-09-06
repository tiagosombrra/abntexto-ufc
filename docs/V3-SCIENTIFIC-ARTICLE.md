# V3 Scientific Article — Execution Plan

Updated: 2026-09-05  
Status: ACTIVE — STEP 2 IMPLEMENTED / CI PENDING AFTER CURRENCY RECONCILIATION

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

No article presentation rule or proof state was promoted by Step 1.

## Step 2 — Required article front block — IMPLEMENTED / CI PENDING

Implementation checkpoint: `90293af760c4063b02a16831196ec3d932f1471d`.

The bounded implementation adds `abntexto-ufc/articles.def` and loads it through `abntexto-ufc.cls`. The new public route is `\ufcPrintArticleFrontMatter{...}` and is valid only for `type=scientific-article`.

| Surface | Implemented behavior | Evidence boundary |
|---|---|---|
| Primary title | reuses `title`; 12 pt, centered, bold, uppercase and single-spaced | same-document PDF typography/centering calibration plus source guard |
| Primary authorship | reuses `author` | rendered article-specific marker |
| Authorship metadata note | uses `article-author-note` | rendered through an actual footnote; PDF bottom-region evidence |
| Submission date | uses `submission-date` | rendered in article front block |
| Approval date | reuses `approval-date` | rendered in article front block |
| Primary summary | required argument to `\ufcPrintArticleFrontMatter` | rendered `Resumo:` surface with controlled marker |
| Foreign title/summary | deliberately absent | Step 3 remains the only place to implement optional foreign elements |
| Article body typography | deliberately not activated | Step 4 remains authoritative |
| Recommendations | not converted into hard failures | no summary word-count/keyword-count/paragraph-count enforcement |

Article-specific evidence added:

- `tests/documents/scientific-article-front-block.tex`;
- `tests/checks/scientific_article_front_block.py`;
- `tests/integration/scientific-article-front-block.sh`;
- the existing `scientific-article-profile.sh` now invokes the front-block gate, so the permanent profile matrix exercises the article front block under pdfLaTeX and LuaLaTeX.

Expected structured evidence:

`ARTICLE-FRONT-BLOCK-EVIDENCE status=PASS engines=2 rules=title-required,authorship-required,summary-required,dates-required,title-typography,authorship-footnote presentation_rules_promoted=0 optional_foreign_elements_promoted=0 recommendations_promoted=0`

## Step 2 first gate classification

The first synchronized Step 2 checkpoint `768d355eda11f47b4cebbb6864247e9fc2aa728f` was rejected by Static `34003576066`. The failure was:

`Normative currency failed: scientific-article runtime appeared before foundation activation`.

Classification: **stale control-policy coupling**, not article runtime, source-authority or presentation failure. `tests/checks/normative_currency.py` still encoded the pre-activation invariant that `abntexto-ufc/articles.def` must never exist, even though Regression Audit, Core Corrections, Reference PDF Validation and Scientific Article Step 1 had already authorized the active Scientific Article phase.

Correction checkpoint: `e29501bd8cae98d6442f08e17bc3a54892fc7e0d`.

The correction:

- keeps the same current article authority sources (`abnt-nbr-6022-2018`, `ufc-guia-artigos-2022`);
- records article runtime as active only in `scientific-article`, `final-certification` or `release` phases;
- binds activation to the retained source-contract SHA, accepted shared-foundation `main` SHA and Step 1 acceptance SHA;
- preserves article proof state as manual/conditional-manual;
- does not weaken technical-edition precedence or alter any article rule predicate.

`docs/NORMATIVE-CURRENCY.md` and `standards/version-policy.json` were updated in the same correction cycle.

### Step 2 acceptance gate

Step 2 remains **IMPLEMENTED / CI PENDING** until a post-reconciliation synchronized checkpoint passes:

1. Static contract;
2. full Linux integration;
3. canonical article profile routing on both engines;
4. rendered article front-block evidence on both engines;
5. unchanged six-profile non-article matrix;
6. no optional/recommended/conditional modality drift.

No article rule in `standards/coverage-rules-article.json` is promoted merely because this implementation or its targeted evidence exists. Proof-state promotion remains a later explicit evidence-hardening decision.

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
| 2 | Required article front block | **IMPLEMENTED — CI PENDING AFTER CURRENCY RECONCILIATION** | implementation `90293af...`; currency fix `e29501b...`; post-fix synchronized Static/full Linux required |
| 3 | Optional foreign elements | QUEUED | Foreign title/summary may be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | QUEUED | Required article structure and 12 pt/justified/2 cm/single-spaced body are validated |
| 5 | Recommendations and conditional applicability | QUEUED | Advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | Rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | Provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + full Linux + article-specific acceptance on one immutable SHA |

## Current branch and next action

- Canonical base: `main` with merge `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.
- Historical integration branch `plan/v3-regression-reset`: no new work.

Next: run the post-reconciliation Static and full Linux gates, classify any new failure without weakening tests, and only after both are green mark Step 2 accepted and activate Step 3.
