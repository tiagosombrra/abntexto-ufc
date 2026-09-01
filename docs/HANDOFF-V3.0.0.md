# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-01

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline**.
- Active B4 work item: **B4-D — final residual audit and closeout**.
- Active B4-D focus: **helper ownership, consumer integrity, residual identity/language classification, and temporary-executor absence**.
- Active branch/trunk: `main`.
- B4 operational issue: **#187**.
- Latest certified clean implementation checkpoint: **`1a126c37653728941ce1ada762376c5fec69cb02`**.
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
- validator project identity changed from the retired legacy identity to `abntexto-ufc · standalone validator`.

Remote validation was deliberately fail-closed:

- run `33498491307` exposed the traceability assumption;
- run `33498624481` exposed the coverage assumption and remaining dead evidence ID;
- run **`33498811794` PASS** after complete reconciliation.

Final B4-A gate covered Python compilation, standards JSON parsing, `normative_full_contract.py`, full `validator_source.py`, JS syntax, explicit invariants for `spine.conditional`, current identity assertions, and `git diff --check`. Temporary validation workflow was removed before PR merge. No runtime/API, proof-state, rule-ID, expected numeric value or tolerance changed.

### B4-B — Stale identity and metadata cleanup

**DONE** through PR #191, squash-merged at **`001d63dbc4ecd6e555ee735cd0515b6c9203225e`**.

B4-B performed a fresh active-tree metadata/identity audit rather than relying on GitHub code-search zeros. Remote inventory run **`33499411771` PASS** confirmed:

- zero old repository-name occurrences;
- retired validator identity retained only at classified migration/negative-test/history boundaries;
- active version/process residue isolated to `layout.def`, `public-api.def`, and the PDF/A project-policy locator;
- current class/build identity is v3.0.0.

Corrections:

- `layout.def` chapter-mode comment/error now refers to the current UFC profile rather than a v2 profile;
- `public-api.def` comments describe the retained Portuguese compatibility behavior and explicitly defer API migration to V3-R2, removing v2.x/B2R-B3 process identity without changing any commands or keys;
- `pdfa.profile.project` retains the same project-policy rule/value but its locator now identifies the current PDF/A-2b implementation policy without a stale v2.1.0 version label;
- three literal retired-validator references introduced by the prior checkpoint documentation were rewritten so `canonical_identity.py` remains fail-closed.

Final bounded validation run **`33500381847` PASS** covered the atomic contract, complete `validator_source.py`, `canonical_identity.py`, `repository_contract.py`, JSON parsing, exact residual assertions, and `git diff --check`. Validator-source evidence reported `normative_contract_changed=false`, `proof_state_changed=false`, `locator_policy_changed=false`, and `reference_tolerances_changed=false`. Temporary B4-B workflows were removed before PR merge.

### B4-C — Validator/tool technical-language rebaseline

**DONE** through PR #197, with final implementation checkpoint **`1a126c37653728941ce1ada762376c5fec69cb02`**. Entry language-boundary inventory run **`33501038117` PASS** classified the current surfaces before editing.

Preserved boundaries:

- stable report schema fields, check/rule IDs, profiles and modes already use canonical English identifiers and remain unchanged;
- academic/rendered Portuguese such as `Capa`, `Folha de aprovação`, `Resumo`, `Sumário` and `Referências` remains document-domain wording;
- official UFC/ABNT requirements and normative source text remain unchanged;
- dependency-owned spelling and literal document tokens remain unchanged;
- Portuguese LaTeX runtime/API identifiers remain deferred to V3-R2.

Project-owned technical validator vocabulary, generic categories, diagnostics/evidence/correction messages, report/export headings and Web controls are B4-C candidates only when all producers/consumers move together.

#### B4-C1 — shared status/verdict vocabulary

**DONE** through PR #193, squash-merged at **`97c808081f5a964498b7a3e71d902aeb8a9bbcf8`**.

The shared technical interface now uses:

- statuses: `PASS`, `FAIL`, `WARNING`, `MANUAL REVIEW`, `NOT APPLICABLE`;
- verdicts: `FAIL`, `REVIEW REQUIRED`, `AUTOMATED CHECKS PASSED WITH WARNINGS`, `AUTOMATED CHECKS PASSED`.

