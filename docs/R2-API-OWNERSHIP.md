# V3-R2 API Ownership Inventory

Updated: 2026-09-02

## Purpose

This document closes R2-A inventory and defines the implementation order for the v3 runtime/API migration. It is an engineering ownership map, not a normative formatting source.

Entry checkpoint: `0a2c2c3879986ca27b731f54b974db12524258df` on canonical `main` after certified V3-R1 closure.

Authoritative migration contract: `release/v3-api-migration.json`.

## Current-state finding

`abntexto-ufc/public-api.def` is a transitional forwarding layer loaded last by `abntexto-ufc.cls`. Canonical English setup keys, commands and environments currently forward to Portuguese project-owned behavior implemented elsewhere. R2 must absorb each canonical surface into its responsibility-owning module and then remove `public-api.def`; it must not replace the current forwarding direction with another compatibility layer.

The editable reference document still uses the Portuguese project API. Every runtime lot therefore migrates the corresponding `template/` and test consumers atomically with the behavior owner.

## Responsibility ownership

| Runtime surface | Current behavior owner | R2 responsibility |
|---|---|---|
| document type, print mode, cover/catalog-card/coat-of-arms policy, metadata, project predicates | `abntexto-ufc/core.def` | direct canonical setup keys and canonical internal state/metadata vocabulary |
| font family and strict-font policy | `abntexto-ufc/fonts.def` | direct `font` / `strict-font` ownership and canonical diagnostics |
| table/code/algorithm/glossary/index module selection | `abntexto-ufc/modules.def` | direct canonical module keys/values; remove project-owned `nativo` / `nenhum` state |
| page geometry, duplex flow, front-matter breaks, structural list environments | `abntexto-ufc/layout.def` | consume canonical state; own canonical list environments; internalize layout plumbing |
| approval/dedication/acknowledgments/epigraph/errata/summary/abstract/front-matter lists/TOC | `abntexto-ufc/frontmatter.def` | direct canonical rendering commands and definition-list API; preserve rendered Portuguese labels |
| institutional asset path | `abntexto-ufc/institutional.def` | direct `coat-of-arms-file` ownership |
| academic cover/title/catalog card and initial page | `abntexto-ufc/academic-works.def` | direct canonical commands/key; consume canonical state |
| research-project cover/title specialization | `abntexto-ufc/research-projects.def` | specialize canonical cover/title behavior; consume canonical metadata/state |
| figures/charts/text tables/code/algorithms/source/note and optional object APIs | `abntexto-ufc/objects.def` | direct canonical commands/environments/hooks; replace project-owned Portuguese object IDs while preserving rendered labels |
| bibliography resource registration and reference section | `abntexto-ufc/bibliography.def` | direct canonical bibliography commands; preserve rendered `Referências` |
| glossary/index presentation | `abntexto-ufc/backmatter.def` | direct canonical glossary/index commands; internalize setup/heading plumbing |
| current ABNTexto/LaTeX compatibility | `abntexto-ufc/integrations/abntexto.def` | retain only genuine upstream adaptation; update the canonical definition-list environment in the same lot as its owner |
| forwarding-only canonical aliases | `abntexto-ufc/public-api.def` | progressively shrink as owners absorb surfaces; remove completely at R2 closeout |

## Upstream boundary classification

Non-English identifiers are not migrated merely because they are non-English when they are genuinely owned upstream. Current examples include ABNTexto-facing `grafico` / `quadro` identifiers and upstream public commands such as `\legend`, `\keywords`, `\appendix`, `\annex`, `\pretextual`, and `\textual` where required by the dependency contract.

Project-owned Portuguese identifiers remain migration targets. In particular, `codigo` / `algoritmo`, Portuguese setup keys/values, Portuguese public rendering commands/environments, Portuguese metadata keys, and project-owned `pretextual` / `posttextual` engineering terminology must not survive R2 as active project-owned engineering API.

## Migration lots

### R2-B1 — canonical setup and internal state vocabulary

Operational issue: #234.

Move all canonical setup keys/values into their direct owners in `core.def`, `fonts.def`, `modules.def`, `institutional.def`, and `academic-works.def`. Migrate document-type values, print-mode values, project-owned boolean/configuration values, metadata property keys and module state to the canonical vocabulary. Update all state consumers in `layout.def`, `frontmatter.def`, `academic-works.def`, `research-projects.def`, template configuration and tests in the same lot. Remove the migrated setup forwarding entries from `public-api.def`.

### R2-B2 — academic and front-matter public rendering API

Move `\ufcPrintCover`, `\ufcPrintTitlePage`, `\ufcPrintApprovalPage`, `\ufcPrintCatalogCard`, dedication/acknowledgments/epigraph/errata, summary/abstract, front-matter lists, list entry and table-of-contents commands into `academic-works.def`, `research-projects.def`, and `frontmatter.def` as appropriate. Rebind `layout.def` command hooks to canonical commands and remove the corresponding Portuguese project commands and forwarding definitions atomically.

### R2-B3 — structural/object environments, optional object API and extension hooks

Make `ufclettereditems`, `ufcdashedsubitems`, `ufcdefinitionlist`, `ufcobject`, `ufclisting`, and `ufcalgorithm` the direct environments in their owners. Update `integrations/abntexto.def` together with `ufcdefinitionlist`. Move source/note/list-of-chart/code/algorithm and optional listing/minted APIs to direct canonical ownership. Rename project extension hooks to `\ufcSectionHook` and `\ufcObjectLegendHook`. Replace project-owned object IDs `codigo` / `algoritmo`; preserve genuine upstream `grafico` / `quadro` only at integration boundaries.

### R2-B4 — bibliography/back-matter API and plumbing internalization

Move `\ufcAddBibliographyResource`, `\ufcPrintReferences`, `\ufcPrintGlossary`, and `\ufcPrintIndex` to direct ownership. Internalize non-semantic plumbing listed by the API contract, including layout/front-matter/back-matter heading and module-setup helpers. Preserve Portuguese rendered academic headings.

### R2-B5 — final consumer migration and forwarding-layer removal

Migrate any remaining template/test/documentation consumers, remove `abntexto-ufc/public-api.def` from the tree and from `abntexto-ufc.cls`, run a fail-closed residual scan for project-owned Portuguese API/internal identifiers, reconcile `release/v3-test-migration.json`, and produce `docs/MIGRATING-TO-V3.md` from the authoritative old-to-new mappings. No runtime aliases are introduced.

## Cross-lot invariants

- Project-owned engineering identifiers are English; rendered Brazilian academic content remains in the language required by the document.
- No normative rule ID, expected value, tolerance, locator, or proof state changes without explicit new normative evidence.
- Producer, state consumer, template consumer and test consumer move together.
- No blind global replacement.
- No new Portuguese-to-English or English-to-Portuguese runtime compatibility layer.
- Upstream identifiers are changed only when the project owns them.
- Proprietary Microsoft fonts remain external and are never redistributed.
- CTAN submission remains an explicit later release action.
- `make static-check` and the permanent `Linux integration` gate validate each behavioral lot; heavier certification is rerun only when current-state changes require it.

## R2-A exit condition

R2-A is complete when this ownership map, `release/v3-api-migration.json`, `release/v3-test-migration.json`, `release/v3-path-migration.json`, the roadmap and handoff agree on the migration sequence and R2-B1 is explicitly activated with no unresolved owner ambiguity.
