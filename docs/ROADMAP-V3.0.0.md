# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-02

## Status

**V3-R1 DONE. V3-R2 ACTIVE — R2-B1 canonical setup and internal state vocabulary.**

Canonical `main` after R1 closeout: `0a2c2c3879986ca27b731f54b974db12524258df`. Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.

R2-A ownership inventory is DONE through issue #232. Active implementation issue: #234. Machine authority: `release/v3-roadmap.json`.

## Roadmap summary

| Stage | Status | Checkpoint / issue | Result | Remaining work |
|---|---|---|---|---|
| R1-S0 | DONE | repository sanitation | History governance rebaselined | None |
| R1-S1 | DONE | `1c7291592689f10a0e6fb043d404597ae8e53c02` | Control plane repaired | None |
| R1-S2 | DONE | `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1` | v3 promoted to `main` | None |
| R1-B1 | DONE | `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd` | Canonical physical naming | None |
| R1-B2 | DONE | `03d7f5ceb1a325d26c712ba5e619ee85530a022b` | Legacy purge/minimization | None |
| R1-B3 | DONE | `7a3b018a43630ed46b375117790acc732ae67b40` | Semantic/path-consumer closure | None |
| R1-B4 | DONE | `1a126c37653728941ce1ada762376c5fec69cb02` | Tools/validator/metadata/language rebaseline | None |
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` | Deterministic release/public bundles | Actual CTAN submission is a later explicit action |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` | Permanent `make static-check` | None |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` | Permanent optimized workflows | Optional branch-rule enforcement |
| R1-B8 | DONE | candidate `9b1752565ac217c04ffa22a9ef272cdf078af380` | Complete Windows/font/Unicode/embedding/PDF-A-2b certification | None |
| V3-R1 closeout | DONE | PR #233 → `0a2c2c3879986ca27b731f54b974db12524258df` | R1 control plane closed; #227 completed | None |
| R2-A | DONE | issue #232; `docs/R2-API-OWNERSHIP.md` | Direct owners, upstream boundaries and migration lots classified | None |
| R2-B1 | ACTIVE | issue #234 | Canonical setup/internal state migration | Implement and validate |
| R2-B2 | PENDING | — | Academic/front-matter public rendering API | After B1 |
| R2-B3 | PENDING | — | Structural/object environments, optional object API and hooks | After B2 |
| R2-B4 | PENDING | — | Bibliography/back-matter API and plumbing internalization | After B3 |
| R2-B5 | PENDING | — | Final consumer migration, `public-api.def` removal and migration documentation | After B4 |
| V3-R3 | BLOCKED | — | Standards/tests/language semantic hardening | After R2 |
| V3-R4 | BLOCKED | — | Final certification | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and final user/maintainer docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |

## R1 certification record

R1-B8 certified the complete `template/main.tex` matrix on Windows run `33649620219` and final Linux inspection run `33655108349`. Literal institutional text-family identity, engine-appropriate math-font policy, Unicode extraction, full embedding and PDF/A-2b all passed. The final R1→R2 control-plane PR #233 passed `Static contract` run `33656361564` and `Linux integration` run `33656361474` with `PASS=30 FAIL=0 SKIP=0`, then merged at `0a2c2c3879986ca27b731f54b974db12524258df`. Issue #227 is closed completed.

## R2 ownership result

`public-api.def` is confirmed as transitional forwarding debt rather than a true behavior owner. Canonical surfaces must move into the module that already owns the underlying behavior. `template/main.tex` and test consumers still use the Portuguese project API, so consumer migration is part of each behavioral lot rather than a final bulk replacement.

See `docs/R2-API-OWNERSHIP.md` for the direct-owner matrix, upstream-boundary classification and exact R2-B1…B5 sequence.

## Immediate action

Execute **R2-B1 issue #234**. Migrate canonical setup keys/values and internal state vocabulary with all live consumers atomically. Do not migrate unrelated public rendering commands, add runtime compatibility aliases, change normative semantics without new evidence, redistribute proprietary fonts, or perform actual CTAN submission.
