# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-06

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active task branch | `feat/v3-scientific-article` |
| Active PR | #286 |
| Active phase | **Scientific Article** |
| Step 1 | ACCEPTED — `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1` |
| Step 2 | ACCEPTED — `0947669c2c096dca93991e042d8ae245754688ba`; Static `34026680871`; Linux `34026680882` |
| Step 3 | ACCEPTED — `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba`; Static `34031144114`; Linux `34031144269` |
| README user guide | ACCEPTED — `a99f1e19eac1294eac35fb1da85196a1b8295d1a`; Static `34054110778`; Linux `34054110738` |
| Step 4 implementation | `e5291137d4753b7d776916ca0f08c67929dbb76b` |
| Rejected Step 4 checkpoint | `8b52ee4b36b23868fecce9bbe9b843f689ccc01e`; Static `34058435312` PASS; Linux `34058435311` FAIL |
| Failure | article body gap `20.700 pt` vs single-spacing calibration `13.800 pt` |
| Active work | **Step 4 body-spacing initialization-order correction implemented; acceptance rerun pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 4 failure classification

Linux `34058435311` executed the bounded `article` scope. `validator-source`, profile, front block and foreign-elements gates passed; `scientific-article-body` failed. The checker measured the article body at the shared academic-work 1.5-spacing gap (`20.700 pt`) while the same-document `\singlesp` calibration was `13.800 pt`.

This is a runtime initialization-order defect, not a checker defect and not a normative-authority dispute. The existing Step 4 body checker remains unchanged.

## Correction applied in the current synchronized checkpoint

`abntexto-ufc/articles.def` retains the `scientific-article` predicate but moves the body typography activation from a generic `\AtBeginDocument` registration to `\AddToHook{begindocument/end}{...}`. This makes the article-only single-spacing override execute after shared begin-document layout initialization.

| Surface | Correction / invariant |
|---|---|
| Runtime | article-only body override runs at `begindocument/end` |
| Typography target | 12 pt, justified, 2 cm first-line indent, zero extra paragraph spacing, single spacing |
| Checker | unchanged; must still distinguish `13.800 pt` single spacing from `20.700 pt` 1.5 spacing |
| Structural negative case | unchanged; missing Desenvolvimento must still be rejected |
| Non-article profiles | no intended runtime change |
| Proof state | unchanged; Step 6 still owns promotion/hardening |

The exact correction SHA is recorded only after this synchronized commit exists. Step 4 remains unaccepted until Static and bounded Linux are green on that checkpoint.

## Current acceptance gate

| Gate | Required result |
|---|---|
| Static | PASS on corrected synchronized Step 4 checkpoint |
| Linux | `article` scope PASS with all five checks |
| Body typography | 12 pt / justified / 2 cm / single under pdfLaTeX and LuaLaTeX |
| Negative structure | missing Desenvolvimento rejected for the intended reason |
| Compatibility | article correction remains profile-scoped |
| Authority | no modality/proof-state strengthening to obtain green CI |

Step 5 — **Recommendations and conditional applicability** — remains blocked until a later documentation checkpoint records Step 4 acceptance.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and required/optional/recommended/conditional distinctions.
- Do not treat shared implementation as article proof.
- Do not weaken the Step 4 spacing checker after the real runtime failure.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
