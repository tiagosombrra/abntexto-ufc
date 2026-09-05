# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Core Corrections**.
- Front Matter and Annex Closeout checkpoint `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8`: Static `33980847191`, Linux `33980847189` success, `PASS=31 FAIL=0 SKIP=0`; explicit reviewer evidence PASS for items 1, 2, 7 and 34.
- Acceptance-state synchronization checkpoint: `c066697691df748a3b24a716ba69d5e4cb168f5d`.
- Current 34-item state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Current batch: **Core Corrections — Phase-end Regression Candidate**.
- Candidate contract: `docs/V3-CORE-CORRECTIONS-PHASE-END.md`.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Current candidate rule

The commit that first introduces `docs/V3-CORE-CORRECTIONS-PHASE-END.md` in this synchronized state is the immutable Core Corrections phase-end candidate. Its SHA is recorded only after the commit exists.

Required gate on that exact SHA:

1. Static contract;
2. full Linux integration;
3. existing phase-specific acceptance evidence remains green;
4. no shared runtime FAIL appears;
5. item 33 remains explicit/fail-closed.

## Immediate action

1. publish the synchronized phase-end candidate commit;
2. wait for Static and full Linux on that exact SHA;
3. classify any failure before changing code/tests;
4. if both pass, record candidate SHA/run IDs and close Core Corrections;
5. activate **Reference PDF Validation** in the same phase-transition documentation cycle;
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
