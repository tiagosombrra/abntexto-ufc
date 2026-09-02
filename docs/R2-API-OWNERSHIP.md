# V3-R2 API Ownership Inventory

Updated: 2026-09-02

## Purpose

This document records the completed R2-A ownership inventory, the closed R2-B1 setup/state migration, the closed R2-B2 academic/front-matter migration, and the bounded implementation order for the remaining v3 runtime/API migration. It is an engineering ownership map, not a normative formatting source.

R2-A entry checkpoint: `0a2c2c3879986ca27b731f54b974db12524258df`.
R2-B1 merged checkpoint: `ded5e77733795aa2958606e899d4e27f12f64df4`.
R2-B2 merged checkpoint: `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`.
Authoritative migration contract: `release/v3-api-migration.json`.

## Current-state finding

`abntexto-ufc/public-api.def` remains a transitional forwarding layer loaded last by `abntexto-ufc.cls`. B1 removed setup-key forwarding and B2 removed academic/front-matter command forwarding. Canonical setup/state and academic/front-matter rendering behavior are directly owned by responsibility modules. The remaining forwarding debt is bounded to B3 structural/object surfaces and B4 bibliography/back-matter surfaces before complete removal in B5.

The editable reference document and tests use the canonical B1/B2 surfaces but still contain structural/object consumers owned by B3 and bibliography/back-matter consumers owned by B4. Each remaining runtime lot therefore migrates the corresponding `template/` and test consumers atomically with the behavior owner.

A late B2-closeout audit also found four active release consumers outside the primary template/test sweep: `docs/ctan-example.tex`, `release/ctan/abntexto-ufc.tex`, `tools/build-public-bundles.py`, and `tests/checks/public_bundles.py`. Their residual v2 setup assumptions were repaired immediately and classified as B1/B2 consumer reconciliation, not B3 work. Final audit run `33696155771` / job `100465339990` passed source compilation, public/distribution bundle validation, reproducibility, stale-token scanning, cleanup, `git diff --check`, and `make static-check`.

## Responsibility ownership

| Runtime surface | Direct/current behavior owner | R2 responsibility/status |
|---|---|---|
| document type, print mode, cover/catalog-card/coat-of-arms policy, metadata, project predicates | `abntexto-ufc/core.def` | B1 DONE — direct canonical setup/state ownership |
| font family and strict-font policy | `abntexto-ufc/fonts.def` | B1 DONE — direct `font` / `strict-font` ownership |
| table/code/algorithm/glossary/index module selection | `abntexto-ufc/modules.def` | B1 DONE — canonical module keys/values |
| page geometry, duplex flow, front-matter breaks, structural list environments | `abntexto-ufc/layout.def` | B1 state DONE; B2 hook rebinding DONE; B3 structural environments ACTIVE |
| approval/dedication/acknowledgments/epigraph/errata/summary/abstract/front-matter lists/TOC | `abntexto-ufc/frontmatter.def` | B2 DONE — direct canonical rendering commands; B3 definition-list environment ACTIVE |
| institutional asset path | `abntexto-ufc/institutional.def` | B1 DONE — direct `coat-of-arms-file` ownership |
| academic cover/title/catalog card and initial page | `abntexto-ufc/academic-works.def` | B1 key/state DONE; B2 rendering commands DONE |
| research-project cover/title specialization | `abntexto-ufc/research-projects.def` | canonical B1 state consumer; B2 canonical cover/title specialization DONE |
| figures/charts/text tables/code/algorithms/source/note and optional object APIs | `abntexto-ufc/objects.def` | B3 ACTIVE |
| bibliography resource registration and reference section | `abntexto-ufc/bibliography.def` | B4 PENDING |
| glossary/index presentation | `abntexto-ufc/backmatter.def` | canonical B1 module-state consumer; B4 PENDING |
| current ABNTexto/LaTeX compatibility | `abntexto-ufc/integrations/abntexto.def` | retain genuine upstream adaptation; canonical definition-list environment migration ACTIVE in B3 |
| forwarding-only canonical aliases | `abntexto-ufc/public-api.def` | setup forwarding removed in B1; academic/front-matter forwarding removed in B2; absorb B3/B4 then remove completely in B5 |

## Upstream boundary classification

Non-English identifiers are not migrated merely because they are non-English when they are genuinely owned upstream. Current examples include ABNTexto-facing `grafico` / `quadro` identifiers and upstream public commands such as `\legend`, `\keywords`, `\appendix`, `\annex`, `\pretextual`, and `\textual` where required by the dependency contract.

Project-owned Portuguese identifiers remain migration targets. Portuguese public rendering commands/environments, project-owned object IDs, and project-owned pretextual/posttextual engineering terminology must not survive R2 as active project-owned engineering API. Rendered Portuguese labels remain protected document content.

## Migration lots

### R2-B1 — canonical setup and internal state vocabulary — DONE

Operational issue: #234. Implementation PR: #236. Merged `main`: `ded5e77733795aa2958606e899d4e27f12f64df4`.

