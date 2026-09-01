# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-01

## Checkpoint

- Repository: **`tiagosombrra/abntexto-ufc`**.
- Phase: **V3-R1 ACTIVE**.
- Active implementation stage: **R1-BLOCK-7 — Optimized Remote Workflow Restoration**.
- Active B7 work item: **B7-C — optimized Linux integration/release orchestration**.
- Active B7 sub-item: **B7-C2 — permanent Linux PR integration orchestration consuming the certified repository-owned `make check` contract**.
- Active B7 focus: **introduce a bounded permanent Linux PR integration workflow that delegates to `make check`, keeps gate logic repository-owned, and avoids heavy execution on every intermediate commit**.
- Active branch/trunk: `main`.
- B7 operational issue: **#213**.
- Latest certified clean implementation checkpoint: **`ced68313ed2c362a6617d7df6ef9adfd2df6c0b5`**.
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

Permanent workflow orchestration is B7-owned. B6 closed with zero permanent workflows and a certified local/static entry point; B7-B has now restored the first permanent workflow, `Static contract`, as a direct `make static-check` consumer.

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

**DONE.** Operational issue #187 closed after B4-D zero-diff certification; latest implementation checkpoint remains `1a126c37653728941ce1ada762376c5fec69cb02`.

B4 owns current technical surfaces in `tools/`, `validator/`, and metadata consumed by them. It does not own R2 runtime/API migration, B5 distribution implementation, B6 permanent gates, B7 workflow restoration, or B8 final Windows/font/PDF-A certification.

### Entry inventory

Remote run `33496512650` established the initial consumer matrix. Inventory/stale-identity steps passed; the overall run failed only because `validator_source.py` exposed `spine.conditional` as an extension without unified executable evidence.

Observed ownership:

- `fetch-abntexto.py` has no current textual consumer but is explicitly an upstream `abntexto` pin/fetch helper for Overleaf/public bundle construction: **classified B5-owned**, retained for B5 unless B5 supersedes it.
- `prepare-windows-fonts.ps1` and `convert-encoding-to-unicode.ps1` form a live Windows-font preparation chain consumed by `abntexto-ufc/fonts.def`: **classified B8-owned**.
- normative contract/measurement helpers are live validator/test infrastructure.
- `validate-ufc-pdf.py` has 11 live consumers.
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

**DONE.** Initial remote audit run `33508301453` completed the ownership/consumer inventory and exposed two fail-closed facts: the temporary audit workflow itself contained retired-identity search literals, and five version-labelled messages remain in `tests/integration/font-embedding.sh`. Those five messages are classified as B8-owned font-certification residue and were not pulled into B4.

**Final run `33511105257` PASS.** It reconfirmed all 10 tools and all four validator files, live consumers, B5/B8 ownership assignments, classified document-language residue, normative atomic/cross-surface/validator contracts, full validator-source checks, 14-module canonical identity, repository contract, and diff integrity. The workflow self-removed at audit-branch commit `c042ffb`; compare against `main` reported zero changed files. B4-D therefore required no implementation merge and changed no normative semantics, proof state, locator policy, reference tolerance, measurement behavior, or runtime/API.

## R1-BLOCK-5 — Distribution and Public Bundle Rebaseline

**DONE.** Operational closure log: issue #199. Entry implementation checkpoint: `1a126c37653728941ce1ada762376c5fec69cb02`; certified B5 implementation/closure checkpoint: `4bc0f544020234bc14a8f2261927f65721b6eddb`.

B5 owns the current public/distribution bundle contract: producer and consumer inventory, canonical source set, flatten/copy rules, manifests, deterministic generation, reproducibility, and current build-path/distribution-policy reconciliation. `tools/fetch-abntexto.py` enters B5 as an explicitly assigned upstream/bundle helper and must be retained, replaced, or removed only through a proven current distribution role.

B5 does not own V3-R2 runtime/API migration, B6 permanent static gates, B7 permanent workflow restoration, or B8 Windows/font/PDF-A certification. The five version-labelled messages classified in the font-only integration gate remain B8-owned.

### B5-A — Inventory and distribution contract

**DONE — zero-diff certification.** Remote run `33512036280` PASS established the current distribution contract and self-removed its temporary workflow; the audit branch has zero changed files versus `main`. There is no current bundle producer or tracked `dist/` tree. `Makefile` exposes build/check entry points only. `tools/fetch-abntexto.py` is a valid pinned upstream fetcher but has no functional consumer. `build-path.sh` validates the repository build; `overleaf-stable.sh` assumes an already-flattened staging root, is not wired into `tests/run.py`, and still contains a removed font-check path plus stale engineering diagnostics.

