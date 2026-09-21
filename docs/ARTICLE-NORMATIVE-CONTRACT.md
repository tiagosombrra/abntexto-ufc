# Scientific Article Normative Contract

Updated: 2026-09-19

This document is the human-readable view of the current scientific-article contract. Machine-readable standards files under `standards/` remain authoritative for validation.

## Current state

The scientific-article profile is an active supported runtime profile in the canonical `abntexto-ufc.cls`.

Its rule contract contains 18 article-specific rules. Runtime implementation, executable support and normative proof remain distinct concepts: source presence or a successful compilation does not automatically promote a rule to fully proven normative status.

The current implementation is validated through dedicated profile, front-block, foreign-element, body, recommendation and final-PDF evidence.

## Authority set and precedence

The current UFC normalization surface includes the corrected 2022 scientific-article guide (file corrected in 2023). The article guide is the institutional article-specific baseline, while current technical editions govern their technical domains.

The article presentation standard tracked by the project is ABNT NBR 6022:2018.

Cross-cutting article requirements use the current citation/reference/summary and related technical standards already present in the project registry, including:

- ABNT NBR 10520:2023;
- ABNT NBR 6023:2025;
- ABNT NBR 6024:2012;
- ABNT NBR 6028:2021;
- applicable IBGE tabular guidance.

When the UFC article guide cites superseded technical editions, those citations are contextual only and do not override the current technical contract.

For submission to a specific periodical, that periodical's instructions remain an applicability boundary and must be checked independently.

## Requirement versus recommendation

Modality is preserved.

Mandatory statements are treated as requirements. Recommendations and optional elements are not promoted to mandatory rules merely because the runtime supports them.

The following remain recommendations:

- 150–250-word summary interval;
- minimum three keywords;
- single-paragraph summary;
- right-aligned authorship.

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
| `article.authorship.metadata.footnote` | required | footnote route + rendered evidence | Guia UFC de Artigos 2022, p. 9 |
| `article.authorship.alignment.recommended` | recommended | advisory support only; non-enforcing | Guia UFC de Artigos 2022, p. 9 |
| `article.body.typography` | required | direct two-engine final-PDF body measurement | Guia UFC de Artigos 2022, p. 12 |
| `article.summary.word-count.recommended` | recommended | advisory support only | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10–11 |
| `article.summary.keywords.minimum.recommended` | recommended | advisory support only | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10–11 |
| `article.summary.single-paragraph.recommended` | recommended | advisory support only | ABNT NBR 6028:2021; Guia UFC de Artigos 2022, p. 10–11 |
| `article.journal-guidelines.precedence` | required-when-applicable | target-journal-bound conditional manual review | Guia UFC de Artigos 2022, p. 6 |

## Presentation values currently implemented

Primary article title:

- centered;
- uppercase;
- bold;
- 12 pt;
- single spacing.

Article body:

- 12 pt;
- justified;
- 2 cm first-line indent;
- single spacing.

Complementary author identification is routed through a footnote. The contract requires the information route but does not freeze unsupported physical geometry.

## Presentation observation boundary

The article rule contract requires the presence of Introduction, Development and Final Considerations and defines body typography.

It does not establish a separate article-specific rule requiring continuous primary-section flow or forbidding a section from beginning on a new page.

Therefore a page-start observation is not promoted into a new defect or normative predicate without current authority supporting that requirement.

## Proof and implementation policy

`standards/evidence/proof-policy.json` remains conservative: executable validation does not automatically imply `PROVEN`.

Shared green mechanisms, profile registration, runtime presence or source-only implementation are insufficient by themselves. Evidence must match the owning rule and the declared proof/contribution policy.

The current scientific-article implementation must:

- keep one canonical `scientific-article` profile;
- reuse cross-cutting project infrastructure;
- preserve required/optional/recommended/conditional semantics;
- preserve journal-specific instructions as a conditional applicability boundary;
- remain covered by dedicated runtime and rendered-PDF evidence;
- keep normative source, implementation and proof-state changes synchronized.

Any material change to authority, modality, evidence ownership, validation mode or proof disposition must update the machine-readable contract and this human-readable view in the same work cycle.
