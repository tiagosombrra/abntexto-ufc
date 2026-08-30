# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-08-30

## Checkpoint

- Phase: **V3-R1 ACTIVE**.
- Active block: **R1 Block 3 — residual path-consumer reconciliation**.
- Branch: `refactor/v3-r1-rebaseline`.
- Latest completed implementation SHA: `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Non-negotiable clean-tree rule

The active v3 repository is not an archive. Historical/process evidence belongs to Git history, tags, releases, issues, pull requests, and certified SHAs. No history directories, dormant future-feature files, or completed campaign ledgers remain merely for convenience.

Temporary migration contracts may remain only while directly consumed by R1/R2. Remove or consolidate them when their consumer disappears.

## CI rule

`.github/workflows/` remains absent during structural R1 reconstruction. CI is restored only after the permanent static gates and current paths are stable. Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs are candidate/certification work, not intermediate-commit work.

## Engineering-language rule

Every project-owned technical surface is English, including validator implementation and technical UI. Portuguese is limited to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, and required upstream identifiers at explicit integration boundaries.

## R1 Block 1 — DONE

Canonical physical naming closed at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.

## R1 Block 2 — DONE

Closed at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

Completed cleanup:

- deleted v2 handoff/audit/naming inventory and history directory;
- deleted N15/B2R release ledgers and compatibility-only checkers;
- deleted deprecated `ufctex.cls`;
- deleted N9–N12 campaign/reconciliation snapshots and phase-only checkers;
- deleted dedicated dormant article rule/locator files until V3-A1;
- deleted N4 coverage promotion/audit ledgers and rewrote coverage validation against the current contract;
- deleted obsolete N2 reconciliation ledger/checker;
- replaced Portuguese v2 normative technical docs with `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md`;
- rewrote active README/architecture/language policy for the v3 active tree.

A physical-tree audit found no active history directory, N15/B2R physical artifact, dedicated article rule file, or obsolete reconciliation ledger. Current locator/source evidence stays because active validators consume it.

## R1 Block 3 — ACTIVE

Goal: remove stale references and retired engineering terminology from active consumers without performing the R2 runtime API rewrite.

Known work:

1. migrate central normative tool paths from `normativa/` to `standards/`;
2. migrate active checker paths from `normativa/` to `standards/`;
3. migrate integration fixtures from `tests/normativa/` to `tests/documents/` or current fixtures;
4. remove references to deleted N-phase/v2 checkers;
5. eliminate active `oracle`, `pretextual`, `posttextual`, and v2 engineering labels where they are project-owned technical terminology;
6. update the repository contract for the new normative documentation and forbidden old names;
7. validate that every active runner points to an existing file and every current evidence file has a current consumer.

`tests/integration/normative-complement.sh` is a confirmed stale consumer: it still calls a removed N12 checker, `tests/normativa/...`, `tests/v2-*` scripts, uses v2 temp-log names, and emits Portuguese technical diagnostics. It must be rebuilt rather than patched cosmetically.

The central loaders `tools/normative_catalog.py`, `tools/normative_atomic.py`, and `tools/normative_full.py` still resolve `normativa/`; they are first-order Block 3 fixes.

## Remaining R1 order

4. Makefile/tools/validator/metadata technical rebaseline.
5. Distribution and public bundle flattening.
6. Permanent static gates.
7. Optimized workflow restoration.
8. Repository identity plus exhaustive clean-tree R1 closure.

## Immediate action

Start Block 3 with the central normative loaders and the runner-called integration scripts. Re-run structural inventory after each coherent migration set; do not defer a known stale consumer to R2.
