# abntexto-ufc — Naming and public API policy

Updated: 2026-08-29

Status: **active engineering policy for N15-B2R and later v2.x work. B2 setup naming is closed; B3 command/environment naming is next.**

## 1. Core principle

Project-owned engineering surfaces use English: internal identifiers, source comments, tests/checkers/tools, canonical public API and new machine-readable engineering fields.

Do not translate merely for engineering consistency: official UFC/ABNT wording, bibliographic titles, quoted normative text, institutional labels, Portuguese academic example content or historical evidence identifiers whose stability matters.

## 2. Compatibility principle

Public API migration in v2.x is additive.

- supported Portuguese setup keys and values remain accepted;
- supported Portuguese project-owned commands/environments remain aliases or wrappers when a canonical English equivalent is introduced;
- upstream commands are not renamed for local style consistency;
- extension hooks remain stable unless an explicit API decision changes them;
- supported public-surface removal requires a deprecation/removal policy and normally a major-version boundary.

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

Canonical `\ufcsetup` keys use lowercase English kebab-case.

B2R-B2 established the complete reviewed canonical setup-key vocabulary while preserving all B1 compatibility keys. The implementation is centralized in `abntexto-ufc/public-api.def` and forwards to certified runtime behavior.

Final B2 setup inventory:

- 67 legacy keys;
- 65 canonical keys added;
- 132 live setup keys total;
- 45 legacy enumerated `(key,value)` identities;
- 34 canonical enumerated identities added;
- 79 scoped setup-value identities total.

Canonical semantic groups include document/profile, institution, academic programs/degrees, project metadata, work metadata, advisors, epigraph, committee/examiners, optional modules, assets and pagination.

`volume` is retained as-is because it is already an appropriate canonical English identifier. A compatibility-only project coat-of-arms key does not receive a second canonical synonym.

## 5. Semantic metadata naming

Canonical metadata names describe the role consumed by runtime rather than mechanically translate Portuguese tokens.

Important distinctions include:

- `masters-graduate-program` versus `masters-program`;
- `masters-degree-field` versus `masters-concentration`;
- analogous doctorate fields;
- `project-nature-statement` as the complete nature statement override;
- `advisor-feminine-label` and `coadvisor-feminine-label` as grammatical output switches;
- `examiner-N` / `examiner-N-unit` / `examiner-N-institution` for committee members.

If a new metadata field cannot be named with this semantic precision, treat it as an API design decision rather than a cosmetic translation.

## 6. Setup values — B2 DONE

Setup-value identity is `(setup key, value)`, not a global value token.

Canonical booleans are `true` / `false`; existing `sim` / `nao` remain compatibility forms where already supported.

Canonical document profile values:

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

External package/runtime identifiers remain unchanged when they identify concrete integrations.

## 7. UFC-owned commands and environments — B3 policy

New canonical project-owned public commands use the `\ufc...` prefix and English semantics.

B2R-B3 owns command/environment aliases. It must **not** mechanically create canonical aliases for all 47 exported commands or all 6 UFC environments. Each exported surface must first be classified as one of:

- canonical project API;
- Portuguese compatibility API;
- upstream compatibility API;
- exported helper;
- extension hook;
- internal implementation accidentally exported.

Only supported project API receives new canonical wrappers. Existing Portuguese public surfaces remain supported during v2.x.

Known reviewed command directions from the B1 inventory include cover, title page, approval page, catalog card, references and bibliography-resource behavior. Summary/abstract naming requires explicit language-role validation before implementation so vernacular and foreign-language summary semantics are not conflated.

Environment wrappers must preserve semantics, optional arguments and nesting behavior.

## 8. Other engineering identifiers

Python uses English `snake_case`; constants use `UPPER_SNAKE_CASE` where appropriate. New source comments and developer diagnostics are English. New JSON engineering fields use English `snake_case` unless schema/history requires stability.

Historical schema fields are not renamed casually; migration requires compatibility or explicit schema-version handling.

## 9. Names intentionally preserved

Preserve official UFC units, resolutions, guides and acts; official ABNT titles; bibliographic titles; quoted normative text; Portuguese academic examples; stable normative evidence IDs; release/audit IDs already consumed by ledgers; external/upstream commands; and `normativa/` during B2R.

