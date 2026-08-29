# abntexto-ufc — Naming and public API policy

Updated: 2026-08-29

Status: **active engineering policy for N15-B2R and later v2.x work. Setup naming (B2) and command/environment naming (B3) are closed; B4 EN/PT behavioral equivalence is ACTIVE.**

## 1. Core principle

Project-owned engineering surfaces use English: internal identifiers, source comments, tests/checkers/tools, canonical public API and new machine-readable engineering fields.

Do not translate merely for engineering consistency: official UFC/ABNT wording, bibliographic titles, quoted normative text, institutional labels, Portuguese academic example content or historical evidence identifiers whose stability matters.

## 2. Compatibility principle

Public API migration in v2.x is additive.

- supported Portuguese setup keys and values remain accepted;
- supported Portuguese project-owned commands/environments remain supported alongside canonical English wrappers;
- upstream commands are not renamed merely for local style consistency;
- extension hooks remain stable unless an explicit API decision changes them;
- supported public-surface removal requires an explicit deprecation/removal policy and normally a major-version boundary.

Canonical English API may be the documented default without invalidating Portuguese compatibility input.

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

`volume` remains canonical as-is. The project-specific coat-of-arms compatibility synonym remains compatibility-only and does not gain a duplicate English synonym.

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

## 7. UFC-owned commands — B3 DONE

Canonical project-owned public commands use `\ufc` followed by an English UpperCamel semantic name. Already-canonical commands and exported helpers are not renamed merely for cosmetic consistency.

The completed B3 disposition is:

- 7 canonical project commands retained;
- 9 exported English helpers retained;
- upstream `\keywords` retained as upstream API;
- 25 Portuguese compatibility commands mapped to canonical wrappers;
- 5 project public commands with non-canonical names mapped to canonical wrappers.

B3 added exactly 30 canonical commands without removing any existing command, producing 77 live commands total.

Important semantic rules:

- `\ufcPrintAbstract` wraps the existing English-language abstract behavior and preserves the B1-approved target;
- `\ufcPrintSummary` wraps the Portuguese primary-language `Resumo`; it must not collapse into `\ufcPrintAbstract`;
- `\ufcSummaryKeywords` wraps `Palavras-chave`; upstream `\keywords` remains the English-label command;
- `\ufcPrintEpigraph[short|long]` forwards to compatibility `[curta|longa]`;
- `\ufcPrintListOfTextTables` denotes the distinct UFC/ABNT `quadro` list and must not collapse into statistical tables or charts;
- `\ufcAddBibliographyResource` is the canonical bibliography-resource command;
- `\ufcSource` and `\ufcNote` are the canonical object-source/note commands;
- `\ufcInputListing` and `\ufcInputMinted` are conditional and exist only when their corresponding certified module surface exists.

Canonical wrappers live in `abntexto-ufc/public-api.def`; behavior ownership remains in the certified compatibility/runtime modules during v2.x.

## 8. UFC-owned environments — B3 DONE

Canonical environment names are lowercase `ufc` plus an English semantic name. Completed mappings are:

- `ufcalineas` → `ufclettereditems`;
- `ufcsubalineas` → `ufcdashedsubitems`;
- `ufclistadefinicoes` → `ufcdefinitionlist`;
- `ufcobjeto` → `ufcobject`;
- `ufcalgoritmo` → `ufcalgorithm`.

`ufclisting` is already English and remains canonical as-is.

Environment wrappers preserve nesting and argument behavior. Canonical signatures are:

- `ufclettereditems`: no arguments;
- `ufcdashedsubitems`: no arguments;
- `ufcdefinitionlist`: optional width, default `3cm`;
- `ufcobject`: optional placement, default `\placepos`;
- `ufcalgorithm`: optional placement and line-number frequency, defaults `\placepos` and `1`;
- `ufclisting`: optional placement and conditional availability under `code=listings`.

## 9. Exported helpers and upstream surfaces

Do not create aliases merely to make every exported symbol look uniform. Retained project helpers include page-break, heading, TOC and optional-module setup helpers already expressed in English. Upstream compatibility surfaces such as `\keywords`, `\textapud`, `\usechapters` and `\printlegendbox` keep their upstream identities.

Extension hooks remain `\ufcsectionhook` and `\ufcobjectlegendhook`.

## 10. Other engineering identifiers

Python uses English `snake_case`; constants use `UPPER_SNAKE_CASE` where appropriate. New source comments and developer diagnostics are English. New JSON engineering fields use English `snake_case` unless schema/history requires stability.

Historical schema fields are not renamed casually; migration requires compatibility or explicit schema-version handling.

## 11. Names intentionally preserved

Preserve official UFC units, resolutions, guides and acts; official ABNT titles; bibliographic titles; quoted normative text; Portuguese academic examples; stable normative evidence IDs; release/audit IDs already consumed by ledgers; external/upstream commands; and `normativa/` during B2R.

The deprecated compatibility class entrypoint remains a wrapper. Its exact identifier stays confined to structured machine inventory and explicitly exempt historical/compatibility surfaces; arbitrary narrative occurrences remain disallowed.

## 12. Layered public API contracts

