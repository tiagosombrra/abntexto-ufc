# N15-B2R naming inventory

Updated: 2026-08-29

B2R-A, B2R-B1, B2R-B2, B2R-B3 and B2R-B4 are closed. **The canonical-English/public-compatibility migration is fully DONE and re-certified on `main` `ce659b578b4fc9cc929af4aadc3e613df469ba77`.**

The bounded B4 post-merge state sync closed in PR #156. N15-B2B scientific-article runtime is now ACTIVE on `feat/n15-b2b-scientific-article-runtime`, created from that exact certified `main`.

## Machine contracts

- frozen B1 baseline: `release/n15-b2r-b-public-api.json`;
- frozen B2 setup delta: `release/n15-b2r-b2-setup-aliases.json`;
- frozen B3 command/environment delta: `release/n15-b2r-b3-command-environment-aliases.json`;
- completed B4 equivalence contract: `release/n15-b2r-b4-en-pt-equivalence.json`;
- historical B2R-A/N12 evidence: `release/n15-b2r-a-naming-inventory.json`.

Frozen identities used by B4 and preserved by B2B:

- B1: `c1f545e0e707822959db851a74d29f4068dff731`;
- B2: `19df208fb59af5ea37556d962e5986a43094c7f5`;
- B3: `bfcbf8aca3fba3fd602f62895f10fa2d6277b5a4`;
- public-API runtime: `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- N12 workflow: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## Final B2R public inventory

- setup keys: 67 compatibility + 65 canonical additions = **132**;
- scoped setup values: 45 compatibility + 34 canonical additions = **79**;
- commands: 47 prior + 30 canonical additions = **77**;
- UFC environments: 6 prior + 5 canonical additions = **11**;
- extension hooks: **2**.

Portuguese v2.x surfaces remain supported. N15-B2B activates the previously reserved `type=article` / `tipo=artigo` pair in the isolated `articles.def` runtime module without rewriting the frozen B2R public-alias layer.

## Setup naming — B2 DONE

Canonical `\ufcsetup` keys use semantic English kebab-case while preserving compatibility keys. Representative mappings include:

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
| `programa-doutorado` | `doctoral-graduate-program` |
| `nome-doutorado` | `doctoral-program` |
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

Canonical B2R profile values are `undergraduate-capstone`, `specialization-capstone`, `masters-thesis`, `doctoral-thesis`, `research-project` and `anonymized-research-project`. Canonical print values are `single-sided` and `double-sided`; boolean-style choices use `true`/`false`.

The full B2R key/value map remains frozen in the B2 machine contract. The scientific-article pair is a later N15-B2B runtime delta, not a rewrite of B2 evidence.

## Command naming — B3 DONE

B3 added 30 canonical commands while preserving all 47 prior commands. Important mappings include:

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
| `\imprimirreferencias` | `\ufcPrintReferences` |
| `\imprimirresumo` | `\ufcPrintSummary` |
| `\imprimirsumario` | `\ufcPrintTableOfContents` |
| `\palavraschave` | `\ufcSummaryKeywords` |
| `\ufcbibliografia` | `\ufcAddBibliographyResource` |
| `\ufcfonte` | `\ufcSource` |
| `\ufcnota` | `\ufcNote` |

Semantic decisions remain frozen:

- `\ufcPrintSummary` and `\ufcPrintAbstract` are distinct language-role surfaces;
- `\ufcPrintEpigraph[short|long]` forwards to compatibility `[curta|longa]`;
- `\ufcPrintListOfTextTables` preserves the distinct `quadro` object family;
- optional listing/minted aliases remain conditional on their certified module surfaces;
- upstream `\keywords` remains upstream API.

## Environment naming — B3 DONE

| Compatibility/current environment | Canonical environment |
| --- | --- |
| `ufcalineas` | `ufclettereditems` |
| `ufcsubalineas` | `ufcdashedsubitems` |
| `ufclistadefinicoes` | `ufcdefinitionlist` |
| `ufcobjeto` | `ufcobject` |
| `ufcalgoritmo` | `ufcalgorithm` |

`ufclisting` is already English and remains canonical as-is.

## B2R-B4 — semantic/output equivalence — DONE

B4 made no API/runtime/normative/workflow change. It certified the completed canonical-English vocabulary against the supported Portuguese compatibility vocabulary.

Static evidence validated:

- all 65 distinct canonical setup-key mappings plus retained `volume`;
- all 45 reviewed compatibility setup-value source identities;
- all 30 canonical command wrappers;
- all 5 canonical environment wrappers;
- exact B1/B2/B3 contract blobs;
- exact public-runtime and N12 workflow blobs;
- unchanged public counts: 132/79/77/11/2.

Paired runtime evidence required and passed:

- exact normalized internal-state equality;
- exact extracted layout-text equality;
- equal page count and dimensions;
- equal TOC/list/bibliography artifacts;
- equal per-page raster SHA-256;
- PDF/A-2b declaration for both outputs.

Final paired evidence: 66 state lines, 23 pages, raster equality on all 23 pages, all state/text/geometry/auxiliary/raster/PDF-A predicates true, `PASS=16 FAIL=0 SKIP=0`.

### B4 exact-head certification

PR #155 exact head:

`44c9c5082598b82e67a0b3ef009c4bb71a584571`

- `behind_by=0`;
- Source #442 — SUCCESS, run `33262519263`;
- preflight #1115 — SUCCESS, run `33262519254`.

Resulting `main` after protected squash merge:

`a4f2660ef46826c7d61a7dc3d9de6554f6d6a825`

Post-merge certification:

- Source #443 — SUCCESS, run `33263191118`;
- preflight push #1116 — SUCCESS, run `33263191096`;
- Gate T #1117 — SUCCESS, run `33263196260`;
- Distribution #249 — SUCCESS, run `33263191120`.

### B4 state-sync closure

PR #156 closed the bounded documentation transition. Its exact head `1a4b5feb5517dd820d010613b24d2fffd346d6e5` passed Source #444 (`33265851911`) and preflight #1118 (`33265851907`) with `behind_by=0`, then squash-merged to:

`main` `ce659b578b4fc9cc929af4aadc3e613df469ba77`

That exact resulting `main` was re-certified by:

- Source #445 — SUCCESS, run `33266313000`;
- preflight/Gate T #1119 — SUCCESS, run `33266312999`;
- Distribution #250 — SUCCESS, run `33266313007`;
- Overleaf stable proxy — SUCCESS;
- Windows literal Times New Roman/Arial build/certification — SUCCESS;
- reference/profile PDF/A-2b, objects/bibliography, post-textuals, structure and deterministic distribution — SUCCESS;
- GitHub Release — correctly skipped because no tag exists.

## Article boundary — N15-B2B ACTIVE

B2R no longer blocks article support. B2B starts from certified `main` `ce659b57...` and uses canonical engineering naming `articles.def` plus `type=article`, with additive Portuguese `tipo=artigo` compatibility.

B2B is intentionally a later layered delta. It must not rewrite the frozen B2R ledgers or `public-api.def`, must not change the established 132/79/77/11/2 B2R baseline accounting, and must not regress thesis/dissertation/project profiles. Runtime evidence and B2B certification are tracked separately in `release/n15-b2b-article-runtime.json`; proof-state closure remains N15-B2C.
