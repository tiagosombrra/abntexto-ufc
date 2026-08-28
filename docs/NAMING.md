# abntexto-ufc — Naming and public API policy

Updated: 2026-08-28

Status: **normative engineering policy for N15-B2R and later v2.x work**.

This document defines how engineering-facing names are normalized without translating UFC/ABNT institutional content or breaking supported v2.x documents.

## 1. Core principle

The engineering language of the project is English.

This applies to new or normalized:

- internal implementation filenames;
- internal identifiers;
- source-code comments;
- test/checker names;
- tooling names;
- canonical public API names owned by `abntexto-ufc`;
- machine-readable engineering fields where changing them does not invalidate historical evidence.

It does **not** imply that academic content, official UFC/ABNT names, citations, normative quotations, institutional labels or user-facing Portuguese document text should be translated.

## 2. Compatibility principle

N15-B2R is additive for public API compatibility.

During v2.x:

- supported Portuguese setup keys remain accepted;
- supported Portuguese setup values remain accepted where already exposed;
- supported Portuguese UFC-owned commands/environments remain available as aliases or compatibility wrappers;
- upstream `abntexto`/`abntex2` compatibility commands are not renamed merely for local style consistency;
- removal of a supported public surface requires a separate deprecation/removal policy and, normally, a major-version boundary.

Canonical English API may become the documented default without making Portuguese compatibility input invalid.

## 3. Naming conventions

### 3.1 Files and directories

Use lowercase English names with hyphens when multiple words are needed.

Preferred examples:

- `fonts.def`
- `modules.def`
- `frontmatter.def`
- `backmatter.def`
- `academic-works.def`
- `research-projects.def`
- `articles.def`
- `objects.def`
- `bibliography.def`
- `frontmatter/`
- `chapters/`
- `backmatter/`
- `figures/`
- `assets/institutional/`

Do not rename historical evidence files merely to satisfy style consistency when the rename would damage traceability or produce disproportionate churn.

### 3.2 LaTeX public setup keys

Canonical `\ufcsetup` keys use lowercase English kebab-case.

Examples:

- `type`
- `print-mode`
- `cover`
- `catalog-card`
- `coat-of-arms`
- `font`
- `strict-font`
- `tables`
- `code`
- `algorithms`
- `glossary`
- `index`
- `author`
- `title`
- `subtitle`
- `approval-date`
- `advisor`
- `coadvisor`

Portuguese compatibility aliases such as `tipo`, `impressao`, `capa`, `ficha-catalografica`, `brasao`, `fonte`, `codigo`, `autor`, `titulo`, `orientador` and `coorientador` remain supported when they are already part of the v2.x public surface.

### 3.3 Setup values

Canonical booleans use:

- `true`
- `false`

Existing `sim` / `nao` inputs remain compatibility values where already supported.

Canonical profile values should be explicit and internationally unambiguous. Prefer terms such as:

- `undergraduate-capstone`
- `specialization-capstone`
- `masters-thesis`
- `doctoral-thesis`
- `research-project`
- `anonymized-research-project`
- `article`

Do not use an English term whose international academic meaning is materially ambiguous when a more explicit value is available.

### 3.4 UFC-owned LaTeX commands

New canonical UFC-owned public commands should use a consistent `\ufc...` prefix and English semantic names.

Preferred style:

- `\ufcPrintCover`
- `\ufcPrintTitlePage`
- `\ufcPrintApprovalPage`
- `\ufcPrintCatalogCard`
- `\ufcPrintAbstract`
- `\ufcPrintReferences`
- `\ufcAddBibliographyResource`

Existing Portuguese commands remain supported when they are part of the current public API or upstream compatibility surface.

The migration must explicitly classify each command as one of:

1. canonical `abntexto-ufc` API;
2. Portuguese compatibility alias;
3. upstream compatibility API;
4. private/internal command.

No command should be renamed based only on spelling without this classification.

### 3.5 Environments

New UFC-owned environments use English semantic names. Existing Portuguese environments may remain compatibility aliases.

Environment renaming must preserve semantics and nesting behavior, not only names.

### 3.6 Python and JavaScript

Use conventional English identifiers:

- modules/files: `snake_case.py` where Python convention applies;
- functions/variables: `snake_case` in Python;
- JavaScript identifiers: existing project convention, with English semantic names;
- constants: `UPPER_SNAKE_CASE` where appropriate.

### 3.7 JSON engineering fields

New engineering fields use English `snake_case` unless an established schema in that file already uses another convention.

