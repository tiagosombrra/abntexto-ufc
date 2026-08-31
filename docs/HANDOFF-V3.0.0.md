# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-08-30

## Checkpoint

- Phase: **V3-R1 ACTIVE**.
- Active control stage: **R1-S1 — Control Plane Repair**.
- Functional R1 Block 3 work is paused until S1 closes and S2 trunk rebaseline is decided.
- Active branch: `refactor/v3-r1-rebaseline`.
- Observed pre-repair HEAD: `54dfcb6a3a4303c7ecc41a0577c49d4ab2d4a723`.
- Latest certified clean checkpoint before the control repair: `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Repository sanitation status

**R1-S0 is complete.**

- A verified mirror and full-history Git bundle were created before destructive ref cleanup.
- The remote branch namespace was reduced from 154 branches to exactly two: `main` and `refactor/v3-r1-rebaseline`.
- Legacy `1.x`, v2.x, N-phase/N15/B2R, audit, preview, maintenance, release, temporary, and abandoned v3 branches were removed from the active repository namespace after preservation.
- Pull requests #157 and #158 were closed as superseded by the v3 reconstruction.
- Immutable version tags remain protected and unchanged.
- `main` remains protected by the stable-branch ruleset.

## Control-plane findings

The old clean checkpoint `38f21f...` is 12 commits behind the observed pre-repair HEAD `54dfcb6...`.

Those 12 commits do not leave a product migration delta in `standards/`, `tests/`, or `validator/`. The net delta from `38f21f...` to `54dfcb6...` is limited to:

- `.github/workflows/r1-semantic-identity-audit.yml`;
- `tools/r1_path_consumers_repair.py`;
- `docs/HANDOFF-V3.0.0.md`;
- `docs/ROADMAP-V3.0.0.md`;
- `release/v3-roadmap.json`.

The temporary workflow was intended to produce a commit named `refactor: reconcile remaining R1 path consumers`, but no such commit exists. Therefore the intended residual path-consumer migration is **not certified as completed**.

The temporary workflow and repair script are being removed as abandoned control scaffolding during S1. They must not be interpreted as completed Block 3 implementation.

## Non-negotiable rules

The active v3 repository is not an archive. Historical/process evidence belongs to Git history, immutable tags, releases, issues, pull requests, certified SHAs, and verified external backups.

Every project-owned technical surface is English. Portuguese is limited to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, and current runtime/upstream identifiers at explicit boundaries. R1 must not rewrite the current Portuguese runtime API; that belongs to R2.

Permanent automatic CI remains absent during structural R1 reconstruction. A temporary executor may exist only for a bounded operation and must be removed before its checkpoint. Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs remain candidate/certification work.

## Previously closed R1 implementation blocks

- **Block 1 — canonical physical naming:** `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.
- **Block 2 — legacy purge and active-tree minimization:** `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

## Certified Block 3 checkpoints before control rebaseline

1. `8d8f7081b123999618d4d6e5ec5009a18ce0a89b` — central normative loaders use `standards/`.
2. `4fd0e61ea198ed1307e511895b254c59f5ea0dc4` — negative-path and normative-complement consumers use current paths/checkers.
3. `e6d7a1ce5864387ba1ccae15d21de78ddd05c2f3` — canonical reference-document build restored on `template/`.
4. `1b6db7598d69a6a0d8442d09e589fa8d2e151477` — layout/font/PDF/locator gates reconnected.
5. `d4a348c6bb1600f0fc616c1ce23c1636db606097` — PDF validator/PDF-A gates target `template/main.pdf`.
6. `1cd88899bd25592944e37042419aa146e39c1de6` — front matter rebaselined end-to-end.
7. `66c1005f326ee6523e420165ddb9de595ef49d3d` — test-migration contract reconciled.
8. `bde108b7ff0076605643e870ae7cd86ce69a7e76` — standards consumers and generated-bytecode hygiene reconciled.
9. `91424aab55b08d0931654cd895db9ac7925ca15c` — validation ownership normalized to current runner IDs.
10. `38f21f0271d67fa99ef2e6bf1e91b122ac61daf6` — prior one-shot workflow scaffolding removed; this remains the latest certified clean implementation checkpoint before S1.

## Immediate action

Finish **R1-S1** by verifying that Git, `release/v3-roadmap.json`, this handoff, the engineering roadmap, workflow inventory, and temporary-artifact inventory agree after the control repair.

Then perform **R1-S2 — Trunk Rebaseline** planning and minimal validation before any promotion of v3 to `main`.

Only after S1/S2 may Block 3 resume. When it resumes, audit the actual current tree first and migrate only residual N-phase/N15/B2R/`oracle`/operational-v2 engineering identity that still exists. Do not assume the abandoned temporary executor completed that work.
