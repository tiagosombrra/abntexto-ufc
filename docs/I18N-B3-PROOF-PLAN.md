# P0.8 B3 — 11 list and contents public APIs

State: **preparation only**. This branch was created from main
\`12714f82e9616f9cd3c88ed5e305e7b65762f691\`, before B1's expected
protected merge. It must not be merged into main or used to claim new PASS
until B1 main certification is complete and B3 CI/evidence has been checked
against its own immutable source commit.

## Inventory and grouping

**Nine commands from integrated 7-profile PDFs**:
\`\ufcPrintListOfFigures\`, \`\ufcPrintListOfTables\`,
\`\ufcPrintListOfIllustrations\`, \`\ufcPrintListOfTextTables\`,
\`\ufcPrintListOfCharts\`, \`\ufcPrintListOfAbbreviationsAndAcronyms\`,
\`\ufcPrintListOfSymbols\`, \`\ufcPrintTableOfContents\`,
\`\ufcListEntry\`.

**Two commands from optional-module 3-profile PDFs**:
\`\ufcPrintListOfCodeListings\`, \`\ufcPrintListOfAlgorithms\`.

## Existing evidence and required probes

- \`tests/integration/frontmatter/i18n-b3-integrated-list-evidence.py\`:
  seven profile PDFs in each of PT, EN, ES, FR; preserve blank physical
  pages; ensure command appears once in applicable TeX source, correct
  localized list heading appears exactly once in a physical PDF page,
  entry is present **on that same list page**, and caption appears
  **on a later textual-body page**, never on a different pretextual list.
  Reject unexpected list in nonapplicable profiles. Verify the public
  \`\ufcListEntry\` term and definition on one body page. 21 negative
  source/heading/entry/body and duplication mutations.
- \`tests/integration/objects/i18n-b3-optional-list-evidence.py\`:
  three optional-module PDFs per locale, two list public APIs, 10 negative
  mutations, list and following body caption, exact original byte SHA256,
  original seven-API receipts and scoped profile-applicability.
- Exploratory preaudit against original B1 source
  \`e3f0ebcab9321aaa4c3341c9c79c1e11511d07ce\`:
  180 integrated plus 12 optional positive observable PDF predicates,
  across four languages. **Not B3 certification**: these PDFs belong to
  a prior source and preflight of the new B3 validators is not yet run
  in GitHub CI.

## Integration steps, mandatory order

1. Certify B1 PR #587 and verify its protected squash commit on main.
   B1's 47 bounded PASS / 25 PENDING must be present on main and the
   **five/six postmerge workflows must pass** on the exact merge SHA.
2. Reconcile B3 branch with new main, ideally create a fresh branch from
   certified main and copy **only** the two B3 scripts and this plan,
   avoiding a stale-base PR diff and needless workflow conflicts.
3. Add these scripts to the pre-existing integrated/optional matrix
   workflow triggers and steps; add full Linux/Release path triggers and
   \`tests/integration_suites.py\` classification. Never create hosted
   workflows prohibited by AGENTS.md.
4. Execute fail-closed preflights (21 + 10 mutants) and original real
   PDF jobs for four languages, inspect original ZIP artifacts outside
   the runner, require physical-page positions, original SHA and BCP47
   locale catalog. Fix regressions without weakening the predicates.
5. Promote only individually certified B3 IDs in the 72-ID ledger with
   new proof suites and exact source SHA, run/artifact IDs and negative
   counts, retaining global human normative/linguistic review PENDING.
6. Require Static, Canonical, Integrated Matrix, Optional Matrix, Linux
   Integration complete, and Linux Release/CTAN pkgcheck complete on
   **final B3 ledger HEAD**. Review SHA-bound, protected squash, and
   certify new main.

Potential main total after an independently certified B3: **58 PASS /
14 PENDING / 0 NA**. This is a mathematical target, not the current
state or a normative release certificate.

**Nonnegotiable:** no change to published v3.0.5 source/tags/assets,
\`v3.1.0 UNRELEASED\` and \`publication_authorized=false\`.
Human ABNT/UFC, visual typography/pagination and official translations
remain PENDING. Empty duplex pages observed in integrated PDFs need a
separate normative assessment, not implicit acceptance by this proof.
