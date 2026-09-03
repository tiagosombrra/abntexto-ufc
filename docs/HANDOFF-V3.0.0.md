# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- R2 product closure: `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`; merged-main release run `33745603468` = `PASS=32 FAIL=0 SKIP=0`.
- R2 closeout / R3-A inventory source: `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`.
- R3-A/#250: **DONE**.
- R3-B1/#252: **DONE** through PR #258.
- R3-B1 implementation head: `347a80a8f88dd03c037ff19faf4f741cfbab7d6f`.
- R3-B1 closure/main SHA: `afb9f16403aafd8752a0aa8b0713f85c41204d1b`.
- R3-B1 focused enforcement run: `33758202351` — PASS, including deliberate rejection of `dedication.position.start`.
- R3-B1 PR gates: Static `33758758911` PASS; Linux `33758758877` / job `100659542227` = `PASS=30 FAIL=0 SKIP=0`.
- Active phase: **V3-R3**.
- Active stage: **R3-B2 — normative proof-state and coverage semantics hardening**.
- Active issue: **#253**.
- R3 inventory: `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## What R3-B1 established

Front-matter proof evidence is now fail-closed. B1 fixed the stale approval-profile generator, canonical summary keyword observation, extraction-sensitive title/approval markers, dedication spacing fixture behavior, and short-epigraph extractor fragmentation. It separated explicit-line spacing evidence from natural-wrap alignment evidence, enforced proof-contributing front-matter checkers, preserved pagination's intrinsic fail-closed behavior, and added a negative fixture that must be rejected.

The final PR integration gate passed all 30 checks. The changes did not modify normative source authority, rule IDs, expected values, locators, tolerances, applicability, runtime API, or proof-state policy.

## R3 lots

| Lot | Issue | Status | Purpose |
|---|---:|---|---|
| R3-B1 | #252 | DONE | front-matter evidence truthfulness and fail-closed enforcement |
| R3-B2 | #253 | ACTIVE | normative proof-state and coverage semantics |
| R3-B3 | #254 | PENDING | semantic test integrity and expanded residual enforcement |
| R3-B4 | #255 | PENDING | engineering-language enforcement and closed-contract consolidation |
| R3-B5 | #256 | PENDING | R3 closeout and exact R4 entry |

## Immediate action

Execute issue #253 from `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. Inventory all 17 manual/conditional rules, audit `automatic-partial` proof claims, reconcile strict traceability with the proof/evidence registries, and make coverage metrics distinguish enforced automatic evidence, bounded positive evidence, conditional/manual evidence and support-only observations without changing normative meaning.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, values, locators, tolerances, applicability or proof state without current evidence. `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` stay unchanged unless source/currency facts change. Do not start R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission during R3-B2 through R3-B4. Literal Windows-font certification remains R4-owned.
