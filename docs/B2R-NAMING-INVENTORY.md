# N15-B2R naming inventory

Updated: 2026-08-29

B2R-A, B2R-B1 and B2R-B2 are closed. **B2R-B3 is ACTIVE on `refactor/n15-b2r-b3-command-environment-aliases`.**

Certified B3 base:

`main` `cb0df822401a926c4c5987f904b29f5898fb1775`

Machine contracts:

- frozen B1 baseline: `release/n15-b2r-b-public-api.json`;
- frozen B2 setup delta: `release/n15-b2r-b2-setup-aliases.json`;
- active B3 command/environment delta: `release/n15-b2r-b3-command-environment-aliases.json`;
- historical B2R-A/N12 evidence: `release/n15-b2r-a-naming-inventory.json`.

Frozen blobs:

- B1: `c1f545e0e707822959db851a74d29f4068dff731`;
- B2: `19df208fb59af5ea37556d962e5986a43094c7f5`;
- N12 workflow: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## B2R-B2 — DONE

B2 established the canonical setup vocabulary without removing Portuguese compatibility:

- 67 legacy setup keys;
- 65 canonical setup keys;
- 132 setup keys total;
- 45 legacy scoped values;
- 34 canonical scoped values;
- 79 scoped values total;
- 47 commands;
- 6 environments;
- 2 hooks.

PR #152 implemented B2; PR #153 was its bounded state sync. Final certified B2 base `cb0df822...` passed:

- Source #429 — SUCCESS, run `33249228729`;
- preflight/Gate T #1100 — SUCCESS, run `33249228669`;
- Distribution #247 — SUCCESS, run `33249228670`;
- Overleaf and Windows literal-font certification — SUCCESS.

## B2R-B3 — command and environment aliases — ACTIVE

### Scope rule

B3 is additive and changes only canonical command/environment naming. It must not change:

- the 132 setup keys;
- the 79 scoped setup values;
- the 2 extension hooks;
- normative/runtime behavior;
- article runtime;
- the frozen N12 workflow.

All new wrappers live in `abntexto-ufc/public-api.def` and forward to certified v2.x behavior.

### Command disposition

The 47 B1 commands have complete disposition coverage:

- 7 already-canonical project commands are retained;
- 9 exported English helpers are retained;
- upstream `\keywords` is retained as upstream compatibility API;
- 25 Portuguese compatibility commands receive English wrappers;
- 5 project public commands still using Portuguese/lowercase names receive English wrappers.

B3 adds 30 commands, for 77 total.

### Canonical command map

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

### Semantic command decisions

- `\ufcPrintAbstract` remains the B1-approved wrapper for the English-language `\imprimirabstract` behavior.
- `\ufcPrintSummary` wraps `\imprimirresumo`; summary and abstract are deliberately distinct.
- `\ufcSummaryKeywords` wraps Portuguese `Palavras-chave`; upstream `\keywords` remains unchanged for the English label.
- `\ufcPrintEpigraph` uses canonical option values `short` / `long`, forwarding to legacy `curta` / `longa`.
- `\ufcPrintListOfTextTables` is the English engineering name for the distinct UFC/ABNT `quadro` list; it must not collapse into statistical tables or charts.
- Optional listing/minted commands remain conditional on their corresponding module surface.

### Retained commands

Already-canonical project API:

- `\ufcsetup`, `\ufcDocumentType`, `\ufcPrintMode`, `\ufcMeta`;
- `\ufcIfProjectTF`, `\ufcIfAnonymizedProjectTF`, `\ufcMathFontPolicy`.

Exported helpers retained without cosmetic aliases:

- `\ufcPrimarySectionBreak`, `\ufcPretextualBreak`, `\ufcRegisterUncountedPhysicalPage`;
- `\ufcstarttoc`, `\ufcPretextualHeading`, `\ufcPosttextualHeading`;
- `\ufcSetupGlossaryModule`, `\ufcIndexHeading`, `\ufcSetupIndexModule`.

Upstream English API `\keywords` is retained as-is.

### Environment map

| Compatibility/current environment | Canonical environment |
| --- | --- |
| `ufcalineas` | `ufclettereditems` |
| `ufcsubalineas` | `ufcdashedsubitems` |
| `ufclistadefinicoes` | `ufcdefinitionlist` |
| `ufcobjeto` | `ufcobject` |
| `ufcalgoritmo` | `ufcalgorithm` |

`ufclisting` is already English and remains canonical as-is.

B3 adds 5 environments, for 11 total.

Signatures are preserved:

- `ufclettereditems`: no arguments;
- `ufcdashedsubitems`: no arguments;
- `ufcdefinitionlist`: optional width, default `3cm`;
- `ufcobject`: optional placement, default `\placepos`;
- `ufcalgorithm`: optional placement + line-number frequency, defaults `\placepos` and `1`;
- `ufclisting`: optional placement, remains conditional on `code=listings`.

### Executable contract

`tests/checks/public_api_contract.py` now treats B1+B2+B3 as layered contracts. B3 additionally requires:

- frozen B1/B2 blobs;
- 30 unique canonical command additions;
- complete migration-source coverage;
- preservation of all B1-approved command mappings;
- reviewed command signatures;
- 5 canonical environment additions plus retained `ufclisting`;
- 77 total commands, 11 total environments and 2 hooks;
- setup totals still exactly 132/79;
- article runtime disabled;
- N12 workflow blob unchanged.

Smoke evidence:

- `tests/normativa/public-api-command-environment-aliases.tex`;
- `tests/v2-public-api-command-environment-check.sh`.

The smoke verifies canonical command/environment existence, exercises lettered/dashed/definition-list wrappers, activates `listings` and `algpseudocodex`, verifies the corresponding conditional aliases and confirms that the minted alias is not live under `code=listings`.

## Article boundary

`type=article` and its Portuguese compatibility form remain reserved-only. Scientific-article runtime starts only after B2R-B3 and B2R-B4 close and their resulting `main` is re-certified.

## B3 closure sequence

1. finish documentation and machine-ledger synchronization;
2. inspect branch against certified `cb0df822...` and require `behind_by=0`;
3. open PR and freeze final head;
4. obtain exact-head Source + LaTeX preflight SUCCESS;
5. squash-merge with expected-head protection;
6. re-certify resulting main through Source, full Gate T/preflight and Distribution;
7. use at most one bounded receipt sync if required;
8. start B2R-B4 from the resulting certified main.
