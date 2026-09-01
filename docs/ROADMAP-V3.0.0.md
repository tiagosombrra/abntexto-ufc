# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-01

## Status

**V3-R1 ACTIVE — R1-BLOCK-4 done; R1-BLOCK-5 active; B5-A active.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B1 DONE → R1-B2 DONE → R1-B3 DONE → R1-B4 DONE → R1-B5 ACTIVE → R1-B6…B8 BLOCKED → R2+ BLOCKED**

B4 internal sequence:

**B4-A DONE → B4-B DONE → B4-C DONE [C1 DONE → C2a DONE → C2b DONE] → B4-D DONE**

- Canonical repository: `tiagosombrra/abntexto-ufc`.
- Active trunk: `main`.
- B5 operational issue: #199.
- Latest certified implementation checkpoint: **`1a126c37653728941ce1ada762376c5fec69cb02`**.
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

Run **`33502021542` PASS** validated cross-surface/validator contracts, full validator source, canonical identity, repository contract, syntax/JSON/diff integrity and explicit academic-label preservation. Run **`33502137178` PASS** removed the initial executor. Review found and blocked one accidental substring artifact before merge; run **`33506189097` PASS** repaired it, reran proportional gates and self-removed the repair workflow.

##### B4-C2b — diagnostics, report/export labels and Web UI

**DONE** via PR #197 at **`1a126c37653728941ce1ada762376c5fec69cb02`**. Project-owned CLI/Web diagnostics, evidence/correction messages, report/export labels, download names and generic validator UI were normalized to English. The Web UI now declares `lang=en`; fail-closed local-processing consumers moved together with the disclosure.

Evidence: `33506603720` inventory PASS; `33506913061` invalid oversized executor/no functional change; `33507239950` exposed a missing disclosure consumer; `33507392053` PASS after reconciliation; patch review exposed two PDF/UA residuals; `33507630613` failed closed on cardinality; **`33507724964` PASS** completed the review repair. Protected academic/normative/runtime boundaries and normative proof state remained unchanged.

### B4-D — Residual audit and closeout

**DONE.** Run `33508301453` performed the final ownership/consumer inventory and failed closed only because the temporary audit workflow contained its own retired-identity search literals; it also classified five version-labelled messages in the font-only integration gate as B8-owned residue. Corrected run **`33511105257` PASS** reconfirmed 10 tools, four validator files, all live consumers, B5/B8 assignments, language boundaries, atomic/cross-surface/validator contracts, validator-source checks, canonical identity, repository contract and diff integrity. The audit workflow self-removed and the audit branch has zero changed files versus `main`; no implementation merge was required.

## R1-BLOCK-5 — Distribution and Public Bundle Rebaseline

**ACTIVE.** Operational issue #199. Entry checkpoint: `1a126c37653728941ce1ada762376c5fec69cb02`.

Purpose: reconstruct the current public/distribution bundle contract from the v3 canonical tree. B5 will inventory producers and consumers, define the canonical source set and flatten/copy rules, reconcile manifests/policies/build-path integration, determine the current role of `tools/fetch-abntexto.py`, and make bundle generation deterministic and reproducible without reviving retired release scaffolding.

### B5-A — Inventory and distribution contract

**ACTIVE.** Fresh remote inventory first; historical distribution assumptions are advisory only. Map Makefile targets, build-path consumers, public bundle manifests/policies/evidence, runtime/support files, upstream inputs, and tracked distribution residue. Classify before editing.

## Remaining R1 blocks

- **R1-B4 DONE** — tools/validator/metadata rebaseline.
- **R1-B5 ACTIVE** — distribution/public bundle flattening and reproducibility.
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

Start **B5-A** from canonical `main` with implementation checkpoint `1a126c37653728941ce1ada762376c5fec69cb02` and issue #199. Produce a fresh remote distribution/public-bundle producer/consumer inventory and classify each current or residual surface before implementation. Keep B6 permanent gates, B7 permanent workflow restoration, B8 final certification and V3-R2 runtime/API work out of scope.
