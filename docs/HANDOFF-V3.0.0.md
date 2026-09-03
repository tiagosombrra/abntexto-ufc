# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- R2-B4 product merge on `main`: `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`.
- B4 control-plane entry used by PR #247: `ab900797836eb068b3f100574759816eadb039d5`.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-B5 — final consumer migration and forwarding-layer removal**.
- Active issue: **#240**.
- R2-B4 / #239: **DONE through PR #247; issue closed completed**.
- R2-B3 / #238, R2-B2 / #237, R2-B1 / #234 and R2-A / #232: **DONE**.
- Certified R1 candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, machine contracts, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## R2 evidence

| Lot | Status | Main checkpoint | Validation |
|---|---|---|---|
| B1 | DONE | `ded5e77733795aa2958606e899d4e27f12f64df4` | Linux `33668283890` = `30/0/0` |
| B2 | DONE | `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout `0650845b922271fc134d20ef2a8c36ebb999ef91` | Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0` |
| B3 | DONE | `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Static `33704346418`; Linux `33704346429` = `30/0/0` |
| B4 | DONE | `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` | Static `33736117556`; Linux `33736117558` = `30/0/0` |
| B5 | ACTIVE | issue #240; product entry `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` | implementation pending after this closeout merges |

## B4 closure finding

Bibliography/reference/glossary/index public commands are direct owners. The repeated B4 `29/1/0` runs were fail-closed evidence-observer failures, not runtime layout regressions. The final observer measures the full rendered heading line: `ÍNDICE REMISSIVO` passed centered with delta `0.0002 pt`; validator locator policy, tolerances and proof state remained unchanged.

## Current runtime/API state

All semantic public API surfaces migrated in B1–B4 are directly owned. `public-api.def` is now an empty transitional file and the class still loads it once. B5 removes that file and load, performs the final project-owned Portuguese runtime/internal residual scan, reconciles the migration contracts as consumed, and creates `docs/MIGRATING-TO-V3.md` from the authoritative mappings.

## Immediate action

Execute #240 only from the merged B4-to-B5 control-plane checkpoint. Remove `public-api.def` and its class load, validate the final residual boundaries, generate the migration guide, and run proportional permanent gates. Do not mark R2 closed until the B5 implementation is merged and its closure evidence is reconciled.

## Hard boundaries

No runtime aliases; preserve rendered Portuguese academic wording and genuine upstream APIs; no normative rule/value/tolerance/locator-policy/proof-state changes without evidence; no proprietary-font redistribution; no CTAN submission during R2.
