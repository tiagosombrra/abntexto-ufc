# V3-R2 API Ownership Inventory

Updated: 2026-09-03

## Purpose

This document records the R2 owner map and bounded B1–B5 migration sequence. It is engineering control-plane documentation, not a normative formatting source.

R2-A entry: `0a2c2c3879986ca27b731f54b974db12524258df`. B1 merge: `ded5e77733795aa2958606e899d4e27f12f64df4`. B2 merge: `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`. B3 merge: `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. B4 control-plane entry: `ab900797836eb068b3f100574759816eadb039d5`. B4 merge/B5 product entry: `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`. Authority: `release/v3-api-migration.json`.

## Current-state finding

B1 through B4 forwarding has been absorbed by direct owners. `public-api.def` is now intentionally empty; B5 removes that file and its class load, runs the final residual migration scan, reconciles the consumed contracts, and creates the user migration guide.

## Responsibility ownership

| Runtime surface | Direct owner | R2 status |
|---|---|---|
| setup, profile state, metadata | `core.def` | B1 DONE |
| fonts | `fonts.def` | B1 DONE |
| optional module state | `modules.def` | B1/B4 DONE |
| layout/structural lists/section hook | `layout.def` | B1/B2/B3 DONE |
| front matter + definition list | `frontmatter.def` | B2/B3 DONE |
| institutional assets | `institutional.def` | B1 DONE |
| academic cover/title/catalog card | `academic-works.def` | B1/B2 DONE |
| research-project specialization | `research-projects.def` | B1/B2 DONE |
| objects/source/note/lists/listing/minted/algorithm/object hook | `objects.def` | B3 DONE |
| ABNTexto definition-list integration/upstream boundary | `integrations/abntexto.def` | B3 DONE |
| bibliography resources/references | `bibliography.def` | B4 DONE |
| glossary/index | `backmatter.def` | B4 DONE |
| forwarding-only layer | `public-api.def` | empty; physical removal in B5 |

## Upstream boundaries

Dependency-owned identifiers remain only where required by the dependency contract, including `grafico` / `quadro` and upstream commands such as `\legend`, `\keywords`, `\appendix`, `\annex`, `\pretextual`, and `\textual`. Rendered Portuguese labels remain protected document content.

## Lots

### R2-B1 — DONE
Issue #234 / PR #236. Final Linux `33668283890` = `30/0/0`.

### R2-B2 — DONE
Issue #237 / PR #242; closeout #243. Final implementation Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0`.

### R2-B3 — DONE
Issue #238 / PR #245. Merge `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`; Static `33704346418`; Linux `33704346429` = `30/0/0`.

### R2-B4 — DONE
Issue #239 / PR #247. Product entry `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`, control-plane entry `ab900797836eb068b3f100574759816eadb039d5`, head `c2afa9e283380a1ae008638c73d12561eb97e537`, merge `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`. Final Static `33736117556` passed and Linux `33736117558` / `100587276948` = `PASS=30 FAIL=0 SKIP=0`. The final heading observer preserved the rendered `ÍNDICE REMISSIVO` and measured the whole line; no runtime aliases, normative semantics, locator policy, tolerances or proof-state changed.

### R2-B5 — ACTIVE
Issue #240. After this closeout merges: remove `public-api.def` and its class load, perform the final project-owned Portuguese runtime/API/internal residual sweep, reconcile consumed contracts, and generate `docs/MIGRATING-TO-V3.md`. Migration support remains documentation-only; no runtime aliases.

## Invariants

Project-owned engineering identifiers are English; rendered Brazilian academic content remains as required. Owner and consumers move together. No normative rule/value/tolerance/locator-policy/proof-state change without evidence. Proprietary Microsoft fonts stay external. CTAN submission is a later explicit release action.
