# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Core Corrections**.
- Regression baseline: `c4bf51b574647226ee488440579ec2a204c16c79`; Static `33937439818` and Linux `33937439846` succeeded.
- Object/Core checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`: Static `33965794475` and Linux `33965794519` succeeded, `PASS=31 FAIL=0 SKIP=0`.
- Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c`: Static `33969505681` and Linux `33969505614` succeeded, `PASS=31 FAIL=0 SKIP=0`; librarian items 11, 16 and 28 closed.
- Engineering-language hardening checkpoint `edeb14b7a96d1cab3ad9551701087ddf4dff059a`: Static `33972111694` and Linux `33972111696` succeeded; permanent detector reports zero project-owned Portuguese technical diagnostics.
- Current 34-item state: `28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.
- Current bounded batch: **Core Corrections — References**.
- Reference evidence implementation `63d20de2894e6ba4149bac0b2aba3efeb1aef27f` adds controlled reviewer-specific cases for items 30-32; acceptance is pending synchronized Static/full Linux.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Current reference implementation

Implementation `63d20de...` is intentionally evidence-only: it does not change `abntexto-ufc/standards/nbr6023-2025.def` or any normative runtime rule.

It adds:

1. reviewer-specific evidence that an online entry without location/publisher does not receive unknown-publication markers under the already-established compatibility behavior (item 30);
2. a controlled thesis/dissertation entry whose work type, institution/location and single consistent year are checked explicitly (item 31 hardening);
3. a controlled ABNT standard entry checking publisher/year data and a bibliography-specific `@mvbook` entry checking the reviewed `2 v.` physical description (item 32);
4. explicit `LIBRARIAN-REVIEW-EVIDENCE` lines for items 30, 31 and 32.

The existing `tests/integration/multivolume.sh` remains document-pagination evidence only and is not reused as bibliography evidence.

## Immediate action

1. publish the synchronized checkpoint containing implementation `63d20de...` and these control-document updates;
2. run Static contract and full Linux integration on that exact checkpoint;
3. if the multivolume `@mvbook` expectation does not render as reviewed, classify the evidence failure and do not change runtime without sufficient authority;
4. if both gates pass, promote item 32 from PARTIAL to PASS and update the 34-item matrix to `29 PASS / 4 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`;
5. then continue canonical confirmation for items 1, 2, 7 and 34;
6. keep item 33 untouched/fail-closed.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase/acceptance/evidence state and branch/checkpoint facts must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Targeted checks never authorize a phase transition by themselves.

## Hard boundaries

- Do not resume Scientific Article while Core Corrections or Reference PDF Validation are open.
- Preserve the closed V3 public API unless current evidence explicitly authorizes a change.
- Do not translate reviewer comments directly into normative runtime behavior when current authority remains unresolved.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
