# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-03

## Status

**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 ACTIVE.**

R3-A inventory source is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-B1/#252 closed through PR #258: implementation head `347a80a8f88dd03c037ff19faf4f741cfbab7d6f`, squash-merged main `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. Focused enforcement run `33758202351` passed; PR Static `33758758911` passed; Linux integration `33758758877` / job `100659542227` passed `PASS=30 FAIL=0 SKIP=0`. The deliberate negative front-matter fixture was rejected on `dedication.position.start`. No normative rule ID, expected value, locator, tolerance, applicability, or proof-state policy changed. Active implementation issue: #253. Machine authority: `release/v3-roadmap.json`.

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
| R3-B2 | ACTIVE | issue #253; entry `afb9f16403aafd8752a0aa8b0713f85c41204d1b` | harden normative proof-state and coverage semantics | classify 17 manual/conditional rules; distinguish enforced, bounded-positive, conditional/manual and support-only evidence |
| R3-B3 | PENDING | issue #254 | semantic test integrity + expanded residual enforcement | after B2 |
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

## R3-B2 entry

The baseline remains 19 sources and 181 active rules: 164 currently classified automatic and 17 manual/conditional, with 11 project-policy/technical-profile rules, 32 runner gates, 10 registered evidence checks and 9 validator checks. B1 makes front-matter enforcement trustworthy but does not by itself prove that the aggregate coverage vocabulary distinguishes enforcement from mere observation.

B2/#253 must inventory all 17 manual/conditional rules, audit every `automatic-partial` rule, reconcile strict traceability/proof-state/evidence registries, and expose coverage counts that do not call a rule covered merely because a named check ran. Source authority, precedence, rule IDs, expected values, tolerances, locators and applicability stay fixed absent new current normative evidence.

## Immediate action

Execute **R3-B2 / issue #253** from `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. Start with source-only inventory and targeted normative/validator checks. Use `make check` before merge only if integration evidence semantics are touched, and `make release-check` only if release-only proof-state behavior changes.
