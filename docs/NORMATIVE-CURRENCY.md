# Normative Currency Policy

Updated: 2026-09-19

`abntexto-ufc` follows the most recent applicable technical edition that is currently in force. An older ABNT edition does not govern an active requirement merely because it is cited by an older UFC guide.

## Decision rule

For technical requirements:

**current applicable ABNT standard → compatible/complementary current UFC requirement → current UFC guide → implementation**.

For institutional requirements:

**current UFC act → current UFC institutional requirement → current UFC guide → applicable technical standard → implementation**.

Current-source conflicts are review items and must not be resolved silently.

## Explicit technical supersessions

The following older editions are contextual only for the current baseline:

- ABNT NBR 14724:2011 → ABNT NBR 14724:2024;
- ABNT NBR 6023:2018 → ABNT NBR 6023:2025;
- ABNT NBR 10520:2002 → ABNT NBR 10520:2023;
- ABNT NBR 12225:2004 → ABNT NBR 12225:2023;
- ABNT NBR 15287:2011 → ABNT NBR 15287:2025.

An older publication year does not imply obsolescence when no superseding edition exists. Currency is determined by normative status, not by year alone.

## UFC guides

UFC normalization guides are institutional sources interpreted under the precedence rule above. When a guide cites a superseded technical edition, compatible institutional guidance may remain useful, but the superseded edition does not become technically governing again.

## Scientific articles

The Scientific Article source-contract reconstruction reconfirmed the corrected UFC scientific-article guide (2022, corrected file dated 2023-04-27) and ABNT NBR 6022:2018 as the current article-presentation basis. The guide's embedded NBR 10520:2002 and NBR 6023:2018 references are superseded for their technical domains by NBR 10520:2023 and NBR 6023:2025.

The scientific-article runtime is active in the canonical `abntexto-ufc.cls` and is governed by the current 18-rule article contract in `standards/coverage-rules-article.json` plus the applicable cross-cutting current technical standards.

Runtime activation is distinct from proof-state promotion. The presence of scientific-article behavior in the canonical `abntexto-ufc.cls`, profile routing, or source implementation does not by itself prove article presentation predicates. Article-specific rendered evidence remains required before changing article rule proof state.

The currency checker binds scientific-article runtime presence to the canonical class and to the recorded activation/source authority. Source presence, normative authority and proof contribution remain separate concerns.

## Source updates

When a new technical edition or UFC act is identified:

1. review the source before changing runtime behavior;
2. identify every affected rule and locator;
3. update current machine-readable contracts under `standards/`;
4. remove superseded active authority from the current contract;
5. reconcile implementation, tests, validator behavior, and active documentation;
6. certify the exact candidate head only after the source transition is internally consistent.

Superseded source states remain available through Git/history when audit evidence is needed; they do not govern current rules.
