# abntexto-ufc architecture

Updated: 2026-09-19

This document describes the current engineering architecture of `abntexto-ufc`. It is intentionally limited to the supported repository/runtime model and does not serve as a chronology of earlier implementation phases.

The latest published release is v3.0.3. The active unreleased development line is v3.0.4.

## Design principles

The repository follows these constraints:

- one canonical project-owned runtime source;
- one canonical public project API;
- explicit separation between project runtime, upstream dependencies, normative data, tests, tooling and documentation;
- deterministic, auditable distribution production;
- no generated release/build products tracked in Git;
- no proprietary Microsoft font files redistributed;
- institutional assets handled according to their explicit distribution policy;
- fail-closed validation for repository, normative, distribution and release contracts;
- published tags/releases/assets are immutable project evidence.

## Top-level layout

```text
abntexto-ufc.cls
template/
  main.tex
  frontmatter/
  chapters/
  backmatter/
  figures/
assets/
  institutional/
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
  README.md
  USER-GUIDE.md
  COMMAND-REFERENCE.md
  ARCHITECTURE.md
  RELEASE-STATE.md
release/
  ctan/
  history/
.github/
  workflows/
```

Local release/audit material belongs under ignored `.release/` and is never part of the tracked repository.

## Canonical runtime

`abntexto-ufc.cls` is the only canonical project-owned runtime source.

The class is internally divided into clearly delimited responsibility sections covering:

- core configuration and metadata;
- fonts and typography;
- page/text layout;
- optional modules;
- pre-textual elements;
- institutional presentation;
- academic-work profiles;
- scientific articles;
- research projects;
- figures, tables, listings, algorithms and other academic objects;
- upstream `abntexto` compatibility;
- citations and references;
- current-standard adaptations such as NBR 6023:2025 behavior;
- post-textual elements.

These are source-organization sections inside one class, not separately distributed runtime modules.

The same tracked class is consumed by repository tests and is distributed through Template, Overleaf and CTAN surfaces. Distribution builders must not transform project source into a different project runtime.

Required invariant:

```text
tracked canonical class
    == tested project runtime
    == Template project runtime
    == Overleaf project runtime
    == CTAN project runtime
```

For CTAN, equality is enforced byte-for-byte for the project-owned `abntexto-ufc.cls`.

## Public API ownership

The public project API is implemented by the canonical class, represented machine-readably by `standards/public-api.json`, and documented for users in `docs/COMMAND-REFERENCE.md`.

Historical migration mappings under `release/history/v3/` are retained only for negative/residual validation and auditability; they are not authority for the current public API.

Project-owned configuration keys, commands and environments have a single implementation owner. Public behavior is implemented directly in the canonical class; forwarding-only compatibility layers are not part of the supported runtime.

Dependency-owned identifiers remain at the upstream boundary when they are required to interact correctly with the dependency.

## Upstream boundary

`abntexto-ufc` depends on the external `abntexto` class.

The repository does not fork or silently redefine the complete upstream project. Project-specific compatibility/adaptation behavior is isolated inside the canonical class and covered by integration tests.

Distribution rules differ by surface:

- CTAN keeps `abntexto` external;
- Overleaf vendors the pinned supported `abntexto.cls` required for a self-contained import;
- Template assumes the supported external dependency is available in the local TeX installation.

## Template and public bundles

`template/` is the canonical editable TCC tutorial source.

It is deliberately a realistic, compact user project rather than an exhaustive technical manual. Complete API documentation belongs in `docs/COMMAND-REFERENCE.md`; normative explanations belong in the relevant current documentation and standards data.

The distribution pipeline produces:

- the CTAN archive;
- the editable Template archive;
- the self-contained Overleaf archive;
- `SHA256SUMS`.

Template and Overleaf must contain exactly the project institutional PNG required by the canonical tutorial and preserve `coat-of-arms=true`. They embed a reference PDF rebuilt from the exact bundled source.

The CTAN archive intentionally excludes institutional mark assets and uses `coat-of-arms=false` in its minimal example.

