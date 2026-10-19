# Source currency and corrigenda gap matrix — 2026-10-19

**Development branch:** v3.1.0 UNRELEASED. **Snapshot source:** `standards/catalog/catalog.json` at certified `main=5908e9c00d059a8f645bf36b411eb1a7d444af46`. **Scope:** all 21 active runtime catalog sources; source-audit registry separately holds 27 source records (including sources outside the runtime subset). **This document is a discovery/triage log, not a new normative authority or compliance certificate.**

## What was and was not checked

On 2026-10-19, public institutional pages and bibliographic listings were sampled to check the *claimed editions*, source locations and precedence. The official [UFC normalisation page](https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/) lists five guide families, refers numeric tables to IBGE, and explains its use under UFC resolution 17/2017. The [UFC deposit information hub](https://biblioteca.ufc.br/pt/servicos-e-produtos/recebimento-e-divulgacao-de-dissertacoes-teses-e-tccs/) describes the 2026 joint instruction regarding *visible* catalog cards; that instruction is **already registered** in the runtime catalog as `ufc-in-2-2026`. Avoid duplicating that rule.

Independent corroboration of editions includes the [UFES library normalisation page](https://biblioteca.ufes.br/manuais-de-normalizacao) (NBR 14724:2024, 10520:2023, 6023:2025 and 6028:2021), the [PUCRS library note about NBR 15287](https://biblioteca.pucrs.br/noticias/atualizacao-da-norma-de-projeto-de-pesquisa-da-abnt-nbr-15287/) (2025 revision), the [DIN Media 6022:2018 record](https://www.dinmedia.de/en/standard/abnt-nbr-6022/291015508) and [DIN Media 6034:2004 record](https://www.dinmedia.de/en/standard/abnt-nbr-6034/180777148) (both list CURRENT), and [Einstein library's NBR 6027:2012 citation](https://biblioteca.einstein.br/pt-br/sumario). These are **corroborating references**, not per-item authoritative ABNT edition/errata receipts.

The [ABNT official catalogue search](https://www.abntcatalogo.com.br/pav.aspx) was accessible only as a search form; no item-specific ABNT status, errata/revision ledger, or licensed full-text comparison was acquired. **Corrigenda: NOT VERIFIED for all ten ABNT technical sources.** A search that finds no errata does **not** prove there are none. The five UFC guide PDFs and institutional act were not individually revalidated clause by clause in this slice. The dated `checked_at` fields in the actual source registries remain unchanged.

**Evidence key:** `I` = official institutional landing-page / index corroboration, not document revision/corrigenda signoff; `S` = secondary library corroboration only; `D` = standards distributor listing, not ABNT-publisher signoff; `U` = only current repository registration corroborated, fresh external primary check outstanding.

## Complete current-catalog source inventory (21 records)

| Source ID | Recorded status / last checked | Evidence now | Remaining priority |
|---|---|---|---|
| `ufc-normalizacao-2026` | `current` / 2026-09-04 | **I** — Official UFC library landing page lists five normalization guides and points to IBGE for numeric tables; page-level listing only. | Check guide files and institutional amendment dates. |
| `ufc-guia-trabalhos-2022` | `current-with-superseded-norm-references` / 2026-08-22 | **I** — Linked as a guide from the official UFC library page; internal older ABNT citations require precedence handling. | Review the latest linked PDF revision and the clauses for seven profiles. |
| `ufc-guia-artigos-2022` | `current-with-superseded-norm-references` / 2026-09-04 | **I** — Linked as an article guide by UFC; project records corrected 2023 PDF, not independently reconfirmed here. | Recheck corrected-file version and article-profile source predicates. |
| `ufc-guia-citacoes-2025` | `current-with-superseded-norm-references` / 2026-08-22 | **I** — Listed as a citations guide; earlier 6023:2018 cross-reference must not supersede 6023:2025. | Verify guide revision/errata, citations and reference interplay. |
| `ufc-guia-referencias-2023` | `current-with-superseded-norm-references` / 2026-08-22 | **I** — Linked as a UFC references guide; predates recorded NBR 6023:2025. | Identify institutional-only detail and stale technical examples. |
| `ufc-guia-projetos-2019` | `current-with-superseded-norm-references` / 2026-08-22 | **I** — Listed as the research-project guide; predates recorded NBR 15287:2025. | Reconcile profile-specific mandatory/optional clauses against 15287:2025. |
| `ufc-in-2-2026` | `current` / 2026-08-22 | **I** — Official UFC deposit page identifies joint Normative Instruction 2/2026 and visual catalog-card dispensation; already catalogued. | Check current applicability to TCC/dissertations/theses and any later revocation. |
| `ufc-deposito-tcc-2026` | `current` / 2026-08-22 | **I** — Official UFC deposit hub links TCC receiving guidance; individual page terms not reaudited. | Recheck receipt, metadata, one-file and institutional process rules. |
| `ufc-deposito-pos-2026` | `current` / 2026-08-22 | **I** — Official UFC deposit hub links theses/dissertations guidance; individual page terms not reaudited. | Recheck institutional deposit metadata and programme exceptions. |
| `abnt-nbr-14724-2024` | `current` / 2026-08-22 | **S** — UFES library normalisation page independently cites 14724:2024; current ABNT per-item status/errata not accessible here. | Confirm official ABNT current-status, errata and applicable 2024 clauses. |
| `abnt-nbr-10520-2023` | `current` / 2026-09-04 | **S** — UFES library independently cites 10520:2023; full ABNT primary publication/errata not reviewed. | Confirm official per-item status and citation-clause corrections. |
| `abnt-nbr-6023-2025` | `current` / 2026-09-04 | **S** — UFES and UNICAMP library guidance independently cites 6023:2025; no claim of full text/errata check. | Confirm official current status, amendments, corrected versions and examples. |
| `abnt-nbr-15287-2025` | `current` / 2026-08-22 | **S** — PUCRS library documents the 2025 project-standard revision; full ABNT status/errata not independently checked. | Confirm official edition and reconcile project profiles, appendices, annexes. |
| `abnt-nbr-6022-2018` | `current` / 2026-09-04 | **D** — Independent DIN Media catalog currently marks 6022:2018 CURRENT; ABNT publisher still authoritative. | Confirm ABNT status/corrigenda and article/journal applicability. |
| `abnt-nbr-6028-2021` | `current` / 2026-09-04 | **S** — UFES library notes NBR 6028 update in 2021, not full primary ABNT status. | Confirm per-item ABNT current status/errata and abstract predicates. |
| `abnt-nbr-6024-2012` | `current` / 2026-09-04 | **U** — Recorded in project registry; no fresh primary-authority per-item verification. | Check ABNT edition, amendments, section-numbering effects. |
| `abnt-nbr-6027-2012` | `current` / 2026-08-22 | **S** — Independent Einstein library cites 6027:2012 for contents, not an ABNT status/errata assertion. | Confirm ABNT current status and TOC edge cases. |
| `abnt-nbr-6034-2004` | `current` / 2026-08-22 | **D** — Independent DIN Media catalog marks 6034:2004 CURRENT; no ABNT publisher status/errata check. | Confirm ABNT status and index-profile applicability. |
| `abnt-nbr-12225-2023` | `current` / 2026-08-22 | **U** — Recorded in project registry; no fresh per-item primary status/errata verification. | Confirm ABNT status and spine constraints where physically relevant. |
| `ibge-tabular-1993` | `current-for-tabular-presentation` / 2026-09-04 | **I** — UFC library page delegates numeric-table presentation to IBGE; it does not establish clause-wide conformance. | Keep §8.3 legacy long-table risk tracked; do not expand this closed workstream now. |
| `capes-portaria-206-2018` | `current` / 2026-08-22 | **U** — Listed in project catalog; government regulation and any replacement were not independently rechecked. | Confirm official CAPES act current status and funding acknowledgement applicability. |

## Severity, dependencies and the next bounded steps

1. **P0: technical-edition/corrigenda verification** for the ten ABNT technical sources via item-specific ABNT catalogue receipts and lawful primary-text access. Prioritise NBR 14724:2024, 6023:2025, 10520:2023 and 15287:2025 because they apply to many document profiles. Do not substitute secondary university guides for publisher authority or overwrite `checked_at` with this exploratory audit date.
2. **P0: UFC institutional precedence** — re-evaluate all five current-guide files and check for corrections after the 2026 deposit instruction, especially older embedded NBR 6023:2018, 10520:2002, 14724:2011 and 15287:2011 references. Separate technical supersession from still-compatible institutional requirements. Existing `ufc-in-2-2026` means no duplicate catalog rule is warranted.
3. **P1: profile mapping** — link each confirmed source edition/section/erratum to the seven public document-type evidence sets; distinguish `required`, `optional`, `recommended`, `not applicable` and `manual review`. Obtain human visual acceptance of real PDF pairs before any claims stronger than existing `automatic-partial`.
4. **P1: no-table macro progression** — next separate engineering slices after this *source audit* should cover seven-profile PDF review, then backward-compatible PT-default / EN–ES–FR labels and commands, site/validator usability, and PDF/UA dependencies (#459). The original `longabnttblr` §8.3(d) risk remains recorded in #501, **not a reason to begin another incremental table PR now**.
5. **P2: promotion gate** — only after verified primary edition/corrigendum, explicit clause locator, impacted predicate inventory and an exact-SHA CI + PDF regression may machine catalog statuses, rule proofs, implementation or validator outcomes change.

## Source-change and publication invariants

- Authority remains `standards/catalog/catalog.json`, `standards/catalog/version-policy.json` and the catalog's source precedence rules. This *audit record* adds no rule and changes no machine-source status or proof contribution.
- Preserve 29 catalog parent normative rules, seven public document profiles, current test obligations and published v3.0.5 tags/release artifacts.
- v3.1.0 remains **UNRELEASED**. A successful development CTAN pkgcheck is not release authorization.
- Reference issues: [#488](https://github.com/tiagosombrra/abntexto-ufc/issues/488) (cross-domain audit), [#489](https://github.com/tiagosombrra/abntexto-ufc/issues/489) (macro plan), [#359](https://github.com/tiagosombrra/abntexto-ufc/issues/359) (engineering).
