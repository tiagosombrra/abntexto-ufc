# N15-B2R naming inventory

Updated: 2026-08-28

Current certified base: `main` `3a7d5e55d0bbd8df279e3e3f6eecb72b98af709b`.

Current active branch: `refactor/n15-b2r-b-public-api`.

B2R-A is closed. B2R-B is active, with **B2R-B1 technically certified on PR #150 and awaiting final exact-head CI before merge**.

This document is the human-readable companion to the active B2R-B machine ledger `release/n15-b2r-b-public-api.json`. `release/n15-b2r-a-naming-inventory.json` remains the historical B2R-A/N12-sensitive ledger and must not be repurposed. `docs/NAMING.md` remains the naming policy. `docs/HANDOFF-V2.2.0.md` is the canonical continuation point.

## Mandatory synchronization rule

B2R cannot close if this file, the active machine ledger, the naming policy and the canonical handoff disagree with live Git/PR/CI state.

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

PR #146 was squash-merged. Resulting `main` `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1` was certified by Source #367, preflight #1030, Gate T #1031 and Distribution #239. A1 changed neither public API nor runtime behavior.

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

### Frozen N12 boundary

`.github/workflows/latex-preflight.yml` remains byte-identical at:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

The historical N12 manifest/hashes remain unchanged. The B2R-A ledger retains the approved historical-path reconstruction fields required by `tests/checks/normative_n12_matrix.py`.

### A2 certified closure

The final A2 merge candidate `22e9e4e872aca8aca16b143b249d62fe516c3359` passed Source #408, Reference Preview #62, PR preflight #1073, Gate T #1074 and Distribution #241. PR #148 was squash-merged and produced `main` `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`, which then passed Source #410, preflight #1076, Gate T #1077, Distribution #242 and PDF Validator #136.

The subsequent A2 documentation-sync closure advanced `main` to `3a7d5e55d0bbd8df279e3e3f6eecb72b98af709b`, which is the certified base used by B2R-B.

## B2R-B1 — PUBLIC API BASELINE/CHECKER

Status: **TECHNICALLY CERTIFIED ON PR #150; FINAL EXACT-HEAD CI PENDING**.

B1 intentionally contains no canonical-English runtime aliases. Its purpose is to freeze and classify the existing API/export surface before any additive migration.

### Baseline inventory

The machine ledger records:

- 2 class entrypoints;
- 67 `\ufcsetup` keys;
- 45 enumerated setup values scoped by `(setup key, value)`;
- 47 exported commands;
- 6 UFC environments;
- 2 explicit extension hooks: `\ufcsectionhook` and `\ufcobjectlegendhook`;
- upstream compatibility overrides separately from UFC-owned project API;
- `type=article` / `tipo=artigo` as reserved future surfaces only, with runtime still blocked until N15-B2B.

The `(setup key, value)` identity is deliberate. Repeated values such as `true`, `false`, `sim` and `nao` are not globally unique API identities.

### Checker contract

`tests/checks/public_api_contract.py` verifies the ledger against the implementation and fails on:

- missing baseline keys/values/commands/environments/hooks;
- duplicate inventory identities;
- supported-surface removal;
- unreviewed new project-owned public identifiers;
- drift of the frozen N12 workflow blob.

`tests/run.py` now includes `public-api` as a dependency of `repository`, so the checker is exercised by the existing frozen workflow without editing `.github/workflows/latex-preflight.yml`.

### CI-discovered blockers

Initial head `d3f55442e22eced43784089c24b5423f092123f2` demonstrated that the new checker itself was correct: preflight #1081 logged `public-api PASS` with `keys=67 values=45 commands=47 environments=6 hooks=2` and `article_runtime=false`.

The same run failed only in `distribution-source`, where the older canonical-identity scanner had not yet classified the two structured ledger fields required to document the deprecated legacy compatibility entrypoint.

Head `1438d85e22a787ce7ab92bcd7abd06e259afa05d` corrected that boundary narrowly: only those exact two structured inventory lines are permitted. The ledger as a whole is not exempt, and any additional unclassified legacy identity still fails.

The first documentation-sync head `f722620d1baaaac3cedb66f3e2b58e21bc564f88` passed Source Contract #418 and all substantive LaTeX/normative checks in preflight #1086. Its sole failure was `distribution-source`, because the human documentation repeated the deprecated identity narratively. The correction keeps the legacy identity confined to the two structured inventory fields instead of broadening scanner exemptions.

### Technical certification receipts

Head `1438d85e22a787ce7ab92bcd7abd06e259afa05d` passed:

- Normative Source Contract #414 — SUCCESS;
- LaTeX preflight #1082 — SUCCESS;
- structure job — SUCCESS;
- reference document and reference PDF/A-2b — SUCCESS;
- complete 12-profile matrix and profile PDF/A-2b — SUCCESS;
- objects/bibliography — SUCCESS;
- post-textuals — SUCCESS.

No public API behavior, scientific-article runtime, normative contract, formatting intent or pagination intent changed in B1.

## B2R-B2 — NEXT AFTER B1 MERGE/RECERTIFICATION

B2R-B2 introduces canonical-English setup keys/values additively while preserving every supported Portuguese v2.x surface.

Already-reviewed key direction includes:

- `tipo` → `type`;
- `impressao` → `print-mode`;
- `capa` → `cover`;
- `ficha-catalografica` → `catalog-card`;
- `brasao` → `coat-of-arms`;
- `fonte` → `font`;
- `fonte-estrita` → `strict-font`;
- `tabelas` → `tables`;
- `codigo` → `code`;
- `algoritmos` → `algorithms`;
- `glossario` → `glossary`;
- `indice` → `index`;
- `autor` → `author`;
- `titulo` → `title`;
- `subtitulo` → `subtitle`;
- `data-aprovacao` → `approval-date`;
- `orientador` → `advisor`;
- `coorientador` → `coadvisor`.

Reviewed profile values are:

- `tccgraduacao` → `undergraduate-capstone`;
- `tccespecializacao` → `specialization-capstone`;
- `dissertacao` → `masters-thesis`;
- `tese` → `doctoral-thesis`;
- `projeto` → `research-project`;
- `projetoanonimizado` → `anonymized-research-project`.

Canonical booleans use `true` / `false`; existing `sim` / `nao` remain compatibility forms.

### Review-required boundary

Do not mechanically translate unresolved surfaces. `print-mode` values, detailed academic metadata (`programa-*`, `nome-*`, `titulo-*`, `area-*`, committee/member fields), optional-module values, remaining commands and UFC environments require semantic review before becoming canonical names.

In particular, `programa-mestrado`, `nome-mestrado`, `titulo-mestre` and `area-mestrado` represent distinct academic functions, as do the corresponding doctoral/project fields. Translation must preserve those semantics rather than apply word substitution.

## Next executable action

1. Require Source Contract and LaTeX preflight to pass on the corrected final exact head.
2. Confirm PR #150 mergeability and `behind_by=0`.
3. Squash-merge PR #150 with exact-head protection.
4. Re-certify resulting `main`.
5. Begin B2R-B2 from that re-certified `main`.

Do not start scientific-article runtime until all B2R-B subphases close and the resulting `main` is re-certified.
