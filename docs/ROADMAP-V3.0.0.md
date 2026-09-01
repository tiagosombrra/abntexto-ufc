# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-01

## Status

**V3-R1 ACTIVE — R1-BLOCK-3 is closed; R1-BLOCK-4 is active.**

Current sequence:

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B1 DONE → R1-B2 DONE → R1-B3 DONE → R1-B4 ACTIVE → R1-B5…B8 BLOCKED → R2+ BLOCKED**

- Canonical repository: `tiagosombrra/abntexto-ufc`.
- Active branch/trunk: `main`.
- Latest certified clean implementation checkpoint: `7a3b018a43630ed46b375117790acc732ae67b40`.
- R1-BLOCK-3 closure checkpoint: `7a3b018a43630ed46b375117790acc732ae67b40`.
- R1-S2 promotion checkpoint: `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`.
- Certified v2 baseline: `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

## Authority

Current Git facts and canonical machine state must agree. `release/v3-roadmap.json` is machine authority; `docs/HANDOFF-V3.0.0.md`, this roadmap, and `AGENTS.md` define the human-readable state and bootstrap. Disagreement fails closed.

`main` is the canonical trunk/merge target. Short-lived branches are implementation vehicles only.

## Completed reconstruction stages

### R1-S0 — Repository sanitation

**DONE.** Full-history backup verified before ref cleanup; stale legacy/process refs retired; immutable tags preserved.

### R1-S1 — Control plane repair

**DONE** at `1c7291592689f10a0e6fb043d404597ae8e53c02`.

### R1-S2 — Trunk rebaseline

**DONE** at `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1`. v3 promoted to `main` without history rewrite; agreed reference/static gates passed.

### R1-BLOCK-1 — Canonical physical naming

**DONE** at `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd`.

### R1-BLOCK-2 — Legacy purge and active-tree minimization

**DONE** at `03d7f5ceb1a325d26c712ba5e619ee85530a022b`.

### R1-BLOCK-3 — Semantic / Path-Consumer Closure

**DONE** at `7a3b018a43630ed46b375117790acc732ae67b40`.

Internal closure sequence:

**B3-A DONE → B3-B DONE → B3-C DONE → B3-D DONE → B3-E DONE → B3-F DONE**

Key checkpoints:

- B3-A path-consumer reconciliation — PR #159, `e4bf60836ac7a9cd1d544232b9a4e1ef019efe04`;
- B3-B process-identity closure — PR #160, `dbc7f774df2cd0ac1b0f6479653290c6f19b6809`;
- B3-C final checker closure — PR #169, `625e82f9ef4780989d4635e500d72d09eab02992`;
- B3-D legacy identity/dead-code purge — `8f7c05b32f228633e4802a6fa8c14babf16fd685`;
- B3-E project-owned oracle terminology — PR #182, `bf36982ab2ff08b8585c4acc570c48364e9ecc1f`;
- B3-F final residual closure — PR #185, `7a3b018a43630ed46b375117790acc732ae67b40`.

Block 3 final evidence:

- repository contract PASS: 392 tracked files, zero history directories, zero legacy class;
- canonical class identity PASS: 14 modules aligned;
- zero retired v2/N9–N15/B2R active path identities;
- zero unclassified active project-owned `oracle` identity;
- stale font POC path/job identity repaired;
- no temporary workflow/executor retained;
- relevant Python/shell syntax and `git diff --check` PASS;
- no runtime/API, normative rule/value/tolerance, proof-state, distribution, permanent-CI, or certification changes introduced by B3-F.

## R1-BLOCK-4 — Tools, Validator, and Metadata Technical Rebaseline

**ACTIVE.**

Purpose: make project-owned tooling, validator, and technical metadata reflect the final R1 v3 architecture instead of carrying inherited v2/process-era language, dead helpers, stale ownership, or stale repository/package metadata.

### B4 entry inventory

Audit current live-tree surfaces:

1. `tools/`
   - current developer helpers;
   - fetch/measurement/certification helpers;
   - dead or duplicated utilities;
   - helpers explicitly owned by B5 or B8.
2. `validator/`
   - source filenames and module ownership;
   - project-owned identifiers, controls, diagnostics, labels, and CLI/help text;
   - Portuguese technical language versus legitimate Portuguese document data;
   - stale assumptions about old paths/version/repository identity.
3. current metadata/technical prose consumed by code
   - version/package/repository strings;
   - control descriptions and diagnostic terminology;
   - migration metadata only where still actively consumed.

### B4 classification rules

Every finding must be classified as one of:

- current v3 technical surface — retain or normalize now;
- assigned B5 distribution helper — retain for B5;
- assigned B8 certification helper — retain for B8;
- explicit upstream/integration boundary — retain dependency-owned spelling;
- document/rendered Portuguese data — retain;
- dead/superseded helper or metadata — remove;
- R2 runtime/API surface — defer intact to R2.

### B4 constraints

- project-owned engineering identifiers, diagnostics, and technical labels are English;
- do not translate academic/rendered content merely because it is Portuguese;
- do not rewrite current Portuguese runtime API in R1;
- do not implement B5 bundles, B6 permanent gates, B7 CI, or B8 certification;
- preserve normative rule IDs, expected numeric values, numeric tolerances, and proof state;
- no archive/museum files;
- no blind global replacement;
- producer/consumer changes move together;
- bounded lots with proportional validation only.

### B4 acceptance criteria

B4 closes when:

- every active `tools/` helper has a current or explicitly assigned later-block consumer;
- dead tooling is absent from the active tree;
- validator implementation/CLI/diagnostics use coherent project-owned English technical identity;
- metadata consumed by active tools/validator reflects v3/current repository identity;
- dependency-owned and document-language exceptions are explicitly classifiable;
- tool/validator source checks and relevant syntax/contract checks pass;
- no B5–B8 or R2 implementation is prematurely absorbed;
- final B4 residual audit is clean and any temporary executor is removed before merge.

## Remaining R1 blocks

- **R1-B4 ACTIVE:** tools, validator, metadata technical rebaseline.
- **R1-B5 BLOCKED:** distribution/public bundle flattening and reproducibility.
- **R1-B6 BLOCKED:** permanent cheap/static fail-closed gates.
- **R1-B7 BLOCKED:** optimized workflow restoration.
- **R1-B8 BLOCKED:** final R1 certification, including Windows/font/PDF-A certification.

## R1 exit criteria

R1 closes only when the active product tree has no historical/process artifact competing with current state, no dead helper without a consumer, no stale paths or generated migration scaffolding, coherent project-owned technical language, resolvable canonical build/tool/test/distribution paths, and agreement among Git facts, handoff, roadmap, machine state, governance, and final certification evidence.

## Later phases

- **V3-R2:** direct runtime/API internationalization and removal/absorption of Portuguese project API aliases.
- **V3-R3:** standards/tests/language semantic hardening.
- **V3-R4:** certification only.
- **V3-R5:** foundation freeze plus current migration/user/maintainer documentation.
- **V3-A1/A2:** article work resumes only against the certified v3 foundation.

## Immediate action

Begin **R1-BLOCK-4** at implementation checkpoint `7a3b018a43630ed46b375117790acc732ae67b40`. Open a B4 operational issue and perform a fresh remote inventory of `tools/`, `validator/`, and active technical metadata. Classify findings before editing, then execute bounded cleanup lots with lightweight validation and no permanent workflow.
