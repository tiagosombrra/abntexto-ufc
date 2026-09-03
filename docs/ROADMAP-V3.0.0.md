# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-03

## Status

**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A standards/tests/engineering-language hardening inventory.**

R2 closed on product merge `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` after PR #249, Static `33743809498`, Linux integration `33743809431`, and post-merge Linux release check `33745603468` = `PASS=32 FAIL=0 SKIP=0`. Active R3 entry issue: #250. Machine authority: `release/v3-roadmap.json`.

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
| R2-B1 | DONE | PR #236 → `ded5e77733795aa2958606e899d4e27f12f64df4` | Setup/state direct ownership | None |
| R2-B2 | DONE | PR #242 / closeout #243 | Academic/front-matter direct ownership | None |
| R2-B3 | DONE | PR #245 → `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Structural/object direct ownership | None |
| R2-B4 | DONE | PR #247 → `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` | Bibliography/back-matter direct ownership | None |
| R2-B5 | DONE | PR #249 → `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` | Forwarding layer removed; migration guide + permanent residual gate | None |
| V3-R2 closeout | DONE | issue #240 | v3 project API/runtime migration closed | None |
| R3-A | ACTIVE | issue #250 | Standards/tests/language current-state inventory and lot definition | Complete inventory; classify gaps; define bounded R3 lots |
| V3-R3 implementation | PENDING | defined by R3-A evidence | Semantic hardening | Do not predefine lots before inventory |
| V3-R4 | BLOCKED | — | Final certification | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and final docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |
| CTAN submission | FUTURE | explicit release action | No upload yet | Release-ready stage only |

## R2 closure record

R2-A classified direct owners and upstream boundaries. B1 moved setup/state to direct ownership; B2 moved academic/front-matter rendering; B3 moved structural/object APIs and hooks; B4 moved bibliography/reference/glossary/index APIs. B5 removed the empty forwarding-only `public-api.def`, removed its class load, published the v3 migration guide, and added the permanent fail-closed residual API gate.

B5 PR #249 head `2a8d7223a4aa9ffc80908adc9a84d0784f8dcaf4` passed Static `33743809498` and Linux integration `33743809431` before squash merge `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`. The merged-main `Linux release check` `33745603468` then passed all 32 release checks. No runtime aliases, normative semantic changes, or proof-state changes were introduced by B5.

The pre-existing observational `FRONTMATTER-EVIDENCE` FAIL records remain baseline observations inside passing aggregate gates; R2 did not promote them into normative failures.

## R3 entry rule

R3 is intentionally activated through **R3-A inventory/planning**, because the prior roadmap defined the R3 objective but did not define trustworthy implementation lots. Issue #250 must first inventory:

- current `standards/` source authority, rule coverage, currency and proof state;
- semantic test/check/document coverage, duplicated/orphaned assertions and missing invariants;
- project-owned engineering-language enforcement across runtime, tests, tools, validator, documentation and machine contracts;
- gaps that require new normative evidence versus engineering-only hardening.

Only after that inventory may bounded R3 implementation lots and proportional gates be recorded.

## Immediate action

Execute **R3-A issue #250**. Do not start R4, R5, V3-A1/A2, or CTAN submission and do not change normative semantics merely to satisfy an inventory finding.
