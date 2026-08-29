# abntexto-ufc — Naming and public API policy

Updated: 2026-08-29

Status: **active engineering policy for v2.x. N15-B2R setup, command/environment naming and EN/PT behavioral-equivalence certification are DONE. The bounded B4 post-merge state sync is the only remaining transition step before N15-B2B scientific-article runtime.**

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
- article runtime module `articles.def`;
- `main.tex`, `frontmatter/`, `chapters/`, `backmatter/`, `figures/`, `assets/institutional/`.

Portuguese academic leaf filenames may remain where translation would create unrelated churn. Historical evidence is not renamed for style consistency.

## 4. Public setup keys — B2 DONE

Canonical `\ufcsetup` keys use lowercase English kebab-case. Final setup inventory:

- 67 compatibility keys;
- 65 canonical additions;
- 132 live setup keys total;
- 45 compatibility scoped values;
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
- reserved `article`, activated only by N15-B2B runtime.

Other canonical values include `single-sided` / `double-sided`, `auto`, `times` / `arial`, `native`, `none`, and exact external package identifiers such as `tabularray`, `listings`, `minted`, `algpseudocodex`, `glossaries` and `imakeidx`.

## 7. UFC-owned commands — B3 DONE

Canonical project-owned public commands use `\ufc` followed by an English UpperCamel semantic name. Already-canonical commands and exported helpers are not renamed merely for cosmetic consistency.

B3 added exactly 30 canonical commands without removing any existing command, producing 77 live commands total.

Important semantic rules:

- `\ufcPrintAbstract` wraps the existing English-language abstract behavior;
- `\ufcPrintSummary` wraps the Portuguese primary-language `Resumo`; it must not collapse into `\ufcPrintAbstract`;
- `\ufcSummaryKeywords` wraps `Palavras-chave`; upstream `\keywords` remains the English-label command;
- `\ufcPrintEpigraph[short|long]` forwards to compatibility `[curta|longa]`;
- `\ufcPrintListOfTextTables` denotes the distinct UFC/ABNT `quadro` list;
- `\ufcAddBibliographyResource` is the canonical bibliography-resource command;
- `\ufcSource` and `\ufcNote` are canonical object-source/note commands;
- `\ufcInputListing` and `\ufcInputMinted` are conditional on their corresponding certified code modules.

Canonical wrappers live in `abntexto-ufc/public-api.def`; behavior ownership remains in the certified compatibility/runtime modules during v2.x unless a later phase explicitly changes it.

## 8. UFC-owned environments — B3 DONE

Canonical environment mappings are:

- `ufcalineas` → `ufclettereditems`;
- `ufcsubalineas` → `ufcdashedsubitems`;
- `ufclistadefinicoes` → `ufcdefinitionlist`;
- `ufcobjeto` → `ufcobject`;
- `ufcalgoritmo` → `ufcalgorithm`.

`ufclisting` is already English and remains canonical as-is.

Environment wrappers preserve the certified signatures and nesting behavior.

## 9. Exported helpers and upstream surfaces

Do not create aliases merely to make every exported symbol look uniform. Retained project helpers include page-break, heading, TOC and optional-module setup helpers already expressed in English. Upstream compatibility surfaces such as `\keywords`, `\textapud`, `\usechapters` and `\printlegendbox` keep their upstream identities.

Extension hooks remain `\ufcsectionhook` and `\ufcobjectlegendhook`.

## 10. Other engineering identifiers

Python uses English `snake_case`; constants use `UPPER_SNAKE_CASE` where appropriate. New source comments and developer diagnostics are English. New JSON engineering fields use English `snake_case` unless schema/history requires stability.

Historical schema fields are not renamed casually; migration requires compatibility or explicit schema-version handling.

## 11. Names intentionally preserved

Preserve official UFC units, resolutions, guides and acts; official ABNT titles; bibliographic titles; quoted normative text; Portuguese academic examples; stable normative evidence IDs; release/audit IDs already consumed by ledgers; external/upstream commands; and `normativa/` during v2.x unless a dedicated migration explicitly changes it.

The deprecated compatibility class entrypoint remains a wrapper. Its exact identifier stays confined to structured machine inventory and explicitly exempt historical/compatibility surfaces; arbitrary narrative occurrences remain disallowed.

## 12. Layered public API contracts — B2R DONE

B2R-B uses cumulative machine evidence:

