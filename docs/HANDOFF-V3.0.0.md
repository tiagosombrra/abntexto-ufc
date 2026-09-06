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

## Active Step 4 contract

Step 4 implements and validates the required article textual structure and body typography. The retained article authority contract requires executable article-specific evidence for:

- `article.introduction.required`;
- `article.development.required`;
- `article.final-considerations.required`;
- `article.references.required`;
- `article.body.typography`.

The frozen body presentation values are 12 pt text, justified alignment, 2 cm first-line indentation and single line spacing.

Runtime or shared-mechanism reuse alone is not proof. Step 4 must introduce a bounded article fixture/checker/gate, add that executable gate to the `article` Linux scope in the same material advance, preserve all six non-article profiles, and avoid proof-state promotion until the article-specific evidence is accepted.

## README correction

`README.md` is now treated as the end-user entry point rather than a development diary. It should explain how to select the stable release, use the Overleaf/local bundles, configure the document, compile it and solve common usage problems. Workflow IDs, implementation SHAs, issue chronology, regression history and detailed control-plane state remain in engineering documents and GitHub.

Until v3.0.0 is released, the README must clearly direct normal users to stable v2.1.0 and must not present `main` or `scientific-article` as released functionality.

## Immediate action

| Order | Action |
|---:|---|
| 1 | Keep this Step 3 acceptance and README usability correction synchronized with roadmap and machine state. |
| 2 | Inspect the current article runtime/section infrastructure before designing Step 4 implementation. |
| 3 | Implement one bounded Step 4 article structure/body-typography route without forking shared infrastructure. |
| 4 | Add article-specific positive evidence and a controlled negative path where safe. |
| 5 | Add the Step 4 executable gate to the `article` Linux scope in the same material advance. |
| 6 | Run Static and bounded article/profile Linux acceptance on the synchronized Step 4 checkpoint. |
| 7 | Classify any failure before changing runtime, authority or tests. |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, evidence, integration-scope and branch/checkpoint facts must remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Preserve the 18-rule article source contract and required/optional/recommended/conditional distinctions.
- Do not treat shared implementation as article proof.
- Do not weaken normative traceability or scope fail-closed behavior.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
