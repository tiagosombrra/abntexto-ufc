# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-08-30

## Checkpoint

- Phase: **V3-R1 ACTIVE**.
- Active block: **R1 Block 3 — residual path-consumer reconciliation**.
- Branch: `refactor/v3-r1-rebaseline`.
- Latest completed implementation SHA: `e6d7a1ce5864387ba1ccae15d21de78ddd05c2f3`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Non-negotiable clean-tree rule

The active v3 repository is not an archive. Historical/process evidence belongs to Git history, tags, releases, issues, pull requests, and certified SHAs. No history directory, dormant future-feature file, completed campaign ledger, compatibility file, or unused migration artifact remains merely for convenience.

Temporary migration contracts may remain only while directly consumed by R1/R2. Remove or consolidate them when their consumer disappears.

## CI rule

`.github/workflows/` remains absent during structural R1 reconstruction. CI is restored only after permanent static gates and current paths are stable. Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN, and full multi-engine jobs are candidate/certification work, not intermediate-commit work.

## Engineering-language rule

Every project-owned technical surface is English, including validator implementation and technical UI. Portuguese is limited to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, and required upstream identifiers at explicit integration boundaries.

## Closed R1 blocks

- **Block 1 — canonical physical naming:** `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.
- **Block 2 — legacy purge and active-tree minimization:** `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

Block 2 removed v2 handoff/audit/history artifacts, N15/B2R ledgers, deprecated `ufctex.cls`, N9–N12 phase snapshots/checkers, dormant article rule/locator artifacts, N4 campaign ledgers, obsolete N2 reconciliation state, and Portuguese v2 normative engineering documents. Current evidence remains only where a current validator consumes it.

## R1 Block 3 — ACTIVE

Goal: remove stale references and retired engineering terminology from active consumers without performing the R2 runtime API rewrite.

Completed checkpoints:

1. `8d8f7081b123999618d4d6e5ec5009a18ce0a89b` — central normative loaders use `standards/`; current full-contract machinery no longer exposes N3/N4 campaign identity.
2. `4fd0e61ea198ed1307e511895b254c59f5ea0dc4` — negative-path and normative-complement validation use current paths/checkers; N13 campaign identity and duplicate negative-path execution were removed.
3. `e6d7a1ce5864387ba1ccae15d21de78ddd05c2f3` — the reference document build was restored on the canonical topology:
   - `make compile` builds `template/main.tex` from `template/` with repository class inputs resolved through `TEXINPUTS`;
   - `reference-document.sh` consumes `template/main.{log,pdf,toc}` and current integration scripts;
   - `reference_guide_contract.py` and `reference-guide-map.json` use `standards/` and canonical `template/chapters/` paths;
   - reference image downloads target `template/figures/`;
   - stale physical references to the renamed example flow image, example source file, and figure-license file were corrected.

The Makefile development-build portion was pulled forward from the former Block 4 scope because Block 3's reference gate directly depends on it. This does not authorize R2 semantic/API changes; the current class/runtime version remains 2.1.0 until its designated migration.

## Remaining Block 3 work

1. Audit every integration script listed in `tests/run.py` and its direct checker/tool dependencies.
2. Replace remaining `normativa/`, `tests/normativa/`, removed `tests/v2-*`, N-phase, and project-owned `oracle` engineering references.
3. Reconcile remaining stale paths in template guidance, standards evidence, and validator/checker consumers.
4. Verify runner-to-file integrity and evidence-to-consumer integrity.
5. Run permanent repository/static checks when the dependency graph is current.
6. Synchronize this handoff, roadmap, and machine state after each coherent implementation checkpoint.

## Remaining R1 order

4. Remaining tools/validator/metadata technical rebaseline; the development Makefile path is already resolved as a Block 3 prerequisite.
5. Distribution and public bundle flattening.
6. Permanent static gates.
7. Optimized workflow restoration.
8. Repository identity plus exhaustive clean-tree R1 closure.

## Immediate action

Continue through the remaining `tests/run.py` entry points. Do not move to R2 or certify R1 while any known stale active consumer remains.
