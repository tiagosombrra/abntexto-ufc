# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- PR #285 merged as `e6833ed5cf07aaf1021c690260cecfacec1a119a`, landing the validated shared foundation and accepted Scientific Article Step 1.
- Active task branch: `feat/v3-scientific-article`.
- Active phase: **Scientific Article**.
- Regression Audit: CLOSED.
- Core Corrections candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Reference PDF Validation candidate `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790`, Linux `33985595798`, both SUCCESS.
- Canonical reference PDF: build SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, artifact `9974546873`, SHA-256 `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`, 55/55 visual PASS.
- Librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article source contract: 18 rules in `docs/ARTICLE-NORMATIVE-CONTRACT.md` / `standards/coverage-rules-article.json`.
- Step 1 implementation checkpoint: `b46ba2051f8c9c712a7b5d25748b81baa52b920a`.
- Step 1 synchronized checkpoint `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`: Static `34001350884` SUCCESS; Linux `34001350953` SUCCESS; `PASS=31 FAIL=0 SKIP=0`.
- Step 1 state: **ACCEPTED**.
- Step 2 implementation checkpoint: `90293af760c4063b02a16831196ec3d932f1471d`.
- Step 2 state: **IMPLEMENTED — CI PENDING**.
- Step 2 runtime: new `abntexto-ufc/articles.def` and public `\ufcPrintArticleFrontMatter{...}` route.
- Step 2 rendered evidence: title, authorship, author footnote, submission/approval dates and primary summary under pdfLaTeX/LuaLaTeX; no proof-state promotion yet.
- Issue #217: CLOSED / superseded by current permanent workflow orchestration.
- Issue #18: OPEN and explicit **v3 release blocker** owned by Final Certification/Release; deterministic reference-PDF bytes/hash must be proven before publication.
- No temporary executor is active.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/V3-RELEASE-READINESS.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and `docs/ENGINEERING-LANGUAGE.md`.

## Scientific Article progress

| Step | State | Evidence / boundary |
|---:|---|---|
| 1. Profile and metadata surface | **ACCEPTED** | `b46ba205...`; synchronized `08b878a...`; Static `34001350884`; Linux `34001350953`, 31/31 PASS |
| 2. Required article front block | **IMPLEMENTED — CI PENDING** | implementation `90293af...`; article-specific final-PDF/source gate added for title/authorship/dates/summary |
| 3. Optional foreign elements | QUEUED | foreign title/summary optionality must remain non-mandatory |
| 4. Textual structure/body typography | QUEUED | reuse shared citation/reference/section/object machinery |
| 5. Recommendations/conditional boundary | QUEUED | recommendations advisory; journal instructions conditional |
| 6. Evidence hardening | QUEUED | rule-specific positive/negative proof only |
| 7. Canonical article PDF | QUEUED | real Git-bound TeX Live 2026 artifact + complete visual review |
| 8. Phase-end regression | QUEUED | one immutable SHA; Static + full Linux + article acceptance |

## Step 2 implementation boundary

| Surface | State | Constraint |
|---|---|---|
| `abntexto-ufc/articles.def` | ADDED | only required front-block behavior; no foreign elements/body hook |
| `\ufcPrintArticleFrontMatter{...}` | ADDED | requires `type=scientific-article` and required metadata/primary summary |
| primary title | IMPLEMENTED | 12 pt, centered, bold, uppercase, single-spaced |
| author note | IMPLEMENTED | uses `article-author-note` through a real footnote |
| dates | IMPLEMENTED | `submission-date` + reused `approval-date` |
| primary summary | IMPLEMENTED | required vernacular `Resumo:` surface |
| foreign title/summary | DEFERRED | Step 3 only; remains optional |
| body typography | DEFERRED | Step 4 only |
| recommendations | ADVISORY | no hard failures added |
| article coverage proof state | UNCHANGED | remains manual/conditional-manual pending later truthful promotion |

## Repository and branch readiness

| Surface | State | Action |
|---|---|---|
| `main` | UPDATED | contains PR #285 merge `e6833ed5...`; canonical foundation for all future work |
| `feat/v3-scientific-article` | ACTIVE | validate Step 2 synchronized checkpoint here |
| `plan/v3-regression-reset` | HISTORICAL | no new work; branch deletion is hygiene only |
| historical remote branches | provenance only | not active authority; do not branch new work from them |
| historical opaque R2/R3 docs | provenance only | excluded from active authority set |

## Release-readiness blockers

| Blocker | Owner | Current state | Exit condition |
|---|---|---|---|
| Scientific Article | Scientific Article phase / issue #280 | ACTIVE | complete article runtime/evidence/canonical PDF + phase-end regression |
| Deterministic release reference PDF | Final Certification / Release / issue #18 | OPEN | pin release epoch/`SOURCE_DATE_EPOCH` and prove rebuilt reference-PDF hash stability |
| Literal-font/PDF-A/distribution matrix | Final Certification | QUEUED | one immutable candidate passes the heavy certification matrix |
| Release assets/checksums/publication | Release | QUEUED | final release regression and checklist complete |

## Immediate action

1. complete synchronization of Step 2 implementation facts in roadmap, machine state and bootstrap;
2. run Static and full Linux on the synchronized Step 2 checkpoint;
3. classify any failure before modifying runtime/tests;
4. if both gates pass with `ARTICLE-FRONT-BLOCK-EVIDENCE`, mark Step 2 accepted and activate **Optional foreign elements**;
5. do not promote article rule proof state solely from source presence or shared green checks;
6. keep issue #18 visible as a release blocker without mixing it into article normative behavior;
7. finish Scientific Article with its own immutable phase-end regression before activating Final Certification.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, article-rule evidence, proof state, branch/checkpoint facts, release blockers and temporary-executor lifecycle must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Targeted checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve the accepted non-article foundation and reference PDF presentation.
- Do not change the 18-rule article authority/modality contract without new current source evidence and a separately documented source correction.
- Do not promote recommendations into required failures.
- Do not fork shared citation, reference, section, summary or object infrastructure.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary fonts.
- Resolve issue #18 before v3.0.0 release publication.
- CTAN submission remains blocked until **Release**.
