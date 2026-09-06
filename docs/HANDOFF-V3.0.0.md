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
| Article Step 1 | ACCEPTED — `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`; Static `34001350884`; Linux `34001350953` |
| Article Step 2 | ACCEPTED — `0947669c2c096dca93991e042d8ae245754688ba`; Static `34026680871`; Linux `34026680882`, `PASS=31 FAIL=0 SKIP=0` |
| Article Step 2 evidence | `ARTICLE-PROFILE-EVIDENCE` PASS plus `ARTICLE-FRONT-BLOCK-EVIDENCE` PASS on pdfLaTeX and LuaLaTeX |
| Current batch | **Scientific Article — Optional foreign elements (Step 3)** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

Step 2 acceptance does not promote article rules in `standards/coverage-rules-article.json`; the rule contract remains manual/conditional-manual until the dedicated evidence-hardening step.

## Active authority surfaces

- `release/v3-roadmap.json` — machine state;
- `docs/ROADMAP-V3.0.0.md` — readable phase roadmap;
- this handoff — current execution checkpoint;
- `docs/V3-SCIENTIFIC-ARTICLE.md` — active implementation sequence;
- `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json` — article authority/modality contract;
- `docs/V3-RELEASE-READINESS.md` — release blockers and repository readiness;
- `docs/UFC-LIBRARIAN-REVIEW.md` — protected 34-point shared review contract.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Step 2 acceptance record

The earlier Linux failure `34003838521` was classified as a validator-predicate defect because the checker imposed an unsupported physical-page-height threshold on a genuine `\footnote` route. The validator correction preserved the semantic footnote requirement and rendered 10 pt footnote evidence.

The synchronized checkpoint `0947669c2c096dca93991e042d8ae245754688ba` then passed:

- Static `34026680871` — SUCCESS;
- full Linux `34026680882` — SUCCESS, `PASS=31 FAIL=0 SKIP=0`;
- `ARTICLE-PROFILE-EVIDENCE status=PASS engines=2`;
- `ARTICLE-FRONT-BLOCK-EVIDENCE status=PASS` on both engines;
- all shared/non-article checks remained green.

Therefore Step 2 is accepted and Step 3 is the only active implementation step.

## Step 3 contract — Optional foreign elements

The next bounded implementation must:

1. support a foreign-language title optionally;
2. support a foreign-language summary optionally;
3. allow each element to be independently absent or present;
4. compile cleanly when both are absent;
5. use an explicit article-only route rather than repurposing shared `title-variant` semantics;
6. avoid promoting optional elements into requirements;
7. avoid freezing unsupported typography values as normative claims;
8. exercise present/absent behavior under pdfLaTeX and LuaLaTeX;
9. leave Step 4 article body typography untouched;
10. update all operational documentation with the implementation checkpoint before CI.

## Immediate action

| Order | Action |
|---:|---|
| 1 | Implement Step 3 optional foreign elements and article-specific fixtures/evidence. |
| 2 | Update plan, handoff, roadmap, release readiness and machine state in the same material advance. |
| 3 | Run Static and full Linux on the synchronized branch head. |
| 4 | Classify any failure before changing runtime or validators. |
| 5 | If green, record Step 3 acceptance and activate Step 4. |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase/acceptance/evidence state and branch/checkpoint facts must remain synchronized with the roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Targeted Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the visually accepted shared academic-work PDF baseline.
- Do not change article authority, modality, rule IDs or proof state without explicit evidence and documentation.
- Do not turn recommendations into hard failures.
- Item 33 remains fail-closed.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
