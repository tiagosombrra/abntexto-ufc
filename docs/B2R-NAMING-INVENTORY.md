# N15-B2R naming inventory

Updated: 2026-08-28

Current certified base: `main` `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`.

Active branch: `refactor/n15-b2r-a2-user-layout`.  
Active PR: #147 (draft).

This document is the human-readable companion to `release/n15-b2r-a-naming-inventory.json`. `docs/NAMING.md` remains the naming policy. `docs/HANDOFF-V2.2.0.md` is the canonical project continuation point.

## Mandatory synchronization rule

B2R cannot be closed if this file, the release ledger and the canonical handoff disagree with the live branch/PR/CI state. Update them after material scope decisions, newly discovered CI blockers, blocker fixes, merge/certification events and before handing the project to another conversation.

## B2R-A1 — DONE

Internal package modules were normalized to canonical English paths:

| Previous path | Canonical path |
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

Retained canonical paths are `core.def`, `layout.def`, `compat-abntexto.def` and `compat-nbr6023-2025.def`. Module order is unchanged; `academic-works.def` loads before `research-projects.def`.

PR #146 was squash-merged. Certified resulting `main` `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`:

- Source Contract #367 — SUCCESS;
- LaTeX preflight push #1030 — SUCCESS;
- exact Gate T #1031 — SUCCESS;
- Distribution #239 — SUCCESS.

## B2R-A2 — IMPLEMENTATION CANDIDATE

A2 normalizes only the user-example and distribution-facing repository layout. It does not change `\ufcsetup`, public command semantics, article runtime, or normative predicates/values/locators.

### Approved and implemented moves

| Previous path | Canonical path |
| --- | --- |
| `documento.tex` | `main.tex` |
| `1-pre-textuais/` | `frontmatter/` |
| `2-textuais/` | `chapters/` |
| `3-pos-textuais/` | `backmatter/` |
| `figuras/` | `figures/` |
| `assets/institucional/` | `assets/institutional/` |
| `assets/institucional/brasao-ufc.PNG` | `assets/institutional/ufc-coat-of-arms.png` |

Repository, complete template bundle and Overleaf bundle intentionally share the same canonical content layout. The Overleaf archive keeps `main.tex` at archive root.

A2 deliberately retains Portuguese leaf filenames that describe academic content, for example `frontmatter/resumo.tex`, `backmatter/apendices/` and `backmatter/anexos/`. Test/evidence fixture names and historical normative identifiers are outside the rename scope unless a direct path consumer must be updated.

### Synchronized consumers

The implementation synchronizes:

- `Makefile` default entrypoint;
- `main.tex` content and bibliography references;
- example image/listing/license paths;
- institutional source-only asset path;
- reference-image downloader;
- validation runner;
- reference, corpus, PDF validator and PDF/A checks;
- Overleaf stable proxy and import-bundle contract;
- deterministic release builder and release-package contract;
- distribution-source validation;
- reference preview, reference validation and distribution workflows;
- `tests/smoke/perfil-base.tex`;
- `normativa/reference-guide-map.json` secondary guide-trace source paths;
- README, handoff, naming and normative human documentation.

`tests/v2-distribution-check.sh` rejects reintroduction of legacy A2 top-level paths and scans active tracked text for stale path references. Explicit migration/history ledgers remain allowed to mention old names.

### Secondary trace-map clarification

`normativa/reference-guide-map.json` lives under `normativa/` but is a secondary documentation/rastreability map. Its declared purpose is to connect the commented reference guide to existing normative sources/rules without creating new requirements, and its policy remains `normative_contract_changed=false`.

A2 changed only its `source_file` paths from `2-textuais/...` to `chapters/...`. No source authority, predicate, value, rule ID or normative locator was changed.

### Frozen N12 boundary

`.github/workflows/latex-preflight.yml` is not modified in A2. Required blob:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

Compatibility is preserved by updating the scripts invoked by that workflow so their default reference artifact is `main.pdf`.

### Exact-head CI cycles

First cycle, PR head `1f80043139ae9fabe68c554c264ef7d8c5087cd8`:

- Source Contract #368 — SUCCESS;
- Reference Preview #22 built complete `main.tex` successfully before later PDF/A/proxy steps;
- LaTeX preflight #1032 found two path-only regressions.

Repairs:

1. `normativa/reference-guide-map.json` source-file traces migrated to `chapters/...`;
2. `tests/smoke/perfil-base.tex` summary/abstract paths migrated to `frontmatter/...`.

Second documented cycle, PR head `8b1a0a8013c10cc73ad43115b25d0beca567e529`:

- Source Contract #376 — FAILED only at the human-documentation assertion in `normative_currency.py`;
- catalog, precedence, source audit, source-reference integrity and locator audit had already passed;
- cause: the rewritten `docs/VIGENCIA-NORMATIVA.md` conveyed the supersessions semantically but abbreviated old references as `NBR ...`, while the checker requires exact full strings such as `ABNT NBR 14724:2011` and `ABNT NBR 14724:2024` plus exact CEPE markers.

Repair:

3. `docs/VIGENCIA-NORMATIVA.md` now explicitly lists every full superseded/current ABNT pair from `normativa/version-policy.json`, keeps `ABNT NBR 6022:2018`, the current 2022/corrected-2023 article-guide state, and exact CEPE titles. Repair commit before this documentation sync: `5539e5370447fd97e844dfbadf4663992ab0e176`.

These failures are preserved as migration evidence. They did not require changing normative predicates, values, locators or authority.

### A2 closure requirements

A2 is not DONE until one exact PR head proves all of the following:

- Source Contract green;
- reference build, corpus and PDF/A green;
- twelve-profile matrix and profile PDF/A green;
- structure, objects/bibliography and post-textual regressions green;
- Overleaf stable/import proxy green;
- required Windows literal-font certification green under Gate T;
- deterministic distribution preflight green;
- N12 workflow byte-identical;
- no active stale A2 paths;
- UFC institutional mark remains excluded from public bundles;
- reference-image hashes/licensing unchanged;
- PR `behind_by=0` immediately before merge;
- `HANDOFF`, this inventory, release ledger, README and normative/naming human documentation are synchronized as applicable.

After squash merge, the resulting `main` must be re-certified before B2R-B begins.

## B2R-B — BLOCKED BY A2

Only after A2 merge + post-merge recertification:

- create a machine-readable public API inventory;
- introduce canonical English project-owned public API surfaces;
- retain supported Portuguese keys/values/commands/environments as compatibility aliases throughout v2.x;
- prove canonical-English/Portuguese compatibility semantics and output;
- prevent new unreviewed engineering identifiers from bypassing the naming policy.
