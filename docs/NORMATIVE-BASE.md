# Normative Base

Updated: 2026-08-30

This document is the human-readable normative baseline for the active `abntexto-ufc` v3 scope. Machine-readable evidence lives under `standards/`. This document does not create requirements by itself.

## Precedence

For technical requirements:

**current applicable ABNT standard → compatible/complementary current UFC requirement → current UFC guide → implementation**.

For institutional requirements:

**current UFC act → current UFC institutional requirement → current UFC guide → applicable technical standard → implementation**.

A superseded technical edition is not reactivated merely because an older UFC guide still cites it. A genuine conflict between current sources requires explicit review.

## Active technical basis

| Scope | Current reference |
| --- | --- |
| Academic works | ABNT NBR 14724:2024, corrected edition published 2025-04-01 |
| Citations | ABNT NBR 10520:2023 |
| References | ABNT NBR 6023:2025 |
| Research projects | ABNT NBR 15287:2025 |
| Scientific articles | ABNT NBR 6022:2018, with current cross-cutting citation/reference/summary standards |
| Abstracts/reviews | ABNT NBR 6028:2021 |
| Progressive section numbering | ABNT NBR 6024:2012 |
| Table of contents | ABNT NBR 6027:2012 |
| Index | ABNT NBR 6034:2004 |
| Spine | ABNT NBR 12225:2023 |
| Numerical tables | IBGE, Normas de Apresentação Tabular, 3rd ed., 1993 |
| Catalog card | UFC Joint Instruction No. 2/2026, where applicable |
| CAPES acknowledgment | CAPES Ordinance No. 206/2018, when applicable |

The project must distinguish mandatory requirements, recommendations, conditional requirements, manual checks, and technical certification policies. A green test does not by itself promote a requirement to fully proven normative status.

## Current runtime scope

The certified v3 foundation covers academic works and research projects. V3-A1 has now reintroduced a source-backed scientific-article normative contract without adding article runtime behavior. Article rules are manual/conditional during A1 and become implementation candidates only in V3-A2. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.

## Fonts and PDF/A

UFC guidance admits Times New Roman or Arial for the relevant academic profiles. Literal font identity is certified only by the Windows font gate; portable fallback families do not prove literal Times New Roman or Arial identity.

PDF/A-2b is the project's technical certification target. It satisfies the broader archival-format goal used by the project but must not be described as a UFC requirement for the specific PDF/A-2b conformance level unless UFC explicitly states that level.

## Institutional status

`abntexto-ufc` must not be described as official, approved, or homologated by UFC unless the University explicitly grants that status.

## Maintenance rule

Before a release candidate is certified, current editions and UFC institutional acts must be reconfirmed, affected machine-readable contracts must be reconciled, runtime/tests/documentation must converge, and no superseded source may silently govern an active rule.
