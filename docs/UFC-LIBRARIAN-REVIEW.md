# UFC Librarian Review — Consolidated 34-Point Contract

Updated: 2026-09-09

## Purpose

This document converts the union of the two annotated v1.1.1 review PDFs supplied by the project maintainer into a stable engineering contract for the v3 regression/correction cycle. Reviewer annotations are evidence, not automatic normative truth; current ABNT/UFC authority must be reconciled before normative runtime changes.

## Status vocabulary

- `PASS`: current v3 behavior and evidence satisfy the item.
- `PARTIAL`: behavior, documentation, evidence, or canonical presentation remains incomplete.
- `FAIL`: current v3 behavior/reference output contradicts the accepted requirement.
- `NORMATIVE-REVIEW`: authority remains insufficient to encode the requested behavior safely.

## Current summary

The consolidated review state is **34 PASS, 0 PARTIAL, 0 FAIL, 0 NORMATIVE-REVIEW = 34 items**.

All review items have now been reconciled against the applicable current technical/institutional authority and converted into executable or presentation evidence where appropriate. Reference PDF Validation previously closed with a complete **55/55-page visual PASS with 0 unexplained visual failures**; the later Scientific Article and Final Certification phases preserved the shared foundation.

Item 33 was closed on 2026-09-09 after direct review of the primary ABNT NBR 6023:2025 text. The authoritative locators used for closure are sections **6.6**, **8.1.2**, **8.1.2.2–8.1.2.3**, **8.13**, and **9.1**, together with the standard's examples for online references, legal-person authorship/jurisdiction and repeated authorship. The resulting behavior is regression-tested in `tests/integration/references-6023.sh` with controlled fixtures.

## Consolidated review contract

