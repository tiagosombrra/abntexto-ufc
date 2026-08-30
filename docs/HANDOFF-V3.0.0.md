# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-08-30

## Checkpoint

**V3-R0 is DONE. V3-R1 is ACTIVE.**

Certified v2 source baseline:

`main` `ce659b578b4fc9cc929af4aadc3e613df469ba77`

Active v3 implementation branch:

`refactor/v3-full-internationalization`

R0 contract commit:

`f512268661acbb79137cdcdacc94b82fa3dc1746`

R0 audited tree:

`657c7da1c4f0bd9e7353569fce59c0907c896ea7`

The previous branch `refactor/n15-b2r-c-full-english-canonicalization` is superseded. Do not copy implementation from it.

## Read first

Future sessions must read these in this order:

1. `docs/HANDOFF-V3.0.0.md`;
2. `docs/ROADMAP-V3.0.0.md`;
3. `release/v3-roadmap.json`;
4. `docs/ARCHITECTURE.md`;
5. `docs/ENGINEERING-LANGUAGE.md`;
6. active-phase contract;
7. current Git branch/head and open PR/CI state.

Current active-phase contract:

`release/v3-path-migration.json`

Do not infer phase state from branch names. `release/v3-roadmap.json` is the machine-readable phase authority.

## Frozen v3 architectural decisions

The following decisions are not open during R1/R2 unless an explicit architecture review reopens them:

- target major version is `3.0.0`;
- project engineering language is English;
- academic content language is independent and may remain Portuguese;
- official UFC/ABNT wording may remain in the source language;
- v3 provides no runtime Portuguese project API compatibility;
- `ufctex.cls` is removed;
- `abntexto-ufc.cls` is the sole canonical class entry point;
- canonical English API/state is implemented directly by behavior-owning modules;
- forwarding-only `abntexto-ufc/public-api.def` is removed after ownership absorption;
- repository editable source lives under `template/`;
- user/Overleaf bundles remain flattened for usability;
- `normativa/` becomes `standards/`;
- current upstream adaptations use `abntexto-ufc/integrations/` or `abntexto-ufc/standards/`, not `compat-*` naming;
- active tests use semantic names, not `v2-*` or historical N-phase names;
- upstream non-English identifiers may remain only when technically required and must not be re-exported as canonical project API.

## R0 deliverables

Frozen migration contracts:

- `release/v3-path-migration.json` — physical repository migration, rename/move/remove decisions and stale-path policy;
- `release/v3-api-migration.json` — public/internal runtime ownership, v2→v3 identifier map and removal policy;
- `release/v3-test-migration.json` — test/checker/fixture/workflow/documentation restructuring contract.

The contracts are deterministic migration inputs. R1/R2 implementation must update the contracts only if an actual contradiction is discovered, and such a change requires an explicit architecture rationale rather than an incidental implementation convenience.

## Current phase — V3-R1

Goal: perform physical repository restructuring without prematurely mixing in the canonical runtime rewrite assigned to R2.

Required R1 moves include:

- root editable project → `template/`;
- English names for project-owned template paths;
- `normativa/` → `standards/`;
- `tests/normativa/` → `tests/documents/`;
- Portuguese fixture/test filenames → English semantic filenames;
- active `v2-*` runners → semantic `tests/integration/` / `tests/checks/` names;
- `compat-abntexto.def` → `abntexto-ufc/integrations/abntexto.def`;
- `compat-nbr6023-2025.def` → `abntexto-ufc/standards/nbr6023-2025.def`;
- historical v2 phase ledgers/docs → history namespaces;
- all path references updated atomically.

R1 must not intentionally perform the full setup-key/command/internal-state migration. If a moved path requires a minimal source edit for resolution, make the smallest path-only change and leave semantic runtime renaming for R2.

R1 exit criteria:

1. no stale references to moved/renamed paths;
2. repository layout matches the path contract;
3. distribution staging can reconstruct the intended flattened bundle layout;
4. no generated build artifacts are tracked;
5. changes attributable to R2 are not hidden inside the physical migration;
6. human roadmap, machine roadmap and this handoff remain synchronized at phase closure.

## Next phase — V3-R2

Blocked until R1 closes.

Authority:

`release/v3-api-migration.json`

R2 will:

- convert setup keys/values to direct English runtime ownership;
- convert public commands/environments to direct English implementations;
- rename project-owned internal control sequences/state values to English;
- remove Portuguese project API surfaces;
- remove `ufctex.cls`;
- remove the forwarding-only `public-api.def` layer after ownership absorption;
- retain non-English upstream identifiers only at explicit integration boundaries.

Important: do not keep Portuguese runtime aliases for migration convenience. Migration support is documentation-only in v3.

## Later sequence

| Phase | Status | Purpose |
| --- | --- | --- |
| V3-R0 | DONE | architecture and deterministic migration contracts |
| V3-R1 | ACTIVE | physical repository restructuring |
| V3-R2 | BLOCKED | canonical English runtime |
| V3-R3 | BLOCKED | engineering-language enforcement |
| V3-R4 | BLOCKED | test architecture/regression reconstruction |
| V3-R5 | BLOCKED | documentation/distribution redesign |
| V3-A1 | BLOCKED | scientific article runtime |
| V3-A2 | BLOCKED | scientific article deep evidence |
| V3-H1 | BLOCKED | release hardening |
| V3-RC | BLOCKED | v3.0.0 release candidate |
| V3-FINAL | BLOCKED | exact-head certification/release decision |
| V3-CLEANUP | BLOCKED | branch/history cleanup after immutable release |

## Retained evidence from v2/N15

Do not repeat certified work blindly.

Retained as historical/scientific input:

- N0–N14 normative/runtime/evidence baseline;
- N15-A unrestricted audit;
- N15-B1 source/authority reconciliation;
- N15-B2A scientific-article source and normative contract;
- N15-B2R naming/API evidence.

Superseded architecture:

- additive PT↔EN runtime compatibility from N15-B2R;
- planned N15-B2B/B2C implementation sequence as a v2.2.0 release path.

Article work now resumes only after R5 as V3-A1/A2. Neither prior competing article PR should be merged wholesale into v3.

## Known release-hardening items

Still deferred to V3-H1 unless they become blockers earlier:

- GitHub issue #18: reference PDF bit reproducibility;
- determine whether `reference-validation.yml` provides unique value or should be removed;
- unrestricted final repository audit;
- license/distribution manifest verification;
- stale v2 planning-surface cleanup not already handled by R1/R5.

## Release guardrails

- UFC institutional mark and proprietary Microsoft fonts remain excluded from public bundles unless policy changes explicitly;
- literal Times New Roman/Arial certification remains a Windows Gate T responsibility;
- portable font fallback is not evidence of literal font identity;
- PDF/A-2b remains the project's technical certification target for the broader UFC PDF/A requirement unless a later source/technical decision changes it;
- do not tag/release from an uncertified head;
- branch cleanup remains post-release only;
- old Git tags/releases are historical evidence and must not be rewritten.

## Immediate next action

Execute V3-R1 from `release/v3-path-migration.json`, in bounded mechanical groups, verifying references after each group. Do not start V3-R2 runtime/API rewriting until R1 is explicitly closed in both roadmaps and this handoff.
