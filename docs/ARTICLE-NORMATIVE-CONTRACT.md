# Scientific Article Normative Contract

Updated: 2026-09-05
Status: SOURCE CONTRACT ACCEPTED — RUNTIME IMPLEMENTATION ACTIVE

Historical labels `V3-A1` / `V3-A2` are retained below only when identifying earlier source-contract evidence. Active execution uses the readable phase name **Scientific Article**.

This document is the human-readable view of `standards/coverage-rules-article.json`; the machine-readable standards files remain authoritative for validation.

## Current entry after shared-foundation regression

The article source contract was reconstructed before the deep shared-foundation regression and remains valid as retained authority evidence. Runtime implementation was deliberately deferred until the shared foundation was corrected and its canonical reference PDF accepted.

Current entry prerequisites are now satisfied:

- Core Corrections candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`;
- Reference PDF Validation candidate `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790`, Linux `33985595798`;
- canonical academic-work PDF: 55/55 visual PASS, 0 unexplained visual failures;
- article source-contract product: `4d018a92697e8f39e3a53b034c451e55996c84fb`;
- historical pre-runtime checkpoint: `7a7562d23e8bf6c92abb635718639d617a2ed6ff`;
- certified non-article foundation evidence: `c79f3c73f1d51a30175e8259269504d029442a1c` plus the later regression/correction acceptance above.

Current runtime inspection confirms that `abntexto-ufc/core.def` does not yet expose a `scientific-article` type. No article proof state may be inferred merely from shared non-article gates.

## Reconfirmed authority set

The current UFC normalization page exposes the corrected 2022 scientific-article guide (file corrected in 2023). The article guide remains the institutional article-specific baseline, while current technical editions govern their technical domains. The article presentation standard tracked by the project is ABNT NBR 6022:2018. Cross-cutting article requirements inherit the current citation, reference, section-numbering, abstract and tabular standards already present in the v3 registry: NBR 10520:2023, NBR 6023:2025, NBR 6024:2012, NBR 6028:2021 and IBGE tabular guidance.

The UFC article guide still embeds obsolete references to NBR 10520:2002 and NBR 6023:2018. Those editions are contextual only. They do not override the current NBR 10520:2023 and NBR 6023:2025 contracts.

## Precedence

For article-specific technical requirements, the current applicable technical standard governs and compatible UFC article guidance supports it. For UFC institutional presentation details not defined as technical-standard requirements, the current UFC article guide governs. For citations and references, the current cross-cutting v3 contracts govern their domains rather than stale editions embedded in the older article guide.

For submission to a specific periodical, the journal's own instructions are an applicability boundary and must be checked before treating the generic UFC article profile as sufficient.

## Requirement versus recommendation

Modality is preserved. `deve`/mandatory-element statements are represented as requirements. `convém`, `sugerimos` and optional-element statements are not promoted to mandatory rules.

In particular, the 150-250-word summary interval, a minimum of three keywords, a single-paragraph summary and right-aligned authorship remain recommendations rather than hard runtime requirements.

## Rule contract

| Rule | Normativity | Current validation | Locator |
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

## Required presentation values already frozen by the contract

`article.title.primary.typography`:

- alignment: center;
- case: uppercase;
- weight: bold;
- font size: 12 pt;
- line spacing: single.

`article.body.typography`:

- font size: 12 pt;
- alignment: justified;
- first-line indent: 2 cm;
- line spacing: single.

`article.authorship.metadata.footnote` requires complementary author identification in a footnote, including affiliation/biographical information and support for contact information.

## Locator and proof policy

Public UFC guide locators are verified directly. Where a rule also depends on proprietary ABNT clause text that is not directly available to the current evidence corpus, `standards/locator-audit-article.json` records the bounded reason rather than inventing clause wording or a locator.

At Scientific Article entry, all article rules remain `manual` or `conditional-manual`. Proof may advance only from new article-specific executable evidence. Mechanism reuse, shared green tests or profile registration alone are not proof.

## Scientific Article implementation contract

The active phase may implement only the canonical `scientific-article` profile and executable evidence required to realize this contract. It must:

- reuse cross-cutting citation/reference/section/table/summary infrastructure;
- preserve the validated non-article foundation;
- keep required/optional/recommended/conditional semantics distinct;
- add positive article-specific evidence before proof promotion;
- add controlled negative paths where safe;
- preserve journal instructions as a conditional boundary;
- return any source conflict to authority review rather than runtime guesswork;
- produce a provenance-bound canonical article PDF and complete visual inspection before phase closeout;
- finish with a **phase-end regression** on one immutable candidate.

The execution plan is `docs/V3-SCIENTIFIC-ARTICLE.md`.

## Historical provenance

The original source-contract work was merged at `4d018a92697e8f39e3a53b034c451e55996c84fb` and later closed at `7a7562d23e8bf6c92abb635718639d617a2ed6ff`. Those historical labels and SHAs establish provenance only. They do not override the post-regression readable roadmap or authorize blind restoration of earlier article implementation attempts.

Every **material advance** in the active Scientific Article phase must synchronize this contract only when authority, modality, evidence ownership or proof state actually changes; ordinary runtime progress belongs in `docs/V3-SCIENTIFIC-ARTICLE.md`, handoff, roadmap and machine state.
