# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- R2-B5 product merge: `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` through PR #249.
- R2-B5 Static contract: `33743809498` = PASS.
- R2-B5 Linux integration: `33743809431` = PASS.
- Post-merge Linux release check: `33745603468` = `PASS=32 FAIL=0 SKIP=0`.
- Active phase: **V3-R3**.
- Active stage: **R3-A — standards, tests, and engineering-language hardening inventory**.
- Active issue: **#250**.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## R2 closure

| Lot | Status | Main checkpoint | Validation |
|---|---|---|---|
| B1 | DONE | `ded5e77733795aa2958606e899d4e27f12f64df4` | Linux `33668283890` = `30/0/0` |
| B2 | DONE | `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout `0650845b922271fc134d20ef2a8c36ebb999ef91` | Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0` |
| B3 | DONE | `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Static `33704346418`; Linux `33704346429` = `30/0/0` |
| B4 | DONE | `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` | Static `33736117556`; Linux `33736117558` = `30/0/0` |
| B5 | DONE | `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` | Static `33743809498`; Linux `33743809431` PASS; release `33745603468` = `32/0/0` |

R2-B5 removed `abntexto-ufc/public-api.def` and its class load, added `docs/MIGRATING-TO-V3.md`, and made `tests/checks/v3_api_residual.py` a permanent fail-closed source gate. No runtime compatibility alias layer was added.

## Current runtime/API state

The v3 project API is directly owned by its behavior modules. The forwarding-only layer is absent. Removed v2 project API is migration-documentation material only; active runtime/template/test consumers are protected by the permanent residual gate.

## Immediate action

Execute issue #250 as **R3-A inventory/planning only**. Inventory current `standards/` authority/proof state, semantic test coverage and engineering-language enforcement, classify gaps, then define bounded R3 implementation lots. Do not infer or pre-stage later R3 lots before the inventory establishes them.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, expected values, tolerances, locators or proof state without explicit current evidence. Do not start R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission during R3-A.
