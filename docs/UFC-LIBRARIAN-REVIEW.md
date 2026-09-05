# UFC Librarian Review — Consolidated 34-Point Contract

Updated: 2026-09-04

## Purpose

This document converts the two annotated v1.1.1 review PDFs supplied by the project maintainer into a stable, reviewable engineering input for the v3 regression. The PDFs remain external review evidence; they are not committed to the repository.

The two review files must be considered together. The later combined review does not contain every annotation present in the earlier Eliene-only file, so this contract uses the union of both review layers.

These 34 items are **review requirements/evidence**, not automatically normative truth. When an item conflicts with the current ABNT edition, a current UFC institutional act, or the current project normative catalog, the conflict must be reconciled under `docs/NORMATIVE-BASE.md` before runtime behavior or proof state is changed.

## Status vocabulary

- `PASS`: current v3 behavior and evidence already satisfy the review item.
- `PARTIAL`: the mechanism exists, but the reference template, documentation, evidence, or an edge case remains incomplete.
- `FAIL`: current v3 behavior/reference output still contradicts the review item.
- `NORMATIVE-REVIEW`: review evidence conflicts with, or is not yet reconciled against, current normative authority.

## Consolidated review contract

| # | Review requirement | Current v3 assessment | Primary surfaces |
|---:|---|---|---|
| 1 | Department/unit line must be optional (`se houver`) and omitted cleanly when absent. | PARTIAL | `core.def`, `academic-works.def`, `template/main.tex` |
| 2 | Pre-textual author field/examples must make clear that the complete author name is required. | PARTIAL | `template/main.tex`, reference guidance |
| 3 | Optional subtitle must be rendered consistently on cover, title page, and approval page. | PASS | `frontmatter.def`, `academic-works.def` |
| 4 | Advisor identification on the title page must end with the requested final punctuation. | FAIL | `frontmatter.def`, `academic-works.def` |
| 5 | Co-advisor/co-advisora must be supported and rendered conditionally when present. | PASS | `core.def`, `frontmatter.def` |
| 6 | Master's and doctoral nature blocks must include area of concentration when applicable, including title and approval pages. | PASS | `core.def`, `frontmatter.def` |
| 7 | Committee member institution must support the `Instituição (sigla)` presentation where applicable. | PARTIAL | `core.def`, `frontmatter.def`, `template/main.tex` |
| 8 | Approval-page committee must support the additional members required by the reviewed example and remain variable in size. | PASS | `frontmatter.def`, `template/main.tex` |
| 9 | CAPES-funded works must carry guidance for the mandatory acknowledgment from Portaria CAPES nº 206/2018. | PASS | `template/frontmatter/acknowledgments.tex`, normative catalog |
| 10 | `RESUMO` must begin at the first usable text line/heading position instead of being vertically displaced. | PASS, verify in final visual baseline | `frontmatter.def`, front-matter geometry tests |
| 11 | Figure/table/object titles must follow sentence-case capitalization where applicable (for example, `atmosfera superior`). | PARTIAL | reference content, object fixtures |
| 12 | Lists of abbreviations/acronyms and symbols must align with the 3 cm left text margin. | PASS, keep regression evidence | `frontmatter.def`, `integrations/abntexto.def`, alignment checks |
| 13 | Pre-textual elements must not appear in the table of contents; the contents begin with the textual section (`Introdução`). | PASS | `frontmatter.def`, TOC checks |
| 14 | Do not create synthetic aggregate `APÊNDICES` or `ANEXOS` pages/TOC entries; start directly with `APÊNDICE A` / `ANEXO A`. | PASS | `template/main.tex`, appendix/annex checks |
| 15 | Appendix and annex entries in the TOC must use the required uppercase/bold presentation. | PASS, verify final visual baseline | appendix/annex integration and checks |
| 16 | First body-text use of UFC should present the full institutional name followed by `(UFC)` where the acronym is introduced. | PARTIAL | reference prose/examples |
| 17 | The reviewed academic text requests the same text font throughout; technical demonstration snippets must not accidentally change academic body typography. | NORMATIVE-REVIEW | template documentation, typography policy |
| 18 | Author and corporate-author names in citations must use the capitalization required by current NBR 10520 rather than legacy all-caps citation output. | PASS | `bibliography.def`, citation checks |
| 19 | Long direct quotations must include the page or other required locator when the source provides one. | PARTIAL | citation fixtures, reference guide |
| 20 | Parenthetical citation punctuation after a long direct quotation must not contain the reviewed extraneous full stop before the citation. | PARTIAL, add explicit fixture | citation fixtures/checks |
| 21 | Figure/table/object title/caption size was explicitly reviewed as 12 pt, the same size as the body text. | NORMATIVE-REVIEW — current project policy is 10 pt | `standards/catalog.json`, `objects.def`, object checks, reference guide |
| 22 | Object title, source, and note blocks must use single spacing. | PASS | `objects.def`, object geometry checks |
| 23 | Object source indication should include a page locator when applicable. | PARTIAL | reference examples, citation/source guidance |
| 24 | Alínea items begin with lowercase text when grammatically continuing the introductory sentence. | PASS | `layout.def`, reference fixture |
| 25 | Alínea items use semicolons between intermediate items and appropriate final punctuation. | PASS | `layout.def`, reference fixture |
| 26 | A nested subalínea sequence is introduced with a colon and uses the required subordinate punctuation. | PASS | `layout.def`, reference fixture |
| 27 | Alíneas are ordered alphabetically, not by Arabic numerals. | PASS | `ufclettereditems`, reference fixture |
| 28 | Example section/subsection headings must follow sentence-case where appropriate, including `Usando fórmulas matemáticas`, `Usando código-fonte`, `Usando teoremas, proposições etc.`, `Usando questões`, and `Resultados do experimento A`; `etc.` keeps its period. | PARTIAL | reference content/headings |
| 29 | First-line paragraph indentation must be consistent with the adopted UFC body-text rule. | PASS | `layout.def`, body-paragraph checks |
| 30 | Unknown place/publisher data must not emit obsolete/inappropriate `[S. l.: s. n.]` patterns for online resources; UFC electronic-reference examples must follow current NBR 6023 handling. | PASS/PARTIAL — compatibility exists; output fixtures need reviewer-case coverage | `nbr6023-2025.def`, bibliography fixtures |
| 31 | Thesis/dissertation references must use the correct work-type structure and must not duplicate or contradict the year. | PASS for current Almeida fixture; add regression cases | `template/backmatter/references.bib`, bibliography checks |
| 32 | Standard and multivolume examples must use the reviewed publisher/year and physical-description conventions, including cases such as `2 v.` when applicable. | PARTIAL | bibliography fixtures and guide |
| 33 | DOI/availability presentation, repeated-author treatment, `São Paulo (Estado)` examples, and related reference examples must be reconciled against current NBR 6023:2025 before implementation. | NORMATIVE-REVIEW | `bibliography.def`, `nbr6023-2025.def`, bibliography fixtures |
| 34 | Appendix/annex headings must use the required bold presentation, and annexed external material must explicitly identify its source. | PARTIAL — heading behavior exists; annex source guidance is missing | appendix/annex integration, `template/backmatter/annexes/annex-a.tex` |

