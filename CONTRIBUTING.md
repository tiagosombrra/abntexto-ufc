# Contributing to abntexto-ufc

Contributions should improve the current supported project. Historical implementation phases are not a prerequisite for contributing.

## Before changing the repository

Read:

1. `README.md`;
2. `docs/README.md`;
3. `docs/ARCHITECTURE.md`;
4. `docs/RELEASE-STATE.md`;
5. `AGENTS.md` for fail-closed maintainer/control rules.

If the change affects academic formatting or normative behavior, also read the applicable current normative documentation and machine-readable standards under `standards/`.

## Branch and pull-request workflow

Create a short-lived branch from current `main`.

Keep each pull request bounded to one coherent concern. Do not mix runtime changes, repository cleanup, release control and unrelated documentation changes unless they are technically inseparable.

The repository uses squash merges. Merged topic branches are expected to disappear after merge.

Published version tags, GitHub Release assets and checksums must never be rewritten.

## Source-of-truth rules

- `abntexto-ufc.cls` is the canonical project-owned runtime.
- `template/` is the canonical editable tutorial project.
- `docs/COMMAND-REFERENCE.md` documents the supported public project API.
- `standards/` owns machine-readable normative authority and traceability.
- `tests/` owns regression/evidence behavior.
- `release/v3-release-candidate.json` and `docs/RELEASE-STATE.md` own current release/development state.

Do not introduce a second project runtime or duplicate normative truth.

## Local checks

For source-only changes:

```bash
make static-check
```

For changes that can affect compilation, runtime behavior, generated PDFs, public bundles or validation:

```bash
make check
```

For release-grade changes, candidate/freeze control, distribution architecture or other changes explicitly requiring complete certification:

```bash
make release-check
```

A change is not complete merely because one narrow test passes. Run the scope required by the ownership and risk of the change.

## LaTeX/runtime changes

Runtime changes must preserve the documented public API unless the active development line explicitly authorizes a reviewed API change.

When changing `abntexto-ufc.cls`:

- keep responsibility sections clear;
- preserve engine compatibility covered by tests;
- update command/user documentation when public behavior changes;
- update normative evidence only when the authoritative rule/implementation relationship changes;
- add or update regression coverage for the changed behavior;
- do not add generated PDFs, logs or build residue to Git.

## Normative changes

Do not infer an academic rule from memory or from an older embedded reference.

A normative change must reconcile:

- the current source catalog;
- precedence;
- current-edition policy;
- rule/locator data;
- implementation behavior;
- automated/manual evidence classification.

If current authority cannot be established, stop the change and document the ambiguity instead of guessing.

## Documentation changes

Active documentation describes the current supported project.

Do not add user-facing documentation whose primary purpose is explaining retired versions or closed implementation phases. Historical evidence belongs only in controlled history when it still has audit value.

Keep links repository-relative where possible and make sure they resolve.

## Distribution changes

The current distribution contract is documented in `docs/CTAN-RELEASE.md` and `docs/ARCHITECTURE.md`.

In particular:

- CTAN excludes UFC institutional marks and proprietary Microsoft font files;
- Template and Overleaf include the authorized project institutional PNG used by the canonical example;
- Overleaf vendors the pinned upstream `abntexto.cls`;
- the project-owned `abntexto-ufc.cls` distributed through all surfaces must remain the canonical tracked runtime.

## Pull-request checklist

Before requesting merge, verify:

- [ ] the change has one clear scope;
- [ ] active documentation matches the implemented current behavior;
- [ ] no generated or local-only artifacts are tracked;
- [ ] required static/integration/release checks pass;
- [ ] tests cover changed runtime or validation behavior;
- [ ] published releases/tags/assets remain untouched;
- [ ] normative claims are supported by current controlled sources;
- [ ] the PR description records material invariants and known limitations.

## Reporting problems

For reproducible technical problems, include:

- abntexto-ufc version or commit;
- TeX Live version;
- engine (pdfLaTeX or LuaLaTeX);
- document profile;
- operating system;
- a minimal reproducible example when possible;
- relevant log excerpt;
- expected and observed behavior.

For security or supply-chain concerns, follow `SECURITY.md`.
