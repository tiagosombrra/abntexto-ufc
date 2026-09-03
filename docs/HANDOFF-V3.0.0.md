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
- R3-B2/#253: **DONE** through PR #260.
- R3-B2 entry checkpoint: `32c3221c813790e938ffb29d1f4ee55c2812c47d`.
- R3-B2 implementation head: `55a833fc17daddc2526c4f42e6830470de6df873`.
- R3-B2 closure/main SHA: `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`.
- R3-B2 inventory run: `33764122865` — 113 `automatic-partial`, 94 direct-owner evidence, 19 ownership/evidence gaps, unsafe `PROVEN` = 0.
- R3-B2 independent full validation: `33768364069` — `PASS=31 FAIL=0 SKIP=0`.
- R3-B2 PR gates: Static `33768911131` PASS; Linux `33768911126` / job `100694266254` = `PASS=31 FAIL=0 SKIP=0`.
- R3-B2 final contribution: 181 rules; 113/113 `automatic-partial` bounded-positive; 37 enforced-automatic; 14 support-only; 10 conditional-review; 6 manual-review; 1 not-applicable; automation-gap = 0.
- Post-merge technical release run: `33772854355` / job `100707196590` — `PASS=33 FAIL=0 SKIP=0` for `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`.
- Active phase: **V3-R3**.
- Active stage: **R3-B3 — semantic test integrity and expanded residual enforcement**.
- Active issue: **#254**.
- R3 inventory: `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.

Git facts, `release/v3-roadmap.json`, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## What R3-B2 established

A named or green validation mechanism is no longer treated as proof by association. Complete coordinated runs now classify current-run rule-specific contribution against declared evidence owners. Every `automatic-partial` rule must produce a current rule-specific PASS from a declared owner or the contribution gate fails closed with `automation-gap`.

The 17 non-automatic rules are individually justified. The final runtime projection is 37 `enforced-automatic` + 113 `bounded-positive` + 14 `support-only` = 164 automatic declarations, with 10 conditional reviews, 6 manual reviews and 1 not-applicable rule. This projection does not alter the proof-state baseline: bounded-positive rules remain `PARTIAL`; support-only observations are not enforcement.

No normative source authority, precedence, rule ID, expected value, locator, tolerance, applicability, proof-state default, rendered-format requirement, or public runtime API changed in B2.

## R3 lots

| Lot | Issue | Status | Purpose |
|---|---:|---|---|
| R3-B1 | #252 | DONE | front-matter evidence truthfulness and fail-closed enforcement |
| R3-B2 | #253 | DONE | normative proof-state and coverage semantics |
| R3-B3 | #254 | ACTIVE | semantic test integrity and expanded residual enforcement |
| R3-B4 | #255 | PENDING | engineering-language enforcement and closed-contract consolidation |
| R3-B5 | #256 | PENDING | R3 closeout and exact R4 entry |

## Immediate action

Execute issue #254 from `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. Audit fixture/test generators for substitutions and semantic no-ops, add fail-closed assertions that generated variants actually differ and use canonical v3 values, expand removed-v2 residual scanning to behavior-affecting project-owned shell/Python/workflow/JSON/tool surfaces, inventory duplicate/orphan/support-only/label-behavior mismatches, and keep positive/negative evidence coupled to the same rule IDs.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, values, locators, tolerances, applicability or proof state without current evidence. `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` stay unchanged unless source/currency facts change. `docs/MIGRATING-TO-V3.md` stays unchanged unless the public API changes. Do not start R3-B4/B5, R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission before their recorded entry conditions. Literal Windows-font certification remains R4-owned.
