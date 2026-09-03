# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-03

## Status

**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 ACTIVE.**

R3-A inventory source is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. Its validating Static `33747658673` passed and Linux integration `33747658602` passed `PASS=30 FAIL=0 SKIP=0`. The inventory is recorded in `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`. Active implementation issue: #252. Machine authority: `release/v3-roadmap.json`.

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
| R3-A | DONE | issue #250; inventory source `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5` | current standards/test/language/proof gaps classified; five bounded lots defined | None |
| R3-B1 | ACTIVE | issue #252 | make front-matter evidence truthful and fail-closed | repair generator/observer defects; discriminate remaining findings; enforce proof |
| R3-B2 | PENDING | issue #253 | harden normative proof-state and coverage semantics | after B1 |
| R3-B3 | PENDING | issue #254 | semantic test integrity + expanded residual enforcement | after B2 |
| R3-B4 | PENDING | issue #255 | engineering-language enforcement + contract consolidation | after B3 |
| R3-B5 | PENDING | issue #256 | R3 closeout and immutable R4 entry | after B4 |
| V3-R4 | BLOCKED | — | final certification | after R3-B5 |
| V3-R5 | BLOCKED | — | foundation freeze and final docs | after R4 |
| V3-A1/A2 | BLOCKED | — | scientific-article work | after certified foundation |
| CTAN submission | FUTURE | explicit release action | no upload yet | release-ready stage only |

## R3-A inventory summary

The current source/contract baseline is green: 19 sources, 181 active rules, 164 automatic, 17 manual/conditional, 11 project-policy/technical-profile rules, 32 runner gates, 10 registered evidence checks and 9 validator checks. No new normative source/currency evidence was introduced, so the normative-base and currency documents remain unchanged.

The major hardening issue is evidence truthfulness rather than broad runtime instability. `make check` is green, but several front-matter checkers are audit-only even when they emit `FAIL`. R3-A also found a stale v2 profile substitution in the approval generator, a canonical-keyword observer bug in summary evidence, a residual-gate scope gap for scripts/engineering sources, Portuguese project-owned diagnostics/machine identifiers not covered by the current language enforcement, and two closed R2 migration contracts requiring consumer audit before consolidation.

See `docs/R3-HARDENING-INVENTORY.md` for the classified findings and ownership.

## Lot sequencing rationale

B1 comes first because proof must be truthful before any later coverage metric can be trusted. B2 then hardens proof-state/coverage semantics using corrected evidence. B3 generalizes the lesson to all test generators and the permanent residual gate. B4 makes the engineering-language policy executable and removes only closed contracts proven to be unconsumed. B5 performs R3 closeout and records a single exact R4 entry checkpoint.

## Immediate action

Execute **R3-B1 / issue #252**. Use targeted front-matter validation during iteration, then full `make check` before merge. Do not treat current audit findings as authority to change normative values or runtime semantics until fixture/observer defects are excluded.
