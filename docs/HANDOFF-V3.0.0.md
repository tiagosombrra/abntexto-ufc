# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-08-30

## Checkpoint

- Phase: **V3-R1 ACTIVE**.
- Active block: **R1 Block 2 — legacy purge and active-tree minimization**.
- Branch: `refactor/v3-r1-rebaseline`.
- Latest completed implementation SHA: `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Clean-tree rule

Do not create or retain repository museums.

Historical evidence belongs to Git history, tags, releases, certified commit/blob SHAs, issues, and pull requests. The active v3 tree contains only:

1. files required by the current v3 product/runtime/tests/build/distribution; or
2. temporary migration contracts directly consumed by the active migration.

Therefore:

- no `docs/history/`, `release/history/`, or `standards/history/`;
- no v2/N15/B2R/N-phase handoff, ledger, campaign snapshot, audit report, or compatibility inventory without an active v3 consumer;
- no dormant future-phase article files before V3-A1;
- no compatibility checker retained merely to prove past compatibility;
- no duplicate old/new documentation during renames;
- temporary migration contracts are deleted or consolidated when no longer needed.

A deletion and the repair/removal of all current consumers are one atomic cleanup responsibility.

## CI rule

`.github/workflows/` remains absent during structural R1 work. When restored, automatic CI must be cheap, filtered, and cancel superseded runs. Gate T, Overleaf, PDF/A, distribution/CTAN, and full multi-engine suites are candidate/certification jobs rather than intermediate-commit jobs.

## Engineering-language rule

Every project-owned technical surface is English, including validator implementation and UI. Portuguese is limited to academic output/data, official names/wording, literal Portuguese payload under test, and necessary upstream integration identifiers.

## Block 1 — DONE

Closed at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.

The active physical tree now uses the canonical `template/`, `standards/`, semantic test roots, current integration/standard-adapter roots, and no `oracle`/old document-phase terminology in tracked path names.

## Block 2 — ACTIVE

Perform a dependency-aware purge. Current confirmed removal candidates include:

- `docs/history/` and its v2 audit;
- `docs/B2R-NAMING-INVENTORY.md`;
- `docs/HANDOFF-V2.2.0.md`;
- obsolete v2 `docs/NAMING.md`;
- historical `release/final-audit.json` and `release/n15-*` ledgers;
- N9–N12 process/reconciliation snapshots under `standards/` when they are not current normative inputs;
- dormant article-only standards/checkers until V3-A1;
- `tests/checks/public_api_contract.py` and other phase-specific v2 audit/source-authority checkers;
- deprecated `ufctex.cls`.

Current v3 migration contracts remain only because R1/R2 still consume them.

Current Portuguese technical documentation filenames must be renamed, not duplicated: `docs/NORMAS.md` and `docs/VIGENCIA-NORMATIVA.md` require English active names with consumers updated.

## Required reconciliation in this block

`tests/run.py` is known stale and must be fixed together with the purge: remove the historical public-API gate, replace `pdf-oracle-core` with current PDF validation naming, and use `template/main.pdf` where the reference document path is required.

Do not leave deleted-file references for a later block when they are direct consequences of this purge.

## Remaining R1 order

3. residual path-consumer reconciliation;
4. Makefile/tools/validator/metadata paths;
5. distribution and public bundle flattening;
6. permanent static gates;
7. optimized workflow restoration;
8. canonical repository identity plus exhaustive clean-tree R1 closure.

## Immediate action

Commit the active-tree policy authorities, then execute the dependency-aware legacy purge on the same branch with Actions disabled. Verify the resulting tracked tree before advancing the roadmap.
