# abntexto-ufc — Naming and public API policy

Updated: 2026-08-28

Status: **active engineering policy for N15-B2R and later v2.x work**.

This document defines how engineering-facing names are normalized without translating UFC/ABNT institutional content or breaking supported v2.x documents.

## 1. Core principle

The engineering language of the project is English for project-owned engineering surfaces: internal identifiers, source comments, tests/checkers/tools, canonical public API and new machine-readable engineering fields.

Do not translate merely for engineering consistency: official UFC/ABNT wording, bibliographic titles, quoted normative text, institutional labels, Portuguese academic example content or historical evidence identifiers whose stability matters.

## 2. Compatibility principle

Public API migration in v2.x is additive.

- supported Portuguese setup keys remain accepted;
- supported Portuguese values remain accepted where already public;
- supported Portuguese project-owned commands/environments remain aliases or wrappers when a canonical English equivalent is introduced;
- upstream commands are not renamed for local style consistency;
- supported public-surface removal requires an explicit deprecation/removal policy and normally a major-version boundary.

Canonical English API may become the documented default without invalidating Portuguese compatibility input.

## 3. Engineering file/directory convention

Use lowercase English names and hyphens when appropriate. Canonical examples already adopted include:

- `fonts.def`, `modules.def`, `frontmatter.def`, `institutional.def`;
- `academic-works.def`, `research-projects.def`, `objects.def`, `bibliography.def`, `backmatter.def`;
- future `articles.def`;
- `main.tex`, `frontmatter/`, `chapters/`, `backmatter/`, `figures/`, `assets/institutional/`.

Portuguese academic leaf filenames may remain where translation would create unrelated churn. Historical evidence is not renamed merely for style consistency.

## 4. Public setup keys

Canonical `\ufcsetup` keys use lowercase English kebab-case.

Reviewed direction:

- `type`;
- `print-mode`;
- `cover`;
- `catalog-card`;
- `coat-of-arms`;
- `font`;
- `strict-font`;
- `tables`;
- `code`;
- `algorithms`;
- `glossary`;
- `index`;
- `author`;
- `title`;
- `subtitle`;
- `approval-date`;
- `advisor`;
- `coadvisor`.

B2R-B1 inventories the existing API but introduces no English runtime aliases. B2R-B2 is the setup-key/value alias phase.

## 5. Setup values

Canonical booleans are `true` / `false`. Existing `sim` / `nao` remain compatibility forms where already supported.

