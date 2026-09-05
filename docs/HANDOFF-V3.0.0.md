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
- Validated Core Corrections checkpoint: `3f47081cbbd00a44b9ee86a6b406580e79b593c0`.
- Static `33965794475`: success.
- Full Linux `33965794519`: success, `PASS=31 FAIL=0 SKIP=0`.
- Object typography review item 21: **PASS**. Automated final-PDF evidence confirms illustration/table upper identification/title at 12 pt and lower source at 10 pt; the IBGE table subset also passes.
- Current implementation checkpoint: `c464a1bc2ca04a4ce398878f25e9521f5840d48e`, adding canonical-reference source regressions for librarian items 11, 16 and 28.
- Current synchronized documentation checkpoint is being built on top of `c464a1b...`; branch acceptance for that reference-content batch is pending.
- Current 34-item state: `25 PASS / 8 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.
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

1. publish the synchronized checkpoint containing `c464a1bc2ca04a4ce398878f25e9521f5840d48e` plus this documentation update;
2. require normal Static contract and full Linux integration on that branch checkpoint;
3. verify the new source-level evidence for items 11, 16 and 28 is green;
4. extend canonical `reference-corpus.sh` evidence so the generated PDF explicitly confirms reviewed sentence-case object titles/headings and first body-text `Universidade Federal do Ceará (UFC)`;
5. only then reclassify items 11/16/28 if the PDF evidence supports closure;
6. continue bounded reference work for items 30-32 without changing item 33 absent authoritative current-edition evidence.

After those bounded corrections, finish canonical front-matter and annex confirmation, then freeze one Core Corrections phase-end candidate and run the complete Static/full Linux phase-end regression.

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
