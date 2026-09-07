# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 4 SUPPORTED SINGLE-SPACING CORRECTION / ACCEPTANCE RERUN PENDING

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
| 4 | Textual structure and body typography | **SUPPORTED SINGLE-SPACING CORRECTION IMPLEMENTED — CI PENDING** | `49e7b17...` rejected deprecated `\\spacing{1}` warning before physical body validation; implementation `6a7ef821...` uses supported `\\singlesp` plus `cmd/textual/after` |
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
| `09b870d0f7f3771884d55e2e922921051df2dfe0` | Static `34072362333` PASS; Linux `34072362335` article PASS=4 FAIL=1; body still `20.700 pt` | front-block-only route transient; first `\\section` invokes `\\textual` and restores shared state |
| `49e7b179f7de9274f1cbf01fefed20ce04eae8e0` | Static `34111737479` PASS; Linux `34111737488` `SCOPE=complete PASS=32 FAIL=2 SKIP=1` | deprecated `\\spacing{1}` warning stopped front-block/body gates before physical Step 4 validation |

The latest Linux result does not overturn the `\\textual` transition diagnosis. It shows that the attempted persistent-state implementation used an obsolete API. The warning policy is kept strict, and the physical body checker remains authoritative because `49e7...` never reached it.

## Current runtime correction — `6a7ef821875c40b6fe0bbc3cca25e3c0ff4cb307`

The article body function now:

- uses the supported `\\singlesp` route;
- sets the first-line indent to 2 cm and paragraph extra spacing to zero;
- keeps justified alignment;
- remains guarded by `type=scientific-article`;
- is invoked after the required primary summary;
- is re-applied by `\\AddToHook{cmd/textual/after}{...}` so the automatic textual transition is followed immediately by the article-specific body contract.

The dedicated body gate now requires `\\singlesp`, explicitly rejects deprecated `\\spacing{1}`, and retains the textual-transition hook requirement. The physical PDF checker and missing-development negative fixture are unchanged. Step 2 and Step 3 remain isolated from Step 4 implementation tokens.

Article proof state is not promoted by this correction.

## Acceptance gate for Step 4

1. Static contract passes on the synchronized correction checkpoint;
2. Linux passes all five article checks;
3. positive body PDFs under pdfLaTeX and LuaLaTeX prove 12 pt, justified alignment, 2 cm first-line indent and single spacing;
4. the same body typography survives the first numbered-section `\\textual` transition;
5. no deprecated spacing warning is emitted;
6. missing-development negative fixture is rejected for the intended structural reason;
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
| Latest rejected synchronized checkpoint | `49e7b179f7de9274f1cbf01fefed20ce04eae8e0` |
| Current runtime implementation | `6a7ef821875c40b6fe0bbc3cca25e3c0ff4cb307` |

Next: publish the synchronized documentation checkpoint containing implementation `6a7ef821...`, run Static plus Linux, classify any remaining failure fail-closed, and only after physical green acceptance advance to Step 5.
