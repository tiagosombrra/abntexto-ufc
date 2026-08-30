# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**V3-R1 ACTIVE — complete repository rebaseline.**

- Active branch: `refactor/v3-r1-rebaseline`.
- Certified v2 baseline: `main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`.
- Latest completed implementation checkpoint: `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.
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

The v3 branch is a working product tree, not an archive.

- No history/museum directories.
- No file is retained solely for historical convenience, a completed campaign, or a future feature.
- Historical evidence lives in Git commits, tags, releases, certified SHAs, issues, and pull requests.
- Temporary migration contracts remain only while the active migration directly consumes them.
- Deletion of an obsolete artifact and reconciliation of its direct consumers are one coherent change.
- Scientific-article implementation/contracts return only when V3-A1 becomes active.

## Engineering-language policy

Project-controlled technical surfaces are English: paths/files, LaTeX project API and internals, setup state, source comments, diagnostics, scripts, tests, workflows, technical documentation, validator implementation/UI, and machine-readable technical keys.

Portuguese is restricted to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, or a necessary upstream identifier at an explicit integration boundary.

## CI policy

The R1 reconstruction branch has no automatic workflows. When CI is restored near R1 closure it must be cheap, filtered, and cancellation-aware; heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine work is candidate/certification-only.

## V3-R0

**DONE.** Frozen migration contracts were established before implementation.

## V3-R1

### Block 1 — canonical physical naming

**DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.

### Block 2 — legacy purge and active-tree minimization

**DONE** at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

Removed from the active tree:

- v2 handoff/audit/naming inventory and `docs/history/`;
- N15/B2R release ledgers and v2 compatibility checkers;
- deprecated `ufctex.cls`;
- N9–N12 campaign/reconciliation snapshots and their phase-only checkers;
- dormant article rule/locator artifacts until V3-A1;
- N4 coverage campaign ledgers, replacing campaign reconstruction with direct current-contract coverage validation;
- obsolete N2 reconciliation ledger/checker;
- Portuguese v2 normative technical documents, replaced by current English v3 contracts.

Physical closure audit found no active `docs/history`, `n15-*`, `b2r`, dedicated article rule artifact, or reconciliation ledger path.

Files such as current locator evidence remain because they are consumed by current validators; active evidence is not treated as historical clutter.

### Block 3 — residual path-consumer reconciliation

**ACTIVE.** Repair remaining stale references inside active files without semantic runtime API migration.

Primary work:

- `normativa/` → `standards/` in active tools/checkers/integration scripts;
- old `tests/normativa/` / renamed test paths → current `tests/documents/` and semantic paths;
- remove internal `oracle`, N-phase, v2, pretextual/posttextual engineering terminology from active consumers;
- reconcile references to removed documentation and checkers;
- update repository contract to require the current normative docs and reject superseded names;
- keep changes path/engineering-only where runtime API semantics belong to R2.

### Remaining R1 blocks

4. Makefile, tools, validator, and metadata path/technical-language reconciliation.
5. Distribution/Overleaf/CTAN staging with `template/` flattened only in public bundles.
6. Permanent static gates for topology, language, inventory, and plan consistency.
7. Optimized workflow restoration.
8. Canonical repository identity, exhaustive clean-tree audit, and R1 closure.

### R1 exit criteria

- no dead historical/migration artifacts without an active consumer;
- no history/archive directories;
- zero obsolete physical paths and stale active references;
- zero project-owned Portuguese technical paths;
- zero active v2/N-phase/N15/B2R/`oracle` engineering identity;
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
- **V3-A1/A2:** article work is reintroduced when active, using Git history as evidence and reconfirming current sources.
- **V3-H1 → V3-RC → V3-FINAL → V3-CLEANUP** follow in order.

## Immediate action

Execute R1 Block 3 from the clean physical baseline: reconcile stale active references and terminology, validate the resulting dependency graph, then synchronize authorities before Block 4.
