# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-01

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline**.
- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `7a3b018a43630ed46b375117790acc732ae67b40`.
- R1-BLOCK-3 closure checkpoint: `7a3b018a43630ed46b375117790acc732ae67b40`.
- R1-S2 trunk promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 control-plane closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

The repository was renamed to `abntexto-ufc` on 2026-09-01 without changing repository identity, history, tags, issues, pull requests, or governance. The old repository name is not an active project identity.

`main` is the canonical trunk and merge target. Short-lived task branches are allowed by `AGENTS.md`; phase/stage authority remains the machine state plus this handoff and the engineering roadmap on `main`.

## Completed reconstruction control stages

- **R1-S0 DONE:** verified full-history backup, stale ref/PR sanitation, immutable tags preserved.
- **R1-S1 DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`: abandoned executor/workflow removed; control plane repaired.
- **R1-S2 DONE** at `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`: v3 line promoted to `main` without history rewrite; reference build and agreed promotion gates passed.

Permanent CI remains intentionally absent during structural R1 reconstruction.

## R1-BLOCK-1 — Canonical physical naming

**DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.

## R1-BLOCK-2 — Legacy purge and active-tree minimization

**DONE** at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

## R1-BLOCK-3 — Semantic / Path-Consumer Closure

**DONE** at `7a3b018a43630ed46b375117790acc732ae67b40`.

Block 3 closed the live-tree path, process, runner, evidence, legacy-version, and obsolete project-owned validation terminology debt without changing runtime/API semantics or normative values.

### B3-A — Path-consumer reconciliation

**DONE** via PR #159 at `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`.

### B3-B — Normative process-identity closure

**DONE** via PR #160 at `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`.

- obsolete phase/process identity removed;
- 172 markers migrated to functional namespaces;
- rule IDs, numeric expected values, tolerances, proof state, and runtime/API semantics preserved.

### B3-C — Runner/evidence integrity and bounded portability

**DONE.** B3-C1: PR #168 at `da775552be190bf09d8a790c33e9f7f4582da699`; B3-C2: PR #169 at `625e82f9ef4780989d4635e500d72d09eab02992`.

Eight baseline-equivalent runner/checker defects were closed, including producer/consumer path alignment, Windows UTF-8 handling, Biber job naming, vector calibration, appendix/annex stale process accounting, and the shared vector parser for the footnote separator.

### B3-D — Operational legacy identity and dead-code purge

**DONE** at `8f7c05b32f228633e4802a6fa8c14babf16fd685`; issue #171 closed.

- current package/class identity is 3.0.0;
- stale v1/v2 runner/temp/log/gate identity removed;
- dead v2-era distribution/release implementation purged rather than archived;
- B5 will rebuild distribution from current architecture;
- retained legacy references are classified as certified history, migration contract, compatibility boundary, or negative assertion.

### B3-E — Project-owned oracle terminology

**DONE** via PR #182 at `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`; issue #181 closed.

- 31 implementation files changed exactly 1:1 (+31/-31);
- 20 runner job basenames migrated to functional validation naming;
- seven checker diagnostics migrated to validation terminology;
- table-IBGE producer/consumer binding moved together from `oracle_extension` to `validation_extension`;
- post-change audit found zero obsolete active project-owned `oracle` identity outside classified migration/control/negative surfaces;
- temporary audit workflow removed before merge.

### B3-F — Final Block 3 residual audit

**DONE** via PR #185 at `7a3b018a43630ed46b375117790acc732ae67b40`; issue #184 closed.

Final repairs were intentionally narrow:

- `tests/checks/repository_contract.py` no longer self-matches its own forbidden path literals and explicitly classifies canonical control-plane text;
- `tests/integration/font-poc.sh` uses `tests/documents/${family}-font-poc.tex` and `${family}-font-${engine}-poc`.

Final lightweight audit evidence:

- repository contract PASS: `tracked_files=392 history_directories=0 legacy_class=0`;
- canonical identity PASS: 14 modules aligned;
- control-plane agreement PASS;
- retired v2/N9–N15/B2R active path identities: 0;
- unclassified active project-owned `oracle` occurrences: 0;
- canonical font POC producer/consumer binding PASS;
- relevant Python compilation PASS;
- relevant shell syntax PASS;
- `git diff --check` PASS;
- temporary workflow/executor removed before merge;
- no runtime/API, normative rule/value/tolerance, proof-state, distribution, permanent-CI, font/PDF certification, or R2 behavior change.

## R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline

**ACTIVE / NEXT IMPLEMENTATION WORK.**

B4 is a technical-surface rebaseline, not a runtime/API rewrite. Start with a fresh live-tree inventory of:

- `tools/` developer and certification helpers;
- `validator/` implementation, controls, diagnostics, and technical labels;
- current project-owned metadata and technical prose consumed by tooling;
- orphaned/dead helpers with no current or assigned later-block consumer;
- remaining Portuguese project-owned engineering identifiers/diagnostics on those surfaces;
- stale repository/package metadata that still names the old repository, old version state, or superseded technical architecture.

B4 rules:

- project-owned technical language is English;
- academic/rendered Portuguese data and upstream identifiers at explicit integration boundaries remain untouched;
- no R2 runtime/API migration;
- no B5 distribution implementation;
- no B6 permanent-gate design or B7 workflow restoration;
- no B8 Windows/font/PDF-A final certification;
- delete dead helpers instead of preserving them as historical artifacts;
- preserve normative rule IDs, expected numeric values, tolerances, and proof state;
- use bounded lots and proportional checks; do not rerun heavyweight gates unless a B4 change invalidates them.

B4 closes only when the active tools/validator/metadata surfaces have coherent v3 ownership and English technical identity, dead helpers are removed or explicitly assigned to later blocks, current consumers resolve, and a final bounded residual audit passes.

## Remaining R1 sequence

- **R1-B4 ACTIVE:** tools, validator, metadata technical rebaseline.
- **R1-B5 BLOCKED:** distribution/public bundle flattening and reproducibility.
- **R1-B6 BLOCKED:** permanent cheap/static fail-closed gates.
- **R1-B7 BLOCKED:** optimized permanent workflow restoration.
- **R1-B8 BLOCKED:** final R1 certification, including Windows/font/PDF-A certification.

## Non-negotiable rules

The active v3 repository is not an archive. Historical/process evidence belongs to Git history, immutable tags, releases, issues, pull requests, certified SHAs, and verified external backups.

Every project-owned technical surface is English. Portuguese remains allowed for academic/rendered content, bibliography data, official UFC/ABNT wording, literal output under test, and current runtime/upstream identifiers at explicit boundaries. Runtime/API internationalization is V3-R2.

Do not create permanent automatic CI during structural reconstruction. Do not rerun passed heavyweight gates without a current-state reason.

## Immediate action

Start **R1-BLOCK-4** from canonical remote `main` with implementation checkpoint `7a3b018a43630ed46b375117790acc732ae67b40`. Create an operational B4 issue, inventory `tools/`, `validator/`, and current metadata surfaces, classify each finding by current consumer or assigned later-block owner, then execute bounded cleanup lots without absorbing B5–B8 or R2 work.
