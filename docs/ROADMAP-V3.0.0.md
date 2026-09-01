# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-01

## Status

**V3-R1 ACTIVE — R1-BLOCK-6 done; R1-BLOCK-7 active; B7-A/B/C1/C2 done; B7-C3 active.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B1 DONE → R1-B2 DONE → R1-B3 DONE → R1-B4 DONE → R1-B5 DONE → R1-B6 DONE → R1-B7 ACTIVE → R1-B8 BLOCKED → R2+ BLOCKED**

B4 internal sequence:

**B4-A DONE → B4-B DONE → B4-C DONE [C1 DONE → C2a DONE → C2b DONE] → B4-D DONE**

B7 internal sequence:

**B7-A DONE → B7-B DONE → B7-C ACTIVE [C1 DONE → C2 DONE → C3 ACTIVE] → B7-D PENDING**

- Canonical repository: `tiagosombrra/abntexto-ufc`.
- Active trunk: `main`.
- B7 operational issue: #213.
- Latest certified implementation checkpoint: **`cea59bcf4927da9a9c4a48268dca67cc9535854e`**.
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

**DONE.** Operational issue #187 closed after zero-diff B4-D certification.

Purpose: every active project-owned tooling/validator/metadata surface must reflect current v3 architecture, have a real consumer/current role or an explicit later-block assignment, and use coherent project-owned technical identity. B4 does not implement B5 distribution, B6 permanent gates, B7 CI, B8 final certification or R2 runtime/API migration.

### Entry inventory and ownership

Remote run `33496512650` produced a live consumer matrix for all 10 `tools/` files and all four `validator/` files. The inherited `spine.conditional` validator-contract mismatch was reconciled in B4-A.

Ownership classifications:

- `fetch-abntexto.py` → **B5-owned upstream/bundle helper**;
- `prepare-windows-fonts.ps1` + `convert-encoding-to-unicode.ps1` → **B8-owned Windows/font certification chain**;
- normative/measurement helpers → current validation infrastructure;
- `validate-ufc-pdf.py` → current, 11 live consumers;
- all four files in `validator/` → current product surfaces.

### B4-A — Inventory blockers and ownership classification

**DONE** via PR #189 at **`a4fbbdcb381709cb542c8f991ef152d8a635f790`**.

Results:

- `spine.conditional` is the sole full-contract `not-applicable` rule and now carries zero executable checks plus explicit applicability;
- executable validation modes continue to require non-empty evidence;
- full contract, traceability, coverage and validator-source semantics agree fail-closed;
- dead `distribution-source` evidence removed while B5 retains live `build-path` evidence;
- active reference-assets User-Agent moved to 3.0.0;
- validator product identity moved to `abntexto-ufc`.

Final B4-A validation run **`33498811794` PASS**. Normative IDs/values/tolerances and proof state were unchanged.

### B4-B — Stale identity and metadata cleanup

**DONE** via PR #191 at **`001d63dbc4ecd6e555ee735cd0515b6c9203225e`**.

Inventory run **`33499411771` PASS** confirmed no old repository-name occurrence and isolated active stale identity to current layout/API comments and the PDF/A project-policy locator. The lot:

- rebased chapter-profile wording to the current UFC profile;
- replaced v2.x/B2R-B3 process comments with current compatibility-boundary language and explicit V3-R2 deferral;
- rebased the PDF/A-2b project-policy locator without changing rule semantics;
- removed live documentation contamination that would violate canonical identity checking.

Final run **`33500381847` PASS** covered atomic contract, full validator-source chain, canonical identity, repository contract, JSON and diff integrity. Proof state, normative semantics and reference tolerances remained unchanged.

### B4-C — Validator/tool technical-language rebaseline

**DONE** through PR #197 at **`1a126c37653728941ce1ada762376c5fec69cb02`**. Entry language-boundary inventory run **`33501038117` PASS** classified the current Web/CLI surfaces before modification.

Preserved boundaries:

- stable machine schema/check/rule identifiers, profiles and modes;
- academic/rendered Portuguese document-element terminology;
- official UFC/ABNT requirement and source wording;
- dependency-owned spelling and literal document tokens;
- Portuguese LaTeX runtime/API identifiers until V3-R2.

Project-owned validator status/verdict vocabulary, technical categories and levels, diagnostics/evidence/correction messages, report/export headings and Web controls may be normalized only with all consumers updated together.

#### B4-C1 — shared status/verdict vocabulary

**DONE** via PR #193 at **`97c808081f5a964498b7a3e71d902aeb8a9bbcf8`**.

