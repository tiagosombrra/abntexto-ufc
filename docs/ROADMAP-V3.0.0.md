# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**V3-R1 ACTIVE — complete repository rebaseline.**

- Active branch: `refactor/v3-r1-rebaseline`.
- Certified v2 baseline: `main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`.
- Latest completed implementation checkpoint: `91424aab55b08d0931654cd895db9ac7925ca15c`.
- Latest clean checkpoint: `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6`.
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
- `bde108b7ff0076605643e870ae7cd86ce69a7e76`: standards consumers were reconciled with current physical contracts, stale constructed standard paths were eliminated, generated Python bytecode was purged and permanently ignored, and full-contract, object-scope, normative-currency, Python syntax, shell syntax, and diff checks passed.
- `91424aab55b08d0931654cd895db9ac7925ca15c`: validation ownership was normalized against canonical `tests/run.py` check IDs; obsolete aliases were collapsed to semantic owners, manual checks remained manual, the Windows literal-font/PDF-A gate remains an explicit external owner for workflow restoration, and fifteen validation-policy consumers were migrated from the retired N5 policy contract to `validation-reference-policy.json` schema 2. Static gates passed before publication.
- `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6`: all four R1 one-shot workflow executors/auditors were removed after use. The branch contains no temporary workflow scaffolding at this checkpoint and, by policy, no permanent automatic workflows until Block 7 restoration.

The Makefile development build was pulled forward from the former Block 4 scope because `reference-document.sh` directly depends on `make compile`. This is dependency correction, not runtime/API migration; class/runtime version remains 2.1.0 until its designated phase.

Validation-owner policy after `91424aab...`:

- automatic validation metadata uses canonical semantic `tests/run.py` owners;
- `approval.signatures` and `capes` remain manual/conditional-manual requirements and therefore do not require a runner owner;
- `windows-font-pdfa` remains a platform-specific external gate and must receive its permanent workflow owner in Block 7;
- no permanent workflow is currently present in the R1 reconstruction branch.

Remaining Block 3 work:

- remove remaining active N-phase/N15/B2R campaign identity from standards scenarios, validators, checkers, and integration scripts by migrating producers and consumers together;
- replace remaining project-owned `oracle` engineering terminology with semantic validation terminology without changing normative values, rule IDs, evidence predicates, or runtime behavior;
- remove active `v2`/`V2` engineering identity from test temporary paths, messages, contracts, and metadata where it is operational rather than immutable evidence;
- verify runner-to-file and evidence-to-consumer integrity across tests, tools, validator, and active metadata after the identity migration;
- run permanent repository/static checks once the dependency graph and engineering identity are current.

### Remaining R1 blocks

4. Remaining tools, validator, and metadata technical rebaseline. The Makefile development build is already resolved as a Block 3 prerequisite.
5. Distribution/Overleaf/CTAN staging with repository `template/` flattened only in public bundles.
6. Permanent static gates for topology, language, inventory, and plan consistency.
7. Optimized workflow restoration, including the permanent owner of the Windows literal-font/PDF-A gate.
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

Migrate the remaining active N-phase/N15/B2R/`oracle`/v2 engineering identity across standards producers and their checker/integration/validator consumers as one bounded Block 3 operation. Preserve normative semantics and do not advance to Block 4 while any stale active consumer or process identity remains.