No distribution surface may contain proprietary Microsoft font files.

## Standards and normative data

`standards/` is the machine-readable normative authority for:

- source catalog and precedence;
- atomic/current rules;
- rule coverage and applicability;
- source locators;
- normative proof/evidence classification;
- controlled validation scenarios.

Human-readable normative context lives in:

- `docs/NORMATIVE-BASE.md`;
- `docs/NORMATIVE-CURRENCY.md`;
- `docs/ARTICLE-NORMATIVE-CONTRACT.md`;
- `docs/UFC-LIBRARIAN-REVIEW.md`.

Runtime code implements the behavior required by that reconciled contract but is not itself the normative-source catalog.

## Test architecture

The permanent test surface is divided into:

- `tests/checks/` — source/repository/normative contracts;
- `tests/documents/` — controlled LaTeX documents;
- `tests/fixtures/` — input data and controlled assets;
- `tests/integration/` — compile/render/distribution gates;
- `tests/smoke/` — bounded smoke coverage;
- `tests/run.py` — coordinated integration/release runner;
- `tests/static.py` — static/source contract entry point.

Tests are part of the architecture. A source-layout refactor is incomplete until all checks that inspect source ownership are reconciled to the new canonical source model.

## Validation and CI

The repository keeps three distinct engineering workflows:

- **Static Contract** — source-only, fast, deterministic checks;
- **Linux Integration** — compile/render/integration validation, with scoped selection when appropriate;
- **Linux Release Check** — complete release-grade validation, distribution generation and CTAN package checks.

GitHub Pages is deployed by a separate Pages workflow.

The protected `main` branch requires the permanent PR statuses configured by the repository ruleset. Release-grade evidence remains a separate certification control and may be forced by release-marker changes when a structural runtime change requires complete validation.

A complete release-grade run covers, among other evidence:

- repository and API contracts;
- canonical tutorial;
- supported engines/profiles;
- bibliography/current-reference behavior;
- PDF/A;
- Unicode;
- font embedding/policy;
- public bundle reconstruction;
- archive integrity and reproducibility;
- CTAN `pkgcheck`;
- reference/review PDFs.

## Validator

`validator/` is a local-processing Web/Lite validation surface.

Its source, normative catalog and browser behavior are tested separately from the CLI/deep local validation path. The browser validator does not upload user PDFs to a server.

The validator consumes generated normative data from the same controlled standards source rather than maintaining a second independent normative truth.

## Documentation architecture

Current documentation lives directly under `docs/` and is indexed by `docs/README.md`.

Controlled historical engineering evidence lives under:

- `docs/history/v3/`;
- `release/history/v3/`.

Historical documents are audit evidence only. They do not define the current runtime, current user workflow or current release state.

Current release/lifecycle authority is:

1. current Git/GitHub facts;
2. `release/v3-release-candidate.json`;
3. `docs/RELEASE-STATE.md`;
4. current durable technical documentation.

## Release-state architecture

`release/v3-release-candidate.json` is the stable machine-readable release/development state path.

During the active v3.0.4 line it must remain explicitly unreleased until a separately certified freeze:

```text
candidate_state = NOT_FROZEN
candidate_sha = null
publication_state = UNPUBLISHED
publication_authorized = false
```

The marker also preserves the receipt of the latest published release without allowing that release to be retargeted or rebuilt.

Release invariant:

```text
certified source SHA
    == visually approved source SHA
    == tagged source SHA
    == source SHA of published release bytes
```

## Architecture gates

The repository architecture is considered coherent when all of the following hold:

- exactly one tracked project-owned runtime class exists;
- no legacy project runtime-module directory is tracked;
- public API and command documentation agree;
- all active documentation links resolve;
- no generated PDF/ZIP/build residue is tracked;
- public bundles use the same canonical project runtime;
- CTAN class identity is byte-equal to the tracked canonical class;
- institutional/proprietary asset policies pass;
- retained tests/checks are reachable and purposeful;
- current documentation contains current state rather than closed implementation chronology;
- Static Contract and applicable integration/release gates pass.
