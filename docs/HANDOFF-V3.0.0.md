# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset` until this closeout PR is merged; Scientific Article should continue on a fresh short-lived branch from the updated `main`.
- Active phase: **Scientific Article**.
- Regression Audit: CLOSED.
- Core Corrections candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Reference PDF Validation candidate `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790`, Linux `33985595798`, both SUCCESS.
- Canonical reference build SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, run `33983729996`, artifact `9974546873`.
- Canonical PDF SHA-256 `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`; 55 A4 pages; PDF 1.7; TeX Live 2026/pdfLaTeX; unencrypted; fonts embedded.
- Complete 200 DPI visual review: **PASS — 55/55 pages, 0 unexplained visual FAIL**.
- Librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.
- Current runtime inspection: no `scientific-article` type is present in `abntexto-ufc/core.def`; article implementation starts from this corrected shared foundation.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap, active phase documents and this handoff must describe the same phase and acceptance state. Disagreement fails closed.

## Reference PDF Validation closeout

The phase-end candidate `b64074c64941895f97fbe0f795ce826c798d17ce` passed the required same-SHA gate:

| Evidence | Result |
|---|---|
| Static contract | `33985595790` — SUCCESS |
| Full Linux integration | `33985595798` — SUCCESS |
| Canonical PDF provenance | PASS |
| Complete page review | 55/55 PASS |
| Unexplained visual failures | 0 |
| Temporary build executor | absent |

Later reruns `33987639785` and `33987639788` also completed successfully and are corroborating evidence, not the primary phase-end binding.

Reference PDF Validation is therefore CLOSED. No visual correction queue remains open.

## Scientific Article entry

The article phase starts only after the corrected shared foundation and accepted canonical academic-work PDF. The retained source-backed contract contains 18 `article.*` rules: required, optional, recommended and conditional-manual semantics must remain distinct.

The first implementation gap is explicit: `abntexto-ufc/core.def` currently has no canonical `type / scientific-article` route. Do not restore historical article code blindly. Implement against the current contract and current architecture.

Immediate implementation order:

1. establish the canonical `scientific-article` profile and minimal metadata/public API required by the 18-rule contract;
2. add article-specific positive compile/evidence fixtures before claiming proof;
3. implement the required title/authorship/date/summary presentation and optional foreign-title/foreign-summary routes;
4. implement/reuse textual structure and single-spaced article body presentation without forking shared citation/reference/section/object machinery;
5. preserve recommendation semantics as advisory evidence rather than hard failure;
6. add controlled negative evidence where safe and couple rejection to positive PASS for the same rule;
7. build and visually inspect a canonical scientific-article PDF;
8. synchronize all documentation and run a Scientific Article phase-end regression on one immutable SHA.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, article-rule evidence, proof state, branch/checkpoint facts and temporary-executor lifecycle must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Targeted checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve the accepted non-article foundation and reference PDF presentation.
- Do not change the 18-rule article authority/modality contract without new current source evidence and a separately documented source correction.
- Do not translate reviewer comments or historical article code directly into normative runtime behavior.
- Do not promote recommendations into required failures.
- Do not fork shared citation, reference, section, summary or object infrastructure for the article profile.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
