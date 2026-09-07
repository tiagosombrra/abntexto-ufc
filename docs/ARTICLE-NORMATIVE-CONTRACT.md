# Scientific Article Normative Contract

Updated: 2026-09-07
Status: SOURCE CONTRACT ACCEPTED — RUNTIME IMPLEMENTATION ACTIVE / STEP 6 EVIDENCE HARDENING

Historical labels `V3-A1` / `V3-A2` are retained only when identifying earlier source-contract evidence. Active execution uses the readable phase name **Scientific Article**.

This document is the human-readable view of `standards/coverage-rules-article.json`; the machine-readable standards files remain authoritative for validation.

## Current entry after shared-foundation regression

The article source contract was reconstructed before the deep shared-foundation regression and remains valid as retained authority evidence. Runtime implementation was deliberately deferred until the shared foundation was corrected and its canonical reference PDF accepted.

Current prerequisites and integration facts:

- Core Corrections candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`;
- Reference PDF Validation candidate `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790`, Linux `33985595798`, canonical academic-work PDF 55/55 visual PASS;
- article source-contract product `4d018a92697e8f39e3a53b034c451e55996c84fb`;
- shared foundation integrated at `e6833ed5cf07aaf1021c690260cecfacec1a119a`;
- canonical `main` currently `789c6f3f4669ae36c3d4fe831ae939a340592568`;
- active article branch reconciled with current `main` by merge `ae7e2cf2484e0b4329cc30ea80a95d0788e0e9f4`;
- Scientific Article Steps 1–5 accepted; Step 6 evidence hardening active.

Runtime presence is **not** proof of an article rule by itself. Step 6 may change validation/evidence ownership only when direct article-specific executable evidence supports the claim. Source-backed requirement text, modality, locators and applicability remain stable without new authority.

## Reconfirmed authority set

The current UFC normalization page exposes the corrected 2022 scientific-article guide (file corrected in 2023). The article guide remains the institutional article-specific baseline, while current technical editions govern their technical domains. The article presentation standard tracked by the project is ABNT NBR 6022:2018. Cross-cutting article requirements inherit current citation, reference, section-numbering, abstract and tabular standards already present in the v3 registry: NBR 10520:2023, NBR 6023:2025, NBR 6024:2012, NBR 6028:2021 and IBGE tabular guidance.

The UFC article guide still embeds obsolete references to NBR 10520:2002 and NBR 6023:2018. Those editions are contextual only and do not override the current contracts.

## Precedence

For article-specific technical requirements, the current applicable technical standard governs and compatible UFC article guidance supports it. For UFC institutional presentation details not defined as technical-standard requirements, the current UFC article guide governs. For citations and references, current cross-cutting v3 contracts govern rather than stale editions embedded in the older article guide.

For submission to a specific periodical, the journal's own instructions are an applicability boundary and must be checked before treating the generic UFC article profile as sufficient.

## Requirement versus recommendation

Modality is preserved. `deve`/mandatory-element statements are requirements. `convém`, `sugerimos` and optional-element statements are not promoted to mandatory rules.

In particular, the 150–250-word summary interval, a minimum of three keywords, a single-paragraph summary and right-aligned authorship remain recommendations rather than hard runtime requirements.

## Rule contract

| Rule | Normativity | Step 6 evidence boundary | Locator |
|---|---|---|---|
| `article.title.primary.required` | required | direct front-block executable evidence exists | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8 |
| `article.authorship.required` | required | direct front-block executable evidence exists | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8 |
| `article.summary.primary.required` | required | direct front-block executable evidence exists | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8 |
| `article.dates.submission-approval.required` | required | direct front-block executable evidence exists | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11 |
| `article.introduction.required` | required | direct article-body executable evidence exists | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.development.required` | required | direct article-body evidence + controlled negative path exists | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.final-considerations.required` | required | direct article-body executable evidence exists | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.references.required` | required | direct article-body executable evidence exists | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.title.foreign.optional` | optional | direct present/absent article scenarios exist; optionality must remain | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8–9 |
| `article.summary.foreign.optional` | optional | direct present/absent article scenarios exist; optionality must remain | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11 |
| `article.title.primary.typography` | required | direct final-PDF front-block measurement exists | Guia UFC de Artigos 2022, p. 9 |
| `article.authorship.metadata.footnote` | required | direct footnote-route + rendered 10 pt evidence exists | Guia UFC de Artigos 2022, p. 9 |
| `article.authorship.alignment.recommended` | recommended | advisory support only; non-enforcing | Guia UFC de Artigos 2022, p. 9 |
| `article.body.typography` | required | direct two-engine final-PDF body measurement exists | Guia UFC de Artigos 2022, p. 12 |
| `article.summary.word-count.recommended` | recommended | advisory support only; outside-recommendation case accepted | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10–11 |
| `article.summary.keywords.minimum.recommended` | recommended | advisory support only; fewer-than-three case accepted | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10–11 |
| `article.summary.single-paragraph.recommended` | recommended | advisory support only; multi-paragraph case accepted | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10–11 |
| `article.journal-guidelines.precedence` | required-when-applicable | remains target-journal-bound `conditional-manual` | Guia UFC de Artigos 2022, p. 6 |

The machine validation modes remain governed by `standards/coverage-rules-article.json`. Step 6 updates those modes only when the synchronized evidence map and checker make the ownership truthful; this human view must then be updated atomically.

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

`article.authorship.metadata.footnote` requires complementary author identification in a footnote, including affiliation/biographical information and support for contact information. The contract does not freeze a physical-page percentage for the note position; evidence must prove footnote semantics without inventing unsupported geometry.

## Locator and proof policy

Public UFC guide locators are verified directly. Where a rule also depends on proprietary ABNT clause text that is not directly available to the evidence corpus, `standards/locator-audit-article.json` records the bounded reason rather than inventing clause wording or a locator.

`standards/proof-policy.json` remains conservative: a rule moving to executable validation does not automatically become `PROVEN`. Full proof requires the policy's stronger combination of scenario, positive assertion, final-output measurement when applicable and meaningful negative evidence or documented technical exception.

Shared green mechanisms, profile registration, runtime presence, or source-only implementation alone are not article proof.

## Scientific Article implementation contract

The active phase must:

- keep one canonical `scientific-article` profile;
- reuse cross-cutting citation/reference/section/table/summary infrastructure;
- preserve the validated non-article foundation;
- keep required/optional/recommended/conditional semantics distinct;
- add article-specific positive evidence before executable proof ownership;
- add controlled negative paths where safe;
- preserve journal instructions as a conditional boundary;
- return any source conflict to authority review rather than runtime guesswork;
- produce a provenance-bound canonical article PDF and complete visual inspection before phase closeout;
- finish with a **phase-end regression** on one immutable candidate using **complete Linux scope**.

The execution plan is `docs/V3-SCIENTIFIC-ARTICLE.md`.

## Historical provenance

The original source-contract work was merged at `4d018a92697e8f39e3a53b034c451e55996c84fb` and later closed at `7a7562d23e8bf6c92abb635718639d617a2ed6ff`. Those historical labels and SHAs establish provenance only. They do not override the post-regression readable roadmap or authorize blind restoration of earlier implementation attempts.

Every **material advance** that changes authority, modality, evidence ownership, validation mode, proof disposition or a factual runtime observation represented here must synchronize this contract in the same work cycle. Ordinary runtime progress remains in `docs/V3-SCIENTIFIC-ARTICLE.md`, handoff, roadmap and machine state.
