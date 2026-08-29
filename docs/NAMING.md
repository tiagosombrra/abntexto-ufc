# abntexto-ufc — Naming and public API policy

Updated: 2026-08-29

Status: **active engineering policy for N15-B2R and later v2.x work**.

This document defines how engineering-facing names are normalized without translating UFC/ABNT institutional content or breaking supported v2.x documents.

## 1. Core principle

The engineering language of the project is English for project-owned engineering surfaces: internal identifiers, source comments, tests/checkers/tools, canonical public API and new machine-readable engineering fields.

Do not translate merely for consistency: official UFC/ABNT wording, bibliographic titles, quoted normative text, institutional labels, Portuguese academic example content or historical evidence identifiers whose stability matters.

## 2. Compatibility principle

Public API migration in v2.x is additive.

- supported Portuguese setup keys remain accepted;
- supported Portuguese values remain accepted where already public;
- supported Portuguese project-owned commands/environments remain aliases or wrappers when a canonical English equivalent is introduced;
- upstream commands are not renamed for local style consistency;
- supported public-surface removal requires an explicit deprecation/removal policy and normally a major-version boundary.

Canonical English API may become the documented default without invalidating Portuguese compatibility input.

## 3. Engineering file/directory convention

Use lowercase English names and hyphens where appropriate. Canonical examples include:

- `fonts.def`, `modules.def`, `frontmatter.def`, `institutional.def`;
- `academic-works.def`, `research-projects.def`, `objects.def`, `bibliography.def`, `backmatter.def`;
- `public-api.def` as the canonical public-alias layer;
- future `articles.def`;
- `main.tex`, `frontmatter/`, `chapters/`, `backmatter/`, `figures/`, `assets/institutional/`.

Portuguese academic leaf filenames may remain where translation would create unrelated churn. Historical evidence is not renamed merely for style consistency.

## 4. Public setup keys

Canonical `\ufcsetup` keys use lowercase English kebab-case.

B2R-B2 establishes the complete canonical setup-key vocabulary while preserving all B1 compatibility keys. The implementation is centralized in `abntexto-ufc/public-api.def` and forwards to certified runtime behavior.

Canonical semantic groups are:

- document/profile: `type`, `print-mode`, `cover`, `catalog-card`, `coat-of-arms`;
- institution: `institution`, `institution-acronym`, `center`, `department`;
- academic programs/degrees: `undergraduate-program`, `undergraduate-degree`, `specialization-program`, `masters-graduate-program`, `masters-program`, `masters-degree-field`, `masters-concentration`, doctorate analogues;
- project metadata: `project-program`, `project-type`, `submission-entity`, `project-nature-statement`, `project-identifier`;
- work metadata: `author`, `title`, `subtitle`, `title-variant`, `volume`, `year`, `location`, `approval-date`;
- advisors: `advisor`, `advisor-institution`, `advisor-unit`, `advisor-feminine-label` and coadvisor analogues;
- epigraph: `epigraph-author`;
- committee: `examiner-N`, `examiner-N-unit`, `examiner-N-institution`, currently N=2..6;
- modules/assets/pagination: `font`, `strict-font`, `tables`, `code`, `algorithms`, `glossary`, `index`, `coat-of-arms-file`, `initial-page`.

`volume` is retained as-is because it is already an appropriate canonical English identifier. A compatibility-only project coat-of-arms key does not receive a second canonical English synonym.

## 5. Semantic metadata naming

Canonical metadata names describe the role consumed by the runtime rather than mechanically translate the Portuguese token.

Important distinctions:

- `masters-graduate-program` is the graduate-program line, while `masters-program` is the program/course display name;
- `masters-degree-field` is the field named after the degree title, while `masters-concentration` is the concentration area;
- doctorate fields follow the same distinction;
- `project-nature-statement` is the complete nature statement override, not merely a project category;
- `advisor-feminine-label` and `coadvisor-feminine-label` control grammatical output labels;
- `examiner-N` represents an examination/approval committee member and avoids a literal collection-name translation.

If a new metadata field cannot be named with this level of semantic precision, treat it as an API design decision rather than a cosmetic translation.

## 6. Setup values

Setup-value identity is `(setup key, value)`, not a global value token.

Canonical booleans are `true` / `false`; existing `sim` / `nao` remain compatibility forms where already supported.

