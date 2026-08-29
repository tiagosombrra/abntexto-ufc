# N15-B2R naming inventory

Updated: 2026-08-29

B2R-A and B2R-B1 are closed. **B2R-B2 implementation is DONE and fully post-merge certified; only the bounded state-sync branch remains before B2R-B3 starts.**

Certified B2 implementation `main`:

`f6ba39bcbe50c324f6ab5f1856595cfcf7f8f0f9`

State-sync branch:

`docs/n15-b2r-b2-post-merge-sync`

Machine contracts:

- frozen B1 baseline: `release/n15-b2r-b-public-api.json`;
- B2 additive delta: `release/n15-b2r-b2-setup-aliases.json`;
- historical B2R-A/N12 evidence: `release/n15-b2r-a-naming-inventory.json`.

Frozen N12 workflow blob:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## B2R-A — DONE

B2R-A1 normalized internal package module filenames to English. B2R-A2 normalized repository/example/distribution engineering paths while preserving Portuguese academic leaf filenames where appropriate.

## B2R-B1 — DONE

PR #150 established the pre-migration public/exported API baseline and executable checker. PR #151 synchronized that result.

B1 baseline:

- 2 class entrypoints;
- 67 setup keys;
- 45 enumerated setup values scoped by `(setup key, value)`;
- 47 exported commands;
- 6 UFC environments;
- 2 explicit extension hooks.

Frozen B1 machine-ledger blob:

`c1f545e0e707822959db851a74d29f4068dff731`

Certified B2 starting point after PR #151:

`main` `1a3731575f9fe06a7f7d9a132f5152998edc6cee`

with Source #425, preflight/Gate T #1094 and Distribution #245 all SUCCESS.

## B2R-B2 — canonical English setup aliases — DONE IMPLEMENTATION

### Design rule

Canonical-English setup keys live in:

`abntexto-ufc/public-api.def`

The layer is loaded after existing runtime modules and forwards canonical input to certified Portuguese behavior. Existing Portuguese setup keys/values remain supported throughout v2.x.

No command/environment alias and no article runtime were introduced in B2.

### Final inventory counts

- legacy setup keys: 67;
- canonical setup keys added: 65;
- total setup keys: 132;
- legacy enumerated values: 45;
- canonical enumerated values added: 34;
- total enumerated `(key,value)` identities: 79;
- exported commands: 47, unchanged;
- environments: 6, unchanged;
- extension hooks: 2, unchanged;
- article runtime: false.

`volume` is already an English identifier and remains canonical as-is. The project-specific coat-of-arms compatibility key remains compatibility-only.

### Canonical setup-key map

Core/profile and presentation:

| Compatibility key | Canonical key |
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
| `volume` | `volume` |
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
| `brasao-arquivo` | `coat-of-arms-file` |
| `pagina-inicial` | `initial-page` |

Committee pattern:

- `banca-N` → `examiner-N`;
- `banca-N-unidade` → `examiner-N-unit`;
- `banca-N-ies` → `examiner-N-institution`;
- supported `N`: 2 through 6.

Optional modules:

| Compatibility key | Canonical key |
| --- | --- |
| `fonte` | `font` |
| `fonte-estrita` | `strict-font` |
| `tabelas` | `tables` |
| `codigo` | `code` |
| `algoritmos` | `algorithms` |
| `glossario` | `glossary` |
| `indice` | `index` |

### Canonical setup values

Profiles:

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`.

Other choices:

- `print-mode`: `single-sided`, `double-sided`;
- `cover`: `auto`, `true`, `false`;
- `catalog-card`: `true`, `false`;
- `coat-of-arms`: `true`, `false`;
- advisor/coadvisor feminine-label switches: `true`, `false`;
- `font`: `times`, `arial`;
- `strict-font`: `true`, `false`;
- `tables`: `native`, `tabularray`;
- `code`: `none`, `listings`, `minted`;
- `algorithms`: `none`, `algpseudocodex`;
- `glossary`: `none`, `glossaries`;
- `index`: `none`, `imakeidx`.

Package identifiers remain unchanged where they identify exact external integrations.

### Semantic decisions

Detailed academic metadata was named by runtime role rather than literal translation. In particular:

- graduate-program, program, degree-field and concentration remain distinct;
- `project-nature-statement` denotes the complete nature statement override;
- feminine-label flags describe grammatical output behavior;
- committee metadata is represented as examiner/member data.

No B2 setup-key or setup-value entry remains unresolved.

### Executable evidence

`tests/checks/public_api_contract.py` validates the frozen B1 ledger plus B2 delta and rejects B1 drift, supported legacy removals, missing/unreviewed canonical setup additions, incomplete mappings, new command/environment/hook surfaces, live article values and frozen N12 workflow drift.

`tests/normativa/public-api-aliases.tex` plus `tests/v2-public-api-alias-check.sh` exercise all 65 canonical setup keys and assert forwarding into certified legacy state.

Exact PR-head certification on `2fd3bc28cc37e6c05f4e37f0b0315adb99765573`:

- Source #426 — SUCCESS, run `33247218637`;
- preflight #1096 — SUCCESS, run `33247218623`;
- `N15-EVIDENCE b2r-b2-alias-smoke keys=65 status=PASS`;
- public-API totals: 132 keys, 79 scoped values, 47 commands, 6 environments, 2 hooks;
- article runtime false;
- `behind_by=0` before merge.

PR #152 was squash-merged with exact-head protection and produced:

`main` `f6ba39bcbe50c324f6ab5f1856595cfcf7f8f0f9`.

Post-merge certification:

- Source #427 — SUCCESS, run `33247641697`;
- preflight/Gate T #1097 — SUCCESS, run `33247641696`;
- Distribution #246 — SUCCESS, run `33247641702`;
- reference/PDF-A, profiles/PDF-A, objects/bibliography, post-textuals and structure — SUCCESS;
- Overleaf stable proxy — SUCCESS;
- Windows literal Times New Roman/Arial build and identity/Unicode/embedding/PDF-A certification — SUCCESS;
- release PDF/A, deterministic bundles, Overleaf import proxy, candidate upload and aggregate distribution-preflight — SUCCESS.

## Article boundary

`type=article` and its Portuguese compatibility form remain reserved-only. Scientific-article runtime belongs to N15-B2B only after B2R-B3 and B2R-B4 close and the resulting `main` is re-certified.

## B2 bounded state-sync rule

This state-sync branch records B2 closure only. After it is exact-head certified, merged and its resulting `main` is certified once, no further receipt-only state-sync PR is allowed. B3 begins from that certified `main`.

## B2R-B3 next scope

B3 must first classify all 47 exported commands and 6 UFC environments. Canonical wrappers are added only for surfaces that are genuinely supported project API. Portuguese compatibility remains additive. Upstream compatibility surfaces and extension hooks are not renamed for stylistic consistency.

Known reviewed command directions from B1 include cover, title page, approval page, catalog card, references and bibliography-resource surfaces. Summary/abstract naming requires explicit language-role validation before implementation.

Full paired Portuguese/English semantic and rendered-output equivalence remains B2R-B4 scope.
