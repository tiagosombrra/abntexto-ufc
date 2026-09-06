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
| README user-guide correction | **ACCEPTED** — `a99f1e19eac1294eac35fb1da85196a1b8295d1a`; Static `34054110778`; Linux `34054110738` |
| Active work | **Step 4 — textual structure and body typography** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## README acceptance

The root README is now accepted as the end-user entry point rather than an execution-history page.

| Checkpoint | Result |
|---|---|
| Rejected first rewrite | `3e3ece5a3607303dd31aee35c67ce4140fb90d94`; Static `34053874788` rejected unclassified retired class identity; Linux `34053874750` succeeded |
| Corrected user guide | `a99f1e19eac1294eac35fb1da85196a1b8295d1a` |
| Static | `34054110778` — SUCCESS |
| Linux | `34054110738` — SUCCESS |

The accepted README directs normal users to stable v2.1.0, explains Overleaf/local setup, document structure, configuration, compilation and common problems, and keeps detailed SHAs/runs/issues/regression history out of user onboarding. The canonical-identity gate was not weakened.

## Step 3 acceptance

The synchronized Step 3 checkpoint `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba` passed Static `34031144114` and Linux `34031144269`. Optional foreign title/summary scenarios, scope fallback and the six-profile non-article compatibility boundary are accepted. Earlier failures remain historical evidence only.

## Active Step 4 contract

Step 4 implements and validates the required article textual structure and body typography. It owns:

- `article.introduction.required`;
- `article.development.required`;
- `article.final-considerations.required`;
- `article.references.required`;
- `article.body.typography`.

The frozen body presentation values are 12 pt text, justified alignment, 2 cm first-line indentation and single line spacing.

The shared academic-work layout currently activates 1.5 line spacing globally. Therefore Step 4 must use the smallest profile-specific override for `scientific-article`; simply reusing shared layout is not sufficient evidence. The implementation must remain isolated from the six accepted non-article profiles.

## Immediate action

| Order | Action |
|---:|---|
| 1 | Inspect existing article/shared layout and PDF checker patterns. |
| 2 | Implement the smallest article-only body-typography activation. |
| 3 | Add one article fixture proving introduction, development, final considerations and references. |
| 4 | Add physical PDF evidence for 12 pt, justification, 2 cm first-line indent and single spacing. |
| 5 | Add a controlled negative path where the checker can reject a missing required structure. |
| 6 | Register the Step 4 executable gate in `tests/run.py` and the `article` Linux suite in the same material advance. |
| 7 | Synchronize this handoff, roadmap, execution plan and machine state. |
| 8 | Require Static + bounded article/profile Linux PASS before Step 4 acceptance. |

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
