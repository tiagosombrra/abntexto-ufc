# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-01

## Status

**V3-R1 ACTIVE — R1-BLOCK-3 remains active; B3-A, B3-B and B3-C are closed on `main`; B3-D is active.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B3 ACTIVE → R1-B4…B8 BLOCKED → R2+ BLOCKED**

Block 3 internal sequence:

**B3-A DONE → B3-B DONE → B3-C DONE → B3-D ACTIVE → B3-E PENDING → B3-F PENDING**

- Canonical repository: `tiagosombrra/abntexto-ufc`.
- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `2ad7da8eae03c40fbea3d875843628387ec0e25d`.
- R1-S2 promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- R1-S1 closure: `1c7291592689f10a0e6fb043d404597ae8e53c02`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

The GitHub repository was renamed to `abntexto-ufc` on 2026-09-01 without changing repository identity, history, tags, issues, pull requests, or governance. The former repository name is not an active technical identity.

## Authority and bootstrap

Current Git facts and the canonical machine state must agree. `release/v3-roadmap.json` declares intended phase/stage; `docs/HANDOFF-V3.0.0.md` and this roadmap explain that state. `AGENTS.md` defines the mandatory session bootstrap.

`main` is the canonical trunk and merge target. Short-lived task branches are permitted, but they do not replace `main` as the control-plane `active_branch`.

If Git, machine state, handoff, roadmap, workflow inventory, or temporary-artifact inventory disagree, advancement fails closed. Memory, historical branches, old PRs, old workflows, and prior chat context are not phase authorities.

## R1-S0 — Repository Sanitation & Control Rebaseline

**DONE.**

- verified Git mirror and full-history bundle created before ref deletion;
- stale/abandoned audit, v2.x, N-phase/N15/B2R, preview, maintenance, release, temporary, legacy `1.x`, and abandoned v3 refs removed from the active namespace;
- PRs #157 and #158 closed as superseded;
- immutable release tags preserved;
- active branch governance reduced to `main` plus short-lived task branches.

No archive replacement branches are permitted in the active repository.

## R1-S1 — Control Plane Repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`.

The abandoned temporary migration workflow/executor was removed, root `AGENTS.md` was added, and canonical state/docs were synchronized. The abandoned executor did not certify additional Block 3 implementation work.

## R1-S2 — Trunk Rebaseline

**DONE.**

The v3 line was promoted to `main` by direct fast-forward without rewriting history. Reference build and agreed promotion gates passed; permanent CI remained intentionally absent. The stale `latex-preflight` requirement remains deferred until Block 7.

## R1 Block 3 — Semantic / Path-Consumer Closure

**ACTIVE.**

### B3-A — Path-consumer reconciliation

**DONE** through PR #159 at `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`.

This lot reconciled stale active paths and producer/consumer path references without absorbing later distribution or CI work.

### B3-B — Normative process-identity closure

**DONE** through PR #160 at `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`.

Closure evidence:

- obsolete validator/scenario phase ownership removed;
- obsolete active phase-qualified marker/process identity removed;
- 172 markers migrated to functional namespaces;
- active N6/N9/N10 markers: 0;
- stale active phase diagnostics: 0;
- active lower-case N5–N15 process identity in B3-B scope: 0;
- active legacy `N*-EVIDENCE` labels: 0;
- producer/consumer mismatches: 0;
- marker namespace collisions: 0;
- rule IDs, numeric expected values, numeric tolerances, proof state, and runtime/API semantics preserved.

Functional differential validation classified 29/29 relevant tests: 21 PASS, 8 baseline-equivalent pre-existing blocks, 0 introduced regressions, and 0 unresolved classifications.

### B3-C — Runner/evidence integrity and bounded portability

**DONE.**

B3-C closed the eight defects exposed by B3-B differential validation without changing normative rule IDs, expected numeric values, numeric tolerances, proof state, or runtime/API semantics.

B3-C1 merged through replacement PR #168 at `da775552be190bf09d8a790c33e9f7f4582da699` and reconciled:

- catalog-card runner/file handoff;
- long-quotation evidence producer/consumer path;
- research-project TeX job/Biber artifact naming;
- short direct citation UTF-8 checker process;
- vector-rule validation tolerance-key bindings;
- table-IBGE same-run vector calibration production.

The original draft PR #164 was closed unmerged solely because the connector could not transition its draft state; PR #168 used the same implementation branch/content.

B3-C2 merged through PR #169 at `625e82f9ef4780989d4635e500d72d09eab02992` and reconciled:

- appendix/annex obsolete undefined-`scope` process-progress accounting while preserving the exact 13-rule campaign;
- footnote separator vector extraction by replacing the bespoke stroked-line-only parser with the shared vector-rule parser, retaining the same 50 mm length, left-margin origin, vertical relation, and validation-policy tolerances.

Issue #163 is closed as the B3-C operational continuity record. No temporary validation workflow remains.

