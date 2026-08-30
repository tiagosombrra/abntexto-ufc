# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**ACTIVE — V3-R1 physical repository restructuring.**

Certified v2 source baseline:

`main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`

Active v3 branch:

`refactor/v3-full-internationalization`

V3-R0 was closed after the exhaustive repository/API/test migration contracts were frozen in commit:

`f512268661acbb79137cdcdacc94b82fa3dc1746`

The previous experimental branch `refactor/n15-b2r-c-full-english-canonicalization` is superseded and must not be used as an implementation source.

## Current authorities

Read these in order before continuing implementation:

1. `docs/HANDOFF-V3.0.0.md`;
2. `docs/ROADMAP-V3.0.0.md`;
3. `release/v3-roadmap.json`;
4. `docs/ARCHITECTURE.md`;
5. `docs/ENGINEERING-LANGUAGE.md`;
6. `release/v3-path-migration.json`;
7. `release/v3-api-migration.json`;
8. `release/v3-test-migration.json`.

The machine-readable phase authority is `release/v3-roadmap.json`.

## Why v3

The v2.x line introduced an additive English API while retaining Portuguese technical identifiers and compatibility wrappers. The v3 decision is intentionally breaking and stricter:

- one canonical engineering language: English;
- one canonical project public API: English;
- one canonical project internal runtime vocabulary: English;
- no Portuguese compatibility API in the v3 runtime;
- no deprecated `ufctex.cls` compatibility entry point;
- no forwarding-only `public-api.def` layer;
- project-owned paths, scripts, fixtures, diagnostics, comments and active technical documentation use English;
- academic/example content may remain in Portuguese because document language is independent from engineering language;
- official institutional/normative wording may remain in the authoritative language.

Removing the published v2 Portuguese API is a breaking change, therefore the target is **v3.0.0**.

## Non-negotiable language boundary

Must be English when project-owned:

- repository directories and filenames;
- LaTeX public commands, environments, setup keys and technical values;
- LaTeX internal control sequences and state values;
- comments and technical diagnostics in `.def`, `.cls`, `.py`, `.sh`, `.ps1`, workflows and Makefiles;
- test, fixture, checker and CI engineering names;
- active engineering documentation and machine-readable schema fields;
- release/distribution tooling and metadata.

May remain in Portuguese when it is content/evidence rather than project engineering nomenclature:

- rendered academic prose and headings;
- sample UFC academic metadata;
- bibliography data;
- official UFC/ABNT names, acts and guide titles;
- direct normative wording;
- test payload text when Portuguese output is the behavior being tested;
- upstream non-English identifiers that the project must call at an explicit integration boundary.

## Target repository architecture

```text
.
├── abntexto-ufc.cls
├── abntexto-ufc/
│   ├── core.def
│   ├── fonts.def
│   ├── layout.def
│   ├── modules.def
│   ├── frontmatter.def
│   ├── institutional.def
│   ├── academic-works.def
│   ├── research-projects.def
│   ├── articles.def                 # introduced only in V3-A1
│   ├── objects.def
│   ├── bibliography.def
│   ├── backmatter.def
│   ├── integrations/
│   │   └── abntexto.def
│   └── standards/
│       └── nbr6023-2025.def
├── template/
│   ├── main.tex
│   ├── frontmatter/
│   ├── chapters/
│   ├── backmatter/
│   └── figures/
├── assets/institutional/
├── standards/
├── tests/
│   ├── checks/
│   ├── documents/
│   ├── fixtures/
│   ├── integration/
│   └── smoke/
├── tools/
├── validator/
├── docs/
├── release/
└── .github/workflows/
```

Repository and distribution layout are intentionally different: the repository stores the editable project below `template/`; user/Overleaf bundles flatten it so users still receive root-level `main.tex`, `frontmatter/`, `chapters/`, `backmatter/` and `figures/`.

## Architectural principles

1. Single ownership: every project behavior/policy has one runtime owner.
2. No compatibility indirection: v3 removes Portuguese project API aliases and `ufctex.cls`.
3. No cosmetic wrappers: public commands express supported semantic capabilities.
4. English-first implementation: canonical English identifiers directly own runtime behavior/state.
5. Content/runtime separation: Portuguese academic output is content, not engineering nomenclature.
6. Repository/distribution separation: source maintainability does not dictate user bundle ergonomics.
7. Machine-enforced invariants: path language, naming, ownership, stale references and release metadata are checked.
8. Historical evidence remains history: old ledgers are preserved but do not control v3 runtime naming.
9. Runtime phases do not close on documentation alone.
10. Final release requires exact-head certification.

## Phase plan

### V3-R0 — Architecture and migration contract

Status: **DONE**

Closed by contract commit `f512268661acbb79137cdcdacc94b82fa3dc1746`.

Frozen deliverables:

- `release/v3-path-migration.json` — deterministic physical-path classification and migration map;
- `release/v3-api-migration.json` — canonical v3 public/internal API ownership and removal map;
- `release/v3-test-migration.json` — semantic test/fixture/workflow/documentation migration contract.

Key decisions frozen by R0:

