# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 4 GATE COUPLING CORRECTED / ACCEPTANCE RERUN PENDING

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
| 4 | Textual structure and body typography | **GATE CORRECTION IMPLEMENTED — CI PENDING** | runtime spacing failure at `8b52ee4...`; runtime-order correction at `177a621...`; stale source-token guards now corrected |
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

### Runtime defect — `8b52ee4b36b23868fecce9bbe9b843f689ccc01e`

Static `34058435312` passed. Bounded Linux `34058435311` passed four of five article gates and failed `scientific-article-body`. The checker physically measured `20.700 pt` body spacing against a same-document `13.800 pt` single-spacing calibration. The article was retaining the shared academic-work 1.5 spacing.

Classification: **real runtime initialization-order defect**. The body checker was not weakened.

### Gate-coupling defect — `177a62115e1dc28b24394ed4061600c3a7386fca`

Static `34070809181` passed. Bounded Linux `34070809177` produced `PASS=2 FAIL=3`: validator-source and profile passed, while front-block, foreign-elements and body gates stopped immediately because their source guards still required the literal token `\AtBeginDocument{\ufc_article_apply_body_typography:}`.

The runtime had intentionally moved to `\AddToHook{begindocument/end}{...}` so the article override would execute after shared layout initialization. Therefore this second failure is classified as **stale implementation-token coupling in integration guards**, not evidence that the runtime correction failed. The normal physical body checker did not run in that failed body gate.

## Current gate correction

The three shell gates now require the semantically accepted route:

`\AddToHook{begindocument/end}{\ufc_article_apply_body_typography:}`

They still independently require the body function and canonical `scientific-article` predicate. No physical measurement or structural negative predicate is removed or relaxed.

| Surface | State |
|---|---|
| Runtime profile predicate | PRESERVED |
| Runtime ordering | `begindocument/end` PRESERVED |
| Front-block two-engine PDF checks | PRESERVED |
| Foreign optionality scenarios | PRESERVED |
| Body 12 pt / 2 cm / justification checks | PRESERVED |
| Body single-spacing measurement | PRESERVED — must match single calibration |
| Missing-development negative fixture | PRESERVED |
| Article proof-state promotion | NONE |

The exact synchronized gate-correction SHA is recorded after this commit exists.

## Acceptance gate for Step 4

1. Static contract passes;
2. bounded Linux `article` passes all five checks;
3. positive body PDFs under pdfLaTeX and LuaLaTeX prove 12 pt, justified alignment, 2 cm first-line indent and single spacing;
4. missing-development negative fixture is rejected for the intended structural reason;
5. source guards prove profile-scoped post-shared-initialization activation without freezing an obsolete implementation spelling;
6. article authority, modality and proof state are unchanged.

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
- Do not retain a source-token check when it contradicts the accepted runtime ordering needed to satisfy the same physical requirement.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.
- Runtime correction checkpoint: `177a62115e1dc28b24394ed4061600c3a7386fca`.

Next: publish the synchronized gate-correction checkpoint, run Static plus bounded Linux, classify any remaining failure fail-closed, and only after green acceptance advance to Step 5.
