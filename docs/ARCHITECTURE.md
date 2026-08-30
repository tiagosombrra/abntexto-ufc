# abntexto-ufc v3 Architecture

Updated: 2026-08-30

## Purpose

This document defines the target engineering architecture for `abntexto-ufc` v3.0.0. It is normative for repository organization and module ownership, but it does not create academic formatting requirements. Academic requirements are governed by the standards and institutional source contracts.

## Design goals

The v3 architecture must be:

- English-first for engineering identifiers and explanations;
- structurally explicit;
- easy to navigate for maintainers;
- stable for local, Overleaf and CTAN distribution;
- free of runtime compatibility layers whose only purpose is to preserve the removed v2 Portuguese project API;
- modular without duplicate ownership;
- testable through machine-readable contracts.

## Top-level responsibilities

### `abntexto-ufc.cls`

Single canonical class entry point. It loads the supported upstream base class and project runtime modules in a documented order.

The v3 product does not ship `ufctex.cls` as a compatibility wrapper.

### `abntexto-ufc/`

Runtime implementation only. User-editable academic content does not live here.

Canonical module responsibilities:

- `core.def` — canonical setup keys, document/profile state, shared metadata primitives and project-wide conditionals;
- `fonts.def` — typography selection, strict-font policy and engine-specific font resolution;
- `layout.def` — page geometry, section/page-break policy and structural layout primitives;
- `modules.def` — optional feature-module selection and initialization;
- `frontmatter.def` — pre-textual/front-matter rendering capabilities;
- `institutional.def` — UFC institutional assets/presentation policies;
- `academic-works.def` — capstone/dissertation/thesis-specific behavior;
- `research-projects.def` — research-project profiles;
- `articles.def` — scientific-article profile, introduced only in V3-A1;
- `objects.def` — figures, charts, text tables, code listings, algorithms and object captions/notes;
- `bibliography.def` — citation/reference integration and canonical bibliography public surface;
- `backmatter.def` — appendices, annexes, glossary, index and post-textual/back-matter behavior.

### `abntexto-ufc/integrations/`

Adapters for external packages/classes where the project must account for an upstream implementation detail. These are not deprecated compatibility layers.

Example:

- `abntexto.def` — targeted adaptation to supported `abntexto` behavior.

An integration module must state:

1. which upstream package/class it integrates with;
2. which upstream behavior requires adaptation;
3. the minimum supported upstream version;
4. how the adaptation is tested;
5. when the adaptation can be removed.

### `abntexto-ufc/standards/`

Narrow runtime adaptations required to satisfy a current technical-standard behavior not yet fully supplied by an upstream dependency.

Example:

- `nbr6023-2025.def` — targeted bibliography adaptation for the current NBR 6023:2025 contract.

These modules must not be called `compat-*`. Their purpose is current conformance, not backward compatibility.

### `template/`

Editable reference academic project. Its engineering paths are English; its rendered academic content may be Portuguese.

```text
template/
├── main.tex
├── frontmatter/
├── chapters/
├── backmatter/
└── figures/
```

Typical filenames are English even when file contents are Portuguese:

- `frontmatter/acknowledgments.tex`;
- `frontmatter/dedication.tex`;
- `frontmatter/summary.tex`;
- `chapters/1-introduction.tex`;
- `chapters/2-theoretical-framework.tex`;
- `backmatter/references.bib`;
- `backmatter/appendices/appendix-a.tex`.

### `standards/`

Machine-readable source catalog, precedence, atomic rules, coverage rules, locators and normative evidence metadata.

This directory is data/contract infrastructure, not LaTeX runtime. Runtime standard-specific adaptations belong under `abntexto-ufc/standards/`.

### `tests/`

Tests are organized by responsibility:

- `checks/` — Python/static/oracle contract checkers;
- `documents/` — LaTeX documents used to exercise normative/runtime behavior;
- `fixtures/` — small supporting source/data fixtures;
- `integration/` — executable shell/Python runners that build or inspect real artifacts;
- `smoke/` — minimal compile/sanity cases.

Active tests must not encode a major-version prefix such as `v2-` in their filenames unless the test intentionally validates a historical version.

### `tools/`

Developer/release tooling. Tool names, comments, help text and diagnostics are English.

### `validator/`

User-facing PDF validation application. Engineering implementation is English; human-facing interface language may support Portuguese and/or English independently.

### `docs/`

Active engineering documentation. English is the canonical language for architecture, maintenance, API, build, release and migration documentation.

Historical prose does not need to remain duplicated in active documentation because Git preserves previous versions.

### `release/`

Machine-readable phase, audit, distribution and release ledgers. Active schema/field names are English.

Historical ledgers may preserve historical identifiers when they are evidence, but they must not constrain v3 runtime naming.

## Module loading order

The final exact order is validated during V3-R2/R4, but the architectural dependency direction is:

```text
core
  ↓
fonts / layout
  ↓
modules
  ↓
frontmatter / institutional
  ↓
academic-works / research-projects / articles
  ↓
objects
  ↓
integrations and standards adapters where required
  ↓
bibliography
  ↓
backmatter
```

The class must not load a forwarding-only public API module. Canonical public commands belong to the module that owns their behavior.

## Ownership rule

A project-owned internal control sequence may be defined in exactly one runtime module.

Examples:

- page-break policy belongs to `layout.def`;
- reference rendering belongs to `bibliography.def`;
- article code may select or call these capabilities but may not redefine their internal owners.

The repository audit must detect duplicate project-owned internal definitions across runtime modules.

## Public API rule

The v3 public API is implemented directly by behavior owners.

Examples:

- `\ufcPrintReferences` belongs to `bibliography.def`;
- `\ufcPrintCover` belongs to the academic/institutional module that owns cover rendering;
- `\ufcPrintSummary` belongs to `frontmatter.def`;
- `\ufcSource` and `\ufcNote` belong to `objects.def`.

No command exists solely as an alias to a removed Portuguese project command.

## Upstream identifiers

English canonicalization applies only to identifiers owned by this project.

The implementation may legitimately use upstream APIs whose names are outside project control, including `abntexto`, LaTeX, `biblatex`, `babel`, `tabularray-abnt`, `glossaries`, `imakeidx`, and similar dependencies.

An upstream Portuguese identifier is not automatically a violation if it is genuinely owned by an upstream dependency and cannot be replaced without forking that dependency.

## Repository versus bundle layout

Source repository:

```text
template/main.tex
```

Template/Overleaf bundle:

```text
main.tex
frontmatter/
chapters/
backmatter/
figures/
```

The distribution pipeline is responsible for staging/flattening the editable template. This keeps repository architecture maintainable while preserving a simple end-user project.

## Historical compatibility policy

v3 is a breaking major release. Runtime compatibility with removed project-owned Portuguese v2 API is not provided.

Migration support is documentation only, through a future `docs/MIGRATION-V2-TO-V3.md` mapping old identifiers to canonical v3 identifiers.

Git tags/releases preserve old implementations for users who must remain on v2.

## Architecture gate

V3-R4 must enforce at least:

- canonical class entry point exists;
- deprecated v2 class wrapper absent;
- forwarding-only public API module absent;
- runtime module ownership unique;
- required runtime modules loaded exactly once;
- upstream integration modules explicitly scoped;
- project-owned paths satisfy engineering-language policy;
- template source tree and distribution output tree are both valid;
- no generated build artifact is tracked.
