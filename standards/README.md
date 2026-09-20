# Standards data architecture

`standards/` contains the machine-readable normative, institutional and validation-control data for the current project.

It is the structured source used by repository validators and evidence checks. It does not replace the underlying authoritative standards/institutional sources.

## Main data groups

### Current public API

- `public-api.json` — machine-readable contract for the currently supported project-owned setup keys, values, commands and environments. The historical migration mapping in `release/history/v3/v3-api-migration.json` is retained only for negative/residual validation and is not current API authority.

### Source authority and precedence

- `catalog.json` — active runtime source catalog.
- `precedence.json` — conflict/precedence rules.
- `source-audit.json` — controlled source-status audit.
- `source-status-policy.json` — status interpretation rules.
- `version-policy.json` — current-edition policy.

### Rules and coverage

- `atomic-rules.json` — base atomic rule contract.
- `atomicity-plan.json` — decomposition/atomicity control.
- `coverage-rules*.json` — current rule extensions by subject/profile.
- `evidence-registry.json` — registered evidence producers/ownership.
- `evidence-contribution-policy.json` — contribution/proof semantics.
- `proof-policy.json` and `false-coverage-policy.json` — proof-state guardrails.

### Locators

`locator-audit*.json` maps current rule authority to reviewed source locators and explicit evidence status.

### Controlled scenarios

Files ending in `-scenario.json` define deterministic validation scenarios for specific observable requirements such as margins, citations, front matter, bibliography behavior, tables and other document properties.

### Validation policy

- `validation-reference-policy.json`;
- `validation-overrides.json`;
- `test-surface-policy.json`;
- related validation-extension data.

These files control how evidence is interpreted; they must not silently strengthen a manual/recommended rule into an automatic normative proof.

## Maintenance rules

When authoritative material changes:

1. update source/status/currency data first;
2. reconcile precedence;
3. update affected atomic/current rules and locators;
4. update implementation behavior if required;
5. update evidence classification and controlled scenarios;
6. run the source/static contract;
7. run integration/release validation when observable output can change.

Do not update a rule merely to make a test pass. The source authority and intended normative semantics must be established first.

## Current human-readable context

See:

- `docs/NORMATIVE-BASE.md`;
- `docs/NORMATIVE-CURRENCY.md`;
- `docs/ARTICLE-NORMATIVE-CONTRACT.md`;
- `docs/UFC-LIBRARIAN-REVIEW.md`.

Historical implementation evidence is not stored in this directory as an alternate standards tree.
