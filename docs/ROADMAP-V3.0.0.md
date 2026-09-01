# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-01

## Status

**V3-R1 ACTIVE — R1-BLOCK-3 remains active; B3-A through B3-D are closed on `main`; B3-E is active.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B3 ACTIVE → R1-B4…B8 BLOCKED → R2+ BLOCKED**

Block 3 internal sequence:

**B3-A DONE → B3-B DONE → B3-C DONE → B3-D DONE → B3-E ACTIVE → B3-F PENDING**

- Canonical repository: `tiagosombrra/abntexto-ufc`.
- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `8f7c05b32f228633e4802a6fa8c14babf16fd685`.
- R1-S2 promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

The GitHub repository was renamed to `abntexto-ufc` on 2026-09-01 without changing repository ID, history, tags, issues, pull requests, or governance. The former repository name is not an active technical identity.

## Authority and bootstrap

Current Git facts and the canonical machine state must agree. `release/v3-roadmap.json` declares intended phase/stage; `docs/HANDOFF-V3.0.0.md` and this roadmap explain that state. `AGENTS.md` defines the mandatory session bootstrap.

`main` is the canonical trunk and merge target. Short-lived task branches are permitted but do not replace `main` as the control-plane `active_branch`.

If Git, machine state, handoff, roadmap, workflow inventory, or temporary-artifact inventory disagree, advancement fails closed. Memory, historical branches, old PRs, old workflows and prior chat context are not phase authorities.

## R1-S0 — Repository sanitation and control rebaseline

**DONE.** Verified mirror/full-history backup preceded destructive ref cleanup. Legacy 1.x/v2.x/process/audit/temporary refs were removed from the active namespace, immutable tags were preserved, stale PRs were closed, and steady-state remote development was reduced to `main` plus short-lived task branches.

## R1-S1 — Control plane repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`. Removed abandoned temporary migration executor/workflow, added root `AGENTS.md`, and synchronized control-plane state.

## R1-S2 — Trunk rebaseline

**DONE.** The v3 line was promoted to `main` by fast-forward without history rewrite. Reference build and agreed promotion gates passed. Permanent CI remains intentionally absent until B7.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

### B3-A — Path-consumer reconciliation

**DONE** through PR #159 at `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`.

### B3-B — Normative process-identity closure

**DONE** through PR #160 at `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`.

Obsolete phase/process identity was removed and 172 markers migrated to functional namespaces. Normative rule IDs, expected numeric values, numeric tolerances, proof state and runtime/API semantics were preserved. Differential validation: 21 PASS, 8 baseline-equivalent pre-existing blocks, 0 introduced regressions, 0 unresolved.

### B3-C — Runner/evidence integrity and bounded portability

**DONE.** PR #168 at `da775552be190bf09d8a790c33e9f7f4582da699` closed six runner/evidence defects; PR #169 at `625e82f9ef4780989d4635e500d72d09eab02992` closed appendix/annex stale scope accounting and footnote vector parsing. Issue #163 is closed. No temporary validation workflow remains.

### B3-D — Operational legacy identity and dead-code purge

**DONE** at `8f7c05b32f228633e4802a6fa8c14babf16fd685`.

B3-D expanded from label cleanup into explicit active-tree legacy purge. Dead/superseded v1/v2-era implementation and tests were removed rather than renamed or archived. Surviving legacy references are permitted only as certified history, migration contracts, compatibility boundaries, or negative tests.

Completed lots:

- **D1** `c506df5afc16263f797df80b9c2561d5007da9a7`: catalog-card, research-project and font-POC runner identity.
- **D2A** `f4d703b34df53868f782598dd9502c0da684c345`: six stale V2 gate/diagnostic labels.
- **D2B** `094b369a077009f212adb33e8a814ee9bb167b4a`: five v2-qualified temp/log producer-consumer paths.
- **D3** `2ad7da8eae03c40fbea3d875843628387ec0e25d`: current package/class identity moved to v3.0.0; dead distribution runner and coordinated gate removed.
- **D4** `456186a7f963c78af3cf00e5f561a616f5072c30`: final active runner v2/V2 identity removed from six current runners.
- **D5** `8f7c05b32f228633e4802a6fa8c14babf16fd685`: obsolete release/distribution implementation purged; 12 files, +17/-1129. Removed stale Make targets, release builder, five release/CTAN/Overleaf checkers, v2 CTAN docs, unused Actions artifact downloader, and stale identity exemptions.

B3-D closure evidence:

- current package/class metadata identifies 3.0.0;
- active product hierarchy has no v1/v2 version-qualified engineering layout;
- current runners have no known v1/v2-qualified temp/log/gate identity;
- dead release/distribution surface is removed instead of preserved as compatibility;
- `README.md` v2.1.0 statement is certified-history context;
- `release/v3-api-migration.json`, `release/v3-path-migration.json`, and `release/v3-test-migration.json` remain explicit migration contracts and do not reference the D5-deleted helpers;
- `canonical_identity.py`, `repository_contract.py`, and the architecture absence statement retain only negative legacy assertions;
- `docs/ctan-example.tex` and `tools/fetch-abntexto.py` are assigned to B5; reference-image tooling remains current; Windows font helper chain is assigned to B8.

### B3-E — Project-owned oracle terminology

**ACTIVE.**

Run a fresh live-tree audit of `oracle` terminology. Replace project-owned engineering `oracle` naming when it is inherited implementation/process identity. Preserve a use only when `oracle` is genuinely the correct testing/theoretical concept.

B3-E invariants:

- no normative rule-ID changes;
- no expected numeric-value changes;
- no numeric-tolerance changes;
- no proof-state changes;
- no runtime/API migration;
- no B5 distribution reconstruction;
- no permanent CI or B8 certification work.

Known historical/advisory examples are not authority and must be re-audited on current `main`; one previously deferred example was the `vector-rule-oracle-calibration` runner/job identity.

### B3-F — Final Block 3 residual audit

**PENDING.** After B3-E, run a fresh live-tree residual audit, verify producer/consumer integrity, control-plane agreement, active-tree minimization and absence of obsolete Block 3 identities. Close R1-BLOCK-3 only if no active Block 3 residue remains.

## Remaining R1 blocks

- **R1-B4:** tools, validator, and metadata technical rebaseline.
- **R1-B5:** distribution/public bundle flattening and reproducibility.
- **R1-B6:** permanent cheap/static fail-closed gates.
- **R1-B7:** optimized permanent workflow restoration.
- **R1-B8:** final clean-tree, repository identity, branch policy, documentation, state, checks, assets, Windows/font and PDF/A certification.

## R1 exit criteria

R1 closes only when a new maintainer or agent can determine current state without reconstructing historical context. Required conditions include no dead legacy or migration artifacts without consumers, no archive/history tree in the active product, no obsolete physical paths or stale references, no generated migration scaffolding, explicit classification of retained legacy references, coherent English project-owned technical surfaces, resolvable build/test/distribution paths at their assigned block, fail-closed static gates, optimized CI, and agreement among Git facts, roadmap, handoff and machine state.

## Later phases

- **V3-R2:** direct runtime/API internationalization and removal/absorption of Portuguese project API aliases.
- **V3-R3:** standards/tests/language semantic hardening.
- **V3-R4:** certification only.
- **V3-R5:** foundation freeze and current migration/user/maintainer documentation.
- **V3-A1/A2:** article work resumes only against the certified v3 foundation.

## Immediate action

Start **B3-E — project-owned oracle terminology cleanup** from canonical remote `main` at certified implementation checkpoint `8f7c05b32f228633e4802a6fa8c14babf16fd685`. Re-audit the live tree, classify every `oracle` occurrence, change obsolete project-owned engineering identity only, preserve legitimate testing/domain terminology and all normative semantics, then proceed to B3-F.
