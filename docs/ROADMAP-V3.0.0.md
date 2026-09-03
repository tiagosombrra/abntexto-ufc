# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-03

## Status

**V3-R1 DONE. V3-R2 ACTIVE — R2-B5 final consumer migration and forwarding-layer removal.**

R2-B4 product merge on `main`: `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`. Active implementation issue: #240. Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`. Machine authority: `release/v3-roadmap.json`.

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
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` | Deterministic release/public bundles | CTAN submission remains later |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` | Permanent static contract | None |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` | Permanent optimized workflows | Optional branch-rule enforcement |
| R1-B8 | DONE | candidate `9b1752565ac217c04ffa22a9ef272cdf078af380` | Windows/font/Unicode/embedding/PDF-A-2b certification | None |
| V3-R1 closeout | DONE | PR #233 → `0a2c2c3879986ca27b731f54b974db12524258df` | R1 closed | None |
| R2-A | DONE | issue #232 | Direct owners/upstream boundaries/lots classified | None |
| R2-B1 | DONE | PR #236 → `ded5e77733795aa2958606e899d4e27f12f64df4` | Setup/state direct ownership; `30/0/0` | None |
| R2-B2 | DONE | PR #242 → `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout #243 → `0650845b922271fc134d20ef2a8c36ebb999ef91` | Academic/front-matter direct ownership; `30/0/0`; release `32/0/0` | None |
| R2-B3 | DONE | issue #238; PR #245 → `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Structural/object direct ownership; Linux `33704346429` = `30/0/0` | None |
| R2-B4 | DONE | issue #239; PR #247 → `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` | Bibliography/reference/glossary/index direct ownership; Static `33736117556`; Linux `33736117558` = `30/0/0` | None |
| R2-B5 | ACTIVE | issue #240; product entry `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` | Final residual migration and forwarding-layer removal | Remove `public-api.def`/class load; residual scan; migration guide; close R2 |
| V3-R3 | BLOCKED | no issue activated yet | Standards/tests/language semantic hardening | After R2 |
| V3-R4 | BLOCKED | — | Final certification | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and final docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |
| CTAN submission | FUTURE | explicit release action | No upload during R2 | Release-ready stage only |

## R1 certification record

R1-B8 certified the complete `template/main.tex` matrix on Windows run `33649620219` and final Linux inspection run `33655108349`. Literal institutional text-family identity, engine-appropriate math-font policy, Unicode extraction, embedding and PDF/A-2b passed. PR #233 closed R1 with Static `33656361564` and Linux integration `33656361474`, `PASS=30 FAIL=0 SKIP=0`.

## R2 progress record

R2-A established direct behavior ownership and the B1–B5 sequence. `public-api.def` is transitional forwarding debt, not a behavior owner.

R2-B1 moved canonical setup/state into direct owners. Its first full integration failed closed at `24/6/0`, exposing six stale dynamic consumers; final run `33668283890` passed `30/0/0`, and PR #236 merged at `ded5e77733795aa2958606e899d4e27f12f64df4`.

R2-B2 moved academic/front-matter rendering into direct ownership. PR #242 merged at `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout #243 established B3 entry `0650845b922271fc134d20ef2a8c36ebb999ef91`. Release-source audit `33696155771` reconciled CTAN/example/public-bundle consumers.

R2-B3 made structural/object environments, source/note/list APIs, optional listing/minted APIs, hooks and project-owned object IDs direct owners. Final Linux `33704346429` passed `30/0/0`; PR #245 squash-merged at `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`.

R2-B4 used control-plane entry `ab900797836eb068b3f100574759816eadb039d5`. Bibliography/reference/glossary/index commands became direct owners and non-semantic plumbing became private. Three integration attempts failed closed at `29/1/0` on the shared unnumbered-heading evidence locator while the dedicated index gate remained green. The final observer measures the complete rendered heading line instead of a single locator word; `ÍNDICE REMISSIVO` passed at delta `0.0002 pt`. Final head `c2afa9e283380a1ae008638c73d12561eb97e537` passed Static `33736117556` and Linux `33736117558` / `100587276948` at `PASS=30 FAIL=0 SKIP=0`. PR #247 squash-merged at `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` and issue #239 closed completed. `public-api.def` is now empty and reserved solely for physical removal in B5.

The pre-existing observational `FRONTMATTER-EVIDENCE` FAIL records remain baseline observations inside passing aggregate gates and were not changed by the API migration.

## Immediate action

Execute **R2-B5 issue #240** only after this B4-to-B5 control-plane closeout is merged. Remove `abntexto-ufc/public-api.def` and its load from `abntexto-ufc.cls`; run the fail-closed repository-wide residual scan for project-owned Portuguese runtime/API/internal identifiers; create `docs/MIGRATING-TO-V3.md` from `release/v3-api-migration.json`; reconcile the migration contracts as consumed; validate with Static/Linux and release checks when warranted; then close R2. Do not activate an R3 issue until one is explicitly created.
