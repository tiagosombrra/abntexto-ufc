# R3 Hardening Inventory

Updated: 2026-09-03

## Purpose

R3 hardens the truthfulness of the v3 foundation before final certification. The original R3-A inventory was taken from `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`; its baseline had 19 sources, 181 rules, 164 automatic rules, 17 manual/conditional rules, 11 project-policy/technical-profile rules, 32 runner gates, 10 registered evidence checks and 9 validator checks.

R3-B1/#252 is now closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 is active.

## R3-B1 closeout evidence

- implementation head: `347a80a8f88dd03c037ff19faf4f741cfbab7d6f`;
- focused enforced front-matter run: `33758202351` — PASS;
- PR Static contract: `33758758911` — PASS;
- PR Linux integration: `33758758877` / job `100659542227` — `PASS=30 FAIL=0 SKIP=0`;
- negative evidence: `FRONTMATTER-NEGATIVE-EVIDENCE status=PASS rejected_rule=dedication.position.start`;
- normative rule IDs/values/locators/tolerances/applicability changed: **no**;
- proof-state policy changed: **no**;
- runtime/public API changed: **no**;
- temporary executor residue: **none**.

## Findings resolved by R3-B1

| R3-A finding | Resolution |
|---|---|
| Front-matter audit not enforced | Proof-contributing front-matter runners now use enforced semantics; pagination keeps its existing intrinsic fail-closed path. |
| Approval profile generator stale v2 substitution | Generator now varies the canonical `type` value and asserts that each intended profile was actually produced. |
| Summary canonical keyword macro not recognized | Source paragraph observer recognizes canonical `\ufcSummaryKeywords` while retaining the genuine upstream `\keywords` boundary. |
| Dedication spacing discrepancy | Classified as fixture/observer artifact: a long marker wrapped physically and doubled the marker gap. Short controlled markers now produce the calibrated 20.7 pt spacing. |
| Short epigraph alignment discrepancy | Classified as extraction artifact: quote/right-edge fragments are geometrically coalesced; natural-wrap alignment evidence passes without tolerance relaxation. |
| Title/approval marker discrepancies | Classified as extraction-sensitive fixture markers; robust short markers now survive wrapping/extraction. Academic approval profiles pass and project profiles are explicitly observed as suppressed. |

The final front-matter gate is internally consistent: all proof-contributing positive evidence is PASS and the deliberate negative case is rejected. B1 therefore did not justify a runtime-format or normative-value change.

## Findings still open

| Finding | Owner | Issue | Status | Required result |
|---|---|---:|---|---|
| Coverage check name does not imply enforcement | R3-B2 | #253 | ACTIVE | Coverage must distinguish actual enforcing/bounded proof from a check merely being named/run. |
| 17 manual/conditional rules require classification | R3-B2 | #253 | ACTIVE | Each rule must be justified as legitimate manual/conditional behavior or identified as automation debt. |
| Residual gate engineering scope gap | R3-B3 | #254 | PENDING | Extend semantic/residual protection to behavior-affecting project-owned scripts/generators. |
| Engineering-language diagnostics gap | R3-B4 | #255 | PENDING | Enforce English technical diagnostics/comments/UI without touching rendered academic Portuguese. |
| Engineering profile identifiers remain Portuguese | R3-B4 | #255 | PENDING | Migrate project-owned machine identifiers where consumer-safe and preserve genuine content/upstream boundaries. |
| Closed migration contract cleanup | R3-B4 | #255 | PENDING | Prove consumers before consolidating/removing closed R2 contracts. |

## R3 lot state

| Lot | Status | Entry / result |
|---|---|---|
| R3-A/#250 | DONE | inventory source `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5` |
| R3-B1/#252 | DONE | PR #258 → `afb9f16403aafd8752a0aa8b0713f85c41204d1b`; `PASS=30 FAIL=0 SKIP=0` |
| R3-B2/#253 | ACTIVE | entry `afb9f16403aafd8752a0aa8b0713f85c41204d1b` |
| R3-B3/#254 | PENDING | after B2 |
| R3-B4/#255 | PENDING | after B3 |
| R3-B5/#256 | PENDING | after B4; closes R3 and records immutable R4 entry |

## R3-B2 entry contract

B2 must not equate `validation.checks` membership with enforcement. It must inventory the 17 manual/conditional rules, audit every `automatic-partial` rule, reconcile `normative_traceability --strict-evidence` with the proof-state and evidence registries, and expose coverage classes that distinguish enforced automatic evidence, bounded-positive evidence, conditional/manual evidence, and support-only observation where the current schemas permit.

No source/currency fact changed in B1, so `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` remain intentionally unchanged. The R2 migration guide also remains unchanged because B1 changed no public runtime API.