The deprecated legacy class entrypoint remains a compatibility wrapper. Its exact identity is confined to structured machine inventory and explicitly exempt historical/compatibility surfaces; arbitrary narrative occurrences remain disallowed.

## 10. Public API contracts

B2R-B uses layered machine evidence:

- `release/n15-b2r-b-public-api.json` — frozen B1 baseline;
- `release/n15-b2r-b2-setup-aliases.json` — B2 additive setup delta/closure evidence;
- `release/n15-b2r-a-naming-inventory.json` — historical B2R-A/N12-sensitive evidence.

Certified B1 baseline blob:

`c1f545e0e707822959db851a74d29f4068dff731`

Frozen N12 workflow blob:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

`tests/checks/public_api_contract.py` validates B1+B2 exact setup sets, mapping coverage, command/environment/hook stability, disabled article runtime and frozen workflow boundaries.

## 11. Behavioral equivalence

Naming work must not change document semantics or formatting merely because identifiers change.

B2R-B2 verifies semantic setup forwarding with `tests/normativa/public-api-aliases.tex` and `tests/v2-public-api-alias-check.sh`; all 65 canonical setup keys are exercised and asserted against existing runtime state.

B2R-B4 owns complete paired canonical-English/Portuguese semantic and rendered-output equivalence across profiles and representative documents. That gate must cover structure, PDF/A, reference output, objects/bibliography, post-textuals, Overleaf, deterministic distribution and Windows literal-font certification.

## 12. Article timing

Scientific-article runtime is delayed until B2R-B closes and the resulting `main` is re-certified.

Therefore:

- do not create a temporary Portuguese article module;
- eventual runtime module is canonical `articles.def`;
- canonical surface is reserved as `type=article`;
- Portuguese compatibility form remains reserved;
- reservation is not runtime support;
- article behavior should use centralized profile capabilities or equivalent policy rather than scattered language-dependent conditionals.

## 13. Current migration state

### B2R-A1 — DONE

Internal module paths normalized by PR #146 and re-certified.

### B2R-A2 — DONE

User/example/distribution engineering layout normalized by PR #148 plus state-sync closure.

### B2R-B1 — DONE

PR #150 established the baseline/checker. PR #151 closed documentation synchronization and produced certified B2 base `1a3731575f9fe06a7f7d9a132f5152998edc6cee`.

### B2R-B2 — DONE IMPLEMENTATION

PR #152 was exact-head certified and squash-merged. Resulting certified implementation main:

`f6ba39bcbe50c324f6ab5f1856595cfcf7f8f0f9`

Receipts:

- Source #427 — SUCCESS, run `33247641697`;
- preflight/Gate T #1097 — SUCCESS, run `33247641696`;
- Distribution #246 — SUCCESS, run `33247641702`;
- Overleaf and Windows literal-font build/certification — SUCCESS.

Current bounded state-sync branch: `docs/n15-b2r-b2-post-merge-sync`.

After this state-sync is merged and its resulting `main` is certified once, B2 is closed without another receipt-only PR.

### B2R-B3 — NEXT

Create `refactor/n15-b2r-b3-command-environment-aliases` from the exact certified main produced after the bounded B2 state sync. First action is classification of the 47 exported commands and 6 UFC environments; implementation follows the reviewed classification.

## 14. Mandatory documentation synchronization

After a material naming decision, CI-discovered blocker/fix, PR merge/certification or next-action change, synchronize as applicable:

- `docs/HANDOFF-V2.2.0.md`;
- `docs/B2R-NAMING-INVENTORY.md`;
- active B2R machine delta/ledger;
- this policy when naming decisions/state change;
- user/release documentation when described public surfaces change.

Historical B2R-A and frozen B1 evidence are not rewritten merely to record later phase state.

A state-sync may be bounded to prevent an infinite receipt loop: once a state-sync PR itself is merged and its resulting main is re-certified, the next implementation branch becomes the place to record continuation state.

## 15. Review checklist

Before adding an engineering-facing identifier, verify ownership, semantic precision, naming convention, duplication, compatibility needs, schema/API impact, preservation of official wording and documentation-sync requirements.

If any point is unclear, treat the identifier as an API/design decision rather than a cosmetic rename.