- `ufctex.cls` is removed in v3;
- `abntexto-ufc/public-api.def` is removed after canonical responsibilities are absorbed directly by owning modules;
- Portuguese v2 project API aliases are not retained at runtime;
- `main.tex` and editable academic source move to `template/` in the repository;
- `normativa/` becomes `standards/`;
- `tests/normativa/` becomes `tests/documents/`;
- active test runners use semantic names rather than `v2-*` or historical phase identifiers;
- Portuguese academic content remains valid inside English-named files;
- upstream non-English identifiers are allowed only where technically required at explicit integration boundaries.

R0 had no runtime change, so no new runtime certification was required to close the planning contract.

### V3-R1 — Physical repository restructuring

Status: **ACTIVE**

Authority: `release/v3-path-migration.json`.

Scope:

- move the editable reference project under `template/`;
- rename project-owned Portuguese paths to English;
- move `normativa/` to `standards/`;
- rename/reorganize active test documents, fixtures and integration runners;
- move current upstream adaptation modules to `abntexto-ufc/integrations/` and `abntexto-ufc/standards/`;
- move v2 historical ledgers/docs out of active v3 engineering surfaces;
- update path references atomically;
- keep runtime semantic rewrites out of R1 unless minimally necessary to preserve path resolution.

Exit criteria:

- zero stale references to moved paths;
- target repository structure matches the R0 contract;
- distribution staging can still reconstruct the intended flattened user bundle;
- no generated artifacts are tracked;
- R1 restructuring does not accidentally introduce the R2 canonical-runtime rewrite early.

### V3-R2 — Canonical English runtime

Status: **BLOCKED by V3-R1**

Authority: `release/v3-api-migration.json`.

Scope:

- make English setup keys and values direct runtime owners/state;
- make English commands/environments direct implementations;
- rename project-owned internal identifiers to English;
- remove Portuguese public API and compatibility forwarding;
- remove `public-api.def` after ownership absorption;
- remove `ufctex.cls`;
- preserve upstream identifiers only at explicit integration boundaries.

Exit criteria:

- one project public API only;
- zero project-owned Portuguese API/internal identifiers in active runtime;
- no compatibility forwarding layer;
- all supported profiles compile through canonical v3 API.

### V3-R3 — Engineering-language enforcement

Status: **BLOCKED by V3-R2**

Scope: enforce English project-owned comments, diagnostics, CI labels, scripts and active engineering prose while preserving intentional Portuguese academic content and authoritative source wording.

Exit criteria: project-owned Portuguese technical paths/comments/diagnostics/canonical examples = 0, subject to scoped semantic exemptions.

### V3-R4 — Test architecture and regression reconstruction

Status: **BLOCKED by V3-R3**

Authority: `release/v3-test-migration.json`.

Scope: rebuild the active suite around semantic v3 contracts, remove PT↔EN compatibility tests, preserve valid normative/layout/font/PDF-A evidence, restore module ownership/repository audits and update distribution/workflow path assumptions.

### V3-R5 — Documentation and distribution redesign

Status: **BLOCKED by V3-R4**

Scope: English-first README/CTAN/maintainer docs, human migration guide from v2, canonical examples and distribution/Overleaf staging from `template/` with no executable legacy compatibility layer.

### V3-A1 — Scientific article runtime architecture

Status: **BLOCKED by V3-R5**

Supersedes N15-B2B. Reuse the already reviewed N15-B2A article source/normative contract, but implement the runtime anew against the v3 architecture. Do not merge either old competing B2B implementation wholesale.

### V3-A2 — Scientific article deep evidence

Status: **BLOCKED by V3-A1**

Supersedes N15-B2C. Certify the 13 article predicates at the strongest justified evidence level and keep advisory recommendations advisory.

### V3-H1 — Release hardening

Status: **BLOCKED by V3-A2**

Absorbs remaining N15-B3 work, including GitHub issue #18 (reference-PDF bit reproducibility), obsolete workflow review, unrestricted audit, license/distribution verification and stale-surface cleanup.

### V3-RC — v3.0.0 release candidate

Status: **BLOCKED by V3-H1**

Atomically promote all version surfaces to 3.0.0, build local/template/Overleaf/CTAN candidates, perform controlled double builds and certify exact head.

### V3-FINAL — Exact-head certification and release decision

Status: **BLOCKED by V3-RC**

Required exact-head gates include standards/source contract, repository audit, LaTeX preflight, PDF/A, Windows literal fonts/Gate T, Overleaf import proxy and Distribution preflight. Release/tag only after all required gates succeed and the protected merge state is exact.

### V3-CLEANUP — Post-release repository cleanup

Status: **BLOCKED by V3-FINAL**

Delete superseded implementation/audit branches only after immutable v3.0.0 release/tag exists. Preserve historical evidence through Git/history rather than active compatibility runtime.

## Mapping from the previous plan

| Previous work | v3 treatment |
| --- | --- |
| N0–N14 | certified historical evidence; do not repeat blindly |
| N15-A | unrestricted audit input retained |
| N15-B1 | source/authority reconciliation retained |
| N15-B2A | article normative contract retained |
| N15-B2R | historical naming evidence retained; additive compatibility architecture superseded |
| N15-B2B | superseded by V3-A1 |
| N15-B2C | superseded by V3-A2 |
| N15-B3 | absorbed by V3-H1 |
| N15-C | superseded by V3-RC |
| N15-D | superseded by V3-FINAL |

## Current next action

Execute **V3-R1** exactly from `release/v3-path-migration.json`. Do not begin canonical runtime/API rewriting until the physical restructuring and stale-path checks satisfy the R1 exit criteria.
