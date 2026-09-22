# Standards data architecture

`standards/` contains the machine-readable normative, institutional and validation-control data for the current project.

It is the structured source used by repository validators and evidence checks. It does not replace the underlying authoritative standards/institutional sources.

## Main data groups

### Current public API

- `api/public-api.json` — machine-readable contract for the currently supported project-owned setup keys, values, commands and environments. The historical migration mapping in `release/history/v3/v3-api-migration.json` is retained only for negative/residual validation and is not current API authority.

### Source authority and precedence

Current source authority data is grouped under `standards/catalog/`:

- `catalog/catalog.json` — active runtime source catalog.
- `catalog/precedence.json` — conflict/precedence rules.
- `catalog/source-audit.json` — controlled source-status audit.
- `catalog/source-status-policy.json` — status interpretation rules.
- `catalog/version-policy.json` — current-edition policy.
- `catalog/reference-guide-map.json` — reviewed mapping to the human-readable reference guide.

Loaders resolve these authorities recursively by unique filename identity. The nested taxonomy is organizational only; it does not create a second source of truth.

### Rules and coverage

Current rule authorities are grouped under `standards/rules/`:

- `rules/atomic-rules.json` — base atomic rule contract.
- `rules/coverage-rules*.json` — current rule extensions by subject/profile.

`atomicity-plan.json` remains a decomposition/migration control artifact until the dedicated migrations slice moves it. Evidence registries and proof/validation policies remain separate authorities and are intentionally not part of `standards/rules/`.

### Evidence and validation semantics

Current evidence/proof authorities are grouped under `standards/evidence/`:

- `evidence/article-evidence-map.json` — scientific-article evidence ownership map.
- `evidence/evidence-contribution-policy.json` — conservative proof-contribution semantics.
- `evidence/evidence-registry.json` — typed non-runner evidence registry.
- `evidence/false-coverage-policy.json` — false-coverage prevention policy.
- `evidence/proof-policy.json` — proof/evidence state policy.
- `evidence/test-surface-policy.json` — standalone/dynamic/manual test-surface ownership.
- `evidence/validation-overrides.json` — rule-local validation ownership overrides.
- `evidence/validation-reference-policy.json` — shared final-PDF measurement policy and tolerances.
- `evidence/vector-rule-validation-extension.json` — calibrated vector-rule measurement extension used by final-PDF evidence checks.

### Locators

Current locator-audit authorities are grouped under `standards/audits/locator/`.

- `audits/locator/locator-audit.json` — consolidated locator audit.
- `audits/locator/locator-audit-*.json` — domain-specific locator audits for article, back matter, citations, deposit, layout/pagination, objects/equations, references, sections/footnotes/nature and typography/paragraphs.

These files map current rule authority to reviewed source locators and explicit evidence status. They remain unique machine-readable authorities; no flat compatibility copies are retained.

### Controlled scenarios

Files ending in `-scenario.json` define deterministic validation scenarios for specific observable requirements such as margins, citations, front matter, bibliography behavior, tables and other document properties.

### Validation policy

Validation semantics and final-PDF measurement policy are grouped under `standards/evidence/`. This taxonomy is organizational only: these controls must not silently strengthen a manual/recommended rule into an automatic normative proof.

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