Coordinated Web/CLI interface vocabulary now uses:

- statuses: `PASS`, `FAIL`, `WARNING`, `MANUAL REVIEW`, `NOT APPLICABLE`;
- verdicts: `FAIL`, `REVIEW REQUIRED`, `AUTOMATED CHECKS PASSED WITH WARNINGS`, `AUTOMATED CHECKS PASSED`.

The CLI, Web app, technical contract, vectors, contract test, integration consumer and Web status legend moved together. Stable IDs/schema fields, normative/academic text, measurement behavior and LaTeX runtime/API stayed unchanged.

Remote validation run **`33501306482` PASS** covered Python/JS syntax, JSON, `normative_validator_contract.py`, full `validator_source.py`, canonical identity, repository contract, exact vocabulary assertions and diff integrity. No temporary workflow remained at checkpoint.

#### B4-C2 — technical categories, diagnostics, report labels and Web UI

**DONE.** Implemented as bounded sublots.

##### B4-C2a — technical taxonomy and levels

**DONE** via PR #195 at **`3a24ae4f148ea6fd60a6e66eb7cbf42aecd629c8`**. Generic project-owned technical categories, validation levels, synthetic cross-surface taxonomy and CLI report headings were normalized to English while academic/domain terms remained Portuguese.

Run **`33502021542` PASS** validated cross-surface/validator contracts, full validator source, canonical identity, repository contract, syntax/JSON/diff integrity and explicit academic-label preservation. Run **`33502137178` PASS** removed the initial executor. Review found and blocked one accidental substring artifact before merge; run **`33506189097` PASS** repaired it, reran the proportional gates and self-removed the repair workflow.

##### B4-C2b — diagnostics, report/export labels and Web UI

**DONE** via PR #197 at **`1a126c37653728941ce1ada762376c5fec69cb02`**. Project-owned CLI/Web diagnostics, evidence/correction messages, report/export labels, download names and generic validator UI were normalized to English. The Web UI now declares `lang=en`; fail-closed local-processing consumers moved together with the disclosure.

Evidence: `33506603720` inventory PASS; `33506913061` invalid oversized executor/no functional change; `33507239950` exposed a missing disclosure consumer; `33507392053` PASS after reconciliation; patch review exposed two PDF/UA residuals; `33507630613` failed closed on cardinality; **`33507724964` PASS** completed the review repair. Protected academic/normative/runtime boundaries and normative proof state remained unchanged.

### B4-D — Residual audit and closeout

**DONE.** Run `33508301453` performed the final ownership/consumer inventory and failed closed only because the temporary audit workflow contained its own retired-identity search literals; it also classified five version-labelled messages in the font-only integration gate as B8-owned residue. Corrected run **`33511105257` PASS** reconfirmed 10 tools, four validator files, all live consumers, B5/B8 assignments, language boundaries, atomic/cross-surface/validator contracts, validator-source checks, canonical identity, repository contract and diff integrity. The audit workflow self-removed and the audit branch has zero changed files versus `main`; no implementation merge was required.

## R1-BLOCK-5 — Distribution and Public Bundle Rebaseline

**DONE.** Operational closure log: issue #199. Entry checkpoint: `1a126c37653728941ce1ada762376c5fec69cb02`; certified B5 implementation/closure checkpoint: `4bc0f544020234bc14a8f2261927f65721b6eddb`.

Purpose: reconstruct the current public/distribution bundle contract from the v3 canonical tree. B5 will inventory producers and consumers, define the canonical source set and flatten/copy rules, reconcile manifests/policies/build-path integration, determine the current role of `tools/fetch-abntexto.py`, and make bundle generation deterministic and reproducible without reviving retired release scaffolding.

### B5-A — Inventory and distribution contract

**DONE — zero-diff.** Run `33512036280` PASS found no current bundle producer or tracked distribution artifacts. The repository contract says public/Overleaf bundles flatten `template/`; public archives exclude the UFC institutional mark. `fetch-abntexto.py` remains a verified pinned fetcher without a functional consumer. `build-path.sh` is live; `overleaf-stable.sh` expects staging that does not currently exist and contains a removed font-check path. Distribution policy remains project policy with `build-path` as current evidence. The audit workflow self-removed and the branch is zero-diff.

### B5-B — Deterministic v3 staging and public/Overleaf bundles

