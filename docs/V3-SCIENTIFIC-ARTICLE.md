# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 5 ORCHESTRATION ACCEPTED / KEYWORD-SENTINEL CORRECTION PENDING CI

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
| 5 | Recommendations and conditional applicability | **EVIDENCE-HARNESS CORRECTION ACTIVE** | `6507da...` complete 36/36 PASS; `02e1ea...` Static PASS and auto scope=`article`; Linux `34129625475` passed 5/6 and failed only long synthetic keyword extraction |
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

## Accepted Step 5 evidence before current correction

Linux `34126602083` on `6507da00275d8a69093541d6e6cb119a1b6f6cb3` ran `SCOPE=complete PASS=36 FAIL=0 SKIP=0`. All six Scientific Article gates passed. The recommendation evidence proved two engines, recommended and outside-recommendation scenarios, non-fatal recommendation nonconformance, conditional-manual journal precedence and zero proof-state promotion.

Static `34126602062` failed only because mixed orchestration + article paths selected `complete`. That orchestration defect was corrected at `02e1ea6e25c008c93f8ec3ba26af7f3cea03cf14`.

## Orchestration correction result

| Gate | Result |
|---|---|
| Static `34129625390` | **PASS** |
| Incremental auto scope | **`article`**, as required |
| Linux `34129625475` | `SCOPE=article PASS=5 FAIL=1 SKIP=0` |
| Validator/source | PASS |
| Profile | PASS |
| Front block | PASS |
| Foreign elements | PASS |
| Body | PASS |
| Recommendations | FAIL only on exact extraction of `ARTICLEADVISORYKEYTHREE` for recommended + pdfLaTeX |

The recommendation contract checker itself passed before the rendered-marker failure and reported `recommended_rules=4`, `journal_rules=1`, `recommendation_mode=manual`, `journal_mode=conditional-manual`, `proof_state_promoted=0`.

## Current failure classification and correction

The long artificial keyword sentinel is the only failing predicate. The summary marker was rendered, the PDF compiled without unrecognized warnings/overflow, and earlier Step 5 evidence already proved the recommendation semantics. Therefore the current correction targets the evidence harness first, not runtime.

The two controlled fixtures now use short extraction-safe keyword sentinels. The integration gate requires all three recommended keyword markers and the single outside-recommendation marker to appear in `pdftotext -layout` output under both pdfLaTeX and LuaLaTeX. If the shortened sentinels still fail, the result is reclassified before any further change.

## Step 5 acceptance gate

| Gate | Required result |
|---|---|
| Static contract | PASS |
| Automatic inference | `article` |
| Linux `article` | six first-class checks PASS |
| Recommended scenario | both engines compile and render summary + `ARTKEYONE`, `ARTKEYTWO`, `ARTKEYTHREE` |
| Outside-recommendation scenario | both engines compile and render both paragraphs + `ARTOUTKEY` |
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
- A synthetic PDF-text sentinel failure is isolated from runtime semantics before changing runtime.
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
| Orchestration correction checkpoint | `02e1ea6e25c008c93f8ec3ba26af7f3cea03cf14` |
| Orchestration Static | `34129625390` PASS |
| Orchestration Linux | `34129625475`, scope=`article`, downstream keyword-sentinel failure only |

Next: publish the synchronized short-sentinel correction, require Static + bounded Linux `article`, record the exact checkpoint results, then activate Step 6 only if all six article checks pass.
