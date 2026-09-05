# V3 Reference PDF Validation

Updated: 2026-09-05  
Status: ACTIVE — VISUAL REVIEW PASS / PHASE-END CANDIDATE

## Purpose

This phase validates the corrected canonical V3 reference PDF as a rendered document. Source-level and integration tests remain necessary but are not sufficient for presentation acceptance.

Core Corrections closed on immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, which passed Static `33982156041` and full Linux `33982156042`; Linux summary: `PASS=31 FAIL=0 SKIP=0`.

## Accepted canonical artifact provenance

Fresh canonical PDF build:

- source/build SHA: `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`;
- temporary workflow run: `33983729996` — SUCCESS;
- artifact ID: `9974546873`;
- artifact name: `v3-reference-pdf-da02f17df4d2d0a1568edbbe8bfbbfffb7208966`;
- source: `template/main.tex`;
- engine: pdfLaTeX / pdfTeX `1.40.29`;
- TeX Live: 2026;
- PDF SHA-256: `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`;
- size: 450652 bytes;
- pages: 55;
- page geometry: A4, `595.276 x 841.89 pt`;
- PDF version: 1.7;
- encrypted: no;
- preflight: PASS;
- fonts: all listed entries embedded.

The temporary build executor is removed. The older 2026-09-04 PDF is comparison-only.

## Visual review

The complete visual-review record is `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`.

Result:

- rendered at 200 DPI;
- pages reviewed: 55/55;
- unexplained visual FAIL: 0;
- clipping/overlap/broken replacement glyph: 0;
- unexpected blank page: 0;
- presentation-sensitive librarian reconfirmation: PASS;
- optional page-36 licensed-photo fallback: intentional normal-build behavior.

A preservation-only raster comparison against the older V3 PDF retained 55 pages in both documents; 28 pages were pixel-identical at 120 DPI and 27 changed in accepted correction/reference-content areas.

## Validation loop

1. Establish artifact provenance and bind PDF to a concrete Git SHA. — **PASS**
2. Preflight page count, A4 geometry, PDF version, fonts/embedding and extraction viability. — **PASS**
3. Render every page at 200 DPI. — **PASS**
4. Inspect complete page sequence for clipping, overlap, glyphs, pagination, margins, headings and object overflow. — **PASS**
5. Reconfirm presentation-sensitive librarian-review items 10, 15, 21 and 34 plus canonical examples 1, 2, 7, 11, 16 and 28. — **PASS**
6. Compare older preserved surfaces where useful, without treating the old PDF as authority. — **PASS**
7. Record all visual findings. — **PASS**
8. Classify defects before modification. — **NOT TRIGGERED: no visual defect found**
9. Rebuild/re-render after correction. — **NOT APPLICABLE: no correction required**
10. Freeze synchronized repository state and run phase-end regression. — **CURRENT**

## Page-level review groups

| Group | Scope | State |
|---|---|---|
| Artifact provenance and preflight | SHA, engine, A4, page count, metadata, extraction, embedding | PASS |
| Cover/title/approval pages | optional department, complete author, punctuation, committee institution/acronym | PASS |
| Other pre-textual pages | errata, dedication, acknowledgements, epigraph, RESUMO/ABSTRACT, lists, TOC | PASS |
| Main text | headings, paragraphs, citations, quotations, alíneas, pagination | PASS |
| Figures/tables/code/algorithms/equations | title/source typography, bounds, spacing, locators | PASS |
| References | layout and controlled examples; item 33 authority-deferred | PASS — VISUAL |
| Appendices/annexes/index | heading/TOC presentation, source attribution, pagination | PASS |
| Global visual quality | clipping, overlap, glyphs, whitespace anomalies, page-side behavior | PASS |

## Known authority boundary

Librarian-review item 33 remains `NORMATIVE-REVIEW`. This phase observes current bibliography presentation but does not convert disputed NBR 6023:2025 edge cases into runtime requirements without authoritative current-edition text.

## Current phase-end candidate rule

This synchronized visual-review-complete repository state is frozen as one immutable Reference PDF Validation phase-end candidate. The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`; the actual candidate SHA is recorded after commit creation and later written with workflow results.

The candidate must pass:

1. Static contract;
2. full Linux integration;
3. existing phase-specific acceptance evidence.

## Exit gate

Reference PDF Validation -> Scientific Article requires:

- accepted canonical PDF provenance;
- complete page-level visual PASS;
- reproducible presentation evidence;
- temporary executor absent;
- documentation/machine state synchronized;
- Static contract and full Linux integration green on one immutable Reference PDF Validation candidate.

Scientific Article runtime remains deferred until this gate closes.
