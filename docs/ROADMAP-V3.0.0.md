# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-03

## Status

**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 DONE; R3-B3 DONE; R3-B4 DONE; R3-B5 ACTIVE.**

R3-A inventory source is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-B1/#252 closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 closed through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`, with 113/113 `automatic-partial` rules bounded-positive and zero automation gaps. The B2→B3 control-plane checkpoint is `44874c84b375396de8b9e3b24a40c47b5006f19b`. R3-B3/#254 closed through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`: Static `33792280764` PASS; Linux `33792280797` / job `100771483526` = `PASS=31 FAIL=0 SKIP=0`; post-merge release `33794112546` / job `100777542613` = `PASS=33 FAIL=0 SKIP=0`. Its permanent residual contract covers 302 sources (134 LaTeX + 168 engineering), retained test/check reachability is 147/147 with zero orphaned scripts, and controlled negative paths require a positive PASS for the same `rule_id`. No normative rule ID, expected value, locator, tolerance, applicability, source authority/precedence, proof-state default, rendered requirement, or public runtime API changed. R3-B4/#255 closed through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`: bounded run `33814870180` PASS; Static `33814977737` PASS; Linux `33814977730` / job `100844995945` = `PASS=31 FAIL=0 SKIP=0`; post-merge release `33816137774` / job `100848593542` = `PASS=33 FAIL=0 SKIP=0`. Permanent B4 baseline is 305 sources (134 LaTeX + 171 engineering), 148/148 retained scripts reachable, zero orphans, zero Portuguese technical diagnostics, zero retired profile IDs and zero closed unconsumed contracts. Active implementation issue: #256. Machine authority: `release/v3-roadmap.json`.

## Roadmap summary

| Stage | Status | Checkpoint / issue | Result | Remaining work |
|---|---|---|---|---|
| R1-S0/S1/S2 | DONE | reconstruction bootstrap | sanitation, control plane and v3 trunk promotion complete | None |
| R1-B1…B7 | DONE | through `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` | architecture, bundles, static contract and permanent CI complete | Optional branch-rule enforcement only |
| R1-B8 | DONE | candidate `9b1752565ac217c04ffa22a9ef272cdf078af380` | Windows/font/Unicode/embedding/PDF-A-2b certification complete | None |
| V3-R1 closeout | DONE | PR #233 → `0a2c2c3879986ca27b731f54b974db12524258df` | R1 closed | None |
| R2-A | DONE | issue #232 | owner/upstream-boundary inventory | None |
| R2-B1 | DONE | PR #236 → `ded5e77733795aa2958606e899d4e27f12f64df4` | setup/state direct ownership | None |
| R2-B2 | DONE | PR #242 / #243 | academic/front-matter direct ownership | None |
| R2-B3 | DONE | PR #245 → `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | structural/object direct ownership | None |
| R2-B4 | DONE | PR #247 → `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` | bibliography/back-matter direct ownership | None |
| R2-B5 | DONE | PR #249 → `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` | forwarding layer removed; migration guide + permanent residual gate | None |
| V3-R2 closeout | DONE | PR #251 → `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5` | canonical control plane reconciled; R3-A opened | None |
| R3-A | DONE | issue #250 | standards/test/language/proof gaps classified; five bounded lots defined | None |
| R3-B1 | DONE | issue #252; PR #258 → `afb9f16403aafd8752a0aa8b0713f85c41204d1b` | front-matter observers/generators repaired; proof-contributing evidence fail-closed; negative rejection proven | None |
| R3-B2 | DONE | issue #253; PR #260 → `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` | 17 non-automatic rules classified; 113/113 `automatic-partial` bounded-positive; explicit enforced/support-only semantics | None |
| R3-B3 | DONE | issue #254; PR #262; canonical entry `44874c84b375396de8b9e3b24a40c47b5006f19b`; merge `fbee5bd329f98a389c2880932af40547c8d1674e` | 302-source residual gate; 147/147 reachable checks; zero orphaned scripts; Linux 31/0/0; release 33/0/0 | None |
| R3-B4 | DONE | issue #255; PR #264; canonical entry `f0b3df319501bef0a6257ac23d42f28c59ad73a0`; merge `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390` | permanent engineering-language enforcement; canonical profile IDs; closed-contract consolidation; PR `31/0/0`; release `33/0/0` | None |
| R3-B5 | ACTIVE | issue #256; entry `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390` | R3 closeout and immutable R4 entry | reconcile final candidate; run Static + full Linux; record exact R4 entry SHA |
| V3-R4 | BLOCKED | — | final certification | after R3-B5 |
| V3-R5 | BLOCKED | — | foundation freeze and final docs | after R4 |
| V3-A1/A2 | BLOCKED | — | scientific-article work | after certified foundation |
| CTAN submission | FUTURE | explicit release action | no upload yet | release-ready stage only |

## R3-B1 closeout

