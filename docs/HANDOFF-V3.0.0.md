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
| Step 4 implementation | `e5291137d4753b7d776916ca0f08c67929dbb76b` |
| Step 4 rejected runtime checkpoint | `8b52ee4b36b23868fecce9bbe9b843f689ccc01e`; Static `34058435312` PASS; Linux `34058435311` FAIL |
| Runtime correction checkpoint | `177a62115e1dc28b24394ed4061600c3a7386fca`; Static `34070809181` PASS; Linux `34070809177` FAIL |
| Current work | **Step 4 stale gate-coupling correction implemented; acceptance rerun pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Failure sequence and classification

| Checkpoint | Result | Classification |
|---|---|---|
| `8b52ee4...` | body PDF measured `20.700 pt` vs single calibration `13.800 pt` | real runtime initialization-order defect |
| `177a621...` | Static PASS; Linux `article` PASS=2 FAIL=3 before physical body check | stale source-gate coupling to literal `\AtBeginDocument{...}` token |

The runtime fix itself was not disproved by `34070809177`: the front-block, foreign-elements and body shell gates stopped at source-token guards before compiling their normal PDF evidence. The profile gate passed.

## Current correction

The runtime remains profile-scoped and registered at `begindocument/end` so it runs after shared layout initialization. The three article integration scripts now protect that accepted semantic route instead of requiring the retired `\AtBeginDocument{...}` spelling.

| Surface | Current rule |
|---|---|
| Runtime ordering | `\AddToHook{begindocument/end}{\ufc_article_apply_body_typography:}` |
| Profile boundary | canonical `scientific-article` predicate remains mandatory |
| Physical spacing evidence | unchanged; must measure true single spacing |
| Front block/foreign elements | still compile and validate under both engines |
| Negative structure | missing Desenvolvimento remains rejected |
| Proof state | unchanged |

The exact synchronized gate-correction SHA is recorded after this commit exists. Step 4 remains unaccepted until Static and bounded Linux pass on it.

## Acceptance gate before Step 5

| Gate | Required |
|---|---|
| Static | PASS |
| Linux `article` | PASS=5 FAIL=0 |
| Body PDF | 12 pt, justified, 2 cm indent, single spacing under pdfLaTeX and LuaLaTeX |
| Negative structure | intended missing-Development rejection |
| Source guards | verify profile-scoped post-shared-initialization route without freezing obsolete hook syntax |
| Authority/proof state | unchanged |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and modality distinctions.
- Do not weaken physical PDF predicates to compensate for runtime defects.
- Do not freeze implementation syntax when semantic/runtime evidence is the contract.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