**DONE** via PR #202 at **`426b506da9f6bf6255263efdb4caad19d4bcd16d`**. Current v3 distribution now has deterministic template and Overleaf ZIP producers, a public-bundle structure/reproducibility checker, a `make public-bundles` entry point, explicit flattened staging, pinned upstream `abntexto.cls` only for Overleaf, and fail-closed institutional/proprietary asset exclusion. Final run **`33514846706` PASS** validated reproducible archives, safe paths, canonical identity/repository contract, and `pdflatex` + `lualatex` compilation of the extracted Overleaf bundle on TeX Live 2025. Temporary validation workflow removed.

### B5-C — Class/CTAN candidate and distribution metadata

**DONE** via PR #204 at **`4bc0f544020234bc14a8f2261927f65721b6eddb`**. The complete distribution producer now emits the class/runtime, CTAN, template and Overleaf ZIPs plus `SHA256SUMS`. CTAN packaging was benchmarked against accepted `abntexto-uece` and reconciled with current CTAN guidance: one browsing-friendly package root, CTAN-specific English README, tracked manual source/PDF, example, current runtime and external `abntexto`. Run **`33519160480` PASS** proved reproducibility, metadata/layout, checksums and TeX Live 2026 installation smoke; run **`33519793206` PASS** ran CTAN `pkgcheck 4.1.0` with zero error/warning diagnostics. CTAN submission remains a later explicit release action and `docs/CTAN-RELEASE.md` records the maintainer procedure.

### B5-D — Residual/reproducibility closeout

**DONE — zero-diff certification.** Initial run `33523356265` reconfirmed distribution/public reproducibility and repository identity but failed closed on an executor machine-key mismatch; manual review simultaneously found two stale control-plane residues. PR #206 repaired only those roadmap/machine-state residues, validated by `33523899178` PASS. Final run **`33524219575` PASS** certified five deterministic outputs including checksums, public and CTAN contracts, distribution-policy alignment, zero tracked generated `dist/` files, zero permanent workflows, canonical identity/repository contract and coherent control plane. The temporary audit self-removed and the audit branch is zero-diff versus `main`, so no B5-D implementation merge was required. The certified functional checkpoint remains `4bc0f544020234bc14a8f2261927f65721b6eddb`.

## R1-BLOCK-6 — Permanent Cheap/Static Fail-Closed Gates

**DONE.** Operational issue #207 closed. Certified functional closure checkpoint: **`4c25c27b758e4b99db11187b34b9043776566871`**.

### B6-A — Validation inventory and dependency classification

**DONE.** Run `33525282652` inventoried 69 Python checkers, 74 shell integrations, four validator files and 26 broad-runner checks. Run `33525499620` failed closed only to classify one PDF-input checker and one evidence-writing checker out of the source-only tier. Nineteen other candidates passed without working-tree side effects. The final composition avoids redundant execution because `validator_source.py` already aggregates the central normative/validator source chain.

### B6-B — Canonical permanent static gate

**DONE** via PR #211 at **`4c25c27b758e4b99db11187b34b9043776566871`**. `tests/static.py` + `make static-check` is the permanent cheap/source-only contract. Runs `33527802639` and `33528078426` PASS certified syntax/data checks, identity/contracts, no-side-effect behavior, dirty-tree preservation and malformed JSON rejection. README and architecture record the validation-tier ownership; `tests/run.py` remains the broader integration/release runner.

### B6-C — Residual audit and B7 handoff

**DONE — zero-diff.** Run **`33529190303` PASS** reconfirmed exact gate composition, both exclusions, zero heavy/runtime leakage, zero side effects and zero permanent workflows. Observed cost was **1.859 s** on hosted Ubuntu. No B6-C implementation merge was required.

## R1-BLOCK-7 — Optimized Remote Workflow Restoration

**ACTIVE.** Operational issue #213. Entry checkpoint: `4c25c27b758e4b99db11187b34b9043776566871`; latest certified implementation checkpoint: **`cea59bcf4927da9a9c4a48268dca67cc9535854e`**.

B7 restores permanent GitHub Actions as orchestration over current repository entry points; workflow YAML must not duplicate gate internals.

### B7-A — Workflow/runner dependency inventory and orchestration design

**DONE.** Run `33530309579` inventoried the current runner surface and established the orchestration boundary: 30 PR checks, 32 release checks, with only `pdfa` and `profile-pdfa` release-only. The broad runner is TeX/PDF-heavy and depends on pdflatex/lualatex, Biber, Poppler, glossary/index/minted tooling. Historical successful CI establishes pinned checkout/setup actions, Python 3.13, Node 24 and TeX Live 2026 as the current Linux runner pattern; B8 retains hosted Windows/font certification.

