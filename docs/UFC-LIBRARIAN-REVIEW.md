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

Regression Audit is closed. Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` closed item 21 with Static `33965794475` and Linux `33965794519` green (`PASS=31 FAIL=0 SKIP=0`).

Canonical-reference source checkpoint `3ae9dd698e021a117ba2b64ebf970dc8c507fa8f` subsequently passed Static `33968579418` and full Linux `33968579449`, again with `PASS=31 FAIL=0 SKIP=0`. Both runs emit source-level PASS evidence for review items 11, 16 and 28.

Implementation checkpoint `a1149f169f06b2db620bc5df69d0870b60fe583c` extends the compiled canonical-reference gate with PDF-text evidence for those same three items. They remain `PARTIAL` until that implementation is synchronized to the branch and Static/full Linux acceptance is green.

Current review state: **25 PASS, 8 PARTIAL, 0 FAIL, 1 NORMATIVE-REVIEW = 34 items**.

## Consolidated review contract

| # | Review requirement | Current v3 assessment | Primary surfaces |
|---:|---|---|---|
| 1 | Department/unit line must be optional (`se houver`) and omitted cleanly when absent. | PARTIAL — guidance/runtime improved; canonical blank/filled confirmation remains. | `core.def`, `academic-works.def`, `template/main.tex` |
| 2 | Pre-textual author field/examples must make clear that the complete author name is required. | PARTIAL — canonical placeholder corrected; final reference-PDF confirmation remains. | `template/main.tex`, reference guidance |
| 3 | Optional subtitle must be rendered consistently on cover, title page, and approval page. | PASS | `frontmatter.def`, `academic-works.def` |
| 4 | Advisor identification on the title page must end with the requested final punctuation. | PASS — runtime correction present and full integration green. | `frontmatter.def`, `academic-works.def` |
| 5 | Co-advisor/co-advisora must be supported and rendered conditionally when present. | PASS | `core.def`, `frontmatter.def` |
| 6 | Master's and doctoral nature blocks must include area of concentration when applicable, including title and approval pages. | PASS | `core.def`, `frontmatter.def` |
| 7 | Committee member institution must support the `Instituição (sigla)` presentation where applicable. | PARTIAL — canonical examples improved; final approval-page confirmation remains. | `core.def`, `frontmatter.def`, `template/main.tex` |
| 8 | Approval-page committee must support additional members and remain variable in size. | PASS | `frontmatter.def`, `template/main.tex` |
| 9 | CAPES-funded works must carry guidance for the mandatory acknowledgment from Portaria CAPES nº 206/2018. | PASS | `template/frontmatter/acknowledgments.tex`, normative catalog |
| 10 | `RESUMO` must begin at the first usable text line/heading position instead of being vertically displaced. | PASS — retain final visual confirmation. | `frontmatter.def`, front-matter geometry tests |
| 11 | Figure/table/object titles must follow sentence-case capitalization where applicable. | PARTIAL — source evidence accepted at `3ae9dd...`; generated-PDF gate implemented at `a1149...`, branch acceptance pending. | reference content, `reference_guide_contract.py`, `reference-document.sh` |
| 12 | Lists of abbreviations/acronyms and symbols must align with the 3 cm left text margin. | PASS | front-matter alignment checks |
| 13 | Pre-textual elements must not appear in the table of contents. | PASS | TOC checks |
| 14 | Do not create synthetic aggregate `APÊNDICES` or `ANEXOS` pages/TOC entries. | PASS | appendix/annex checks |
| 15 | Appendix and annex entries in the TOC must use the required uppercase/bold presentation. | PASS — retain final visual confirmation. | appendix/annex integration and checks |
| 16 | First body-text use of UFC should present the full institutional name followed by `(UFC)`. | PARTIAL — source evidence accepted at `3ae9dd...`; rendered full-name gate implemented at `a1149...`, branch acceptance pending. | reference prose/examples, source/PDF reference gates |
| 17 | Academic text/code demonstrations must not accidentally change the adopted text family/nominal size. | PASS — code typography regression proves same family and nominal 12 pt across exercised body/code/algorithm paths. | `fonts.def`, `tests/integration/code-typography.sh` |
| 18 | Author/corporate-author names in citations must follow current NBR 10520 capitalization rather than legacy all-caps output. | PASS | `bibliography.def`, citation checks |
| 19 | Long direct quotations must include the page or other required locator when the source provides one. | PASS — reviewer fixture renders `p. 42`; full Linux green. | citation fixtures/checks |
| 20 | Parenthetical citation punctuation after a long direct quotation must not contain an extraneous full stop before the citation. | PASS — explicit positive/negative reviewer gate; full Linux green. | citation fixtures/checks |
| 21 | Figure/table/object upper identification/title must use body-size typography (12 pt); lower legend/source/note remain reduced where applicable. | PASS — Static `33965794475` and Linux `33965794519` green; final-PDF and IBGE evidence confirm 12 pt upper / 10 pt lower split. | `objects.def`, `modules.def`, object/IBGE final-PDF checks |
| 22 | Object title, source, and note blocks must use single spacing. | PASS | `objects.def`, object geometry checks |
| 23 | Object source indication should include a page locator when applicable. | PASS — external illustration fixture renders `p. 42`; full Linux green. | documentary-source fixture/check |
| 24 | Alínea items begin with lowercase text when grammatically continuing the introductory sentence. | PASS | `layout.def`, reference fixture |
| 25 | Alínea items use semicolons between intermediate items and appropriate final punctuation. | PASS | `layout.def`, reference fixture |
| 26 | A nested subalínea sequence is introduced with a colon and uses the required subordinate punctuation. | PASS | `layout.def`, reference fixture |
| 27 | Alíneas are ordered alphabetically, not by Arabic numerals. | PASS | `ufclettereditems`, reference fixture |
| 28 | Example section/subsection headings must follow sentence case where appropriate, including correct `etc.` punctuation. | PARTIAL — source evidence accepted at `3ae9dd...`; generated-PDF gate implemented at `a1149...`, branch acceptance pending. | reference content/headings, source/PDF reference gates |
| 29 | First-line paragraph indentation must be consistent with the adopted UFC body-text rule. | PASS | body-paragraph checks |
| 30 | Unknown place/publisher data must not emit obsolete/inappropriate patterns for online resources; electronic examples must follow current NBR 6023 handling. | PASS/PARTIAL — compatibility and current profile tests exist; reviewer-case coverage remains. | `nbr6023-2025.def`, bibliography fixtures |
| 31 | Thesis/dissertation references must use the correct work-type structure and must not duplicate or contradict the year. | PASS — retain/add negative duplicate-year regression. | bibliography fixtures |
| 32 | Standard and multivolume examples must use the accepted publisher/year and physical-description conventions when applicable. | PARTIAL | bibliography fixtures/reference guide |
| 33 | DOI/availability, repeated-author treatment, `São Paulo (Estado)` and related edge cases must be reconciled against current NBR 6023:2025 before runtime changes. | NORMATIVE-REVIEW | bibliography runtime/fixtures/locator audit |
| 34 | Appendix/annex headings must use the required bold presentation, and annexed external material must explicitly identify its source. | PARTIAL — source example and heading behavior exist; canonical visual confirmation remains. | appendix/annex integration, canonical annex |

## Resolved authority decision — object title typography

The project accepts 12 pt, single-spaced upper illustration/table/object identification/title and reduced 10 pt, single-spaced lower source/legend/note where applicable. Acceptance evidence is complete for the automated contract: Static `33965794475`, Linux `33965794519`, illustration/table final-PDF checks and the IBGE table subset are green. Item 21 is `PASS`.

## Remaining normative conflict

Review item 33 remains fail-closed. Current NBR 6023:2025 is the governing technical edition, but exact authoritative text for the disputed DOI/online/repeated-author/corporate-author cases is not available in the current evidence corpus. Do not implement older review wording as current runtime law without that authority.

## Acceptance rule

No item is closed merely because source text looks plausible or a related test is green. Closure requires the applicable combination of authority/project classification, correct runtime/reference behavior, positive regression evidence, negative evidence where machine-detectable, and canonical presentation evidence when presentation is part of the requirement.
