# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 5 EVIDENCE GREEN / ORCHESTRATION CORRECTION PENDING CI

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
| 4 | Textual structure and body typography | ACCEPTED | `005956bd...`; Static `34119007413`; Linux `34119007425` |
| 5 | Recommendations and conditional applicability | **EVIDENCE GREEN / CHECKPOINT NOT YET ACCEPTED** | `6507da...`; Linux `34126602083` complete 36/36 PASS; Static `34126602062` failed only mixed orchestration+article scope inference |
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
| `article.journal-guidelines.precedence` | required-when-applicable | journal instructions apply only in target-journal submission context; generic UFC profile remains fallback |

No Step 5 change modifies rule IDs, locators, normativity, applicability or proof state.

## Step 5 evidence result at `6507da...`

Linux `34126602083` ran `SCOPE=complete PASS=36 FAIL=0 SKIP=0`. All six Scientific Article gates passed. The recommendation evidence reported two engines, two scenarios, outside-recommendation compilation success, short summary acceptance, multiple-paragraph acceptance, fewer-than-three-keywords acceptance, right-aligned generic author default, zero hard recommendation failures, conditional-manual journal precedence and zero proof-state promotion.

Static `34126602062` failed after the article recommendation contract itself passed. The only failing predicate was the Linux integration suite contract: orchestration + article paths incorrectly selected `complete` rather than `article`.

## Current correction and hardening

The synchronized correction does two bounded things:

1. fix `tests/integration_suites.py` so orchestration paths are neutral when a recognized technical domain is present, while orchestration-only remains `smoke` and unknown/force-complete technical paths still select `complete`;
2. harden `scientific-article-recommendations.sh` and its controlled fixtures with unique rendered keyword markers, proving the PDF contains the expected keyword output in both the recommendation-following and outside-recommendation scenarios.

Neither change modifies the retained article rule registry or runtime normative behavior.

## Step 5 acceptance gate

| Gate | Required result |
|---|---|
| Static contract | suite inference + recommendation contract PASS |
| Automatic inference | orchestration + Step 5 path selects `article` |
| Linux `article` | six first-class checks PASS |
| Recommended scenario | both engines compile and render controlled summary/keyword markers |
| Outside-recommendation scenario | both engines compile and render both paragraphs + controlled keyword marker |
| Journal precedence | remains conditional-manual and context-bound |
| Steps 1–4 | remain green |
| Proof state | no promotion merely from recommendation/default reuse |

Step 6 is not activated until this corrected checkpoint is accepted and documented.

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
| Step 5 implementation checkpoint | `6507da00275d8a69093541d6e6cb119a1b6f6cb3` |
| Step 5 Linux | `34126602083` complete 36/36 PASS |
| Step 5 Static | `34126602062` orchestration inference failure |

Next: publish the synchronized inference correction + rendered keyword hardening checkpoint, require Static + bounded Linux `article`, record the exact candidate results, then activate Step 6.
