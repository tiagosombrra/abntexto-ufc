# R3 Hardening Inventory

Updated: 2026-09-03

## Purpose

R3 hardens the truthfulness of the v3 foundation before final certification. The original R3-A inventory was taken from `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`; its baseline had 19 sources, 181 rules, 164 automatic declarations, 17 manual/conditional rules, 11 project-policy/technical-profile rules, 32 runner gates, 10 registered evidence checks and 9 validator checks.

R3-B1/#252 is closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 is closed through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. The B2→B3 control-plane checkpoint is `44874c84b375396de8b9e3b24a40c47b5006f19b`. R3-B3/#254 is closed through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`. R3-B4/#255 is closed through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`. R3-B5/#256 is active.

## R3-B1 closeout evidence

- implementation head: `347a80a8f88dd03c037ff19faf4f741cfbab7d6f`;
- focused enforced front-matter run: `33758202351` — PASS;
- PR Static contract: `33758758911` — PASS;
- PR Linux integration: `33758758877` / job `100659542227` — `PASS=30 FAIL=0 SKIP=0`;
- negative evidence: `FRONTMATTER-NEGATIVE-EVIDENCE status=PASS rejected_rule=dedication.position.start`;
- normative semantics / proof-state policy / runtime API changed: **no**.

## R3-B2 closeout evidence

- entry checkpoint: `32c3221c813790e938ffb29d1f4ee55c2812c47d`;
- final implementation head: `55a833fc17daddc2526c4f42e6830470de6df873`;
- merge/main SHA: `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`;
- issue / PR: #253 / #260;
- inventory run: `33764122865` — 113 `automatic-partial`, 94 direct-owner contributions, 19 ownership/evidence gaps, unsafe `PROVEN` = 0;
- independent complete validation: `33768364069` — `PASS=31 FAIL=0 SKIP=0`;
- PR Static contract: `33768911131` — PASS;
- PR Linux integration: `33768911126` / job `100694266254` — `PASS=31 FAIL=0 SKIP=0`;
- post-merge Linux release: `33772854355` / job `100707196590` — `PASS=33 FAIL=0 SKIP=0`;
- final contribution: 113/113 `automatic-partial` = `bounded-positive`; 37 `enforced-automatic`; 14 `support-only`; 10 `conditional-review`; 6 `manual-review`; 1 `not-applicable`; 0 `automation-gap`;
- proof-state baseline preserved: `PARTIAL=113`, `NOT_PROVEN=51`, `MANUAL=6`, `CONDITIONAL=10`, `NOT_APPLICABLE=1`;
- normative rule IDs/values/locators/tolerances/applicability/source authority/precedence changed: **no**;
- public runtime API changed: **no**;
- temporary executor residue: **none**.

## R3-B3 closeout evidence

- canonical B3 entry/control-plane checkpoint: `44874c84b375396de8b9e3b24a40c47b5006f19b`;
- implementation head: `5c35979e2d86b0559c5ad5373a88b83be2daf829`;
- merge/main SHA: `fbee5bd329f98a389c2880932af40547c8d1674e`;
- issue / PR: #254 / #262;
- bounded executor: `33792107946` / job `100770917618`;
- PR Static contract: `33792280764` — PASS;
- PR Linux integration: `33792280797` / job `100771483526` — `PASS=31 FAIL=0 SKIP=0`;
- post-merge Linux release: `33794112546` / job `100777542613` — `PASS=33 FAIL=0 SKIP=0`;
- residual scope: 134 LaTeX + 168 engineering = 302 sources; runtime aliases = 0; forwarding layer absent;
- test surface: 147/147 retained scripts reachable, 3 standalone classified, 0 orphaned;
- profile generator: six canonical values, six distinct generated sources, fail-closed no-op detection;
- negative paths require same-`rule_id` positive PASS before controlled rejection;
- normative semantics / proof-state defaults / public runtime API changed: **no**.

## R3-B4 closeout evidence

