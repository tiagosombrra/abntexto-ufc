# V3 Scientific Article — Execution Plan

Updated: 2026-09-05  
Status: ACTIVE — STEP 1 ACCEPTED / REPOSITORY INTEGRATION NEXT

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

## Step 1 — Profile and metadata surface — ACCEPTED

Technical implementation checkpoint: `b46ba2051f8c9c712a7b5d25748b81baa52b920a`.
Synchronized acceptance checkpoint: `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`.

Acceptance evidence:

- Static contract `34001350884`: SUCCESS;
- full Linux integration `34001350953`: SUCCESS, `PASS=31 FAIL=0 SKIP=0`;
- article profile evidence: `ARTICLE-PROFILE-EVIDENCE status=PASS engines=2 canonical_type=scientific-article metadata=submission-date,approval-date,article-author-note presentation_rules_promoted=0`;
- all six accepted non-article profiles remained green in the full profile matrix.

Implemented changes:

- added the single canonical runtime choice `type = scientific-article` in `abntexto-ufc/core.def`;
- no article compatibility alias was added;
- reused existing generic metadata `author`, `title` and `approval-date`;
- added only the new required article metadata surfaces `submission-date` and `article-author-note`;
- left foreign-title semantics for the optional-foreign-elements step instead of silently repurposing `title-variant`;
- added `tests/checks/scientific_article_profile_contract.py` to protect canonical naming and metadata ownership;
- added a dedicated two-engine compile fixture/gate for profile selection and metadata round-trip;
- chained that bounded article gate from the existing profile-matrix integration so the six accepted non-article profiles remain exercised unchanged.

No article presentation rule or proof state is promoted by Step 1. `standards/coverage-rules-article.json` remains source-reviewed/manual or conditional-manual until rule-specific article evidence is implemented.

## Repository integration boundary

PR #285 carries the accepted shared foundation and Step 1 while `main` is still stale. The next operation is to merge that integration boundary, then create a fresh `feat/v3-scientific-article` branch from updated `main`. Step 2 runtime work must start on that fresh branch, not on historical `plan/v3-regression-reset` and not from stale `main`.

## Metadata decision

| Contract need | Current surface | Decision |
|---|---|---|
| Primary authorship | `author` | reuse |
| Primary title | `title` | reuse |
| Approval date | `approval-date` | reuse |
| Submission date | `submission-date` | new article-required core metadata |
| Complementary author footnote content | `article-author-note` | new article-required core metadata |
| Foreign title | not yet bound | defer to optional foreign elements; do not infer from `title-variant` |
| Primary/foreign summary content | document content route | implement in required front block / optional foreign elements |

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no compatibility aliases or retired Portuguese machine identifiers.
- Preserve all accepted non-article profiles and the shared academic-work reference-PDF baseline.
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
| 2 | Required article front block | NEXT AFTER PR #285 MERGE | Required title/authorship/date/summary elements have article-specific rendered evidence |
| 3 | Optional foreign elements | QUEUED | Foreign title/summary may be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | QUEUED | Required article structure and 12 pt/justified/2 cm/single-spaced body are validated |
| 5 | Recommendations and conditional applicability | QUEUED | Advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | Rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | Provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + full Linux + article-specific acceptance on one immutable SHA |

## Next action

1. merge PR #285 after the Step 1 acceptance synchronization passes its Static gate;
2. create `feat/v3-scientific-article` from updated `main`;
3. synchronize branch/control facts on that new branch;
4. implement **Required article front block** with article-specific rendering/evidence for primary title, authorship metadata footnote, submission/approval dates and primary summary without contaminating accepted academic-work front matter.
