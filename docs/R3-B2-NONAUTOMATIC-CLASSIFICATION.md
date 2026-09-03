# R3-B2 Non-Automatic Rule Classification

Updated: 2026-09-03

R3-B2 reviewed every full-contract rule whose validation mode is not automatic. The authoritative machine-readable classification is `standards/evidence-contribution-policy.json`; this document provides the review rationale in compact form.

| Rule | Validation mode | Evidence class | Rationale |
|---|---|---|---|
| `deposit.approval-signatures` | manual | manual-review | Deposit-time inspection is required for signature images or handwritten/digital signatures. |
| `deposit.capes` | conditional-manual | conditional-review | Applies only to CAPES-funded work and retains an institutional applicability boundary. |
| `font.size.reduced.catalog-card` | manual | manual-review | Internal typography belongs to an externally supplied catalog-card PDF. |
| `format.text.color` | manual | manual-review | Fixture observations support the rule, but complete-document color compliance remains conservatively manual. |
| `spine.conditional` | not-applicable | not-applicable | Printed-spine requirements are outside the standard electronic package. |
| `deposit.metadata.workflow` | manual | manual-review | DSpace metadata belongs to the institutional repository workflow, not PDF rendering. |
| `accessibility.pdfua.profile` | manual | manual-review | PDF/UA is an additional technical profile and is not claimed as a general UFC deposit requirement. |
| `distribution.overleaf-ctan.policy` | manual | manual-review | Distribution readiness is project policy and requires release/distribution review. |
| `glossary.element.optional` | conditional | conditional-review | The glossary is optional and evidence depends on the present/absent route. |
| `volume.number.cover-title-page` | conditional | conditional-review | Applies only to multi-volume documents. |
| `errata.element.optional` | conditional | conditional-review | The errata element is optional and is evaluated through present/absent routes. |
| `errata.position` | conditional | conditional-review | Position is relevant only when errata is present. |
| `errata.contents` | conditional | conditional-review | Contents are relevant only when errata is present. |
| `list.illustrations.optional` | conditional | conditional-review | The list is optional and depends on the corresponding content route. |
| `list.tables.optional` | conditional | conditional-review | The list is optional and depends on the corresponding content route. |
| `list.abbreviations.optional` | conditional | conditional-review | The list is optional and evaluated through present/absent routes. |
| `list.symbols.optional` | conditional | conditional-review | The list is optional and evaluated through present/absent routes. |

No rule in this set was reclassified as automatic merely because a related gate is green. The proof-state baseline remains conservative: six `MANUAL`, ten `CONDITIONAL`, one `NOT_APPLICABLE`, 113 `PARTIAL`, and 51 `NOT_PROVEN` rules.

R3-B2 closed through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` with this 17-rule classification unchanged and with no non-automatic rule promoted merely from a green related gate.
