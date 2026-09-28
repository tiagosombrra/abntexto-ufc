# Tools ownership

The `tools/` tree contains repository-owned build, validation, measurement and maintenance entry points. Its current root layout is intentional: several files are stable Makefile/CLI entry points, while the shared Python modules are imported directly by a large part of the test architecture.

Phase 5B measured **77 of 84 Python checks** as direct consumers of the root tools surface or named tool entry points. Moving these files merely to create deeper directories would add broad path/import churn without adding validation capability, so their current paths are retained deliberately.

## Stable build and release entry points

These root-level programs are invoked directly by the repository build/release interface and should keep their paths stable unless a separately bounded migration updates and validates every consumer:

- `build-distribution-bundles.py` — builds deterministic CTAN/template/Overleaf distribution archives;
- `build-public-bundles.py` — builds public editable/Overleaf bundles;
- `fetch-abntexto.py` — retrieves/verifies the pinned upstream `abntexto.cls` dependency used by repository validation/release flows.

The Makefile is the primary repository interface for these programs.

## Shared normative and repository libraries

These modules are intentionally importable from the `tools/` root by checks across many domains:

- `normative_atomic.py` — atomic normative-rule helpers;
- `normative_catalog.py` — normative catalog lookup/loading;
- `normative_full.py` — full-contract loading and shared normative semantics;
- `repository_paths.py` — canonical repository path/source lookup helpers.

They are internal repository libraries rather than standalone user commands, but their paths are high-fanout test infrastructure and should not move casually.

## PDF measurement libraries

- `pdf_measurement.py` — shared PDF geometry, text, typography and measurement primitives;
- `pdf_vector_measurement.py` — shared vector/rule measurement primitives.

These modules are reused by normative checks throughout layout, sections, citations, frontmatter, objects and validator surfaces.

## Validation CLI

- `validate-ufc-pdf.py` — repository PDF validation CLI entry point.

Treat its path as a stable repository command surface. Refactoring internals is preferable to relocating the entry point.

## Windows support and conversion utilities

- `prepare-windows-fonts.ps1` — Windows font preparation/support helper;
- `convert-encoding-to-unicode.ps1` — encoding conversion helper;
- `convert-unicode-encoding-to-glyphs.ps1` — Unicode/glyph conversion helper.

These are developer/support utilities, not CI helpers.

## CI helpers

Workflow-specific logic lives under `tools/ci/`. See [`tools/ci/README.md`](ci/README.md) for the contract between workflow YAML and repository-owned CI scripts.

CI-only helpers should normally remain in `tools/ci/` rather than moving to the root. Conversely, shared libraries should not move into `tools/ci/` solely because CI happens to consume them.

## Placement rules

When adding or reorganizing a tool:

1. keep direct Makefile/workflow/CLI entry points stable unless a bounded migration updates every consumer;
2. prefer `tools/ci/` for logic whose ownership is specifically GitHub Actions/CI orchestration;
3. keep broadly shared repository Python libraries at a stable import location;
4. avoid compatibility copies that create two authoritative implementations;
5. require a concrete ownership or maintenance benefit before moving a high-fanout path;
6. preserve fail-closed checks and run the normal Static/Linux validation path after structural changes.

The goal is clear ownership with stable contracts, not directory depth for its own sake.
