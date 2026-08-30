# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**V3-R1 ACTIVE — complete repository rebaseline.**

- Active branch: `refactor/v3-r1-rebaseline`.
- Certified v2 baseline: `main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`.
- Latest completed implementation checkpoint: `e6d7a1ce5864387ba1ccae15d21de78ddd05c2f3`.
- R1 Block 1: **DONE** — canonical physical naming.
- R1 Block 2: **DONE** — legacy purge and active-tree minimization.
- Current subgate: **R1 Block 3 — residual path-consumer reconciliation**.

## Authorities

1. `release/v3-roadmap.json`
2. `docs/HANDOFF-V3.0.0.md`
3. `docs/ROADMAP-V3.0.0.md`
4. `docs/ARCHITECTURE.md`
5. `docs/ENGINEERING-LANGUAGE.md`
6. active v3 migration contracts under `release/`

A subgate cannot close while these authorities disagree.

## Active-tree policy

The v3 branch is a working product tree, not an archive. Historical/process evidence belongs to Git commits, tags, releases, certified SHAs, issues, and pull requests. No history directory, completed campaign ledger, dormant future-feature artifact, or compatibility file is retained solely for convenience. Temporary migration contracts remain only while directly consumed by the active migration.

## Engineering-language policy

Project-controlled technical surfaces are English: paths/files, LaTeX project API and internals, setup state, source comments, diagnostics, scripts, tests, workflows, technical documentation, validator implementation/UI, machine-readable technical keys, and release tooling.

Portuguese is restricted to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, or a necessary upstream identifier at an explicit integration boundary.

## CI policy

The R1 reconstruction branch has no automatic workflows. CI returns near R1 closure only after permanent static gates and current paths are stable. Restored intermediate CI must be cheap, filtered, and cancellation-aware; heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine work is candidate/certification-only.

## V3-R0

**DONE.** Frozen migration contracts were established before implementation.

## V3-R1

### Block 1 — canonical physical naming

**DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.

### Block 2 — legacy purge and active-tree minimization

**DONE** at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

The active tree no longer carries v2 handoff/audit files, history directories, N15/B2R ledgers, N9–N12 phase snapshots, the deprecated `ufctex.cls`, dormant article contracts, N4 coverage campaign ledgers, the obsolete N2 reconciliation ledger, or Portuguese v2 normative engineering documents. Current evidence files remain only when consumed by current validators.

### Block 3 — residual path-consumer reconciliation

**ACTIVE.** Repair remaining stale references inside active files without performing the R2 runtime API rewrite.

Completed within Block 3:

- `8d8f7081b123999618d4d6e5ec5009a18ce0a89b`: central normative loaders moved from `normativa/` to `standards/` and stopped exposing N3/N4 campaign identity as the current full-contract model;
- `4fd0e61ea198ed1307e511895b254c59f5ea0dc4`: negative-path and normative-complement validation moved to current document/checker paths and dropped N13 campaign identity/duplicate execution;
- `e6d7a1ce5864387ba1ccae15d21de78ddd05c2f3`: canonical reference build path restored, reference-guide paths moved to `standards/` and `template/`, reference assets moved under `template/figures/`, and stale physical figure/code references that blocked the reference build were removed.

The Makefile development build entry point was pulled forward from the old Block 4 scope because `reference-document.sh` directly depends on `make compile`. This is a dependency correction, not a runtime/API migration: `VERSION` remains `2.1.0` until the class/runtime version changes in the appropriate phase.

Remaining Block 3 work:

- inspect every script called by `tests/run.py` and its direct checker/tool dependencies;
- remove remaining `normativa/`, `tests/normativa/`, removed `tests/v2-*`, N-phase, and project-owned `oracle` path/engineering references;
- reconcile remaining stale file references in the reference template and current standards/checkers;
- ensure every active runner target exists and every current evidence artifact has a current consumer;
- run the permanent repository/static checks once the dependency graph is fully current.

### Remaining R1 blocks

4. Remaining tools, validator, and metadata path/technical-language rebaseline. The Makefile development build path is already resolved as a Block 3 prerequisite.
5. Distribution/Overleaf/CTAN staging with repository `template/` flattened only in public bundles.
6. Permanent static gates for topology, language, inventory, and plan consistency.
7. Optimized workflow restoration.
8. Canonical repository identity, exhaustive clean-tree audit, and R1 closure.

### R1 exit criteria

- no dead historical/migration artifact without an active consumer;
- no history/archive directory;
- zero obsolete physical paths and stale active references;
- zero project-owned Portuguese technical paths;
- zero active v2/N-phase/N15/B2R/`oracle` engineering identity outside explicit upstream/runtime boundaries that are scheduled for R2;
- zero generated artifacts or temporary migration scaffolding;
- canonical template/class/build/tool/test/distribution paths resolve;
- static gates pass;
- optimized CI cannot spam intermediate commits;
- roadmap, machine state, and handoff agree.

## Later phases

- **V3-R2:** English-only direct runtime ownership; remove Portuguese project API/aliases and absorb/remove `public-api.def`.
- **V3-R3:** standards/tests/language semantic hardening.
- **V3-R4:** certification only.
- **V3-R5:** foundation freeze and current migration/user/maintainer documentation only.
- **V3-A1/A2:** article work returns when active, using Git history as evidence and reconfirming current sources.
- **V3-H1 → V3-RC → V3-FINAL → V3-CLEANUP** follow in order.

## Immediate action

Continue R1 Block 3 by auditing the remaining `tests/run.py` integration entry points and their direct dependencies. Do not advance to semantic runtime migration or distribution work while a stale active consumer remains.