Canonical document profile values are:

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`;
- future reserved `article`.

Other B2 canonical values:

- `print-mode`: `single-sided`, `double-sided`;
- `cover`: `auto`, `true`, `false`;
- `font`: `times`, `arial`;
- `tables`: `native`, `tabularray`;
- `code`: `none`, `listings`, `minted`;
- `algorithms`: `none`, `algpseudocodex`;
- `glossary`: `none`, `glossaries`;
- `index`: `none`, `imakeidx`.

Package/runtime identifiers such as `tabularray`, `listings`, `minted`, `algpseudocodex`, `glossaries` and `imakeidx` remain unchanged because those values identify concrete external integrations.

## 7. UFC-owned commands and environments

New canonical project-owned public commands use the `\ufc...` prefix and English semantics.

B2R-B2 does not introduce command or environment aliases. B2R-B3 owns that work.

Reviewed command direction already recorded in the B1 machine inventory includes cover, title-page, approval-page, catalog-card, references and bibliography-resource surfaces. Summary/abstract naming still requires language-role validation before B3 implementation so vernacular and foreign-language behavior are not conflated.

Before adding a command/environment alias, classify the existing surface as canonical project API, Portuguese compatibility API, upstream compatibility API, exported helper or internal implementation. Environment wrappers must preserve semantics, optional arguments and nesting behavior.

## 8. Other engineering identifiers

Python uses English `snake_case`; constants use `UPPER_SNAKE_CASE` where appropriate. New source comments and developer diagnostics are English. New JSON engineering fields use English `snake_case` unless schema/history requires stability.

Historical schema fields are not renamed casually; migration requires compatibility or explicit schema-version handling.

## 9. Names intentionally preserved

Preserve official UFC units, resolutions, guides and acts; official ABNT titles; bibliographic titles; quoted normative text; Portuguese academic examples; stable normative evidence IDs; release/audit IDs already consumed by ledgers; external/upstream commands; and `normativa/` during B2R.

The deprecated legacy class entrypoint remains a compatibility wrapper. Its exact identity is confined to the structured machine inventory and explicitly exempt historical/compatibility surfaces. New narrative occurrences are not allowed.

## 10. Public API contracts

B2R-B uses layered machine evidence:

- `release/n15-b2r-b-public-api.json` — frozen B1 baseline;
- `release/n15-b2r-b2-setup-aliases.json` — B2 additive setup delta;
- `release/n15-b2r-a-naming-inventory.json` — historical B2R-A/N12-sensitive evidence.

The certified B1 baseline blob used by B2 is:

`c1f545e0e707822959db851a74d29f4068dff731`

`tests/checks/public_api_contract.py` validates both B1 and B2 without weakening the frozen `.github/workflows/latex-preflight.yml` boundary. It checks exact setup sets, mapping coverage, command/environment/hook stability, disabled article runtime and the frozen N12 workflow blob.

## 11. Behavioral equivalence

Naming work must not change document semantics or formatting merely because identifiers change.

B2R-B2 verifies semantic forwarding with `tests/normativa/public-api-aliases.tex` and `tests/v2-public-api-alias-check.sh`. All 65 canonical setup keys are exercised and asserted against the corresponding existing runtime state.

B2R-B4 owns complete paired canonical-English/Portuguese semantic and rendered-output equivalence across profiles and representative documents. That later gate should cover structure, PDF/A, reference output, objects/bibliography, post-textuals, Overleaf, deterministic distribution and Windows literal-font certification.

## 12. Article timing

Scientific-article runtime is delayed until B2R-B closes and the resulting `main` is re-certified.

Therefore:

- do not create a temporary Portuguese article module;
- eventual runtime module is canonical `articles.def`;
- canonical surface is reserved as `type=article`;
- Portuguese compatibility form remains reserved;
- reservation is not runtime support;
- article behavior should use centralized profile capabilities or an equivalent policy rather than scattered language-dependent conditionals.

## 13. Current migration state

### B2R-A1 — DONE

Internal module paths normalized by PR #146 and re-certified.

### B2R-A2 — DONE

User/example/distribution engineering layout normalized by PR #148 plus state-sync closure.

### B2R-B1 — DONE

PR #150 established the baseline/checker. PR #151 closed documentation synchronization and produced the certified B2 base:

`1a3731575f9fe06a7f7d9a132f5152998edc6cee`

That SHA passed Source #425, preflight/Gate T #1094 and Distribution #245, including Overleaf and Windows literal-font certification.

### B2R-B2 — ACTIVE

B2 introduces 65 canonical setup keys and 34 canonical enumerated values while preserving the 67 legacy keys and 45 legacy values. Total live setup inventory is 132 keys and 79 scoped values. Commands, environments and hooks remain unchanged.

The active branch is `refactor/n15-b2r-b2-setup-aliases`. Its final PR head must be exact-head certified before merge.

### B2R-B3 — BLOCKED BY B2

Canonical command/environment aliases begin only from the re-certified main produced by B2 closure.

## 14. Mandatory documentation synchronization

After a material naming decision, CI-discovered blocker/fix, PR merge/certification or next-action change, synchronize as applicable:

- `docs/HANDOFF-V2.2.0.md`;
- `docs/B2R-NAMING-INVENTORY.md`;
- active B2R machine delta/ledger;
- this policy when naming decisions/state change;
- user/release documentation when described public surfaces change.

Historical B2R-A and frozen B1 evidence are not rewritten merely to record later phase state.

## 15. Review checklist

Before adding an engineering-facing identifier, verify ownership, semantic precision, naming convention, duplication, compatibility needs, schema/API impact, preservation of official wording and documentation-sync requirements.

If any point is unclear, treat the identifier as an API/design decision rather than a cosmetic rename.
