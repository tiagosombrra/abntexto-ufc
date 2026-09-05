# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Core Corrections**.
- Pre-regression baseline: `c4bf51b574647226ee488440579ec2a204c16c79`.
- Regression planning checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`.
- Regression baseline Static `33937439818`: success.
- Regression baseline Linux `33937439846`: success.
- Object/Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`: Static `33965794475` success; Linux `33965794519` success, `PASS=31 FAIL=0 SKIP=0`.
- Canonical-reference source checkpoint `3ae9dd698e021a117ba2b64ebf970dc8c507fa8f`: Static `33968579418` success; Linux `33968579449` success, `PASS=31 FAIL=0 SKIP=0`.
- Source-level librarian evidence for items 11, 16 and 28 is accepted at `3ae9dd...`.
- Current implementation checkpoint: `a1149f169f06b2db620bc5df69d0870b60fe583c`, adding compiled canonical-PDF text evidence for items 11, 16 and 28. Branch acceptance is pending.
- Current 34-item state: `25 PASS / 8 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` until generated-PDF acceptance closes any of those items.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents:

- `release/v3-roadmap.json`
- `docs/ROADMAP-V3.0.0.md`
- `docs/V3-CORRECTION-PLAN.md`
- `docs/UFC-LIBRARIAN-REVIEW.md`
- `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`
- `docs/V3-REGRESSION-AUDIT.md`

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Mandatory operating discipline

Every material advance updates the relevant execution documentation and this handoff in the same work cycle. Phase state, acceptance state, current correction batch, evidence state, and machine-readable facts must also be synchronized in `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json`.

Every phase requires a phase-end regression before closure. Targeted checks are necessary evidence for individual corrections but never authorize a phase transition by themselves.

## Immediate action

Continue **Core Corrections — Canonical Reference Content**:

1. publish the synchronized branch checkpoint containing `a1149f169f06b2db620bc5df69d0870b60fe583c` plus this documentation state;
2. require normal Static contract and full Linux integration on that checkpoint;
3. inspect the `Reference document` gate for explicit generated-PDF evidence lines for items 11, 16 and 28;
4. if green, reclassify items 11, 16 and 28 from PARTIAL to PASS and synchronize all control documents; expected review totals become `28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`;
5. then fix the newly identified engineering-language coverage gap: mixed Portuguese/English project-owned diagnostics in `tests/integration/multivolume.sh` and `tests/integration/references-6023.sh` currently evade the static language detector; strengthen the detector without flagging legitimate academic Portuguese and translate the affected diagnostics;
6. continue bounded reference work for items 30-32 without changing item 33 absent authoritative current-edition evidence.

After those bounded corrections, finish canonical front-matter and annex confirmation, then freeze one Core Corrections phase-end candidate and run the complete Static/full Linux phase-end regression.

## Newly classified regression finding

The latest source-level acceptance exposed an independent evidence-quality issue: `tests/checks/engineering_language.py` reports zero Portuguese project-owned technical diagnostics, but mixed diagnostics remain in at least `multivolume.sh` and `references-6023.sh`. The current term matcher does not detect phrases such as `após a cover`, `não continuou`, `identificação completa`, `não aparece`, or the mixed NBR 6023 diagnostic using `após a data`.

This is not a runtime formatting defect, but it is a false-negative in a permanent governance gate. It must be corrected as a bounded Core Corrections evidence-hardening task after the current canonical-PDF batch, with self-tests that prove detection while preserving academic Portuguese literals.

## Phase-end regression rule

For every phase closeout:

1. freeze one immutable candidate SHA after implementation and documentation synchronization;
2. run Static contract plus full relevant Linux integration;
3. run phase-specific acceptance surfaces on the same candidate;
4. include canonical-PDF checks whenever presentation is in scope;
5. include the heavy literal-font/Windows/PDF-A/distribution matrix when closing Final Certification;
6. record SHA, workflow IDs, conclusions and required manual/visual results;
7. any unexplained failure keeps the phase open;
8. synchronize handoff, roadmap, machine state and review/correction matrices after the result.

## Hard boundaries

- Do not resume Scientific Article while Core Corrections or Reference PDF Validation are open.
- Preserve the closed V3 public API unless current evidence explicitly authorizes a change.
- Do not translate reviewer comments directly into normative runtime behavior when current authority remains unresolved.
- Do not weaken tests merely to recover green CI.
- Do not close a phase on targeted checks alone.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
