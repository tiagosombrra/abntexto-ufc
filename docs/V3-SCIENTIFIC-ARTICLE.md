# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 4 PHYSICAL BODY PASS / NEGATIVE STRUCTURE CHECKER CORRECTION PENDING CI

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
| 4 | Textual structure and body typography | **PHYSICAL BODY PASS — NEGATIVE STRUCTURE CHECKER FIX IMPLEMENTED, CI PENDING** | `05194675...`: Static `34115345674` PASS; Linux `34115345586` article PASS=4 FAIL=1; both positive engines physically PASS; checker correction `4039fa011...` |
| 5 | Recommendations and conditional applicability | BLOCKED | begins only after Step 4 acceptance is recorded |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Step 4 contract

Step 4 owns `article.introduction.required`, `article.development.required`, `article.final-considerations.required`, `article.references.required`, and `article.body.typography`.

| Property | Required value |
|---|---|
| Font size | 12 pt |
| Alignment | justified |
| First-line indent | 2 cm |
| Line spacing | single |
| Required structure evidence | rendered headings for Introduction, Development, Final Considerations and References |

## Fail-closed evidence sequence

| Checkpoint | Result | Classification |
|---|---|---|
| `8b52ee4b36b23868fecce9bbe9b843f689ccc01e` | Static `34058435312` PASS; Linux `34058435311` body gap `20.700 pt` vs `13.800 pt` | real runtime spacing defect |
| `177a62115e1dc28b24394ed4061600c3a7386fca` | Static `34070809181` PASS; Linux `34070809177` stopped three gates on stale `AtBeginDocument` token | stale implementation-token gate coupling |
| `bf6c48e0cc1e5d19751ad2ff112db77fce799706` | Static `34071163701` PASS; Linux `34071163702` article PASS=4 FAIL=1; body still `20.700 pt` | `begindocument/end` route physically ineffective |
| `09b870d0f7f3771884d55e2e922921051df2dfe0` | Static `34072362333` PASS; Linux `34072362335` article PASS=4 FAIL=1; body still `20.700 pt` | front-block-only route transient; first `\\section` invokes `\\textual` and restores shared state |
| `49e7b179f7de9274f1cbf01fefed20ce04eae8e0` | Static `34111737479` PASS; Linux `34111737488` `SCOPE=complete PASS=32 FAIL=2 SKIP=1` | deprecated `\\spacing{1}` warning stopped front-block/body gates before physical Step 4 validation |
| `05194675f7d41d8c4f35227e67e8ee303d1ea79a` | Static `34115345674` PASS; Linux `34115345586` `SCOPE=article PASS=4 FAIL=1`; positive body evidence PASS twice at `13.800 pt` | runtime/body presentation corrected; negative fixture misclassified because structure detector matched `desenvolvimento` in prose rather than a heading |

## Physical Step 4 evidence at `05194675...`

| Engine | Font | First-line indent | Justification | Body gap | Same-document single calibration | Result |
|---|---:|---:|---|---:|---:|---|
| pdfLaTeX | 12 pt | `57.125 pt` (`0.432 pt` delta from 2 cm) | within tolerance | `13.800 pt` | `13.800 pt` | PASS |
| LuaLaTeX | 12 pt | `57.125 pt` (`0.432 pt` delta from 2 cm) | within tolerance | `13.800 pt` | `13.800 pt` | PASS |

This is the first Step 4 run that physically proves the supported `\\singlesp` plus `cmd/textual/after` route under both engines. It does not by itself close Step 4 because the negative structural evidence still failed for an unintended reason.

## Negative structure defect and correction

The negative fixture intentionally omits `\\section{Desenvolvimento}` while retaining prose that mentions the word `desenvolvimento`. The old `validate_structure()` folded the entire PDF text and used substring search, so those prose occurrences incorrectly satisfied the required-Development predicate. The checker then continued into physical marker validation and failed on missing `ARTICLEBODYSTART`, producing the wrong negative reason.

Technical correction `4039fa011b7f54f4f0be6d004131fc0e06567e2e`:

- preserves the adversarial negative fixture unchanged;
- scans normalized extracted text line by line;
- requires each structural element to match one complete rendered heading line;
- accepts an optional progressive section number before a heading;
- rejects missing or duplicate required headings;
- preserves ordering checks;
- does not change body typography measurements, tolerances, runtime or article proof state.

A negative fixture now counts only if it is rejected for the intended missing-heading predicate.

## Acceptance gate for Step 4

1. Static contract passes on the synchronized checker-correction checkpoint;
2. Linux passes all five article checks;
3. positive body PDFs under pdfLaTeX and LuaLaTeX retain 12 pt, justified alignment, 2 cm first-line indent and single spacing;
4. the same body typography survives the first numbered-section `\\textual` transition;
5. no deprecated spacing warning is emitted;
6. missing-development negative fixture is rejected specifically because the Development heading is absent;
7. front-block and foreign-element gates remain green without Step 4 token coupling;
8. article authority, modality and proof state are unchanged.

Step 5 does not begin until these results are recorded in a later documentation checkpoint.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no aliases.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain conditional.
- Shared implementation is not article proof.
- Do not weaken warning or physical PDF evidence after a runtime defect.
- Required-structure evidence must identify rendered headings, not incidental prose tokens.
- Negative evidence must fail for the intended predicate.
- Do not couple earlier accepted Step gates to later implementation syntax when a dedicated later gate owns that contract.
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
| Latest synchronized Step 4 checkpoint | `05194675f7d41d8c4f35227e67e8ee303d1ea79a` |
| Current checker correction | `4039fa011b7f54f4f0be6d004131fc0e06567e2e` |

Next: publish one synchronized checkpoint containing `4039fa011...` and this control-plane update, run Static plus Linux, classify any remaining failure fail-closed, and only after all five article checks are green record Step 4 acceptance and activate Step 5.
