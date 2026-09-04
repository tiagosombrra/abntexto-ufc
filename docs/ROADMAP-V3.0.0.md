# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-04

## Status

**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE. V3-R4 DONE. V3-R5/#272 DONE through PR #276 at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9` with certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` unchanged. V3-A1/#275 is ACTIVE from exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`; article runtime implementation is not allowed in A1.**

R3-A inventory source is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-B1/#252 closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 closed through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`, with 113/113 `automatic-partial` rules bounded-positive and zero automation gaps. The B2→B3 control-plane checkpoint is `44874c84b375396de8b9e3b24a40c47b5006f19b`. R3-B3/#254 closed through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`: Static `33792280764` PASS; Linux `33792280797` / job `100771483526` = `PASS=31 FAIL=0 SKIP=0`; post-merge release `33794112546` / job `100777542613` = `PASS=33 FAIL=0 SKIP=0`. Its permanent residual contract covers 302 sources (134 LaTeX + 168 engineering), retained test/check reachability is 147/147 with zero orphaned scripts, and controlled negative paths require a positive PASS for the same `rule_id`. No normative rule ID, expected value, locator, tolerance, applicability, source authority/precedence, proof-state default, rendered requirement, or public runtime API changed. R3-B4/#255 closed through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`: bounded run `33814870180` PASS; Static `33814977737` PASS; Linux `33814977730` / job `100844995945` = `PASS=31 FAIL=0 SKIP=0`; post-merge release `33816137774` / job `100848593542` = `PASS=33 FAIL=0 SKIP=0`. Permanent B4 baseline is 305 sources (134 LaTeX + 171 engineering), 148/148 retained scripts reachable, zero orphans, zero Portuguese technical diagnostics, zero retired profile IDs and zero closed unconsumed contracts. Active implementation issue: #275 (V3-A1). Machine authority: `release/v3-roadmap.json`.

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
| R3-B5 | DONE | issue #256; PR #268 → `d90a675a844724c33a5727d8d980027c46291eb0`; product candidate `c79f3c73f1d51a30175e8259269504d029442a1c` | final R3 gates green; all findings resolved; immutable R4 predecessor recorded | None |
| V3-R4 | DONE | issue #267; run `33855800767`; closeout PR #273 → `0b0f5d989163dc6b1429feeb2d8a7c66988647bb` | 4/4 strict font/engine cells PASS; Unicode, embedding and PDF/A-2b PASS; temporary executor removed | None |
| V3-R5 | DONE | issue #272; entry `0b0f5d989163dc6b1429feeb2d8a7c66988647bb`; PR #276 → `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`; frozen product `c79f3c73f1d51a30175e8259269504d029442a1c` | release `33/0/0`; package/bundle/checksum/asset audit PASS; PR Linux `31/0/0`; zero residue | None |
| V3-A1 | ACTIVE | issue #275; exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`; certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` | source/normative article contract only; runtime work not started | reconfirm article authorities/currency/precedence and derive conservative rule contract |
| V3-A2 | BLOCKED | — | article runtime/test implementation | after A1 source contract closes |
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

## R3-B5 closeout

R3-B5/#256 entered through `e5d6ab1962ee04935ee68a6ae36f268350d59a3b`, validated product candidate `c79f3c73f1d51a30175e8259269504d029442a1c`, and closed canonically through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`. PR #268 Static `33825615520` passed and Linux integration `33825615541` / job `100877511446` passed `PASS=31 FAIL=0 SKIP=0`. The underlying exact-main candidate had already passed Static `33824038991` and release `33824039033` / job `100872747975` at `PASS=33 FAIL=0 SKIP=0`.

All R3-A findings are resolved. Permanent evidence remains 113/113 `automatic-partial` bounded-positive, 37 enforced-automatic, 14 support-only, 10 conditional-review, 6 manual-review, 1 not-applicable, and zero automation gaps. Residual scope remains 305 sources, retained test/check reachability remains 148/148 with zero orphans, and engineering-language/closed-contract invariants remain green. No normative authority, precedence, rule ID, expected value, locator, tolerance, applicability, proof-state default, rendered requirement, source/currency fact, or public runtime API changed.

