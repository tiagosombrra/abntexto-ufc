# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**ACTIVE — V3-R1 complete repository rebaseline.**

Certified v2 baseline: `main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

Clean v3 planning baseline: `ca2ab12163d16e5eef80c0c8ce9fea543064ab10`.

Active implementation branch: `refactor/v3-r1-rebaseline`.

Superseded implementation branches:

- `refactor/v3-full-internationalization`;
- `refactor/v3-foundation-cleanup`;
- `refactor/n15-b2r-c-full-english-canonicalization`.

These branches are historical evidence only, not implementation sources.

## Current authorities

Read in order:

1. `docs/HANDOFF-V3.0.0.md`;
2. `docs/ROADMAP-V3.0.0.md`;
3. `release/v3-roadmap.json`;
4. `docs/ARCHITECTURE.md`;
5. `docs/ENGINEERING-LANGUAGE.md`;
6. `release/v3-path-migration.json`;
7. `release/v3-api-migration.json`;
8. `release/v3-test-migration.json`.

`release/v3-roadmap.json` is the machine-readable phase authority.

## No-debt execution policy

1. No known active-tree debt in a phase scope may cross that phase gate.
2. No temporary migration workflow, rewrite script, compatibility shim or path bridge survives V3-R1.
3. Historical evidence may retain old names, but active code, tests, tools, CI, distribution, validator and engineering documentation must not depend on them.
4. V3-R1 starts with GitHub Actions disabled on the reconstruction branch.
5. Heavy automatic CI is not enabled during R1.
6. Workflows are restored only after their paths and semantics have been deliberately migrated.
7. V3-R4 is certification only; it cannot receive deferred migration, cleanup, path repair or naming repair.

## Frozen architectural decisions

- target release `3.0.0`;
- project engineering language English;
- academic content may remain Portuguese;
- official UFC/ABNT wording may remain in its authoritative language;
- one canonical project runtime API, in English;
- no Portuguese project runtime aliases;
- `ufctex.cls` removed in v3;
- `abntexto-ufc.cls` is the sole canonical class entry point;
- English API/state directly owns behavior;
- forwarding-only `abntexto-ufc/public-api.def` removed after ownership absorption;
- editable document source under `template/`;
- public template/Overleaf bundles flatten `template/` to bundle root;
- `normativa/` → `standards/`;
- upstream integration under `abntexto-ufc/integrations/`;
- standard adapters under `abntexto-ufc/standards/`;
- active tests use semantic names rather than version/phase identifiers;
- upstream non-English identifiers may remain only at explicit integration boundaries.

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
│   ├── integrations/abntexto.def
│   └── standards/nbr6023-2025.def
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
└── .github/workflows/               # restored only after migrated
```

Repository and distribution layouts are intentionally different. The repository keeps editable sources under `template/`; public bundles expose `main.tex`, `frontmatter/`, `chapters/`, `backmatter/` and `figures/` at bundle root.

## V3-R0 — Architecture and deterministic migration contracts

Status: **DONE**.

Contract commit: `f512268661acbb79137cdcdacc94b82fa3dc1746`.

Frozen inputs:

- `release/v3-path-migration.json`;
- `release/v3-api-migration.json`;
- `release/v3-test-migration.json`.

## V3-R1 — Complete repository rebaseline

Status: **ACTIVE**.

Authority: `release/v3-path-migration.json`.

R1 is not merely a file move. It must leave the entire active repository structurally coherent before R2 begins.

Required scope:

- establish final repository directory layout;
- move editable academic sources under `template/`;
- rename project-owned technical paths and filenames to English;
- move `normativa/` to `standards/`;
- move `tests/normativa/` to `tests/documents/`;
- reorganize fixtures, runners, checkers and smoke tests under semantic names;
- move current abntexto integration to `abntexto-ufc/integrations/abntexto.def`;
- move NBR 6023 adapter to `abntexto-ufc/standards/nbr6023-2025.def`;
- isolate historical v2/N15 evidence under history namespaces;
- update `template/main.tex` and every active path reference;
- update `abntexto-ufc.cls` module loading paths;
- update `Makefile`, `tools/` and validator path assumptions;
- migrate every active GitHub workflow, including `latex-preflight.yml`, before restoring it;
- adapt distribution and Overleaf staging to flatten `template/`;
- preserve functional tests while changing structural/path assumptions;
- add a permanent structural/path contract checker;
- remove all temporary migration workflows/scripts before R1 closes.

R1 deliberately does not perform the full Portuguese-to-English runtime API rewrite assigned to R2.

