# Migrating to abntexto-ufc v3

abntexto-ufc v3 is a breaking API release. The v2 Portuguese project API is not retained as a runtime compatibility layer. Existing documents must be migrated to the canonical v3 English project API before they are compiled with v3.

This guide is derived from `release/v3-api-migration.json`, which remains the machine-readable authority for the migration contract. Portuguese academic content rendered in the document is not being anglicized. Genuine dependency-owned APIs are also not renamed merely for consistency.

## Migration rules

1. Use `abntexto-ufc` as the only class entry point.
2. Replace v2 project-owned setup keys, setup values, commands, environments, extension hooks and object identifiers with the v3 names below.
3. Do not add local Portuguese↔English compatibility wrappers. v3 intentionally has no runtime alias layer.
4. Keep normal Portuguese document content, headings and metadata values in Portuguese when appropriate.
5. Keep dependency-owned commands such as `\legend`, `\keywords`, `\appendix`, `\annex`, `\pretextual` and `\textual` when required by the upstream integration.
6. `grafico` and `quadro` may still appear only where required by the upstream ABNTexto/tabularray boundary. They are not canonical abntexto-ufc v3 object identifiers.

## Class entry point

| v2 | v3 |
| --- | --- |
| `ufctex` | `abntexto-ufc` |

## Setup keys

| v2 key | v3 key |
| --- | --- |
| `tipo` | `type` |
| `impressao` | `print-mode` |
| `capa` | `cover` |
| `ficha-catalografica` | `catalog-card` |
| `brasao` | `coat-of-arms` |
| `ies` | `institution` |
| `sigla` | `institution-acronym` |
| `centro` | `center` |
| `departamento` | `department` |
| `curso-graduacao` | `undergraduate-program` |
| `habilitacao` | `undergraduate-degree` |
| `curso-especializacao` | `specialization-program` |
| `programa-mestrado` | `masters-graduate-program` |
| `nome-mestrado` | `masters-program` |
| `titulo-mestre` | `masters-degree-field` |
| `area-mestrado` | `masters-concentration` |
| `programa-doutorado` | `doctoral-graduate-program` |
| `nome-doutorado` | `doctoral-program` |
| `titulo-doutor` | `doctoral-degree-field` |
| `area-doutorado` | `doctoral-concentration` |
| `programa-projeto` | `project-program` |
| `tipo-projeto` | `project-type` |
| `entidade-submissao` | `submission-entity` |
| `natureza-projeto` | `project-nature-statement` |
| `identificador-projeto` | `project-identifier` |
| `autor` | `author` |
| `titulo` | `title` |
| `subtitulo` | `subtitle` |
| `variacao-titulo` | `title-variant` |
| `ano` | `year` |
| `local` | `location` |
| `data-aprovacao` | `approval-date` |
| `orientador` | `advisor` |
| `orientador-ies` | `advisor-institution` |
| `orientador-unidade` | `advisor-unit` |
| `orientador-feminino` | `advisor-feminine-label` |
| `coorientador` | `coadvisor` |
| `coorientador-ies` | `coadvisor-institution` |
| `coorientador-unidade` | `coadvisor-unit` |
| `coorientador-feminino` | `coadvisor-feminine-label` |
| `autor-epigrafe` | `epigraph-author` |
| `banca-2` | `examiner-2` |
| `banca-2-unidade` | `examiner-2-unit` |
| `banca-2-ies` | `examiner-2-institution` |
| `banca-3` | `examiner-3` |
| `banca-3-unidade` | `examiner-3-unit` |
| `banca-3-ies` | `examiner-3-institution` |
| `banca-4` | `examiner-4` |
| `banca-4-unidade` | `examiner-4-unit` |
| `banca-4-ies` | `examiner-4-institution` |
| `banca-5` | `examiner-5` |
| `banca-5-unidade` | `examiner-5-unit` |
| `banca-5-ies` | `examiner-5-institution` |
| `banca-6` | `examiner-6` |
| `banca-6-unidade` | `examiner-6-unit` |
| `banca-6-ies` | `examiner-6-institution` |
| `fonte` | `font` |
| `fonte-estrita` | `strict-font` |
| `tabelas` | `tables` |
| `codigo` | `code` |
| `algoritmos` | `algorithms` |
| `glossario` | `glossary` |
| `indice` | `index` |
| `brasao-arquivo` | `coat-of-arms-file` |
| `pagina-inicial` | `initial-page` |

