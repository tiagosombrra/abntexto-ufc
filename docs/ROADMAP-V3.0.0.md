# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**V3-R1 ACTIVE — repository trunk rebaseline before functional continuation.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 ACTIVE → R1-B3 PAUSED → R1-B4…B8 BLOCKED → R2+ BLOCKED**

- Active branch: `refactor/v3-r1-rebaseline`.
- R1-S1 closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Latest certified clean implementation checkpoint before the control rebaseline: `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6`.
- Certified v2 baseline: `main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Authority and bootstrap

Current Git facts and the canonical machine state must agree. `release/v3-roadmap.json` declares intended phase/stage; `docs/HANDOFF-V3.0.0.md` and this roadmap explain that state. `AGENTS.md` defines the mandatory session bootstrap.

If Git, machine state, handoff, roadmap, workflow inventory, or temporary-artifact inventory disagree, advancement fails closed. Memory, historical branches, old PRs, old workflows, and prior chat context are not phase authorities.

## R1-S0 — Repository Sanitation & Control Rebaseline

**DONE.**

- verified Git mirror and full-history bundle created before ref deletion;
- remote branches reduced from 154 to exactly `main` plus `refactor/v3-r1-rebaseline`;
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

S1 removed the temporary workflow and repair executor, added `AGENTS.md`, synchronized canonical state/docs, and passed post-publication verification: exactly two remote branches, no open PRs, no temporary workflow, and no temporary executor.

## R1-S2 — Trunk Rebaseline

**ACTIVE.**

Goal: make v3 the unambiguous repository trunk while preserving ancestry and release history.

Required sequence:

1. confirm v3 is a descendant of the certified v2 `main` baseline;
2. inspect `main` ruleset/protection and required status checks;
3. run only minimal current-state gates needed for promotion safety;
4. require clean control state and zero temporary artifacts;
5. perform a controlled history-preserving promotion to `main`;
6. verify the resulting `main` HEAD and repository default branch;
7. delete `refactor/v3-r1-rebaseline` after successful promotion;
8. verify the steady-state branch namespace.

Planned end state:

- `main` = current v3 development;
- v2.1 recoverable through immutable version tags, GitHub Releases, Git history, and verified external backup;
- no permanent v2 maintenance branch unless a real maintenance requirement exists.

## R1 Block 3 — Semantic / Path-Consumer Closure

**PAUSED until S2 closes.**

Previously certified checkpoints remain valid through `38f21f...`; the abandoned temporary executor after that checkpoint does not close additional Block 3 work.

When Block 3 resumes, audit the actual then-current tree and address only residuals that still exist:

- active N-phase/N15/B2R process identity;
- project-owned `oracle` engineering terminology;
- operational v2/V2 identity in active technical surfaces;
- stale producer-consumer references;
- runner-to-file integrity;
- evidence-to-consumer integrity;
- validator/scenario naming and ownership.

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

Complete R1-S2 and verify trunk promotion. Do not resume Block 3 until `main` is the unambiguous v3 trunk and the temporary rebaseline branch has been retired.
