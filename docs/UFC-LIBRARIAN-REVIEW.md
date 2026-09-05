# UFC Librarian Review — Consolidated 34-Point Contract

Updated: 2026-09-05

## Purpose

This document converts the two annotated v1.1.1 review PDFs supplied by the project maintainer into a stable engineering contract for the v3 regression/correction cycle. The two review files are complementary; this contract uses their union.

Reviewer annotations are evidence, not automatic normative truth. When a review item interacts with a current ABNT edition, UFC institutional requirement, or the project normative catalog, authority must be reconciled before runtime/proof state changes.

## Status vocabulary

- `PASS`: current v3 behavior and evidence satisfy the item.
- `PARTIAL`: behavior, documentation, evidence, or a visual/canonical edge remains incomplete.
- `FAIL`: current v3 behavior/reference output contradicts the accepted requirement.
- `NORMATIVE-REVIEW`: current authority is still insufficient to encode the requested behavior safely.

## Current summary

Validated checkpoint `f6ca012164273e67480dca127fe17b392e8a8a21` passed Static contract run `33939512055` and full Linux integration run `33939512019`.

Object-typography implementation checkpoint `f2f5124c4adcb34069a667f1ef80c76fb17728bd` migrated the illustration/object path, normative rule IDs, locators and final-PDF expectations. Branch-level Static run `33963240056` passed, but full Linux run `33963240297` correctly failed the object-geometry gate with one isolated residual: illustration identification measured 12 pt and illustration/table sources measured 10 pt, while the `tabularray-abnt` table identification still measured 10 pt instead of 12 pt.

The root cause was the project compatibility adapter in `abntexto-ufc/modules.def`, which still overrode `caption,lasthead,capcont` to `\abntsmall`. Follow-up implementation commit `7ec385ebecf21ba17e59db1e7ec16d3336f4bf4c` restores those upper table styles to `\normalsize` while retaining reduced lower continuation/source/note typography. Review item 21 remains `FAIL` until the corrected branch checkpoint passes Static contract and full Linux integration.

Current review state: **24 PASS, 8 PARTIAL, 1 FAIL, 1 NORMATIVE-REVIEW = 34 items**.

## Consolidated review contract

