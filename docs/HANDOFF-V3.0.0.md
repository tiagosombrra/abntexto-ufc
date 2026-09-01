# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-01

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-3 — Semantic / Path-Consumer Closure**.
- Active Block 3 work item: **B3-E — Project-owned oracle terminology cleanup**.
- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `8f7c05b32f228633e4802a6fa8c14babf16fd685`.
- R1-S2 trunk promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 control-plane closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

The GitHub repository was renamed to `abntexto-ufc` on 2026-09-01 without changing repository ID, history, `main`, tags, issues, pull requests, or governance. The old repository name is not an active project identity and must not be reintroduced into project-owned technical surfaces.

`main` is the canonical trunk and merge target. Short-lived task branches are permitted by `AGENTS.md`, but canonical phase/stage authority remains in the control-plane files on `main`.

## R1-S0 — Repository sanitation

**DONE.**

- verified mirror and full-history Git bundle created before destructive ref cleanup;
- legacy `1.x`, v2.x, N-phase/N15/B2R, audit, preview, maintenance, release, temporary and abandoned v3 branches removed from the active namespace after preservation;
- PRs #157 and #158 closed as superseded;
- immutable version tags preserved;
- steady-state remote namespace reduced to `main` plus short-lived task branches.

## R1-S1 — Control plane repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`.

S1 removed the abandoned temporary migration workflow/executor, added root `AGENTS.md`, and synchronized machine state, handoff, and roadmap. The abandoned executor did not certify additional Block 3 migration work.

## R1-S2 — Trunk rebaseline

**DONE.** The v3 line was promoted to `main` without rewriting history. The reference build and agreed Python, shell, normative, validator-source, and diff-integrity gates passed. Permanent CI remains intentionally absent until the later workflow-restoration block.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

### B3-A — Path-consumer reconciliation

**DONE** via PR #159 at `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`.

### B3-B — Normative process-identity closure

**DONE** via PR #160 at `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`.

Closure preserved normative rule IDs, numeric expected values, numeric tolerances, proof state, and runtime/API semantics while removing obsolete phase/process identity. The 172 migrated markers use functional namespaces. Differential validation classified 29/29 relevant tests: 21 PASS, 8 baseline-equivalent pre-existing blocks, 0 introduced regressions, 0 unresolved classifications.

### B3-C — Runner/evidence integrity and bounded portability

**DONE.**

- B3-C1 via PR #168 at `da775552be190bf09d8a790c33e9f7f4582da699`: catalog-card handoff, long-quotation evidence path, research-project job/Biber naming, short-direct-citation UTF-8, vector-rule tolerance binding, table-IBGE vector calibration.
- B3-C2 via PR #169 at `625e82f9ef4780989d4635e500d72d09eab02992`: appendix/annex stale `scope` accounting removed and footnote separator migrated to the shared vector parser with normative values/tolerances preserved.
- Issue #163 is closed. No temporary validation workflow remains.

### B3-D — Operational v1/v2 identity and legacy-code purge

**DONE** at implementation checkpoint `8f7c05b32f228633e4802a6fa8c14babf16fd685`. Operational continuity is issue #171.

Completed bounded lots:

- **B3-D1** — stale runner identity removed from catalog-card, research-project and font POC; merged at `c506df5afc16263f797df80b9c2561d5007da9a7`.
- **B3-D2A** — stale `V2` diagnostic/gate labels removed from six runners; merged at `f4d703b34df53868f782598dd9502c0da684c345`.
- **B3-D2B** — stale v2-qualified temp/log identity removed from five runners with producer/consumer paths moved together; merged at `094b369a077009f212adb33e8a814ee9bb167b4a`.
- **B3-D3** — active package/class version identity moved from 2.1.0 to 3.0.0; dead 281-line `tests/integration/distribution.sh` and its coordinated gate removed; merged at `2ad7da8eae03c40fbea3d875843628387ec0e25d`.
- **B3-D4** — final active v2/V2 runner identity removed from reference-corpus, bibliography, references-6023, object, backmatter and profile-matrix; merged at `456186a7f963c78af3cf00e5f561a616f5072c30`.
- **B3-D5** — dead v2-era distribution/publication surface purged; merged at `8f7c05b32f228633e4802a6fa8c14babf16fd685`. Removed obsolete package/distribution Make targets, old release builder, five stale release/CTAN/Overleaf checkers, v2 CTAN README/changelog, unused Actions artifact downloader, and stale identity-check exemptions. Footprint: 12 files, +17/-1129.

B3-D closure classification:

- **certified history:** README/public baseline statements, certified v2 SHA, explicit historical v2 lineage comments;
- **migration contracts:** `release/v3-api-migration.json`, `release/v3-path-migration.json`, `release/v3-test-migration.json`;
- **negative tests/assertions:** `tests/checks/canonical_identity.py`, `tests/checks/repository_contract.py`, and the architecture statement proving `ufctex.cls` is absent;
- **assigned future/current helpers:** `docs/ctan-example.tex` and `tools/fetch-abntexto.py` are B5 inputs; `tools/fetch-reference-images.py` is current; `tools/prepare-windows-fonts.ps1` plus `tools/convert-encoding-to-unicode.ps1` are the B8 Windows/font helper chain.

The three migration contracts were checked for references to the D5-deleted release helpers; none were found. No active v1/v2 product hierarchy remains. Current runners no longer use v1/v2-qualified temp/log/gate identity. Dead distribution code is not retained as a museum or compatibility layer.

### B3-E — Project-owned oracle terminology

**ACTIVE / NEXT IMPLEMENTATION WORK.**

Perform a fresh live-tree inventory of project-owned `oracle` terminology. Replace obsolete engineering naming with functional validation/evidence terminology. Preserve only legitimate theoretical/testing uses where `oracle` actually describes the testing concept rather than inherited project identity.

Do not change normative rule IDs, expected values, tolerances, proof state, runtime/API behavior, B5 distribution work, or later certification scope.

### B3-F — Final Block 3 residual audit

**PENDING.** After B3-E, audit the live tree for remaining Block 3 residue, producer/consumer integrity and control-plane agreement. Close Block 3 only if no active semantic/path/identity residue remains.

## Non-negotiable rules

The active v3 repository is not an archive. Historical/process evidence belongs to Git history, immutable tags, releases, issues, pull requests, certified SHAs and verified external backups.

Every project-owned technical surface is English. Portuguese is limited to academic/rendered content, bibliography data, official UFC/ABNT wording, literal Portuguese output under test, and current runtime/upstream identifiers at explicit boundaries. R1 must not rewrite the current Portuguese runtime API; that belongs to R2.

Permanent automatic CI remains absent during structural R1 reconstruction. Heavy Windows/font, Overleaf, PDF/A, distribution/CTAN and full multi-engine certification remain assigned to later R1 blocks.

Do not rerun previously passed gates unless a relevant change invalidates them.

## Remaining R1 blocks

- **R1-B4:** tools, validator, and metadata technical rebaseline.
- **R1-B5:** distribution/public bundle flattening and reproducibility.
- **R1-B6:** permanent cheap/static fail-closed gates.
- **R1-B7:** optimized permanent workflow restoration.
- **R1-B8:** final R1 certification, including Windows/font/PDF-A certification.

## Immediate action

Start **B3-E — project-owned oracle terminology cleanup** from canonical remote `main` at implementation checkpoint `8f7c05b32f228633e4802a6fa8c14babf16fd685`. Build a fresh inventory, classify each occurrence as obsolete project-owned engineering identity or legitimate testing/domain terminology, change only the obsolete project-owned identity, preserve normative semantics, then proceed to B3-F final Block 3 residual closure.
