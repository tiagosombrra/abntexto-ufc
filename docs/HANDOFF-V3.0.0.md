# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Core Corrections**.
- Regression baseline: `c4bf51b574647226ee488440579ec2a204c16c79`; Static `33937439818` and Linux `33937439846` succeeded.
- Object/Core checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`: Static `33965794475` and Linux `33965794519` succeeded.
- Canonical-reference checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c`: Static `33969505681` and Linux `33969505614` succeeded; items 11, 16 and 28 closed.
- Engineering-language checkpoint `edeb14b7a96d1cab3ad9551701087ddf4dff059a`: Static `33972111694` and Linux `33972111696` succeeded; permanent audit reports zero project-owned Portuguese technical diagnostics.
- Reference evidence checkpoint `bcd851b3176b516091a254bc57b5ae4e8add9358`: Static `33974062993` and Linux `33974063103` succeeded, `PASS=31 FAIL=0 SKIP=0`; items 30-32 evidence passed and item 32 closed.
- Current 34-item state: `29 PASS / 4 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.
- Current bounded batch: **Core Corrections — Front Matter and Annex Closeout**.
- Initial evidence implementation: `33bdd0bd5f9360c645b4166071c32dbba6c647f0`.
- Synchronized checkpoint `48e7e6841b63ea62d6811e734dde09931b8f608c` failed Static `33980486317` only on engineering-language wording in the new complete-author diagnostic.
- Correction `dc381d4517341062d53ae5e93082c7856fc4af17` replaces that diagnostic wording with engineering English; corrected synchronized acceptance is pending.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Failure classification

Static `33980486317` is **not** a LaTeX/runtime, front-matter, annex, or librarian-review failure. The strengthened permanent language detector rejected the phrase `pre-textual` inside a newly added project-owned failure diagnostic. That is exactly the guard's intended behavior.

Correction `dc381d45...` changes only the diagnostic string. Evidence predicates, fixtures, canonical content, runtime and normative mapping are unchanged.

## Current evidence scope

1. item 1 — blank department omitted and filled department rendered on the academic cover;
2. item 2 — canonical generated output contains `NOME COMPLETO DO AUTOR`;
3. item 7 — doctoral approval page preserves `Instituição Externa de Teste (IET)`;
4. item 34 — canonical generated PDF contains annex heading/source attribution and generated TOC contains the annex entry; independent final-PDF evidence remains responsible for bold/uppercase/12 pt/centered heading semantics.

## Immediate action

1. synchronize documentation/machine state on top of `dc381d45...`, explicitly recording Static `33980486317` as a classified gate failure;
2. publish that checkpoint to `plan/v3-regression-reset`;
3. run Static contract and full Linux integration on that exact checkpoint;
4. require explicit PASS evidence for items 1, 2, 7 and 34;
5. classify any new failure before changing runtime or evidence strength;
6. if both gates pass, promote the review matrix to `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` and synchronize all control documents;
7. prepare a separate immutable **Core Corrections phase-end regression** candidate;
8. activate Reference PDF Validation only after the phase-end regression is green and recorded;
9. keep item 33 untouched/fail-closed.

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