The immutable predecessor required by R4 is therefore `d90a675a844724c33a5727d8d980027c46291eb0`. V3-R3 and R3-B5 are DONE. R4 subsequently certified product candidate `c79f3c73f1d51a30175e8259269504d029442a1c` in run `33855800767` and closed through PR #273 at `0b0f5d989163dc6b1429feeb2d8a7c66988647bb`; R5 later closed through PR #276 at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`.

## V3-R4 certification result

V3-R4/#267 certification run `33855800767` completed successfully against exact product candidate `c79f3c73f1d51a30175e8259269504d029442a1c`. Preflight job `100968686875` proved the launch `main` differed from the product only in the expected ten documentation/control-plane files and passed `make static-check`. Windows job `100968747942` compiled the strict four-cell Times New Roman/Arial × pdfLaTeX/LuaLaTeX matrix. Linux job `100970109387` verified literal institutional text-family identity independently from math-font policy, Unicode extraction, complete font embedding and PDF/A-2b for all four artifacts. Cleanup job `100970307670` removed the temporary certification workflow.

The evidence artifact is `9930304564` with digest `sha256:ca21bf1771c45e2003b2448ea019b6eb7b93c8468eff1330df76340a943eeca2`; the Windows PDF matrix artifact is `9930280624` with digest `sha256:934044738f21261137014984114d33516b8601c0710107687903ad2f59a6b565`. pdfLaTeX correctly uses `NEW-TX-MATH`; `TeXGyreTermesX-Regular` is accepted only as part of that math stack and is not treated as institutional text fallback. LuaLaTeX uses the independent OpenType math route. No runtime API, normative semantics or proof-state default changed, and proprietary Microsoft fonts were not redistributed.

R4 closed canonically through PR #273 at `0b0f5d989163dc6b1429feeb2d8a7c66988647bb`. This immutable closeout SHA became the exact V3-R5 entry. V3-R5 subsequently completed its foundation freeze and closed through PR #276 at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`. The certified product remains `c79f3c73f1d51a30175e8259269504d029442a1c`, and V3-A1/#275 is the current active stage.

## V3-R5 foundation-freeze closeout

V3-R5/#272 entered from `0b0f5d989163dc6b1429feeb2d8a7c66988647bb` and preserved R4-certified product `c79f3c73f1d51a30175e8259269504d029442a1c` unchanged. The full release gate completed `PASS=33 FAIL=0 SKIP=0` in run `33866258865` / job `101001704635`; final package/freeze run `33869888601` / job `101013093747` passed source-only validation, reproducible public and complete distribution bundles, SHA-256 checksums, expected class/CTAN layouts, external `abntexto` semantics, institutional/proprietary asset exclusions and zero tracked/untracked residue. PR #276 then passed Static `33872118250` and Linux `33872118241` / job `101020688121` at `PASS=31 FAIL=0 SKIP=0` and squash-merged at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`.

No product-affecting path, public runtime API, normative semantics, source/currency fact, locator/tolerance/applicability policy, proof-state default or rendered requirement changed in R5. `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain unchanged. V3-R5 is DONE and `908ee2eb2ec04c030d74a9a4b146fba38fb745a9` is the exact immutable V3-A1 entry.

## V3-A1 entry

V3-A1/#275 is ACTIVE from `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`. A1 must reconfirm the current authoritative source set for the UFC scientific-article profile and applicable ABNT standards, derive current predicates/locators/applicability and requirement-versus-recommendation distinctions, integrate them with current currency/precedence/traceability/proof-state machinery, and define a bounded V3-A2 implementation contract. Historical pre-v3 article research is discovery evidence only. No article runtime/profile implementation is allowed in A1.

## Immediate action

Execute V3-A1/#275 source reconciliation. Keep the certified non-article foundation `c79f3c73f1d51a30175e8259269504d029442a1c` unchanged unless current source evidence demonstrates a separately bounded cross-cutting conflict. V3-A2 and actual CTAN submission remain blocked.
