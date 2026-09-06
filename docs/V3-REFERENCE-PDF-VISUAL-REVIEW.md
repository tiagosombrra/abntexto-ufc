# V3 Reference PDF — Complete Visual Review

Updated: 2026-09-05  
Status: COMPLETE — ACCEPTED

## Artifact under review

The reviewed artifact is the provenance-bound canonical V3 PDF built from repository SHA
`da02f17df4d2d0a1568edbbe8bfbbfffb7208966` by temporary workflow run `33983729996`
(artifact `9974546873`).

- file: `abntexto-ufc-v3-canonical.pdf`;
- SHA-256: `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`;
- size: 450652 bytes;
- pages: 55;
- page size: A4 (`595.276 x 841.89 pt`);
- PDF version: 1.7;
- engine: pdfLaTeX / pdfTeX 1.40.29;
- TeX Live: 2026;
- encrypted: no;
- text based: yes;
- all fonts reported embedded by `pdffonts`.

The pre-existing 2026-09-04 PDF remains comparison-only and is not acceptance evidence.

## Review method

The canonical PDF was rendered completely at 200 DPI. All 55 pages were reviewed in sequence using grouped contact sheets, with targeted full-page inspection of presentation-sensitive and high-density pages. Independent preflight was repeated with PDF tooling before visual acceptance.

The review checked clipping, overlaps, broken glyphs, unexpected blank pages, pagination, heading placement, front matter, object bounds, reference-list presentation, appendix/annex presentation and the intentional fallback behavior for optional externally downloaded reference photographs.

No replacement character (`U+FFFD`) was found in extracted text.

A later independent recovery of artifact `9974546873` repeated the structural inspection and complete contact-sheet scan. It confirmed 55 A4 pages, PDF 1.7, unencrypted text-based output, embedded fonts and no newly observed visual defect. This corroborates the original review rather than creating a new acceptance artifact.

## Complete page review

| Pages | Surface | Result | Review notes |
|---|---|---|---|
| 1 | Cover | PASS | Complete-author placeholder visible; optional department omitted cleanly; coat of arms and institutional hierarchy are centered; no clipping or overlap. |
| 2 | Title page | PASS | Author/title/nature/advisor/city/year are visually stable; advisor final punctuation is visible; no overflow. |
| 3 | Errata | PASS | Heading/table/reference line render cleanly with large intentional remaining whitespace. |
| 4 | Approval page | PASS | Six-member committee fits the page; `Instituição (SIGLA)` surfaces render; separators and text blocks do not collide. |
| 5-7 | Dedication, acknowledgements, epigraph | PASS | Sparse layouts are intentional and stable; no unexpected headings or overflow. |
| 8-9 | RESUMO / ABSTRACT | PASS | Headings start at the expected top presentation position; summary and keyword blocks are visually clean. |
| 10-15 | Lists | PASS | Illustration/table/code/algorithm/abbreviation/symbol lists are legible, aligned and unclipped. |
| 16-18 | Table of contents | PASS | Three-page TOC is continuous; post-textual entries are uppercase/bold where required; no synthetic aggregate APÊNDICES/ANEXOS entry is present. |
| 19-33 | Main textual guide | PASS | Page numbers, headings, paragraphs, footnotes/citations and section transitions remain inside the text area with no visible collision or glyph defect. |
| 34-35 | Synthetic figures / object bounds | PASS | Upper identifications are visually distinct from reduced lower source/note blocks; objects remain bounded. |
| 36 | External institutional-photo examples | PASS — INTENTIONAL FALLBACK | The normal canonical build intentionally renders bordered fallback boxes when licensed external photographs are not downloaded. Source/note blocks remain correct and bounded. |
| 37 | Graph / frame | PASS | Graph, axis labels, source/note and following frame render without collision or clipping. |
| 38 | Numeric table / code start | PASS | Open-side IBGE-style table, title/source/note and first code example render cleanly. |
| 39 | Code examples | PASS | C++, external Python and Java examples remain readable and bounded; source blocks are separated from code. |
| 40-41 | Algorithms, equation, long quotation, alíneas | PASS | Algorithm objects, equation number, long-quote block, alínea/subalínea indentation and punctuation are visually stable. |
| 42-45 | Resources and post-textual guidance | PASS | Headings and text blocks remain stable; no overflow or unexpected blank page. |
| 46-47 | References | PASS | Two-page list is readable, left aligned, single-spaced within entries and free of clipping; item 33 remains an authority question, not a visual failure. |
| 48 | Glossary | PASS | Heading and definition layout are stable. |
| 49-52 | Appendices A-D | PASS | Each appendix starts on its own page; uppercase/bold centered heading presentation is clean; examples remain bounded. |
| 53-54 | Annexes A-B | PASS | Uppercase/bold centered headings render correctly; Annex A explicitly presents `Fonte:` attribution; no aggregate annex page is introduced. |
| 55 | Index | PASS | Two-column index is balanced, readable and inside margins; page number placement is stable. |

## Presentation-sensitive librarian reconfirmation

| Review item | Rendered evidence | Result |
|---:|---|---|
| 1 | Page 1 omits the blank department line without leaving a stray label or visible gap artifact. | PASS |
| 2 | Pages 1, 2 and 4 visibly render `NOME COMPLETO DO AUTOR`. | PASS |
| 7 | Page 4 visibly renders committee institutions with `(UFC)` and `(SIGLA)`. | PASS |
| 10 | Page 8 presents `RESUMO` at the normal top heading position with no vertical displacement anomaly. | PASS |
| 11 | Object titles in pages 34-40 use sentence-case examples without legacy title capitalization. | PASS |
| 15 | Page 18 shows appendix/annex TOC entries in uppercase and bold presentation. | PASS |
| 16 | The main-text reference guide preserves the full institutional first-use form already source/PDF-gated; no presentation regression was observed. | PASS |
| 21 | Pages 34-40 visually preserve body-size upper object identification and reduced lower source/note typography; independent final-PDF measurement remains 12 pt / 10 pt. | PASS |
| 28 | Main-text example headings remain sentence case; no legacy malformed `etc.` heading is visible. | PASS |
| 34 | Pages 53-54 have uppercase/bold centered annex headings; page 53 visibly includes external-material `Fonte:` attribution. | PASS |

Item 33 remains `NORMATIVE-REVIEW`. This visual inspection does not strengthen disputed NBR 6023:2025 edge cases into normative requirements.

## Preservation comparison

A raster comparison against the older 2026-09-04 V3 PDF was performed only as preservation evidence. Both documents contain 55 pages. At 120 DPI, 28 pages were pixel-identical and 27 pages changed. The changed pages correspond to accepted corrections/reference-content updates; the comparison revealed no page-count drift. The older PDF is not treated as current authority.

## Global result

- pages reviewed: 55/55;
- unexplained visual FAIL: 0;
- clipping/overlap/broken-glyph finding: 0;
- unexpected blank-page finding: 0;
- presentation-sensitive librarian reconfirmations: PASS;
- optional external-photo fallback: intentional and documented;
- item 33: remains authority-deferred.

**Visual review result: PASS.**

## Phase-end acceptance

The visual review was incorporated into immutable Reference PDF Validation candidate `b64074c64941895f97fbe0f795ce826c798d17ce`.

- Static `33985595790`: SUCCESS.
- Full Linux `33985595798`: SUCCESS.

Reference PDF Validation is therefore CLOSED. This document remains the visual baseline for later regression comparison.

## Ongoing regression rule

Every later **material advance** that affects shared presentation must preserve this baseline or explicitly classify and revalidate the difference. Every later phase still requires its own **phase-end regression** before closure.
