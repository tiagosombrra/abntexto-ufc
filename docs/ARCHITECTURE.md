# abntexto-ufc v3 Architecture

Updated: 2026-08-30

This document defines the target engineering architecture for `abntexto-ufc` v3.0.0. It governs repository organization and project-owned module/API ownership; it does not create academic formatting requirements.

## Design principles

The v3 tree must be explicit, English-first for engineering surfaces, easy to navigate, free of duplicate ownership, testable, distribution-safe, and free of runtime compatibility layers whose only purpose is preserving removed v2 project API.

The repository is an active product tree, not an archive. Historical evidence belongs to Git commits, tags, releases, issues, pull requests, and certified SHAs. No `history/` museum directories or dormant future-phase ledgers are part of the active architecture.

## Top-level layout

```text
abntexto-ufc.cls
abntexto-ufc/
  core.def
  fonts.def
  layout.def
  modules.def
  frontmatter.def
  institutional.def
  academic-works.def
  research-projects.def
  objects.def
  bibliography.def
  backmatter.def
  integrations/abntexto.def
  standards/nbr6023-2025.def
template/
  main.tex
  frontmatter/
  chapters/
  backmatter/
  figures/
assets/institutional/
standards/
tests/
  checks/
  documents/
  fixtures/
  integration/
  smoke/
tools/
validator/
docs/
release/
```

`articles.def` is introduced only when V3-A1 becomes active. It is not pre-staged as a dormant foundation module.

## Runtime ownership

`abntexto-ufc.cls` is the only canonical class entry point. v3 does not ship `ufctex.cls`.

Runtime responsibilities are separated as follows:

- `core.def`: setup keys, document/profile state, shared metadata, common conditionals;
- `fonts.def`: font selection, strict-font policy, engine-specific font resolution;
- `layout.def`: page geometry, section/page-break policy, structural layout primitives;
- `modules.def`: optional feature selection and initialization;
- `frontmatter.def`: front-matter rendering capabilities;
- `institutional.def`: UFC institutional presentation/assets;
- `academic-works.def`: capstone/dissertation/thesis behavior;
- `research-projects.def`: research-project behavior;
- `objects.def`: figures, charts, tables, listings, algorithms, captions, source/note handling;
- `bibliography.def`: citation/reference integration and public bibliography surface;
- `backmatter.def`: appendices, annexes, glossary, index, and back-matter behavior.

A project-owned internal control sequence has one behavior owner. Public commands are implemented directly by the module that owns the behavior; no forwarding-only compatibility layer is part of the final v3 runtime. `public-api.def` is therefore transitional R2 debt and must disappear after direct ownership is absorbed.

## Upstream boundaries

`abntexto-ufc/integrations/` contains current adapters to external package/class behavior. These are not legacy compatibility layers. An upstream identifier may remain non-English when it is genuinely owned by the dependency and must be called at an explicit integration boundary, but it must not be re-exported as canonical project API.

`abntexto-ufc/standards/` contains narrow runtime adaptations required for a current technical-standard behavior, such as the current NBR 6023:2025 bibliography adapter.

## Editable template and public bundles

The source repository keeps the editable example under `template/`:

```text
template/main.tex
```

Template and Overleaf bundles flatten `template/` so the user receives:

```text
main.tex
frontmatter/
chapters/
backmatter/
figures/
```

Flattening is a distribution staging responsibility; it must not distort the repository architecture. `tools/build-public-bundles.py`, exposed through `make public-bundles`, currently produces a version-rooted template archive and a root-flat Overleaf import archive. The latter alone vendors the pinned upstream `abntexto.cls`. Public staging excludes the UFC institutional asset and proprietary Microsoft fonts, and `tests/checks/public_bundles.py` proves archive structure, safe paths and reproducibility. Class/CTAN-candidate packaging is a separate B5-C responsibility.

## Standards data

Top-level `standards/` contains the current machine-readable source catalog, precedence, rules, locators, and normative evidence metadata needed by the active product. Process ledgers from completed campaigns are not retained merely as historical records.

Scientific-article normative/runtime material is reintroduced only in V3-A1 after current sources are reconfirmed.

## Tests and tooling

- `tests/checks/`: static and machine-readable contract checks;
- `tests/documents/`: LaTeX validation documents;
- `tests/fixtures/`: supporting test data;
- `tests/integration/`: executable build/inspection runners;
- `tests/smoke/`: minimal compilation cases;
- `tools/`: developer/release tooling.

Active path names must not encode retired major-version or N-phase identities.

## Validator

`validator/` is project-owned engineering software. Its implementation, controls, technical labels, and diagnostics are English. Portuguese text extracted from or evaluated inside a Brazilian academic PDF is document data, not validator engineering nomenclature.

## Documentation and release state

`docs/` contains current engineering documentation only. `release/` contains current machine-readable migration/release state only. A migration contract remains tracked only while an active migration consumes it; after use it is removed or consolidated.

## Breaking v3 API policy

v3 provides one canonical project API. Removed Portuguese v2 project API is not retained through runtime aliases. Migration support is documentation-only and is written when the migration surface is final; it is not pre-staged as dormant files during R1/R2.

## Architecture gates

The final foundation must prove at least:

- one canonical class entry point;
- deprecated v2 class wrapper absent;
- forwarding-only public API module absent;
- unique runtime ownership;
- required runtime modules loaded exactly once;
- explicitly scoped upstream integrations;
- English project-owned engineering paths;
- valid repository template layout and valid flattened public bundle layout;
- no generated artifacts, archive directories, or unused migration scaffolding tracked.
