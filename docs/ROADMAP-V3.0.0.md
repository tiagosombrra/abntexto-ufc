# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-31

## Status

**V3-R1 ACTIVE — R1-BLOCK-3 remains active; B3-A and B3-B are closed on `main`; B3-C is next.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B3 ACTIVE → R1-B4…B8 BLOCKED → R2+ BLOCKED**

Block 3 internal sequence:

**B3-A DONE → B3-B DONE → B3-C NEXT → B3-D PENDING → B3-E PENDING → B3-F PENDING**

- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`.
- R1-S2 promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Authority and bootstrap

Current Git facts and the canonical machine state must agree. `release/v3-roadmap.json` declares intended phase/stage; `docs/HANDOFF-V3.0.0.md` and this roadmap explain that state. `AGENTS.md` defines the mandatory session bootstrap.

`main` is the canonical trunk and merge target. Short-lived task branches are permitted, but they do not replace `main` as the control-plane `active_branch`.

If Git, machine state, handoff, roadmap, workflow inventory, or temporary-artifact inventory disagree, advancement fails closed. Memory, historical branches, old PRs, old workflows, and prior chat context are not phase authorities.

## R1-S0 — Repository Sanitation & Control Rebaseline

**DONE.**

- verified Git mirror and full-history bundle created before ref deletion;
- stale/abandoned audit, v2.x, N-phase/N15/B2R, preview, maintenance, release, temporary, legacy `1.x`, and abandoned v3 refs removed from the active namespace;
- PRs #157 and #158 closed as superseded;
- immutable release tags preserved;
- active branch governance reduced to `main` plus short-lived task branches.

No archive replacement branches are permitted in the active repository.

## R1-S1 — Control Plane Repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`.

The abandoned temporary migration workflow/executor was removed, root `AGENTS.md` was added, and canonical state/docs were synchronized. The abandoned executor did not certify additional Block 3 implementation work.

## R1-S2 — Trunk Rebaseline

**DONE.**

The v3 line was promoted to `main` by direct fast-forward without rewriting history. Reference build and agreed promotion gates passed; permanent CI remained intentionally absent. The stale `latex-preflight` requirement remains deferred until Block 7.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

### B3-A — Path-consumer reconciliation

**DONE** through PR #159 at `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`.

This lot reconciled stale active paths and producer/consumer path references without absorbing later distribution or CI work.

### B3-B — Normative process-identity closure

**DONE** through PR #160 at `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`.

Closure evidence:

- obsolete validator/scenario phase ownership removed;
- obsolete active phase-qualified marker/process identity removed;
- 172 markers migrated to functional namespaces;
- active N6/N9/N10 markers: 0;
- stale active phase diagnostics: 0;
- active lower-case N5–N15 process identity in B3-B scope: 0;
- active legacy `N*-EVIDENCE` labels: 0;
- producer/consumer mismatches: 0;
- marker namespace collisions: 0;
- rule IDs, numeric expected values, numeric tolerances, proof state, and runtime/API semantics preserved.

Functional differential validation classified 29/29 relevant tests: 21 PASS, 8 baseline-equivalent pre-existing blocks, 0 introduced regressions, and 0 unresolved classifications.

### B3-C — Runner/evidence integrity and bounded portability

**NEXT.**

Initial bounded defect set, discovered during B3-B differential validation:

1. appendix/annex — undefined `scope`;
2. catalog card — runner/file `FileNotFoundError`;
3. footnote separator — missing evidence vector;
4. long quotation — Windows path-separator handling;
5. research project — Biber invoked without `.bcf`;
6. short direct citation — CP1252 `UnicodeEncodeError`;
7. table IBGE vector — missing vector calibration;
8. vector-rule validation — horizontal-tolerance binding drift.

B3-C owns runner-to-file integrity, evidence-to-consumer integrity, and bounded Windows/Python portability for these defects. It must not silently change normative values or tolerances.

### B3-D — Operational v2/V2 identity

**PENDING.**

Close stale operational `v2`/`V2` identity only where it remains active technical identity. Preserve legitimate historical/negative references and do not rewrite runtime API boundaries assigned to R2.

### B3-E — Project-owned oracle terminology

**PENDING.**

Replace project-owned engineering `oracle` terminology where it represents obsolete implementation naming. Preserve legitimate theoretical/testing uses of the term.

### B3-F — Final Block 3 residual audit

**PENDING.**

Run a live-tree residual audit after B3-C/D/E, verify producer/consumer integrity and control-plane agreement, and close R1-BLOCK-3 only if no active Block 3 residue remains.

Do not absorb later-block responsibilities into B3. Distribution/public bundle reconstruction, permanent CI, Overleaf/CTAN, Windows-font certification, PDF/A certification, and other heavyweight surfaces stay in their assigned later blocks.

R1 must not rewrite the Portuguese runtime API; that belongs to R2.

## Remaining R1 blocks

- **R1-B4:** tools, validator, and metadata technical rebaseline.
- **R1-B5:** distribution/public bundle flattening and reproducibility.
- **R1-B6:** permanent cheap/static fail-closed gates.
- **R1-B7:** optimized permanent workflow restoration; temporary executor lifecycle is create → execute → validate → delete within one checkpoint.
- **R1-B8:** final clean-tree, repository identity, branch policy, documentation, state, checks, and asset certification.

## R1 exit criteria

R1 closes only when a new maintainer or agent can open the repository and determine the current state without reconstructing historical context.

Required conditions include:

- no historical/process artifact competing with active state;
- no dead migration artifact without an active consumer;
- no archive/history tree in the active product repository;
- zero obsolete physical paths and stale active references;
- zero generated or temporary migration scaffolding;
- project-owned technical surfaces follow the engineering-language policy;
- canonical build/tool/test/distribution paths resolve;
- static gates pass;
- optimized CI cannot spam intermediate commits;
- branch policy, roadmap, machine state, and handoff agree.

## Later phases

- **V3-R2:** direct runtime/API internationalization and removal/absorption of Portuguese project API aliases.
- **V3-R3:** standards/tests/language semantic hardening.
- **V3-R4:** certification only.
- **V3-R5:** foundation freeze and current migration/user/maintainer documentation only.
- **V3-A1/A2:** article work returns only against the certified v3 foundation.
- Later H1/RC/FINAL/CLEANUP phases follow in order.

## Immediate action

Start **B3-C — runner/evidence integrity and bounded portability** from canonical remote `main`. The latest certified clean implementation checkpoint preceding the control-plane synchronization is `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`. Audit and repair only the eight known defects above first, using proportional validation and preserving normative semantics. Do not repeat B3-B or completed S2 gates unless a B3-C change directly invalidates them.
