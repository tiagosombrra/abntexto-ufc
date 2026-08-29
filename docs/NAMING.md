# abntexto-ufc — Naming and public API policy

Updated: 2026-08-29

Status: **active engineering policy for N15-B2R and later v2.x work. B2 setup naming is closed; B3 command/environment naming is ACTIVE.**

## 1. Core principle

Project-owned engineering surfaces use English: internal identifiers, source comments, tests/checkers/tools, canonical public API and new machine-readable engineering fields.

Do not translate merely for engineering consistency: official UFC/ABNT wording, bibliographic titles, quoted normative text, institutional labels, Portuguese academic example content or historical evidence identifiers whose stability matters.

## 2. Compatibility principle

Public API migration in v2.x is additive.

- supported Portuguese setup keys and values remain accepted;
- supported Portuguese project-owned commands/environments remain supported when canonical English wrappers are introduced;
- upstream commands are not renamed merely for local style consistency;
- extension hooks remain stable unless an explicit API decision changes them;
- supported public-surface removal requires an explicit deprecation/removal policy and normally a major-version boundary.

Canonical English API may become the documented default without invalidating Portuguese compatibility input.

## 3. Engineering file/directory convention

Use lowercase English names and hyphens where appropriate. Canonical examples include:

- `fonts.def`, `modules.def`, `frontmatter.def`, `institutional.def`;
- `academic-works.def`, `research-projects.def`, `objects.def`, `bibliography.def`, `backmatter.def`;
- `public-api.def` as the canonical public-alias layer;
- future `articles.def`;
- `main.tex`, `frontmatter/`, `chapters/`, `backmatter/`, `figures/`, `assets/institutional/`.

Portuguese academic leaf filenames may remain where translation would create unrelated churn. Historical evidence is not renamed for style consistency.

## 4. Public setup keys — B2 DONE

Canonical `\ufcsetup` keys use lowercase English kebab-case. B2R-B2 established the complete reviewed canonical setup vocabulary while preserving all B1 compatibility keys.

Final setup inventory:

- 67 legacy keys;
- 65 canonical keys added;
- 132 live setup keys total;
- 45 legacy scoped values;
- 34 canonical scoped values added;
- 79 scoped setup-value identities total.

`volume` remains canonical as-is. The project-specific coat-of-arms compatibility key remains compatibility-only and does not gain a duplicate English synonym.

## 5. Semantic metadata naming

Canonical metadata names describe runtime role rather than mechanically translate Portuguese tokens. Important distinctions include:

- `masters-graduate-program` versus `masters-program`;
- `masters-degree-field` versus `masters-concentration`;
- analogous doctorate fields;
- `project-nature-statement` as the complete nature statement override;
- `advisor-feminine-label` / `coadvisor-feminine-label` as grammatical output switches;
- `examiner-N` / `examiner-N-unit` / `examiner-N-institution` for committee members.

If a new metadata field cannot be named with this precision, treat it as an API-design decision rather than a cosmetic translation.

## 6. Setup values — B2 DONE

Setup-value identity is `(setup key, value)`, not a global value token. Canonical booleans are `true` / `false`; existing `sim` / `nao` remain compatibility forms where already public.