B1 repaired the evidence model before considering runtime changes. The approval matrix now exercises the intended six canonical v3 types rather than relying on a stale v2 substitution. Summary paragraph counting recognizes `\ufcSummaryKeywords`. Title-page/approval markers were shortened to survive PDF extraction, dedication spacing fixtures no longer create accidental physical-line wrapping, and short-epigraph geometry coalesces extractor fragments without relaxing the normative tolerance.

Spacing and alignment are now intentionally separated: explicit-line fixtures prove spacing while natural-wrap fixtures prove justification. Proof-contributing front-matter runners execute enforced semantics; optional-list and TOC checkers expose enforcement explicitly, while pagination retains its pre-existing intrinsic fail-closed behavior. The negative fixture deliberately places the dedication above its permitted start and the gate proves rejection at `dedication.position.start`.

The full PR gate passed all 30 integration checks. The R3-A front-matter findings are therefore resolved as observer/generator/enforcement defects, not as evidence requiring a normative or runtime-format change.

## R3-B2 closeout

B2 repaired the distinction between traceable mechanisms, current-run rule-specific contribution, and conservative proof state. The 17 non-automatic rules are explicitly classified as 10 `conditional-review`, 6 `manual-review`, and 1 `not-applicable`; none was promoted merely because a related gate was green.

The coordinated contribution gate now runs after complete validation and intersects current-run structured evidence with each rule's declared owners. The final PR run closed with 181 rules: 113/113 `automatic-partial` as `bounded-positive`, 37 `enforced-automatic`, 14 `support-only`, 10 `conditional-review`, 6 `manual-review`, 1 `not-applicable`, and zero `automation-gap`. `bounded-positive` remains `PARTIAL`, not `PROVEN`.

B2 entered from `32c3221c813790e938ffb29d1f4ee55c2812c47d`, used inventory run `33764122865`, and merged through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. Static `33768911131` passed; Linux integration `33768911126` / job `100694266254` and independent validation `33768364069` both passed `PASS=31 FAIL=0 SKIP=0`. Post-merge Linux release `33772854355` / job `100707196590` passed `PASS=33 FAIL=0 SKIP=0`. Source authority, precedence, rule IDs, expected values, tolerances, locators, applicability, proof-state defaults and public runtime API were unchanged.

## R3-B3 closeout

R3-B3/#254 entered from the reconciled B2→B3 control-plane checkpoint `44874c84b375396de8b9e3b24a40c47b5006f19b`, not directly from the earlier B2 product SHA. Its implementation head was `5c35979e2d86b0559c5ad5373a88b83be2daf829` and PR #262 squash-merged at `fbee5bd329f98a389c2880932af40547c8d1674e`.

The six-profile generator is fail-closed and bound to canonical v3 values; `tests/checks/v3_api_residual.py` now covers 134 LaTeX plus 168 behavior-affecting engineering sources; deliberate removed-v2 literals require narrow `negative-test-literal` annotation; retained test/check scripts are 147/147 reachable with three standalone certification/release checks explicitly classified and zero orphaned scripts; obsolete `frontmatter_validation.py` was removed; public/distribution bundle checks reject the removed forwarding layer; and negative-path evidence requires a positive PASS for the same `rule_id`.

Static `33792280764` passed. PR Linux integration `33792280797` / job `100771483526` passed `PASS=31 FAIL=0 SKIP=0`. Post-merge Linux release `33794112546` / job `100777542613` passed `PASS=33 FAIL=0 SKIP=0`, including release-only PDF/A checks. Normative semantics, proof-state defaults and the public runtime API did not change.

## R3-B4 closeout

R3-B4/#255 entered canonically from `f0b3df319501bef0a6257ac23d42f28c59ad73a0`, implemented on `4c22a9444db6720c0c8ae59ec8cec4bff6344672` and squash-merged through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`. `tests/checks/engineering_language.py` is now a permanent static contract; project-owned technical profile IDs use canonical v3 values; academic/normative/bibliographic Portuguese remains protected; `release/v3-api-migration.json` is retained for its two permanent consumers; and the two closed unconsumed migration contracts were removed. The permanent baseline is 305 residual-scanned sources and 148/148 reachable retained scripts with zero orphans. Static, PR Linux and post-merge release are green, and no normative semantics, proof-state defaults or public runtime API changed.

## R3-B5 entry

R3-B5/#256 starts after this B4→B5 control-plane checkpoint, from product SHA `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`. It owns final R3 reconciliation, truthful-evidence confirmation, `make static-check`, full `make check`, temporary-executor/migration-artifact absence, and recording the exact immutable R4 certification entry. It must not perform R4 certification.

## Immediate action

Execute **R3-B5 / issue #256** from the canonical B4→B5 checkpoint. Do not start R4 final certification, R5, V3-A1/A2, or CTAN submission before B5 records the immutable R4 entry.
