# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-01

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-3 — Semantic / Path-Consumer Closure**.
- Active Block 3 work item: **B3-F — Final Block 3 residual audit**.
- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`.
- R1-S2 trunk promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 control-plane closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

The GitHub repository was renamed to `abntexto-ufc` on 2026-09-01 without changing repository ID, history, `main`, tags, issues, pull requests, or governance. The old repository name is not an active project identity.

`main` is the canonical trunk and merge target. Short-lived task branches are permitted by `AGENTS.md`, but canonical phase/stage authority remains in the control-plane files on `main`.

## R1-S0 — Repository sanitation

**DONE.** Verified full-history backup preceded destructive ref cleanup; stale legacy/process branches and superseded PRs were retired; immutable version tags were preserved.

## R1-S1 — Control plane repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`. The abandoned migration executor/workflow was removed, root `AGENTS.md` was added, and canonical state/docs were synchronized.

## R1-S2 — Trunk rebaseline

**DONE.** The v3 line was promoted to `main` without rewriting history. The reference build and agreed Python, shell, normative, validator-source, and diff-integrity gates passed. Permanent CI remains intentionally absent until the later workflow-restoration block.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

### B3-A — Path-consumer reconciliation

**DONE** via PR #159 at `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`.

### B3-B — Normative process-identity closure

**DONE** via PR #160 at `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`. Obsolete phase/process identity was removed and 172 markers migrated to functional namespaces while preserving rule IDs, expected numeric values, tolerances, proof state, and runtime/API semantics.

### B3-C — Runner/evidence integrity and bounded portability

**DONE.** B3-C1 merged through PR #168 at `da775552be190bf09d8a790c33e9f7f4582da699`; B3-C2 merged through PR #169 at `625e82f9ef4780989d4635e500d72d09eab02992`. Issue #163 is closed.

### B3-D — Operational v1/v2 identity and legacy-code purge

**DONE** at implementation checkpoint `8f7c05b32f228633e4802a6fa8c14babf16fd685`; operational continuity is issue #171.

Completed lots:

- **B3-D1** `c506df5afc16263f797df80b9c2561d5007da9a7` — stale runner identity in catalog-card, research-project and font POC;
- **B3-D2A** `f4d703b34df53868f782598dd9502c0da684c345` — stale V2 diagnostics/gates;
- **B3-D2B** `094b369a077009f212adb33e8a814ee9bb167b4a` — v2-qualified temporary/log producer-consumer identity;
- **B3-D3** `2ad7da8eae03c40fbea3d875843628387ec0e25d` — active package/class identity moved to 3.0.0 and dead distribution runner removed;
- **B3-D4** `456186a7f963c78af3cf00e5f561a616f5072c30` — final v2/V2 runner identity removed;
- **B3-D5** `8f7c05b32f228633e4802a6fa8c14babf16fd685` — dead v2-era release/distribution surface purged (+17/-1129).

Remaining legacy-version references are explicitly classified as certified history, migration contracts, compatibility boundaries, or negative assertions. Distribution is rebuilt later in B5 rather than preserving the dead v2 implementation.

### B3-E — Project-owned oracle terminology

**DONE** via PR #182, squash-merged at `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`. Operational continuity is issue #181.

Fresh remote inventory was produced by a temporary branch-only executor and identified obsolete project-owned `oracle` identity in integration job basenames, checker diagnostics, and validation-contract fields/descriptions. The executor was removed before merge.

Closure evidence:

- 31 implementation files changed exactly once: +31/-31;
- 20 runner job basenames migrated from `textual-oracle-*` / `*-oracle` to functional `validation-*` naming;
- seven checker failure diagnostics migrated from `oracle failed` to `validation failed`;
- table-IBGE producer/consumer key moved together from `oracle_extension` to `validation_extension`;
- table-typography and vector-rule descriptions now use validation/reference terminology;
- post-change exhaustive `git grep` found zero obsolete active project-owned `oracle` occurrences outside explicitly classified control-plane, migration-contract, and negative-test surfaces;
- Python compilation of modified checkers PASS;
- shell syntax for all modified runners PASS;
- modified standards JSON parsing PASS;
- `git diff --check` PASS;
- normative rule IDs, expected numeric values, tolerances, proof state, and runtime/API semantics unchanged;
- no permanent workflow remains.

The B3-E audit also exposed two independent residuals deliberately deferred to B3-F: `tests/checks/repository_contract.py` self-matches its own forbidden path literals, and `tests/integration/font-poc.sh` still contains obsolete `normativa/` / `tests/normativa/` literals.

### B3-F — Final Block 3 residual audit

**ACTIVE / NEXT IMPLEMENTATION WORK.**

B3-F must repair the known residuals above, then run a fresh lightweight live-tree audit covering:

- repository contract and canonical identity checks;
- stale path/consumer references;
- active v1/v2/process identity;
- project-owned `oracle` residue outside classified migration/history/control/negative uses;
- temporary workflow/executor absence;
- producer/consumer integrity for the B3 changes;
- control-plane agreement;
- proportional Python/shell syntax and `git diff --check` only where relevant.

Do not rerun heavyweight LaTeX/PDF/font/distribution certification unless B3-F changes invalidate those gates. B3-F closes R1-BLOCK-3 only if the live tree has no remaining Block 3 residue.

## Non-negotiable rules

The active v3 repository is not an archive. Historical/process evidence belongs to Git history, immutable tags, releases, issues, pull requests, certified SHAs and verified external backups.

Every project-owned technical surface is English. Portuguese is limited to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, and current runtime/upstream identifiers at explicit boundaries. R1 must not rewrite the current Portuguese runtime API; that belongs to R2.

Permanent automatic CI remains absent during structural R1 reconstruction. Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN and full multi-engine certification remain assigned to later R1 blocks.

Do not rerun previously passed gates unless a relevant change invalidates them.

## Remaining R1 blocks

- **R1-B4:** tools, validator, and metadata technical rebaseline.
- **R1-B5:** distribution/public bundle flattening and reproducibility.
- **R1-B6:** permanent cheap/static fail-closed gates.
- **R1-B7:** optimized permanent workflow restoration.
- **R1-B8:** final R1 certification, including Windows/font/PDF-A certification.

## Immediate action

Start **B3-F — final Block 3 residual audit** from canonical remote `main` with latest certified implementation checkpoint `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`. Repair the known repository-contract self-match and stale `font-poc.sh` path literals, run the bounded final residual audit, remove any temporary executor before checkpoint, and close R1-BLOCK-3 only if the audit is clean. Then activate R1-BLOCK-4.
