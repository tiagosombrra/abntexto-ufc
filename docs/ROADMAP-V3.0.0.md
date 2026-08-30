# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**V3-R1 ACTIVE — complete repository rebaseline.**

- Active branch: `refactor/v3-r1-rebaseline`.
- Certified v2 baseline: `main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`.
- Latest completed implementation checkpoint: `1cd88899bd25592944e37042419aa146e39c1de6`.
- Latest migration-contract reconciliation: `66c1005f326ee6523e420165ddb9de595ef49d3d`.
- R1 Block 1: **DONE** — canonical physical naming.
- R1 Block 2: **DONE** — legacy purge and active-tree minimization.
- R1 Block 3: **ACTIVE** — residual path-consumer reconciliation.

## Authorities

1. `release/v3-roadmap.json`
2. `docs/HANDOFF-V3.0.0.md`
3. `docs/ROADMAP-V3.0.0.md`
4. `docs/ARCHITECTURE.md`
5. `docs/ENGINEERING-LANGUAGE.md`
6. active v3 migration contracts under `release/`

A subgate cannot close while these authorities disagree.

## Governing policies

The active v3 branch is a working product tree, not an archive. Historical/process evidence belongs to Git commits, tags, releases, certified SHAs, issues, and pull requests. No history directory, completed campaign ledger, dormant future-feature artifact, or compatibility file is retained solely for convenience.

Project-controlled technical surfaces are English. Portuguese is restricted to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, or a necessary upstream/current-runtime identifier at an explicit boundary. Runtime Portuguese keys/values remain unchanged during R1 and migrate only in R2.

The R1 reconstruction branch has no permanent automatic workflows until optimized workflow restoration. Temporary one-shot migration executors are removed immediately after use and must not exist at a checkpoint. Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine work is candidate/certification-only.

## V3-R0

**DONE.** Migration contracts were frozen before implementation.

## V3-R1

### Block 1 — canonical physical naming

**DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.

### Block 2 — legacy purge and active-tree minimization

**DONE** at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

### Block 3 — residual path-consumer reconciliation

**ACTIVE.** Repair stale references inside active files without performing the R2 runtime API rewrite.

Completed checkpoints:

- `8d8f7081b123999618d4d6e5ec5009a18ce0a89b`: central normative loaders moved from `normativa/` to `standards/`; current full-contract machinery no longer exposes N3/N4 campaign identity.
- `4fd0e61ea198ed1307e511895b254c59f5ea0dc4`: negative-path and normative-complement validation moved to current paths/checkers; N13 campaign identity and duplicate execution removed.
- `e6d7a1ce5864387ba1ccae15d21de78ddd05c2f3`: canonical reference build path restored; reference-guide and reference assets moved to current topology; stale physical example references repaired.
- `1b6db7598d69a6a0d8442d09e589fa8d2e151477`: layout, font-configuration, PDF-validation-core, PDF-geometry, and locator-audit gates reconnected to current fixtures/contracts.
- `d4a348c6bb1600f0fc616c1ce23c1636db606097`: PDF validator and PDF/A gates moved to `template/main.pdf`; PDF/A controlled negative validation retained while N13 campaign identity was removed.
- `1cd88899bd25592944e37042419aa146e39c1de6`: front matter contracts, fixtures, documents, checkers, and integration consumers were rebaselined to current semantic identities; obsolete project-owned `pretextual`, `posttextual`, `oracle`, and N6 validation identities were removed while upstream `\pretextual` boundaries were preserved; full normative-contract consistency passed.
- `66c1005f326ee6523e420165ddb9de595ef49d3d`: the v3 test-migration contract was reconciled with the implemented front matter evidence architecture; nonexistent oracle checker targets were removed.

All temporary `r1-frontmatter-*` workflow executors were removed before this checkpoint.

The Makefile development build was pulled forward from the former Block 4 scope because `reference-document.sh` directly depends on `make compile`. This is dependency correction, not runtime/API migration; class/runtime version remains 2.1.0 until its designated phase.

Remaining Block 3 work:

- inspect every remaining `tests/run.py` integration entry point and direct dependency;
- remove remaining active `normativa/`, `tests/normativa/`, removed `tests/v2-*`, N-phase, B2R, and project-owned `oracle` engineering references outside explicit current-runtime/upstream boundaries;
- reconcile remaining standards validation-check IDs with current semantic runner IDs;
- verify runner-to-file and evidence-to-consumer integrity across tests, tools, validator, and active metadata;
- run permanent repository/static checks once the dependency graph is current.

### Remaining R1 blocks

4. Remaining tools, validator, and metadata technical rebaseline. The Makefile development build is already resolved as a Block 3 prerequisite.
5. Distribution/Overleaf/CTAN staging with repository `template/` flattened only in public bundles.
6. Permanent static gates for topology, language, inventory, and plan consistency.
7. Optimized workflow restoration.
8. Canonical repository identity, exhaustive clean-tree audit, and R1 closure.

### R1 exit criteria

- no dead historical/migration artifact without an active consumer;
- no history/archive directory;
- zero obsolete physical paths and stale active references;
- zero project-owned Portuguese technical paths;
- zero active v2/N-phase/N15/B2R/`oracle` engineering identity outside current runtime/upstream boundaries scheduled for R2;
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
- **V3-A1/A2:** article work returns against the certified v3 foundation.
- **V3-H1 → V3-RC → V3-FINAL → V3-CLEANUP** follow in order.

## Immediate action

Complete the residual active-tree audit across the remaining `tests/run.py` graph, standards validation IDs, tools, validator, and metadata. Do not advance to Block 4 while a stale active consumer remains.
