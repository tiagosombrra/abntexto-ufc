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
- Regression audit: `docs/V3-REGRESSION-AUDIT.md` — closed.
- Executable correction queue: `docs/V3-CORRECTION-PLAN.md`.
- Consolidated review input: `docs/UFC-LIBRARIAN-REVIEW.md` with exactly 34 tracked requirements.
- Scientific-article authority reconstruction is retained, but article runtime remains deferred.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must describe the same active phase. Disagreement fails closed.

## Immediate action

Continue **Core Corrections** in bounded batches:

1. correct unambiguous shared runtime/reference defects and add regression evidence;
2. keep disputed object-title typography fail-closed until current authority is reconciled;
3. keep disputed NBR 6023:2025 DOI/online/repeated-author cases fail-closed until current-edition evidence is available;
4. remove stale V2-era guidance and retired public API vocabulary from the canonical V3 reference;
5. update the 34-item matrix only after the corresponding correction evidence is green;
6. advance to **Reference PDF Validation** only after all shared P0/P1 corrections are closed.

## First Core Corrections batch

The first batch targets only unambiguous defects and reference guidance:

- title-page advisor/co-advisor final punctuation;
- optional department guidance and complete-author-name placeholder;
- committee institution/acronym examples;
- first textual use of Universidade Federal do Ceará (UFC);
- current V3 public profile/key vocabulary;
- long-direct-quote locator guidance without fabricating a locator for synthetic text;
- explicit annex source example;
- rejection of stale V2/current-reference vocabulary through the reference-guide contract.

This batch intentionally does **not** change object title size or disputed bibliography runtime.

## Hard boundaries

- Do not resume Scientific Article runtime while Core Corrections or Reference PDF Validation are open.
- Preserve the closed V3 public API unless current evidence authorizes a change.
- Do not convert reviewer comments directly into normative runtime behavior when current authority is unresolved.
- Do not weaken tests merely to recover a green build.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
