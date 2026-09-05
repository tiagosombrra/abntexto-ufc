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
- Engineering-language hardening checkpoint `edeb14b7a96d1cab3ad9551701087ddf4dff059a`: Static `33972111694` and Linux `33972111696` succeeded; the permanent detector reports zero project-owned Portuguese technical diagnostics.
- Current 34-item state: `28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.
- Current bounded batch: **Core Corrections — References**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Immediate action

Continue **Core Corrections — References** with bounded, authority-safe evidence only:

1. add an explicit negative regression proving thesis/dissertation references do not duplicate or contradict the year (item 31 hardening);
2. add a bibliography-specific standard example using the current ABNT publisher/year data already present in the canonical reference corpus (item 32);
3. add a bibliography-specific multivolume physical-description example and evidence without confusing it with the document-pagination `multivolume.sh` gate (item 32);
4. retain existing electronic-resource unknown-publication-data coverage for item 30 and add only reviewer-specific evidence that does not strengthen unresolved NBR 6023:2025 semantics;
5. keep item 33 untouched and fail-closed because DOI/online/repeated-author/corporate-author edge-case clause text remains unavailable;
6. synchronize all affected execution documents in the same material advance;
7. run Static contract and full Linux integration before accepting the bounded reference batch.

## Accepted engineering-language closeout

The strengthened detector progressively exposed previously missed project-owned Portuguese diagnostics in several integration gates. The project corrected the diagnostic surfaces instead of weakening detection. Checkpoint `edeb14...` is accepted because Static `33972111694` and full Linux `33972111696` both passed on the same SHA, with `ENGINEERING-LANGUAGE-EVIDENCE ... portuguese_technical_diagnostics=0`.

Historical failed discovery runs remain useful evidence and are not erased: they demonstrate fail-closed detection and documentation-governance enforcement.

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
