# N15-B2R naming inventory

Updated: 2026-08-28

Current certified base: `main` `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`.

B2R-A is closed. The next executable naming phase is **B2R-B**.

This document is the human-readable companion to `release/n15-b2r-a-naming-inventory.json`. `docs/NAMING.md` remains the naming policy. `docs/HANDOFF-V2.2.0.md` is the canonical continuation point.

## Mandatory synchronization rule

B2R cannot close if this file, the machine ledger and the canonical handoff disagree with live Git/PR/CI state.

## B2R-A1 — DONE

Internal module filenames were normalized to English:

| Previous | Canonical |
| --- | --- |
| `abntexto-ufc/fontes.def` | `abntexto-ufc/fonts.def` |
| `abntexto-ufc/modulos.def` | `abntexto-ufc/modules.def` |
| `abntexto-ufc/pretextuais.def` | `abntexto-ufc/frontmatter.def` |
| `abntexto-ufc/institucional.def` | `abntexto-ufc/institutional.def` |
| `abntexto-ufc/trabalhos.def` | `abntexto-ufc/academic-works.def` |
| `abntexto-ufc/projetos.def` | `abntexto-ufc/research-projects.def` |
| `abntexto-ufc/objetos.def` | `abntexto-ufc/objects.def` |
| `abntexto-ufc/bibliografia.def` | `abntexto-ufc/bibliography.def` |
| `abntexto-ufc/postextuais.def` | `abntexto-ufc/backmatter.def` |

PR #146 was squash-merged. Resulting `main` `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1` was certified by Source #367, preflight #1030, Gate T #1031 and Distribution #239.

A1 changed neither public API nor runtime behavior.

## B2R-A2 — DONE

A2 normalized only user-example and distribution-facing repository paths:

| Previous | Canonical |
| --- | --- |
| `documento.tex` | `main.tex` |
| `1-pre-textuais/` | `frontmatter/` |
| `2-textuais/` | `chapters/` |
| `3-pos-textuais/` | `backmatter/` |
| `figuras/` | `figures/` |
| `assets/institucional/` | `assets/institutional/` |
| `assets/institucional/brasao-ufc.PNG` | `assets/institutional/ufc-coat-of-arms.png` |

Repository, full-template bundle and Overleaf bundle share the canonical layout; Overleaf keeps `main.tex` at ZIP root. Portuguese academic leaf filenames remain intentionally retained.

A2 did not change public `\ufcsetup` semantics, article runtime, normative predicates/values/locators/authority, formatting intent or pagination intent.

### Frozen N12 boundary

`.github/workflows/latex-preflight.yml` remains byte-identical at:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

The historical N12 manifest/hashes remain unchanged. Only the two authorized current-to-historical path reconstructions in `tests/smoke/perfil-base.tex` remain in the machine ledger:

- `frontmatter/resumo` → `1-pre-textuais/resumo`;
- `frontmatter/abstract` → `1-pre-textuais/abstract`.

### Migration findings resolved

A2 reconciled bounded path consumers only: reference-map traces, profile fixtures, human currency markers, container Git `safe.directory`, the N12 historical bridge, CAPES guidance, generated/reference-image paths, compiled-guide examples, CTAN documentation/policy paths and the legacy-path scanner boundary case.

The final documentation-sync blocker also restored required A1/A2 compatibility fields in the machine ledger and final newlines in the Markdown ledgers instead of weakening the frozen N12 checker.

### Final certified merge candidate

Draft PR #147 could not be transitioned to ready through the automation connector. It was closed without merge and replaced by non-draft PR #148 over the exact same certified content SHA:

`22e9e4e872aca8aca16b143b249d62fe516c3359`

Exact-head certification before merge:

- Source Contract #408 — SUCCESS;
- Reference Preview #62 — SUCCESS;
- PR LaTeX preflight #1073 — SUCCESS;
- Gate T #1074 — SUCCESS, including Overleaf and Windows literal Times New Roman/Arial certification;
- Distribution #241 — SUCCESS;
- `behind_by=0`;
- frozen N12 blob preserved.

PR #148 was squash-merged and produced:

`main` `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`.

### Post-merge recertification

The resulting `main` passed:

- Source Contract #410 — SUCCESS;
- LaTeX preflight push #1076 — SUCCESS;
- Gate T #1077 — SUCCESS;
- Distribution #242 — SUCCESS;
- PDF Validator #136 — SUCCESS.

Therefore B2R-A2 is closed and no A2 implementation task remains.

## B2R-B — READY

B2R-B is the next executable phase. Its contract is additive: supported Portuguese public surfaces remain valid throughout v2.x while canonical project-owned English surfaces are introduced.

Required work:

1. create a machine-readable public API inventory before changing public names;
2. inventory at least class entrypoints, `\ufcsetup` keys, enumerated values, public commands, environments and upstream-owned surfaces;
3. record canonical English names and Portuguese compatibility aliases explicitly;
4. introduce canonical English setup keys and values without removing Portuguese forms;
5. preserve Portuguese commands/environments through wrappers or aliases where a canonical English project-owned equivalent is introduced;
6. add an executable public-API contract checker;
7. prove canonical-English/Portuguese semantic and rendered-output equivalence with paired fixtures;
8. reject accidental removals and unreviewed new project-owned public identifiers;
9. exact-head certify the completed phase before merge.

### Initial API surface to inventory

`abntexto-ufc/core.def` currently exposes a Portuguese-centric `\ufcsetup` interface. Existing public setup names include `tipo`, `impressao`, `capa`, `ficha-catalografica`, `brasao`, `fonte`, metadata names such as `autor`, `titulo`, `orientador` and profile values such as `tccgraduacao`, `tccespecializacao`, `dissertacao`, `tese`, `projeto` and `projetoanonimizado`.

The naming policy in `docs/NAMING.md` already reserves the corresponding canonical-English direction; B2R-B must formalize it in a machine-readable inventory and executable checks before or together with implementation.

## Next executable action

Create a fresh B2R-B branch from certified `main` `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`. First commit only the machine-readable public API inventory and its checker/contract scaffolding. Do not start scientific-article runtime until B2R-B has been merged and the resulting `main` re-certified.
