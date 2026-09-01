# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-01

## Status

**V3-R1 ACTIVE — R1-BLOCK-4 active; B4-A done; B4-B done; B4-C active.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B1 DONE → R1-B2 DONE → R1-B3 DONE → R1-B4 ACTIVE → R1-B5…B8 BLOCKED → R2+ BLOCKED**

B4 internal sequence:

**B4-A DONE → B4-B DONE → B4-C ACTIVE → B4-D PENDING**

- Canonical repository: `tiagosombrra/abntexto-ufc`.
- Active trunk: `main`.
- B4 operational issue: #187.
- Latest certified implementation checkpoint: **`001d63dbc4ecd6e555ee735cd0515b6c9203225e`**.
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
- validator project identity updated from the retired legacy branding to `abntexto-ufc`.

Normative rule ID, values, requirement, locator, sources, applicability, proof state, expected numeric values and tolerances were unchanged.

Validation sequence was intentionally fail-closed:

- `33498491307` exposed traceability's old assumption;
- `33498624481` exposed coverage/dead-evidence residue;
- **`33498811794` PASS** after complete reconciliation.

The final run covered Python compilation, JSON parsing, full-contract check, complete `validator_source.py`, JS syntax, exact identity/invariant assertions and `git diff --check`. Temporary workflow removed before merge.

### B4-B — Stale identity and metadata cleanup

**DONE** via PR #191 at **`001d63dbc4ecd6e555ee735cd0515b6c9203225e`**.

A fresh branch-only inventory, run **`33499411771` PASS**, established the residual identity baseline instead of trusting incomplete GitHub code-search results. It confirmed:

- no old repository-name occurrences;
- retired validator identity only at classified migration, negative-test, architecture or historical boundaries;
- active stale identity limited to the chapter-profile wording in `layout.def`, v2.x/B2R-B3 process comments in `public-api.def`, and the versioned PDF/A project-policy locator;
- class/build version identity already aligned to v3.0.0.

B4-B corrections:

- `layout.def` now describes the current UFC normative profile without changing chapter-mode behavior;
- `public-api.def` comments describe the retained Portuguese compatibility behavior and explicitly defer its migration to V3-R2; no commands, keys or forwarding behavior changed;
- `pdfa.profile.project` retains the same rule ID, project-policy authority, technical-profile normativity and PDF/A-2b value, but the locator now names the current implementation policy rather than stale v2.1.0 identity;
- canonical handoff/roadmap no longer inject literal retired-validator branding into the live identity audit.

The repair executor itself was kept fail-closed: intermediate attempts exposed documentation and temporary-executor identity contamination rather than weakening the checker. Final remote run **`33500381847` PASS** covered:

- atomic normative contract;
- complete `validator_source.py` chain;
- `canonical_identity.py`;
- `repository_contract.py`;
- JSON parsing;
- explicit residual assertions;
- `git diff --check`.

Validator-source evidence reported `normative_contract_changed=false`, `proof_state_changed=false`, `locator_policy_changed=false`, and `reference_tolerances_changed=false`. All temporary B4-B workflows were removed before the PR checkpoint.

### B4-C — Validator/tool technical-language rebaseline

**ACTIVE.** Inventory and classify project-owned technical language across:

- `tools/validate-ufc-pdf.py`;
- `validator/app.js`;
- `validator/index.html`;
- `validator/validation-contract.json`;
- `validator/validation-vectors.json`;
- their tests and consumers.

B4-C may normalize project-owned engineering diagnostics, technical UI labels, report/export labels and internal metadata only when the change is producer/consumer-safe.

Preserve these boundaries:

- academic/rendered Portuguese;
- official UFC/ABNT wording and normative requirement text;
- literal test vectors/output that are part of an explicit contract;
- dependency-owned spelling;
- current Portuguese runtime/API identifiers, which migrate only in V3-R2.

Do not turn B4-C into a schema/API rewrite. Stable rule/check IDs and externally consumed schema fields remain unchanged unless proven internal and changed together with every consumer.

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

Start **B4-C** from canonical `main` with implementation checkpoint `001d63dbc4ecd6e555ee735cd0515b6c9203225e`. Run a branch-only, read-only language-boundary inventory over the validator/CLI surfaces and their consumers. Classify every candidate string before editing; preserve academic/normative/literal-test/dependency/R2-runtime boundaries; then apply only bounded producer/consumer-safe technical-language corrections, validate proportionally, remove temporary executors, and update issue #187 plus the canonical control-plane files after the merged lot.