B2R-B uses cumulative machine evidence:

- `release/n15-b2r-b-public-api.json` — frozen B1 baseline;
- `release/n15-b2r-b2-setup-aliases.json` — frozen B2 additive setup delta;
- `release/n15-b2r-b3-command-environment-aliases.json` — frozen B3 command/environment delta;
- `release/n15-b2r-b4-en-pt-equivalence.json` — active B4 equivalence contract;
- `release/n15-b2r-a-naming-inventory.json` — historical B2R-A/N12 evidence.

B4 freezes:

- B1 blob `c1f545e0e707822959db851a74d29f4068dff731`;
- B2 blob `19df208fb59af5ea37556d962e5986a43094c7f5`;
- B3 blob `bfcbf8aca3fba3fd602f62895f10fa2d6277b5a4`;
- public-API runtime blob `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- N12 workflow blob `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

`tests/checks/public_api_contract.py` validates B1+B2+B3 in layers. B4 may not expand or rewrite that API surface.

## 13. Behavioral equivalence — B4 ACTIVE

Naming migration is complete only when identifier changes are proven not to change document semantics or formatting.

Earlier evidence:

- B2 validates setup forwarding through `tests/normativa/public-api-aliases.tex` and `tests/v2-public-api-alias-check.sh`;
- B3 validates command/environment presence and conditional activation through `tests/normativa/public-api-command-environment-aliases.tex` and `tests/v2-public-api-command-environment-check.sh`.

B4 adds the complete paired compatibility/canonical proof while freezing the certified runtime.

Static B4 checks require:

- all 65 distinct canonical setup-key mappings plus retained `volume`;
- all 45 reviewed legacy setup-value source identities to resolve through the canonical choices;
- all 30 canonical command wrappers to retain their declared compatibility target;
- all 5 canonical environment wrappers to retain their declared compatibility environment;
- exact B1/B2/B3/runtime/N12 blob identities;
- unchanged public counts: 132 setup keys, 79 scoped values, 77 commands, 11 environments, 2 hooks.

Paired runtime checks compile equivalent PT and EN documents and require:

- exact normalized internal-state equality;
- exact extracted layout-text equality;
- equal page count and dimensions;
- equal generated TOC/list/bibliography artifacts when present;
- equal per-page raster SHA-256 at fixed rendering parameters;
- PDF/A-2b declaration for both outputs.

Raw PDF byte identity is not required because metadata/internal identifiers may differ without changing observable output.

B4 evidence files are:

- `tests/checks/public_api_equivalence_contract.py`;
- `tests/normativa/public-api-equivalence.tex`;
- `tests/fixtures/public-api-equivalence-summary.tex`;
- `tests/v2-public-api-equivalence-check.sh`.

`tests/run.py` makes the repository audit depend on B4 equivalence. This deliberately reuses the existing frozen preflight workflow instead of editing N12.

Full B4 closure still requires the normal post-merge Gate T and Distribution, which cover both document engines, all profiles, PDF/A, objects/bibliography, post-textuals, Overleaf, deterministic packaging and Windows literal-font certification.

## 14. Article timing

Scientific-article runtime is delayed until B2R-B4 closes and the resulting `main` is fully re-certified.

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

PR #152 implemented canonical setup aliases; PR #153 closed the bounded state sync.

### B2R-B3 — DONE

PR #154 was exact-head certified and squash-merged. Resulting B4 base:

`92f17418dfeee4d2d45456912af9f8c399457cc1`

Certification:

- Source #433 — SUCCESS, run `33253212796`;
- preflight push #1105 — SUCCESS, run `33253212823`;
- Gate T #1106 — SUCCESS, run `33253216564`;
- Distribution #248 — SUCCESS, run `33253212813`;
- Overleaf and Windows literal-font build/certification — SUCCESS.

### B2R-B4 — ACTIVE

Branch: `refactor/n15-b2r-b4-en-pt-equivalence`.

B4 owns equivalence evidence only. It does not own runtime/API changes. Its PR must be certified on an exact head, then the resulting `main` must pass Source, full Gate T and Distribution before N15-B2B is unblocked.

## 16. Mandatory documentation synchronization

After a material naming decision, CI-discovered blocker/fix, PR merge/certification or next-action change, synchronize as applicable:

- `docs/HANDOFF-V2.2.0.md`;
- `docs/B2R-NAMING-INVENTORY.md`;
- active B2R machine delta/ledger;
- this policy when naming decisions/state change;
- user/release documentation when described public surfaces change.

Historical B2R-A and frozen B1/B2/B3 evidence are not rewritten merely to record later phase state.

Avoid receipt loops: active-phase documentation may record the prior phase's certified base, while live CI remains execution authority for the current phase.

## 17. Review checklist

Before adding an engineering-facing identifier, verify ownership, semantic precision, naming convention, duplication, compatibility needs, schema/API impact, optional-module lifetime, preservation of official wording and documentation-sync requirements.

During B4 specifically, any observed PT/EN mismatch must be classified before changing code. Evidence/fixture defects should be fixed in evidence; a real runtime defect requires an explicit scope decision because the B3 runtime is frozen.
