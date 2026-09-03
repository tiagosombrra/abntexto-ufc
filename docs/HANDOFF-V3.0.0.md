# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- R2 product closure: `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`; merged-main release run `33745603468` = `PASS=32 FAIL=0 SKIP=0`.
- R2 closeout / R3-A inventory source: `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`.
- R3-A/#250: **DONE**.
- R3-B1/#252: **DONE** through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`.
- R3-B2/#253: **DONE** through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`; final contribution = 113/113 `automatic-partial` bounded-positive with zero automation gaps.
- B2→B3 control-plane checkpoint: `44874c84b375396de8b9e3b24a40c47b5006f19b`.
- R3-B3/#254: **DONE** through PR #262.
- R3-B3 implementation head: `5c35979e2d86b0559c5ad5373a88b83be2daf829`.
- R3-B3 closure/main SHA: `fbee5bd329f98a389c2880932af40547c8d1674e`.
- R3-B3 PR gates: Static `33792280764` PASS; Linux `33792280797` / job `100771483526` = `PASS=31 FAIL=0 SKIP=0`.
- R3-B3 post-merge release: `33794112546` / job `100777542613` = `PASS=33 FAIL=0 SKIP=0`.
- R3-B3 integrity: 302 residual-scanned sources (134 LaTeX + 168 engineering), 147/147 retained scripts reachable, 3 standalone checks classified, 0 orphaned, negative evidence coupled to positive PASS by identical `rule_id`.
- Active phase: **V3-R3**.
- Active stage: **R3-B4 — engineering-language enforcement and closed-contract consolidation**.
- Active issue: **#255**.
- R3 inventory: `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.

Git facts, `release/v3-roadmap.json`, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## What R3-B3 established

The active semantic-test surface is now fail-closed against generator no-ops and removed-v2 API residue across behavior-affecting engineering sources. The six-profile generator asserts canonical variation, the residual gate scans 303 sources, and deliberate historical/negative literals require narrow explicit annotation rather than broad file exemptions.

Every retained test/check script is either reachable from a repository-owned gate or explicitly classified as standalone certification/release support: 147/147 reachable, three standalone, zero orphaned. Negative-path cases must observe a current positive PASS for the same normative `rule_id` before controlled rejection can count.

No normative source authority, precedence, rule ID, expected value, locator, tolerance, applicability, proof-state default, rendered-format requirement, or public runtime API changed in B3.

## R3 lots

| Lot | Issue | Status | Purpose |
|---|---:|---|---|
| R3-B1 | #252 | DONE | front-matter evidence truthfulness and fail-closed enforcement |
| R3-B2 | #253 | DONE | normative proof-state and coverage semantics |
| R3-B3 | #254 | DONE | semantic test integrity and expanded residual enforcement |
| R3-B4 | #255 | ACTIVE | engineering-language enforcement and closed-contract consolidation |
| R3-B5 | #256 | PENDING | R3 closeout and exact R4 entry |

## Immediate action

Execute issue #255 from `fbee5bd329f98a389c2880932af40547c8d1674e`. Add scoped permanent engineering-language enforcement, preserve rendered/official/bibliographic/upstream Portuguese boundaries, migrate project-owned Portuguese technical profile/scenario identifiers consumer-safely, translate remaining project-owned diagnostics/comments/UI, and audit `release/v3-test-migration.json` plus `release/v3-path-migration.json` for live consumers before consolidation/removal.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, values, locators, tolerances, applicability or proof state without current evidence. `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` stay unchanged unless source/currency facts change. `docs/MIGRATING-TO-V3.md` stays unchanged unless the public API changes. Do not start R3-B5, R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission before their recorded entry conditions. Literal Windows-font certification remains R4-owned.