`volume` is already the canonical spelling and therefore needs no rename.

## Setup values

| v2 value | v3 value |
| --- | --- |
| `tccgraduacao` | `undergraduate-capstone` |
| `tccespecializacao` | `specialization-capstone` |
| `dissertacao` | `masters-thesis` |
| `tese` | `doctoral-thesis` |
| `projeto` | `research-project` |
| `projetoanonimizado` | `anonymized-research-project` |
| `anverso` | `single-sided` |
| `frente-verso` | `double-sided` |
| `sim` | `true` |
| `nao` | `false` |
| `nativo` | `native` |
| `nenhum` | `none` |
| `curta` | `short` |
| `longa` | `long` |

The canonical module values also include `tabularray`, `listings`, `minted`, `algpseudocodex`, `glossaries` and `imakeidx` where applicable.

## Public commands

| v2 command | v3 command |
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

The canonical v3 setup entry point remains `\ufcsetup`. Public state/query helpers retained by v3 include `\ufcDocumentType`, `\ufcPrintMode`, `\ufcMeta`, `\ufcIfProjectTF`, `\ufcIfAnonymizedProjectTF` and `\ufcMathFontPolicy`.

## Public environments

| v2 environment | v3 environment |
| --- | --- |
| `ufcalineas` | `ufclettereditems` |
| `ufcsubalineas` | `ufcdashedsubitems` |
| `ufclistadefinicoes` | `ufcdefinitionlist` |
| `ufcobjeto` | `ufcobject` |
| `ufcalgoritmo` | `ufcalgorithm` |

`ufclisting` is already canonical and remains unchanged.

## Extension hooks

| v2 hook | v3 hook |
| --- | --- |
| `\ufcsectionhook` | `\ufcSectionHook` |
| `\ufcobjectlegendhook` | `\ufcObjectLegendHook` |

## Object identifiers

| v2 project-owned identifier | v3 identifier |
| --- | --- |
| `codigo` | `code` |
| `algoritmo` | `algorithm` |

The rendered labels may still be “Código” and “Algoritmo”. Do not blindly replace document labels such as `cod:...` or `alg:...`; those are author payload, not project API identifiers.

## Internal helpers removed from the public surface

The following v2/v3-transition helpers are implementation details in v3 and must not be called by user documents: `\ufcPrimarySectionBreak`, `\ufcPretextualBreak`, `\ufcRegisterUncountedPhysicalPage`, `\ufcstarttoc`, `\ufcPretextualHeading`, `\ufcPosttextualHeading`, `\ufcSetupGlossaryModule`, `\ufcIndexHeading` and `\ufcSetupIndexModule`.

Use semantic public commands such as `\ufcPrintReferences`, `\ufcPrintGlossary` and `\ufcPrintIndex` instead of reaching into layout/back-matter plumbing.

## Minimal v3 setup example

```tex
\documentclass{abntexto-ufc}

\ufcsetup{
  type = doctoral-thesis,
  print-mode = single-sided,
  coat-of-arms = true,
  author = {Nome da Pessoa Autora},
  title = {Título do trabalho},
  location = {Fortaleza},
  year = {2026},
  font = times,
  strict-font = false
}
```

## Verification after migration

After migrating a project:

1. search the project for the old names listed above;
2. compile using only the `abntexto-ufc` class;
3. do not recreate aliases for removed names;
4. if contributing to this repository, run `make static-check` and `make check`.

The repository's static contract includes a fail-closed v3 API residual check. It rejects removed project-owned API identifiers in active runtime/template/test sources and rejects any reintroduction of the forwarding-only `public-api.def` layer.
