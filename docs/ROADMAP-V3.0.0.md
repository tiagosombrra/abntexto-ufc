# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-31

## Status

**V3-R1 ACTIVE — trunk rebaseline closed; semantic/path-consumer closure resumed on `main`.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B3 ACTIVE → R1-B4…B8 BLOCKED → R2+ BLOCKED**

- Active branch: `main`.
- R1-S2 promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Previous certified clean implementation checkpoint before the control rebaseline: `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Authority and bootstrap

Current Git facts and the canonical machine state must agree. `release/v3-roadmap.json` declares intended phase/stage; `docs/HANDOFF-V3.0.0.md` and this roadmap explain that state. `AGENTS.md` defines the mandatory session bootstrap.

If Git, machine state, handoff, roadmap, workflow inventory, or temporary-artifact inventory disagree, advancement fails closed. Memory, historical branches, old PRs, old workflows, and prior chat context are not phase authorities.

## R1-S0 — Repository Sanitation & Control Rebaseline

**DONE.**

- verified Git mirror and full-history bundle created before ref deletion;
- remote branches reduced from 154 to `main` plus the temporary v3 rebaseline branch;
- stale/abandoned audit, v2.x, N-phase/N15/B2R, preview, maintenance, release, temporary, legacy `1.x`, and abandoned v3 refs removed from the active namespace;
- PRs #157 and #158 closed as superseded;
- immutable release tags preserved;
- stable-branch ruleset narrowed to `main` after legacy `1.x` removal.

No archive replacement branches are permitted in the active repository.

## R1-S1 — Control Plane Repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`.

Audit result for `38f21f...` → pre-repair `54dfcb6...`:

- 12 commits ahead, 0 behind;
- no net product migration delta in `standards/`, `tests/`, or `validator/`;
- net changes confined to a temporary workflow, repair script, and control state/docs;
- expected workflow product commit `refactor: reconcile remaining R1 path consumers` absent;
- attempted residual migration therefore not certified as completed.

S1 removed the temporary workflow and repair executor, added `AGENTS.md`, synchronized canonical state/docs, and passed post-publication verification.

## R1-S2 — Trunk Rebaseline

**DONE.**

The v3 line was promoted to `main` by direct fast-forward.

Verified facts:

1. certified v2 `main` baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`;
2. promoted v3 checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`;
3. ancestry immediately before promotion: 95 commits ahead, 0 behind;
4. merge base: exactly the certified v2 baseline;
5. no merge commit, squash, rebase, or history rewrite;
6. reference build passed on TeX Live 2026;
7. agreed syntax, normative, validator-source, and diff-integrity promotion gates passed;
8. permanent CI remained intentionally absent during the structural reconstruction;
9. stale `latex-preflight` protection was removed for the controlled promotion and must remain absent until optimized CI is restored in Block 7.

The temporary `refactor/v3-r1-rebaseline` branch has no continuing development role and is retired during S2 closeout. The intended steady-state development branch is `main`.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

Previously certified checkpoints through `38f21f...` remain useful evidence; the abandoned temporary executor after that checkpoint does not close additional Block 3 work.

Audit the actual current `main` tree and address only residuals that still exist:

- active N-phase/N15/B2R process identity;
- project-owned `oracle` engineering terminology;
- operational v2/V2 identity in active technical surfaces;
- stale producer-consumer references;
- runner-to-file integrity;
- evidence-to-consumer integrity;
- validator/scenario naming and ownership;
- bounded portability issues exposed by current checks, including Windows subprocess encoding where applicable.

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

Continue **R1-BLOCK-3** on `main`. Start from a live-tree residual inventory, close the remaining semantic/path-consumer classes as a bounded set, and do not repeat completed S2 promotion gates without a current-state reason.