CLI, Web, `validation-contract.json`, `validation-vectors.json`, validator-contract expectations, PDF-validator integration consumer and Web status legend changed together. Stable schema fields/check IDs, normative/academic wording, measurement behavior and LaTeX runtime/API were not changed.

Remote validation run **`33501306482` PASS** covered Python/JS syntax, JSON parsing, `normative_validator_contract.py`, complete `validator_source.py`, `canonical_identity.py`, `repository_contract.py`, explicit vocabulary assertions and `git diff --check`. Temporary B4-C1 workflow was removed before merge.

#### B4-C2 — technical categories, diagnostics, report labels, and Web UI

**DONE.** Implemented as bounded producer/consumer-safe sublots.

##### B4-C2a — technical taxonomy and validation levels

**DONE** through PR #195, squash-merged at **`3a24ae4f148ea6fd60a6e66eb7cbf42aecd629c8`**.

C2a normalized only project-owned generic technical categories (`Typography`, `Structure`, `Metadata`, `Accessibility`, `Integrity`, `UFC Deposit`), validation levels (`automatic`, `geometric`, `typographic`, `heuristic`, `deep`, `conditional`), synthetic validation-vector taxonomy, and CLI report headings. Academic/domain labels such as `Capa`, `Folha de aprovação`, `Resumo`, `Sumário` and `Referências` were explicitly preserved.

Remote run **`33502021542` PASS** covered Python/JS/JSON syntax, cross-surface/validator contracts, complete validator-source, canonical identity, repository contract, explicit taxonomy and academic-label assertions, and diff integrity. Cleanup run **`33502137178` PASS** removed the first temporary executor. Pre-merge review then found one substring artifact (`checks automatics`); repair run **`33506189097` PASS** restored the Portuguese diagnostic message because detailed-message translation belongs to C2b, reran the proportional gates, and removed its own temporary workflow.

##### B4-C2b — diagnostics, report/export labels, and Web UI

**DONE** through PR #197, squash-merged at **`1a126c37653728941ce1ada762376c5fec69cb02`**. CLI/Deep and Web/Lite project-owned diagnostics/evidence/corrections, report/export labels, download names, and generic Web controls/disclosures are now English. The Web surface declares `lang=en`; both local-processing disclosure consumers moved with the UI literal.

Validation remained fail-closed: inventory `33506603720` PASS; oversized executor `33506913061` failed before jobs with no functional change; compact run `33507239950` exposed an additional disclosure consumer; migration run **`33507392053` PASS** after reconciliation. Patch review found two remaining PDF/UA technical strings; repair run `33507630613` failed closed on the actual two-occurrence cardinality, and corrected run **`33507724964` PASS** completed the translation and self-removed. Academic/domain labels (`Capa`, `Folha de aprovação`, `Resumo`, `Sumário`, `Referências`), official normative content, stable schema/check/rule IDs, dependency spelling, measurement behavior, proof state, and Portuguese LaTeX runtime/API were preserved.

### B4-D — Final B4 residual audit/closeout

**ACTIVE / NEXT.** Re-audit helper ownership/current role, live consumers, temporary-executor absence, project-owned identity/language residue, and the bounded validator/tool contract. Any residual must be classified before editing. Closure requires proportional source/contract/syntax/diff checks PASS with no normative semantic, proof-state, tolerance, or runtime/API drift.

## Remaining R1 sequence

- **R1-B4 ACTIVE** — tools/validator/metadata rebaseline.
- **R1-B5 BLOCKED** — distribution/public bundle flattening and reproducibility.
- **R1-B6 BLOCKED** — permanent cheap/static fail-closed gates.
- **R1-B7 BLOCKED** — optimized permanent workflow restoration.
- **R1-B8 BLOCKED** — final R1 certification including Windows/font/PDF-A.

## Immediate action

Start B4-D from canonical remote `main` using `1a126c37653728941ce1ada762376c5fec69cb02` as the latest certified implementation checkpoint. Run a branch-only residual audit over B4-owned tools/validator/metadata surfaces and their consumers. Confirm every helper is current or explicitly B5/B8-assigned, no dead helper or temporary executor remains, and every residual project-owned identity/language occurrence is classified. Repair only proven B4-owned residue, validate proportionally, and then close B4 and synchronize the control plane before activating B5.
