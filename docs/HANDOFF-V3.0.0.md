# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-01

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline**.
- Active branch/trunk: `main`.
- B4 operational issue: **#187**.
- B4 working branch: `refactor/v3-r1-b4-tools-validator`.
- Latest certified clean implementation checkpoint: `7a3b018a43630ed46b375117790acc732ae67b40`.
- R1-BLOCK-3 closure checkpoint: `7a3b018a43630ed46b375117790acc732ae67b40`.
- B4 activation/control-plane merge: `3512d8b29f2b3634f4ba69bdbc160fa1bc667c19` (documentation/state only; not a new implementation checkpoint).
- R1-S2 trunk promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

`main` is the canonical source of truth and merge target. Short-lived branches are implementation vehicles only. The repository rename to `abntexto-ufc` preserved repository identity, history, tags, issues, pull requests, and governance.

## Completed reconstruction stages

- **R1-S0 DONE:** repository sanitation, verified full-history backup, obsolete refs/PRs retired, immutable version tags preserved.
- **R1-S1 DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`: control plane repaired and abandoned executor/workflow removed.
- **R1-S2 DONE** at `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`: v3 promoted to `main` without history rewrite; reference build and agreed promotion gates passed.
- **R1-BLOCK-1 DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`: canonical physical naming.
- **R1-BLOCK-2 DONE** at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`: legacy purge and active-tree minimization.

Permanent CI remains intentionally absent during structural R1 reconstruction.

## R1-BLOCK-3 — Semantic / Path-Consumer Closure

**DONE** at `7a3b018a43630ed46b375117790acc732ae67b40`.

Block 3 closed live-tree path/process identity, runner/evidence defects, v1/v2 operational identity, dead distribution-era code, obsolete project-owned `oracle` terminology, and the final residual contract/path issues without changing runtime/API semantics or normative values.

Key checkpoints:

- B3-A — PR #159, `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`;
- B3-B — PR #160, `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`;
- B3-C final checker closure — PR #169, `625e82f9ef4780989d4635e500d72d09eab02992`;
- B3-D legacy/dead-code purge — `8f7c05b32f228633e4802a6fa8c14babf16fd685`;
- B3-E validation terminology — PR #182, `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`;
- B3-F final residual closure — PR #185, `7a3b018a43630ed46b375117790acc732ae67b40`.

Final Block 3 evidence: repository contract PASS (`tracked_files=392`, `history_directories=0`, `legacy_class=0`), 14 canonical modules aligned, zero retired v2/N9–N15/B2R active paths, zero unclassified active project-owned `oracle` occurrences, font POC canonical binding PASS, relevant Python/shell syntax PASS, `git diff --check` PASS, and no temporary workflow retained.

## R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline

**ACTIVE.** Operational continuity: issue #187.

B4 owns the current technical surfaces in `tools/`, `validator/`, and metadata consumed by them. It does not own the R2 runtime/API rewrite, B5 distribution reconstruction, B6 permanent gates, B7 workflow restoration, or B8 final Windows/font/PDF-A certification.

### B4 entry inventory — remote run 33496512650

A branch-only inventory was executed from `refactor/v3-r1-b4-tools-validator`. The inventory steps themselves **PASSED**. The overall run concluded FAIL only in the bounded source-check step because `tests/checks/validator_source.py` exposed a pre-existing contract defect:

`Full normative contract failed: extended rules without unified evidence: spine.conditional`

This is a fail-closed B4 finding. It has not been repaired or reclassified yet.

The inventory recorded 10 files in `tools/` and four live files in `validator/`.

#### Tool consumer matrix

- `tools/convert-encoding-to-unicode.ps1` → `tools/prepare-windows-fonts.ps1`.
- `tools/fetch-abntexto.py` → **0 textual consumers detected**; do not delete until classified as either explicit upstream/bootstrap helper or dead helper.
- `tools/fetch-reference-images.py` → `Makefile`.
- `tools/normative_atomic.py` → `tests/checks/validator_source.py`.
- `tools/normative_catalog.py` → `tests/checks/validator_source.py`.
- `tools/normative_full.py` → `standards/coverage-rules.json`, `tests/checks/validator_source.py`.
- `tools/pdf_measurement.py` → `tests/checks/validator_source.py`.
- `tools/pdf_vector_measurement.py` → `standards/vector-rule-validation-extension.json`, `tests/integration/table-ibge-vector-evidence.sh`, `tests/integration/vector-rule-validation.sh`.
- `tools/prepare-windows-fonts.ps1` → `abntexto-ufc/fonts.def`; retain as B8-relevant unless later evidence disproves the consumer relationship.
- `tools/validate-ufc-pdf.py` → eight live consumers across normative validator checks, source checks, `pdf-validator.sh`, and `validator/validation-contract.json`.

#### Validator consumer matrix

All four validator files have live consumers and are **not** dead-code candidates:

- `validator/app.js` → seven consumers;
- `validator/index.html` → three consumers;
- `validator/validation-contract.json` → two consumers;
- `validator/validation-vectors.json` → three consumers.

#### Confirmed stale B4 identities

1. `tools/fetch-reference-images.py` still sends User-Agent `abntexto-ufc/2.1.0 reference-assets`.
2. `validator/index.html` still presents the inherited identity `ufctex · ferramenta independente`.
3. `tools/validate-ufc-pdf.py`, `validator/app.js`, `validator/index.html`, and validator report/export labels contain substantial Portuguese **project-owned technical UI/output language**. These must be classified carefully: project-owned engineering identity/diagnostics belong in English in B4, while academic/rendered Portuguese, official UFC/ABNT wording, literal output under test, and current runtime/API identifiers remain allowed.
4. No old repository-name occurrence was found in the audited B4 surfaces.

### Temporary executor state

The temporary `.github/workflows/b4-inventory.yml` exists **only** on branch `refactor/v3-r1-b4-tools-validator`. It is not present on `main` and must be deleted from the branch before any B4 implementation PR/checkpoint is merged.

### B4 rules

- Project-owned engineering identifiers, diagnostics, technical labels, and internal metadata are English.
- Academic/rendered Portuguese and explicit upstream/runtime identifiers are preserved at documented boundaries.
- Do not rewrite the current Portuguese runtime API before V3-R2.
- Delete dead helpers instead of preserving them as historical artifacts.
- Producer/consumer changes move together.
- Preserve normative rule IDs, expected numeric values, tolerances, and proof state.
- Use bounded lots and proportional validation; do not rerun heavyweight gates unless invalidated by a B4 change.
- No permanent workflow is introduced in B4.

### B4 next action

1. Classify the `spine.conditional` evidence defect and repair it only if it is genuinely owned by B4/current validator-source integrity; do not silently weaken the validator.
2. Classify `tools/fetch-abntexto.py` as current upstream/bootstrap helper versus dead helper.
3. Remove the stale `2.1.0` User-Agent identity and `ufctex` validator identity in a bounded lot.
4. Separate validator English-engineering cleanup from legitimate Portuguese document/runtime surfaces before editing.
5. Remove the temporary inventory workflow before the first B4 checkpoint PR.

B4 closes only when every active helper has a current or explicitly assigned later-block role, dead tooling is absent, validator/tool metadata reflects current v3 identity, project-owned technical surfaces are coherent, proportional checks pass, and the final B4 residual audit is clean.

## Remaining R1 sequence

- **R1-B4 ACTIVE:** tools, validator, metadata technical rebaseline.
- **R1-B5 BLOCKED:** distribution/public bundle flattening and reproducibility.
- **R1-B6 BLOCKED:** permanent cheap/static fail-closed gates.
- **R1-B7 BLOCKED:** optimized permanent workflow restoration.
- **R1-B8 BLOCKED:** final R1 certification including Windows/font/PDF-A.

## Non-negotiable rules

The active repository is not an archive. Historical/process evidence belongs in Git history, immutable tags, releases, issues, PRs, certified SHAs, and verified backups. No dead legacy helper is retained merely as documentation.

Git facts, `release/v3-roadmap.json`, this handoff, and `docs/ROADMAP-V3.0.0.md` must agree. Any disagreement fails closed.
