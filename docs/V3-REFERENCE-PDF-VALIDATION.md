# V3 Reference PDF Validation

Updated: 2026-09-05
Status: ACTIVE — CANONICAL REBUILD IN PROGRESS

## Purpose

This phase validates the corrected canonical V3 reference PDF as a rendered document. Source-level and integration tests remain necessary but are not sufficient for presentation acceptance.

Core Corrections closed on immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, which passed Static `33982156041` and full Linux `33982156042`; Linux summary: `PASS=31 FAIL=0 SKIP=0`.

## Artifact provenance finding

The pre-existing local PDF generated on 2026-09-04 (`abntexto-ufc-v3-template-example.pdf`, 55 pages, 449654 bytes) is **REJECTED as the canonical acceptance artifact**. It is a real LaTeX PDF, but its rendered content predates accepted Core Corrections: extraction still shows `NOME SOBRENOME`, a populated department line, and the title-page advisor line without the accepted final punctuation. It therefore remains comparison-only and must not be used to close this phase.

A fresh canonical build is being generated from the current remote branch using temporary workflow `.github/workflows/tmp-reference-pdf.yml`. The workflow records Git SHA, workflow run, TeX Live 2026, pdfLaTeX, `pdfinfo` and SHA-256 and uploads the resulting PDF as a short-lived artifact. The temporary workflow must be removed after the artifact is recovered and validated.

## Artifact rule

Only a real LaTeX build is admissible. The canonical PDF must be compiled from the repository with TeX Live 2026 or an equivalent explicitly recorded environment. Synthetic ReportLab or hand-recreated PDFs are not acceptable evidence.

A PDF generated from an older checkpoint may be used only as a comparison artifact. It must not be promoted to the canonical candidate when later runtime or canonical-reference changes can affect rendered output.

## Validation loop

1. Establish artifact provenance and bind the PDF to a concrete Git SHA.
2. Preflight the PDF: page count, A4 geometry, PDF version, fonts/embedding observations, extraction viability and obvious structural warnings.
3. Render every page at 200 DPI with the repository-independent PDF review tooling.
4. Inspect the complete page sequence for clipping, overlap, broken glyphs, incorrect blank pages, unexpected pagination, inconsistent margins, heading drift and object overflow.
5. Reconfirm presentation-sensitive librarian-review items, especially 10, 15, 21 and 34, plus canonical examples for 1, 2, 7, 11, 16 and 28.
6. Compare unchanged surfaces with the accepted V2.1 preservation baseline where useful. V2.1 is preservation evidence, not current normative authority.
7. Record every visual finding as PASS, FAIL or NOT-APPLICABLE with page evidence.
8. If a defect is found, classify it as runtime, reference-content, evidence-observer or artifact-provenance failure before changing implementation.
9. Rebuild, re-render and re-inspect after any correction.
10. Close the phase only after the accepted canonical artifact and one immutable phase-end regression candidate are both green.

## Page-level review groups

| Group | Scope | Current state |
|---|---|---|
| Artifact provenance and preflight | SHA, engine, A4, page count, metadata, extraction | BUILDING FRESH ARTIFACT |
| Cover/title/approval pages | optional department, complete author, punctuation, committee institution/acronym | PENDING |
| Other pre-textual pages | errata, dedication, acknowledgements, epigraph, RESUMO/ABSTRACT, lists, TOC | PENDING |
| Main text | headings, paragraphs, citations, quotations, alíneas, pagination | PENDING |
| Figures/tables/code/algorithms/equations | title/source typography, bounds, spacing, locators | PENDING |
| References | layout and controlled examples; item 33 remains authority-deferred | PENDING |
| Appendices/annexes/index | heading/TOC presentation, source attribution, pagination | PENDING |
| Global visual quality | clipping, overlap, glyphs, whitespace anomalies, page-side behavior | PENDING |

## Known authority boundary

Librarian-review item 33 remains `NORMATIVE-REVIEW`. This phase may observe the current rendered bibliography but must not convert disputed NBR 6023:2025 edge cases into runtime requirements without authoritative current-edition text.

## Exit gate

Reference PDF Validation -> Scientific Article requires:

- canonical PDF provenance tied to an accepted repository SHA;
- complete page-level visual checklist with no unexplained FAIL;
- reproducible evidence for presentation-sensitive requirements;
- temporary PDF-build executor removed;
- documentation and machine state synchronized;
- Static contract and full Linux integration green on one immutable Reference PDF Validation phase-end candidate.

Scientific Article runtime remains deferred until this gate closes.
