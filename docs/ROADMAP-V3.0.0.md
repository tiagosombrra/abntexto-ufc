# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-03

## Status

**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 DONE; R3-B3 ACTIVE.**

R3-A inventory source is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-B1/#252 closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 closed through PR #260: final implementation head `55a833fc17daddc2526c4f42e6830470de6df873`, squash-merged main `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. Inventory run `33764122865` found 113 `automatic-partial` rules, 94 with direct owner evidence and 19 ownership/evidence gaps. Independent full validation `33768364069` and PR Linux `33768911126` / job `100694266254` both passed `PASS=31 FAIL=0 SKIP=0`; PR Static `33768911131` passed. The final contribution gate classified all 113/113 `automatic-partial` rules as bounded-positive with zero automation gaps, while preserving conservative proof states. No normative rule ID, expected value, locator, tolerance, applicability, source authority/precedence, proof-state default, or public runtime API changed. Active implementation issue: #254. Machine authority: `release/v3-roadmap.json`.

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
| R3-B3 | ACTIVE | issue #254; entry `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` | semantic test integrity + expanded residual enforcement | audit generators/check semantics; expand fail-closed residual scope; couple positive/negative evidence |
| R3-B4 | PENDING | issue #255 | engineering-language enforcement + contract consolidation | after B3 |
| R3-B5 | PENDING | issue #256 | R3 closeout and immutable R4 entry | after B4 |
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

## R3-B3 entry

R3-B3/#254 starts from `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. It must prove that active test/generator labels correspond to real semantic variation and expand the permanent removed-v2 residual contract across behavior-affecting project-owned engineering surfaces. The lot audits `.sh`, `.py`, workflows, machine JSON/tool surfaces, generator substitutions, duplicate/orphan/support-only checks, and positive/negative rule-ID coupling while preserving explicit migration records, negative tests, rendered academic content and genuine upstream boundaries.

B3 gates are proportional but fail closed: `make static-check` must include the expanded residual contract, each repaired generator gets a focused semantic assertion, and full `make check` is required before merge.

## Immediate action

Execute **R3-B3 / issue #254** from `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. Start with the generator/residual-scope inventory, then repair bounded semantic no-op risks and extend permanent residual enforcement. Do not start R3-B4, R3-B5, R4, R5, V3-A1/A2, or CTAN submission before their recorded entry conditions.
