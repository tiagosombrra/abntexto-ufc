# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 1 ACCEPTED / SCOPED LINUX ORCHESTRATION CURRENT

## Purpose

Implement and validate one canonical `scientific-article` profile on top of the corrected, visually accepted shared V3 foundation. This phase realizes the retained 18-rule source-backed article contract without forking cross-cutting infrastructure or weakening accepted non-article behavior.

Authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.

## Accepted entry evidence

| Entry requirement | Evidence | State |
|---|---|---|
| Regression Audit closed | green audit regression | PASS |
| Core Corrections closed | `5f67560a...`; Static `33982156041`; Linux `33982156042` | PASS |
| Reference PDF Validation closed | `b64074c...`; Static `33985595790`; Linux `33985595798` | PASS |
| Canonical shared PDF visually accepted | 55/55 pages, 0 unexplained visual FAIL | PASS |
| Article authority contract retained | 18 source-backed `article.*` rules | PASS |
| Shared librarian review state | 33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW | PASS / EXPLICIT AUTHORITY GAP |
| PR #285 integration | merged to `main` as `e6833ed5cf07aaf1021c690260cecfacec1a119a` | PASS |
| Temporary executors | none active | PASS |

## Step 1 — Profile and metadata surface — ACCEPTED

Technical implementation checkpoint: `b46ba2051f8c9c712a7b5d25748b81baa52b920a`.  
Synchronized acceptance checkpoint: `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`.

Acceptance evidence:

- Static `34001350884`: SUCCESS;
- full Linux `34001350953`: SUCCESS, `PASS=31 FAIL=0 SKIP=0`;
- `ARTICLE-PROFILE-EVIDENCE status=PASS engines=2 canonical_type=scientific-article metadata=submission-date,approval-date,article-author-note presentation_rules_promoted=0`;
- six accepted non-article profiles remained green.

Implemented Step 1 surface:

- one canonical runtime choice `type = scientific-article`;
- no compatibility alias;
- reuse `author`, `title` and `approval-date`;
- new article metadata only for `submission-date` and `article-author-note`;
- foreign-title semantics deliberately deferred to Step 3;
- dedicated profile/metadata compile evidence on pdfLaTeX + LuaLaTeX;
- no article presentation rule promoted merely by profile registration.

## Infrastructure checkpoint before Step 2

PR #285 is already merged. Before opening Step 2 runtime work, the repository is stabilizing bounded Linux orchestration on `ci/scoped-linux-integration` created from current `main`.

This is an infrastructure checkpoint, not an article normative step. It must:

- add named intermediate Linux suites and automatic changed-path inference;
- make documentation-only changes skip heavy Linux;
- fail unknown/shared/core/standards technical surfaces closed to `complete`;
- include executable `scientific-article-profile` plus `validator-source` in `article`;
- preserve `complete` as the only Linux scope accepted for phase-end regression;
- keep Static as the permanent contract guard;
- update `docs/LINUX-INTEGRATION-SCOPES.md`, roadmap, handoff and machine state in the same cycle.

Step 2 runtime must not be implemented on this infrastructure branch. After the orchestration PR merges, create `feat/v3-scientific-article` from updated `main`.

## Metadata decision

| Contract need | Current surface | Decision |
|---|---|---|
| Primary authorship | `author` | reuse |
| Primary title | `title` | reuse |
| Approval date | `approval-date` | reuse |
| Submission date | `submission-date` | article-required metadata added in Step 1 |
| Complementary author footnote | `article-author-note` | article-required metadata added in Step 1 |
| Foreign title | not yet bound | Step 3; do not infer from `title-variant` |
| Primary summary | document content route | Step 2 |
| Foreign summary | document content route | Step 3 optionality |

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no compatibility aliases.
- Preserve accepted non-article profiles and canonical academic-work PDF baseline.
- Reuse bibliography, citation, section, summary and object machinery rather than fork it.
- Do not change article rule IDs, authority, modality, expected values, locators or applicability without new current source evidence.
- Required, optional, recommended and conditional rules remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain a conditional applicability boundary.
- Shared mechanism reuse does not count as article proof.
- Item 33 remains fail-closed.
- Issue #18 remains a release blocker owned by Final Certification/Release.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate using Linux scope `complete`.

## Implementation sequence

| Step | Work | Current state | Acceptance |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| Infrastructure | Scoped Linux orchestration | **CURRENT** | dedicated PR from current `main`; Static + bounded `smoke` evidence; merge before Step 2 |
| 2 | Required article front block | NEXT | required title/authorship/date/summary elements have article-specific rendered evidence |
| 3 | Optional foreign elements | QUEUED | foreign title/summary may be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | QUEUED | required article structure and 12 pt/justified/2 cm/single-spaced body validated |
| 5 | Recommendations and conditional applicability | QUEUED | advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Next action

1. open the orchestration PR with this documentation/control synchronization;
2. push the technical scoped-Linux implementation as the next material advance;
3. verify Static and that the synchronize event selects bounded `smoke` rather than complete historical diff;
4. record accepted orchestration SHA/run IDs and merge it;
5. create `feat/v3-scientific-article` from updated `main`;
6. synchronize branch facts;
7. implement **Required article front block** with article-specific rendering/evidence for primary title, authorship metadata footnote, submission/approval dates and primary summary.
