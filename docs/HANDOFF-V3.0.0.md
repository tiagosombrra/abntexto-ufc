# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Core Corrections**.
- Regression baseline `c4bf51b574647226ee488440579ec2a204c16c79`: Static `33937439818`, Linux `33937439846` success.
- Object/Core checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`: Static `33965794475`, Linux `33965794519` success.
- Canonical-reference checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c`: Static `33969505681`, Linux `33969505614` success.
- Engineering-language checkpoint `edeb14b7a96d1cab3ad9551701087ddf4dff059a`: Static `33972111694`, Linux `33972111696` success.
- Reference evidence checkpoint `bcd851b3176b516091a254bc57b5ae4e8add9358`: Static `33974062993`, Linux `33974063103` success, `PASS=31 FAIL=0 SKIP=0`.
- Front Matter and Annex Closeout checkpoint `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8`: Static `33980847191`, Linux `33980847189` success, `PASS=31 FAIL=0 SKIP=0`; explicit reviewer evidence PASS for items 1, 2, 7 and 34.
- Current 34-item state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Current batch: **Core Corrections — Phase-end Regression Preparation**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Accepted closeout evidence

Linux `33980847189` emitted the required reviewer evidence:

1. item 1 — blank department omitted and filled department rendered on the academic cover;
2. item 2 — canonical generated output contains `NOME COMPLETO DO AUTOR`;
3. item 7 — approval-page institution/acronym form preserved as `Instituição Externa de Teste (IET)`;
4. item 34 — canonical annex source attribution, heading presence and TOC entry confirmed, with the independent final-PDF gate also proving bold/uppercase/12 pt/centered heading semantics.

The run completed `PASS=31 FAIL=0 SKIP=0`. Static `33980847191` also passed. The prior Static `33980486317` remains historical evidence of the engineering-language guard and is not a runtime defect.

## Immediate action

1. publish this acceptance-state synchronization;
2. create a **separate immutable Core Corrections phase-end regression candidate** after this acceptance state is recorded;
3. run Static contract and full Linux integration on that exact candidate SHA;
4. require all phase-specific acceptance evidence to remain green and keep item 33 fail-closed;
5. if the phase-end candidate is green, record its SHA/run IDs, close Core Corrections, and activate **Reference PDF Validation**;
6. do not start Scientific Article until Reference PDF Validation closes.

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
