# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 4 PERSISTENT-SPACING CORRECTION / ACCEPTANCE RERUN PENDING

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
| 4 | Textual structure and body typography | **PERSISTENT-SPACING CORRECTION IMPLEMENTED — CI PENDING** | latest physical failure `09b870d...`; implementation `15ed414...` updates spacing state and rebinds after `\textual` |
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

## Fail-closed evidence sequence

| Checkpoint | Result | Classification |
|---|---|---|
| `8b52ee4b36b23868fecce9bbe9b843f689ccc01e` | Static `34058435312` PASS; Linux `34058435311` body gap `20.700 pt` vs `13.800 pt` | real runtime spacing defect |
| `177a62115e1dc28b24394ed4061600c3a7386fca` | Static `34070809181` PASS; Linux `34070809177` stopped three gates on stale `AtBeginDocument` token | stale implementation-token gate coupling |
| `bf6c48e0cc1e5d19751ad2ff112db77fce799706` | Static `34071163701` PASS; Linux `34071163702` article PASS=4 FAIL=1; body still `20.700 pt` | `begindocument/end` route physically ineffective |
| `09b870d0f7f3771884d55e2e922921051df2dfe0` | Static `34072362333` PASS; Linux `34072362335` article PASS=4 FAIL=1; body still `20.700 pt` | front-block-only route also transient; first `\section` invokes `\textual`, which restores shared 1.5 spacing |

The latest Linux result is decisive because all four preceding article checks passed. The remaining failure is caused by the upstream state transition itself, not by source-gate ambiguity.

## Current runtime correction — `15ed414d3f1474157fe2e34de2d97ae6e76dd5ff`

`abntexto` stores its current spacing factor in `\currspacing`. `\singlesp` changes only the current baseline, while `\textual` later executes `\spacing{1.5}` and resets paragraph indentation. Therefore a front-block-only call cannot persist into the first numbered section.

The article body function now:

- uses `\spacing{1}` so the persistent spacing factor is single;
- sets the first-line indent to 2 cm and paragraph extra spacing to zero;
- keeps justified alignment;
- remains guarded by `type=scientific-article`;
- is invoked after the required primary summary;
- is also re-applied by `\AddToHook{cmd/textual/after}{...}` so the automatic textual transition cannot restore the academic-work 1.5-spacing/1.5-cm state.

The dedicated body gate is strengthened accordingly: it requires the persistent spacing route and textual-transition rebound while leaving the physical checker unchanged. Step 2 and Step 3 remain isolated from Step 4 implementation tokens.

Article proof state is not promoted by this correction.

## Acceptance gate for Step 4

1. Static contract passes on the synchronized correction checkpoint;
2. bounded Linux `article` passes all five checks;
3. positive body PDFs under pdfLaTeX and LuaLaTeX prove 12 pt, justified alignment, 2 cm first-line indent and single spacing;
4. the same body typography survives the first numbered-section `\textual` transition;
5. missing-development negative fixture is rejected for the intended structural reason;
6. front-block and foreign-element gates remain green without Step 4 token coupling;
7. article authority, modality and proof state are unchanged.

Step 5 does not begin until these results are recorded in a later documentation checkpoint.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no aliases.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain conditional.
- Shared implementation is not article proof.
- Do not weaken physical PDF evidence after a runtime defect.
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
| Latest rejected physical checkpoint | `09b870d0f7f3771884d55e2e922921051df2dfe0` |
| Current runtime implementation | `15ed414d3f1474157fe2e34de2d97ae6e76dd5ff` |

Next: publish the synchronized documentation checkpoint containing implementation `15ed414...`, run Static plus bounded Linux `article`, classify any remaining failure fail-closed, and only after green acceptance advance to Step 5.
