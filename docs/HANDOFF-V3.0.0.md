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
| Latest rejected Step 4 checkpoint | `09b870d0f7f3771884d55e2e922921051df2dfe0`; Static `34072362333` PASS; Linux `34072362335` FAIL |
| Current Step 4 implementation | `15ed414d3f1474157fe2e34de2d97ae6e76dd5ff` |
| Current work | **Persist article single spacing across the upstream `textual` transition; acceptance rerun pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 4 failure classification

| Checkpoint | Result | Classification |
|---|---|---|
| `8b52ee4...` | body PDF measured `20.700 pt` vs single calibration `13.800 pt` | real runtime spacing defect |
| `177a621...` | three article gates stopped on retired `AtBeginDocument` token before body PDF check | stale test-token coupling |
| `bf6c48e...` | Static PASS; Linux article PASS=4 FAIL=1; body again `20.700 pt` vs `13.800 pt` | begin-document route physically ineffective |
| `09b870d...` | Static `34072362333` PASS; Linux `34072362335` PASS=4 FAIL=1; body still `20.700 pt` vs `13.800 pt` | front-block-only activation also transient; first section resets shared spacing through `\textual` |

The latest failure isolates the upstream state transition. `abntexto`'s first numbered section invokes `\textual`, which sets `\spacing{1.5}` and a 1.5 cm paragraph indent. `\singlesp` changes the current baseline only and does not replace that persistent spacing state.

Implementation `15ed414d3f1474157fe2e34de2d97ae6e76dd5ff` therefore uses `\spacing{1}` inside the article-only body function and re-applies it through `cmd/textual/after`. The same function still runs after the required primary summary so body content before the first section is also correct. The article type guard remains the isolation boundary for non-article profiles.

## Acceptance gate before Step 5

| Gate | Required |
|---|---|
| Static | PASS on the synchronized correction checkpoint |
| Linux `article` | PASS=5 FAIL=0 |
| Body PDF | 12 pt, justified, 2 cm indent, single spacing under pdfLaTeX and LuaLaTeX |
| Persistent state | body spacing survives the automatic `\textual` transition |
| Negative structure | missing Desenvolvimento rejected for the intended reason |
| Step 2/3 isolation | earlier accepted gates remain independent of Step 4 implementation syntax |
| Authority/proof state | unchanged |

## Immediate action

1. publish the synchronized checkpoint containing implementation `15ed414d...` plus this control-plane update;
2. run Static and bounded Linux `article`;
3. classify any failure before changing runtime/tests;
4. if all five article checks pass, record Step 4 acceptance and activate Step 5;
5. later, close Scientific Article only after canonical article PDF visual review and a complete phase-end regression on one immutable SHA.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and modality distinctions.
- Do not weaken physical PDF predicates to compensate for runtime defects.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
