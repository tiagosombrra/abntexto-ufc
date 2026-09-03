# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-02

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical R2-B4 product entry on `main`: `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-B4 — bibliography and back-matter API ownership**.
- Active issue: **#239**.
- R2-B3 / #238: **DONE through PR #245; issue closed completed**.
- R2-B2 / #237, R2-B1 / #234 and R2-A / #232: **DONE**.
- Certified R1 candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, machine contracts, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## R2 evidence

| Lot | Status | Main checkpoint | Validation |
|---|---|---|---|
| B1 | DONE | `ded5e77733795aa2958606e899d4e27f12f64df4` | Linux `33668283890` = `30/0/0` |
| B2 | DONE | `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout `0650845b922271fc134d20ef2a8c36ebb999ef91` | Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0` |
| B3 | DONE | `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Static `33704346418` PASS; Linux `33704346429` = `PASS=30 FAIL=0 SKIP=0` |
| B4 | ACTIVE | entry `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | implementation pending |
| B5 | PENDING | issue #240 | after B4 |

## Current runtime/API state

B1 setup/state, B2 academic/front-matter and B3 structural/object surfaces are directly owned. B3 migrated project-owned `codigo` / `algoritmo` to `code` / `algorithm`; genuine upstream `grafico` / `quadro` remain only at integration boundaries. `public-api.def` now contains exactly four B4 forwards: bibliography resource registration, references, glossary and index.

## Immediate action

Execute #239 from `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. Absorb the four remaining commands into `bibliography.def` and `backmatter.def`, internalize implementation-only plumbing, migrate live consumers atomically and validate. B5 removes `public-api.def` and creates `docs/MIGRATING-TO-V3.md`.

## Hard boundaries

No runtime aliases; preserve rendered Portuguese academic wording and genuine upstream APIs; no normative rule/value/tolerance/locator/proof-state changes without evidence; no proprietary-font redistribution; no CTAN submission during R2.
