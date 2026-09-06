# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 1 ACCEPTED / SCOPED LINUX ORCHESTRATION CHECKPOINT

## Purpose

Implement and validate one canonical `scientific-article` profile on top of the corrected, visually accepted shared V3 foundation. This phase realizes the retained 18-rule source-backed article contract without forking cross-cutting infrastructure or weakening accepted non-article behavior.

Authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.  
Linux orchestration contract: `docs/LINUX-INTEGRATION-SCOPES.md`.

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
- added only `submission-date` and `article-author-note` as new article metadata surfaces;
- left foreign-title semantics for the optional-foreign-elements step;
- added `tests/checks/scientific_article_profile_contract.py`;
- added a dedicated two-engine `tests/integration/scientific-article-profile.sh` gate.

No article presentation rule or proof state is promoted by Step 1. `standards/coverage-rules-article.json` remains source-reviewed/manual or conditional-manual until rule-specific article evidence is implemented.

## Current infrastructure checkpoint — scoped Linux integration

The former PR orchestration ran the complete `make check` path for every technical synchronization. That made small Scientific Article increments wait for the entire repository matrix.

The replacement keeps one permanent workflow but adds named suites:

| Scope | Scientific Article use |
|---|---|
| `article` | default bounded suite for article-specific intermediate runtime/evidence; includes `validator-source` + executable `scientific-article-profile` |
| `profiles` | compatibility work for the six accepted non-article profiles |
| `reference-document` / `reference-pdf` | only when article work intentionally affects shared canonical-reference surfaces |
| domain suites | bounded shared changes such as objects, bibliography, layout or front matter |
| `complete` | shared/unknown paths and **mandatory Scientific Article phase-end regression** |

PR `auto` uses only the incremental pushed range on `synchronize` events, so a long-lived PR does not repeatedly re-run the full historical diff. Initial/reopened/ready events still use the full PR diff. Unknown technical paths fail closed to `complete`.

Manual workflow dispatch provides explicit scope choices. `auto` on manual dispatch resolves to `complete`.

As Steps 2–7 add article-specific executable gates, each new gate must be added to the `article` suite in the same **material advance**. A scoped green run never promotes a rule or closes the phase by itself.

## Repository integration boundary

PR #285 carries the accepted shared foundation, Step 1 and the scoped Linux orchestration checkpoint while `main` is still stale. After this infrastructure checkpoint is green, merge that integration boundary, then create a fresh `feat/v3-scientific-article` branch from updated `main`. Step 2 runtime work must start on that fresh branch.

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
- The phase ends only after a complete **phase-end regression** on one immutable candidate using the `complete` Linux scope.

## Implementation sequence

| Step | Work | Current state | Acceptance |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| CI | Scoped Linux orchestration | **CURRENT** | Static suite contract + bounded PR Linux run; complete remains phase-end-only |
| 2 | Required article front block | NEXT AFTER PR #285 MERGE | Required title/authorship/date/summary elements have article-specific rendered evidence |
| 3 | Optional foreign elements | QUEUED | Foreign title/summary may be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | QUEUED | Required article structure and body typography are validated |
| 5 | Recommendations and conditional applicability | QUEUED | Advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | Rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | Provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Next action

1. accept the scoped Linux orchestration checkpoint only after Static and the bounded PR Linux run pass;
2. record the checkpoint SHA/run IDs and synchronize the docs/machine state;
3. merge PR #285;
4. create `feat/v3-scientific-article` from updated `main`;
5. implement **Required article front block**, using `article` scope for intermediate article-only changes and `complete` only when shared/global surfaces or phase-end policy require it.