- canonical B4 entry/control-plane checkpoint: `f0b3df319501bef0a6257ac23d42f28c59ad73a0`;
- final implementation head: `4c22a9444db6720c0c8ae59ec8cec4bff6344672`;
- merge/main SHA: `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`;
- issue / PR: #255 / #264;
- bounded validation run: `33814870180` — PASS;
- PR Static contract: `33814977737` — PASS;
- PR Linux integration: `33814977730` / job `100844995945` — `PASS=31 FAIL=0 SKIP=0`;
- post-merge Linux release: `33816137774` / job `100848593542` — `PASS=33 FAIL=0 SKIP=0`;
- engineering-language audit: Portuguese technical diagnostics=0, retired profile IDs=0, closed unconsumed contracts=0, live API-contract consumers=2;
- permanent residual scope: 134 LaTeX + 171 engineering = 305 sources;
- test surface: 148/148 retained scripts reachable, zero orphaned;
- normative semantics / proof-state defaults / public runtime API changed: **no**.

## Findings resolved

| R3-A finding | Resolution | Lot |
|---|---|---|
| Front-matter audit not enforced | Proof-contributing front-matter runners now use enforced semantics; pagination keeps its intrinsic fail-closed path. | R3-B1 |
| Approval profile generator stale v2 substitution | Generator varies canonical `type` and asserts the intended profile was produced. | R3-B1 |
| Summary canonical keyword macro not recognized | Canonical `\ufcSummaryKeywords` is recognized while retaining the genuine upstream `\keywords` boundary. | R3-B1 |
| Dedication spacing discrepancy | Fixture/observer artifact from physical-line wrapping; controlled markers match calibrated spacing. | R3-B1 |
| Short epigraph alignment discrepancy | Extraction fragmentation repaired without tolerance relaxation. | R3-B1 |
| Title/approval marker discrepancies | Extraction-stable markers prove order and profile behavior. | R3-B1 |
| Coverage check name does not imply enforcement | Runtime contribution gate intersects rule-specific current-run evidence with declared owners; green mechanism registration alone is not proof. | R3-B2 |
| 17 manual/conditional rules require classification | All 17 are individually classified: 10 conditional-review, 6 manual-review, 1 not-applicable; none is auto-promoted from a green gate. | R3-B2 |

## Findings resolved in R3-B4

| Finding | Owner | Issue | Status | Required result |
|---|---|---:|---|---|
| Engineering-language diagnostics gap | R3-B4 | #255 | RESOLVED | Permanent checker enforces English project-owned technical diagnostics/comments/UI while protecting rendered academic Portuguese. |
| Engineering profile identifiers remain Portuguese | R3-B4 | #255 | RESOLVED | Project-owned profile/scenario machine IDs use canonical v3 English values; protected content/upstream boundaries remain unchanged. |
| Closed migration contract cleanup | R3-B4 | #255 | RESOLVED | `v3-api-migration.json` retained for two live consumers; closed unconsumed test/path contracts removed. |

## R3 lot state

| Lot | Status | Entry / result |
|---|---|---|
| R3-A/#250 | DONE | inventory source `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5` |
| R3-B1/#252 | DONE | PR #258 → `afb9f16403aafd8752a0aa8b0713f85c41204d1b`; `PASS=30 FAIL=0 SKIP=0` |
| R3-B2/#253 | DONE | PR #260 → `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`; PR `PASS=31 FAIL=0 SKIP=0`; release `PASS=33 FAIL=0 SKIP=0`; 113/113 bounded-positive, automation-gap=0 |
| R3-B3/#254 | DONE | entry `44874c84b375396de8b9e3b24a40c47b5006f19b`; PR #262 → `fbee5bd329f98a389c2880932af40547c8d1674e`; PR `PASS=31 FAIL=0 SKIP=0`; release `PASS=33 FAIL=0 SKIP=0` |
| R3-B4/#255 | DONE | entry `f0b3df319501bef0a6257ac23d42f28c59ad73a0`; PR #264 → `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`; PR `PASS=31 FAIL=0 SKIP=0`; release `PASS=33 FAIL=0 SKIP=0` |
| R3-B5/#256 | ACTIVE | entry product `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`; closes R3 and records immutable R4 entry |

## R3-B5 entry contract

B5 starts only after the B4→B5 control-plane checkpoint merges. Its product entry is `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`. It must reconcile all canonical control-plane surfaces against Git facts, confirm that no unclassified FAIL/UNASSESSED is represented as proof-contributing PASS, confirm proof/coverage/residual/language gates remain green, run `make static-check` and full `make check`, verify temporary executors and cleanup-only migration artifacts are absent, and record the exact immutable R4 certification entry. R4 Windows/literal-font certification is explicitly out of scope.

No source/currency fact or public runtime API changed in B4, so `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md` and `docs/MIGRATING-TO-V3.md` remain intentionally unchanged.
