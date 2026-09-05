# UFC Librarian Review — Consolidated 34-Point Contract

Updated: 2026-09-05

## Purpose

This document converts the union of the two annotated v1.1.1 review PDFs supplied by the project maintainer into a stable engineering contract for the v3 regression/correction cycle. Reviewer annotations are evidence, not automatic normative truth; current ABNT/UFC authority must be reconciled before normative runtime changes.

## Status vocabulary

- `PASS`: current v3 behavior and evidence satisfy the item.
- `PARTIAL`: behavior, documentation, evidence, or canonical presentation remains incomplete.
- `FAIL`: current v3 behavior/reference output contradicts the accepted requirement.
- `NORMATIVE-REVIEW`: authority remains insufficient to encode the requested behavior safely.

## Current summary

The Front Matter and Annex Closeout checkpoint `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8` passed Static `33980847191` and full Linux `33980847189`, with `PASS=31 FAIL=0 SKIP=0`. That Linux run emitted explicit `LIBRARIAN-REVIEW-EVIDENCE` PASS records for items 1, 2, 7 and 34.

Core Corrections then closed on immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, which passed Static `33982156041` and full Linux `33982156042`; Linux again ended `PASS=31 FAIL=0 SKIP=0` with the resolved reviewer evidence retained.

The consolidated review state remains **33 PASS, 0 PARTIAL, 0 FAIL, 1 NORMATIVE-REVIEW = 34 items**. Reference PDF Validation is now responsible for the remaining presentation reconfirmation of already-PASS visual requirements; visual review does not silently change normative classification.

Item 33 remains deliberately fail-closed pending authoritative current NBR 6023:2025 text for the disputed DOI/availability/repeated-author/corporate-author cases. This unresolved authority item does not authorize speculative runtime changes.

## Consolidated review contract

