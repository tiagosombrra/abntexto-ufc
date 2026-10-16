# Normative Base

Updated: 2026-10-13 (targeted UFC guide-source reconciliation; technical standard recertification pending)

This document is the human-readable normative baseline for the current `abntexto-ufc` scope. Machine-readable evidence lives under `standards/`. This document does not create requirements by itself.

## Precedence

For technical requirements:

**current applicable ABNT standard → compatible/complementary current UFC requirement → current UFC guide → implementation**.

For institutional requirements:

**current UFC act → current UFC institutional requirement → current UFC guide → applicable technical standard → implementation**.

A superseded technical edition is not reactivated merely because an older UFC guide still cites it. A genuine conflict between current sources requires explicit review.

## 2026-10-16 — Document-type-aware structural validation (v3.1.0 development)

The previously global Web/Lite and CLI/Deep `structure.*` text checks incorrectly applied final-work frontmatter to all seven document profiles. In this bounded Phase-2 slice, `validator/document-applicability.json` is the single authoritative interface matrix, with an exact generated static JavaScript representation. Document type is separate from the validator rigor/capability modes `strict`, `portable`, `accessibility`. The existing final academic-work types retain their established baseline. For `research-project` and `anonymized-research-project`, `standards/rules/coverage-rules-project.json` establishes an optional cover and excludes approval page, summary and abstract; required project structure must still be reviewed against ABNT NBR 15287:2025. For `scientific-article`, `docs/ARTICLE-NORMATIVE-CONTRACT.md` establishes the primary summary and references and the optional foreign-language summary; there is no universal TCC cover, approval page or contents page requirement. Journal-specific constraints remain conditional/manual.

Only **text-token presence** is currently evaluated: required/absent → FAIL, required/present → bounded PASS, optional/present → MANUAL REVIEW, optional/absent → NOT APPLICABLE, inapplicable → NOT APPLICABLE. A text match does **not** prove layout position, section completeness, semantics, actual document-type identity, valid anonymity, or full ABNT/UFC compliance. This does not alter any parent catalog rule or promote normative proof states. The associated regression verifies 7 × 8 modality controls on positive/negative synthetic text and exercised productive PDFs in existing Web/Lite and CLI routes; dedicated real scientific-article/research-project positive/negative PDF evidence remains a subsequent distinct phase before any stronger profile-wide claim.

## 2026-10-14 — Conditional IBGE note ordering in generated PDFs (development v3.1.0)

