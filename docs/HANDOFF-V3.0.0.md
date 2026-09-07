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
| Latest rejected synchronized Step 4 checkpoint | `49e7b179f7de9274f1cbf01fefed20ce04eae8e0`; Static `34111737479` PASS; Linux `34111737488` FAIL, `SCOPE=complete PASS=32 FAIL=2 SKIP=1` |
| Current Step 4 implementation | `6a7ef821875c40b6fe0bbc3cca25e3c0ff4cb307` |
| Current work | **Use supported `\\singlesp` and reapply article typography after `\\textual`; acceptance rerun pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 4 failure classification

| Checkpoint | Result | Classification |
|---|---|---|
| `8b52ee4...` | body PDF measured `20.700 pt` vs single calibration `13.800 pt` | real runtime spacing defect |
| `177a621...` | three article gates stopped on retired `AtBeginDocument` token before body PDF check | stale test-token coupling |
| `bf6c48e...` | Static PASS; Linux article PASS=4 FAIL=1; body again `20.700 pt` vs `13.800 pt` | begin-document route physically ineffective |
| `09b870d...` | Static `34072362333` PASS; Linux `34072362335` PASS=4 FAIL=1; body still `20.700 pt` vs `13.800 pt` | front-block-only activation transient; first section resets shared spacing through `\\textual` |
| `49e7b17...` | Static `34111737479` PASS; Linux `34111737488` `SCOPE=complete PASS=32 FAIL=2 SKIP=1` | deprecated `\\spacing{1}` warning stopped article front-block/body checks before physical body validation |

The `49e7...` result narrows the defect again. Reapplying article typography after `\\textual` remains necessary, but `\\spacing{1}` is an obsolete upstream API and cannot be accepted by the repository warning policy. The physical body checker was not reached in that run, so no physical Step 4 acceptance is inferred from it.

Implementation `6a7ef821875c40b6fe0bbc3cca25e3c0ff4cb307` replaces `\\spacing{1}` with supported `\\singlesp`, retains `cmd/textual/after`, and keeps activation after the required summary. The dedicated body source gate now requires the supported route and explicitly rejects a regression to deprecated `\\spacing{1}`. Physical predicates remain unchanged.

## Acceptance gate before Step 5

| Gate | Required |
|---|---|
| Static | PASS on the synchronized correction checkpoint |
| Linux | all five article checks PASS; complete scope may run when selected by orchestration |
| Body PDF | 12 pt, justified, 2 cm indent, single spacing under pdfLaTeX and LuaLaTeX |
| Transition persistence | body spacing and 2 cm indent survive the automatic `\\textual` transition |
| API compatibility | no deprecated `\\spacing` warning; supported `\\singlesp` route |
| Negative structure | missing Desenvolvimento rejected for the intended reason |
| Step 2/3 isolation | earlier accepted gates remain independent of Step 4 implementation syntax |
| Authority/proof state | unchanged |

## Immediate action

1. publish the synchronized checkpoint containing implementation `6a7ef821...` plus this control-plane update;
2. run Static and Linux on that exact synchronized checkpoint;
3. classify any failure before changing runtime/tests;
4. if all five article checks pass with physical body evidence, record Step 4 acceptance and activate Step 5;
5. later, close Scientific Article only after canonical article PDF visual review and a complete phase-end regression on one immutable SHA.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and modality distinctions.
- Do not weaken warning or physical PDF predicates to compensate for runtime defects.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
