# NBR 6023:2025 — Librarian Review Item 33 Decision

Updated: 2026-09-08  
Status: AUTHORITY-RESOLVED — IMPLEMENTATION/CI PENDING

## Purpose

This document resolves the authority gap behind librarian-review item 33 using the current ABNT NBR 6023:2025. The historical reviewer annotations remain evidence, but runtime behavior is changed only where the current edition supports the behavior.

## Authority decision

| Subcase | Current-edition basis | V3 decision |
|---|---|---|
| Online documents | NBR 6023:2025, 6.6 | A document actually consulted online carries the electronic address introduced by `Disponível em:` and the access date introduced by `Acesso em:`. |
| Online monographs | NBR 6023:2025, 7.2.2, referring to 6.6 | Apply the online-address/access rule. DOI may be included as complementary information when useful or necessary to identify the document. |
| Electronic journal articles | NBR 6023:2025, 7.7.6, referring to 7.7.5 and 6.6 | Include DOI when it exists. If the article was consulted online, also apply the 6.6 online-address/access requirements. |
| Corporate / government author | NBR 6023:2025, 8.1.2 | Enter the work by the known or highlighted corporate form and standardize the same corporate author across the reference list. Preserve jurisdiction qualifiers such as `SÃO PAULO (Estado)` rather than mechanically uppercasing the qualifier. |
| Repeated author | Current NBR 6023:2025 institutional implementation guidance and the current `biblatex-abnt` repetition mechanism | Repeat the author name in subsequent references. Do not restore the legacy underscore/dash substitution. |

## Source record

The clause-level evidence used for this decision was rechecked on 2026-09-08 from publicly accessible institutional copies/guidance for the current edition:

- 6.6 and 7.2.2: `https://engenhariaedesenvolvimentosustentavel.ufes.br/sites/engenhariaedesenvolvimentosustentavel.ufes.br/files/field/anexo/abnt_nbr_6023_-_referencias.pdf`;
- 7.7.6: current-edition copies exposing the electronic-periodical clause, including institutional/publicly accessible copies indexed by the project research;
- 8.1.2 and the `SÃO PAULO (Estado)` current-edition example: `https://vigilanciasanitaria.prefeitura.rio/wp-content/uploads/sites/84/2025/10/ABNT-NBR-6023-2025-Normatizacao-de-referencias.pdf` and other institutional copies;
- repeated-author operational guidance aligned to NBR 6023:2025: Colégio Pedro II and current SciELO journal instructions.

The repository stores locators, paraphrases and source URLs only; it does not vendor copyrighted standard text.

## Implementation boundaries

1. Set `repeatfields=true` explicitly so the project contract does not depend on an upstream default for repeated authors.
2. Add controlled reference fixtures for:
   - an online journal article with DOI + URL + access date;
   - two consecutive works by the same personal author;
   - the government/corporate author form `SÃO PAULO (Estado)`.
3. Preserve the existing DOI-only fixture to prove that a DOI alone does not synthesize URL/access metadata.
4. Do not globally rewrite DOI values as `https://doi.org/...`; DOI and online-address metadata remain separate fields.
5. Do not invent `url` or `urldate` when source metadata do not state that the document was consulted online.
6. Keep the current UFC/ABNT source-precedence contract unchanged.

## Acceptance gate

Item 33 moves from `NORMATIVE-REVIEW` to `PARTIAL` when this authority decision and implementation are committed. It moves to `PASS` only after the controlled 16-case NBR 6023:2025 profile passes with pdfLaTeX and LuaLaTeX and the synchronized Release Static, complete Linux and Linux release-check gates are green.

Any CI failure is classified before changing the rule or test. The authority decision is not weakened merely to recover green status.
