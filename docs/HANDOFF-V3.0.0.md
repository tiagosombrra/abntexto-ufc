# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-08-31

## Checkpoint

- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-3 — Semantic / Path-Consumer Closure**.
- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`.
- R1-S2 trunk promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 control-plane closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

`main` remains the canonical trunk and merge target. Short-lived task branches are permitted by `AGENTS.md`, but canonical phase/stage authority remains in the control-plane files on `main`.

## R1-S0 — Repository sanitation

**DONE.**

- A verified mirror and full-history Git bundle were created before destructive ref cleanup.
- Legacy `1.x`, v2.x, N-phase/N15/B2R, audit, preview, maintenance, release, temporary, and abandoned v3 branches were removed from the active namespace after preservation.
- Pull requests #157 and #158 were closed as superseded by the v3 reconstruction.
- Immutable version tags remain protected and unchanged.
- The steady-state remote development namespace is `main` plus short-lived task branches only.

## R1-S1 — Control plane repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`.

S1 removed the abandoned temporary migration workflow/executor, added root `AGENTS.md`, and synchronized machine state, handoff, and roadmap. The abandoned executor did not produce a certified Block 3 migration checkpoint.

## R1-S2 — Trunk rebaseline

**DONE.**

The v3 line was promoted to `main` without rewriting history.

Verified promotion facts:

- source checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`;
- former certified v2 `main`: `ce659b578b4fc9cc929af4aadc3e613df469ba77`;
- promotion mode: direct fast-forward;
- reference build passed on TeX Live 2026;
- agreed Python, shell, normative, validator-source, and diff-integrity gates passed;
- permanent CI remained intentionally absent;
- the stale `latex-preflight` status requirement remains deferred until R1-BLOCK-7.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

### B3-A — Path-consumer reconciliation

**DONE** via PR #159, merged at `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`.

- stale active project paths and consumers were reconciled;
- producer/consumer path references were normalized to the current repository layout;
- no later-block distribution/CI work was absorbed.

### B3-B — Normative process-identity closure

**DONE** via PR #160, squash-merged at `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`.

B3-B removed obsolete active process identity from validator/scenario/checker/fixture/evidence surfaces while preserving normative semantics.

Verified closure evidence:

- validator phase ownership removed;
- active scenario `phase` metadata/readers removed where obsolete;
- 172 phase-qualified markers migrated to functional namespaces;
- final functional namespaces include `IL` (illustration), `HL` (multiline hanging), `SI` (section indicator), and `SS` (subsection spacing);
- active N6/N9/N10 markers: 0;
- stale active phase diagnostics: 0;
- active lower-case N5–N15 process identities in B3-B scope: 0;
- active legacy `N*-EVIDENCE` labels: 0; `VALIDATION-EVIDENCE` is the shared active label;
- migrated producer/consumer mismatches: 0;
- namespace collisions: 0;
- normative rule IDs changed: 0;
- numeric expected values changed: 0;
- numeric tolerances changed: 0;
- proof state changed: false;
- runtime/API R2 changes: 0;
- B5/B6/B7/B8/control-plane/CI changes in B3-B: 0.

Functional differential validation for B3-B classified 29/29 relevant tests:

- 21 PASS;
- 8 BASELINE_EQUIVALENT_BLOCKED;
- 0 regressions introduced by B3-B;
- 0 unresolved classifications.

### B3-C — Runner/evidence integrity and bounded portability

**NEXT / ACTIVE WORK ITEM.**

Eight pre-existing defects were exposed during B3-B differential validation and remain outside B3-B closure:

1. appendix/annex — undefined `scope` consumer;
2. catalog card — `FileNotFoundError` in runner/file handoff;
3. footnote separator — missing evidence vector;
4. long quotation — Windows path-separator handling;
5. research project — Biber invoked without a generated `.bcf`;
6. short direct citation — CP1252 `UnicodeEncodeError` while emitting evidence;
7. table IBGE vector — missing vector calibration;
8. vector-rule validation — horizontal-tolerance binding drift.

B3-C must repair these as bounded runner-to-file, evidence-to-consumer, or Windows portability defects. It must not rewrite normative values/tolerances or broaden into distribution/CI work.

### Remaining Block 3 sequence

After B3-C:

- **B3-D:** close operational `v2`/`V2` identity in active technical surfaces;
- **B3-E:** close project-owned `oracle` engineering terminology where it is not a legitimate domain/testing term;
- **B3-F:** final live-tree residual audit and Block 3 closure.

Do not broaden Block 3 into CI/distribution reconstruction. Distribution workflows, permanent CI, Overleaf/CTAN, Windows-font certification, PDF/A certification, and heavyweight certification remain later-block work.

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
11. `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04` — B3-A path-consumer reconciliation merged through PR #159.
12. `dbc7f774df2cd0ac1b0f6479653290c6f19b6809` — B3-B normative process-identity closure merged through PR #160.

## Immediate action

Start **B3-C — runner/evidence integrity and bounded portability** from canonical remote `main`. The latest certified clean implementation checkpoint preceding the control-plane synchronization is `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`. Treat the eight known defects above as the initial bounded audit set. Do not repeat B3-B or completed S2 gates unless a B3-C change directly invalidates them.
