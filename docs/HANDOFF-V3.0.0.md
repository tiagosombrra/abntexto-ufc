# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-04

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1 through V3-R5: **DONE**.
- Certified non-article foundation: `c79f3c73f1d51a30175e8259269504d029442a1c`.
- V3-A1/#275: **DONE**.
- A1 exact entry: `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`.
- A1 source-contract PR #279: `4d018a92697e8f39e3a53b034c451e55996c84fb`.
- A1 closeout PR #281: `7a7562d23e8bf6c92abb635718639d617a2ed6ff`.
- A1 source-only validation `33894907220` PASS; Static `33895016834` PASS; Linux `33895016774` / job `101095498647` = `PASS=31 FAIL=0 SKIP=0`.
- Scientific-article source contract: 18 rules = 17 manual + 1 conditional-manual; no runtime/proof promotion occurred in A1.
- V3-A2/#280: **ACTIVE** from exact predecessor `7a7562d23e8bf6c92abb635718639d617a2ed6ff`.
- A2 runtime implementation: **STARTED** in the bounded canonical-profile lot; article proof promotion remains pending article-specific evidence.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Continue V3-A2/#280 from its exact entry `7a7562d23e8bf6c92abb635718639d617a2ed6ff`. The canonical `scientific-article` runtime/profile-matrix lot is in progress; next add article-specific fail-closed rule evidence, then promote only the rules actually proven by that evidence.

## Hard boundaries

Preserve certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` and the closed v3 API. Do not change article authority, modality, rule IDs, locators, applicability or proof state without new current evidence. No runtime aliases or retired Portuguese machine identifiers. No proprietary-font redistribution. CTAN submission remains a separate future release action.