The current architecture requires `template/` to be flattened for public/Overleaf bundles, excludes the UFC institutional mark from public redistribution, and keeps distribution/Overleaf/TeX Live/CTAN as project policy rather than UFC/ABNT normativity. Historical distribution code is advisory only; reusable principles are deterministic archives, explicit source sets, SHA256 manifests, safe paths, pinned upstream `abntexto.cls`, and exclusion of institutional/proprietary assets. Retired legacy class/module identities, old artifact names, and permanent workflows are not reusable.

### B5-B — Deterministic v3 staging and public/Overleaf bundles

**DONE** through PR #202, squash-merged at **`426b506da9f6bf6255263efdb4caad19d4bcd16d`**. The lot introduced `tools/build-public-bundles.py`, the `make public-bundles` producer entry point, `tests/checks/public_bundles.py`, an explicit flattened-staging Overleaf consumer, and the v3 public-template header. It now emits deterministic `abntexto-ufc-template-3.0.0.zip` and `abntexto-ufc-overleaf-3.0.0.zip`; the template bundle is version-rooted and the Overleaf bundle is import-root-flat. Only the Overleaf archive vendors the pinned upstream `abntexto.cls`. Public archives disable and exclude the UFC institutional mark and reject proprietary Microsoft font files and development-only paths.

Remote validation was fail-closed. Run `33514329081` exposed an executor misuse of a correctly cleaned temporary upstream file; run `33514454139` proved structure/reproducibility and exposed that the TeX container itself lacked Git; final run **`33514846706` PASS** reported `PUBLIC-BUNDLE-EVIDENCE status=PASS artifacts=2 reproducible=2 safe_paths=PASS institutional_assets=excluded`, canonical identity PASS, repository contract PASS, and successfully compiled the extracted Overleaf bundle with both `pdflatex` and `lualatex` on TeX Live 2025. Existing font-embedding and PDF/A proxy assertions also passed. The temporary workflow self-removed before merge. No runtime/API or normative semantic/proof/tolerance/locator change occurred.

### B5-C — Class/CTAN candidate and distribution metadata

**DONE** through PR #204, squash-merged at **`4bc0f544020234bc14a8f2261927f65721b6eddb`**. `make distribution-bundles` now composes the certified B5-B public bundles with a deterministic class/runtime archive, a CTAN submission candidate and `SHA256SUMS`. The CTAN candidate uses one browsing-friendly `abntexto-ufc/` directory, a dedicated English package README, tracked manual source plus deterministic PDF, a minimal example, current class/runtime modules and LICENSE. `abntexto` remains an external dependency for class/CTAN packages and is vendored only by the separate Overleaf bundle.

The accepted `abntexto-uece` package was used as a practical packaging benchmark, then reconciled with current CTAN upload guidance rather than copied blindly. Initial run `33516334003` PASS proved the first deterministic package contract. The benchmark exposed the need for CTAN-facing README/PDF documentation and a simpler browsing layout. Corrected run **`33519160480` PASS** proved five reproducible outputs, checksums, class/CTAN layouts, README metadata, deterministic documentation PDF, external `abntexto`, canonical identity, repository contract and TeX Live 2026 install/compile smoke. Run `33519663437` was executor-only (ubuntu-latest lacked `pdflatex`). Final run **`33519793206` PASS** executed CTAN `pkgcheck 4.1.0` on the extracted candidate with no error or warning diagnostics. All temporary workflows self-removed. CTAN acceptance/submission itself remains a later explicit release action; see `docs/CTAN-RELEASE.md`.

### B5-D — Final B5 residual/reproducibility audit

**DONE — zero-diff certification.** Run `33523356265` reconfirmed all distribution/public product checks but failed on an audit-key mismatch; the same review exposed two stale roadmap/machine-state residues. PR #206 repaired those control-plane residues and run `33523899178` PASS validated the repair. Final run **`33524219575` PASS** certified five deterministic outputs including `SHA256SUMS`, public/CTAN contracts, distribution policy, zero tracked generated `dist/` files, zero permanent workflows, canonical identity/repository contract and coherent control plane. The temporary executor self-removed and the final audit branch is zero-diff versus `main`; no B5-D implementation merge was required.

## R1-BLOCK-6 — Permanent Cheap/Static Fail-Closed Gates

**DONE.** Operational issue #207 closed; certified B6 functional closure checkpoint: **`4c25c27b758e4b99db11187b34b9043776566871`**.

B6 established a single permanent side-effect-free source-only validation entry point while keeping the broad integration/release runner separate.

### B6-A — Validation inventory and dependency classification

**DONE.** Run `33525282652` PASS inventoried 69 Python checkers, 74 shell integrations, four validator files and 26 broad-runner checks. Refinement run `33525499620` failed closed only to classify two exclusions: one checker requires generated PDF inputs and one cheap checker writes evidence. Nineteen other measured candidates passed without working-tree side effects. Redundancy analysis established `validator_source.py` as the aggregate normative/validator source contract.

### B6-B — Canonical permanent static gate

