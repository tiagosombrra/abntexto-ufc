# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- R2 product closure: `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`; merged-main release run `33745603468` = `PASS=32 FAIL=0 SKIP=0`.
- R2 closeout/control-plane source baseline and R3-A inventory source: `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`.
- R3-A planning issue: **#250 — DONE**.
- R3-A validation evidence: Static `33747658673` PASS; Linux `33747658602` = `PASS=30 FAIL=0 SKIP=0`.
- Active phase: **V3-R3**.
- Active stage: **R3-B1 — front-matter evidence truthfulness and fail-closed enforcement**.
- Active issue: **#252**.
- R3 inventory: `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## R3-A findings

R3-A did not discover new normative source/currency evidence. The source baseline remains 19 sources and 181 rules: 164 classified automatic and 17 manual/conditional. The current integration suite is green, but front-matter evidence truthfulness is not yet sufficient for R4 because audit-only producers can emit FAIL while the umbrella gate exits successfully.

Two concrete semantic defects were established before any runtime change:

1. `frontmatter-approval-evidence.sh` still substitutes the removed v2 text `tipo = tese` even though the fixture uses canonical `type = doctoral-thesis`; the profile matrix is therefore not proven to vary as labelled.
2. the summary source-paragraph observer does not recognize canonical `\ufcSummaryKeywords`, producing a false two-paragraph vernacular finding.

Additional dedication, short-epigraph, title-page and approval observations remain unresolved until B1 discriminates fixture/observer behavior from runtime behavior.

## R3 lots

| Lot | Issue | Status | Purpose |
|---|---:|---|---|
| R3-B1 | #252 | ACTIVE | front-matter evidence truthfulness and fail-closed enforcement |
| R3-B2 | #253 | PENDING | normative proof-state and coverage semantics |
| R3-B3 | #254 | PENDING | semantic test integrity and expanded residual enforcement |
| R3-B4 | #255 | PENDING | engineering-language enforcement and closed-contract consolidation |
| R3-B5 | #256 | PENDING | R3 closeout and exact R4 entry |

## Immediate action

Execute issue #252. Repair fixtures/observers first; do not change runtime behavior merely to remove an audit FAIL. Once front-matter proof-contributing evidence is truthful, enable enforcement or explicitly classify support-only observations so an aggregate PASS cannot hide a normative FAIL.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, values, locators, tolerances, applicability or proof state without current evidence. Do not start R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission during R3-B1 through R3-B4. Literal Windows-font certification remains R4-owned.
