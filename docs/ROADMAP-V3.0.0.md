# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-01

## Status

**V3-R1 ACTIVE — R1-BLOCK-3 remains active; B3-A through B3-E are closed on `main`; B3-F is active.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B3 ACTIVE → R1-B4…B8 BLOCKED → R2+ BLOCKED**

Block 3 internal sequence:

**B3-A DONE → B3-B DONE → B3-C DONE → B3-D DONE → B3-E DONE → B3-F ACTIVE**

- Canonical repository: `tiagosombrra/abntexto-ufc`.
- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`.
- R1-S2 promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

The GitHub repository was renamed to `abntexto-ufc` on 2026-09-01 without changing repository ID, history, tags, issues, pull requests, or governance. The former repository name is not an active technical identity.

## Authority and bootstrap

Current Git facts and the canonical machine state must agree. `release/v3-roadmap.json` declares intended phase/stage; `docs/HANDOFF-V3.0.0.md` and this roadmap explain that state. `AGENTS.md` defines the mandatory session bootstrap.

`main` is the canonical trunk and merge target. If Git, machine state, handoff, roadmap, workflow inventory, or temporary-artifact inventory disagree, advancement fails closed.

## R1-S0 — Repository sanitation and control rebaseline

**DONE.** Verified full-history backup preceded destructive ref cleanup; obsolete development/process refs were retired and immutable release tags preserved.

## R1-S1 — Control plane repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`.

## R1-S2 — Trunk rebaseline

**DONE.** The v3 line was promoted to `main` without history rewrite. Reference build and agreed promotion gates passed. Permanent CI remains intentionally absent until B7.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

### B3-A — Path-consumer reconciliation

**DONE** through PR #159 at `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`.

### B3-B — Normative process-identity closure

**DONE** through PR #160 at `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`. Obsolete phase/process identity was removed; 172 markers migrated to functional namespaces; normative semantics were preserved.

### B3-C — Runner/evidence integrity and bounded portability

**DONE.** PR #168 at `da775552be190bf09d8a790c33e9f7f4582da699` and PR #169 at `625e82f9ef4780989d4635e500d72d09eab02992` closed the eight baseline-equivalent runner/checker defects exposed by B3-B.

### B3-D — Operational legacy identity and dead-code purge

**DONE** at `8f7c05b32f228633e4802a6fa8c14babf16fd685`.

Completed lots D1–D5 removed stale v1/v2 runner/temp/log/gate identity and purged dead release/distribution implementation instead of preserving it as compatibility. Current package/class identity is 3.0.0. Remaining legacy references are explicitly classified as certified history, migration contracts, compatibility boundaries, or negative assertions. Distribution is reconstructed later in B5.

### B3-E — Project-owned oracle terminology

**DONE** via PR #182 at `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`.

A fresh exhaustive branch-only audit located inherited project-owned `oracle` terminology. B3-E then made 31 exact 1:1 changes (+31/-31):

- 20 integration job basenames use functional validation naming;
- seven checker diagnostics use `validation failed` rather than `oracle failed`;
- table-IBGE `oracle_extension` producer/consumer binding is now `validation_extension`;
- typography/vector-rule descriptions use validation/reference terminology.

A temporary executor validated exact replacement counts, checker Python compilation, all modified runner shell syntax, JSON parsing, and `git diff --check`. The executor was removed before PR merge. Exhaustive post-change grep found zero obsolete active project-owned `oracle` identity outside classified control-plane, migration-contract and negative-test occurrences. Rule IDs, numeric expected values, tolerances, proof state, and runtime/API semantics did not change.

### B3-F — Final Block 3 residual audit

**ACTIVE.**

Known entry residue from the B3-E audit:

1. `tests/checks/repository_contract.py` currently self-matches the forbidden path literals it defines, producing false failures for its own negative patterns.
2. `tests/integration/font-poc.sh` still contains obsolete `normativa/` and `tests/normativa/` literals.

B3-F must repair those residues narrowly, then run a fresh lightweight final audit proving:

- repository contract PASS;
- canonical identity PASS;
- no stale active path/consumer references;
- no active v1/V1/v2/V2 or retired process identity;
- no obsolete project-owned `oracle` identity outside classified migration/history/control/negative surfaces;
- no temporary workflow/executor tracked;
- producer/consumer bindings touched by Block 3 remain aligned;
- control-plane documents agree;
- proportional Python/shell syntax and `git diff --check` PASS.

Heavy LaTeX/PDF/font/distribution certification is not rerun unless the B3-F changes invalidate it. R1-BLOCK-3 closes only after this audit is clean.

## Remaining R1 blocks

- **R1-B4:** tools, validator, and metadata technical rebaseline.
- **R1-B5:** distribution/public bundle flattening and reproducibility.
- **R1-B6:** permanent cheap/static fail-closed gates.
- **R1-B7:** optimized permanent workflow restoration.
- **R1-B8:** final clean-tree, repository identity, branch policy, documentation, state, checks, assets, Windows/font and PDF/A certification.

## R1 exit criteria

R1 closes only when a new maintainer or agent can determine current state without reconstructing historical context. Required conditions include no dead legacy/migration artifacts without consumers, no archive/history tree in the active product, no obsolete physical paths or stale references, no generated migration scaffolding, explicit classification of retained legacy references, coherent English project-owned technical surfaces, and agreement among Git facts, roadmap, handoff and machine state.

## Later phases

- **V3-R2:** direct runtime/API internationalization and removal/absorption of Portuguese project API aliases.
- **V3-R3:** standards/tests/language semantic hardening.
- **V3-R4:** certification only.
- **V3-R5:** foundation freeze and current migration/user/maintainer documentation.
- **V3-A1/A2:** article work resumes only against the certified v3 foundation.

## Immediate action

Start **B3-F — final Block 3 residual audit** from canonical remote `main`, using `bf36982ab2ff08b8585c4acc570c48364e9ecc1f` as the latest certified implementation checkpoint. Repair the repository-contract self-match and stale font-POC path literals, execute a bounded final residual audit, remove any temporary audit executor before checkpoint, and close Block 3 only if clean. Then activate R1-BLOCK-4.
