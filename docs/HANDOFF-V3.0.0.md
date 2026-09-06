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
| Step 2 | ACCEPTED — `0947669c2c096dca93991e042d8ae245754688ba`; Static `34026680871`; Linux `34026680882`, `PASS=31 FAIL=0 SKIP=0` |
| Step 3 implementation | `81e08321222efb03626ac421fc645bd66edd5ae8` — CI pending |
| Step 3 evidence surface | `tests/integration/scientific-article-foreign-elements.sh`; four present/absent scenarios under both engines |
| Current batch | **Scientific Article — Optional foreign elements evidence validation** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

The Step 3 implementation is not accepted merely because it exists. The synchronized branch head must pass Static and full Linux, and the new gate must emit the expected optionality evidence without disturbing accepted non-article profiles.

## Step 3 implementation record

`81e08321222efb03626ac421fc645bd66edd5ae8` adds:

- explicit article-only `\ufcPrintArticleForeignElements{foreign-title}{foreign-summary}`;
- independent blank-safe title and summary rendering;
- four controlled scenarios: neither, title only, summary only, both;
- pdfLaTeX/LuaLaTeX evidence through the permanent scientific-article profile gate;
- source guards that reject `title-variant` repurposing and premature `\AtBeginDocument` body-typography activation;
- no change to the 18-rule article proof state.

Expected structured evidence:

`ARTICLE-FOREIGN-ELEMENTS-EVIDENCE status=PASS engines=2 scenarios=4 title_optional=true summary_optional=true independent=true title_variant_reused=false presentation_rules_promoted=0 recommendations_promoted=0`

## Active authority surfaces

- `release/v3-roadmap.json` — machine state;
- `docs/ROADMAP-V3.0.0.md` — readable roadmap;
- this handoff — current execution checkpoint;
- `docs/V3-SCIENTIFIC-ARTICLE.md` — implementation sequence;
- `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json` — article authority/modality contract;
- `docs/V3-RELEASE-READINESS.md` — release blockers/readiness;
- `docs/UFC-LIBRARIAN-REVIEW.md` — shared 34-point contract.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Immediate action

| Order | Action |
|---:|---|
| 1 | Publish the synchronized Step 3 implementation checkpoint. |
| 2 | Run Static and full Linux on the same branch head. |
| 3 | Require `ARTICLE-FOREIGN-ELEMENTS-EVIDENCE` PASS on both engines and keep the non-article profile matrix green. |
| 4 | Classify any failure before changing runtime or validators. |
| 5 | If green, record Step 3 acceptance and activate Step 4 — textual structure/body typography. |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase/acceptance/evidence state and branch/checkpoint facts must remain synchronized with the roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Targeted Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Do not change article authority, modality, rule IDs or proof state from Step 3 implementation alone.
- Foreign title/summary remain independently optional.
- Do not repurpose `title-variant` for article foreign-title semantics.
- Article body typography remains Step 4 work.
- Recommendations remain advisory.
- Item 33 remains fail-closed.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
