# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 5 IMPLEMENTED / SYNCHRONIZED CI PENDING

## Purpose

Implement and validate one canonical `scientific-article` profile on top of the corrected, visually accepted shared V3 foundation. The phase realizes the retained 18-rule source-backed article contract without forking cross-cutting infrastructure or weakening accepted non-article behavior.

Authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.  
Linux orchestration contract: `docs/LINUX-INTEGRATION-SCOPES.md`.

## Step status

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign elements | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | ACCEPTED | `005956bd...`; Static `34119007413`; Linux `34119007425`; `SCOPE=article PASS=5 FAIL=0 SKIP=0` |
| 5 | Recommendations and conditional applicability | **IMPLEMENTED — CI PENDING** | dedicated first-class recommendation/conditional gate added to `article`; synchronized Static + article Linux required |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Step 5 authority scope

| Rule | Normativity | Preserved meaning |
|---|---|---|
| `article.authorship.alignment.recommended` | recommended | right alignment is the generic default, not a document-validity condition |
| `article.summary.word-count.recommended` | recommended | 150–250 words is advisory, not a rejection interval |
| `article.summary.keywords.minimum.recommended` | recommended | at least three keywords is advisory |
| `article.summary.single-paragraph.recommended` | recommended | one-paragraph summary is advisory |
| `article.journal-guidelines.precedence` | required-when-applicable | journal instructions are checked only for target-journal submission; generic UFC profile remains fallback |

No Step 5 change modifies these rule IDs, locators, normativity, applicability or proof state.

## Step 5 implementation

The Step 5 evidence surface now consists of:

1. `tests/checks/scientific_article_recommendations_contract.py`, which freezes recommendation modality as `recommended` + `manual`, freezes journal precedence as `required-when-applicable` + `conditional-manual`, preserves `target-journal-submission` applicability, confirms the generic right-aligned author default, and verifies controlled fixture semantics;
2. `tests/documents/scientific-article-recommendations-recommended.tex`, whose summary remains inside the 150–250-word guidance, one paragraph and at least three keywords;
3. `tests/documents/scientific-article-recommendations-outside.tex`, which deliberately uses a short summary, two paragraphs and fewer than three keywords while retaining all required article metadata;
4. `tests/integration/scientific-article-recommendations.sh`, which compiles both scenarios with pdfLaTeX and LuaLaTeX and proves that recommendation nonconformance alone does not create a class/validator rejection;
5. first-class registration of `scientific-article-recommendations` in `tests/run.py` and the `article` Linux suite.

The earlier fixture-only checkpoint `f4453337d2de94260d7ebda4cead9803a6a9cb64` passed Static `34124565217` and Linux `34124565158`, but that Linux run still contained only the five Step 1–4 article checks. It is therefore useful preflight evidence, not Step 5 acceptance.

## Step 5 acceptance gate

| Gate | Required result |
|---|---|
| Static contract | recommendation contract + suite registration PASS |
| Linux `article` | six first-class checks PASS, including Step 5 |
| Recommended scenario | compiles on both engines |
| Outside-recommendation scenario | compiles on both engines despite short/multi-paragraph/fewer-keyword recommendation deviations |
| Journal precedence | remains conditional-manual and context-bound |
| Steps 1–4 | remain green |
| Proof state | no promotion merely from recommendation/default reuse |

The commit containing this synchronized implementation is the Step 5 acceptance candidate. Its exact SHA and workflow run IDs are recorded only after CI completes; the candidate itself is not amended while CI is running.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no aliases.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain conditional.
- Shared implementation is not article proof.
- Do not weaken Step 4 physical PDF evidence.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

| Fact | Value |
|---|---|
| Canonical base | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active branch | `feat/v3-scientific-article` |
| Active PR | #286 |
| Step 4 accepted checkpoint | `005956bd615042a12fb0393fddd4941b635f6ce3` |
| Step 5 fixture preflight | `f445333...`; Static `34124565217` PASS; Linux `34124565158` PASS but Step 5 gate not yet registered there |

Next: publish this synchronized Step 5 gate checkpoint, wait for Static and bounded Linux `article`, record the exact candidate SHA/results, and only then activate Step 6.
