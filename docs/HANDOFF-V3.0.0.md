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
| Active work | **Step 4 implemented — Static/Linux acceptance pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 4 material advance

The Step 4 implementation is intentionally bounded to the article profile.

| Surface | Change | Acceptance meaning |
|---|---|---|
| `articles.def` | article-only begin-document body activation: 12 pt, justified, 2 cm first-line indent, zero extra paragraph spacing, single spacing | runtime requirement implemented without changing non-article profiles |
| Positive fixture | Introdução, Desenvolvimento, Considerações finais and Referências | required textual structure can be proved on an article-specific PDF |
| PDF checker | physical 12 pt, 2 cm indent, justification and single-spacing measurements | shared implementation is not used as proof |
| Negative fixture | omits Desenvolvimento | validator must reject deterministically |
| Step 2/3 guards | pre-Step4 ban on `\AtBeginDocument` replaced by positive profile-scoped Step4 boundary | old protection is transitioned rather than deleted |
| Coordinated runner | new `scientific-article-body` check | Step 4 is independently executable |
| `article` Linux suite | new body check added and statically required | scoped CI cannot omit Step 4 |
| Proof state | unchanged | Step 6 still owns proof-state hardening/promotion |

Implementation commit: `e5291137d4753b7d776916ca0f08c67929dbb76b`. The branch is published only after the documentation/machine-state commit on top of that implementation, so CI evaluates the synchronized state.

## Current acceptance gate

| Gate | Required result |
|---|---|
| Static | PASS on the synchronized Step 4 checkpoint |
| Linux | bounded `article` scope PASS with profile/front-block/foreign/body checks |
| Positive body evidence | both pdfLaTeX and LuaLaTeX physical measurements PASS |
| Negative structure | missing Desenvolvimento rejected for the intended reason |
| Compatibility | no change to six accepted non-article profiles/shared foundation |
| Authority | no article modality or proof-state strengthening solely to get green CI |

Any failure is classified before runtime/test changes. Step 4 remains unaccepted until both required CI gates are recorded green.

## Next step after acceptance

Step 5 — **Recommendations and conditional applicability** — may start only after a later documentation checkpoint records the Step 4 Static/Linux results. Recommendations remain advisory and journal-specific instructions remain required only when applicable.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the retained 18-rule article source contract and required/optional/recommended/conditional distinctions.
- Do not treat shared implementation as article proof.
- Do not weaken normative traceability, canonical identity or scope fail-closed behavior.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
