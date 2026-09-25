# Test architecture

This directory contains the permanent validation surface for the current `abntexto-ufc` project.

## Entry points

- `tests/static.py` — source-only/static contract.
- `tests/run.py` — coordinated integration/release runner.
- `tests/integration_suites.py` — named integration scopes used by CI and local runs.

The standard repository commands are:

```bash
make static-check
make check
make release-check
```

## Directory roles

### `checks/`

Python source contracts for repository structure, API ownership, normative state, validator behavior, evidence classification and generated/distribution invariants.

These checks are fail-closed: a source-layout or authority change is incomplete until the affected contract is updated deliberately.

Current semantic namespaces:

- `checks/repository/` — repository identity, governance, metadata, path/suite integrity, engineering-language and librarian-review control checks.
- `checks/distribution/` — deterministic public/CTAN/template/Overleaf bundle validation checks used by release-candidate packaging.
- `checks/validator/` — validator source and isolated PDF measurement-core contracts; validator applications and integration/E2E surfaces remain in their existing namespaces.
- `checks/profiles/` — document-profile and scientific-article source/rendering contracts; integration scripts and document fixtures remain in their existing namespaces.
- `checks/api/` — public-API residual/migration contracts that verify retired aliases and migration-state cleanliness without modifying runtime API behavior.
- `checks/governance/` — normative governance/source-authority contracts covering configuration, source currency, locators, negative paths, precedence, proof state, rule migrations, source references and reference-guide consistency.
- `checks/evidence/` — normative evidence, coverage, atomic/full contract, cross-surface, traceability, validator-contract and test-surface integrity checks.
- `checks/frontmatter/` — frontmatter geometry/evidence and normative cover, title-page, approval, acknowledgments, errata, lists, pagination, summary and TOC contracts.
- `checks/citations/` — citation, quotation and reference-layout/semantics contracts for UFC/ABNT textual and bibliographic behavior.
- `checks/layout/` — body paragraph, footnote, page geometry, PDF/A and typography contracts for rendered-layout behavior.
- `checks/sections/` — section hierarchy, indicator, spacing, recto/duplex, multiline-hanging and unnumbered-heading contracts.
- `checks/objects/` — equation, illustration, table, vector-rule and academic-object scope contracts for rendered-object behavior.
- `checks/backmatter/` — appendix/annex and index/glossary contracts for post-textual document behavior.

All current Python checks are assigned to semantic namespaces below `checks/`; the flat `checks/` root contains no check scripts. Recursive basename resolution remains the path authority.

### `documents/`

Controlled LaTeX documents used to exercise public behavior across supported profiles and scenarios.

They are test inputs, not user templates.

### `fixtures/`

Controlled bibliography/data/assets used by integration scenarios.

Fixtures should remain minimal and deterministic. They are not a second source of normative truth.

### `integration/`

Shell-based compilation/render/distribution gates. These cover engine behavior, PDF properties, bibliography, profiles, academic objects, front/back matter, public bundles and other end-to-end contracts.

### `smoke/`

Bounded smoke coverage for fast sanity checks where a full integration route is not required.

## Recursive path ownership

Movable test/check identities are resolved by unique basename through `tests/path_resolver.py`. Permanent runners should use `check_file(...)` and `integration_file(...)` plus `repository_relative(...)` instead of hard-coded movable paths.

Resolution is recursive and fail-closed: a missing basename fails, and duplicate basenames are treated as ambiguous rather than choosing one implicitly. This invariant must be established before checks or integration scripts are moved into semantic subdirectories.

Checks that may move below `tests/checks/` must not derive repository root from a fixed `Path(__file__).resolve().parents[N]` depth. They locate the stable `tests/` ancestor containing `path_resolver.py`, add that directory to `sys.path`, and import canonical `ROOT` from `path_resolver`. The path-resolution contract rejects fixed-depth root derivation in nested checks.

## Evidence model

Tests may produce structured evidence consumed by normative and release validation.

A passing supporting test does not automatically prove a normative rule. Evidence ownership, contribution and proof state are controlled by `standards/` policies and the corresponding checks.

## Runtime-source rule

The current project runtime is the single tracked `abntexto-ufc.cls`.

Tests that inspect implementation source must inspect that canonical class or a documented external boundary. No test should depend on a removed project-owned runtime-module directory.

## Adding tests

When adding or changing a test:

- bind it to a real current behavior/contract;
- avoid duplicate coverage without a distinct purpose;
- keep generators fail-closed when requested semantic variation is not applied;
- ensure retained scripts are reachable from a permanent entry point or explicitly classified;
- avoid network dependencies in ordinary source/static checks;
- clean all generated files after local execution;
- do not commit generated PDFs/logs.

## CI ownership

- Static Contract executes the source-only contract.
- Linux Integration executes the appropriate integration scope.
- Linux Release Check executes complete release-grade validation and distribution checks.

For current workflow/scoping details, see `docs/LINUX-INTEGRATION-SCOPES.md` and `docs/ARCHITECTURE.md`.
