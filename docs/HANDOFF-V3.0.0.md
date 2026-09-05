# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Core Corrections**.
- Pre-regression baseline: `c4bf51b574647226ee488440579ec2a204c16c79`.
- Regression planning checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`.
- Regression baseline Static `33937439818`: success; Linux `33937439846`: success.
- Object/Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`: Static `33965794475` success; Linux `33965794519` success, `PASS=31 FAIL=0 SKIP=0`.
- Canonical-reference source checkpoint `3ae9dd698e021a117ba2b64ebf970dc8c507fa8f`: Static `33968579418` success; Linux `33968579449` success, `PASS=31 FAIL=0 SKIP=0`.
- Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c`: Static `33969505681` success; Linux `33969505614` success, `PASS=31 FAIL=0 SKIP=0`; items 11, 16 and 28 closed.
- Current 34-item state: `28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.
- Engineering-language synchronized checkpoint `fd3727d89848eb52a9c79021cd9765ad9e1806db`: Static `33970711005` failed because the stronger detector exposed an additional Portuguese project-owned diagnostic in `tests/integration/algorithm-numbering.sh`.
- Current correction implementation: `5c5b9593cd12f3b6fa3108b579514c3c25edcb54`, translating all diagnostics in that gate and expanding the detector/self-test. Synchronized acceptance is pending.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents:

- `release/v3-roadmap.json`
- `docs/ROADMAP-V3.0.0.md`
- `docs/V3-CORRECTION-PLAN.md`
- `docs/UFC-LIBRARIAN-REVIEW.md`
- `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`
- `docs/V3-REGRESSION-AUDIT.md`
- `docs/ENGINEERING-LANGUAGE.md`

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Immediate action

Continue **Core Corrections — Engineering Language Evidence Hardening**:

1. publish a synchronized checkpoint containing correction `5c5b9593cd12f3b6fa3108b579514c3c25edcb54` plus this documentation state;
2. run normal Static contract and full Linux integration;
3. require the strengthened detector/self-test to pass with zero project-owned Portuguese technical diagnostics;
4. if additional diagnostics are exposed, correct them rather than weakening detection;
5. when Static/full Linux are green, close this evidence-hardening finding and synchronize all control documents;
6. continue bounded NBR 6023:2025 work for items 30-32 while keeping item 33 fail-closed;
7. finish canonical confirmation for items 1, 2, 7 and 34, then freeze the Core Corrections phase-end candidate.

## Engineering-language failure classification

Static run `33970711005` is classified as an expected fail-closed discovery from stronger evidence coverage. It found `tests/integration/algorithm-numbering.sh:66` with a project-owned Portuguese failure message. Inspection of that gate showed additional Portuguese/mixed diagnostics in the same script, so the correction translates the entire diagnostic surface rather than patching only the first reported line.

The detector is also expanded for the newly exposed line-numbering phrase family and its self-test grows from 11 to 13 cases. This is test/evidence strengthening, not runtime-document behavior change.

## Mandatory operating discipline

Every material advance updates the relevant execution documentation and this handoff in the same work cycle. Phase state, acceptance state, current correction batch, evidence state, and machine-readable facts must also be synchronized in `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json`.

Every phase requires a phase-end regression before closure. Targeted checks are necessary evidence for individual corrections but never authorize a phase transition by themselves.

## Hard boundaries

- Do not resume Scientific Article while Core Corrections or Reference PDF Validation are open.
- Preserve the closed V3 public API unless current evidence explicitly authorizes a change.
- Do not translate reviewer comments directly into normative runtime behavior when current authority remains unresolved.
- Do not weaken tests merely to recover green CI.
- Do not close a phase on targeted checks alone.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
