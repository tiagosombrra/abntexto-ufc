# Documentation index

This directory contains the current human-readable documentation for `abntexto-ufc`.

The documentation describes the current supported project only. Historical implementation phases, closed release work and retired API evidence are not user guidance and live under `docs/history/v3/` or `release/history/v3/` when they still have audit value.

## User documentation

- [USER-GUIDE.md](USER-GUIDE.md) — recommended document-authoring workflow, profiles, academic elements, compilation and validation.
- [COMMAND-REFERENCE.md](COMMAND-REFERENCE.md) — canonical public configuration keys, commands and environments.
- [WINDOWS-FONT-SUPPORT.md](WINDOWS-FONT-SUPPORT.md) — scoped support for literal Windows font validation.

## Architecture and engineering

- [ARCHITECTURE.md](ARCHITECTURE.md) — current repository/runtime architecture and ownership boundaries.
- [ENGINEERING-LANGUAGE.md](ENGINEERING-LANGUAGE.md) — language policy for project-owned engineering surfaces.
- [LINUX-INTEGRATION-SCOPES.md](LINUX-INTEGRATION-SCOPES.md) — integration scopes and CI selection rules.

## Normative and institutional basis

- [NORMATIVE-BASE.md](NORMATIVE-BASE.md) — active normative/institutional basis and precedence.
- [NORMATIVE-CURRENCY.md](NORMATIVE-CURRENCY.md) — policy for current technical editions and supersessions.
- [ARTICLE-NORMATIVE-CONTRACT.md](ARTICLE-NORMATIVE-CONTRACT.md) — scientific-article normative contract.
- [UFC-LIBRARIAN-REVIEW.md](UFC-LIBRARIAN-REVIEW.md) — consolidated librarian-review contract and evidence status.

## Release and distribution

- [RELEASE-STATE.md](RELEASE-STATE.md) — current published baseline and active development state.
- [CTAN-RELEASE.md](CTAN-RELEASE.md) — reusable GitHub/CTAN release discipline and distribution contract.

## Repository-wide contributor material

The following files live at repository root because they apply to the whole project:

- [../CONTRIBUTING.md](../CONTRIBUTING.md) — contribution workflow and required validation;
- [../SECURITY.md](../SECURITY.md) — security and supply-chain reporting scope;
- [../CITATION.cff](../CITATION.cff) — software citation metadata;
- [../AGENTS.md](../AGENTS.md) — fail-closed maintainer/automation control rules.

## Historical evidence

`docs/history/v3/` and `release/history/v3/` are audit namespaces. Their contents may intentionally mention old phases, branches, API names, issues or release states. They do not define the current user experience or current project architecture.

For current facts, prefer this order:

1. current Git/GitHub state;
2. `release/v3-release-candidate.json`;
3. [RELEASE-STATE.md](RELEASE-STATE.md);
4. current documentation listed above;
5. controlled historical evidence.
