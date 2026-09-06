# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 3 SCOPE-FALLBACK CORRECTION / SCOPED CI PENDING

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
| 3 | Optional foreign elements | **IMPLEMENTED — SCOPE FALLBACK FIX / CI PENDING** | runtime `81e0832...`; scoped migration `336bc982...`; runner fix `4068414...`; scope fallback `0a48d72...` |
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

| Checkpoint / run | Result | Classification |
|---|---|---|
| `567a5b2...` / Linux `34028373060` | foreign-elements scenario inspected expected rerun warnings after one pass | evidence-convergence defect |
| `336bc982...` / Static `34030098936` | dynamic `tests/run.py` load could not import sibling `integration_suites.py` | runner import-path defect |
| `336bc982...` / Linux `34030098924` | intended `profiles,article`; 7/8 checks PASS; only validator-source failed on same import | runner import-path defect |
| `4f1c9a1...` / Static `34030827665` | **SUCCESS** | runner import correction confirmed |
| `4f1c9a1...` / Linux `34030827664` | scope determination stopped at `fatal: bad object` for unavailable synchronize `before` SHA; no integration check ran | workflow scope-fallback defect |

The latest Linux failure is not an article result because TeX integration never started. The workflow assumed the synchronize event's `before` commit remained reachable after history changes. The correct fail-closed behavior is to validate incremental endpoints before use and otherwise use the full PR base/head diff.

Technical correction `0a48d72c83b601c3ca8e0942f4c9b735ac5f0eb9`:

1. uses `git cat-file -e` to validate synchronize `before` and `after` commits;
2. falls back to full PR scope when either is unavailable, instead of crashing;
3. extends `linux_integration_suites.py` so Static protects the fallback contract;
4. asserts exactly six non-article profiles and excludes `scientific-article` from `profile-matrix.sh`;
5. emits explicit `PROFILE-MATRIX-EVIDENCE`;
6. records `convergence_passes=2` and `warnings_checked_after_final_pass=true` for foreign-element evidence;
7. changes no article runtime, authority, modality or proof state.

## Scoped Linux integration

Intermediate article work uses bounded scope where safe. On a normal reachable synchronize range, the current correction touches profile and article evidence surfaces and must select the union `profiles,article`.

If a synchronize endpoint is unavailable, `auto` falls back to the full PR diff. That may select `complete`; this is deliberate fail-closed behavior, not a weakening of the optimization contract.

`article` currently includes:

- `validator-source`;
- `scientific-article-profile`;
- `scientific-article-front-block`;
- `scientific-article-foreign-elements`.

As Steps 4–7 add article-specific executable gates, add them to `article` in the same **material advance**. `profiles` remains a separate six-profile compatibility suite.

## Step 3 acceptance gate

Step 3 remains open until one synchronized checkpoint proves:

1. Static contract PASS, including `LINUX-SUITE-EVIDENCE`, dynamic runner import, and missing-before fallback contract;
2. Linux bounded scope `profiles,article` PASS on the same SHA under a normal reachable incremental range;
3. `ARTICLE-PROFILE-EVIDENCE` PASS;
4. `ARTICLE-FRONT-BLOCK-EVIDENCE` PASS;
5. `ARTICLE-FOREIGN-ELEMENTS-EVIDENCE` PASS for all four scenarios under both engines with two-pass convergence and final-pass warning inspection;
6. `PROFILE-MATRIX-EVIDENCE` PASS, exactly six non-article profiles, both engines green;
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
- Do not weaken normative traceability or scope fail-closed behavior.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.

Next: publish the synchronized checkpoint containing technical correction `0a48d72...`, require Static and Linux on the same SHA, classify any failure, and only after both required bounded gates are green mark Step 3 accepted and activate Step 4.
