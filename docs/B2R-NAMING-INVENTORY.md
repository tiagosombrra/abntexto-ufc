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
- `tests/v2-capes-guidance-check.sh`;
- `tests/v2-distribution-check.sh`, including container-safe Git access and boundary-aware legacy-path detection;
- `tests/checks/normative_n12_matrix.py` bounded A2 historical-content bridge;
- `.gitignore` generated/reference-image paths;
- the compiled guide's explicit layout/path examples;
- `docs/README-CTAN.md` canonical institutional-asset compatibility path;
- `tests/v2-ctan-policy-check.py` canonical binary policy paths;
- README, handoff, naming and normative human documentation.

`tests/v2-distribution-check.sh` rejects reintroduction of legacy A2 top-level paths and scans active tracked text for stale path references. Explicit migration/history ledgers remain allowed to mention old names. The scanner uses token boundaries so a path such as `figuras/` is not falsely inferred from identifiers such as `imprimirlistadefiguras/before`.

### Secondary trace-map clarification

`normativa/reference-guide-map.json` lives under `normativa/` but is a secondary documentation/rastreability map. Its declared purpose is to connect the commented reference guide to existing normative sources/rules without creating new requirements, and its policy remains `normative_contract_changed=false`.

A2 changed only its `source_file` paths from `2-textuais/...` to `chapters/...`. No source authority, predicate, value, rule ID or normative locator was changed.

### Frozen N12 boundary

`.github/workflows/latex-preflight.yml` is not modified in A2. Required blob:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

The N12 matrix manifest and certified historical hashes also remain unchanged. A1 reconstructs historical `\ProvidesFile` identities for renamed modules. A2 reconstructs only the two path strings changed inside `tests/smoke/perfil-base.tex` — `frontmatter/resumo` → `1-pre-textuais/resumo` and `frontmatter/abstract` → `1-pre-textuais/abstract` — before computing the historical blob. Any other content drift remains a failure.

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

3. `docs/VIGENCIA-NORMATIVA.md` explicitly lists every full superseded/current ABNT pair from `normativa/version-policy.json`, keeps `ABNT NBR 6022:2018`, the current 2022/corrected-2023 article-guide state, and exact CEPE titles. Repair commit before documentation sync: `5539e5370447fd97e844dfbadf4663992ab0e176`.

Third cycle, PR head `a0bf9d060a188aa963d7e7f7002a538ef3dee2e0`:

- Source Contract #380 — SUCCESS;
- Reference Preview #34 — SUCCESS, including reference PDF/A and public TeX Live 2025 proxy;
- LaTeX preflight #1044 confirmed reference document + PDF/A SUCCESS, twelve-profile build + twelve-profile PDF/A SUCCESS and post-textual SUCCESS;
- the structure job failed on three migration consumers, while the substantive layout/font/geometry/math/project/build-path/multivolume/catalog-card checks shown after those failures continued to pass.

Repairs:

4. distribution-source scan now invokes `git -c safe.directory=<repo> ls-files -z`, avoiding the Git dubious-ownership failure inside the TeX Live container without changing the frozen workflow;
5. `tests/checks/normative_n12_matrix.py` now uses the machine-ledger-controlled reverse-content bridge for exactly the two profile-fixture paths changed by A2; the N12 manifest, certified hashes and frozen workflow remain unchanged;
6. `tests/v2-capes-guidance-check.sh` now reads `frontmatter/agradecimentos.tex` instead of the removed `1-pre-textuais/agradecimentos.tex`.

Fourth cycle, PR head `3fcd7a6d8cf09567c9e6c79448b8a3f0dbf3899c`:

- Source Contract #387 — SUCCESS;
- Reference Preview #41 — SUCCESS, including PDF/A and TeX Live 2025 compatibility proxy;
- LaTeX preflight #1051: profile matrix 12/12 + 12 PDF/A SUCCESS, reference + PDF/A SUCCESS, post-textual SUCCESS, objects/bibliography SUCCESS;
- `structure` reached `PASS=13 FAIL=1`: the only failure was the active stale-path scanner under `distribution-source`;
- the three repairs from #1044 were independently confirmed: `normative-complement` PASS with the bounded N12 content-rewrite bridge, and `pretextual` PASS including CAPES guidance.

The scanner reported nine files. Classification and repair:

7. `.gitignore` contained real old generated/reference-image paths and now uses `main.pdf` and `figures/...`;
8. the compiled reference-guide chapters still contained five explicit old example paths; those human-facing examples now use `main.tex`, `frontmatter/...` and `backmatter/referencias.bib`;
9. `docs/README-CTAN.md` now documents the canonical `assets/institutional/ufc-coat-of-arms.png` compatibility path;
10. `tests/v2-ctan-policy-check.py` now classifies the same binary blobs under their canonical A2 paths, with hashes unchanged;
11. `abntexto-ufc/layout.def` was a false positive only: the raw substring `figuras/` appeared inside `imprimirlistadefiguras/before`. The scanner was made boundary-aware rather than exempting `layout.def`, so genuine legacy paths still fail while unrelated identifiers do not.

The historical failed runs remain migration evidence. None required changing normative predicates, values, locators, source authority, public API, article runtime or formatting behavior.

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