Canonical document profile values are:

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`;
- future reserved `article`.

Other canonical values include `single-sided` / `double-sided`, `auto`, `times` / `arial`, `native`, `none`, and exact external package identifiers such as `tabularray`, `listings`, `minted`, `algpseudocodex`, `glossaries` and `imakeidx`.

## 7. UFC-owned commands — B3 policy

Canonical project-owned public commands use `\ufc` followed by an English UpperCamel semantic name. B3 does not rename already-canonical commands or exported helpers merely for cosmetic consistency.

The B1 47-command surface has complete B3 disposition:

- 7 canonical project commands retained;
- 9 exported English helpers retained;
- upstream `\keywords` retained as upstream API;
- 25 Portuguese compatibility commands mapped to canonical wrappers;
- 5 project public commands with non-canonical names mapped to canonical wrappers.

B3 therefore adds exactly 30 canonical commands without removing any existing command.

Important semantic rules:

- `\ufcPrintAbstract` wraps the existing English-language abstract behavior and preserves the B1-approved target;
- `\ufcPrintSummary` wraps the Portuguese primary-language `Resumo`; it must not collapse into `\ufcPrintAbstract`;
- `\ufcSummaryKeywords` wraps `Palavras-chave`; upstream `\keywords` remains the English-label command;
- `\ufcPrintEpigraph[short|long]` forwards to legacy `[curta|longa]`; Portuguese values remain available through the compatibility command;
- `\ufcPrintListOfTextTables` denotes the distinct UFC/ABNT `quadro` list and must not collapse into statistical tables or charts;
- `\ufcAddBibliographyResource` is the canonical bibliography-resource command;
- `\ufcSource` and `\ufcNote` replace Portuguese project-owned labels in canonical usage;
- `\ufcInputListing` and `\ufcInputMinted` are conditional and must exist only when their corresponding certified legacy module surface exists.

The canonical wrappers live in `abntexto-ufc/public-api.def`; behavior ownership remains in the certified legacy/runtime modules during v2.x.

## 8. UFC-owned environments — B3 policy

Canonical environment names are lowercase `ufc` plus an English semantic name. B3 mappings are:

- `ufcalineas` → `ufclettereditems`;
- `ufcsubalineas` → `ufcdashedsubitems`;
- `ufclistadefinicoes` → `ufcdefinitionlist`;
- `ufcobjeto` → `ufcobject`;
- `ufcalgoritmo` → `ufcalgorithm`.

`ufclisting` is already English and remains canonical as-is.

Environment wrappers must preserve nesting and argument behavior. Canonical signatures are:

- `ufclettereditems`: no arguments;
- `ufcdashedsubitems`: no arguments;
- `ufcdefinitionlist`: optional width, default `3cm`;
- `ufcobject`: optional placement, default `\placepos`;
- `ufcalgorithm`: optional placement and line-number frequency, defaults `\placepos` and `1`;
- `ufclisting`: optional placement and conditional availability under `code=listings`.

## 9. Exported helpers and upstream surfaces

Do not create aliases merely to make every exported symbol look uniform. Retained project helpers include page-break, heading, TOC and optional-module setup helpers already expressed in English. Upstream compatibility surfaces such as `\keywords`, `\textapud`, `\usechapters` and `\printlegendbox` keep their upstream identities.

Extension hooks remain `\ufcsectionhook` and `\ufcobjectlegendhook` throughout B3.

## 10. Other engineering identifiers

Python uses English `snake_case`; constants use `UPPER_SNAKE_CASE` where appropriate. New source comments and developer diagnostics are English. New JSON engineering fields use English `snake_case` unless schema/history requires stability.

Historical schema fields are not renamed casually; migration requires compatibility or explicit schema-version handling.

## 11. Names intentionally preserved

Preserve official UFC units, resolutions, guides and acts; official ABNT titles; bibliographic titles; quoted normative text; Portuguese academic examples; stable normative evidence IDs; release/audit IDs already consumed by ledgers; external/upstream commands; and `normativa/` during B2R.

The deprecated legacy class entrypoint remains a compatibility wrapper. Its exact identity stays confined to structured machine inventory and explicitly exempt historical/compatibility surfaces; arbitrary narrative occurrences remain disallowed.

## 12. Public API contracts

B2R-B uses layered machine evidence:

- `release/n15-b2r-b-public-api.json` — frozen B1 baseline;
- `release/n15-b2r-b2-setup-aliases.json` — frozen B2 additive setup delta;
- `release/n15-b2r-b3-command-environment-aliases.json` — active B3 command/environment delta;
- `release/n15-b2r-a-naming-inventory.json` — historical B2R-A/N12 evidence.

Frozen blobs used by B3:

- B1: `c1f545e0e707822959db851a74d29f4068dff731`;
- B2: `19df208fb59af5ea37556d962e5986a43094c7f5`;
- N12 workflow: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

`tests/checks/public_api_contract.py` validates B1+B2+B3 in layers. B3 may expand commands/environments only; setup surfaces and hooks remain exact.

## 13. Behavioral equivalence

Naming work must not change document semantics or formatting merely because identifiers change.

B2 validates setup forwarding through `tests/normativa/public-api-aliases.tex` and `tests/v2-public-api-alias-check.sh`.

B3 validates command/environment presence and conditional activation through:

- `tests/normativa/public-api-command-environment-aliases.tex`;
- `tests/v2-public-api-command-environment-check.sh`.

B2R-B4 owns complete paired Portuguese/canonical semantic and rendered-output equivalence across profiles and representative documents. That later gate must cover structure, PDF/A, reference output, objects/bibliography, post-textuals, Overleaf, deterministic distribution and Windows literal-font certification.

## 14. Article timing

Scientific-article runtime is delayed until B2R-B closes and the resulting `main` is re-certified.

Therefore:

- no temporary Portuguese article module;
- eventual runtime module is canonical `articles.def`;
- canonical surface remains reserved as `type=article`;
- Portuguese compatibility form remains reserved;
- reservation is not runtime support;
- article behavior should use centralized profile capabilities or equivalent policy rather than scattered language-dependent conditionals.

## 15. Current migration state

### B2R-A1 — DONE

Internal module paths normalized by PR #146 and re-certified.

### B2R-A2 — DONE

User/example/distribution engineering layout normalized by PR #148 plus state-sync closure.

### B2R-B1 — DONE

PR #150 established the API baseline/checker; PR #151 closed its state sync.

### B2R-B2 — DONE

PR #152 implemented canonical setup aliases; PR #153 closed the bounded state sync. Certified B3 base:

`cb0df822401a926c4c5987f904b29f5898fb1775`

Certification:

- Source #429 — SUCCESS, run `33249228729`;
- preflight/Gate T #1100 — SUCCESS, run `33249228669`;
- Distribution #247 — SUCCESS, run `33249228670`;
- Overleaf and Windows literal-font build/certification — SUCCESS.

### B2R-B3 — ACTIVE

Branch: `refactor/n15-b2r-b3-command-environment-aliases`.

Machine contract, wrappers, checker extension and command/environment smoke evidence are implemented. The next gate is exact-head PR certification.

### B2R-B4 — BLOCKED BY B3

B4 begins only from the re-certified main produced by B3 closure.

## 16. Mandatory documentation synchronization

After a material naming decision, CI-discovered blocker/fix, PR merge/certification or next-action change, synchronize as applicable:

- `docs/HANDOFF-V2.2.0.md`;
- `docs/B2R-NAMING-INVENTORY.md`;
- active B2R machine delta/ledger;
- this policy when naming decisions/state change;
- user/release documentation when described public surfaces change.

Historical B2R-A and frozen B1/B2 evidence are not rewritten merely to record later phase state.

A bounded state sync may be used after B3 merge if final receipts require it, but no unbounded receipt loop is allowed.

## 17. Review checklist

Before adding an engineering-facing identifier, verify ownership, semantic precision, naming convention, duplication, compatibility needs, schema/API impact, optional-module lifetime, preservation of official wording and documentation-sync requirements.

If any point is unclear, treat the identifier as an API/design decision rather than a cosmetic rename.
