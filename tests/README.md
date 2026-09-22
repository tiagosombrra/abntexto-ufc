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

Checks not yet assigned to a semantic namespace remain at `checks/` until their family receives the same location-independence and stale-path preparation; no compatibility copies are retained.

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
