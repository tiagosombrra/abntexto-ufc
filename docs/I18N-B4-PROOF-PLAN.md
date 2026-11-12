# P0.8 — B4 / 14 remaining internationalization API identifiers

## Preparation only — no PR and no ledger promotion

Base is the currently merged B1 \`main@9a2348e6fba9517f735ad64ad818ceb54ee52f59\`.
B3 PR #588 is under exact-head CI validation, targeting **58/72 bounded PASS**.
This branch exists only to preserve B4 scientific test design while B3's
post-ready checks and protected merge remain pending. Its base must be
reconciled with the eventually certified B3 main before opening **one B4 PR**.

## Exact fourteen-ID inventory

**Eleven IDs in original seven-profile/four-language integrated PDFs**
(source generator \`tests/integration/frontmatter/generate-integrated-locale.py\`):

- \`\ufcSource\` — source label and attributable content beside the actual
  object/caption; reject a label detached from the object or translated
  author-supplied data.
- \`\ufcNote\` — note label and supplied text adjacent to the object.
- \`\ufcAddBibliographyResource\` — two distinct real BibTeX/Biber resources,
  exact source command count, Biber exit/manifest receipts and entries from
  both sources in the PDF; reject omission of either resource and forged
  bibliography-only source presence.
- \`\ufcPrintReferences\` — unique localized references heading and distinct
  visible bibliographic entries after the textual body.
- \`\ufcPrintGlossary\` — one populated, localized glossary in doctoral thesis
  only, appearing on its own **physical** PDF page after references.
- \`\ufcPrintIndex\` — one populated, localized index in doctoral thesis only,
  following annexes; correct physical PDF page.
- \`\legend\` (retained upstream) — custom figure, chart, quadro captions with
  supplied text and matching object/section context, not merely a token in
  a list of illustrations.
- \`\appendix\` / \`\annex\` (retained upstream) — distinct localized headings
  and source-provided chapter bodies on the proper physical pages after
  bibliography; absent from scientific article fixture.
- \`\pretextual\` (retained upstream) — academic/project front matter ordered
  before \`\textual\`; scientific article has an explicit nonapplicable route.
- \`\textual\` (retained upstream) — body section visible and correctly ordered
  before references across all seven document profiles.

**One ID in original optional module PDFs:**

- \`\ufcInputMinted\` — actual imported Python source token in source and PDF,
  minted engine activation, list caption and source attribution. Verify
  \`latexminted\` genuine execution/compiled minted PDF; reject missing import
  and missing code marker, compare original 7-API receipts.

**Two IDs requiring genuinely new isolated evidence:**

- \`\ufcInputListing\` — present in
  \`tests/documents/advanced-objects.tex\`, but the four-locale original
  optional suite does **not** invoke it. Build 4 separately compiled
  locale-specific real PDFs with same fixed \`tests/fixtures/example.cpp\`,
  assert exact input source, embedded C++ code and related caption/source,
  and test disabled/missing input.
- \`\keywords\` (retained upstream) — exercised in
  \`tests/integration/frontmatter/summary-legacy-context.sh\` (historical
  English/legacy cases), but **not** in the 7-profile/four-locale integrated
  manuscripts. Require a dedicated original PDF source/legacy summary
  matrix with independently checked language and author-supplied keyword
  preservation before any all-four-locale bounded PASS.

## Proof and governance controls

1. Reuse original 7 × 4 integrated PDFs and 3 × 4 optional PDFs only where
   the relevant exact source invokes the public API. Preserve duplex blank
   leaves, verify original file hashes, PDF /Root/Lang BCP47 and visible
   *same-page* relation of supplied data to generated labels.
2. Compile isolated new PDFs for the two unexercised APIs. Include negative
   examples and distinguish deliberate ClassErrors from test errors.
3. Audit the original GitHub Actions ZIPs independently, including SHA
   binding to the source commit and per-ID positive and negative receipts.
4. Promote **only individually proven B4 identifiers** into the canonical
   72-ID ledger, never automatically due to shared workflows or source
   token usage. If one of the fourteen fails, keep it PENDING and report
   the actual total rather than claiming global completion.
5. Run six complete workflow gates in existing CI for the **exact final
   ledger HEAD**, technical SHA-bound review, protected squash, then six
   postmerge main gates. Do not create new hosted workflows in violation
   of AGENTS.md.
6. Functional PASS is **not** human UFC/ABNT normative/visual acceptance,
   not an official translation approval and not release authorization.
   The fully published v3.0.5 source, tag and assets remain immutable;
   v3.1.0 stays \`UNRELEASED/publication_authorized=false\`.

**Possible eventual total:** 72/72 bounded functional proofs if and only if
all fourteen B4 IDs independently pass. This is a scientific test target,
**not** the present repository state.


## 2026-11-12 — Implemented preparatory executables (NOT YET CI-CERTIFIED)

Three executable source-bound Python validators now exist **only on this
preparatory branch**, without modifying the existing class, workflows or
ledger:

1. \`tests/integration/frontmatter/i18n-b4-integrated-backmatter-evidence.py\`
   (11 IDs): reuses four-locale/seven-profile source/PDF manifest records,
   exact SHA256, biber receipt, original PDF catalog BCP47 and physical page
   boundaries; requires matching visible object source and note, source and
   bibliography entries from both bibliographic resources, unique localized
   references/glossary/index headings, populated doctoral glossary/index,
   caption text, and appendix/annex/body ordering. \`--preflight\` contains
   15 initial lexical/PDF-heading controls; more real mutation guards may
   be added after the first test iteration.
2. \`tests/integration/objects/i18n-b4-inputminted-evidence.py\` (one ID):
   reuses the 3 × 4 optional-module PDFs plus original seven-API receipts
   and checks actual imported Python source, compiled syntax-highlighted
   content, minted processor execution, list and textual body physical
   pages, source attribution, original SHA256 and /Root/Lang; 9 candidate
   negative controls.
3. \`tests/integration/frontmatter/i18n-b4-isolated-public-api-evidence.py\`
   (two IDs): compiles one **new real InputListing** PDF and one **new real
   legacy keywords-in-localized-summary** PDF per locale, preserving
   original source and full PDF bytes, BCP47 catalog and real language/
   code markers. Includes 18 preflight source/PDF mutations and generated
   manifest. Isolated negative compilation and legacy PT/EN baseline must
   be verified in later CI before either ID can be classified PASS.

All three scripts must be **audited and run in CI** after B3 development
squash and six exact-SHA postmerge gates, and integrated into existing
four-locale workflows only. No new hosted workflows, no branch merge yet,
no premature 72/72 PASS. If an isolated fixture fails, correct the
*actual evidence* without weakening its technical predicates, and retain
any unproved ID as PENDING. Human ABNT/UFC and linguistic acceptance
remain separate from this functional evidence.
