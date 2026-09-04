# Scientific Article Normative Contract — V3-A1

Updated: 2026-09-04

This document records the source-backed scientific-article contract reconstructed in V3-A1. It is a human-readable view of `standards/coverage-rules-article.json`; the machine-readable standards files remain authoritative for validation.

## Scope and entry

- A1 canonical entry: `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`.
- Certified non-article foundation: `c79f3c73f1d51a30175e8259269504d029442a1c`; unchanged by A1.
- A1 implementation base: `e40a56deeca8c22797398b0c95835964aefd2b15`.
- Runtime/profile implementation: **not allowed in A1**.
- Article rules introduced: **18** — 17 manual and 1 conditional-manual.
- A1 evidence owner: `article.source-review`; source classification only, never runtime proof.

## Reconfirmed authority set

The current UFC normalization page continues to expose the corrected 2022 scientific-article guide (file corrected in 2023). The article guide remains the institutional article-specific baseline, while current technical editions govern technical domains. The current article presentation standard remains ABNT NBR 6022:2018. Cross-cutting article requirements inherit the current citation, reference, section-numbering, abstract and tabular standards already present in the v3 source registry: NBR 10520:2023, NBR 6023:2025, NBR 6024:2012, NBR 6028:2021 and IBGE tabular guidance.

The corrected UFC article guide still embeds obsolete references to NBR 10520:2002 and NBR 6023:2018. Those editions are contextual only. They do not override the current NBR 10520:2023 and NBR 6023:2025 entries.

## Precedence

For article-specific technical requirements, the current applicable technical standard governs and compatible UFC article guidance supports it. For UFC institutional presentation details not defined as technical-standard requirements, the current UFC article guide governs. For citations and references, the current cross-cutting v3 contracts govern their domains rather than the stale editions embedded in the older article guide. For submission to a specific periodical, the journal's own instructions are an applicability boundary and must be checked before treating the generic UFC article profile as sufficient.

## Requirement versus recommendation

A1 preserves modality. `deve`/mandatory-element statements are represented as requirements. `convém`, `sugerimos` and optional-element statements are not promoted to mandatory rules. In particular, the 150–250-word summary interval, a minimum of three keywords, a single-paragraph summary and right-aligned authorship are conservative recommendations in A1.

## Rule contract

| Rule | Normativity | A1 validation | Locator |
|---|---|---|---|
| `article.title.primary.required` | required | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8 |
| `article.authorship.required` | required | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8 |
| `article.summary.primary.required` | required | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8 |
| `article.dates.submission-approval.required` | required | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11 |
| `article.introduction.required` | required | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.development.required` | required | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.final-considerations.required` | required | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.references.required` | required | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.title.foreign.optional` | optional | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8-9 |
| `article.summary.foreign.optional` | optional | manual | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11 |
| `article.title.primary.typography` | required | manual | Guia UFC de Artigos 2022, p. 9 |
| `article.authorship.metadata.footnote` | required | manual | Guia UFC de Artigos 2022, p. 9 |
| `article.authorship.alignment.recommended` | recommended | manual | Guia UFC de Artigos 2022, p. 9 |
| `article.body.typography` | required | manual | Guia UFC de Artigos 2022, p. 12 |
| `article.summary.word-count.recommended` | recommended | manual | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10-11 |
| `article.summary.keywords.minimum.recommended` | recommended | manual | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10-11 |
| `article.summary.single-paragraph.recommended` | recommended | manual | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10-11 |
| `article.journal-guidelines.precedence` | required-when-applicable | conditional-manual | Guia UFC de Artigos 2022, p. 6 |

## Locator/proof policy

Public UFC guide locators are verified directly. Where a rule also depends on proprietary ABNT clause text that was not directly available to this execution, `standards/locator-audit-article.json` records `PARTIAL_WITH_REASON`: the current edition is reconfirmed, but no clause wording or exact proprietary locator is invented. Every A1 article rule therefore remains `MANUAL` or `CONDITIONAL` in proof state. No article rule is `PROVEN`, and no existing green foundation gate is counted as article enforcement.

## V3-A2 bounded implementation contract

A2 implements only the canonical `scientific-article` profile and executable tests needed to realize the A1 rule set. The runtime lot introduces direct article ownership and reuses current citation/reference/section/summary/table machinery rather than forking it. Recommendation/optional semantics remain distinct from requirements, journal-specific instructions remain a conditional boundary, and every article proof promotion still requires current positive/negative article-specific evidence. Any source conflict discovered in A2 returns to source review instead of being resolved by runtime guesswork.


## V3-A1 validation closeout

PR #279 merged this source-backed contract at `4d018a92697e8f39e3a53b034c451e55996c84fb` after source-only run `33894907220`, Static `33895016834`, and Linux integration `33895016774` / job `101095498647` all passed; Linux closed `PASS=31 FAIL=0 SKIP=0`. No article runtime/profile code was introduced and no article proof state was promoted. V3-A2 implementation is bounded by issue #280, but remains blocked until the A1 closeout checkpoint is merged and its immutable entry predecessor is recorded.


## V3-A2 canonical entry

V3-A1/#275 closed through PR #281 at exact predecessor `7a7562d23e8bf6c92abb635718639d617a2ed6ff`. V3-A2/#280 is ACTIVE from that SHA and owns only the bounded `scientific-article` runtime/test implementation described above. The source-contract product remains `4d018a92697e8f39e3a53b034c451e55996c84fb` and the certified non-article foundation remains `c79f3c73f1d51a30175e8259269504d029442a1c`. No article runtime implementation had started at the activation checkpoint; the first A2 runtime lot now implements the canonical profile without promoting article proof state.
