# Class-generated internationalization coverage — 3.1.0 development

This is the implementation inventory for the requested PT / EN / ES / FR *complete class-owned visible wording*. It is **not** an institutional authorization to translate fixed, legally significant UFC wording, and does not claim arbitrary author content is translated.

## Contract and precedence

- `document-language=pt|en|es|fr` is **opt-in**. When explicitly set, it selects the manuscript Babel language at document start, all class-owned institutional labels/text, and (unless `labels-language` was explicitly configured) the matching nine pre-textual headings. The user can override the general headings independently by setting `labels-language`.
- When `document-language` is absent, the summary-language policy defaults to PT, the historical Portuguese institutional strings remain, the nine-label presentation remains PT unless selected explicitly and **this class adds no opt-out Babel override**. The inherited Babel/dependency startup can still reset a direct preamble `\selectlanguage{english}` to Brazilian Portuguese; use explicit `document-language=en` for a controlled English manuscript.
- `\DocumentMetadata{lang=...}` is declared by the author before `\documentclass`, and is *not* inferred or silently mutated from `document-language`. English, Spanish and French names of UFC units, degrees, real programs, academic bodies and individual names must be checked against institutional official nomenclature, not guessed by the class.
- The default project type ("Projeto de pesquisa") is translated only when no `project-type` is explicitly supplied. The entire Portuguese research-project nature sentence follows its original composition to preserve the tested baseline. Spanish `Fecha de aprobación` and French `Date d'approbation` are gender-neutral, so they remain grammatically valid for both masculine and feminine academic work types. User-authored and program-mandated titles or nature statements override the descriptive translations.

## Inventory of class-owned text (34 document keys and 9 title keys)

| Surface | Coverage | Binding |
|---|---|---|
| Nine academic frontmatter headings | PT/EN/ES/FR | `labels-language`, automatically mirrors an explicitly set `document-language` unless itself explicitly overridden |
| Main/companion summaries and per-language keyword labels | PT/EN/ES/FR | Explicit summary language (2 labels) |
| Title page/approval page: five applicable nature formulas | PT/EN/ES/FR | `document-language` |
| Supervisor and co-supervisor labels, including gender-specific variants | PT/EN/ES/FR | `document-language` |
| Committee, approval/submission dates, volume and program type captions | PT/EN/ES/FR | `document-language` |
| Bibliography/reference and glossary headings | PT/EN/ES/FR | `document-language` |
| Additional code/algorithm/chart list headings and legend labels | PT/EN/ES/FR | `document-language` |
| Inherited appendix, annex, index, figure/table captions, object source/note prefixes and text-table captions | Opt-in bindings to actual upstream `\appendixlabel`, `\annexlabel`, `\abntextonotelabel` and other available inherited macros | `document-language`, only when relevant macros are provided by installed dependencies |
| Institution names, degree titles, program names, PDF language metadata | Supplied by author or by institution | No automatic translation of proper names or legal descriptors |
| Externally generated citation language, figure/table legends, bibliography localization | Controlled by Babel, biblatex-abnt, abntexto, tabularray-abnt and their installed versions | PDF tests and independent compatibility review required; class does not promise arbitrary third-party terminology is fully translated |
| Body text, quotations, bibliography entry contents, alt text, research data | Supplied by author | Not automatically translated |

The `tests/integration/frontmatter/document-locale-catalog.py` gate rejects missing PT/EN/ES/FR keys and class-owned untranslated rendering routes in the declared catalog. The real `frontmatter-summary-languages.sh` suite renders four-language academic and article PDFs and checks translated thesis nature, committee, advisor, approval and submission dates; earlier seven-profile × four-heading smoke tests remain independent. Five real-PDF regression fixtures exercise inherited appendix/annex headings, source/note prefixes, and plain/normal-sub/alternative-sub object legends (legacy PT plus opt-in PT/EN/ES/FR). The opt-in object legend additionally rebinds the original upstream `\legendlabel` using `\nobreakspace` rather than Babel-active `~`; Spanish Babel otherwise raises `Argument of \language@active@arg~ has an extra }` when ending an object with a legend. Additional dedicated full-length foreign-language documents and an institutional terminology review are required before labeling this as 100% **validated end-to-end**.

## Historical summary keywords in opt-in foreign-language documents

Inside `\ufcPrintSummaryInLanguage{pt|en|es|fr}{file}`, the older `\ufcSummaryKeywords` and `\keywords` helpers are locally rebound to the content language. This prevents a hard-coded Portuguese **Palavras-chave** or English **Keywords** label from leaking into an ES/FR summary when an existing file is reused. Outside the explicit multilingual summary, the historical `\ufcPrintSummary`/`\ufcPrintAbstract` and keyword helper semantics remain unchanged; their meaning is intentionally language-specific. A nine-PDF positive/legacy regression covers the eight locale/helper combinations and the old PT/EN labels. It is a bounded functional proof, **not** a claim that all dependency-owned wording or 28 complete manuscripts are validated.

For the full acceptance target, see [I18N-COMPLETION-MATRIX.md](I18N-COMPLETION-MATRIX.md). A static catalog parity gate never replaces a productive PDF test of all supported commands/environments.

## Project homepage (issue #521)

The class bibliography jurisdiction driver now routes its optional judgment-date prefix through the document-language catalog (PT *julgado em*, EN *judged on*, ES *juzgado el*, FR *jugé le*); the author-supplied court, title and jurisdiction facts are unchanged. A new qpdf JSON v2 inspection independently verifies /Root/Lang against declared metadata in the 28 real primary-language PDFs and rejects missing or mismatched languages. These proofs do not translate legal norms or verify manuscript prose.

The **homepage** now has a separate, opt-in PT-BR/EN/ES/FR browser UI catalog (32 keys), controlled by an accessible language selector and optional `?lang=en|es|fr` deep link. Translation updates visible homepage copy, the document `html.lang` attribute and the meta description; it never rewrites canonical download/repository URLs, artifact names, validator results or normative rule descriptions. Portuguese remains the default without JavaScript. A Static contract verifies catalog parity and baseline content, and the productive offline Chromium E2E exercises all four languages and selector changes.

The **validator** continues to own its independent four-language `validator/ui-locales.js` interface catalog. The author-maintained Markdown manuals, normative wording from third-party libraries and official UFC program/degree names are **not** translated by the homepage feature. The published v3.0.5 stays immutable and v3.1.0 remains unreleased.

## Institutional review before release

English wording such as *Doctoral thesis submitted to...*, *Examining Committee* and translated program descriptions is a **proposed descriptive rendering**, not an official UFC translation. The Brazilian standards and individual postgraduate program can require a Portuguese or bilingual nature statement even for an English manuscript. Normative approval, PDF/UA, physical bibliography compliance, PDF language, glossary/index interactions, typography and full seven-profile acceptance must stay separately gated. The historical Portuguese rendering and the immutable public 3.0.5 tag/assets are preserved; 3.1.0 remains unreleased.

## Optional document modules — dedicated four-locale certification (in progress)

A proposed independent evidence workflow tests listings, code-list titles, pseudocode labels, multi-page `longabnttblr` with per-locale author-supplied source and note keys, and `minted` with real PDF artifacts in PT/EN/ES/FR. Its assertions read PDF text, Babel log and actual `/Root/Lang`, and preserve legacy Portuguese conventions. The module matrix does **not** automatically translate authors' captions, `remark{Fonte}` arguments, source prose, or code listings. Its status remains **PENDING** until all twelve PDFs pass on the exact commit and the main integration gates are green.
