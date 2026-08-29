# abntexto-ufc — Naming and public API policy

Updated: 2026-08-28

Status: **active engineering policy for N15-B2R and later v2.x work**.

This document defines how engineering-facing names are normalized without translating UFC/ABNT institutional content or breaking supported v2.x documents.

## 1. Core principle

The engineering language of the project is English.

This applies to new or normalized:

- internal implementation filenames and identifiers;
- source-code comments and developer diagnostics;
- test/checker/tool names;
- canonical public API names owned by `abntexto-ufc`;
- machine-readable engineering fields when schema/history permits.

It does **not** mean translating:

- academic content;
- official UFC/ABNT names;
- bibliographic titles;
- normative quotations;
- institutional labels;
- historical evidence identifiers whose stability matters.

## 2. Compatibility principle

Public API work in v2.x is additive.

- supported Portuguese setup keys remain accepted;
- supported Portuguese values remain accepted where already public;
- supported Portuguese UFC-owned commands/environments remain aliases or compatibility wrappers;
- upstream commands are not renamed merely for local style consistency;
- removal of a supported public surface requires a separate deprecation/removal policy and normally a major-version boundary.

Canonical English API may become the documented default without invalidating Portuguese compatibility input.

## 3. File and directory conventions

Use lowercase English names with hyphens for multiple words when appropriate.

Canonical examples already adopted:

- `fonts.def`;
- `modules.def`;
- `frontmatter.def`;
- `institutional.def`;
- `academic-works.def`;
- `research-projects.def`;
- `objects.def`;
- `bibliography.def`;
- `backmatter.def`;
- future `articles.def`;
- `main.tex`;
- `frontmatter/`;
- `chapters/`;
- `backmatter/`;
- `figures/`;
- `assets/institutional/`.

Do not rename historical evidence merely for style consistency when the change would damage traceability or create disproportionate churn.

## 4. Public setup keys

Canonical `\ufcsetup` keys introduced by B2R-B use lowercase English kebab-case.

Representative target vocabulary:

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

Existing Portuguese keys such as `tipo`, `impressao`, `capa`, `ficha-catalografica`, `brasao`, `fonte`, `codigo`, `autor`, `titulo`, `orientador` and `coorientador` remain compatibility surfaces throughout v2.x.

B2R-A did **not** introduce these public API aliases; that belongs to B2R-B.

## 5. Setup values

Canonical booleans use:

- `true`;
- `false`.

Existing `sim` / `nao` remain compatibility values where currently supported.