| # | Review requirement | Current v3 assessment | Primary surfaces |
|---:|---|---|---|
| 1 | Department/unit line must be optional (`se houver`) and omitted cleanly when absent. | PARTIAL — guidance/runtime improved; canonical blank/filled visual confirmation remains. | `core.def`, `academic-works.def`, `template/main.tex` |
| 2 | Pre-textual author field/examples must make clear that the complete author name is required. | PARTIAL — canonical placeholder corrected; final reference-PDF confirmation remains. | `template/main.tex`, reference guidance |
| 3 | Optional subtitle must be rendered consistently on cover, title page, and approval page. | PASS | `frontmatter.def`, `academic-works.def` |
| 4 | Advisor identification on the title page must end with the requested final punctuation. | PASS — runtime correction is present and full integration is green. | `frontmatter.def`, `academic-works.def` |
| 5 | Co-advisor/co-advisora must be supported and rendered conditionally when present. | PASS | `core.def`, `frontmatter.def` |
| 6 | Master's and doctoral nature blocks must include area of concentration when applicable, including title and approval pages. | PASS | `core.def`, `frontmatter.def` |
| 7 | Committee member institution must support the `Instituição (sigla)` presentation where applicable. | PARTIAL — canonical examples improved; final approval-page visual confirmation remains. | `core.def`, `frontmatter.def`, `template/main.tex` |
| 8 | Approval-page committee must support additional members and remain variable in size. | PASS | `frontmatter.def`, `template/main.tex` |
| 9 | CAPES-funded works must carry guidance for the mandatory acknowledgment from Portaria CAPES nº 206/2018. | PASS | `template/frontmatter/acknowledgments.tex`, normative catalog |
| 10 | `RESUMO` must begin at the first usable text line/heading position instead of being vertically displaced. | PASS — retain final visual confirmation. | `frontmatter.def`, front-matter geometry tests |
| 11 | Figure/table/object titles must follow sentence-case capitalization where applicable. | PARTIAL | reference content, object fixtures |
| 12 | Lists of abbreviations/acronyms and symbols must align with the 3 cm left text margin. | PASS | front-matter alignment checks |
| 13 | Pre-textual elements must not appear in the table of contents. | PASS | TOC checks |
| 14 | Do not create synthetic aggregate `APÊNDICES` or `ANEXOS` pages/TOC entries. | PASS | appendix/annex checks |
| 15 | Appendix and annex entries in the TOC must use the required uppercase/bold presentation. | PASS — retain final visual confirmation. | appendix/annex integration and checks |
| 16 | First body-text use of UFC should present the full institutional name followed by `(UFC)`. | PARTIAL — reference prose corrected; canonical PDF confirmation remains. | reference prose/examples |
| 17 | Academic text/code demonstrations must not accidentally change the adopted text family/nominal size. | PASS — code typography regression proves same family and nominal 12 pt across body/code/algorithm paths exercised by the gate. | `fonts.def`, `tests/integration/code-typography.sh` |
| 18 | Author/corporate-author names in citations must follow current NBR 10520 capitalization rather than legacy all-caps output. | PASS | `bibliography.def`, citation checks |
| 19 | Long direct quotations must include the page or other required locator when the source provides one. | PASS — reviewer fixture renders `p. 42`; full Linux integration green. | citation fixtures/checks |
| 20 | Parenthetical citation punctuation after a long direct quotation must not contain an extraneous full stop before the citation. | PASS — explicit positive/negative reviewer gate; full Linux integration green. | citation fixtures/checks |
| 21 | Figure/table/object upper identification/title must use body-size typography (12 pt); lower legend/source/note remain reduced where applicable. | FAIL — branch regression isolated the remaining table adapter at 10 pt; commit `7ec385e...` corrects it to body size, but Static/full Linux confirmation is still required before closure. | `objects.def`, `modules.def`, normative contract, object final-PDF checks |
| 22 | Object title, source, and note blocks must use single spacing. | PASS | `objects.def`, object geometry checks |
| 23 | Object source indication should include a page locator when applicable. | PASS — external illustration fixture renders `p. 42`; full Linux integration green. | documentary-source fixture/check |
| 24 | Alínea items begin with lowercase text when grammatically continuing the introductory sentence. | PASS | `layout.def`, reference fixture |
| 25 | Alínea items use semicolons between intermediate items and appropriate final punctuation. | PASS | `layout.def`, reference fixture |
| 26 | A nested subalínea sequence is introduced with a colon and uses the required subordinate punctuation. | PASS | `layout.def`, reference fixture |
| 27 | Alíneas are ordered alphabetically, not by Arabic numerals. | PASS | `ufclettereditems`, reference fixture |
| 28 | Example section/subsection headings must follow sentence case where appropriate, including correct `etc.` punctuation. | PARTIAL | reference content/headings |
| 29 | First-line paragraph indentation must be consistent with the adopted UFC body-text rule. | PASS | body-paragraph checks |
| 30 | Unknown place/publisher data must not emit obsolete/inappropriate patterns for online resources; electronic examples must follow current NBR 6023 handling. | PASS/PARTIAL — compatibility exists; reviewer-case coverage remains. | `nbr6023-2025.def`, bibliography fixtures |
| 31 | Thesis/dissertation references must use the correct work-type structure and must not duplicate or contradict the year. | PASS — retain additional negative regression case. | bibliography fixtures |
| 32 | Standard and multivolume examples must use the accepted publisher/year and physical-description conventions when applicable. | PARTIAL | bibliography fixtures/reference guide |
| 33 | DOI/availability, repeated-author treatment, `São Paulo (Estado)` and related edge cases must be reconciled against current NBR 6023:2025 before runtime changes. | NORMATIVE-REVIEW | bibliography runtime/fixtures/locator audit |
| 34 | Appendix/annex headings must use the required bold presentation, and annexed external material must explicitly identify its source. | PARTIAL — source example and heading behavior exist; canonical visual confirmation remains. | appendix/annex integration, canonical annex |

## Resolved authority decision — object title typography

The UFC academic-work guide currently linked by the Sistema de Bibliotecas states in 4.1(c) that the work uses size 12 generally and lists **legends and sources** of illustrations/tables among the smaller uniform exceptions. Sections 4.9 and 4.10 separately define the **upper identification/title** and the lower source/legend/note surfaces. The two librarian reviews independently mark the upper figure/table title as 12 pt.

Therefore the project classifies review item 21 as an actual runtime/contract defect rather than an unresolved reviewer preference:

- upper illustration/table/object identification/title: **12 pt**, single spaced;
- lower source/legend/note: **10 pt** where the reduced-font rule applies, single spaced;
- title/source/note remain bound to the object width.

The initial migration at `f2f5124c4adcb34069a667f1ef80c76fb17728bd` retires the two semantically incorrect reduced-title rule IDs, records their replacement mapping in `standards/rule-migrations.json`, separates illustration/table locator ownership, and updates object runtime plus final-PDF measurement expectations. Full Linux run `33963240297` then exposed a second independent styling surface: the `tabularray-abnt` compatibility adapter still forced the table caption family to reduced size. Commit `7ec385ebecf21ba17e59db1e7ec16d3336f4bf4c` corrects that residual without weakening the 12 pt/10 pt evidence contract.

The detailed reasoning and provenance are recorded in `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`. Exact current NBR 14724:2024 clause text remains unavailable in the repository; if authoritative licensed text later contradicts this institutional interpretation, the decision must be reopened fail-closed.

## Remaining normative conflict

Review item 33 remains fail-closed. Current NBR 6023:2025 is the governing technical edition, but exact authoritative text for the disputed DOI/online/repeated-author/corporate-author cases is not available in the current evidence corpus. Do not implement older review wording as current runtime law without that authority.

## Acceptance rule

No item is closed merely because a PDF looks plausible or a related test is green. Closure requires the applicable combination of authority/project classification, correct runtime/reference behavior, positive regression evidence, negative evidence where machine-detectable, and canonical visual inspection when presentation is part of the requirement.
