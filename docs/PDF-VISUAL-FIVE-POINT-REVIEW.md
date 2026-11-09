# Five-point visual review: canonical PT tutorial (2026-11-05)

**Scope:** user-marked pages 3, 9, 10, 15 and 18 of the 22-page
`abntexto-ufc-referencia-pt-corrigida-validacao.pdf`.
Input PDF SHA256: `315fc3f92ec7d03d72e869d887f1d1449243b7b00773471555b79c8b6af1af7a`.
Source: issue #555. Prior PDF was technically useful diagnostic evidence, **not a release-certified document**.

## Observations and decisions

1. **TOC/list dotted leaders — defect.** The actual page-9 PDF has an
   initial first-to-second dot separation of 16.87pt in one primary entry,
   followed by an exact 9.00pt pitch; further primary entries exhibit
   13–20pt single anomalous gaps. The root class macro concatenated a forced
   1.1em leader hbox with a separate leader run. Use **one** continuous
   leader stream and assert all neighboring dots share the same 9pt-ish
   pitch across table of contents and pretextual lists using original
   PDF BBox word coordinates, not just PDF text.
2. **Page folio — correctly placed.** The first textual page (physical
   page 10, printed logical folio 9) uses an upper-right Arabic numeral.
   Measured right edge: 56.69pt = 2.00cm from the physical A4 edge; glyph
   top: 52.54pt from the top. The latter differs from the logical 2cm
   baseline anchor because a glyph's bounding box is not a text baseline.
   **Do not move it to the footer.** ABNT NBR 14724:2024 sec. 5.3:
   upper right on recto; upper left on verso. Add an observed-position
   regression with a tolerance for glyph ascent.
3. **IBGE tables — do not introduce alternating colors as a normative
   default.** Keep minimal horizontal rules and open sides. The 1993 IBGE
   tabular standard does not prescribe zebra striping and explicitly
   reserves graphic/editorial design choice; a low-contrast grayscale
   alternative may be documented separately for digital contexts, with
   instructor/library approval and print/contrast verification. Its
   mere presence must never count as IBGE-compliance evidence.
4. **LaTeX logo in ordinary prose — user-requested editorial correction.**
   The special `\\LaTeX{}` control sequence produces a deliberately
   different display logo. Use literal `LaTeX` in the three example
   academic chapters, preserving the selected body family. Do not alter
   monospaced fonts in source-code listings.
5. **Committee signatures — UFC institutional spacing correction.** The
   previous name-to-institution line distance is 13.80pt for all three
   members (single line spacing), with approximately 55pt between
   signature members. The UFC 2022 normalization guide specifies
   centered 12pt text at **1.5 line spacing** for the committee block.
   Use `\\onehalfsp` for names and institutions, a small additional
   gap below each signature rule and an adaptive inter-member gap for
   committees with 3–7 members, then validate real PDF geometry and
   absence of approval-page overflow. The 2022 guide predates NBR
   14724:2024, so avoid presenting this as an exact centimeter value
   mandated by the newer national standard.

## Regression and release gates

The canonical real-PDF contract at
`tests/integration/citations/reference-corpus.sh` now verifies
continuous dot pitch (including list pages), uniform actual committee
name/affiliation vertical geometry, the top-right 2cm textual folio,
and rendered ordinary `LaTeX` rather than a special logo in the
three tutorial chapters. All checks reject the prior marked PDF.
Existing signature-count/multi-profile fixtures continue to test
larger committees; no new CI result is asserted until the exact branch
SHA has compiled actual PDFs and the PDF has been independently reviewed.

Source URLs:
- ABNT NBR 14724:2024 section 5.3 (pagination)
- https://biblioteca.ufc.br/wp-content/uploads/2022/05/guianormalizacaotrabalhosacademicos-17.05.2022.pdf (approval page)
- https://biblioteca.ibge.gov.br/visualizacao/livros/liv23907.pdf (IBGE 1993)

Status: **PENDING_CI_AND_R5_VISUAL_REVIEW**; 3.1.0 remains unreleased.
