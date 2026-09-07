# Scientific Article Normative Contract

Updated: 2026-09-07
Status: SOURCE CONTRACT ACCEPTED — STEP 6 EVIDENCE MAP ACCEPTED / STEP 7 PRESENTATION ACTIVE

Historical labels `V3-A1` / `V3-A2` are retained only when identifying earlier source-contract evidence. Active execution uses the readable phase name **Scientific Article**.

This document is the human-readable view of `standards/coverage-rules-article.json`; the machine-readable standards files remain authoritative for validation.

## Current state

The article source contract was reconstructed before the deep shared-foundation regression and remains valid as retained authority evidence. Runtime implementation started only after the shared foundation and its canonical academic-work reference PDF were accepted.

Current facts:

- Core Corrections candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`;
- Reference PDF Validation candidate `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790`, Linux `33985595798`, 55/55 visual PASS;
- source-contract product `4d018a92697e8f39e3a53b034c451e55996c84fb`;
- canonical `main` `fbf7cc4839ce318024a7d1ed517dd50fab5773ac`;
- active article branch reconciled with current main by `85cf22b6fe5d117bb2611a2865911e0d20a19363`;
- Scientific Article Steps 1–6 accepted;
- Step 6 evidence-map acceptance: `e941a7f9b4685a9bcf687135e8d5168af2d69ec7`, Static `34146793998`, Linux `34146794016`;
- Step 7 canonical article PDF presentation validation active.

Step 6 did not rewrite requirement text, normativity, locators or applicability and promoted zero validation modes. Runtime/executable support remains distinct from normative proof.

## Reconfirmed authority set and precedence

The current UFC normalization surface exposes the corrected 2022 scientific-article guide (file corrected in 2023). The article guide remains the institutional article-specific baseline, while current technical editions govern their technical domains. The article presentation standard tracked by the project is ABNT NBR 6022:2018. Cross-cutting article requirements inherit current citation, reference, section-numbering, abstract and tabular standards already present in the v3 registry: NBR 10520:2023, NBR 6023:2025, NBR 6024:2012, NBR 6028:2021 and IBGE tabular guidance.

The UFC article guide still embeds obsolete references to NBR 10520:2002 and NBR 6023:2018. Those editions are contextual only and do not override current contracts.

For submission to a specific periodical, the journal's own instructions are an applicability boundary and must be checked before treating the generic UFC article profile as sufficient.

## Requirement versus recommendation

Modality is preserved. `deve`/mandatory-element statements are requirements. `convém`, `sugerimos` and optional-element statements are not promoted to mandatory rules. The 150–250-word summary interval, minimum three keywords, single-paragraph summary and right-aligned authorship remain recommendations.

## Rule contract

| Rule | Normativity | Evidence boundary | Locator |
|---|---|---|---|
| `article.title.primary.required` | required | direct front-block executable support | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8 |
| `article.authorship.required` | required | direct front-block executable support | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8 |
| `article.summary.primary.required` | required | direct front-block executable support | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8 |
| `article.dates.submission-approval.required` | required | direct front-block executable support | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11 |
| `article.introduction.required` | required | direct article-body executable support | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.development.required` | required | direct article-body support + controlled negative path | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.final-considerations.required` | required | direct article-body executable support | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.references.required` | required | direct article-body executable support | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 12 |
| `article.title.foreign.optional` | optional | present/absent article scenarios; optionality preserved | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8–9 |
| `article.summary.foreign.optional` | optional | present/absent article scenarios; optionality preserved | ABNT NBR 6022:2018; Guia UFC de Artigos 2022, p. 8, 11 |
| `article.title.primary.typography` | required | direct final-PDF front-block measurement | Guia UFC de Artigos 2022, p. 9 |
| `article.authorship.metadata.footnote` | required | footnote-route + rendered evidence | Guia UFC de Artigos 2022, p. 9 |
| `article.authorship.alignment.recommended` | recommended | advisory support only; non-enforcing | Guia UFC de Artigos 2022, p. 9 |
| `article.body.typography` | required | direct two-engine final-PDF body measurement | Guia UFC de Artigos 2022, p. 12 |
| `article.summary.word-count.recommended` | recommended | advisory support only | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10–11 |
| `article.summary.keywords.minimum.recommended` | recommended | advisory support only | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10–11 |
| `article.summary.single-paragraph.recommended` | recommended | advisory support only | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10–11 |
| `article.journal-guidelines.precedence` | required-when-applicable | target-journal-bound `conditional-manual` | Guia UFC de Artigos 2022, p. 6 |

## Frozen presentation values

`article.title.primary.typography`: centered, uppercase, bold, 12 pt, single spacing.

`article.body.typography`: 12 pt, justified, first-line indent 2 cm, single spacing.

`article.authorship.metadata.footnote` requires complementary author identification in a footnote, including affiliation/biographical information and support for contact information. The contract does not freeze unsupported physical geometry.

## Step 7 presentation observation boundary

The provenance-bound canonical article PDF currently shows primary sections beginning on new pages. The retained 18-rule contract requires the presence of Introduction, Development and Final Considerations and defines body typography, but it contains **no rule requiring continuous primary-section flow or forbidding page starts**.

Therefore this is a factual presentation observation only. It is not a runtime defect or new normative predicate under current authority. New authority would be required before changing section page-start semantics specifically for the article profile.

## Proof and implementation policy

`standards/proof-policy.json` remains conservative: executable validation does not automatically imply `PROVEN`. Shared green mechanisms, profile registration, runtime presence or source-only implementation alone are not article proof.

The active phase must keep one canonical `scientific-article` profile, reuse cross-cutting infrastructure, preserve required/optional/recommended/conditional semantics, preserve journal instructions as a conditional boundary, produce a provenance-bound canonical article PDF with complete visual inspection, and finish with a **phase-end regression** on one immutable candidate using **complete Linux scope**.

Every **material advance** that changes authority, modality, evidence ownership, validation mode, proof disposition or a factual runtime observation represented here must synchronize this contract in the same work cycle. Ordinary runtime progress remains in `docs/V3-SCIENTIFIC-ARTICLE.md`, handoff, roadmap and machine state.