## Immediate conflicts requiring explicit authority reconciliation

### Object title/caption font size

The librarian review repeatedly marks object titles/captions as **12 pt, same as body text**. Current v3 intentionally renders object legends with `\abntsmall` and the machine-readable catalog classifies illustration captions under the 10 pt reduced-font policy. This is a real conflict between review evidence and current project policy. It must be resolved from current UFC/ABNT authority before changing `objects.def`, `standards/catalog.json`, tests, or proof state.

### Bibliographic edge cases

The review was produced against an older template and includes reference-format corrections that predate the project's NBR 6023:2025 compatibility layer. Those comments remain valuable regression cases, but every disputed DOI, unknown-publication-data, repeated-author, thesis/dissertation, and electronic-resource behavior must be checked against the current 2025 standard before it becomes a v3 rule.

### Font consistency in examples

The review's request for the same font throughout the academic text must be separated from legitimate code/command notation used by the reference guide. The regression must prove that documentation markup does not silently redefine the academic body's font policy while still allowing semantically distinct code examples.

## Acceptance rule

No item above is considered closed merely because the PDF looks plausible or a related test is green. Closure requires:

1. current authority or explicit project-policy classification;
2. runtime/reference behavior consistent with that classification;
3. a positive regression fixture or an explicitly manual review contract;
4. a negative fixture for rules whose failure can be automatically detected;
5. final visual inspection of the canonical v3 reference PDF where presentation is part of the requirement.