IBGE *Normas de apresentação tabular*, 3rd ed. (1993), §4.10 requires an attributed source at the foot of a table subject to the publication-level exception. §4.11/§4.11.1 requires a **general note only when needed**, after the source, prefixed `Nota` or `Notas`. §4.12/§4.12.1 requires a **specific note only when needed**, after the general note (if present) and attached to its cell through a callout; §4.12.2 prescribes order for multiple specific notes, which is outside this slice. Verified against [institutional scan, printed pp. 20–21](https://www3.eco.unicamp.br/biblioteca/images/arquivos/pdf/Norma_de_apresentacao_tabular_IBGE_1993.pdf).

A 2026-10-14 local reproducer using `tabularray-abnt` alone observed the upstream template's default last-foot order as **specific note → source → general note**. A narrowly scoped `lastfoot` template-order adjustment was tested in a standalone TeX Live build and changed the order to **source → general note → specific note**. The new `abntexto-ufc.cls` adjustment applies only to its `abnt` and `quadro` table themes when `tables=tabularray`; CI using the actual project class and published runner remains mandatory before declaring the project fix certified. Existing font/style settings are retained.

The `tests/documents/table-ibge-notes-final-pdf.tex` fixture and new `tests/checks/objects/normative_table_ibge_notes.py` verify actual PDF text coordinates. The test compiles **four distinct PDF cases**: declared applicable general+specific note with numbered cell callout → PASS; deliberately absent required general note → FAIL; absent required numbered cell callout → FAIL; and notes genuinely not applicable, intentionally absent → NOT_APPLICABLE. Evidence JSON records physical page, marker boxes, source/general/specific order, callout count, the explicit applicability assumption and the PDF SHA-256. The new integration script is invoked from the existing table vector evidence suite to protect the legacy geometry/title/source/unit regressions.

**Limitations:** whether a note is needed or its prose semantically correct is declared by the controlled scenario rather than inferred from arbitrary user content. Other representations of specific calls, multiple-note ordering (§4.12.2), multipage table note continuation, symbol legends (§4.8.2), and exceptional source attribution are **not** certified. Never impose general/specific notes unconditionally. The 29 existing parent rules, `table.ibge` proof state `automatic-partial`, seven document profiles, and immutable released v3.0.5 source/tag/archives remain unchanged. No v3.1.0 publication authorization.

## 2026-10-13 — Conditional IBGE units: bounded PDF regression (v3.1.0 development)

IBGE *Normas de apresentação tabular*, 3rd ed. (1993), **§4.6** places a unit in the column header or indicator columns **when needed** to clarify the numeric quantity. **§4.6.1** uses a symbol or word **in parentheses**; **§4.6.2** concerns values divided by a constant (not covered by this slice). Source: [IBGE catalog PDF](https://biblioteca.ibge.gov.br/visualizacao/livros/liv23907.pdf), independently inspected in the [institutional copy, printed page 16](https://www3.eco.unicamp.br/biblioteca/images/arquivos/pdf/Norma_de_apresentacao_tabular_IBGE_1993.pdf).

The controlled fixture `tests/documents/table-ibge-unit-final-pdf.tex` and `tests/checks/objects/normative_table_ibge_unit.py` are run by `tests/integration/objects/table-ibge-unit-evidence.sh` via the **existing** IBGE vector integration gate. Three **separately compiled** PDF cases are measured using `pdftotext -bbox-layout`: (1) a declared necessary mass unit `(kg)` in the table header → **PASS**, (2) the same required unit absent from the header, but mentioned unrelatedly in the source → **FAIL** as a negative control, and (3) a scenario where a metrological unit is not applicable, intentionally absent → **NOT_APPLICABLE**. JSON stores per-PDF SHA-256, coordinates, the applicability assumption, localized header evidence and the observed verdict; CI must verify the three PDFs have distinct bytes.

**Proof boundary:** applicability is supplied by each fixture, not inferred automatically from arbitrary documents; actual data semantics, other legal units, alternative locations in indicator columns, constants under §4.6.2, and all other table criteria remain outside this regression. A missing unit **must not cause an unconditional FAIL** in the general validator. This adds no top-level catalog rule; `table.ibge` remains `automatic-partial`, the 29 parent rules and seven profiles remain unchanged, and v3.0.5 publication artifacts are immutable. Successful CI execution is required before any integration or claim of test certification.

## 2026-10-13 — IBGE table title/source PDF evidence (development v3.1.0)

The *third edition (1993)* of IBGE's [Normas de apresentação tabular](https://biblioteca.ibge.gov.br/visualizacao/livros/liv23907.pdf) establishes separate criteria for table identification (§4.1), title (§4.2), units of measure **when applicable** (§4.6), source (§4.10), explanatory notes **when necessary** (§§4.11–4.12), and continuation of tables beyond a page (§8.3). The applicable edition is the same 1993 source already present in `standards/catalog/catalog.json`; this evidence slice does **not** claim a new edition or an exhaustive ABNT audit.

A new bounded checker `tests/checks/objects/normative_table_ibge_text.py`, called by the existing `tests/integration/objects/table-ibge-vector-evidence.sh`, measures **actual PDF text with its page coordinates** from the already audited numeric-table fixture. A positive PDF verifies its caption/identification before the body and an attributed `Fonte` after the last data row; a separately **compiled negative PDF** intentionally omits the source, and must reproduce **TITLE PASS / SOURCE FAIL**. The controls emit per-predicate JSON evidence (PDF page and geometry, controlled marker counts and failure reasons) with `proof_state=automatic-partial`. They do not merely grep the TeX source and do not modify the five existing vector geometry requirements or their normative validation level.

**Normative boundary:** the observed caption token and source label are evidence only for the controlled synthetic fixture. Title semantic completeness (subject, geographic/time scope), correctness of attribution against the actual source, single-table numbering applicability, exceptional publication-wide attribution under §4.10, conditional unit symbols and notes, and multipage continuation remain unproved/manual or conditional. In particular, never impose mandatory units/notes for every table or declare all numeric tables noncompliant if one PDF source line is absent; the IBGE source includes stated applicability conditions and an exceptional reuse of a single source identified in the publication. The existing `table.ibge` catalog rule stays `automatic-partial`. No change to published v3.0.5 or to v3.1.0 publication authorization.

## 2026-10-13 — UFC guide reconciliation (v3.1.0 development target)

UFC's [current normalization page](https://biblioteca.ufc.br/pt/servicos-e-produtos/normalizacao-de-trabalhos-academicos/) lists five normalization guides. The Guide to References (2023) and Guide to Research Projects (2019) were **already present** in `standards/catalog/source-audit.json`, but absent from the compact runtime/source catalog. This correction adds both to `standards/catalog/catalog.json`, `standards/catalog/precedence.json`, and the deterministic Web/Lite catalog, without introducing new normative rules (19→21 sources, 29 rules retained).

The references guide cites superseded **NBR 6023:2018** and is inventoried as **potential institutional context** only; it is deliberately not yet attached to an atomic rule or its source-check proof, pending clause-by-clause review. The governing reference standard remains **NBR 6023:2025**. The research guide cites superseded **NBR 15287:2011**, **NBR 10520:2002**, and **NBR 6023:2018**; no older edition becomes governing. Research-specific criteria require future explicit clause-level applicability mapping. This is a source inventory and strict regression improvement, **not proof** of a complete ABNT corrigenda audit or of full institutional compliance. The catalog and precedence *global* review dates remain at their previously certified values (2026-08-22 and 2026-09-04); the two sources retain the previously documented 2026-08-22 audit check dates, with their 2026-10-13 portal reconfirmation recorded separately in their notes. A full global review-date advance requires corresponding atomic-contract revalidation. No already-published v3.0.5 source/tag/archive is altered.

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

The current runtime supports the documented academic-work profiles, research-project profile and scientific-article profile through the canonical `abntexto-ufc.cls`. Profile support does not by itself promote normative proof state; each rule remains governed by its declared evidence/proof policy. See `docs/ARTICLE-NORMATIVE-CONTRACT.md` for the scientific-article contract.

For research-project covers, the current UFC normalization page continues to publish the institutional project-research guide, whose cover example displays the UFC coat of arms. The textual cover-content list does not independently make the mark an ABNT requirement. Accordingly, `abntexto-ufc` treats the mark as a configurable UFC institutional presentation default for `research-project` and for the current person-anonymized project profile. Explicit `coat-of-arms = false` remains the supported opt-out for external or blind submissions.

## Fonts and PDF/A

UFC guidance admits Times New Roman or Arial for the relevant academic profiles. Literal font identity is certified only by the Windows font gate; portable fallback families do not prove literal Times New Roman or Arial identity.

PDF/A-2b is the project's technical certification target. It satisfies the broader archival-format goal used by the project but must not be described as a UFC requirement for the specific PDF/A-2b conformance level unless UFC explicitly states that level.

## Institutional status

`abntexto-ufc` must not be described as official, approved, or homologated by UFC unless the University explicitly grants that status.

## Maintenance rule

Before a release candidate is certified, current editions and UFC institutional acts must be reconfirmed, affected machine-readable contracts must be reconciled, runtime/tests/documentation must converge, and no superseded source may silently govern an active rule.
