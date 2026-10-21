# v3.1.0 profile × display-locale PDF regression

The v3.1.0 class provides an opt-in `labels-language=pt|en|es|fr` setting for **nine front-matter display headings only**, with Portuguese as the default. It does **not** translate academic content, institutional names, title/degree/submission statements, references, `babel` hyphenation or PDF language metadata. The separately maintained Web/Lite language selector changes **browser presentation only**.

## Automated evidence and limits

The productive Front matter integration gate runs `tests/integration/frontmatter/frontmatter-labels-i18n.sh` for the nine heading translations and the implicit-versus-explicit PT baseline. It additionally runs `tests/integration/frontmatter/profile-locale-matrix.sh`, which builds an independent real `pdflatex` PDF for each of **seven profiles × four opt-in heading languages = 28 scenarios** using `tests/documents/profile-locale-matrix.tex`.

The matrix obtains the six non-article profile identifiers from the existing v3 API contract and adds the scientific-article profile explicitly. It fails for missing/duplicate profile IDs, wrong type/locale assignments, failed TeX builds, final-pass warnings/overflows, invalid A4 geometry, missing body text, absent localized table-of-contents headings in non-article profiles or article-specific front-block/section regressions. Article has no normal academic-work table of contents: a localized TOC heading is **not applicable** to that profile. Every passed case produces a source/PDF SHA-256 and page count in `artifacts/frontmatter/profile-locale-matrix.json` plus one structured log receipt.

This is a display-heading and profile-compatibility **smoke matrix**. All fixture content and `\DocumentMetadata{lang=pt-BR}` stay Portuguese irrespective of selected labels. The test does not certify full translation of 28 academic manuscripts, ABNT/UFC compliance, PDF/UA, accessibility reading order or a reviewer-approved seven-profile publication archive. The latest generated seven-profile release PDFs need separate source-bound human visual approval under [issue #507](https://github.com/tiagosombrra/abntexto-ufc/issues/507). The upstream section-tagging blocker remains [#459](https://github.com/tiagosombrra/abntexto-ufc/issues/459).

For developers: `sh tests/integration/frontmatter/profile-locale-matrix.sh` runs the bounded 28-case PDF test; `sh tests/integration/frontmatter/frontmatter.sh` includes both localization checks in the normal CI suite. This does not modify runtime normative rules or any previously released v3.0.5 asset.