Canonical profile values should be internationally explicit. Current target vocabulary includes:

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`;
- `article`.

Do not choose an English term whose international academic meaning is materially ambiguous when a more precise name exists.

## 6. UFC-owned commands and environments

New canonical UFC-owned public commands use a consistent `\ufc...` prefix and English semantics. Representative future style:

- `\ufcPrintCover`;
- `\ufcPrintTitlePage`;
- `\ufcPrintApprovalPage`;
- `\ufcPrintCatalogCard`;
- `\ufcPrintAbstract`;
- `\ufcPrintReferences`;
- `\ufcAddBibliographyResource`.

Before renaming or aliasing a command, classify it as:

1. canonical `abntexto-ufc` API;
2. Portuguese compatibility API;
3. upstream compatibility API;
4. private/internal implementation.

No public rename is justified by spelling alone. Environment aliases must preserve semantics and nesting behavior.

## 7. Other engineering identifiers

Python uses conventional English `snake_case`; constants use `UPPER_SNAKE_CASE` where appropriate. JavaScript follows the project convention with English semantic names.

New JSON engineering fields use English `snake_case` unless an established schema requires otherwise. Historical schema fields are not renamed casually; schema migration requires compatibility or a version change.

New source-code comments and developer-facing diagnostics are written in English. User-facing academic text may remain Portuguese.

## 8. Names intentionally preserved

Do not translate merely for consistency:

- official UFC units, resolutions, guides and acts;
- official ABNT standard titles;
- bibliographic titles;
- quoted normative text;
- Portuguese academic example content;
- stable `abnt-nbr-*` and `ufc-guia-*` evidence IDs;
- release/audit identifiers already consumed by ledgers;
- external/upstream command names;
- `normativa/` during B2R, because traceability/churn cost outweighs cosmetic benefit.

Portuguese leaf filenames that directly describe academic content may also remain when translating them would create unrelated churn. A2 therefore keeps names such as `frontmatter/resumo.tex`, `backmatter/apendices/` and `backmatter/anexos/`.

## 9. Repository normalization boundary

B2R-A normalized package/example paths only when every active consumer was updated and regression evidence remained green.

The policy permits source and distributed layouts to differ when user experience requires it. For **B2R-A2, the reviewed decision is more specific**: repository source, complete template bundle and Overleaf bundle use the same canonical content layout, with `main.tex` at the bundle/import root.

Current A2 layout:

```text
main.tex
frontmatter/
chapters/
backmatter/
figures/
assets/institutional/ufc-coat-of-arms.png   # source-only
```

The institutional asset remains excluded from public bundles. Renaming the source-only asset does not change its licensing or redistribution policy.

CTAN has its own smaller install/document surface and is not required to contain the complete project example tree.

## 10. Public API contract requirement

B2R-B must create a machine-readable public API inventory before or together with canonical public aliases.

The contract must inventory at least:

- setup keys;
- setup/profile values;
- public commands;
- public environments;
- class entrypoints;
- canonical names;
- compatibility aliases;
- upstream compatibility surfaces;
- deprecation state, if any.

A checker must prevent accidental removal of supported aliases and introduction of unreviewed public engineering identifiers outside this policy.

## 11. Behavioral equivalence

Naming work must not change document semantics or formatting merely because identifiers changed.

Evidence must cover as applicable:

- existing profile builds;
- PDF/A gates;
- reference document;
- structure, objects/bibliography and post-textual regressions;
- Overleaf import/stable behavior;
- deterministic distribution;
- Windows literal-font certification;
- absence of unintended normative-predicate changes.

For B2R-B, representative canonical-English and Portuguese-compatibility documents must additionally demonstrate equivalent semantics/output.

## 12. Article timing

Article runtime is deliberately delayed until B2R closes.

Therefore:

- do not create a temporary Portuguese `artigos.def` implementation;
- create the runtime directly as canonical `articles.def`;
- canonical public surface should be `type=article`;
- `tipo=artigo` becomes the Portuguese compatibility surface defined by B2R-B;
- article-specific behavior should use centralized profile capabilities or an equivalent policy, not scattered language-dependent conditionals.

The article normative contract already exists from B2A; only runtime/evidence remain future work.

## 13. Current migration state

### B2R-A1 — DONE

Internal package-module paths were normalized by PR #146 and the resulting main `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1` was re-certified.

### B2R-A2 — DONE

PR #148 replaced draft PR #147 over the same certified content SHA, was squash-merged, and produced `main` `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`. The resulting main passed Source Contract #410, LaTeX preflight #1076, Gate T #1077, Distribution #242 and PDF Validator #136. A2 changed repository/distribution paths only and preserved the frozen N12 workflow boundary.

### B2R-B — READY

Public English API + Portuguese compatibility aliases are the next executable naming phase. Work begins from certified `main` `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`, starting with the machine-readable API inventory and executable contract checker before or together with alias implementation.

## 14. Mandatory documentation synchronization

Naming decisions are easy to lose across long audit sessions, so documentation synchronization is closure-blocking.

After a material naming decision, CI-discovered blocker, blocker fix, PR merge/certification or change in the next executable step, update as applicable:

- `docs/HANDOFF-V2.2.0.md`;
- `docs/B2R-NAMING-INVENTORY.md`;
- `release/n15-b2r-a-naming-inventory.json`;
- this policy when the naming decision itself changes;
- README/normative human docs when user-visible paths or described implementation change.

A B2R subphase cannot be marked DONE while those documents disagree with live Git/PR/CI state.

## 15. Review checklist for a new identifier

Before adding an engineering-facing name, verify:

- Is it owned by this project rather than upstream?
- Is English appropriate for this surface?
- Is the meaning precise in an academic/LaTeX context?
- Does it follow the convention for its file/language/API type?
- Does it duplicate an existing concept?
- Does it need a Portuguese compatibility alias?
- Does it affect a public API contract or schema?
- Does it preserve official institutional/normative wording where that wording is data?
- Are handoff/ledger/documentation updates required by the change?

If any answer is unclear, treat the name as an API/design decision rather than a cosmetic rename.
