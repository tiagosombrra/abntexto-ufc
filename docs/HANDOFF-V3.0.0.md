# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`; task branches are short-lived.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Core Corrections**.
- Pre-regression `main` baseline: `c4bf51b574647226ee488440579ec2a204c16c79`.
- Regression planning checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`.
- Regression baseline Static run `33937439818`: success.
- Regression baseline Linux run `33937439846`: success.
- Reviewer evidence implementation checkpoint: `1eab2539e418224e2a6ce85ef09065941b719ef7`.
- Latest fully validated Core Corrections/control checkpoint: `f6ca012164273e67480dca127fe17b392e8a8a21`.
- Static contract run `33939512055`: success.
- Full Linux integration run `33939512019`: success, `PASS=31 FAIL=0 SKIP=0`.
- Object-typography implementation checkpoint: `f2f5124c4adcb34069a667f1ef80c76fb17728bd`.
- Object migration generated-tree Static preflight: workflow run `33963033293`, success.
- Object migration branch-level final Static/full Linux regression: pending on the current user-authored documentation/control checkpoint.
- Review items 19, 20 and 23 are confirmed PASS by the full Linux run.
- Review item 17 is confirmed PASS by the code-typography regression evidence.
- Review item 4 is confirmed PASS after the advisor/co-advisor punctuation runtime correction and green integration.
- Review item 21 implementation is complete but remains FAIL until normal branch-level Static/full Linux evidence confirms 12 pt upper identification/title and 10 pt lower source/note behavior.
- Current 34-item state: `24 PASS / 8 PARTIAL / 1 FAIL / 1 NORMATIVE-REVIEW`.
- Remaining unresolved normative review: NBR 6023:2025 edge cases in item 33.
- Scientific Article runtime remains deferred.

Canonical control/evidence documents:

- `release/v3-roadmap.json`
- `docs/ROADMAP-V3.0.0.md`
- `docs/V3-CORRECTION-PLAN.md`
- `docs/UFC-LIBRARIAN-REVIEW.md`
- `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`
- `docs/V3-REGRESSION-AUDIT.md`

Git facts, machine state, roadmap and this handoff must describe the same active phase. Disagreement fails closed.

## Mandatory operating discipline

Every material advance must update the relevant execution documentation and this handoff in the same work cycle. If phase state, acceptance state, current correction batch, evidence state, or branch/checkpoint facts change, update `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json` in the same checkpoint.

Every phase requires a phase-end regression before closure. Targeted checks collected while implementing individual corrections are necessary evidence but do not authorize a phase transition. One immutable candidate SHA must pass the complete relevant regression, required visual/canonical checks must be complete, and the control documentation must record the result before the next phase becomes active.

## Immediate action

Close **Core Corrections — Objects** only after branch-level evidence:

1. run the normal Static contract on the current user-authored checkpoint;
2. run full Linux integration on the same checkpoint;
3. inspect object geometry, illustration final-PDF and table final-PDF evidence for the 12 pt / 10 pt split;
4. if green, move review item 21 from FAIL to PASS and synchronize all control documents;
5. if any check fails, classify the failure and correct the real contract/runtime/evidence defect without weakening the test.

The semantic migration itself is already committed at `f2f5124c4adcb34069a667f1ef80c76fb17728bd`:

- upper illustration/table identification/title is no longer a reduced-font child;
- historical incorrect rule IDs are retired with provenance in `standards/rule-migrations.json`;
- `objects.def` uses 12 pt upper identification/title with single spacing;
- source/legend/note remain reduced 10 pt where applicable;
- illustration/table locator ownership is separated into exact rule-specific locators;
- final-PDF expectations and object geometry checks were updated atomically;
- temporary migration executor/workflow surfaces were removed before the generated checkpoint.

After objects, continue the remaining bounded work:

- front-matter/reference canonical visual confirmations for partial items;
- sentence-case/reference-corpus cleanup;
- unambiguous NBR 6023:2025 regression cases;
- keep item 33 fail-closed until authoritative current-edition evidence exists;
- annex/reference-PDF visual confirmation;
- Core Corrections phase-end regression on one immutable SHA.

## Phase-end regression rule

For every phase closeout:

1. freeze the candidate SHA after implementation and documentation synchronization;
2. run Static contract plus the full relevant Linux integration contract;
3. run phase-specific acceptance surfaces on the same candidate;
4. include canonical-PDF visual checks whenever presentation is in scope;
5. include the heavy literal-font/Windows/PDF-A/distribution matrix when closing Final Certification;
6. record SHA, workflow run IDs, conclusions and manual/visual results;
7. any unexplained failure keeps/reopens the phase and blocks transition;
8. update handoff, roadmap, machine state and review/correction matrices after the regression result.

## Hard boundaries

- Do not resume Scientific Article while Core Corrections or Reference PDF Validation are open.
- Preserve the closed V3 public API unless current evidence explicitly authorizes a change.
- Do not translate reviewer comments directly into normative runtime behavior when current authority remains unresolved.
- Do not weaken tests merely to recover green CI.
- Do not close a phase on targeted checks alone.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
