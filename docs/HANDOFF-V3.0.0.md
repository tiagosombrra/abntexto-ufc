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
- Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c`: Static `33969505681` success; Linux `33969505614` success, `PASS=31 FAIL=0 SKIP=0`. Explicit generated-PDF evidence closed librarian items 11, 16 and 28.
- Current 34-item state: `28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.
- Current implementation checkpoint: `5d74c0c5b85ec501b04c5050af81180ad7e3f2ee`, hardening engineering-language detection and translating known mixed diagnostics. Branch-level Static/full Linux acceptance is pending.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents:

- `release/v3-roadmap.json`
- `docs/ROADMAP-V3.0.0.md`
- `docs/V3-CORRECTION-PLAN.md`
- `docs/UFC-LIBRARIAN-REVIEW.md`
- `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`
- `docs/V3-REGRESSION-AUDIT.md`
- `docs/ENGINEERING-LANGUAGE.md`

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Mandatory operating discipline

Every material advance updates the relevant execution documentation and this handoff in the same work cycle. Phase state, acceptance state, current correction batch, evidence state, and machine-readable facts must also be synchronized in `docs/ROADMAP-V3.0.0.md` and `release/v3-roadmap.json`.

Every phase requires a phase-end regression before closure. Targeted checks are necessary evidence for individual corrections but never authorize a phase transition by themselves.

## Immediate action

Continue **Core Corrections — Engineering Language Evidence Hardening**:

1. publish the synchronized branch checkpoint containing implementation `5d74c0c5b85ec501b04c5050af81180ad7e3f2ee` plus this documentation state;
2. require normal Static contract and full Linux integration on that checkpoint;
3. verify the strengthened `engineering_language.py` self-test and the permanent audit both report zero project-owned Portuguese technical diagnostics after translating the known mixed diagnostics in `multivolume.sh` and `references-6023.sh`;
4. if the strengthened detector exposes additional project-owned mixed diagnostics, correct them rather than weakening the detector;
5. once Static/full Linux are green, close this evidence-hardening finding and synchronize all control documents;
6. then continue bounded reference work for items 30-32 without changing item 33 absent authoritative current-edition evidence.

After the bounded reference work, finish canonical front-matter items 1, 2 and 7 plus annex item 34, then freeze one Core Corrections phase-end candidate and run the complete Static/full Linux phase-end regression.

## Closed canonical-reference evidence batch

Checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c` closed the prior canonical-reference PDF batch. Static `33969505681` and Linux `33969505614` are green; Linux reported `PASS=31 FAIL=0 SKIP=0` and emitted explicit generated-PDF PASS evidence for:

- item 11 — sentence-case object titles and absence of reviewed legacy casing;
- item 16 — rendered `Universidade Federal do Ceará (UFC)` with source-level first-use guard;
- item 28 — sentence-case headings, absence of reviewed legacy headings, and correct `etc.` punctuation.

These items are now PASS and the review totals are `28/5/0/1`.

## Active regression finding — engineering-language false negatives

The permanent engineering-language gate previously reported zero Portuguese project-owned technical diagnostics while mixed diagnostics still existed. The defect is evidence-quality, not document runtime behavior.

Implementation `5d74c0c...` addresses the known gap by:

- adding high-confidence mixed-language phrase detection to `tests/checks/engineering_language.py`;
- extending the self-test from 7 to 11 cases with known former false negatives;
- translating project-owned diagnostics in `tests/integration/multivolume.sh`;
- translating project-owned diagnostics in `tests/integration/references-6023.sh`;
- preserving Portuguese bibliography data, rendered academic strings, official wording and other allowed academic literals.

This finding remains open until synchronized Static/full Linux acceptance is green.

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