| # | Review requirement | Current v3 assessment | Primary surfaces |
|---:|---|---|---|
| 1 | Department/unit line must be optional (`se houver`) and omitted cleanly when absent. | PASS — automated cover evidence plus canonical page-1 visual reconfirmation. | `core.def`, `academic-works.def`, cover evidence |
| 2 | Pre-textual author field/examples must make clear that the complete author name is required. | PASS — canonical output renders `NOME COMPLETO DO AUTOR`; visually reconfirmed. | `template/main.tex`, reference document gate |
| 3 | Optional subtitle must be rendered consistently on cover, title page, and approval page. | PASS | `frontmatter.def`, `academic-works.def` |
| 4 | Advisor identification on the title page must end with the requested final punctuation. | PASS | `frontmatter.def`, `academic-works.def` |
| 5 | Co-advisor/co-advisora must be supported and rendered conditionally when present. | PASS | `core.def`, `frontmatter.def` |
| 6 | Master's and doctoral nature blocks must include area of concentration when applicable, including title and approval pages. | PASS | `core.def`, `frontmatter.def` |
| 7 | Committee member institution must support the `Instituição (sigla)` presentation where applicable. | PASS — approval-page evidence and canonical visual review preserve `(UFC)` / `(SIGLA)`. | `frontmatter.def`, approval-page evidence |
| 8 | Approval-page committee must support additional members and remain variable in size. | PASS | `frontmatter.def`, `template/main.tex` |
| 9 | CAPES-funded works must carry guidance for the mandatory acknowledgment from Portaria CAPES nº 206/2018. | PASS | `template/frontmatter/acknowledgments.tex`, normative catalog |
| 10 | `RESUMO` must begin at the first usable text line/heading position instead of being vertically displaced. | PASS — automated geometry and canonical page-8 visual review agree. | `frontmatter.def`, front-matter geometry tests |
| 11 | Figure/table/object titles must follow sentence-case capitalization where applicable. | PASS — source/PDF gates and canonical object-page visual review. | reference content, source/PDF gates |
| 12 | Lists of abbreviations/acronyms and symbols must align with the 3 cm left text margin. | PASS | front-matter alignment checks |
| 13 | Pre-textual elements must not appear in the table of contents. | PASS | TOC checks |
| 14 | Do not create synthetic aggregate `APÊNDICES` or `ANEXOS` pages/TOC entries. | PASS | appendix/annex checks |
| 15 | Appendix and annex entries in the TOC must use the required uppercase/bold presentation. | PASS — canonical TOC visual review reconfirmed presentation. | appendix/annex integration and checks |
| 16 | First body-text use of UFC should present the full institutional name followed by `(UFC)`. | PASS | reference prose/examples, source/PDF gates |
| 17 | Academic text/code demonstrations must not accidentally change the adopted text family/nominal size. | PASS | `fonts.def`, `tests/integration/code-typography.sh` |
| 18 | Author/corporate-author names in citations must follow current NBR 10520 capitalization rather than legacy all-caps output. | PASS | `bibliography.def`, citation checks |
| 19 | Long direct quotations must include the page or other required locator when the source provides one. | PASS | citation fixtures/checks |
| 20 | Parenthetical citation punctuation after a long direct quotation must not contain an extraneous full stop before the citation. | PASS | citation fixtures/checks |
| 21 | Figure/table/object upper identification/title must use body-size typography (12 pt); lower legend/source/note remain reduced where applicable. | PASS — measured 12/10 pt and visually reconfirmed. | `objects.def`, object/IBGE final-PDF checks |
| 22 | Object title, source, and note blocks must use single spacing. | PASS | `objects.def`, object geometry checks |
| 23 | Object source indication should include a page locator when applicable. | PASS | documentary-source fixture/check |
| 24 | Alínea items begin with lowercase text when grammatically continuing the introductory sentence. | PASS | `layout.def`, reference fixture |
| 25 | Alínea items use semicolons between intermediate items and appropriate final punctuation. | PASS | `layout.def`, reference fixture |
| 26 | A nested subalínea sequence is introduced with a colon and uses the required subordinate punctuation. | PASS | `layout.def`, reference fixture |
| 27 | Alíneas are ordered alphabetically, not by Arabic numerals. | PASS | `ufclettereditems`, reference fixture |
| 28 | Example section/subsection headings must follow sentence case where appropriate, including correct `etc.` punctuation. | PASS | reference content/headings, source/PDF gates |
| 29 | First-line paragraph indentation must be consistent with the adopted UFC body-text rule. | PASS | body-paragraph checks |
| 30 | Unknown place/publisher data must not emit obsolete/inappropriate patterns for online resources; electronic examples must follow current NBR 6023 handling. | PASS — controlled reviewer case accepted. | `nbr6023-2025.def`, bibliography fixtures |
| 31 | Thesis/dissertation references must use the correct work-type structure and must not duplicate or contradict the year. | PASS — controlled single-year evidence accepted. | bibliography fixtures |
| 32 | Standard and multivolume examples must use the accepted publisher/year and physical-description conventions when applicable. | PASS — standard and bibliography-specific `2 v.` evidence accepted. | bibliography fixtures/reference guide |
| 33 | DOI/availability, repeated-author treatment, `São Paulo (Estado)` and related legal-person edge cases must follow current NBR 6023:2025. | **PASS** — primary NBR 6023:2025 reviewed directly: online references preserve `Disponível em:`/`Acesso em:` even when DOI is present; repeated authorship is rendered explicitly; legal-person authorship uses the known/highlighted institutional form; homonymous jurisdiction is disambiguated, including `SÃO PAULO (Estado)`. | `abntexto-ufc.cls`, `bibliography.def`, `tests/fixtures/references-6023-2025.bib`, `tests/integration/references-6023.sh`; NBR 6023:2025 §§ 6.6, 8.1.2, 8.1.2.2–8.1.2.3, 8.13, 9.1 |
| 34 | Appendix/annex headings must use the required bold presentation, and annexed external material must explicitly identify its source. | PASS — final-PDF heading evidence plus canonical pages 53-54 visual source/heading reconfirmation. | appendix/annex integration, canonical annex/reference gate |

## Item 33 closure decision

The earlier fail-closed boundary is removed because primary current-edition authority is now available and has been reviewed directly.

The accepted interpretation is:

1. an online reference carries the prescribed availability and access-date elements; a DOI may additionally be present but does not erase those online-access elements when applicable;
2. consecutive references by the same author repeat the authorship instead of replacing it with an underline/dash convention;
3. a legal-person author is entered by the form by which it is known or highlighted in the document, consistently across references;
4. governmental authorship preserves the superior body/jurisdiction needed for identification, and homonymous state/municipality names are disambiguated with the corresponding parenthetical qualifier, such as `SÃO PAULO (Estado)`.

The runtime makes repeated-author rendering explicit through the `biblatex-abnt` `repeatfields=true` policy. Controlled render fixtures verify all four item-33 surfaces with both pdfLaTeX and LuaLaTeX through the existing NBR 6023 regression gate.

## Acceptance rule

No item is closed merely because source text looks plausible or a related test is green. Closure requires the applicable combination of authority/project classification, correct runtime/reference behavior, positive regression evidence, negative evidence where machine-detectable, and canonical presentation evidence when presentation is part of the requirement.

The same discipline applies to every later **material advance**, and every roadmap phase still requires its own **phase-end regression** before closure.