| # | Review requirement | Current v3 assessment | Primary surfaces |
|---:|---|---|---|
| 1 | Department/unit line must be optional (`se houver`) and omitted cleanly when absent. | PASS — Linux evidence proved blank department omitted and filled department rendered. | `core.def`, `academic-works.def`, cover evidence |
| 2 | Pre-textual author field/examples must make clear that the complete author name is required. | PASS — canonical generated output renders `NOME COMPLETO DO AUTOR`. | `template/main.tex`, reference document gate |
| 3 | Optional subtitle must be rendered consistently on cover, title page, and approval page. | PASS | `frontmatter.def`, `academic-works.def` |
| 4 | Advisor identification on the title page must end with the requested final punctuation. | PASS | `frontmatter.def`, `academic-works.def` |
| 5 | Co-advisor/co-advisora must be supported and rendered conditionally when present. | PASS | `core.def`, `frontmatter.def` |
| 6 | Master's and doctoral nature blocks must include area of concentration when applicable, including title and approval pages. | PASS | `core.def`, `frontmatter.def` |
| 7 | Committee member institution must support the `Instituição (sigla)` presentation where applicable. | PASS — approval-page evidence preserves `Instituição Externa de Teste (IET)`. | `frontmatter.def`, approval-page evidence |
| 8 | Approval-page committee must support additional members and remain variable in size. | PASS | `frontmatter.def`, `template/main.tex` |
| 9 | CAPES-funded works must carry guidance for the mandatory acknowledgment from Portaria CAPES nº 206/2018. | PASS | `template/frontmatter/acknowledgments.tex`, normative catalog |
| 10 | `RESUMO` must begin at the first usable text line/heading position instead of being vertically displaced. | PASS — automated geometry green; explicit visual reconfirmation belongs to Reference PDF Validation. | `frontmatter.def`, front-matter geometry tests |
| 11 | Figure/table/object titles must follow sentence-case capitalization where applicable. | PASS | reference content, source/PDF gates |
| 12 | Lists of abbreviations/acronyms and symbols must align with the 3 cm left text margin. | PASS | front-matter alignment checks |
| 13 | Pre-textual elements must not appear in the table of contents. | PASS | TOC checks |
| 14 | Do not create synthetic aggregate `APÊNDICES` or `ANEXOS` pages/TOC entries. | PASS | appendix/annex checks |
| 15 | Appendix and annex entries in the TOC must use the required uppercase/bold presentation. | PASS — explicit visual reconfirmation belongs to Reference PDF Validation. | appendix/annex integration and checks |
| 16 | First body-text use of UFC should present the full institutional name followed by `(UFC)`. | PASS | reference prose/examples, source/PDF gates |
| 17 | Academic text/code demonstrations must not accidentally change the adopted text family/nominal size. | PASS | `fonts.def`, `tests/integration/code-typography.sh` |
| 18 | Author/corporate-author names in citations must follow current NBR 10520 capitalization rather than legacy all-caps output. | PASS | `bibliography.def`, citation checks |
| 19 | Long direct quotations must include the page or other required locator when the source provides one. | PASS | citation fixtures/checks |
| 20 | Parenthetical citation punctuation after a long direct quotation must not contain an extraneous full stop before the citation. | PASS | citation fixtures/checks |
| 21 | Figure/table/object upper identification/title must use body-size typography (12 pt); lower legend/source/note remain reduced where applicable. | PASS — automated final-PDF evidence green; explicit visual reconfirmation belongs to Reference PDF Validation. | `objects.def`, object/IBGE final-PDF checks |
| 22 | Object title, source, and note blocks must use single spacing. | PASS | `objects.def`, object geometry checks |
| 23 | Object source indication should include a page locator when applicable. | PASS | documentary-source fixture/check |
| 24 | Alínea items begin with lowercase text when grammatically continuing the introductory sentence. | PASS | `layout.def`, reference fixture |
| 25 | Alínea items use semicolons between intermediate items and appropriate final punctuation. | PASS | `layout.def`, reference fixture |
| 26 | A nested subalínea sequence is introduced with a colon and uses the required subordinate punctuation. | PASS | `layout.def`, reference fixture |
| 27 | Alíneas are ordered alphabetically, not by Arabic numerals. | PASS | `ufclettereditems`, reference fixture |
| 28 | Example section/subsection headings must follow sentence case where appropriate, including correct `etc.` punctuation. | PASS | reference content/headings, source/PDF gates |
| 29 | First-line paragraph indentation must be consistent with the adopted UFC body-text rule. | PASS | body-paragraph checks |
| 30 | Unknown place/publisher data must not emit obsolete/inappropriate patterns for online resources; electronic examples must follow current NBR 6023 handling. | PASS — controlled reviewer case accepted at `bcd851b...`. | `nbr6023-2025.def`, bibliography fixtures |
| 31 | Thesis/dissertation references must use the correct work-type structure and must not duplicate or contradict the year. | PASS — controlled single-year evidence accepted at `bcd851b...`. | bibliography fixtures |
| 32 | Standard and multivolume examples must use the accepted publisher/year and physical-description conventions when applicable. | PASS — standard and bibliography-specific `2 v.` evidence accepted at `bcd851b...`. | bibliography fixtures/reference guide |
| 33 | DOI/availability, repeated-author treatment, `São Paulo (Estado)` and related edge cases must be reconciled against current NBR 6023:2025 before runtime changes. | NORMATIVE-REVIEW | bibliography runtime/fixtures/locator audit |
| 34 | Appendix/annex headings must use the required bold presentation, and annexed external material must explicitly identify its source. | PASS — canonical source/heading/TOC evidence plus independent bold-heading final-PDF evidence are green; explicit visual reconfirmation belongs to Reference PDF Validation. | appendix/annex integration, canonical annex/reference gate |

## Remaining normative conflict

Review item 33 remains fail-closed. Current NBR 6023:2025 is the governing technical edition, but exact authoritative text for the disputed edge cases is not available in the current evidence corpus. Do not convert older reviewer wording into current runtime law without that authority.

## Acceptance rule

No item is closed merely because source text looks plausible or a related test is green. Closure requires the applicable combination of authority/project classification, correct runtime/reference behavior, positive regression evidence, negative evidence where machine-detectable, and canonical presentation evidence when presentation is part of the requirement.

Reference PDF Validation may discover a presentation defect in an item currently classified PASS. If that occurs, record and classify the defect before changing this matrix or runtime.
