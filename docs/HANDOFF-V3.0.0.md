# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-01

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline**.
- Active B4 work item: **B4-B — stale identity / metadata residual audit and cleanup**.
- Active branch/trunk: `main`.
- B4 operational issue: **#187**.
- Latest certified clean implementation checkpoint: **`a4fbbdcb381709cb542c8f991ef152d8a635f790`**.
- R1-BLOCK-3 closure checkpoint: `7a3b018a43630ed46b375117790acc732ae67b40`.
- R1-S2 promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

`main` is the canonical source of truth and merge target. Short-lived branches are implementation vehicles only. Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree; disagreement fails closed.

## Completed reconstruction stages

- **R1-S0 DONE:** repository sanitation, verified full-history backup, obsolete refs/PRs retired, immutable version tags preserved.
- **R1-S1 DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`: control plane repair.
- **R1-S2 DONE** at `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`: v3 promoted to `main` without history rewrite; reference build and agreed promotion gates passed.
- **R1-BLOCK-1 DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`: canonical physical naming.
- **R1-BLOCK-2 DONE** at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`: legacy purge and active-tree minimization.
- **R1-BLOCK-3 DONE** at `7a3b018a43630ed46b375117790acc732ae67b40`: semantic/path-consumer closure.

Permanent CI remains intentionally absent during structural R1 reconstruction.

## R1-BLOCK-3 summary

**DONE.** Block 3 closed path/process identity, runner/evidence defects, v1/v2 operational identity, dead distribution-era code, obsolete project-owned `oracle` terminology, and final residual path/contract defects.

Key checkpoints:

- B3-A PR #159 — `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`;
- B3-B PR #160 — `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`;
- B3-C final closure PR #169 — `625e82f9ef4780989d4635e500d72d09eab02992`;
- B3-D legacy/dead-code purge — `8f7c05b32f228633e4802a6fa8c14babf16fd685`;
- B3-E PR #182 — `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`;
- B3-F PR #185 — `7a3b018a43630ed46b375117790acc732ae67b40`.

Final B3 evidence included repository contract PASS, 14 canonical modules aligned, zero retired v2/N9–N15/B2R active paths, zero unclassified active project-owned `oracle` occurrences, relevant syntax/diff checks PASS, and no temporary workflow retained.

## R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline

**ACTIVE.** Operational continuity: issue #187.

B4 owns current technical surfaces in `tools/`, `validator/`, and metadata consumed by them. It does not own R2 runtime/API migration, B5 distribution implementation, B6 permanent gates, B7 workflow restoration, or B8 final Windows/font/PDF-A certification.

### Entry inventory

Remote run `33496512650` established the initial consumer matrix. Inventory/stale-identity steps passed; the overall run failed only because `validator_source.py` exposed `spine.conditional` as an extension without unified executable evidence.

Observed ownership:

- `fetch-abntexto.py` has no current textual consumer but is explicitly an upstream `abntexto` pin/fetch helper for Overleaf/public bundle construction: **classified B5-owned**, retained for B5 unless B5 supersedes it.
- `prepare-windows-fonts.ps1` and `convert-encoding-to-unicode.ps1` form a live Windows-font preparation chain consumed by `abntexto-ufc/fonts.def`: **classified B8-owned**.
- normative contract/measurement helpers are live validator/test infrastructure.
- `validate-ufc-pdf.py` has eight live consumers.
- all four files under `validator/` have live consumers and are current product surfaces.

No old repository-name identity was found in the audited B4 surfaces.

### B4-A — Inventory blockers and ownership classification

**DONE** through PR #189, squash-merged at **`a4fbbdcb381709cb542c8f991ef152d8a635f790`**.

The entry defect was a validator-contract semantics problem, not a normative-rule defect. `spine.conditional` is the only full-contract rule with `validation.mode = not-applicable`; for the electronic package it must not pretend to have executable evidence.

B4-A changes:

- `spine.conditional` keeps the same rule ID, requirement, locator, normativity, sources, values and `printed_spine` applicability, while its validation checks become empty;
- `tools/normative_full.py` now fails closed: `not-applicable` requires an empty checks list and explicit applicability; every executable validation mode still requires non-empty checks;
- `normative_full_contract.py`, `normative_traceability.py`, and `normative_coverage.py` share that distinction;
- stale `distribution-source` evidence ID was removed from the distribution policy; live `build-path` evidence remains and distribution implementation stays B5-owned;
- reference-image User-Agent changed from `abntexto-ufc/2.1.0` to `abntexto-ufc/3.0.0`;
- validator project identity changed from inherited `ufctex` to `abntexto-ufc · standalone validator`.

Remote validation was deliberately fail-closed:

- run `33498491307` exposed the traceability assumption;
- run `33498624481` exposed the coverage assumption and remaining dead evidence ID;
- run **`33498811794` PASS** after complete reconciliation.

Final B4-A gate covered Python compilation, standards JSON parsing, `normative_full_contract.py`, full `validator_source.py`, JS syntax, explicit invariants for `spine.conditional`, current identity assertions, and `git diff --check`. Temporary validation workflow was removed before PR merge. No runtime/API, proof-state, rule-ID, expected numeric value or tolerance changed.

### B4-B — Stale identity and metadata cleanup

**ACTIVE / NEXT.** Two entry identities were already repaired in B4-A (`2.1.0` User-Agent and `ufctex` validator branding). B4-B now performs a fresh residual audit across project/package/version/repository/ownership metadata and removes only stale active technical identity. Historical, migration, B5/B8 and negative-test references remain classified rather than blindly rewritten.

### B4-C — Validator/tool technical-language rebaseline

**PENDING.** Separate project-owned engineering diagnostics/labels from legitimate Portuguese document/runtime surfaces before editing. Academic/rendered Portuguese, official UFC/ABNT wording, literal output under test and current Portuguese runtime/API identifiers remain allowed boundaries; the runtime API itself moves only in R2.

### B4-D — Final B4 residual audit/closeout

**PENDING.** Require all helpers classified, no dead helper retained, all live consumers resolving, validator/tool source checks PASS, temporary workflows absent, and canonical docs/machine state synchronized.

## Remaining R1 sequence

- **R1-B4 ACTIVE** — tools/validator/metadata rebaseline.
- **R1-B5 BLOCKED** — distribution/public bundle flattening and reproducibility.
- **R1-B6 BLOCKED** — permanent cheap/static fail-closed gates.
- **R1-B7 BLOCKED** — optimized permanent workflow restoration.
- **R1-B8 BLOCKED** — final R1 certification including Windows/font/PDF-A.

## Immediate action

Start B4-B from canonical remote `main` using `a4fbbdcb381709cb542c8f991ef152d8a635f790` as the latest certified implementation checkpoint. Perform a fresh residual identity/metadata audit, classify every retained old-version/upstream/later-block occurrence, and make bounded producer/consumer-safe corrections. Keep B4-C technical-language work separate unless a finding is unambiguously identity metadata.
