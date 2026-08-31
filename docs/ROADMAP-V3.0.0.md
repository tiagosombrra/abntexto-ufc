# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**V3-R1 ACTIVE — repository control rebaseline before functional continuation.**

Current sequence:

**R1-S0 DONE → R1-S1 ACTIVE → R1-S2 BLOCKED → R1-B3 PAUSED → R1-B4…B8 BLOCKED → R2+ BLOCKED**

- Active branch: `refactor/v3-r1-rebaseline`.
- Observed pre-S1-repair HEAD: `54dfcb6a3a4303c7ecc41a0577c49d4ab2d4a723`.
- Latest certified clean implementation checkpoint: `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6`.
- Certified v2 baseline: `main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Authority and bootstrap

Current Git facts and the canonical machine state must agree. `release/v3-roadmap.json` declares intended phase/stage; `docs/HANDOFF-V3.0.0.md` and this roadmap explain that state. `AGENTS.md` defines the mandatory session bootstrap.

If Git, machine state, handoff, roadmap, workflow inventory, or temporary-artifact inventory disagree, advancement fails closed. Memory, historical branches, old PRs, old workflows, and prior chat context are not phase authorities.

## R1-S0 — Repository Sanitation & Control Rebaseline

**DONE.**

Results:

- full mirror plus verified full-history bundle created before ref deletion;
- remote branches reduced from 154 to exactly `main` plus `refactor/v3-r1-rebaseline`;
- stale/abandoned audit, v2.x, N-phase/N15/B2R, preview, maintenance, release, temporary, legacy `1.x`, and abandoned v3 refs removed from the active namespace;
- PRs #157 and #158 closed as superseded;
- immutable release tags preserved;
- stable-branch ruleset narrowed to `main` after legacy `1.x` removal.

Historical work remains recoverable through Git objects, tags, releases, PRs, and the verified external backup. No `archive/*` replacement branches are permitted in the active repository.

## R1-S1 — Control Plane Repair

**ACTIVE.**

Purpose: make actual Git state, machine state, documentation, workflow inventory, and temporary-artifact inventory describe the same repository.

Findings from `38f21f...` to pre-repair HEAD `54dfcb6...`:

- 12 commits ahead, 0 behind;
- no net product migration delta in `standards/`, `tests/`, or `validator/`;
- net changes are confined to a temporary workflow, its repair script, and control documentation/state;
- the workflow's expected product commit `refactor: reconcile remaining R1 path consumers` does not exist;
- therefore the attempted residual path-consumer migration is not a completed Block 3 checkpoint.

S1 actions:

- remove `.github/workflows/r1-semantic-identity-audit.yml`;
- remove `tools/r1_path_consumers_repair.py`;
- add root `AGENTS.md` with mandatory fail-closed bootstrap;
- synchronize this roadmap, the canonical handoff, and machine state;
- verify after publication that no temporary workflow/executor remains and the repository has exactly the intended two branches.

S1 exit criteria:

- Git × machine state × handoff × roadmap agree;
- zero forgotten temporary workflows/executors;
- active stage and last certified implementation checkpoint are unambiguous;
- the failed/unfinished temporary migration is not represented as completed work.

## R1-S2 — Trunk Rebaseline

**BLOCKED by S1.**

Goal: make v3 the unambiguous repository trunk without rewriting history.

Before promotion:

- confirm v3 ancestry against the certified v2 baseline;
- inspect current `main` protections/status-check requirements;
- run only the minimal current-state gates needed for safe promotion;
- require clean tree, no temporary artifacts, and synchronized control state.

Planned end state:

- `main` becomes current v3 development;
- v2.1 remains recoverable through immutable tag/release history;
- `refactor/v3-r1-rebaseline` is deleted after successful promotion;
- no permanent v2 maintenance branch is retained unless an actual maintenance requirement exists.

## R1 Block 3 — Semantic / Path-Consumer Closure

**PAUSED until S1 and S2 are resolved.**

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

Close R1-S1 by validating the published control checkpoint. Do not resume Block 3 and do not promote v3 to `main` until S1 is verified closed.
