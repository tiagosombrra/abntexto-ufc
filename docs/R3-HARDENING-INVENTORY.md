# R3 Hardening Inventory

Updated: 2026-09-03

## Purpose

R3 hardens the truthfulness of the v3 foundation before final certification. The original R3-A inventory was taken from `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`; its baseline had 19 sources, 181 rules, 164 automatic declarations, 17 manual/conditional rules, 11 project-policy/technical-profile rules, 32 runner gates, 10 registered evidence checks and 9 validator checks.

R3-B1/#252 is closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 is closed through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. R3-B3/#254 is active.

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
- final contribution: 113/113 `automatic-partial` = `bounded-positive`; 37 `enforced-automatic`; 14 `support-only`; 10 `conditional-review`; 6 `manual-review`; 1 `not-applicable`; 0 `automation-gap`;
- proof-state baseline preserved: `PARTIAL=113`, `NOT_PROVEN=51`, `MANUAL=6`, `CONDITIONAL=10`, `NOT_APPLICABLE=1`;
- normative rule IDs/values/locators/tolerances/applicability/source authority/precedence changed: **no**;
- public runtime API changed: **no**;
- temporary executor residue: **none**.

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

## Findings still open

| Finding | Owner | Issue | Status | Required result |
|---|---|---:|---|---|
| Residual gate engineering scope gap | R3-B3 | #254 | ACTIVE | Extend semantic/residual protection to behavior-affecting project-owned scripts/generators/workflows/machine/tool surfaces. |
| Generator semantic no-op risk | R3-B3 | #254 | ACTIVE | Generated matrices must assert intended canonical variation and reject stale substitutions/no-ops. |
| Test purpose/evidence integrity | R3-B3 | #254 | ACTIVE | Classify duplicate, orphan, support-only and label/behavior-mismatched checks; couple positive/negative rule IDs. |
| Engineering-language diagnostics gap | R3-B4 | #255 | PENDING | Enforce English technical diagnostics/comments/UI without touching rendered academic Portuguese. |
| Engineering profile identifiers remain Portuguese | R3-B4 | #255 | PENDING | Migrate project-owned machine identifiers where consumer-safe and preserve genuine content/upstream boundaries. |
| Closed migration contract cleanup | R3-B4 | #255 | PENDING | Prove consumers before consolidating/removing closed R2 contracts. |

## R3 lot state

| Lot | Status | Entry / result |
|---|---|---|
| R3-A/#250 | DONE | inventory source `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5` |
| R3-B1/#252 | DONE | PR #258 → `afb9f16403aafd8752a0aa8b0713f85c41204d1b`; `PASS=30 FAIL=0 SKIP=0` |
| R3-B2/#253 | DONE | PR #260 → `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`; `PASS=31 FAIL=0 SKIP=0`; 113/113 bounded-positive, automation-gap=0 |
| R3-B3/#254 | ACTIVE | entry `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` |
| R3-B4/#255 | PENDING | after B3 |
| R3-B5/#256 | PENDING | after B4; closes R3 and records immutable R4 entry |

## R3-B3 entry contract

B3 must prove that test/generator labels correspond to actual semantic behavior. It audits generated profile/type substitutions and other no-op risks, adds fail-closed assertions for canonical v3 generated values, expands the permanent removed-v2 residual scan beyond LaTeX/runtime files to behavior-affecting project-owned shell/Python/workflow/JSON/tool surfaces, inventories duplicate/orphan/support-only/label-mismatched checks, and verifies that negative-path families use the same rule identifiers as positive evidence.

The permanent residual contract must exempt only narrow explicit migration documentation/contracts, deliberate negative tests, rendered academic content and genuine upstream boundaries. B3 requires `make static-check`, focused checks for repaired generators and full `make check` before merge.

No source/currency fact changed in B1 or B2, so `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` remain intentionally unchanged. The v3 migration guide also remains unchanged because B2 changed no public runtime API.
