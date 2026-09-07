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
| Steps 1–3 | ACCEPTED |
| Latest fully validated checkpoint | `a99f1e19eac1294eac35fb1da85196a1b8295d1a` |
| Step 4 gate-correction checkpoint | `bf6c48e0cc1e5d19751ad2ff112db77fce799706`; Static `34071163701` PASS; Linux `34071163702` FAIL |
| Current Step 4 runtime implementation | `3796a3c206adb7605160828dcda91f5851a16903` |
| Current work | **Activate article body typography at required front-block completion; acceptance rerun pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 4 failure classification

| Checkpoint | Result | Classification |
|---|---|---|
| `8b52ee4...` | body PDF measured `20.700 pt` vs single calibration `13.800 pt` | real runtime spacing defect |
| `177a621...` | three article gates stopped on retired `AtBeginDocument` token before body PDF check | stale test-token coupling |
| `bf6c48e...` | Static PASS; Linux article scope PASS=4 FAIL=1; body again measured `20.700 pt` vs `13.800 pt` | **real runtime defect remains; `begindocument/end` route is physically ineffective for the required article body** |

The current fix does not relax the checker. `\ufc_article_apply_body_typography:` is now invoked after `\ufc_article_primary_summary:n {#1}` inside the required `\ufcPrintArticleFrontMatter` command. This executes after document startup and before body content. The front-block and foreign-element gates no longer own Step 4 implementation-token assertions; Step 4 remains protected by its dedicated source boundary, two-engine physical measurement and missing-development negative fixture.

## Acceptance gate before Step 5

| Gate | Required |
|---|---|
| Static | PASS on the synchronized correction checkpoint |
| Linux `article` | PASS=5 FAIL=0 |
| Body PDF | 12 pt, justified, 2 cm indent, single spacing under pdfLaTeX and LuaLaTeX |
| Negative structure | missing Desenvolvimento rejected for the intended reason |
| Source boundary | body activation follows required primary summary in the article front block |
| Step 2/3 isolation | front-block and foreign-element gates remain independent of Step 4 implementation syntax |
| Authority/proof state | unchanged |

## Immediate action

1. publish the synchronized checkpoint that contains implementation `3796a3c...` plus this control-plane update;
2. run Static and bounded Linux `article`;
3. classify any failure before changing runtime/tests;
4. if all five article checks pass, record Step 4 acceptance and only then activate Step 5;
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
