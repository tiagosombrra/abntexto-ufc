# N15-B2R naming inventory

Updated: 2026-08-29

B2R-A, B2R-B1, B2R-B2 and B2R-B3 are closed. **B2R-B4 is ACTIVE on `refactor/n15-b2r-b4-en-pt-equivalence`.**

Certified B4 base:

`main` `92f17418dfeee4d2d45456912af9f8c399457cc1`

Machine contracts:

- frozen B1 baseline: `release/n15-b2r-b-public-api.json`;
- frozen B2 setup delta: `release/n15-b2r-b2-setup-aliases.json`;
- frozen B3 command/environment delta: `release/n15-b2r-b3-command-environment-aliases.json`;
- active B4 equivalence contract: `release/n15-b2r-b4-en-pt-equivalence.json`;
- historical B2R-A/N12 evidence: `release/n15-b2r-a-naming-inventory.json`.

Frozen blobs used by B4:

- B1: `c1f545e0e707822959db851a74d29f4068dff731`;
- B2: `19df208fb59af5ea37556d962e5986a43094c7f5`;
- B3: `bfcbf8aca3fba3fd602f62895f10fa2d6277b5a4`;
- public-API runtime: `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- N12 workflow: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## Final naming inventory after B3

B2 established the complete canonical setup vocabulary and B3 completed command/environment naming without removing compatibility surfaces.

Live public inventory:

- setup keys: 67 legacy + 65 canonical additions = **132**;
- scoped setup values: 45 legacy + 34 canonical additions = **79**;
- commands: 47 prior + 30 canonical additions = **77**;
- UFC environments: 6 prior + 5 canonical additions = **11**;
- extension hooks: **2**.

Portuguese v2.x surfaces remain supported. `type=article` and its compatibility form remain reserved-only until N15-B2B.

## Setup naming — B2 DONE

Canonical setup keys use semantic English kebab-case. `volume` is already canonical and remains unchanged; the project-specific coat-of-arms legacy synonym remains compatibility-only.

Representative mappings include:

| Compatibility key | Canonical key |
| --- | --- |
| `tipo` | `type` |
| `impressao` | `print-mode` |
| `capa` | `cover` |
| `ficha-catalografica` | `catalog-card` |
| `brasao` | `coat-of-arms` |
| `ies` | `institution` |
| `curso-graduacao` | `undergraduate-program` |
| `programa-mestrado` | `masters-graduate-program` |
| `nome-mestrado` | `masters-program` |
| `titulo-mestre` | `masters-degree-field` |
| `area-mestrado` | `masters-concentration` |
| `programa-doutorado` | `doctoral-graduate-program` |
| `nome-doutorado` | `doctoral-program` |
| `titulo-doutor` | `doctoral-degree-field` |
| `area-doutorado` | `doctoral-concentration` |
| `autor` | `author` |
| `titulo` | `title` |
| `orientador` | `advisor` |
| `coorientador` | `coadvisor` |
| `fonte` | `font` |
| `tabelas` | `tables` |
| `codigo` | `code` |
| `algoritmos` | `algorithms` |
| `glossario` | `glossary` |
| `indice` | `index` |

Canonical profile values are `undergraduate-capstone`, `specialization-capstone`, `masters-thesis`, `doctoral-thesis`, `research-project` and `anonymized-research-project`. Canonical print values are `single-sided` and `double-sided`; boolean-style choices use `true`/`false`; module selectors retain external package names where applicable.

The full key/value map is frozen in the B2 machine contract rather than duplicated here.

## Command naming — B3 DONE

B3 adds 30 canonical commands while preserving all 47 prior commands.

| Compatibility/current command | Canonical command |
| --- | --- |
| `\imprimirabstract` | `\ufcPrintAbstract` |
| `\imprimiragradecimentos` | `\ufcPrintAcknowledgments` |
| `\imprimircapa` | `\ufcPrintCover` |
| `\imprimirdedicatoria` | `\ufcPrintDedication` |
| `\imprimirepigrafe` | `\ufcPrintEpigraph` |
| `\imprimirerrata` | `\ufcPrintErrata` |
| `\imprimirfichacatalografica` | `\ufcPrintCatalogCard` |
| `\imprimirfolhadeaprovacao` | `\ufcPrintApprovalPage` |
| `\imprimirfolhaderosto` | `\ufcPrintTitlePage` |
| `\imprimirglossario` | `\ufcPrintGlossary` |
| `\imprimirindice` | `\ufcPrintIndex` |
| `\imprimirlistadeabreviaturasesiglas` | `\ufcPrintListOfAbbreviationsAndAcronyms` |
| `\imprimirlistadealgoritmos` | `\ufcPrintListOfAlgorithms` |
| `\imprimirlistadecodigos` | `\ufcPrintListOfCodeListings` |
| `\imprimirlistadefiguras` | `\ufcPrintListOfFigures` |
| `\imprimirlistadegraficos` | `\ufcPrintListOfCharts` |
| `\imprimirlistadeilustracoes` | `\ufcPrintListOfIllustrations` |
| `\imprimirlistadequadros` | `\ufcPrintListOfTextTables` |
| `\imprimirlistadesimbolos` | `\ufcPrintListOfSymbols` |
| `\imprimirlistadetabelas` | `\ufcPrintListOfTables` |
| `\imprimirreferencias` | `\ufcPrintReferences` |
| `\imprimirresumo` | `\ufcPrintSummary` |
| `\imprimirsumario` | `\ufcPrintTableOfContents` |
| `\palavraschave` | `\ufcSummaryKeywords` |
| `\ufcbibliografia` | `\ufcAddBibliographyResource` |
| `\ufcfonte` | `\ufcSource` |
| `\ufcinputlisting` | `\ufcInputListing` |
| `\ufcinputminted` | `\ufcInputMinted` |
| `\ufclistaentrada` | `\ufcListEntry` |
| `\ufcnota` | `\ufcNote` |

Semantic decisions:

- `\ufcPrintSummary` and `\ufcPrintAbstract` remain separate language-role surfaces;
- `\ufcSummaryKeywords` preserves the Portuguese summary keyword label while upstream `\keywords` remains the English-label upstream API;
- `\ufcPrintEpigraph[short|long]` forwards to `[curta|longa]`;
- `\ufcPrintListOfTextTables` preserves the distinct `quadro` object family;
- optional listing/minted aliases remain conditional on their selected code module.

Retained project API/helpers remain unchanged rather than receiving cosmetic synonyms.

## Environment naming — B3 DONE

| Compatibility/current environment | Canonical environment |
| --- | --- |
| `ufcalineas` | `ufclettereditems` |
| `ufcsubalineas` | `ufcdashedsubitems` |
| `ufclistadefinicoes` | `ufcdefinitionlist` |
| `ufcobjeto` | `ufcobject` |
| `ufcalgoritmo` | `ufcalgorithm` |

`ufclisting` is already English and remains canonical as-is.

The wrappers preserve the certified signatures: no arguments for the two list levels, optional `3cm` definition width, optional `\placepos` object placement, and optional algorithm placement/line-number frequency.

## B3 certification — DONE

PR #154 exact head:

`0630d19cb6ba3274d0e2e1a738343f8c74afe148`

Exact-head evidence:

- `behind_by=0`;
- Source #432 — SUCCESS, run `33252829652`;
- preflight #1104 — SUCCESS, run `33252829650`.

Resulting certified B4 base:

`92f17418dfeee4d2d45456912af9f8c399457cc1`

Post-merge evidence:

- Source #433 — SUCCESS, run `33253212796`;
- preflight push #1105 — SUCCESS, run `33253212823`;
- Gate T #1106 — SUCCESS, run `33253216564`;
- Distribution #248 — SUCCESS, run `33253212813`;
- Overleaf stable proxy — SUCCESS;
- Windows literal Times New Roman/Arial build/certification — SUCCESS;
- reference/profile PDF/A-2b and deterministic distribution — SUCCESS.

No B3 receipt-only state-sync PR is required.

## B2R-B4 — semantic/output equivalence — ACTIVE

B4 is not another naming phase. It certifies that the completed English canonical vocabulary is behaviorally equivalent to the supported Portuguese compatibility vocabulary.

Scope authority:

- no public API additions/removals;
- no runtime or normative behavior changes;
- no N12 workflow edits;
- no article runtime;
- `abntexto-ufc/public-api.def` remains frozen at blob `7b61fe70dd85ed895140f846272e097e3ded72cf`.

Static B4 evidence validates:

- all 65 distinct canonical setup-key mappings plus retained `volume`;
- all 45 reviewed legacy setup-value source identities forwarding through canonical choices;
- all 30 canonical command wrappers;
- all 5 canonical environment wrappers;
- exact B1/B2/B3 contract blobs;
- exact runtime and N12 blobs.

Paired runtime evidence compiles the same document through Portuguese and canonical-English surfaces and requires:

- exact normalized internal-state equality;
- exact extracted layout text equality;
- equal page count and dimensions;
- equal TOC/list/bibliography artifacts when generated;
- per-page raster SHA-256 equality;
- PDF/A-2b declarations for both outputs.

Evidence files:

- `tests/checks/public_api_equivalence_contract.py`;
- `tests/normativa/public-api-equivalence.tex`;
- `tests/fixtures/public-api-equivalence-summary.tex`;
- `tests/v2-public-api-equivalence-check.sh`.

`tests/run.py` makes `repository` depend on `public-api-equivalence`, so the existing frozen preflight workflow automatically exercises B4.

## Article boundary

Scientific-article runtime remains **BLOCKED**. N15-B2B starts only after B4 PR exact-head certification, merge, and full resulting-main re-certification through Source, Gate T and Distribution.
