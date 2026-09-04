# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **ACTIVE — R3-A and R3-B1 through R3-B4 DONE; R3-B5 ACTIVE**.
- R3-B4/#255 implementation head: `4c22a9444db6720c0c8ae59ec8cec4bff6344672`.
- R3-B4 PR #264 merge/main SHA: `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`.
- R3-B4 bounded validation: `33814870180` — engineering-language self-test/audit and `make static-check` PASS.
- R3-B4 PR Static contract: `33814977737` — PASS.
- R3-B4 PR Linux integration: `33814977730` / job `100844995945` — `PASS=31 FAIL=0 SKIP=0`.
- R3-B4 post-merge Linux release: `33816137774` / job `100848593542` — `PASS=33 FAIL=0 SKIP=0`.
- R3-B4 permanent baseline: 305 residual-scanned sources (134 LaTeX + 171 engineering); 148/148 retained test/check scripts reachable; zero orphans; zero Portuguese project-owned technical diagnostics; zero retired profile IDs; zero closed unconsumed migration contracts; two live `v3-api-migration` consumers.
- Active stage: **R3-B5 — R3 closeout and exact R4 certification entry**.
- Active issue: **#256**.
- B5 product predecessor: `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`.
- Canonical B5 execution/control-plane entry: `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` from PR #265.
- B5 activation PR gates: Static `33817862525` — PASS; Linux `33817846901` / job `100853855647` — `PASS=31 FAIL=0 SKIP=0`.
- B5 entry post-merge Static `33821489030` — PASS; the post-merge release run is current-state evidence and is recorded when it completes.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md` and `AGENTS.md` must agree. Disagreement fails closed.

## What R3-B4 established

The English-first engineering-language policy is executable rather than aspirational. `tests/checks/engineering_language.py` is part of `make static-check`, project-owned technical profile/scenario IDs use canonical v3 English values, and technical diagnostics/comments are English while rendered academic Portuguese, official/normative wording, bibliography data, literal output under test and genuine upstream boundaries remain protected.

The consumer audit retained `release/v3-api-migration.json` because permanent checks consume it and removed the closed, unconsumed `release/v3-test-migration.json` and `release/v3-path-migration.json` contracts. No normative authority, precedence, rule ID, expected value, locator, tolerance, applicability, proof-state default, rendered-format requirement or public runtime API changed.

## R3 lots

| Lot | Issue | Status | Purpose |
|---|---:|---|---|
| R3-B1 | #252 | DONE | front-matter evidence truthfulness and fail-closed enforcement |
| R3-B2 | #253 | DONE | normative proof-state and coverage semantics |
| R3-B3 | #254 | DONE | semantic test integrity and expanded residual enforcement |
| R3-B4 | #255 | DONE | engineering-language enforcement and closed-contract consolidation |
| R3-B5 | #256 | ACTIVE | R3 closeout and exact R4 certification entry |

## Immediate action

Execute issue #256 from canonical control-plane checkpoint `e5d6ab1962ee04935ee68a6ae36f268350d59a3b`. Reconcile every control-plane surface, prove that evidence semantics remain truthful, run `make static-check` and full `make check` on the final R3 candidate, verify temporary workflows/executors and cleanup-only migration artifacts are absent, and record the exact immutable R4 entry SHA. Do not perform the R4 Windows/literal-font certification inside B5.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, values, locators, tolerances, applicability or proof state without current evidence. `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` remain unchanged because B4 introduced no new normative source/currency facts. `docs/MIGRATING-TO-V3.md` remains unchanged because B4 changed no public runtime API. Do not start R4 certification, R5 foundation freeze, V3-A1/A2 scientific-article work or CTAN submission before their recorded entry conditions.