### B3-D — Operational v1/v2 identity and legacy-code purge

**ACTIVE.**

B3-D closes stale version-qualified technical identity and dead/superseded legacy implementation artifacts that survived earlier structural cleanup.

Completed bounded lots:

- **B3-D1** — stale runner identity in catalog-card, research-project and font POC;
- **B3-D2A** — stale `V2` gate/diagnostic labels removed from six runners, merged at `f4d703b34df53868f782598dd9502c0da684c345`;
- **B3-D2B** — stale v2-qualified temporary fixture/log identity removed from five runners with producer/consumer paths changed together, merged at `094b369a077009f212adb33e8a814ee9bb167b4a`;
- **B3-D3** — active version identity moved from 2.1.0 to target 3.0.0 in `Makefile` and `abntexto-ufc.cls`; the broken `distribution-source` coordinated gate was removed; dead `tests/integration/distribution.sh` was deleted, merged at `2ad7da8eae03c40fbea3d875843628387ec0e25d`.

B3-D3 confirmed that the removed distribution runner was dead legacy code, not a compatibility boundary: it required missing `tests/v2-*` helpers, missing `ufctex.cls`, removed workflows, and obsolete root-layout paths. Current distribution/public-bundle validation will be reconstructed in B5 from current paths and contracts.

B3-D acceptance criteria:

- zero active file/directory names that identify current engineering surfaces as `v1`, `V1`, `v2`, or `V2`;
- zero current runner/log/temp/gate identity qualified as v1/v2;
- canonical current package/class metadata identifies target v3.0.0;
- dead or superseded v1/v2-era code/tests with no current consumer are removed rather than renamed or archived in the active tree;
- every remaining textual v1/v2 reference is explicitly classifiable as certified history, migration contract, compatibility boundary, or negative test;
- references to distribution/release helpers are audited before deferral and may remain only with an assigned future consumer;
- no runtime/API compatibility boundary assigned to R2 is rewritten early.

The current physical product layout is v3-oriented and does not contain an active v1/v2 product hierarchy. Remaining B3-D work is concentrated in inherited runners and explicit legacy references.

### B3-E — Project-owned oracle terminology

**PENDING.**

Replace project-owned engineering `oracle` terminology where it represents obsolete implementation naming. Preserve legitimate theoretical/testing uses of the term.

### B3-F — Final Block 3 residual audit

**PENDING.**

Run a live-tree residual audit after B3-D/E, verify producer/consumer integrity and control-plane agreement, and close R1-BLOCK-3 only if no active Block 3 residue remains.

Do not absorb later-block responsibilities into B3. Distribution/public bundle reconstruction, permanent CI, Overleaf/CTAN, Windows-font certification, PDF/A certification, and other heavyweight surfaces stay in their assigned later blocks.

R1 must not rewrite the Portuguese runtime API; that belongs to R2.

## Remaining R1 blocks

- **R1-B4:** tools, validator, and metadata technical rebaseline.
- **R1-B5:** distribution/public bundle flattening and reproducibility.
- **R1-B6:** permanent cheap/static fail-closed gates.
- **R1-B7:** optimized permanent workflow restoration.
- **R1-B8:** final clean-tree, repository identity, branch policy, documentation, state, checks, and asset certification, including final Windows/font/PDF-A certification.

## R1 exit criteria

R1 closes only when a new maintainer or agent can open the repository and determine the current state without reconstructing historical context.

Required conditions include:

- no historical/process artifact competing with active state;
- no dead migration artifact without an active consumer;
- no dead legacy implementation/test artifact retained merely for reference;
- no archive/history tree in the active product repository;
- zero obsolete physical paths and stale active references;
- zero generated or temporary migration scaffolding;
- every retained legacy-version reference has an explicit active classification;
- project-owned technical surfaces follow the engineering-language policy;
- canonical build/tool/test/distribution paths resolve;
- static gates pass;
- optimized CI cannot spam intermediate commits;
- branch policy, roadmap, machine state, and handoff agree.

## Later phases

- **V3-R2:** direct runtime/API internationalization and removal/absorption of Portuguese project API aliases.
- **V3-R3:** standards/tests/language semantic hardening.
- **V3-R4:** certification only.
- **V3-R5:** foundation freeze and current migration/user/maintainer documentation only.
- **V3-A1/A2:** article work returns only against the certified v3 foundation.
- Later H1/RC/FINAL/CLEANUP phases follow in order.

## Immediate action

Continue **B3-D** from canonical remote `main` at implementation checkpoint `2ad7da8eae03c40fbea3d875843628387ec0e25d`. Finish remaining operational v2/V2 runner cleanup, classify surviving legacy-version references, and audit release/distribution helpers for real B5 consumers. Delete dead/superseded artifacts rather than preserving them. Then proceed to B3-E and B3-F without absorbing R2 or B5–B8 implementation work.
