# Release ownership

The `release/` tree owns repository sources and control records that exist specifically for packaging, release certification and historical release continuity.

## `ctan/`

`release/ctan/` is the canonical repository namespace for CTAN-facing source material used by `tools/build-distribution-bundles.py`:

- `README.md` — package README source;
- `abntexto-ufc.tex` — package manual source;
- `abntexto-ufc-example.tex` — minimal portable example source.

The builder emits the example into the CTAN archive as `abntexto-ufc/abntexto-ufc-example.tex` and compiles the matching PDF. Repository source ownership may evolve on `main`, but already-published release/tag/archive bytes are immutable and must never be replaced retroactively.

CTAN-facing sources must not vendor UFC institutional marks or proprietary Microsoft font files.

## `history/`

`release/history/v3/` contains durable historical release receipts, migration records and prior release-candidate evidence. These files describe past states and should not be rewritten merely to match current development facts.

## Current release control

`release/v3-release-candidate.json` is the current repository control marker for the v3 release line. Changes to release-state metadata must follow the repository release/governance contracts and must not imply that published artifacts were rebuilt or replaced.

## Stable build entry points

Release packaging continues through the stable repository entry points in `tools/` and `tools/ci/`. Phase 5 structural work does not move those externally consumed Makefile/workflow paths unless a separately bounded change preserves their contract explicitly.
