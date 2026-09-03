# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-02

## Status

**V3-R1 DONE. V3-R2 ACTIVE — R2-B4 bibliography and back-matter API ownership.**

Canonical R2-B4 product entry on `main`: `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`. Active implementation issue: #239. Machine authority: `release/v3-roadmap.json`.

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
| R2-B2 | DONE | PR #242 → `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout #243 → `0650845b922271fc134d20ef2a8c36ebb999ef91` | Academic/front-matter direct ownership; final `30/0/0`; release `32/0/0` | None |
| R2-B3 | DONE | issue #238; PR #245 → `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Structural/object direct ownership; Static `33704346418` PASS; Linux `33704346429` `PASS=30 FAIL=0 SKIP=0` | None |
| R2-B4 | ACTIVE | issue #239; entry `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Bibliography/references/glossary/index direct ownership | Implement and validate B4 |
| R2-B5 | PENDING | issue #240 | Final residual migration, remove `public-api.def`, create `docs/MIGRATING-TO-V3.md` | After B4 |
| V3-R3 | BLOCKED | — | Standards/tests/language semantic hardening | After R2 |
| V3-R4 | BLOCKED | — | Final certification | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and final docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |
| CTAN submission | FUTURE | explicit release action | No upload during R2 | Release-ready stage only |

## R1 certification record

R1-B8 certified the complete `template/main.tex` matrix on Windows run `33649620219` and final Linux inspection run `33655108349`. Literal institutional text-family identity, engine-appropriate math-font policy, Unicode extraction, embedding and PDF/A-2b passed. PR #233 closed R1 with Static `33656361564` and Linux integration `33656361474`, `PASS=30 FAIL=0 SKIP=0`.

## R2 progress record

R2-A established direct behavior ownership and the B1–B5 sequence. `public-api.def` is transitional forwarding debt, not a behavior owner.

R2-B1 moved canonical setup/state into direct owners. Its first full integration failed closed at `24/6/0`, exposing six stale dynamic consumers; final run `33668283890` passed `30/0/0`, and PR #236 merged at `ded5e77733795aa2958606e899d4e27f12f64df4`.

R2-B2 moved academic/front-matter rendering into direct ownership, rebound hooks and migrated live consumers. PR #242 merged at `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout #243 established B3 entry `0650845b922271fc134d20ef2a8c36ebb999ef91`. Release-source audit `33696155771` reconciled CTAN/example/public-bundle consumers.

R2-B3 started from reconciled `main` `ca1b789d44343f202f23dd193a391ef85d57986e`. The migration made structural/object environments, source/note/list APIs, optional listing/minted APIs, hooks and project-owned object IDs direct owners. Corrected bounded executor `33703865896` / job `100488717954` passed. Final head `e08592e90072cc6b42b1e7c61163003dc0bf7e28` passed Static `33704346418` and full Linux integration `33704346429` / job `100490158816` at `PASS=30 FAIL=0 SKIP=0`. PR #245 squash-merged at `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`; issue #238 is completed. `public-api.def` now contains only the four B4 bibliography/back-matter forwards.

The pre-existing observational `FRONTMATTER-EVIDENCE` FAIL records remain baseline observations inside passing aggregate gates and were not changed by the API migration.

## Immediate action

Execute **R2-B4 issue #239** from `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. Move `\ufcAddBibliographyResource` and `\ufcPrintReferences` into `bibliography.def`; move `\ufcPrintGlossary` and `\ufcPrintIndex` into `backmatter.def`; internalize non-semantic plumbing; migrate consumers atomically; remove only B4 forwarding debt. Preserve rendered Portuguese headings and genuine upstream behavior. B5 alone removes `public-api.def`. No runtime aliases, normative proof-state changes, proprietary-font redistribution or CTAN submission.
