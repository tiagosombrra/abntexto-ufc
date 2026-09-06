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
| Step 3 implementation | `81e08321222efb03626ac421fc645bd66edd5ae8` |
| Step 3 synchronized head | `567a5b2d21a16b653d7704639bdd5012d7c2f99b`; Static `34028373064` SUCCESS; Linux `34028373060` classified failure |
| Current batch | **Step 3 evidence correction + scoped Linux integration orchestration** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Linux 34028373060 classification

The former full Linux run reached `profiles` only after all preceding shared checks had passed. All six accepted non-article profiles also compiled successfully under both engines. The failure occurred when `profile-matrix.sh` recursively entered the article profile gate and then `scientific-article-foreign-elements.sh`.

The foreign-elements fixture used only one LaTeX pass before warning inspection, so expected first-pass Biber/cross-reference rerun warnings were treated as a failure. This is an **evidence orchestration defect**. It does not establish an article runtime, authority, modality, proof-state, or non-article compatibility failure.

The bounded correction:

- gives each foreign-elements scenario two LaTeX passes before warning inspection;
- makes article profile, required-front-block, and foreign-elements gates first-class checks in `tests/run.py`;
- removes recursive article execution from the non-article profile matrix;
- removes recursive Step 2/3 execution from the profile gate;
- adds named Linux integration scopes and incremental PR scope inference.

No article runtime or normative contract changes in this correction.

## Scoped Linux integration model

| Scope | Purpose |
|---|---|
| `article` | article authority/profile/front-block/foreign-element evidence |
| `profiles` | six accepted non-article profiles plus build-path/multivolume/catalog-card |
| `reference-document`, `reference-pdf` | canonical reference document/presentation |
| `frontmatter`, `layout`, `objects`, `bibliography`, `backmatter` | bounded shared domains |
| `research-project` | research-project-specific integration |
| `smoke` | orchestration-only changes |
| `complete` | shared/unknown technical changes and mandatory phase-end regression |
| `auto` | infer safe scope from changed paths |

On PR `synchronize`, `auto` compares the previous head with the new head. This prevents the complete historical PR diff from forcing a giant run after every small article commit. Opened/reopened/ready events still use the full PR diff. Unknown technical paths fail closed to `complete`.

The implementation contract is `docs/LINUX-INTEGRATION-SCOPES.md`.

## Step 3 acceptance rule

Step 3 remains **IMPLEMENTED / ACCEPTANCE PENDING** until one synchronized checkpoint proves:

1. Static contract PASS, including the Linux-scope static contract;
2. bounded Linux scope containing `profiles,article` PASS for this orchestration migration;
3. `ARTICLE-PROFILE-EVIDENCE`, `ARTICLE-FRONT-BLOCK-EVIDENCE`, and `ARTICLE-FOREIGN-ELEMENTS-EVIDENCE` PASS;
4. non-article profiles remain green;
5. no article rule modality or proof-state drift.

After this one migration checkpoint, ordinary article-only changes should normally select `article` rather than the complete repository matrix.

## Immediate action

| Order | Action |
|---:|---|
| 1 | Publish the synchronized scoped-integration + Step 3 evidence-fix checkpoint. |
| 2 | Require Static PASS and verify the PR Linux run selects `profiles,article`, not `complete`. |
| 3 | Classify any bounded-run failure before modifying runtime or tests. |
| 4 | If green, update docs/machine state with exact checkpoint and run IDs; Step 3 may become ACCEPTED. |
| 5 | Activate Step 4 — textual structure/body typography. |
| 6 | Continue using `article` for article-only intermediate work. |
| 7 | Preserve `complete` for the immutable Scientific Article phase-end regression. |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase/acceptance/evidence/integration-scope state and branch/checkpoint facts must remain synchronized with roadmap and machine state.

Every phase requires a complete **phase-end regression** on one immutable candidate before closure. Scoped Step checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve all accepted non-article profiles and the shared academic-work PDF baseline.
- Do not change article authority, modality, rule IDs or proof state from this orchestration correction.
- Foreign title/summary remain independently optional.
- Do not repurpose `title-variant`.
- Article body typography remains Step 4 work.
- Recommendations remain advisory.
- Item 33 remains fail-closed.
- Issue #18 remains owned by Final Certification/Release.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
