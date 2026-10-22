# Class-generated internationalization coverage — 3.1.0 development

This is the implementation inventory for the requested PT / EN / ES / FR *complete class-owned visible wording*. It is **not** an institutional authorization to translate fixed, legally significant UFC wording, and does not claim arbitrary author content is translated.

## Contract and precedence

- `document-language=pt|en|es|fr` is **opt-in**. When explicitly set, it selects the manuscript Babel language at document start, all class-owned institutional labels/text, and (unless `labels-language` was explicitly configured) the matching nine pre-textual headings. The user can override the general headings independently by setting `labels-language`.
- When `document-language` is absent, the summary-language policy defaults to PT, the historical Portuguese institutional strings remain, the nine-label presentation remains PT unless selected explicitly and **existing Babel language selection is not overridden**.
- `\DocumentMetadata{lang=...}` is declared by the author before `\documentclass`, and is *not* inferred or silently mutated from `document-language`. English, Spanish and French names of UFC units, degrees, real programs, academic bodies and individual names must be checked against institutional official nomenclature, not guessed by the class.
- The default project type ("Projeto de pesquisa") is translated only when no `project-type` is explicitly supplied. User-authored and program-mandated titles or nature statements override the descriptive translations.

## Inventory of class-owned text (32 document keys and 9 title keys)

| Surface | Coverage | Binding |
|---|---|---|
| Nine academic frontmatter headings | PT/EN/ES/FR | `labels-language`, automatically mirrors an explicitly set `document-language` unless itself explicitly overridden |
| Main/companion summaries and per-language keyword labels | PT/EN/ES/FR | Explicit summary language (2 labels) |
| Title page/approval page: five applicable nature formulas | PT/EN/ES/FR | `document-language` |
| Supervisor and co-supervisor labels, including gender-specific variants | PT/EN/ES/FR | `document-language` |
| Committee, approval/submission dates, volume and program type captions | PT/EN/ES/FR | `document-language` |
| Bibliography/reference and glossary headings | PT/EN/ES/FR | `document-language` |
| Additional code/algorithm/chart list headings and legend labels | PT/EN/ES/FR | `document-language` |
| Inherited appendix, annex, index and text-table captions | Best-effort opt-in bindings to available inherited macros | `document-language`, only when relevant macros are provided by installed dependencies |
| Institution names, degree titles, program names, PDF language metadata | Supplied by author or by institution | No automatic translation of proper names or legal descriptors |
| Externally generated citation language, figure/table legends, bibliography localization | Controlled by Babel, biblatex-abnt, abntexto, tabularray-abnt and their installed versions | PDF tests and independent compatibility review required; class does not promise arbitrary third-party terminology is fully translated |
| Body text, quotations, bibliography entry contents, alt text, research data | Supplied by author | Not automatically translated |

The `tests/integration/frontmatter/document-locale-catalog.py` gate rejects missing PT/EN/ES/FR keys and class-owned untranslated rendering routes in the declared catalog. The real `frontmatter-summary-languages.sh` suite renders four-language academic and article PDFs and checks translated thesis nature, committee, advisor, approval and submission dates; earlier seven-profile × four-heading smoke tests remain independent. Additional dedicated full-length foreign-language documents and an institutional terminology review are required before labeling this as 100% **validated end-to-end**.

## Institutional review before release

English wording such as *Doctoral thesis submitted to...*, *Examining Committee* and translated program descriptions is a **proposed descriptive rendering**, not an official UFC translation. The Brazilian standards and individual postgraduate program can require a Portuguese or bilingual nature statement even for an English manuscript. Normative approval, PDF/UA, physical bibliography compliance, PDF language, glossary/index interactions, typography and full seven-profile acceptance must stay separately gated. The historical Portuguese rendering and the immutable public 3.0.5 tag/assets are preserved; 3.1.0 remains unreleased.
