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
  \`\ufcListEntry\` term and definition on one body page. 24 negative
  source/heading/entry/body and duplication mutations.
- \`tests/integration/objects/i18n-b3-optional-list-evidence.py\`:
  three optional-module PDFs per locale, two list public APIs, 14 negative
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
4. Execute fail-closed preflights (24 + 14 mutants) and original real
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


### Independent PDF catalog and BCP47 audit

Each B3 verifier executes `qpdf --json=2 --json-key=qpdf` on the **actual compiled PDF** and checks the root catalog reference, `/Type`, Unicode `/Lang`, BCP47 locale and original manifest receipt. Two new wrong-locale mutations per suite yield **24 integrated plus 14 optional fail-closed controls, 38 total**. These are executable candidate checks, **not yet passed in hosted CI**, and do not authorize B3 ledger promotion.


### Unicidade de legendas (evidência exploratória)

A auditoria local dos ZIPs originais do lote anterior confirmou **120 observações de legendas integradas** e **12 observações de legendas opcionais**, todas com exatamente uma ocorrência no corpo físico do documento. Os dois verificadores B3 agora exigem cardinalidade igual a um e incluem mutantes que duplicam a legenda depois do corpo (um controle no integrado e dois controles no opcional). Isso é um refinamento preliminar, não uma execução do CI B3 nem uma homologação normativa.


## 2026-11-12 — B1 integrated; B3 branch reconciled to main

PR #587 was squash merged into `main@9a2348e6fba9517f735ad64ad818ceb54ee52f59` after all six exact-head workflows passed. The main ledger now contains **47 bounded PASS / 25 PENDING / 0 NA**, `global_acceptance=PENDING`, `publication_authorized=false`, and an unchanged runtime class blob. Independent **postmerge** Linux, Release, integrated PDF, optional PDF and static/canonical workflows were started; certification of that exact main is still required before B3 may proceed to an active PR/merge.

A clean B3 branch `test/489-p08-b3-list-pdf-evidence` was created directly from that merged main SHA and contains both eleven-ID scripts, fail-closed 24 integrated + 14 optional mutation guards, actual PDF qpdf /Root/Lang BCP47 checks, unique body captions, and physical page/SHA256 predicates. The existing four-locale integrated and optional workflows and Linux Release path triggers were updated, as was the complete regression selector and the source crosswalk. **No B3 ledger promotion, formal CI pass, human acceptance or publication is claimed.**

The earlier preparatory branch is superseded for integration; it must not be merged because its base predates PR #587. Once postmerge main certification is green, open **one** B3 PR as draft, record real CI results, inspect original ZIPs and only then promote individually proven B3 commands with exact evidence SHA and artifact IDs (target 58/72 bounded, not guaranteed).
