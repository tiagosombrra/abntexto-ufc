# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 3 EVIDENCE CORRECTION / SCOPED LINUX CI PENDING

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
| 3 | Optional foreign elements | **IMPLEMENTED — EVIDENCE FIX / CI PENDING** | runtime checkpoint `81e0832...`; Linux `34028373060` classified as one-pass evidence-orchestration failure |
| 4 | Textual structure and body typography | QUEUED | required structure + 12 pt/justified/2 cm/single-spaced body |
| 5 | Recommendations and conditional applicability | QUEUED | advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Step 3 implementation — Optional foreign elements

Rules owned by this Step:

- `article.title.foreign.optional`;
- `article.summary.foreign.optional`.

Technical checkpoint `81e08321222efb03626ac421fc645bd66edd5ae8` adds the explicit article-only route:

`\ufcPrintArticleForeignElements{foreign-title}{foreign-summary}`

The two arguments are independently blank-safe. The implementation does not use shared `title-variant`, does not add new metadata keys, and does not activate Step 4 body typography.

Controlled scenarios remain:

| Scenario | Foreign title | Foreign summary |
|---|---|---|
| neither | absent | absent |
| title only | present | absent |
| summary only | absent | present |
| both | present | present |

## Linux 34028373060 — failure classification

The synchronized Step 3 head `567a5b2d21a16b653d7704639bdd5012d7c2f99b` passed Static `34028373064`. The former full Linux run `34028373060` passed every shared check before `profiles`, then successfully built all six accepted non-article profiles under pdfLaTeX and LuaLaTeX.

The only failure occurred after `profile-matrix.sh` recursively called the article profile gate. The first foreign-elements scenario compiled once and then treated expected first-pass Biber/cross-reference rerun warnings as an error.

Classification: **evidence/test orchestration defect**. No article runtime, source authority, modality, proof-state, or non-article compatibility failure is inferred.

Correction:

1. each foreign-elements scenario now receives two LaTeX passes before warning inspection, matching the accepted front-block pattern;
2. `scientific-article-profile`, `scientific-article-front-block`, and `scientific-article-foreign-elements` become independent first-class checks in `tests/run.py`;
3. the six-profile compatibility matrix no longer recursively runs article gates;
4. the profile gate no longer recursively chains Step 2/3 gates;
5. Linux integration gets named bounded scopes.

No runtime or normative contract change is part of this correction.

## Scoped Linux integration

For intermediate Scientific Article work, the default bounded target is `article`:

- `validator-source`;
- `scientific-article-profile`;
- `scientific-article-front-block`;
- `scientific-article-foreign-elements`.

As Steps 4–7 add new article-specific executable gates, add them to `article` in the same **material advance**.

The `profiles` suite is separate and covers the six accepted non-article profiles plus profile/build compatibility. The first migration run is expected to select the union `profiles,article` because this checkpoint changes both orchestration surfaces. Later article-only pushes should normally select `article`.

PR `auto` uses the incremental pushed range on `synchronize`, preventing old accumulated PR history from repeatedly forcing a complete run. Unknown/shared/core changes still fail closed to `complete`.

## Step 3 acceptance gate

Step 3 remains open until one synchronized checkpoint proves:

1. Static contract PASS, including `LINUX-SUITE-EVIDENCE`;
2. Linux bounded scope `profiles,article` PASS for this migration checkpoint;
3. `ARTICLE-PROFILE-EVIDENCE` PASS;
4. `ARTICLE-FRONT-BLOCK-EVIDENCE` PASS;
5. `ARTICLE-FOREIGN-ELEMENTS-EVIDENCE` PASS for all four scenarios under both engines;
6. six-profile compatibility remains green;
7. no article rule-modality or proof-state drift.

A complete repository run is not required for each intermediate Step after this orchestration change. The **phase-end regression** remains stricter: `complete` Linux on one immutable Scientific Article candidate, plus Static and phase-specific acceptance.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no compatibility aliases.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain a conditional applicability boundary.
- Step 3 implementation/evidence correction does not promote any rule in `standards/coverage-rules-article.json`; evidence hardening owns proof-state promotion.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.

Next: publish this synchronized evidence/orchestration checkpoint, require Static and a bounded `profiles,article` Linux run, classify any failure, and only after both are green mark Step 3 accepted and activate Step 4.
