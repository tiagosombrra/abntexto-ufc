# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-02

## Status

**V3-R1 DONE. V3-R2 ACTIVE — R2-A runtime/API ownership inventory and migration planning.**

**R1-S0 DONE → R1-S1 DONE → R1-S2 DONE → R1-B1 DONE → R1-B2 DONE → R1-B3 DONE → R1-B4 DONE → R1-B5 DONE → R1-B6 DONE → R1-B7 DONE → R1-B8 DONE → R2-A ACTIVE → R2-B+ PENDING**

Canonical repository: `tiagosombrra/abntexto-ufc`. Active trunk: `main`.

Certified R1 product candidate: **`9b1752565ac217c04ffa22a9ef272cdf078af380`**. R1 closure issue: #227. Active R2-A issue: #232.

## Authority

`release/v3-roadmap.json` is the machine authority. This roadmap, `docs/HANDOFF-V3.0.0.md`, `AGENTS.md`, and current Git facts form the human-readable control plane. Disagreement fails closed.

## Roadmap summary

| Stage | Status | Checkpoint / evidence | Result | Remaining work |
|---|---|---|---|---|
| R1-S0 | DONE | repository sanitation | History governance rebaselined | None |
| R1-S1 | DONE | `1c7291592689f10a0e6fb043d404597ae8e53c02` | Control plane repaired | None |
| R1-S2 | DONE | `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1` | v3 promoted to `main` | None |
| R1-B1 | DONE | `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd` | Canonical physical naming | None |
| R1-B2 | DONE | `03d7f5ceb1a325d26c712ba5e619ee85530a022b` | Legacy purge/minimization | None |
| R1-B3 | DONE | `7a3b018a43630ed46b375117790acc732ae67b40` | Semantic/path-consumer closure | None |
| R1-B4 | DONE | `1a126c37653728941ce1ada762376c5fec69cb02` | Tools/validator/metadata/language rebaseline | None |
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` | Deterministic release/public bundles | CTAN upload is a later explicit release action |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` | Permanent `make static-check` | None |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` | Permanent optimized workflows | Optional branch-rule enforcement |
| R1-B8 | DONE | `9b1752565ac217c04ffa22a9ef272cdf078af380`; runs `33649620219` + `33655108349` | Full Windows/font/Unicode/embedding/PDF-A certification | None |
| V3-R2 / R2-A | ACTIVE | issue #232 | Runtime/API ownership inventory and migration planning | Complete classification before behavioral migration |
| V3-R2 / R2-B+ | PENDING | — | Direct-ownership migration lots | Defined by R2-A |
| V3-R3 | BLOCKED | — | Standards/tests/language semantic hardening | After R2 |
| V3-R4 | BLOCKED | — | Final certification phase | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and migration/user/maintainer docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |

## Final R1-B8 certification

B8-A tooling repair merged through PR #230 at `d2c24fc85351a410ea1f0101887b2a5228077741`. B8-B strict POC run `33609817951` proved the literal-font pipeline.

B8-C certified complete `template/main.tex`:

- Windows run `33649620219`, job `100313006509`: all Times New Roman/Arial × pdfLaTeX/LuaLaTeX builds PASS;
- Windows artifact `9854415113`, digest `sha256:138b9a4e3c2969db33c512bec91b323cba339bb6ae18afc76786b59d2e0f7a21`;
- final Linux inspection run `33655108349`, job `100331601354`: PASS;
- evidence artifact `9856387211`, digest `sha256:256c96e1c32d839b5b3a3e55f7a355913b7b217609c2f6e2d27104e7e12ffeeb`;
- literal institutional text-family identity: PASS;
- independent engine-appropriate math-font policy: PASS;
- Unicode extraction: PASS;
- font embedding (`emb=yes`): PASS;
- PDF/A-2b: PASS.

The earlier `TeXGyreTermesX-Regular` flag was a checker false positive: it is part of the pdfLaTeX `newtxmath` stack and is not institutional text-family fallback. The final inspection separates text-family identity from math-font policy.

No runtime/API, normative semantics, locator/tolerance, proof-state, or proprietary-font distribution change occurred. Temporary B8 executors were removed.

## V3-R2 — Runtime/API internationalization

### R2-A — Ownership inventory and migration plan

**ACTIVE via issue #232.** This stage is inventory/classification only. It must inventory remaining project-owned Portuguese setup keys/values, commands, environments, hooks and internal behavior owners; classify genuine upstream non-English boundaries; map every canonical English forwarding surface in `abntexto-ufc/public-api.def` to a direct responsibility owner; and define atomic producer/consumer/test/template/documentation migration lots.

`release/v3-api-migration.json` is active. `public-api.def` is transitional R2 debt. Final v3 exposes one canonical project API implemented directly by responsibility-owning modules; removed Portuguese v2 project API is not retained through runtime aliases.

### R2-A exit condition

Every remaining project-owned Portuguese runtime/API surface and every `public-api.def` forwarding mapping has an explicit classification, direct owner, migration lot and validation plan.

## Immediate action

Execute R2-A issue #232. Inventory and classify first; do not perform blind global replacement, normative semantic changes without new evidence, proprietary font redistribution, or actual CTAN submission.
