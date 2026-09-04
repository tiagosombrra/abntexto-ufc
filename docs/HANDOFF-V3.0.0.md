# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **ACTIVE only for exact-entry closeout**.
- R3-A and R3-B1 through R3-B4: **DONE**.
- R3-B5/#256: **TECHNICALLY VALIDATED; exact R4 entry activation pending**.
- Canonical B5 entry: `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` from PR #265.
- Final R3 product/control-plane candidate: `c79f3c73f1d51a30175e8259269504d029442a1c` from PR #266.
- PR #266 Static: `33822238687` — PASS.
- PR #266 Linux: `33822238656` / job `100867206797` — `PASS=31 FAIL=0 SKIP=0`.
- Exact-main Static: `33824038991` — PASS.
- Exact-main release: `33824039033` / job `100872747975` — `PASS=33 FAIL=0 SKIP=0`.
- Evidence contribution: 113/113 `automatic-partial` bounded-positive; 37 enforced-automatic; 14 support-only; 10 conditional-review; 6 manual-review; 1 not-applicable; zero automation gaps.
- Residual baseline: 305 sources (134 LaTeX + 171 engineering).
- Retained test/check reachability: 148/148; zero orphans.
- Engineering-language baseline: zero Portuguese technical diagnostics; zero retired profile IDs; zero closed unconsumed contracts; two live `v3-api-migration` consumers.
- All R3-A findings: **RESOLVED**.
- R4 planning issue: **#267 PREPARED; certification not started**.
- Certified R1 historical candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; current-candidate literal-font recertification remains R4-owned.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Why R3 is not marked DONE yet

The final R3 candidate is technically green, but the roadmap requires an exact immutable R4 entry. A squash-merge SHA does not exist before the merge that creates it. Therefore this checkpoint records completed B5 validation without inventing a future SHA. After this closeout merges, one minimal control-plane activation records that real predecessor SHA, marks R3-B5 and V3-R3 DONE, and activates V3-R4/#267.

## Immediate action

Merge this validated B5 closeout, capture its immutable main SHA, then perform the exact-entry activation. Do not start Windows/literal-font/PDF-A certification before the activation checkpoint is canonical.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative authority, precedence, rule IDs, values, locators, tolerances, applicability, proof-state defaults, or rendered requirements without current evidence. `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain intentionally unchanged. R5 foundation freeze, V3-A1/A2 scientific-article work, and CTAN submission remain blocked.
