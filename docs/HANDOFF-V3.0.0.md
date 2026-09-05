# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-04

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`; task branches are short-lived.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Core Corrections**.
- Pre-regression `main` baseline: `c4bf51b574647226ee488440579ec2a204c16c79`.
- Regression planning checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`.
- Static contract run `33937439818`: success.
- Full Linux regression integration run `33937439846`: success.
- Latest Core Corrections implementation checkpoint: `1eab2539e418224e2a6ce85ef09065941b719ef7`.
- Static contract run `33939021386` for that checkpoint: success.
- Full Linux integration run `33939021352` for that checkpoint: still in progress; review-item closure is deferred until it completes successfully.
- Regression audit: `docs/V3-REGRESSION-AUDIT.md` — closed.
- Executable correction queue: `docs/V3-CORRECTION-PLAN.md`.
- Consolidated review input: `docs/UFC-LIBRARIAN-REVIEW.md` with exactly 34 tracked requirements.
- Scientific-article authority reconstruction is retained, but article runtime remains deferred.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must describe the same active phase. Disagreement fails closed.

## Mandatory operating discipline

Every material advance must update the relevant execution documentation and this handoff in the same work cycle. If the advance changes phase state, acceptance state, current correction batch, evidence state, or branch/checkpoint facts, `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json` must be updated in the same checkpoint as well.

Every phase requires a phase-end regression before closure. Targeted checks collected while implementing individual corrections are necessary evidence but do not authorize a phase transition. Before the next phase becomes active, one immutable candidate SHA must pass the full relevant regression, the run IDs and conclusions must be recorded, required visual/canonical-artifact checks must be complete, and the control documentation must be synchronized with that result. Any unexplained failure blocks transition.

## Immediate action

Continue **Core Corrections** in bounded batches:

1. wait for and classify Linux integration run `33939021352` for checkpoint `1eab2539e418224e2a6ce85ef09065941b719ef7`;
2. if green, update the 34-item review matrix for items 19, 20, and 23 and record the evidence checkpoint;
3. correct unambiguous shared runtime/reference defects and add regression evidence;
4. keep disputed object-title typography fail-closed until current authority is reconciled;
5. keep disputed NBR 6023:2025 DOI/online/repeated-author cases fail-closed until current-edition evidence is available;
6. remove remaining stale V2-era guidance and retired public API vocabulary from the canonical V3 reference;
7. update documentation/control state with every material advance instead of accumulating undocumented work;
8. advance to **Reference PDF Validation** only after all shared P0/P1 corrections are closed and the mandatory Core Corrections phase-end regression is green on one immutable SHA.

## Core Corrections progress

The first implementation batch targets only unambiguous defects and reference guidance:

- title-page advisor/co-advisor final punctuation;
- optional department guidance and complete-author-name placeholder;
- committee institution/acronym examples;
- first textual use of Universidade Federal do Ceará (UFC);
- current V3 public profile/key vocabulary;
- explicit annex source example;
- rejection of stale V2/current-reference vocabulary through the reference-guide contract.

The second implementation batch at `1eab2539e418224e2a6ce85ef09065941b719ef7` adds:

- a long-direct-quotation fixture with a real available locator (`p. 42`);
- a positive/negative punctuation check preventing a full stop before the parenthetical long-quote citation;
- an external-illustration source example/check with locator `p. 42`;
- cleanup of mixed-language engineering diagnostics in touched regression gates.

These changes are implemented but items 19, 20, and 23 remain formally open until full Linux integration confirms them.

This work intentionally does **not** change object title size or disputed bibliography runtime.

## Phase-end regression rule

For every phase closeout:

1. freeze the candidate SHA after implementation and documentation synchronization;
2. run Static contract plus the full relevant Linux integration contract;
3. run phase-specific acceptance surfaces on the same candidate, including canonical-PDF visual checks when applicable;
4. include the heavy literal-font/Windows/PDF-A/distribution matrix when closing Final Certification;
5. record SHA, workflow run IDs, conclusions, visual/manual results, and unresolved exceptions;
6. if any unexplained failure occurs, keep/reopen the phase and correct it before transition;
7. update this handoff, the roadmap, machine state, and the relevant review/correction matrix with the regression result.

## Hard boundaries

- Do not resume Scientific Article runtime while Core Corrections or Reference PDF Validation are open.
- Preserve the closed V3 public API unless current evidence authorizes a change.
- Do not convert reviewer comments directly into normative runtime behavior when current authority is unresolved.
- Do not weaken tests merely to recover a green build.
- Do not close a phase on targeted tests alone; the phase-end regression is mandatory.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
