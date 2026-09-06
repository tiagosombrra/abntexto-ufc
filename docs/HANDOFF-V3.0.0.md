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
| Step 3 | **ACCEPTED** — `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba`; Static `34031144114`; Linux `34031144269` |
| Active work | **Step 4 — textual structure and body typography** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Step 3 acceptance

The synchronized Step 3 checkpoint `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba` passed both required bounded gates:

| Gate | Result |
|---|---|
| Static contract | `34031144114` — SUCCESS |
| Linux integration | `34031144269` — SUCCESS |
| Scope-fallback contract | accepted; unavailable incremental endpoints fall back fail-closed instead of crashing |
| Article profile | accepted under the Step 3 executable suite |
| Required front block | remained green |
| Optional foreign elements | accepted for independently optional title/summary scenarios under both engines |
| Non-article compatibility | exactly six non-article profiles remain the compatibility matrix; `scientific-article` remains separate |
| Normative/proof-state boundary | no authority, modality or proof-state promotion was introduced by the orchestration fixes |

Earlier Step 3 failures remain historical evidence of defects that were corrected before acceptance. They no longer represent the active state.

## README usability correction

The root README is being corrected from an internal execution/history page into the end-user entry point. It now prioritizes stable-release selection, Overleaf/local setup, document structure, configuration, compilation and common user problems.

Documentation checkpoint `3e3ece5a3607303dd31aee35c67ce4140fb90d94` was rejected by Static `34053874788`. The failure was narrow and useful: the user guide accurately named the retired stable class while explaining v2.1.0, but `tests/checks/canonical_identity.py` correctly treats unclassified legacy identity in the active V3 tree as a regression. Linux `34053874750` completed successfully for the documentation-only checkpoint.

Classification: **README/canonical-identity documentation conflict**, not a runtime, article, authority or Step 3 regression. The correction keeps the stable v2.1.0 download/onboarding instructions, removes the retired identity from active README text, and leaves `canonical_identity.py` unchanged.

`AGENTS.md` now makes the ownership boundary explicit: README is user onboarding; SHAs, workflow runs, issue chronology, normative disputes and control-plane history belong in engineering documents and GitHub.

## Active Step 4 contract

Step 4 implements and validates the required article textual structure and body typography. The retained article authority contract requires executable article-specific evidence for:

- `article.introduction.required`;
- `article.development.required`;
- `article.final-considerations.required`;
- `article.references.required`;
- `article.body.typography`.

The frozen body presentation values are 12 pt text, justified alignment, 2 cm first-line indentation and single line spacing.

Runtime or shared-mechanism reuse alone is not proof. Step 4 must introduce a bounded article fixture/checker/gate, add that executable gate to the `article` Linux scope in the same material advance, preserve all six non-article profiles, and avoid proof-state promotion until the article-specific evidence is accepted.

## Immediate action

| Order | Action |
|---:|---|
| 1 | Validate the corrected user-facing README under Static without weakening canonical identity. |
| 2 | Keep Step 3 acceptance and README correction synchronized with roadmap and machine state. |
| 3 | Inspect the current article runtime/section infrastructure before designing Step 4 implementation. |
| 4 | Implement one bounded Step 4 article structure/body-typography route without forking shared infrastructure. |
| 5 | Add article-specific positive evidence and a controlled negative path where safe. |
| 6 | Add the Step 4 executable gate to the `article` Linux scope in the same material advance. |
| 7 | Run Static and bounded article/profile Linux acceptance on the synchronized Step 4 checkpoint. |
| 8 | Classify any failure before changing runtime, authority or tests. |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts must remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the 18-rule article source contract and required/optional/recommended/conditional distinctions.
- Do not treat shared implementation as article proof.
- Do not weaken normative traceability, canonical identity or scope fail-closed behavior.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
