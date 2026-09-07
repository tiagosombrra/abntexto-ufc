# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 4 CORRECTION IMPLEMENTED / ACCEPTANCE RERUN PENDING

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
| 4 | Textual structure and body typography | **CORRECTION IMPLEMENTED — CI PENDING** | rejected synchronized checkpoint `8b52ee4...`: Static `34058435312` PASS; Linux `34058435311` FAIL; current synchronized correction moves article body activation to `begindocument/end` |
| 5 | Recommendations and conditional applicability | BLOCKED | begins only after Step 4 acceptance is recorded |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Step 4 contract — textual structure and body typography

Step 4 owns `article.introduction.required`, `article.development.required`, `article.final-considerations.required`, `article.references.required`, and `article.body.typography`.

| Property | Required value |
|---|---|
| Font size | 12 pt |
| Alignment | justified |
| First-line indent | 2 cm |
| Line spacing | single |

## Rejected Step 4 checkpoint

The synchronized checkpoint `8b52ee4b36b23868fecce9bbe9b843f689ccc01e` produced a useful fail-closed result:

| Gate | Result |
|---|---|
| Static `34058435312` | PASS |
| Linux `34058435311` | FAIL — bounded `article` scope, PASS=4 FAIL=1 |
| `validator-source` | PASS |
| `scientific-article-profile` | PASS |
| `scientific-article-front-block` | PASS |
| `scientific-article-foreign-elements` | PASS |
| `scientific-article-body` | FAIL |

The body checker measured `20.700 pt` between controlled article body lines while the same-document 12 pt `\singlesp` calibration measured `13.800 pt` (`delta=6.900 pt`). The article therefore retained the shared academic-work 1.5 spacing. This is a runtime initialization-order defect. It is not accepted as presentation and the checker is not weakened.

## Step 4 correction

The shared layout registers its academic-work body contract at begin-document time. A separate generic `\AtBeginDocument` registration in `articles.def` was not a sufficiently robust ordering boundary. The correction keeps the runtime profile predicate but schedules the article-specific override at the end of begin-document initialization:

`\AddToHook{begindocument/end}{\ufc_article_apply_body_typography:}`

| Requirement | Correction/evidence surface | State |
|---|---|---|
| Article-only body activation | `articles.def` still checks canonical `scientific-article` | PRESERVED |
| Ordering | activation moved to `begindocument/end` after shared layout initialization | CORRECTED |
| 12 pt body | existing final-PDF checker | UNCHANGED |
| 2 cm first-line indent | existing physical checker | UNCHANGED |
| Justification | existing physical checker | UNCHANGED |
| Single spacing | must now match `13.800 pt` same-document calibration, not `20.700 pt` | RERUN REQUIRED |
| Negative structure | missing Desenvolvimento fixture/checker | UNCHANGED |
| Non-article boundary | no intended change to six non-article profiles | PRESERVED |
| Proof-state promotion | none; Step 6 still owns promotion | PRESERVED |

The exact correction SHA is recorded only after the synchronized runtime/documentation commit is created.

## Acceptance gate for Step 4 correction

1. Static contract passes on the corrected synchronized checkpoint;
2. bounded Linux `article` scope passes all five checks;
3. body evidence measures 12 pt, justified alignment, 2 cm first-line indent and single spacing under pdfLaTeX and LuaLaTeX;
4. missing-development negative fixture is rejected for the intended structural reason;
5. the article-only predicate remains in place and no non-article runtime is intentionally changed;
6. article authority, modality and proof state are not strengthened merely to obtain green CI.

Step 5 does not begin until these results are recorded in a later documentation checkpoint.

## Scoped Linux integration

`article` includes `validator-source`, `scientific-article-profile`, `scientific-article-front-block`, `scientific-article-foreign-elements` and `scientific-article-body`. `profiles` remains a separate six-profile compatibility suite.

A scoped green run never closes the Scientific Article phase. Step 8 still requires Static plus `complete` Linux on one immutable phase-end candidate.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no compatibility aliases.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain conditional.
- Shared implementation is not article proof.
- Do not weaken the spacing checker after a real runtime defect.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.
- Step 4 implementation: `e5291137d4753b7d776916ca0f08c67929dbb76b`.
- Rejected synchronized checkpoint: `8b52ee4b36b23868fecce9bbe9b843f689ccc01e`.

Next: publish the synchronized body-spacing correction checkpoint, run Static plus bounded Linux, classify any failure fail-closed, and only after green acceptance advance documentation to Step 5.