Reviewed canonical profile values:

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`;
- future reserved `article`.

Setup-value identity in the machine contract is `(setup key, value)`, not a global value string.

`print-mode` values and optional-module values remain review-required. Do not choose them by literal translation alone.

## 6. UFC-owned commands and environments

New canonical project-owned public commands use the `\ufc...` prefix and English semantics.

Reviewed command direction includes:

- `\ufcPrintCover`;
- `\ufcPrintTitlePage`;
- `\ufcPrintApprovalPage`;
- `\ufcPrintCatalogCard`;
- `\ufcPrintReferences`;
- `\ufcAddBibliographyResource`.

A canonical abstract command remains a semantic design decision because the current vernacular and foreign-language summary surfaces must not be conflated accidentally.

Before adding an alias, classify the existing surface as canonical project API, Portuguese compatibility API, upstream compatibility API, exported helper or internal implementation. Environment aliases must preserve semantics and nesting behavior.

B2R-B1 inventories 47 exported commands, 6 UFC environments and 2 explicit extension hooks; it does not automatically promote every exported helper into long-term public API.

## 7. Other engineering identifiers

Python uses English `snake_case`; constants use `UPPER_SNAKE_CASE` where appropriate. New source comments and developer diagnostics are English. New JSON engineering fields use English `snake_case` unless schema/history requires stability.

Historical schema fields are not renamed casually; migration requires compatibility or schema-version handling.

## 8. Names intentionally preserved

Preserve official UFC units, resolutions, guides and acts; official ABNT titles; bibliographic titles; quoted normative text; Portuguese academic examples; stable normative evidence IDs; release/audit IDs already consumed by ledgers; external/upstream commands; and `normativa/` during B2R.

The deprecated legacy class entrypoint remains a compatibility wrapper. Its exact identity is recorded only in the structured machine inventory. The canonical-identity scanner intentionally rejects narrative or arbitrary new legacy identities elsewhere.

## 9. Public API contract

`release/n15-b2r-b-public-api.json` is the active B2R-B machine contract. `release/n15-b2r-a-naming-inventory.json` remains historical N12-sensitive B2R-A evidence.

The active contract inventories:

- class entrypoints;
- setup keys and enumerated values;
- exported commands;
- UFC environments;
- extension hooks;
- canonical mappings already reviewed;
- compatibility/upstream classifications;
- reserved future surfaces.

`tests/checks/public_api_contract.py` prevents accidental removal and unreviewed additions and verifies the frozen N12 workflow boundary. It is transitively enforced through `tests/run.py` without changing `.github/workflows/latex-preflight.yml`.

## 10. Behavioral equivalence

Naming work must not change document semantics or formatting merely because identifiers change.

Completed B2R-B must cover existing profile builds, PDF/A gates, reference document, structure, objects/bibliography, post-textuals, Overleaf, deterministic distribution, Windows literal-font certification and absence of unintended normative-contract changes.

B2R-B4 will add paired canonical-English/Portuguese semantic and rendered-output equivalence fixtures. B2R-B1 itself is a baseline/checker phase and changes no runtime API behavior.

## 11. Article timing

Scientific-article runtime is delayed until B2R-B closes and the resulting `main` is re-certified.

Therefore:

- do not create a temporary Portuguese article module;
- eventual runtime module is canonical `articles.def`;
- canonical surface is reserved as `type=article`;
- Portuguese compatibility is reserved as `tipo=artigo`;
- reservation is not runtime support;
- article-specific behavior should use centralized profile capabilities or an equivalent policy rather than scattered language-dependent conditionals.

## 12. Current migration state

### B2R-A1 — DONE

Internal module paths normalized by PR #146 and re-certified.

### B2R-A2 — DONE

User/example/distribution-facing engineering layout normalized by PR #148 plus its state-sync closure. Certified B2R-B1 base: `3a7d5e55d0bbd8df279e3e3f6eecb72b98af709b`.

### B2R-B1 — MERGED; POST-MERGE DISTRIBUTION PENDING

PR #150 was squash-merged from exact head `6d51593e1a167ae657c8dd019f913dc947c34250` to `main` `4d9483ea6acd1dbb86622999a1f289fd6f67bce4`.

Final PR-head certification:

- Source #422 — SUCCESS;
- preflight #1090 — SUCCESS.

Post-merge certification already green:

- Source #423 — SUCCESS;
- preflight push #1091 — SUCCESS;
- Gate T #1092 — SUCCESS, including Overleaf and Windows literal-font build/certification.

Distribution #244 is the only remaining post-merge receipt at this checkpoint; its Gate T prerequisite is already SUCCESS.

### B2R-B2 — BLOCKED UNTIL STATE-SYNC RE-CERTIFICATION

B2R-B2 introduces additive canonical-English setup keys/values, forwarding to certified Portuguese behavior wherever possible. Detailed metadata, print-mode values, optional-module values and remaining commands/environments remain review-required until explicitly resolved.

## 13. Mandatory documentation synchronization

After a material naming decision, CI-discovered blocker/fix, PR merge/certification or next-action change, synchronize as applicable:

- `docs/HANDOFF-V2.2.0.md`;
- `docs/B2R-NAMING-INVENTORY.md`;
- `release/n15-b2r-b-public-api.json` while B2R-B is active;
- this policy when naming decisions/state change;
- user/normative docs if described public surfaces change.

B2R-A's historical machine ledger is not rewritten merely to reflect B2R-B state.

## 14. Review checklist

Before adding an engineering-facing identifier, verify ownership, semantic precision, naming convention, duplication, compatibility needs, schema/API impact, preservation of official wording and documentation-sync requirements.

If any point is unclear, treat the identifier as an API/design decision rather than a cosmetic rename.
