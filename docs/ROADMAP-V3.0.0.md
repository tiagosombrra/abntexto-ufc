# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-01

## Status

**V3-R1 ACTIVE — R1-BLOCK-4 active; B4-A done; B4-B active.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B1 DONE → R1-B2 DONE → R1-B3 DONE → R1-B4 ACTIVE → R1-B5…B8 BLOCKED → R2+ BLOCKED**

B4 internal sequence:

**B4-A DONE → B4-B ACTIVE → B4-C PENDING → B4-D PENDING**

- Canonical repository: `tiagosombrra/abntexto-ufc`.
- Active trunk: `main`.
- B4 operational issue: #187.
- Latest certified implementation checkpoint: **`a4fbbdcb381709cb542c8f991ef152d8a635f790`**.
- R1-BLOCK-3 closure: `7a3b018a43630ed46b375117790acc732ae67b40`.
- R1-S2 promotion: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Authority

`release/v3-roadmap.json` is machine authority; this roadmap, `docs/HANDOFF-V3.0.0.md`, and `AGENTS.md` provide human-readable state/bootstrap. Current Git facts must agree with them; disagreement fails closed.

## Completed reconstruction

- **R1-S0 DONE:** repository sanitation and verified full-history backup.
- **R1-S1 DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`: control plane repair.
- **R1-S2 DONE** at `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`: v3 promoted to `main` without history rewrite.
- **R1-B1 DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`: canonical physical naming.
- **R1-B2 DONE** at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`: legacy purge and active-tree minimization.
- **R1-B3 DONE** at `7a3b018a43630ed46b375117790acc732ae67b40`: semantic/path-consumer closure.

Block 3 removed stale path/process/version identity, dead distribution-era implementation, obsolete project-owned validation terminology, runner/evidence defects and final residual path/contract inconsistencies while preserving runtime/API and normative semantics.

## R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline

**ACTIVE.** Operational issue #187.

Purpose: every active project-owned tooling/validator/metadata surface must reflect current v3 architecture, have a real consumer/current role or an explicit later-block assignment, and use coherent project-owned technical identity. B4 does not implement B5 distribution, B6 permanent gates, B7 CI, B8 final certification or R2 runtime/API migration.

### Entry inventory

Remote run `33496512650` produced a live consumer matrix for all 10 `tools/` files and all four `validator/` files. Inventory/stale-identity steps passed; the source check failed on `spine.conditional`, revealing an inherited semantics mismatch between `validation.mode=not-applicable` and executable-evidence assumptions.

Ownership classifications established during B4-A:

- `fetch-abntexto.py` → **B5-owned upstream/bundle helper**; retain unless B5 replaces it.
- `prepare-windows-fonts.ps1` + `convert-encoding-to-unicode.ps1` → **B8-owned Windows/font certification chain**.
- normative/measurement helpers → current validation infrastructure.
- `validate-ufc-pdf.py` → current, eight live consumers.
- all four files in `validator/` → current product surfaces.

### B4-A — Inventory blockers and ownership classification

**DONE** via PR #189 at **`a4fbbdcb381709cb542c8f991ef152d8a635f790`**.

Results:

- exactly one full-contract rule is `not-applicable`: `spine.conditional`;
- that mode is now represented with zero executable checks plus mandatory explicit applicability;
- all executable validation modes still require non-empty evidence and known coverage;
- full contract, traceability, coverage and validator-source checks now share the same fail-closed semantics;
- dead `distribution-source` evidence ID removed; B5 policy retains live `build-path` evidence;
- active reference-assets User-Agent updated from 2.1.0 to 3.0.0;
- validator project identity updated from `ufctex` to `abntexto-ufc`.

Normative rule ID, values, requirement, locator, sources, applicability, proof state, expected numeric values and tolerances were unchanged.

Validation sequence was intentionally fail-closed:

- `33498491307` exposed traceability's old assumption;
- `33498624481` exposed coverage/dead-evidence residue;
- **`33498811794` PASS** after complete reconciliation.

The final run covered Python compilation, JSON parsing, full-contract check, complete `validator_source.py`, JS syntax, exact identity/invariant assertions and `git diff --check`. Temporary workflow removed before merge.

### B4-B — Stale identity and metadata cleanup

**ACTIVE.** The two known entry identities were fixed in PR #189. B4-B now performs a fresh residual audit over:

- active version/package/repository labels;
- tool User-Agent/headers and generated metadata;
- validator ownership/product identifiers;
- stale old-version metadata that is neither certified history, migration/compatibility boundary, B5/B8 assignment nor negative test;
- producer/consumer metadata alignment.

Do not turn B4-B into a global language rewrite. B4-C owns technical-language normalization.

### B4-C — Validator/tool technical-language rebaseline

**PENDING.** Classify project-owned engineering diagnostics, web/CLI labels, report/export keys and internal metadata versus legitimate Portuguese document/runtime content. Preserve academic/rendered Portuguese, official UFC/ABNT wording, literal test data and current runtime/API identifiers. Runtime/API migration remains R2.

### B4-D — Residual audit and closeout

**PENDING.** Require all helpers classified, no dead helper retained, all consumers resolving, source/contract/syntax checks passing proportionally, no temporary executor/workflow, and canonical docs/machine state synchronized.

## Remaining R1 blocks

- **R1-B4 ACTIVE** — tools/validator/metadata rebaseline.
- **R1-B5 BLOCKED** — distribution/public bundle flattening and reproducibility.
- **R1-B6 BLOCKED** — permanent cheap/static fail-closed gates.
- **R1-B7 BLOCKED** — optimized permanent workflow restoration.
- **R1-B8 BLOCKED** — final R1 certification including Windows/font/PDF-A.

## Later phases

- **V3-R2:** direct runtime/API internationalization and Portuguese project API migration.
- **V3-R3:** standards/tests/language semantic hardening.
- **V3-R4:** certification only.
- **V3-R5:** foundation freeze plus current migration/user/maintainer documentation.
- **V3-A1/A2:** article work resumes only against the certified v3 foundation.

## Immediate action

Start **B4-B** from canonical `main` with implementation checkpoint `a4fbbdcb381709cb542c8f991ef152d8a635f790`. Run a fresh residual metadata/identity inventory, classify each occurrence before editing, repair only active stale technical identity, validate proportionally, remove any temporary executor before checkpoint, and update issue #187 plus the three canonical control-plane files after each merged lot.
