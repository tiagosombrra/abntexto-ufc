# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — ORCHESTRATION ACCEPTED / FEATURE PR PRESERVED

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

## Step 1 — Profile and metadata surface — ACCEPTED ON MAIN

Technical implementation checkpoint: `b46ba2051f8c9c712a7b5d25748b81baa52b920a`.  
Synchronized acceptance checkpoint: `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`.

Acceptance evidence:

- Static `34001350884`: SUCCESS;
- full Linux `34001350953`: SUCCESS, `PASS=31 FAIL=0 SKIP=0`;
- `ARTICLE-PROFILE-EVIDENCE status=PASS engines=2 canonical_type=scientific-article metadata=submission-date,approval-date,article-author-note presentation_rules_promoted=0`;
- six accepted non-article profiles remained green.

## Infrastructure checkpoint — ACCEPTED

PR #287 / `ci/scoped-linux-integration` has accepted technical checkpoint `47ac2e27c5c2f6797269ccc4e1c07caafea1c643`:

- Static `34139608322`: SUCCESS;
- Linux `34139608364`: SUCCESS, `SCOPE=smoke PASS=4 FAIL=0 SKIP=0`;
- Static `LINUX-SUITE-EVIDENCE` includes `runner_file_spec_import=true`;
- automatic synchronize inference selected `smoke` rather than replaying the full historical PR diff.

The preceding `d089215e...` checkpoint is retained as rejected evidence: both Static `34137588226` and Linux `34137588237` found the same location-dependent file-spec import defect. The fix changes no article rule, runtime behavior, normative predicate or suite membership.

PR #287 should merge before article feature work resumes.

## Existing PR #286 — preserved article work

PR #286 / `feat/v3-scientific-article` contains later Scientific Article work beyond the Step 1 foundation. That history is **not discarded**. It remains paused for control-plane advancement until PR #287 merges.

After PR #287 merges:

1. reconcile the existing PR #286 branch with updated `main`;
2. preserve its Step 2–4 implementation/history;
3. obtain executable `article`-scope evidence for the pending Step 4 structural-checker state after reconciliation;
4. only then advance the accepted article step and continue Step 5.

A documentation-only green workflow on PR #286 does not substitute for executable article evidence.

## Metadata decision

| Contract need | Current surface | Decision |
|---|---|---|
| Primary authorship | `author` | reuse |
| Primary title | `title` | reuse |
| Approval date | `approval-date` | reuse |
| Submission date | `submission-date` | article metadata added in Step 1 |
| Complementary author footnote | `article-author-note` | article metadata added in Step 1 |
| Foreign title | preserved article branch implementation | retain optional semantics; confirm after reconciliation |
| Primary summary | preserved article branch implementation | retain required semantics; confirm after reconciliation |
| Foreign summary | preserved article branch implementation | retain independent optionality; confirm after reconciliation |

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
| 1 | Profile and metadata surface | **ACCEPTED ON MAIN** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| Infrastructure | Scoped Linux orchestration | **ACCEPTED — PR #287 MERGE NEXT** | `47ac2e27...`; Static `34139608322`; Linux `34139608364` |
| 2 | Required article front block | **PRESERVED IN PR #286** | revalidate after branch reconciliation |
| 3 | Optional foreign elements | **PRESERVED IN PR #286** | revalidate independent optionality after reconciliation |
| 4 | Textual structure and body typography | **PRESERVED / EXECUTABLE NEGATIVE CHECK PENDING ACCEPTANCE** | article-scope run after reconciliation must exercise structural checker and physical body evidence |
| 5 | Recommendations and conditional applicability | BLOCKED | start only after Step 4 is accepted on reconciled branch |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Next action

1. merge PR #287 after the acceptance-document synchronization remains Static-clean;
2. reconcile existing PR #286 with updated `main`;
3. run executable `article`-scope validation for the pending Step 4 state;
4. synchronize accepted step/proof state;
5. continue Step 5 without replaying or discarding already-preserved work.
