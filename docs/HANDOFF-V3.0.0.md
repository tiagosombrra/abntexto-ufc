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
- Language-hardening checkpoint `fd3727d89848eb52a9c79021cd9765ad9e1806db`: Static `33970711005` failed after the stronger detector exposed a Portuguese project-owned diagnostic in `algorithm-numbering.sh`.
- Correction implementation `5c5b9593cd12f3b6fa3108b579514c3c25edcb54` translates the full diagnostic surface in that gate and expands detector/self-test coverage.
- First synchronized correction checkpoint `6c23a49a86944d646db35b56af877d3bb351c0ec`: Static `33970988780` failed because a shortened roadmap dropped the required `material advance` governance concept. The same concept is restored in both roadmap and correction plan before rerun.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Immediate action

Continue **Core Corrections — Engineering Language Evidence Hardening**:

1. publish the governance-corrected synchronized checkpoint containing implementation `5c5b9593cd12f3b6fa3108b579514c3c25edcb54`;
2. run normal Static contract and full Linux integration;
3. require the strengthened language audit/self-test to report zero project-owned Portuguese technical diagnostics;
4. if more diagnostics are exposed, correct them rather than weakening detection;
5. if governance checks expose documentation drift, reconcile the control plane before feature work;
6. when Static/full Linux are green, close the language-hardening finding and update all control documents;
7. then continue bounded NBR 6023:2025 work for items 30-32, keeping item 33 fail-closed, followed by canonical confirmation for items 1, 2, 7 and 34.

## Failure classification

Static `33970711005` is an expected fail-closed discovery from stronger language evidence. Static `33970988780` is a separate documentation-governance failure introduced by a control-document rewrite; it does not indicate a LaTeX runtime regression. Both are recorded rather than hidden.

The governance correction explicitly restores the required concepts `material advance` and `phase-end regression` in both roadmap and correction plan, matching the permanent `phase_governance.py` contract.

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
