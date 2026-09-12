# V3 Reference PDF Validation

> **Historical evidence — not current release authority.** This record may remain technically informative, but its phase/status statements are historical. Current release state is defined by the v3.0.1 continuation/finalization control plane. See `docs/V3.0.1-DOCUMENT-LIFECYCLE.md`.


Updated: 2026-09-05  
Status: CLOSED — ACCEPTED

## Purpose

This phase validates the corrected canonical V3 academic-work reference PDF as a rendered document. Source-level and integration tests remain necessary but are not sufficient for presentation acceptance.

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

The temporary build executor is removed. The older 2026-09-04 PDF remains comparison-only.

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

An independent follow-up inspection of the recovered artifact repeated PDF preflight and a complete 55-page contact-sheet scan. It confirmed the accepted page count, A4 geometry, embedded fonts and absence of visible clipping, overlap, broken glyphs or unexplained blank pages. No correction was required.

A preservation-only raster comparison against the older V3 PDF retained 55 pages in both documents; 28 pages were pixel-identical at 120 DPI and 27 changed in accepted correction/reference-content areas.

## Validation loop

| Step | Result |
|---|---|
| Establish artifact provenance and bind PDF to a concrete Git SHA | PASS |
| Preflight page count, A4 geometry, PDF version, fonts/embedding and extraction viability | PASS |
| Render every page at 200 DPI | PASS |
| Inspect complete page sequence for clipping, overlap, glyphs, pagination, margins, headings and object overflow | PASS |
| Reconfirm presentation-sensitive librarian-review items | PASS |
| Compare older preserved surfaces where useful without treating old PDF as authority | PASS |
| Record visual findings | PASS |
| Classify defects before modification | NOT TRIGGERED — no visual defect found |
| Rebuild/re-render after correction | NOT APPLICABLE — no correction required |
| Freeze synchronized repository state and run phase-end regression | PASS |

## Phase-end regression

Immutable Reference PDF Validation candidate:

`b64074c64941895f97fbe0f795ce826c798d17ce`

Required same-SHA results:

- Static contract `33985595790` — **SUCCESS**;
- full Linux integration `33985595798` — **SUCCESS**;
- accepted canonical-PDF provenance — **PASS**;
- complete visual-review record — **PASS**;
- temporary executor absent — **PASS**.

Later reruns `33987639785` and `33987639788` also succeeded and corroborate the accepted state; they do not replace the primary immutable phase-end binding above.

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

## Exit result

All Reference PDF Validation exit criteria are satisfied. The phase is **CLOSED** and the roadmap may activate **Scientific Article**.

The accepted academic-work PDF remains a preservation baseline for later phases. Scientific Article work must not regress shared behavior merely to simplify the new profile.

## Regression discipline retained

Every **material advance** after this phase still requires synchronized documentation. Every later phase still requires its own **phase-end regression** on one immutable candidate before closure.
