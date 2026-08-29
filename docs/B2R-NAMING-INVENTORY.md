# N15-B2R naming inventory

Updated: 2026-08-29

B2R-A is closed. B2R-B1 is closed and re-certified. **B2R-B2 is ACTIVE on `refactor/n15-b2r-b2-setup-aliases`.**

Certified B2R-B2 base:

`main` `1a3731575f9fe06a7f7d9a132f5152998edc6cee`

This document is the human companion to two machine contracts:

- frozen B1 baseline: `release/n15-b2r-b-public-api.json`;
- active B2 delta: `release/n15-b2r-b2-setup-aliases.json`.

`release/n15-b2r-a-naming-inventory.json` remains historical B2R-A/N12-sensitive evidence.

The frozen N12 workflow remains byte-identical at blob:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## B2R-A — DONE

B2R-A1 normalized internal package module filenames to English. B2R-A2 normalized repository/example/distribution engineering paths while intentionally preserving Portuguese academic leaf filenames where appropriate.

## B2R-B1 — DONE

PR #150 established the pre-migration public/exported API baseline and executable checker. PR #151 synchronized that result and produced the certified base used by B2.

B1 baseline counts:

- 2 class entrypoints;
- 67 setup keys;
- 45 enumerated setup values scoped by `(setup key, value)`;
- 47 exported commands;
- 6 UFC environments;
- 2 explicit extension hooks.

The B1 machine ledger is frozen during B2 at blob:

`c1f545e0e707822959db851a74d29f4068dff731`

Post-#151 certification of `main` `1a373157...`:

- Source #425 — SUCCESS;
- preflight/Gate T #1094 — SUCCESS;
- Distribution #245 — SUCCESS;
- Overleaf and Windows literal-font certification — SUCCESS.

## B2R-B2 — canonical English setup aliases — ACTIVE

### Design rule

Canonical-English setup keys live in one project-owned layer:

`abntexto-ufc/public-api.def`

The layer is loaded after the existing runtime modules and forwards canonical input to certified Portuguese behavior. Existing Portuguese setup keys/values remain supported throughout v2.x.

No command or environment alias is introduced in B2; those surfaces remain B3 scope.

### Inventory counts

After B2 additions:

- legacy setup keys: 67;
- canonical setup keys added: 65;
- total setup keys: 132;
- legacy enumerated values: 45;
- canonical enumerated values added: 34;
- total enumerated `(key,value)` identities: 79;
- exported commands: 47, unchanged;
- environments: 6, unchanged;
- extension hooks: 2, unchanged.

`volume` is already an English identifier and remains canonical as-is. The project-specific coat-of-arms compatibility key remains compatibility-only and maps to the existing coat-of-arms behavior.

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

Committee members use the systematic pattern:

- `banca-N` → `examiner-N`;
- `banca-N-unidade` → `examiner-N-unit`;
- `banca-N-ies` → `examiner-N-institution`;
- current supported `N` values are 2 through 6.

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

Other choice values:

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

Package identifiers remain unchanged when they are already the exact package/runtime name.

### Semantic naming decisions

The detailed academic metadata was reviewed semantically rather than translated token-by-token:

- graduate-program, program, degree-field and concentration remain distinct concepts;
- `project-nature-statement` denotes the complete override text used in the project nature block;
- feminine-label flags describe grammatical output behavior rather than personal attributes;
- committee metadata is represented as examiner/member data, not as a literal translation of the Portuguese collection noun.

The active B2 delta has no unresolved setup-key or setup-value naming entries.

### Executable contract and smoke evidence

`tests/checks/public_api_contract.py` validates the frozen B1 ledger plus the B2 delta and rejects:

- any B1 ledger drift;
- supported legacy removals;
- missing or unreviewed canonical setup additions;
- incomplete legacy-to-canonical mappings;
- new commands/environments/hooks during B2;
- live article values;
- frozen N12 workflow drift.

`tests/normativa/public-api-aliases.tex` exercises all 65 canonical setup keys. `tests/v2-public-api-alias-check.sh` compiles the fixture and requires assertions that canonical input reaches the corresponding certified legacy state.

Full paired Portuguese/English rendered-output equivalence is intentionally B2R-B4 scope.

## Article boundary

`type=article` and its Portuguese compatibility form remain reserved-only surfaces. They are not accepted live in B2. Scientific-article runtime belongs to N15-B2B after all B2R-B phases close and `main` is re-certified.

## B2 closure sequence

1. complete implementation, executable evidence and documentation synchronization;
2. inspect branch versus certified base and require `behind_by=0`;
3. open the B2 PR;
4. stop mutating the final PR head;
5. obtain exact-head Source and LaTeX preflight SUCCESS;
6. squash-merge with head protection;
7. re-certify resulting `main` through Source, Gate T/preflight and Distribution;
8. synchronize final receipts if necessary without creating an unbounded receipt loop;
9. begin B2R-B3 only from that certified `main`.
