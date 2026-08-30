# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**V3-R1 ACTIVE — complete repository rebaseline.**

- Active branch: `refactor/v3-r1-rebaseline`.
- Certified v2 baseline: `main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`.
- Latest completed implementation checkpoint: `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.
- Current subgate: **R1 Block 2 — legacy purge and active-tree minimization**.

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

- No `docs/history/`, `release/history/`, `standards/history/`, or equivalent museum directories.
- No file is retained solely because it documents a past phase, may be useful later, or provides historical convenience.
- Historical evidence lives in Git commits, tags, releases, certified SHAs, and issue/PR history.
- v2/N-phase/N15/B2R ledgers, handoffs, audit snapshots, compatibility inventories, and superseded checkers are removed from the active v3 tree once they have no current consumer.
- Temporary migration contracts may remain only while they are directly consumed by the active migration. They are removed or consolidated when their migration gate closes.
- Future-phase material is not pre-staged as dormant files. It is reintroduced when that phase becomes active, using Git history as evidence where needed.
- Dead references are treated as defects: deletion of an artifact and reconciliation of its consumers belong to the same coherent block.

## Engineering-language policy

Project-controlled technical surfaces are English: repository paths/files, LaTeX project API and internals, setup keys/state, source comments, diagnostics, scripts, tests, workflows, technical documentation, validator implementation/UI, and JSON/schema technical keys.

Portuguese is allowed only as academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, or a genuinely required upstream identifier at an explicit integration boundary.

No final v3 Portuguese project compatibility API is retained.

## CI policy

The R1 reconstruction branch has no automatic workflows.

When CI is restored near R1 closure:

- automatic checks are static/cheap and path-filtered where practical;
- `concurrency` uses `cancel-in-progress: true`;
- integration jobs run only for affected surfaces, final PR validation, or manual dispatch;
- Windows Gate T, Overleaf, PDF/A, distribution/CTAN, and full multi-engine regression are candidate/certification jobs, not per-commit jobs;
- workflows never mutate the repository or create migration commits;
- final candidate sequence is static gate → affected integration gates → one full exact-SHA certification suite.

## V3-R0

**DONE.** Frozen migration contracts were established before implementation.

## V3-R1

**ACTIVE.** R1 owns all physical topology, active-tree cleanup, path consumers, build/tool/validator paths, distribution staging, static structural gates, and optimized workflow restoration.

### Block 1 — canonical physical naming

**DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.

Completed:

- editable source under `template/`;
- standards root under `standards/`;
- semantic test roots;
- English template/component paths;
- removal of active `oracle`, `pretextual`, `posttextual`, and `textual-oracle` path naming;
- current frontmatter validation paths and fixtures.

### Block 2 — legacy purge and active-tree minimization

**ACTIVE.** Delete, do not archive, artifacts that have no current v3 consumer. Reconcile all direct consumers in the same block.

Scope includes:

- v2/N15/B2R handoffs, inventories, ledgers, audits, and superseded compatibility policies;
- N-phase campaign/reconciliation snapshots that are process history rather than current normative inputs;
- dormant future article artifacts until V3-A1;
- obsolete v2 compatibility checkers;
- deprecated `ufctex.cls`;
- stale technical filenames such as current Portuguese documentation filenames, replacing them with English active names rather than preserving duplicates.

### Remaining R1 blocks

3. Path-consumer reconciliation across tests/checkers/integration/standards.
4. `Makefile`, tools, validator, and metadata path reconciliation.
5. Distribution/Overleaf/CTAN staging with `template/` flattened only in public bundles.
6. Permanent static gates for topology, language, inventory, and plan consistency.
7. Optimized workflow restoration.
8. Canonical repository identity, exhaustive clean-tree audit, and R1 closure.

### R1 exit criteria

- no dead historical/migration artifacts without an active consumer;
- no history/archive directories in the active tree;
- zero obsolete physical paths and stale active references;
- zero project-owned Portuguese technical paths;
- zero active `oracle`, v2, N-phase, N15, or B2R engineering identities;
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
- **V3-A1/A2:** article work is reintroduced when active, using Git history as evidence rather than dormant files.
- **V3-H1 → V3-RC → V3-FINAL → V3-CLEANUP** follow in order.

## Immediate action

Execute R1 Block 2 as an atomic active-tree cleanup: delete unconsumed legacy artifacts, update their active consumers, keep Actions disabled, then synchronize authorities before Block 3.
