# N15-B2R naming inventory

Updated: 2026-08-28

Base: certified `main` `7699ed205d4554df28fc46908fff3be0b92a38f7`.

This document is the human-readable companion to `release/n15-b2r-a-naming-inventory.json`. It records the migration boundary before repository names are changed. `docs/NAMING.md` remains the naming policy.

## Certified starting point

N15-B2A is closed on the base commit above with the following post-merge receipts:

- Source Contract #361 — SUCCESS;
- PDF Validator #135 — SUCCESS;
- LaTeX preflight push #1022 — SUCCESS;
- exact Gate T / LaTeX preflight #1023 — SUCCESS;
- Distribution #238 — SUCCESS.

Distribution #238 also passed release preflight, release PDF/A-2b validation, deterministic bundles, the Overleaf import proxy and candidate upload. GitHub Release publication was skipped as expected because this was a `main` push without a release tag.

## B2R decomposition

B2R is deliberately split so that naming changes do not obscure behavioral changes.

### B2R-A1 — internal package module paths

This is the first mutation scope. It is behavior-preserving and does not change the public API.

| Current path | Canonical path |
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

Retained canonical paths:

- `abntexto-ufc/core.def`;
- `abntexto-ufc/layout.def`;
- `abntexto-ufc/compat-abntexto.def`;
- `abntexto-ufc/compat-nbr6023-2025.def`.

Every module rename must preserve its contents and behavior while synchronizing:

1. the path loaded by `abntexto-ufc.cls`;
2. the module's `\ProvidesFile` identity;
3. ordering checks in `tests/v2-repository-audit.py`;
4. any direct path consumer found by the final reference scan.

The relative load order must remain unchanged. In particular, `academic-works.def` must load before `research-projects.def`.

### Known dynamic consumers

The following surfaces do not require a hard-coded nine-file allowlist migration:

- `tests/v2-canonical-identity-check.py` derives module paths from `abntexto-ufc.cls` and checks the matching `\ProvidesFile` identity;
- `tests/v2-ctan-archive-check.py` derives the CTAN module manifest from the class inputs;
- `tools/build-release-bundles.py` packages the complete `abntexto-ufc/` directory recursively.

These are still regression surfaces and must remain green after the rename.

### B2R-A2 — user example and distribution-facing repository layout

This is intentionally separate because these names are visible to Overleaf/template users and are explicitly referenced by distribution tooling.

Candidates to evaluate in A2 include:

- `documento.tex` → `main.tex`;
- `1-pre-textuais/` → `frontmatter/`;
- `2-textuais/` → `chapters/`;
- `3-pos-textuais/` → `backmatter/`;
- `figuras/` → `figures/`;
- `assets/institucional/` → `assets/institutional/`;
- `brasao-ufc.PNG` → a lowercase English asset name.

These are candidates, not pre-approved renames. The repository source layout and generated Overleaf bundle layout may intentionally differ if that preserves the best import experience. No A2 rename is included in A1.

### B2R-B — canonical English public API

No public API change belongs to B2R-A.

B2R-B will inventory and then introduce canonical English names for project-owned public surfaces, including `\ufcsetup` keys/values and selected UFC-owned commands/environments. Existing supported Portuguese public surfaces remain compatibility aliases throughout v2.x.

## Explicit exclusions from B2R-A1

B2R-A1 does not change:

- `tipo`, `impressao`, `capa`, `autor`, `titulo`, `orientador` or any other public setup key;
- Portuguese profile values;
- public command/environment names;
- normative source IDs, rule IDs, locators or proof-state rows;
- the `normativa/` directory name;
- article runtime behavior;
- `latex-preflight.yml`;
- academic content language.

## Required evidence for A1 closure

A1 is not complete merely because Git recognizes the moves. The exact PR head must prove:

- no old Portuguese internal module path remains loaded by the class;
- every canonical module exists exactly once;
- every `\ProvidesFile` path matches the canonical path;
- module load order is unchanged;
- repository/canonical identity audits pass;
- all twelve existing profile PDFs remain valid;
- PDF/A checks remain green;
- reference document, layout, pre-textual, project, object, bibliography and post-textual regressions remain green;
- Overleaf proxy remains green;
- no public API or normative contract changed.

Only after A1 is merged and the resulting `main` is re-certified should A2 begin.