**DONE** through PR #211 at **`4c25c27b758e4b99db11187b34b9043776566871`**. The permanent surface is `tests/static.py` plus `make static-check`. It validates tracked Python/JSON/shell/JavaScript syntax, diff integrity, canonical identity, repository contract, aggregate validator/normative source contracts, normative object scope and reference-guide contract. README and architecture document the ownership boundary. Runs `33527802639` and `33528078426` PASS certified normal execution, pre-existing dirty-tree preservation, malformed tracked JSON rejection and failure-path status protection. No permanent workflow was added in B6.

### B6-C — Residual audit and B7 handoff

**DONE — zero-diff certification.** Final run **`33529190303` PASS** reconfirmed exact five-check ownership, both classified exclusions, zero TeX/PDF/network/distribution/Windows-font/PDF-A behavior, zero side effects and zero permanent workflows on `main`. Observed `make static-check` cost was **1.859 s** on the hosted Ubuntu runner. The temporary executor self-removed and the audit branch is zero-diff versus `main`; no B6-C implementation merge was required.

## R1-BLOCK-7 — Optimized Remote Workflow Restoration

**ACTIVE.** Operational issue #213. Entry certified implementation checkpoint: `4c25c27b758e4b99db11187b34b9043776566871`; latest certified implementation checkpoint: **`ced68313ed2c362a6617d7df6ef9adfd2df6c0b5`**.

B7 restores GitHub Actions as a thin orchestration layer over repository-owned entry points. Workflow YAML must consume `make static-check`, `make check` and `make release-check` where appropriate rather than duplicate their internal checks. Remote validation is the canonical CI execution path; developer-local state is not required for certification.

### B7-A — Workflow/runner inventory and orchestration design

**DONE.** Remote inventory run `33530309579` established the current orchestration contract: 30 checks in PR mode and 32 in release mode; only `pdfa` and `profile-pdfa` are release-only. The integration surface depends heavily on TeX/PDF tooling (`pdflatex`, `lualatex`, Biber, Poppler, glossary/index/minted paths). The successful historical pattern uses pinned checkout/setup actions, Python 3.13, Node 24 and TeX Live 2026 in a Debian-based TeX runner, with hosted Windows work still reserved for B8.

The same run deliberately probed `make check` on a clean TeX Live 2026 runner. It completed in 501 s with `PASS=22 FAIL=7 SKIP=1`, proving that permanent heavy orchestration must not be restored before the repository-owned runner itself is repaired. The failures are execution/artifact-contract drift: reference-corpus root/output mismatch; stale CAPES front-matter path; detached object-geometry `--commit-sha`; fixture/job-name drift in objects and bibliography; obsolete `filename=` Makefile invocation in profile matrix; stale appendix/annex scenario key; and the dependent reference-spacing skip. No normative-rule regression was established by the probe.

### B7-B — Permanent fast/static workflow

**DONE** through PR #216, squash-merged at **`643397ee2fa49e6bd496889cb287f43167d49b0f`**. `.github/workflows/static-contract.yml` provides stable workflow/job name **`Static contract`**, triggers on pull requests to `main`, pushes to `main`, and manual dispatch, uses read-only repository permissions and concurrency cancellation, pins checkout/setup actions, runs Ubuntu 24.04 with Python 3.13 and Node 24, and delegates the complete validation contract to exactly one command: `make static-check`. Remote run **`33530718380` PASS** certified the permanent workflow. No TeX/PDF/network/distribution/Windows/font/PDF-A behavior was duplicated into YAML.

### B7-C — Optimized Linux integration/release orchestration

**ACTIVE.** B7-C starts with a repository-owned clean-runner repair before permanent heavy workflow YAML is introduced.

- **B7-C1 DONE — clean-runner integration contract repair:** PR #220 merged at `ced68313ed2c362a6617d7df6ef9adfd2df6c0b5` after final TeX Live 2026 run `33545418119` proved `make check` with `PASS=30 FAIL=0 SKIP=0`; final `Static contract` run `33547122520` passed after temporary workflow removal. The repair changed execution/artifact wiring and synthetic fixture markers only; normative IDs, values, tolerances, proof state and runtime/API behavior were preserved.
- **B7-C2 ACTIVE — permanent Linux PR integration orchestration:** add a bounded workflow that delegates to the now-certified `make check` entry point and avoids heavy execution on every intermediate commit when the permanent `Static contract` status is sufficient.
- **B7-C3 PENDING — release orchestration:** define the Linux `make release-check` cadence/trigger without claiming B8 Windows/font/final PDF-A certification.

### B7-D — Residual audit and B8 handoff

**PENDING.** Audit workflow ownership/status semantics, recommend stable required checks/branch-protection policy, remove any temporary executors, and hand final Windows/font/PDF-A certification to B8.

B8 retains final Windows/font/PDF-A certification. V3-R2 retains runtime/API migration. Actual CTAN submission remains an explicit release action outside B7.
