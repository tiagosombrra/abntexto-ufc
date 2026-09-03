# V3-R2 API Ownership Inventory

Updated: 2026-09-02

## Purpose

This document records the R2 owner map and bounded B1–B5 migration sequence. It is engineering control-plane documentation, not a normative formatting source.

R2-A entry: `0a2c2c3879986ca27b731f54b974db12524258df`. B1 merge: `ded5e77733795aa2958606e899d4e27f12f64df4`. B2 merge: `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`. B3 reconciled entry: `ca1b789d44343f202f23dd193a391ef85d57986e`. B3 merge/B4 product entry: `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. Authority: `release/v3-api-migration.json`.

## Current-state finding

B1, B2 and B3 forwarding has been absorbed by direct owners. `public-api.def` now contains exactly four B4 forwards: `\ufcAddBibliographyResource`, `\ufcPrintReferences`, `\ufcPrintGlossary`, and `\ufcPrintIndex`. B4 absorbs them; B5 removes the forwarding file and closes the residual migration.

## Responsibility ownership

| Runtime surface | Direct owner | R2 status |
|---|---|---|
| setup, profile state, metadata | `core.def` | B1 DONE |
| fonts | `fonts.def` | B1 DONE |
| optional module state | `modules.def` | B1 DONE |
| layout/structural lists/section hook | `layout.def` | B1/B2/B3 DONE |
| front matter + definition list | `frontmatter.def` | B2/B3 DONE |
| institutional assets | `institutional.def` | B1 DONE |
| academic cover/title/catalog card | `academic-works.def` | B1/B2 DONE |
| research-project specialization | `research-projects.def` | B1/B2 DONE |
| objects/source/note/lists/listing/minted/algorithm/object hook | `objects.def` | B3 DONE |
| ABNTexto definition-list integration/upstream boundary | `integrations/abntexto.def` | B3 DONE |
| bibliography resources/references | `bibliography.def` | B4 ACTIVE |
| glossary/index | `backmatter.def` | B4 ACTIVE |
| forwarding-only layer | `public-api.def` | four B4 forwards remain; remove in B5 |

## Upstream boundaries

Dependency-owned identifiers remain only where required by the dependency contract, including `grafico` / `quadro` and upstream commands such as `\legend`, `\keywords`, `\appendix`, `\annex`, `\pretextual`, and `\textual`. Rendered Portuguese labels remain protected document content.

## Lots

### R2-B1 — DONE
Issue #234 / PR #236. Final Linux `33668283890` = `30/0/0`.

### R2-B2 — DONE
Issue #237 / PR #242; closeout #243. Final implementation Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0`; release-source audit `33696155771` reconciled CTAN/public-bundle consumers.

### R2-B3 — DONE
Issue #238 / PR #245. Entry `ca1b789d44343f202f23dd193a391ef85d57986e`, head `e08592e90072cc6b42b1e7c61163003dc0bf7e28`, merge `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. Corrected executor `33703865896` passed; Static `33704346418` passed; Linux `33704346429` / job `100490158816` = `PASS=30 FAIL=0 SKIP=0`. No aliases, normative semantic changes or proof-state changes.

### R2-B4 — ACTIVE
Issue #239. Entry `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. Move bibliography/reference commands to `bibliography.def`, glossary/index commands to `backmatter.def`, internalize non-semantic plumbing, migrate consumers and remove only B4 forwards.

### R2-B5 — PENDING
Issue #240. Final residual sweep, remove `public-api.def` and its class load, reconcile consumed contracts, create `docs/MIGRATING-TO-V3.md`. Migration support is documentation-only; no runtime aliases.

## Invariants

Project-owned engineering identifiers are English; rendered Brazilian academic content remains as required. Owner and consumers move together. No normative rule/value/tolerance/locator/proof-state change without evidence. Proprietary Microsoft fonts stay external. CTAN submission is a later explicit release action.
