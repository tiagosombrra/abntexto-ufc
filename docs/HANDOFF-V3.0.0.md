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
- Current 34-item state: `28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.
- Engineering-language hardening remains active. Static `33971849196` on synchronized checkpoint `0818bc2c5f50f6f1c60d4cef98d1c85031cb2fcd` passed repository/phase governance checks and then exposed five project-owned Portuguese diagnostics in `tests/integration/backmatter.sh`.
- Current implementation checkpoint `a1c139a6efa8bacefcd3294f01b1f7ed3447a8dd` translates the complete back-matter technical diagnostic surface and normalizes its technical job identifier while preserving Portuguese academic literals under test.
- `a1c139...` is not accepted until a synchronized branch checkpoint passes Static contract and full Linux integration.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Immediate action

Continue **Core Corrections — Engineering Language Evidence Hardening**:

1. publish a synchronized documentation checkpoint on top of `a1c139...`;
2. run normal Static contract and full Linux integration on that exact checkpoint;
3. require `ENGINEERING-LANGUAGE-EVIDENCE` to report zero project-owned Portuguese technical diagnostics;
4. if stronger detection exposes further diagnostics, translate the complete related engineering surface instead of weakening detection;
5. when Static/full Linux are green, close the language-hardening finding and synchronize all control documents;
6. then continue bounded NBR 6023:2025 work for items 30-32, keeping item 33 fail-closed, followed by canonical confirmation for items 1, 2, 7 and 34.

## Failure classification

- Static `33970711005`: fail-closed discovery from stronger language evidence (`algorithm-numbering.sh`).
- Static `33970988780`: temporary documentation-governance drift; no LaTeX runtime regression.
- Static `33971156481`: governance recovered; stronger language evidence exposed catalog-card/duplex/vector diagnostics.
- Static `33971849196`: governance remained green; stronger language evidence exposed the back-matter diagnostic surface.

These failures do not change the 34-item librarian-review classification. They are evidence-governance findings being removed systematically.

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
