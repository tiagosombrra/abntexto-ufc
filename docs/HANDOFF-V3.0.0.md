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
- Engineering-language discovery checkpoints remain classified: Static `33970711005` exposed `algorithm-numbering.sh`; Static `33970988780` exposed a temporary roadmap governance omission; Static `33971156481` confirmed governance recovery and then exposed four more project-owned Portuguese diagnostics in catalog-card, duplex-backmatter, table-IBGE-vector and vector-rule-validation integration gates.
- Current implementation checkpoint: `1129935fe5e4f97d6fe3798fd5e4777760f0d61b`. It translates the newly exposed diagnostic surfaces and expands `engineering_language.py` self-test coverage to 18 cases while preserving academic Portuguese.
- `1129935...` is not accepted until a synchronized branch checkpoint passes Static contract and full Linux integration.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Immediate action

Continue **Core Corrections — Engineering Language Evidence Hardening**:

1. publish a synchronized documentation checkpoint on top of `1129935...`;
2. run normal Static contract and full Linux integration on that exact branch checkpoint;
3. require `ENGINEERING-LANGUAGE-EVIDENCE` to report zero project-owned Portuguese technical diagnostics and require the 18-case self-test to pass;
4. if stronger detection exposes further diagnostics, inspect and translate the complete related engineering surface rather than weakening detection;
5. when Static/full Linux are green, close the language-hardening finding and synchronize all control documents;
6. then continue bounded NBR 6023:2025 work for items 30-32, keeping item 33 fail-closed, followed by canonical confirmation for items 1, 2, 7 and 34.

## Failure classification

- Static `33970711005`: expected fail-closed discovery from stronger language evidence.
- Static `33970988780`: documentation-governance regression caused by a shortened roadmap; no LaTeX runtime regression. The required `material advance` / `phase-end regression` wording was restored.
- Static `33971156481`: phase governance passed, then stronger language evidence exposed four additional old technical diagnostics. This is another expected hardening discovery.

None of these failures changes the 34-item librarian-review state. The language finding remains an evidence-governance task until a synchronized green checkpoint exists.

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
