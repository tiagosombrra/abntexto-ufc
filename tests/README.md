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