The clean-runner integration probe in the same run took 501 s and ended `PASS=22 FAIL=7 SKIP=1`. Its failures are current execution/artifact-contract defects, not evidence of a normative-rule regression: reference corpus path mismatch, stale CAPES path, detached object-geometry argument, objects/bibliography job-name drift, obsolete profile-matrix Makefile variable, stale appendix/annex evidence metadata, plus dependent reference-spacing skip. This makes clean-runner repair a prerequisite of permanent heavy orchestration.

### B7-B — Permanent fast/static workflow

**DONE** via PR #216 at **`643397ee2fa49e6bd496889cb287f43167d49b0f`**. `.github/workflows/static-contract.yml` is the permanent fast CI surface. Stable workflow/job name is `Static contract`; it runs for PRs to `main`, pushes to `main`, and manual dispatch, with read-only contents permission, bounded concurrency/cancellation, Ubuntu 24.04, Python 3.13 and Node 24. Its only product validation command is `make static-check`; YAML does not duplicate gate internals. Remote run **`33530718380` PASS** certified the workflow.

### B7-C — Optimized Linux integration/release orchestration

**ACTIVE.** Permanent heavy YAML remains blocked until the repository-owned integration entry point is clean-runner safe.

#### B7-C1 — Clean-runner integration contract repair

**DONE.** PR #220 squash-merged at **`ced68313ed2c362a6617d7df6ef9adfd2df6c0b5`**. Final clean TeX Live 2026 run **`33545418119` PASS** proved the repository-owned PR integration contract with **`PASS=30 FAIL=0 SKIP=0`**. Final `Static contract` run **`33547122520` PASS** executed after the temporary certification workflow was removed. No normative rule ID, expected value, tolerance, proof state, runtime/API or B8-owned certification semantic changed.

Completed bounded repair set:

- align reference corpus consumption with `template/main.*` production;
- resolve CAPES front-matter path from the repository root reliably;
- repair the object-geometry evidence argument invocation;
- make object and bibliography fixture job names match their inspected artifacts;
- replace the obsolete profile-matrix `filename=` Makefile call with current explicit compilation semantics;
- align appendix/annex evidence output with the current `engine_matrix_deferred` scenario field;
- rerun broad PR-mode validation and classify any newly exposed failure before touching workflow orchestration.

#### B7-C2 — Permanent Linux PR integration orchestration

**DONE** via PR #222 at **`cea59bcf4927da9a9c4a48268dca67cc9535854e`**. Permanent `Linux integration` uses the proven Linux/TeX runner environment, delegates the heavy gate to `make check`, exposes a stable PR status, skips heavy execution only for drafts and a narrow documentation/control-plane allowlist, fails closed for every other or unknown path, cancels superseded runs, and forces full validation on manual dispatch. PR runs `33548124803` (`Static contract`) and `33548124851` (`Linux integration`) passed; the integration contract closed `PASS=30 FAIL=0 SKIP=0`.

#### B7-C3 — Release orchestration

**ACTIVE.** Define and prove bounded permanent Linux release orchestration over `make release-check`, including trigger/cadence and artifact/evidence handling, without treating Linux release validation as final B8 Windows/font/PDF-A certification.

### B7-D — Residual audit and B8 handoff

**PENDING.** Audit permanent workflow ownership, stable check names, status semantics, concurrency/caching, temporary artifact absence and branch-protection recommendations, then activate B8.

## Remaining R1 blocks

- **R1-B4 DONE** — tools/validator/metadata rebaseline.
- **R1-B5 DONE** — deterministic public/class/CTAN/Overleaf distribution and reproducibility.
- **R1-B6 DONE** — permanent cheap/static fail-closed gate at `4c25c27b758e4b99db11187b34b9043776566871`.
- **R1-B7 ACTIVE** — optimized remote workflow restoration; B7-C2 is complete and B7-C3 release orchestration is active.
- **R1-B8 BLOCKED** — final R1 certification including Windows/font/PDF-A.

## Later phases

- **V3-R2:** direct runtime/API internationalization and Portuguese project API migration.
- **V3-R3:** standards/tests/language semantic hardening.
- **V3-R4:** certification only.
- **V3-R5:** foundation freeze plus current migration/user/maintainer documentation.
- **V3-A1/A2:** article work resumes only against the certified v3 foundation.

## Immediate action

Execute **B7-C2** from canonical remote `main` after this control-plane reconciliation. Add permanent Linux PR integration orchestration as a thin consumer of the certified `make check` contract, choose bounded triggers/concurrency so heavy TeX validation is not forced on every intermediate commit, and keep B7-C3 release orchestration, B8 Windows/font/final PDF-A certification, and V3-R2 runtime/API migration out of scope.
