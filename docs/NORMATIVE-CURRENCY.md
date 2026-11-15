# Normative Currency Policy

Policy baseline: 2026-09-19. Scoped maintenance reconciliation: 2026-11-15 (documentation only; no new ABNT edition/corrigenda certification).

`abntexto-ufc` follows the most recent applicable technical edition that is currently in force. An older ABNT edition does not govern an active requirement merely because it is cited by an older UFC guide.

## 2026-10-19 cross-domain source-currency audit — evidence-limited

The [dated 21-source ABNT/UFC/IBGE/CAPES cross-domain inventory](NORMATIVE-CURRENCY-AUDIT-2026-10-19.md) now records, for **every active catalog source ID**, the repository's prior check date, a separately graded external corroboration tier, the still-unverified edition/corrigenda scope, and concrete next review actions.

**This is a triage record, not a technical-standard recertification.** In particular, official per-item ABNT publisher status and licensed corrigenda/primary clause texts were **not** verified. Do not replace the existing `checked_at` timestamps or promote `table.ibge`, document-profile proofs, or any other active normative rule merely because a university bibliography or distributor listed an edition. Already-recorded UFC Instruction 2/2026 must not be duplicated.

The active roadmap in [issue #489](https://github.com/tiagosombrra/abntexto-ufc/issues/489) still requires item-specific primary ABNT edition/corrigenda and UFC-guide checks, human review bound to the final PDFs, and forthcoming P0.11 site/validator and P0.12 cross-surface acceptance. Previously completed multilingual development evidence is not institutional or linguistic signoff.

**Long-table regression — bounded correction complete, not deferred:** [issue #501](https://github.com/tiagosombrra/abntexto-ufc/issues/501) was closed on 2026-10-24 after [PR #523](https://github.com/tiagosombrra/abntexto-ufc/pull/523) merged into `main=d65c4584269c46b02ebf90d829df9bf7c015d0e6`. The real seven-page default `longabnttblr` fixture with literal body `\\bottomrule` proved one terminal rule and **zero intermediate footer rules**; the uncorrected upstream-theme negative retained six premature rules. The postmerge [Static](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/40117996036), [Linux Integration](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/40117996031) (42/42), and [Linux Release Check](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/40117996022) (38/38) passed at that exact SHA. The default adapter applies only under its class-owned theme; explicit `theme=...` overrides preserve the original behavior and require manual pagination review. This **does not** demonstrate full IBGE compliance for arbitrary long tables, all themes, source semantics or other pagination cases. The 29 parent normative rules and `table.ibge` partial proof boundary remain unchanged.

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

The scientific-article runtime is active in the canonical `abntexto-ufc.cls` and is governed by the current 18-rule article contract in `standards/rules/coverage-rules-article.json` plus the applicable cross-cutting current technical standards.

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