Do not rename historical schema fields casually. Schema migrations require explicit backward/read compatibility or a version bump.

### 3.8 Comments and developer-facing messages

New source-code comments and developer-facing diagnostics are written in English.

User-facing academic/document text may remain Portuguese and should follow its own language/context requirements.

## 4. Names that are intentionally preserved

The following categories are not translated merely for naming consistency:

- official names of UFC units, resolutions, guides and acts;
- official titles of ABNT standards;
- bibliographic titles;
- quoted normative text;
- Portuguese content in academic examples;
- historical normative IDs whose stability is part of traceability;
- release/audit identifiers already consumed by evidence ledgers;
- external/upstream command names.

Examples of stable evidence identifiers include `abnt-nbr-*` and existing `ufc-guia-*` source IDs. Their language is subordinate to traceability and source identity.

## 5. Repository normalization boundaries

N15-B2R-A may normalize internal/package/example filenames only when all references are updated atomically and regression evidence remains green.

The source repository layout and distributed Overleaf/template layout do not have to be identical.

In particular:

- moving the reference/user example under `examples/` is allowed only after distribution/import behavior is verified;
- a distributed bundle may still place `main.tex` at its root for user convenience;
- CTAN and Overleaf package allowlists must be updated together with source moves;
- `normativa/` is not renamed in B2R-A unless a separate evidence-preserving migration demonstrates clear value greater than its traceability/churn cost.

Current default decision: **preserve `normativa/` during B2R**.

## 6. Public API contract

N15-B2R-B must create a machine-readable public API inventory/contract before or together with canonical public API aliases.

The contract must inventory at least:

- setup keys;
- setup values/profile values;
- public commands;
- public environments;
- class entrypoints;
- canonical names;
- compatibility aliases;
- upstream compatibility surfaces;
- deprecation state, if any.

A dedicated checker must prevent accidental removal of supported aliases and introduction of unreviewed public engineering identifiers outside this policy.

## 7. Behavioral equivalence requirement

A naming migration is not allowed to change document semantics or formatting merely because identifiers changed.

For B2R-A and B2R-B, evidence must cover:

- all existing profile builds;
- PDF/A checks already required by the certified matrix;
- reference-document build;
- Overleaf/distribution behavior when affected;
- canonical-English versus Portuguese-compatibility API equivalence for representative documents;
- absence of unintended changes in normative predicates.

Where byte-identical PDF output is not structurally guaranteed because of build metadata, the existing project oracle/equivalence policy governs the comparison. Naming work must not weaken that policy.

## 8. Article-profile timing

The article runtime is intentionally delayed until B2R closes.

Therefore:

- do not create a temporary `artigos.def` file;
- create the eventual module directly under the canonical English name, expected to be `articles.def`;
- expose canonical `type=article` from the start;
- expose `tipo=artigo` only as the Portuguese compatibility surface defined by the B2R public API contract;
- implement article-specific layout through centralized profile capabilities or equivalent policy rather than scattered language-dependent conditionals.

## 9. Migration phases

### N15-B2R-A — repository/internal normalization

1. produce a read-only naming/API inventory;
2. classify each candidate rename by compatibility risk;
3. rename low-risk internal files first;
4. update imports/tests/tools/package builders atomically;
5. normalize the user example structure where safe;
6. run the full existing regression surface;
7. merge only after exact-head certification.

### N15-B2R-B — canonical public API

1. establish the machine-readable public API contract;
2. introduce canonical English keys/values;
3. add compatibility mappings from Portuguese surfaces;
4. add canonical UFC-owned command/environment aliases where beneficial;
5. add equivalence and negative tests;
6. update examples/docs to prefer canonical English API while documenting Portuguese compatibility;
7. merge only after exact-head certification.

## 10. Review checklist for any new identifier

Before adding a new engineering-facing name, verify:

- Is it owned by this project rather than upstream?
- Is English appropriate for this surface?
- Is the meaning precise in an academic/LaTeX context?
- Does it follow the naming convention for its language/file type?
- Does it duplicate an existing concept under another spelling?
- Does it need a Portuguese compatibility alias?
- Does it affect a public API contract or schema?
- Does it preserve official institutional/normative wording where that wording is the data itself?

If any answer is unclear, treat the name as an API/design decision rather than a cosmetic rename.

## 11. Phase boundary

This policy document may be committed during B2A as roadmap/documentation preparation. Its presence alone does not constitute a B2R implementation change.

Actual renames, API aliases, compatibility mappings and naming-enforcement checkers begin only after B2A is merged and the resulting `main` is re-certified.
