# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 3 IMPLEMENTED / CI PENDING

## Purpose

Implement and validate one canonical `scientific-article` profile on top of the corrected, visually accepted shared V3 foundation. The phase realizes the retained 18-rule source-backed article contract without forking cross-cutting infrastructure or weakening accepted non-article behavior.

Authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.

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
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | **ACCEPTED** | `0947669c2c096dca93991e042d8ae245754688ba`; Static `34026680871`; Linux `34026680882`, 31/31 PASS |
| 3 | Optional foreign elements | **IMPLEMENTED — CI PENDING** | technical checkpoint `81e08321222efb03626ac421fc645bd66edd5ae8`; synchronized branch-head Static/full Linux required |
| 4 | Textual structure and body typography | QUEUED | required structure + 12 pt/justified/2 cm/single-spaced body |
| 5 | Recommendations and conditional applicability | QUEUED | advisory semantics stay advisory; journal boundary stays conditional |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + full Linux + article-specific acceptance on one immutable SHA |

## Step 2 acceptance

The final synchronized Step 2 checkpoint `0947669c2c096dca93991e042d8ae245754688ba` passed Static `34026680871` and Linux `34026680882`, `PASS=31 FAIL=0 SKIP=0`. The Linux run emitted article-profile and required-front-block PASS evidence on pdfLaTeX and LuaLaTeX. The corrected validator preserved genuine `\footnote` routing and rendered 10 pt footnote evidence while removing the unsupported physical-page percentage predicate. No article proof state was promoted.

## Step 3 implementation — Optional foreign elements

Rules owned by this Step:

- `article.title.foreign.optional`;
- `article.summary.foreign.optional`.

Technical checkpoint `81e08321222efb03626ac421fc645bd66edd5ae8` adds an explicit article-only public route:

`\ufcPrintArticleForeignElements{foreign-title}{foreign-summary}`

The existing required-front-block command remains unchanged.

### Runtime behavior

| Scenario | Foreign title | Foreign summary | Runtime requirement |
|---|---|---|---|
| neither | absent | absent | render neither; no failure |
| title only | present | absent | render title only |
| summary only | absent | present | render summary only |
| both | present | present | render both |

The two arguments are independently guarded with blank checks. The implementation does not use shared `title-variant`, does not add new metadata keys, and does not activate body typography.

Rendering is intentionally minimally styled because the retained optional rules establish element optionality but do not freeze an independent foreign-element typography contract. Step 3 evidence therefore tests routing/optionality rather than inventing unsupported style predicates.

### Step 3 evidence surface

Added:

- `tests/documents/scientific-article-foreign-both.tex`;
- `tests/documents/scientific-article-foreign-title-only.tex`;
- `tests/documents/scientific-article-foreign-summary-only.tex`;
- `tests/documents/scientific-article-foreign-absent.tex`;
- `tests/integration/scientific-article-foreign-elements.sh`.

The permanent `tests/integration/scientific-article-profile.sh` now invokes both the accepted front-block gate and the new foreign-elements gate.

The foreign-elements gate compiles all four scenarios under pdfLaTeX and LuaLaTeX, checks independent marker presence/absence, rejects `title-variant` reuse, and rejects premature `\AtBeginDocument` body-typography activation.

Expected structured evidence:

`ARTICLE-FOREIGN-ELEMENTS-EVIDENCE status=PASS engines=2 scenarios=4 title_optional=true summary_optional=true independent=true title_variant_reused=false presentation_rules_promoted=0 recommendations_promoted=0`

### Acceptance gate

Step 3 remains **IMPLEMENTED / CI PENDING** until the synchronized branch head passes:

1. Static contract;
2. full Linux integration;
3. new foreign-elements evidence on both engines;
4. accepted front-block evidence;
5. all non-article profiles;
6. no rule-modality or proof-state drift.

Any failure is classified before code/test changes. The gate is not weakened merely to obtain green status.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no compatibility aliases.
- Preserve all accepted non-article profiles and the shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable in runtime and evidence.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain a conditional applicability boundary.
- Step 3 implementation does not promote any rule in `standards/coverage-rules-article.json`; evidence hardening owns proof-state promotion.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.
- Every **material advance** updates handoff, roadmap, machine state, release readiness and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.

Next: publish the synchronized documentation checkpoint on top of `81e0832...`, run Static and full Linux, classify any failure, and only after both are green mark Step 3 accepted and activate Step 4.