R1 exit gate:

- zero obsolete physical paths;
- zero stale path references in the active tree;
- zero project-owned Portuguese technical filenames/directories;
- zero active `v2-*`, historical N-phase or equivalent phase-coded technical filenames;
- zero active dependencies on historical evidence paths;
- all tools, tests and restored workflows use canonical v3 paths;
- `template/main.tex` resolves/builds from its repository location;
- `abntexto-ufc.cls` loads only canonical repository paths;
- distribution staging flattens `template/` correctly;
- Overleaf bundle has root-level `main.tex`;
- permanent repository/path audit passes;
- no generated artifacts are tracked;
- no temporary migration scaffolding remains;
- roadmap, machine roadmap and handoff are synchronized.

Only then may R1 become DONE and R2 become ACTIVE.

## V3-R2 — English-only canonical runtime

Status: **BLOCKED by V3-R1**.

Authority: `release/v3-api-migration.json`.

Scope:

- English setup keys/values directly own runtime state;
- English public commands/environments directly own behavior;
- project-owned internal control sequences and state identifiers become English;
- Portuguese project runtime API/aliases are removed;
- forwarding-only `public-api.def` is dismantled after ownership absorption;
- `ufctex.cls` is removed;
- source comments, warnings, errors and technical diagnostics become English;
- upstream non-English identifiers remain only at explicit integration boundaries.

`article` remains reserved and must not become live during R2.

## V3-R3 — Standards, tests and engineering-language semantic hardening

Status: **BLOCKED by V3-R2**.

Authority: `release/v3-test-migration.json`.

Scope:

- semantically review `standards/`, not only its paths;
- remove obsolete v2 PT↔EN compatibility-equivalence tests;
- preserve or strengthen functional regression coverage;
- make tests/checkers/fixtures independent of historical phase naming;
- enforce the permanent engineering-language contract;
- permit Portuguese only for academic output, official/normative source wording, bibliography data, Portuguese fixture payloads when behavior under test, localized validator UI, and technically required upstream identifiers at explicit integration boundaries.

Exit gate: zero project-owned Portuguese technical language in active engineering surfaces, subject only to these explicit semantic exceptions.

## V3-R4 — CI, release and distribution certification

Status: **BLOCKED by V3-R3**.

R4 is certification only. It must certify the already-clean R1–R3 result through, as applicable:

- Linux and Windows;
- pdfLaTeX and LuaLaTeX;
- Windows literal Times New Roman/Arial Gate T;
- PDF/A-2b technical target;
- template bundle;
- Overleaf proxy/import bundle;
- CTAN bundle;
- distribution manifest/content inspection;
- deterministic/reproducibility checks, including GitHub issue #18 disposition;
- independent clean builds.

No structural migration, naming cleanup or runtime rewrite may be deferred to R4.

## V3-R5 — Foundation freeze and migration documentation

Status: **BLOCKED by V3-R4**.

Freeze the certified v3 foundation, synchronize user/maintainer documentation, document v2→v3 migration without runtime compatibility, and ensure examples describe certified artifacts exactly.

## Later phases

| Phase | Status | Purpose |
| --- | --- | --- |
| V3-A1 | BLOCKED | scientific article runtime, reimplemented against v3 |
| V3-A2 | BLOCKED | scientific article deep evidence |
| V3-H1 | BLOCKED | hardening after article integration |
| V3-RC | BLOCKED | v3.0.0 release candidate |
| V3-FINAL | BLOCKED | exact-head certification and release decision |
| V3-CLEANUP | BLOCKED | post-release branch/history cleanup |

V3-A1 reuses the N15-B2A article normative contract as scientific input, but neither previous competing B2B implementation is merged wholesale.

## Retained evidence and guardrails

Retain N0–N14 certification evidence, N15-A audit input, N15-B1 source reconciliation, N15-B2A article normative contract and N15-B2R naming evidence. The additive PT↔EN runtime compatibility architecture is superseded.

Public bundles continue to exclude the UFC institutional mark and proprietary Microsoft fonts unless policy changes explicitly. Literal Times New Roman/Arial identity remains a Windows Gate T responsibility. Portable fallback does not prove literal font identity. PDF/A-2b remains the project's technical certification target for UFC's broader PDF/A requirement.

## Immediate action

Execute V3-R1 on `refactor/v3-r1-rebaseline`, with GitHub Actions initially disabled. Reconstruct the active tree in bounded, reviewable commits and do not start R2 until the complete R1 gate passes.
