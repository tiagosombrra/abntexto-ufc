# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Reference PDF Validation**.
- Core Corrections immutable phase-end candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da` passed Static `33982156041` and full Linux `33982156042`; Linux summary `PASS=31 FAIL=0 SKIP=0`.
- Current 34-item state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Fresh canonical artifact build SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`.
- Temporary build run `33983729996`: SUCCESS.
- Artifact `9974546873`, `v3-reference-pdf-da02f17df4d2d0a1568edbbe8bfbbfffb7208966`.
- Canonical PDF SHA-256: `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`.
- Canonical PDF: 55 pages, 450652 bytes, A4, PDF 1.7, pdfTeX 1.40.29 / TeX Live 2026, unencrypted; preflight openable and all `pdffonts` entries embedded.
- Artifact provenance/preflight: **PASS**.
- Current batch: **Reference PDF Validation — complete 200 DPI page-level visual review**.
- Temporary workflow `.github/workflows/tmp-reference-pdf.yml` is removed in the provenance-acceptance checkpoint; permanent workflows are unchanged.
- Pre-existing 2026-09-04 PDF remains comparison-only because it predates accepted Core Corrections.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap, active phase document and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Canonical artifact provenance

Temporary workflow run `33983729996` built `template/main.tex` directly from `da02f17d...` with TeX Live 2026/pdfLaTeX. The uploaded provenance record identifies the same Git SHA and run ID. Workflow and local SHA-256 values match exactly.

`pdfinfo` reports 55 A4 pages, PDF 1.7, no encryption and no structural suspect flag. Repository-independent preflight opened the PDF successfully, found it text-based rather than scanned and found no XFA. `pdffonts` reports every listed font embedded.

A front-matter text precheck confirms the fresh artifact contains the accepted complete-author placeholder, omits the blank department field, prints the advisor line with final punctuation, and renders committee institutions/acronyms from the current canonical configuration. These observations are not substitutes for the visual page review.

## Immediate action

1. render all 55 canonical pages at 200 DPI;
2. inspect every page, using grouped contact sheets plus targeted full-page inspection;
3. record page-level PASS/FAIL results and presentation-sensitive librarian evidence;
4. classify every visual defect before modifying runtime/reference content;
5. rebuild/re-render after any correction;
6. once the visual checklist is clean, synchronize documentation and prepare one immutable Reference PDF Validation phase-end candidate;
7. require Static and full Linux on that same candidate before activating Scientific Article.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase/acceptance/evidence state, branch/checkpoint facts, artifact provenance and temporary-executor lifecycle must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Targeted checks and visual spot checks never authorize a phase transition by themselves.

## Hard boundaries

- Do not start Scientific Article while Reference PDF Validation is open.
- Preserve the closed V3 public API unless current evidence explicitly authorizes a change.
- Do not translate reviewer comments directly into normative runtime behavior when current authority remains unresolved.
- Do not use stale or synthetic PDFs as canonical acceptance evidence.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