- `release/n15-b2r-b-public-api.json` — frozen B1 baseline;
- `release/n15-b2r-b2-setup-aliases.json` — frozen B2 setup delta;
- `release/n15-b2r-b3-command-environment-aliases.json` — frozen B3 command/environment delta;
- `release/n15-b2r-b4-en-pt-equivalence.json` — completed B4 equivalence record;
- `release/n15-b2r-a-naming-inventory.json` — historical B2R-A/N12 evidence.

Frozen B4 identities:

- B1 blob `c1f545e0e707822959db851a74d29f4068dff731`;
- B2 blob `19df208fb59af5ea37556d962e5986a43094c7f5`;
- B3 blob `bfcbf8aca3fba3fd602f62895f10fa2d6277b5a4`;
- public-API runtime blob `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- N12 workflow blob `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

Final public counts are 132 setup keys, 79 scoped values, 77 commands, 11 environments and 2 hooks.

## 13. Behavioral equivalence — B4 DONE

Naming migration is certified not to change document semantics or formatting across the reviewed Portuguese/canonical-English surfaces.

B4 static checks certified all setup, setup-value, command and environment forwarding while freezing B1/B2/B3/runtime/N12 identities.

Paired runtime checks certified:

- exact normalized internal-state equality;
- exact extracted layout-text equality;
- equal page count and dimensions;
- equal generated TOC/list/bibliography artifacts;
- equal per-page raster SHA-256 at fixed rendering parameters;
- PDF/A-2b declaration for both outputs.

Final exact-head B4 evidence on PR #155:

- head `44c9c5082598b82e67a0b3ef009c4bb71a584571`;
- `behind_by=0`;
- Source #442 — SUCCESS, run `33262519263`;
- preflight #1115 — SUCCESS, run `33262519254`;
- 66 normalized state lines, 23 pages, raster equality on all pages;
- all state/text/geometry/auxiliary/raster/PDF-A predicates true;
- structural summary `PASS=16 FAIL=0 SKIP=0`.

Protected squash merge produced `main` `a4f2660ef46826c7d61a7dc3d9de6554f6d6a825`, then:

- Source #443 — SUCCESS, run `33263191118`;
- preflight push #1116 — SUCCESS, run `33263191096`;
- Gate T #1117 — SUCCESS, run `33263196260`;
- Distribution #249 — SUCCESS, run `33263191120`;
- Overleaf and Windows literal-font build/certification — SUCCESS;
- PDF/A and deterministic packaging — SUCCESS.

No public-runtime/API divergence was observed during B4.

## 14. Scientific-article naming boundary — N15-B2B next

B2R no longer blocks article support. After the bounded B4 state-sync is certified and merged, N15-B2B activates the reserved article profile.

Article runtime rules:

- canonical module name: `articles.def`;
- canonical setup surface: `type=article`;
- Portuguese compatibility form is additive and must follow the established v2.x policy;
- reservation before B2B is not runtime support;
- article behavior should use centralized profile capabilities or equivalent policy rather than scattered language-dependent conditionals;
- article additions must not regress thesis/dissertation/project profiles or rewrite the frozen B2R compatibility semantics unnecessarily.

## 15. Current migration state

- B2R-A1 — DONE, PR #146;
- B2R-A2 — DONE, PR #148 + state sync;
- B2R-B1 — DONE, PR #150 + PR #151;
- B2R-B2 — DONE, PR #152 + PR #153;
- B2R-B3 — DONE, PR #154;
- B2R-B4 — DONE, PR #155, certified `main` `a4f2660e...`;
- bounded B4 post-merge documentation sync — ACTIVE;
- N15-B2B — next runtime phase after sync certification.

## 16. Mandatory documentation synchronization

After a material naming decision, PR merge/certification or next-action change, synchronize as applicable:

- `docs/HANDOFF-V2.2.0.md`;
- `docs/B2R-NAMING-INVENTORY.md`;
- active B2R machine delta/ledger;
- this policy when naming decisions/state change;
- user/release documentation when described public surfaces change.

Historical B2R-A and frozen B1/B2/B3 evidence are not rewritten merely to record later phase state.

Avoid receipt loops: state-sync exact-head/resulting-main receipts may live in the PR/final execution report after the tracked documents already record the primary B4 certification.

## 17. Review checklist

Before adding an engineering-facing identifier, verify ownership, semantic precision, naming convention, duplication, compatibility needs, schema/API impact, optional-module lifetime, preservation of official wording and documentation-sync requirements.

For N15-B2B, additionally verify that article-specific API is genuinely required, is canonical in English, has the necessary Portuguese v2.x compatibility route, and does not leak article assumptions into unrelated profiles.
