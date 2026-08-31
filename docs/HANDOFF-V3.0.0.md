# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-08-31

## Checkpoint

- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-3 — Semantic / Path-Consumer Closure**.
- Active branch: `main`.
- R1-S2 trunk promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 control-plane closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Previous certified clean implementation checkpoint before the control rebaseline: `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## R1-S0 — Repository sanitation

**DONE.**

- A verified mirror and full-history Git bundle were created before destructive ref cleanup.
- The remote branch namespace was reduced from 154 branches to `main` and the temporary v3 rebaseline branch.
- Legacy `1.x`, v2.x, N-phase/N15/B2R, audit, preview, maintenance, release, temporary, and abandoned v3 branches were removed from the active namespace after preservation.
- Pull requests #157 and #158 were closed as superseded by the v3 reconstruction.
- Immutable version tags remain protected and unchanged.

## R1-S1 — Control plane repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`.

The audit of `38f21f...` through pre-repair HEAD `54dfcb6...` established that the 12 intervening commits did not leave a product migration delta in `standards/`, `tests/`, or `validator/`. Their net delta was limited to a temporary workflow, its repair script, and control documentation/state.

The workflow expected to create `refactor: reconcile remaining R1 path consumers`, but no such commit exists. Therefore that attempted migration is not a completed Block 3 checkpoint.

S1 removed `.github/workflows/r1-semantic-identity-audit.yml` and `tools/r1_path_consumers_repair.py`, added root `AGENTS.md`, and synchronized machine state, handoff, and roadmap.

## R1-S2 — Trunk rebaseline

**DONE.**

The v3 line was promoted to `main` without rewriting history.

Verified promotion facts:

- source checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`;
- former `main`: `ce659b578b4fc9cc929af4aadc3e613df469ba77`;
- ancestry at promotion: 95 commits ahead, 0 behind;
- merge base: exactly the former `main` SHA;
- operation: direct fast-forward `ce659b5... -> d7d4b9d...`;
- no merge commit, squash, rebase, or history rewrite;
- reference build passed on TeX Live 2026;
- agreed Python, shell, normative, validator-source, and diff-integrity gates passed;
- no temporary migration executor or temporary workflow remained at the promotion checkpoint.

The stable-branch ruleset was temporarily reduced to deletion protection, non-fast-forward protection, and linear-history enforcement so the history-preserving fast-forward could occur. The stale `latex-preflight` requirement must not be restored before optimized CI returns in R1-BLOCK-7.

The temporary `refactor/v3-r1-rebaseline` branch was retired during S2 closeout. The steady-state active development branch namespace is `main` only.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

Resume from an audit of the actual `main` tree. Do not infer that the abandoned S1 executor completed residual migration work.

Known residual classes to evaluate in Block 3 include:

- active N-phase/N15/B2R process identity;
- project-owned `oracle` engineering terminology;
- operational v2/V2 identity in active technical surfaces;
- stale producer-consumer references;
- runner-to-file integrity;
- evidence-to-consumer integrity;
- validator/scenario naming and ownership;
- Windows/Python subprocess encoding portability findings observed during S2, where still relevant.

Do not broaden Block 3 into CI/distribution reconstruction. Distribution workflows, permanent CI, and heavyweight certification remain later-block work.

## Non-negotiable rules

The active v3 repository is not an archive. Historical/process evidence belongs to Git history, immutable tags, releases, issues, pull requests, certified SHAs, and verified external backups.

Every project-owned technical surface is English. Portuguese is limited to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, and current runtime/upstream identifiers at explicit boundaries. R1 must not rewrite the current Portuguese runtime API; that belongs to R2.

Permanent automatic CI remains absent during structural R1 reconstruction. Temporary executors must be removed before checkpoint. Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs remain candidate/certification work.

Do not rerun completed checks unless the current state or a relevant change justifies it.

## Previously closed R1 implementation blocks

- **Block 1 — canonical physical naming:** `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.
- **Block 2 — legacy purge and active-tree minimization:** `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

## Certified Block 3 checkpoints before the control rebaseline

1. `8d8f7081b123999618d4d6e5ec5009a18ce0a89b` — central normative loaders use `standards/`.
2. `4fd0e61ea198ed1307e511895b254c59f5ea0dc4` — negative-path and normative-complement consumers use current paths/checkers.
3. `e6d7a1ce5864387ba1ccae15d21de78ddd05c2f3` — canonical reference-document build restored on `template/`.
4. `1b6db7598d69a6a0d8442d09e589fa8d2e151477` — layout/font/PDF/locator gates reconnected.
5. `d4a348c6bb1600f0fc616c1ce23c1636db606097` — PDF validator/PDF-A gates target `template/main.pdf`.
6. `1cd88899bd25592944e37042419aa146e39c1de6` — front matter rebaselined end-to-end.
7. `66c1005f326ee6523e420165ddb9de595ef49d3d` — test-migration contract reconciled.
8. `bde108b7ff0076605643e870ae7cd86ce69a7e76` — standards consumers and generated-bytecode hygiene reconciled.
9. `91424aab55b08d0931654cd895db9ac7925ca15c` — validation ownership normalized to current runner IDs.
10. `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6` — prior one-shot workflow scaffolding removed; latest certified clean implementation checkpoint before S0/S1.

## Immediate action

Continue **R1-BLOCK-3** on `main` with a live-tree residual audit. Do not repeat already completed S2 promotion gates unless a current change justifies them. Keep distribution/CI reconstruction in their assigned later blocks.
