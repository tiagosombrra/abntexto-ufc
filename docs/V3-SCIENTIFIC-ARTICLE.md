# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 5 RECOMMENDATIONS AND CONDITIONAL APPLICABILITY

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
| 4 | Textual structure and body typography | **ACCEPTED** | `005956bd...`; Static `34119007413`; Linux `34119007425`; `SCOPE=article PASS=5 FAIL=0 SKIP=0` |
| 5 | Recommendations and conditional applicability | **ACTIVE** | build modality-preservation evidence; do not create hard recommendation failures |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Step 4 accepted contract

Step 4 owns `article.introduction.required`, `article.development.required`, `article.final-considerations.required`, `article.references.required`, and `article.body.typography`.

| Property | Accepted evidence |
|---|---|
| Font size | 12 pt under pdfLaTeX and LuaLaTeX |
| Alignment | justified within measured tolerance |
| First-line indent | `57.125 pt`, delta `0.432 pt` from 2 cm |
| Line spacing | `13.800 pt`, exactly matching same-document single-spacing calibration |
| Required structure | rendered headings Introduction → Development → Final Considerations → References |
| Negative structure | omitted Development rejected as missing required heading despite prose mentioning `desenvolvimento` |
| Proof state | not promoted in Step 4 |

Linux `34119007425` closed the Step 4 defect chain with all five article checks green. The heading-based checker correction strengthened negative evidence without changing runtime, tolerances, authority or proof state.

## Step 5 authority scope

The retained contract contains four recommendations and one conditional rule:

| Rule | Normativity | Contract |
|---|---|---|
| `article.authorship.alignment.recommended` | recommended | right alignment is a recommendation, not a technical validity requirement |
| `article.summary.word-count.recommended` | recommended | 150–250 words is advisory, not an absolute rejection interval |
| `article.summary.keywords.minimum.recommended` | recommended | at least three keywords is advisory |
| `article.summary.single-paragraph.recommended` | recommended | one-paragraph summary is advisory |
| `article.journal-guidelines.precedence` | required-when-applicable | target-journal instructions must be checked only in journal-submission context; generic UFC profile remains fallback |

The official UFC article guide also describes authorship right alignment as a suggestion and uses recommendation language for the summary/keyword guidance. Step 5 therefore must preserve these distinctions instead of converting style advice into class errors.

## Step 5 implementation strategy

1. add an article recommendation/conditional evidence gate rather than new mandatory runtime validators;
2. compile controlled article scenarios that intentionally sit outside recommended summary length/paragraph shape without class rejection;
3. verify existing right-aligned authorship remains a default presentation choice while the retained rule stays `recommended` in the contract;
4. treat keyword-count recommendation conservatively: do not invent a mandatory keyword element or minimum-count error absent a retained required-element rule;
5. statically verify the journal-precedence rule remains `required-when-applicable`, `conditional-manual`, and applicability-bound to target-journal submission;
6. preserve Steps 1–4 and non-article behavior.

If user-facing keyword support is introduced later, it must remain compatible with this modality and cannot silently strengthen the 18-rule contract.

## Acceptance gate for Step 5

1. Static contract passes on the synchronized implementation checkpoint;
2. Linux article scope passes Steps 1–4 plus the Step 5 executable gate;
3. controlled recommendation-outside-range scenarios compile successfully;
4. no recommendation emits a class error or validator rejection solely for recommendation nonconformance;
5. journal precedence remains conditional/manual and applicability-bound;
6. contract IDs, normativity, locators and proof state remain unchanged;
7. no shared non-article runtime behavior changes.

Step 6 does not begin until these results are recorded in a later documentation checkpoint.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no aliases.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain conditional.
- Shared implementation is not article proof.
- Do not weaken Step 4 physical PDF evidence.
- Do not couple earlier accepted Step gates to later implementation syntax.
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
| Step 4 Static / Linux | `34119007413` PASS / `34119007425` PASS |

Next: implement the bounded Step 5 modality-preservation gate, synchronize this control plane in the same commit cycle, run Static plus article Linux, and only after acceptance activate Step 6.