B1 moved all canonical setup keys/values into their direct owners in `core.def`, `fonts.def`, `modules.def`, `institutional.def`, and `academic-works.def`; migrated document/profile state, boolean/configuration state, metadata property keys and module state; updated all live consumers; and removed the migrated setup forwarding entries from `public-api.def`.

The first full post-migration integration run `33665983360` failed closed at `PASS=24 FAIL=6 SKIP=0`, exposing six stale dynamic test generators. After bounded repair, final implementation head `99fb58deaa1594ca19fb3a00ca9418623e5b25aa` passed `Static contract` run `33668283912` and `Linux integration` run `33668283890` at `PASS=30 FAIL=0 SKIP=0`. No normative semantics/proof state changed and no compatibility alias layer was introduced.

### R2-B2 — academic and front-matter public rendering API — DONE

Operational issue: #237. Implementation PR: #242. Entry `main`: `e418893ee5c89f12cc4ac8d845111c894ec946e4`. Merged `main`: `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`.

B2 moved cover/title/approval/catalog-card, dedication/acknowledgments/epigraph/errata, summary/abstract, front-matter lists, list-entry and table-of-contents commands into direct owners; rebound layout hooks; migrated template/test/reference/CTAN/scenario consumers; and removed B2 forwards from `public-api.def`. The first executor run `33679535751` failed closed on its own cleanup order. Corrected run `33679827267` passed, then strengthened residual audit `33680252116` caught and closed hook/specialization gaps. Final head `4341a2adb4633b634d1e2ad905b1731e8126354b` passed `Static contract` `33680378948` and `Linux integration` `33680378846` / job `100415223907` with `PASS=30 FAIL=0 SKIP=0`; merged-main `Linux release check` `33687588772` passed `PASS=32 FAIL=0 SKIP=0`.

The B2→B3 closeout then exposed a separate active-release-consumer residue: the CTAN example/manual and public-bundle producer/checker still assumed v2 setup vocabulary. Those consumers were reconciled to canonical v3 setup before B3 activation. Audit run `33696155771`, job `100465339990`, passed both CTAN-source compilations, public and distribution bundle reproducibility/layout/asset checks, residual scanning and clean self-removal. No generated reference photograph, runtime alias, normative semantics/proof-state change, proprietary font redistribution or CTAN submission was introduced.

### R2-B3 — structural/object environments, optional object API and extension hooks — ACTIVE

Operational issue: #238. Entry `main`: the canonical B2→B3 closeout merge, after PR #243 passes final permanent gates and lands on `main`.

Make `ufclettereditems`, `ufcdashedsubitems`, `ufcdefinitionlist`, `ufcobject`, `ufclisting`, and `ufcalgorithm` the direct environments in their owners. Update `integrations/abntexto.def` together with `ufcdefinitionlist`. Move source/note/list-of-chart/code/algorithm and optional listing/minted APIs to direct canonical ownership. Rename project extension hooks to `\ufcSectionHook` and `\ufcObjectLegendHook`. Replace project-owned object IDs `codigo` / `algoritmo`; preserve genuine upstream `grafico` / `quadro` only at integration boundaries.

### R2-B4 — bibliography/back-matter API and plumbing internalization — PENDING

Operational issue: #239.

Move `\ufcAddBibliographyResource`, `\ufcPrintReferences`, `\ufcPrintGlossary`, and `\ufcPrintIndex` to direct ownership. Internalize non-semantic plumbing listed by the API contract, including layout/front-matter/back-matter heading and module-setup helpers. Preserve Portuguese rendered academic headings.

### R2-B5 — final consumer migration and forwarding-layer removal — PENDING

Operational issue: #240.

Migrate any remaining template/test/documentation consumers, remove `abntexto-ufc/public-api.def` from the tree and from `abntexto-ufc.cls`, run a fail-closed residual scan for project-owned Portuguese API/internal identifiers, reconcile `release/v3-test-migration.json`, and produce `docs/MIGRATING-TO-V3.md` from the authoritative old-to-new mappings. No runtime aliases are introduced.

## Cross-lot invariants

- Project-owned engineering identifiers are English; rendered Brazilian academic content remains in the language required by the document.
- No normative rule ID, expected value, tolerance, locator, or proof state changes without explicit new normative evidence.
- Producer/behavior owner, state consumer, template consumer and test consumer move together where applicable.
- No blind global replacement.
- No new Portuguese-to-English or English-to-Portuguese runtime compatibility layer.
- Upstream identifiers are changed only when the project owns them.
- Proprietary Microsoft fonts remain external and are never redistributed.
- CTAN submission remains an explicit later release action.
- `make static-check` and the permanent `Linux integration` gate validate each behavioral lot; heavier certification is rerun only when current-state changes require it.

## R2-A exit condition

R2-A is complete. The ownership map, machine contracts and control plane agree on the B1–B5 sequence. B1 and B2 are complete; B3/#238 becomes the sole active implementation lot only after the B2→B3 closeout PR #243 is merged green.
