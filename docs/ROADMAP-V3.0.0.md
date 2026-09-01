# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-01

## Status

**V3-R1 ACTIVE — R1-BLOCK-3 is closed; R1-BLOCK-4 is active.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B1 DONE → R1-B2 DONE → R1-B3 DONE → R1-B4 ACTIVE → R1-B5…B8 BLOCKED → R2+ BLOCKED**

- Canonical repository: `tiagosombrra/abntexto-ufc`.
- Active branch/trunk: `main`.
- B4 operational issue: #187.
- B4 working branch: `refactor/v3-r1-b4-tools-validator`.
- Latest certified clean implementation checkpoint: `7a3b018a43630ed46b375117790acc732ae67b40`.
- B4 activation/control-plane merge: `3512d8b29f2b3634f4ba69bdbc160fa1bc667c19`.
- R1-S2 promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Authority

`release/v3-roadmap.json` is machine authority; this roadmap, `docs/HANDOFF-V3.0.0.md`, and `AGENTS.md` provide human-readable state/bootstrap. Current Git facts must agree with these files. Disagreement fails closed.

## Completed reconstruction stages

- **R1-S0 DONE:** repository sanitation and verified full-history backup.
- **R1-S1 DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`: control plane repair.
- **R1-S2 DONE** at `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`: v3 promoted to `main` without history rewrite.
- **R1-BLOCK-1 DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`: canonical physical naming.
- **R1-BLOCK-2 DONE** at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`: legacy purge and active-tree minimization.
- **R1-BLOCK-3 DONE** at `7a3b018a43630ed46b375117790acc732ae67b40`: semantic/path-consumer closure.

Block 3 internal sequence:

**B3-A DONE → B3-B DONE → B3-C DONE → B3-D DONE → B3-E DONE → B3-F DONE**

Key B3 checkpoints:

- B3-A — PR #159 `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`;
- B3-B — PR #160 `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`;
- B3-C final checker closure — PR #169 `625e82f9ef4780989d4635e500d72d09eab02992`;
- B3-D legacy/dead-code purge — `8f7c05b32f228633e4802a6fa8c14babf16fd685`;
- B3-E validation terminology — PR #182 `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`;
- B3-F residual closure — PR #185 `7a3b018a43630ed46b375117790acc732ae67b40`.

Final B3 evidence: repository contract PASS for 392 tracked files, 14 canonical modules aligned, zero retired v2/N9–N15/B2R active path identities, zero unclassified active project-owned `oracle` identities, no temporary workflow retained, and relevant syntax/diff checks PASS.

## R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline

**ACTIVE.** Operational issue: #187.

Purpose: make project-owned tooling, validator, and consumed metadata reflect current v3 architecture rather than inherited version/process identity, dead helpers, stale ownership, or stale technical language.

### Entry inventory checkpoint

Remote inventory run `33496512650` on branch `refactor/v3-r1-b4-tools-validator` produced a complete first-pass consumer matrix.

The inventory and stale-identity scan steps PASSED. The run's final conclusion was FAIL only because the bounded source-check step invoked `tests/checks/validator_source.py`, which exposed a pre-existing fail-closed defect:

`Full normative contract failed: extended rules without unified evidence: spine.conditional`

This finding must be classified and reconciled before B4 can claim source-check integrity. The validator must not be weakened to hide it.

### Tool classification baseline

Current observed consumers:

- `convert-encoding-to-unicode.ps1` → `prepare-windows-fonts.ps1`;
- `fetch-abntexto.py` → no textual consumer detected; classification required before deletion;
- `fetch-reference-images.py` → `Makefile`;
- `normative_atomic.py` → validator source check;
- `normative_catalog.py` → validator source check;
- `normative_full.py` → coverage rules + validator source check;
- `pdf_measurement.py` → validator source check;
- `pdf_vector_measurement.py` → vector/table validation consumers;
- `prepare-windows-fonts.ps1` → `abntexto-ufc/fonts.def`, preliminarily B8-owned;
- `validate-ufc-pdf.py` → eight live consumers across checks, runner, and validator contract.

No helper is removed solely because its direct reference count is small. Consumer role and later-block ownership must be classified first.

### Validator classification baseline

All four validator files have live consumers:

- `validator/app.js` — 7 consumer references;
- `validator/index.html` — 3;
- `validator/validation-contract.json` — 2;
- `validator/validation-vectors.json` — 3.

The validator directory is therefore an active product surface, not legacy debris.

### Confirmed B4 cleanup candidates

1. `tools/fetch-reference-images.py`: User-Agent still says `abntexto-ufc/2.1.0 reference-assets`.
2. `validator/index.html`: inherited `ufctex · ferramenta independente` identity remains.
3. `tools/validate-ufc-pdf.py`, `validator/app.js`, and `validator/index.html`: significant Portuguese project-owned technical UI/report/diagnostic text requires classification against the English-engineering policy. Academic/rendered Portuguese, official institutional wording, literal output under test, dependency-owned spelling, and current Portuguese runtime/API identifiers are not to be translated indiscriminately.
4. No old repository-name identity was found in audited B4 surfaces.

### Temporary inventory executor

`.github/workflows/b4-inventory.yml` is tracked only on the current B4 working branch. It is not on `main`. It must be removed before any B4 implementation PR/checkpoint is merged.

### B4 classification rules

Every finding is classified as one of:

- current v3 technical surface — retain/normalize in B4;
- B5-owned distribution helper — retain for B5;
- B8-owned certification helper — retain for B8;
- explicit upstream/integration boundary — retain dependency-owned spelling;
- document/rendered Portuguese or literal test data — retain;
- dead/superseded helper or metadata — remove;
- R2 runtime/API surface — defer intact to R2.

### B4 constraints

- Project-owned engineering identifiers, diagnostics, technical labels, and internal metadata are English.
- Do not rewrite the current Portuguese runtime API in R1.
- Do not implement B5 distribution, B6 permanent gates, B7 CI, or B8 final certification.
- Preserve normative rule IDs, expected numeric values, tolerances, and proof state.
- No archive/museum files and no blind global replacement.
- Producer/consumer changes move together.
- Use bounded lots and proportional checks.

### B4 planned lots

**B4-A — inventory blockers and ownership classification**
- classify `spine.conditional` evidence defect;
- classify `fetch-abntexto.py` as current upstream/bootstrap or dead;
- explicitly assign Windows font helpers to B8 if retained.

**B4-B — stale identity/metadata cleanup**
- remove `2.1.0` User-Agent identity;
- replace `ufctex` validator identity with current `abntexto-ufc` technical identity;
- audit package/repository/version metadata consumers together.

**B4-C — validator/tool technical-language rebaseline**
- separate project-owned engineering language from legitimate Portuguese document/runtime content;
- align web/CLI/contract identifiers, diagnostics, exports, and labels without changing normative semantics or R2 API.

**B4-D — final residual audit/closeout**
- all helpers classified;
- dead helpers removed;
- live consumers resolve;
- validator/tool source checks pass;
- temporary executor absent;
- documentation/machine state synchronized.

### B4 acceptance criteria

B4 closes only when every active helper has a current or explicitly assigned later-block role, dead tooling is absent, validator/tool metadata reflects current v3 identity, project-owned technical language is coherent, all relevant consumers resolve, source/syntax/contract checks pass proportionally, and the final residual audit is clean.

## Remaining R1 blocks

- **R1-B4 ACTIVE:** tools, validator, metadata technical rebaseline.
- **R1-B5 BLOCKED:** distribution/public bundle flattening and reproducibility.
- **R1-B6 BLOCKED:** permanent cheap/static fail-closed gates.
- **R1-B7 BLOCKED:** optimized permanent workflow restoration.
- **R1-B8 BLOCKED:** final R1 certification including Windows/font/PDF-A.

## Later phases

- **V3-R2:** direct runtime/API internationalization and Portuguese project API migration.
- **V3-R3:** standards/tests/language semantic hardening.
- **V3-R4:** certification only.
- **V3-R5:** foundation freeze plus current migration/user/maintainer documentation.
- **V3-A1/A2:** article work resumes only against the certified v3 foundation.

## Immediate action

Continue B4 from issue #187. First classify the `spine.conditional` source-contract blocker and `fetch-abntexto.py`; then remove the branch-only inventory workflow and execute B4-B as the first bounded implementation lot. Keep `7a3b018a43630ed46b375117790acc732ae67b40` as the certified implementation checkpoint until a clean B4 implementation merge supersedes it.
