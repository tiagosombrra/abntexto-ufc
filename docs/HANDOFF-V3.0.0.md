# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Scientific Article**.
- Regression Audit: CLOSED.
- Core Corrections candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Reference PDF Validation candidate `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790`, Linux `33985595798`, both SUCCESS.
- Canonical reference PDF: build SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, artifact `9974546873`, SHA-256 `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`, 55/55 visual PASS.
- Librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article source contract: 18 rules in `docs/ARTICLE-NORMATIVE-CONTRACT.md` / `standards/coverage-rules-article.json`.
- Step 1 implementation checkpoint: `b46ba2051f8c9c712a7b5d25748b81baa52b920a`.
- Step 1 state: **Profile and metadata surface implemented; synchronized Static/full Linux acceptance pending**.
- No temporary executor is active.

The task branch remains `plan/v3-regression-reset` because PR #285 still carries the unmerged corrected foundation. Do not split Scientific Article work onto `main` before that foundation is merged; machine state and Git facts must remain aligned.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and `docs/ENGINEERING-LANGUAGE.md`.

## Scientific Article progress

| Step | State | Evidence / boundary |
|---:|---|---|
| 1. Profile and metadata surface | IMPLEMENTED — CI PENDING | `b46ba205...`; canonical `scientific-article`; `submission-date`; `article-author-note`; dedicated two-engine gate |
| 2. Required article front block | QUEUED | start only after Step 1 Static/full Linux acceptance |
| 3. Optional foreign elements | QUEUED | foreign title/summary optionality must remain non-mandatory |
| 4. Textual structure/body typography | QUEUED | reuse shared citation/reference/section/object machinery |
| 5. Recommendations/conditional boundary | QUEUED | recommendations advisory; journal instructions conditional |
| 6. Evidence hardening | QUEUED | rule-specific positive/negative proof only |
| 7. Canonical article PDF | QUEUED | real Git-bound TeX Live 2026 artifact + complete visual review |
| 8. Phase-end regression | QUEUED | one immutable SHA; Static + full Linux + article acceptance |

## Step 1 implementation details

The current article profile work adds only the bounded routing/metadata surface:

- `type = scientific-article` is the sole canonical article type;
- no `article`, `artigo`, `artigo-cientifico`, `artigo-científico` or `scientific_article` runtime alias is accepted;
- existing `author`, `title` and `approval-date` are reused;
- `submission-date` and `article-author-note` are the only new article-required metadata keys introduced at this step;
- foreign-title semantics are deliberately deferred rather than inferred from `title-variant`;
- no article presentation rule has been promoted from manual/conditional-manual based solely on profile registration.

## Immediate action

1. publish the synchronized Step 1 checkpoint containing `b46ba205...` and these control documents;
2. require Static contract and full Linux integration on that synchronized SHA;
3. classify any failure before changing runtime/tests;
4. only after green acceptance, mark Step 1 PASS and begin **Required article front block**;
5. update this handoff, the active plan, roadmap and machine state at every material advance;
6. finish Scientific Article with its own phase-end regression before activating Final Certification.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, article-rule evidence, proof state, branch/checkpoint facts and temporary-executor lifecycle must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Targeted checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve the accepted non-article foundation and reference PDF presentation.
- Do not change the 18-rule article authority/modality contract without new current source evidence and a separately documented source correction.
- Do not promote recommendations into required failures.
- Do not fork shared citation, reference, section, summary or object infrastructure.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
