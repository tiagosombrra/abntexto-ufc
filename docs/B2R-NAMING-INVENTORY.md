# N15-B2R naming inventory

Updated: 2026-08-28

Current certified base: `main` `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`.

This document is the human-readable companion to `release/n15-b2r-a-naming-inventory.json`. `docs/NAMING.md` remains the naming policy.

## Certified starting point

B2R-A1 is closed and post-merge certified on `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`:

- Source Contract #367 — SUCCESS;
- LaTeX preflight push #1030 — SUCCESS;
- exact Gate T / workflow_dispatch #1031 — SUCCESS;
- Distribution #239 — SUCCESS.

Distribution #239 passed release preflight, PDF/A-2b, deterministic bundles, Overleaf import proxy and candidate upload. No new PDF Validator/Pages run was expected because A1 did not modify validator or normative surfaces.

## B2R decomposition

B2R is split so naming changes remain separable from public API and article behavior.

### B2R-A1 — DONE

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

PR #146 was squash-merged and the resulting `main` was fully re-certified before A2 began.

### B2R-A2 — IMPLEMENTATION CANDIDATE

A2 normalizes only the user-example and distribution-facing repository layout. It does not change `\ufcsetup`, public commands, normative predicates or article runtime.

Approved and implemented moves:

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

The institutional coat of arms remains source-only. Public class/template/Overleaf/CTAN bundles continue to exclude it, with release validation using the binary hash rather than trusting only its filename.

A2 deliberately retains Portuguese leaf filenames that describe academic content, such as `frontmatter/resumo.tex`, `backmatter/apendices/` and `backmatter/anexos/`. Test fixtures and normative/evidence identifiers are also outside this rename scope.

### A2 synchronized consumers

The implementation synchronizes:

- `Makefile` default entrypoint;
- `main.tex` content references;
- reference images and example listings;
- institutional asset default path;
- reference-image downloader;
- coordinated validation runner;
- reference, corpus, PDF validator and PDF/A checks;
- Overleaf stable proxy and import-bundle contract;
- deterministic release builder and release-package contract;
- distribution-source validation;
- reference preview, reference audit and distribution workflows;
- README and B2R handoff/ledger documentation.

`tests/v2-distribution-check.sh` additionally rejects reintroduction of legacy A2 top-level paths and scans active tracked text for stale references. Migration ledgers/policy and historical records are exempt because they must preserve the previous names explicitly.

### Frozen N12 boundary

`.github/workflows/latex-preflight.yml` is not modified in A2. Its certified blob must remain:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

Compatibility is preserved by updating the scripts invoked by that frozen workflow so their default reference artifact is `main.pdf`.

### A2 closure requirements

A2 is not DONE until the exact PR head proves:

- `main.tex` is the canonical root entrypoint;
- old top-level user paths are absent;
- active consumers contain no stale A2 paths;
- template and Overleaf bundles expose the canonical layout;
- the UFC institutional mark remains excluded from public bundles;
- reference image hashes remain unchanged;
- repository/distribution audits pass;
- reference and corpus regressions pass;
- twelve-profile matrix and PDF/A remain green;
- Overleaf import/stable proxies remain green;
- required Windows literal-font certification remains green;
- N12 workflow remains byte-identical;
- the branch is `behind_by=0` immediately before merge.

After squash merge, the resulting `main` must be re-certified before B2R-B begins.

### B2R-B — BLOCKED BY A2

B2R-B will introduce canonical English project-owned public API surfaces only after A2 is merged and re-certified. Existing supported Portuguese public surfaces remain compatibility aliases throughout v2.x.
