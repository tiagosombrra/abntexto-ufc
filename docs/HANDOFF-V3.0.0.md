# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active task branch | `feat/v3-scientific-article` |
| Active PR | #286 |
| Active phase | **Scientific Article** |
| Steps 1–3 | ACCEPTED |
| Latest fully validated checkpoint | `a99f1e19eac1294eac35fb1da85196a1b8295d1a` |
| Latest synchronized Step 4 checkpoint | `05194675f7d41d8c4f35227e67e8ee303d1ea79a` |
| Static | `34115345674` — PASS |
| Linux | `34115345586` — FAIL, `SCOPE=article PASS=4 FAIL=1 SKIP=0` |
| Physical body evidence | **PASS under pdfLaTeX and LuaLaTeX**: 12 pt, justified, 2 cm first-line indent, single spacing `13.800 pt` |
| Remaining Step 4 defect | negative structure checker matched `desenvolvimento` in prose instead of requiring a rendered heading |
| Checker correction | `4039fa011b7f54f4f0be6d004131fc0e06567e2e` |
| Current work | **Require structural headings and rerun synchronized Step 4 acceptance** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 4 current classification

| Surface | Result | Classification |
|---|---|---|
| Supported single-spacing API | `\\singlesp`; no deprecated-spacing warning | PASS |
| Textual-transition persistence | `cmd/textual/after` route reached physical body evidence | PASS |
| pdfLaTeX body | 12 pt; indent `57.125 pt`, delta `0.432 pt`; spacing `13.800 pt` | PASS |
| LuaLaTeX body | 12 pt; indent `57.125 pt`, delta `0.432 pt`; spacing `13.800 pt` | PASS |
| Required positive structure | Introduction, Development, Final Considerations, References found | PASS |
| Missing-Development negative | rejected, but for absent `ARTICLEBODYSTART` instead of missing Development | **FAIL — evidence classification defect** |

The runtime spacing defect is therefore physically corrected. Step 4 is not yet accepted because the negative contract requires the fixture to fail for the intended structural reason.

The root cause is in `tests/checks/scientific_article_body.py`: the old structure detector folded the entire extracted PDF and searched for substrings. The negative fixture intentionally says the word `desenvolvimento` in explanatory prose, so that prose incorrectly satisfied the structural predicate.

Correction `4039fa011b7f54f4f0be6d004131fc0e06567e2e` strengthens the detector to match one rendered heading line for each required element, with optional progressive numbering. The negative fixture remains unchanged, so incidental prose can no longer masquerade as a heading. Physical PDF predicates, tolerances, runtime and authority/proof state are unchanged.

## Acceptance gate before Step 5

| Gate | Required |
|---|---|
| Static | PASS on the synchronized checker-correction checkpoint |
| Linux | all five article checks PASS |
| Body PDF | retain 12 pt, justified, 2 cm and 13.800 pt single spacing under both engines |
| Transition persistence | retain physical PASS after automatic `\\textual` transition |
| API compatibility | no deprecated spacing warning |
| Negative structure | missing Development rejected specifically as a missing required heading |
| Step 2/3 isolation | earlier accepted gates remain independent from Step 4 implementation syntax |
| Authority/proof state | unchanged; no proof-state promotion in Step 4 |

## Immediate action

1. publish the synchronized checkpoint containing checker correction `4039fa011...` plus this control-plane update;
2. run Static and Linux on that exact checkpoint;
3. classify any failure before changing runtime/tests;
4. if all five article checks pass and the negative fixture is rejected for the intended reason, record Step 4 acceptance and activate Step 5;
5. later, close Scientific Article only after canonical article PDF visual review and a complete phase-end regression on one immutable SHA.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and modality distinctions.
- Do not weaken warning or physical PDF predicates to compensate for runtime defects.
- Negative fixtures must be rejected for the intended predicate, not an unrelated later error.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
