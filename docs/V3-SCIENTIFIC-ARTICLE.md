# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 3 RUNNER-IMPORT CORRECTION / SCOPED CI PENDING

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
| 3 | Optional foreign elements | **IMPLEMENTED — RUNNER IMPORT FIX / CI PENDING** | runtime `81e0832...`; migration `336bc982...`; technical fix `4068414...` |
| 4 | Textual structure and body typography | QUEUED | required structure + 12 pt/justified/2 cm/single-spaced body |
| 5 | Recommendations and conditional applicability | QUEUED | advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Step 3 implementation — optional foreign elements

Rules owned by this Step:

- `article.title.foreign.optional`;
- `article.summary.foreign.optional`.

Runtime checkpoint `81e08321222efb03626ac421fc645bd66edd5ae8` adds the explicit article-only route:

`\ufcPrintArticleForeignElements{foreign-title}{foreign-summary}`

The arguments are independently blank-safe. The route does not reuse shared `title-variant`, add metadata keys, or activate Step 4 body typography.

| Scenario | Foreign title | Foreign summary |
|---|---|---|
| neither | absent | absent |
| title only | present | absent |
| summary only | absent | present |
| both | present | present |

## Evidence history and current classification

Linux `34028373060` on `567a5b2d21a16b653d7704639bdd5012d7c2f99b` exposed a one-pass warning-inspection defect in the foreign-elements gate. The correction gave each scenario two LaTeX passes and separated article gates from the non-article profile matrix.

Migration checkpoint `336bc982d8442d572b52c4b9b78028e197c178b3` then proved the new orchestration selected `profiles,article`. Linux `34030098924` produced:

| Check | Result |
|---|---|
| `scientific-article-profile` | PASS |
| `scientific-article-front-block` | PASS |
| `scientific-article-foreign-elements` | PASS — 4 scenarios × 2 engines |
| non-article `profiles` | PASS — 6 profiles × 2 engines |
| build path / multivolume / catalog card | PASS |
| `validator-source` | FAIL — runner sibling import path |

Static `34030098936` failed at the same `validator-source` path. `normative_traceability.py` dynamically loads `tests/run.py`; `tests/run.py` imported sibling `integration_suites.py` without first putting `tests/` on `sys.path`. Classification: **runner infrastructure defect**, not article runtime, source authority, modality, proof-state or compatibility failure.

Technical correction `4068414a2c2e1f919246438b516a6092f677925f`:

1. makes the runner import its sibling suite module robustly under direct and dynamic loading;
2. explicitly rejects `scientific-article` from the non-article profile matrix and emits `PROFILE-MATRIX-EVIDENCE`;
3. records `convergence_passes=2` in `ARTICLE-FOREIGN-ELEMENTS-EVIDENCE`;
4. changes no article runtime or normative rule.

## Scoped Linux integration

Intermediate article work uses bounded scope where safe. The current synchronized correction intentionally changes runner orchestration plus `profiles` and `article` evidence surfaces, so PR `auto` must select the union `profiles,article`.

`article` currently includes:

- `validator-source`;
- `scientific-article-profile`;
- `scientific-article-front-block`;
- `scientific-article-foreign-elements`.

As Steps 4–7 add article-specific executable gates, add them to `article` in the same **material advance**. `profiles` remains a separate six-profile compatibility suite.

## Step 3 acceptance gate

Step 3 remains open until one synchronized checkpoint proves:

1. Static contract PASS, including `LINUX-SUITE-EVIDENCE` and dynamic runner import through normative traceability;
2. Linux bounded scope `profiles,article` PASS on the same SHA;
3. `ARTICLE-PROFILE-EVIDENCE` PASS;
4. `ARTICLE-FRONT-BLOCK-EVIDENCE` PASS;
5. `ARTICLE-FOREIGN-ELEMENTS-EVIDENCE` PASS for all four scenarios under both engines with two-pass convergence;
6. `PROFILE-MATRIX-EVIDENCE` PASS and six non-article profiles green;
7. no article rule-modality or proof-state drift.

A complete repository run is not required for this intermediate Step. The **phase-end regression** remains stricter: `complete` Linux on one immutable Scientific Article candidate, plus Static and phase-specific acceptance.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no compatibility aliases.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain conditional.
- Step 3 does not promote article proof state merely because runtime exists.
- Do not weaken normative traceability to repair runner imports.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.

Next: publish the synchronized correction containing technical checkpoint `4068414...`, require Static and `profiles,article` Linux on that same branch checkpoint, classify any failure, and only after both are green mark Step 3 accepted and activate Step 4.
