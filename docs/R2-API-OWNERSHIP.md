# V3-R2 API Ownership Inventory

Updated: 2026-09-03

## Purpose

This document records the completed R2 owner map and bounded B1–B5 migration sequence. It is engineering control-plane documentation, not a normative formatting source.

R2-A entry: `0a2c2c3879986ca27b731f54b974db12524258df`. B1 merge: `ded5e77733795aa2958606e899d4e27f12f64df4`. B2 merge: `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`. B3 merge: `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. B4 merge: `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`. B5 merge/R2 product closure: `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`. Mapping authority retained for permanent residual enforcement: `release/v3-api-migration.json`.

## Final-state finding

R2 is **DONE**. Every canonical v3 project API/runtime surface has a direct behavior owner. `abntexto-ufc/public-api.def` and its class load are absent. User migration is documentation-only through `docs/MIGRATING-TO-V3.md`; no runtime alias layer exists. `tests/checks/v3_api_residual.py` permanently rejects removed project-owned API in active runtime/template/test sources.

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
| forwarding-only layer | — | B5 REMOVED |

## Upstream boundaries

Dependency-owned identifiers remain only where required by the dependency contract, including `grafico` / `quadro` and upstream commands such as `\legend`, `\keywords`, `\appendix`, `\annex`, `\pretextual`, and `\textual`. Rendered Portuguese labels remain protected document content.

## Lots and evidence

| Lot | Status | Product evidence |
|---|---|---|
| R2-B1 | DONE | issue #234 / PR #236; Linux `33668283890` = `30/0/0` |
| R2-B2 | DONE | issue #237 / PR #242; Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0` |
| R2-B3 | DONE | issue #238 / PR #245; Static `33704346418`; Linux `33704346429` = `30/0/0` |
| R2-B4 | DONE | issue #239 / PR #247; Static `33736117556`; Linux `33736117558` = `30/0/0` |
| R2-B5 | DONE | issue #240 / PR #249; Static `33743809498`; Linux `33743809431` PASS; merged-main release `33745603468` = `32/0/0` |

B5 removed the forwarding file/load, completed the residual project-owned API sweep, created the migration guide, and made residual scanning permanent. No runtime aliases, normative semantics, locator policy, tolerances, or proof state changed.

## Invariants after R2

Project-owned engineering identifiers are English; rendered Brazilian academic content remains as required. Genuine upstream non-English identifiers remain only at explicit integration boundaries. Removed v2 project API remains documentation/migration-contract material only. Proprietary Microsoft fonts stay external. CTAN submission remains a later explicit release action.
