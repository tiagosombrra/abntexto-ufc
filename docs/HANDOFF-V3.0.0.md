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
- First object-typography migration checkpoint: `f2f5124c4adcb34069a667f1ef80c76fb17728bd`.
- Branch acceptance Static run `33963240056`: success.
- Branch acceptance Linux run `33963240297`: failure, `PASS=29 FAIL=1 SKIP=1`.
- Isolated Linux failure: table identification/title expected 12 pt, measured 10 pt; illustration identification already passed at 12 pt and illustration/table sources passed at 10 pt.
- Root cause: `abntexto-ufc/modules.def` still forced `tabularray-abnt` `caption,lasthead,capcont` to `\abntsmall`.
- Residual table-adapter correction checkpoint: `7ec385ebecf21ba17e59db1e7ec16d3336f4bf4c`.
- Review item 21 remains FAIL until a new Static/full Linux run confirms the corrected 12 pt upper table title and 10 pt lower source behavior.
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

Continue **Core Corrections — Objects** with the residual table-adapter acceptance gate:

1. run the normal Static contract on the checkpoint containing `7ec385ebecf21ba17e59db1e7ec16d3336f4bf4c`;
2. run full Linux integration on the same branch checkpoint;
3. confirm object geometry reports illustration identification 12 pt, illustration source 10 pt, table identification 12 pt and table source 10 pt;
4. if green, move review item 21 from FAIL to PASS and synchronize all control documents;
5. if any check fails, classify the failure and correct the real runtime/contract/evidence defect without weakening the test.

The object correction history is now explicit:

- `f2f5124...` migrated the normative rule IDs, locators, illustration/object runtime and final-PDF expectations;
- run `33963240297` demonstrated that the independent table adapter still overrode upper table caption size;
- `7ec385e...` restores `caption,lasthead,capcont` to `\normalsize` while retaining `firsthead-text,lasthead-text,conthead-text,lastfoot` at `\abntsmall`;
- the 12 pt/10 pt final-PDF evidence remains unchanged and therefore remains a valid acceptance oracle.

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
