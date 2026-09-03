#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLOSURE_SHA = "afb9f16403aafd8752a0aa8b0713f85c41204d1b"
IMPLEMENTATION_HEAD = "347a80a8f88dd03c037ff19faf4f741cfbab7d6f"
PR = 258
ISSUE = 252
TARGETED_RUN = 33758202351
STATIC_RUN = 33758758911
LINUX_RUN = 33758758877
LINUX_JOB = 100659542227
LINUX_RESULT = "PASS=30 FAIL=0 SKIP=0"
NEXT_ISSUE = 253


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    (ROOT / path).write_text(content.rstrip() + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one exact match, found {count}: {old[:80]!r}")
    write(path, text.replace(old, new, 1))


def replace_regex_once(path: str, pattern: str, replacement: str) -> None:
    text = read(path)
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f"{path}: expected one regex match, found {count}: {pattern!r}")
    write(path, updated)


# README current-state summary.
replace_once(
    "README.md",
    "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE: R3-A inventory is DONE and R3-B1 front-matter evidence hardening is ACTIVE through issue #252.**",
    "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE: R3-A and R3-B1 are DONE; R3-B2 normative proof-state/coverage hardening is ACTIVE through issue #253.**",
)
replace_once(
    "README.md",
    "R2 closed through B5/PR #249 at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` and its control plane was reconciled at `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-A then classified the current standards/test/language/proof gaps without changing normative semantics. Its source baseline remains green under Static `33747658673` and Linux `33747658602` = `PASS=30 FAIL=0 SKIP=0`. The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.",
    f"R2 closed through B5/PR #249 at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` and its control plane was reconciled at `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-A classified the remaining standards/test/language/proof gaps. R3-B1 then closed front-matter evidence truthfulness through PR #{PR} at `{CLOSURE_SHA}`: Static `{STATIC_RUN}` passed, Linux `{LINUX_RUN}` passed `{LINUX_RESULT}`, and the enforced negative fixture was rejected on `dedication.position.start`. No normative rule, locator, tolerance or proof-state policy changed. R3-B2/#253 is now active. The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.",
)
replace_once(
    "README.md",
    "R3-A is complete; `docs/R3-HARDENING-INVENTORY.md` records the evidence gaps and issues #252–#256 define the bounded R3 sequence. R3-B1 is active.",
    "R3-A and R3-B1 are complete; `docs/R3-HARDENING-INVENTORY.md` records the resolved B1 findings and the remaining evidence gaps. R3-B2/#253 is active; issues #254–#256 remain ordered after it.",
)
replace_once(
    "README.md",
    "R3-A/#250 is complete and the active hardening lot is R3-B1/#252; issues #253–#256 define the remaining R3 sequence.",
    f"R3-A/#250 and R3-B1/#252 are complete. B1 merged through PR #{PR} at `{CLOSURE_SHA}` after Static `{STATIC_RUN}` and Linux `{LINUX_RUN}` = `{LINUX_RESULT}`; R3-B2/#253 is active and issues #254–#256 define the remaining R3 sequence.",
)

# Bootstrap/control rules.
replace_once(
    "AGENTS.md",
    "- R3-B1/#252 is ACTIVE and owns front-matter evidence truthfulness/fail-closed enforcement. R3-B2/#253, B3/#254, B4/#255, and B5/#256 remain ordered and pending.",
    f"- R3-B1/#252 is DONE through PR #{PR} at `{CLOSURE_SHA}`. Static `{STATIC_RUN}` and Linux `{LINUX_RUN}` passed, with Linux `{LINUX_RESULT}`; the deliberate front-matter negative fixture was rejected on `dedication.position.start`. R3-B2/#253 is ACTIVE; B3/#254, B4/#255, and B5/#256 remain ordered and pending.",
)
replace_once(
    "AGENTS.md",
    "- Repair fixture/observer defects before changing runtime behavior in response to an audit finding. An aggregate PASS must not be treated as proof when its proof-contributing evidence contains an unclassified FAIL/UNASSESSED record.",
    "- R3-B1 established the front-matter invariant: proof-contributing evidence is enforced, while spacing and natural-wrap alignment use distinct observers. Keep the general fail-closed rule: an aggregate PASS must not be treated as proof when proof-contributing evidence contains an unclassified FAIL/UNASSESSED record.",
)

# Architecture status and the permanent B1 invariant.
replace_once(
    "docs/ARCHITECTURE.md",
    "R3-A is DONE from `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5` and R3-B1/#252 is active. The R3 architecture work is evidence hardening: B1 front matter, B2 proof-state/coverage, B3 semantic test/residual scope, B4 engineering-language/contracts, and B5 closeout/R4 entry.",
    f"R3-A is DONE from `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-B1/#252 is DONE through PR #{PR} at `{CLOSURE_SHA}` after Static `{STATIC_RUN}` and Linux `{LINUX_RUN}` = `{LINUX_RESULT}`; front-matter proof-contributing evidence is now fail-closed and includes deliberate negative rejection. R3-B2/#253 is active. The remaining R3 architecture work is proof-state/coverage, semantic test/residual scope, engineering-language/contracts, and closeout/R4 entry.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "A validation producer must declare whether its observations contribute proof or are audit/support-only. Proof-contributing normative FAIL cannot coexist with a successful owning gate. Test generators must fail closed when a requested semantic variation was not actually applied. Permanent residual/language checks must cover project-owned engineering sources that can affect runtime or test behavior while exempting only explicit migration documentation, negative tests, rendered academic content, and genuine upstream boundaries.",
    "A validation producer must declare whether its observations contribute proof or are audit/support-only. Proof-contributing normative FAIL cannot coexist with a successful owning gate. R3-B1 made this invariant executable for front matter: proof-contributing runners enforce their findings, pagination retains its intrinsic fail-closed path, optional-list and TOC evidence expose explicit enforcement, alignment is measured only from natural wrapping, and a deliberately invalid dedication must be rejected. Test generators must fail closed when a requested semantic variation was not actually applied. Permanent residual/language checks must cover project-owned engineering sources that can affect runtime or test behavior while exempting only explicit migration documentation, negative tests, rendered academic content, and genuine upstream boundaries.",
)

# Language policy remains B4-owned; only the current stage is reconciled.
replace_once(
    "docs/ENGINEERING-LANGUAGE.md",
    "Permanent enforcement must be scoped so valid Brazilian academic content is not confused with engineering nomenclature. R2-B5 made `tests/checks/v3_api_residual.py` part of the permanent static contract, but R3-A proved that current enforcement is incomplete: path checks do not yet police project-owned technical comments/diagnostics/UI, front-matter scripts still contain Portuguese technical diagnostics, and some machine scenario/profile identifiers remain Portuguese. R3-B4/#255 owns the scoped permanent enforcement repair. The final invariants remain: zero Portuguese project-owned technical paths, zero removed Portuguese project API in runtime or behavior-affecting engineering generators, zero Portuguese project-owned technical comments or diagnostics/UI, zero canonical examples using removed API, and zero archive/museum directories in the active tree. Rendered academic Portuguese, official wording, bibliography data, literal output under test, and genuine upstream identifiers remain protected content/boundaries.",
    "Permanent enforcement must be scoped so valid Brazilian academic content is not confused with engineering nomenclature. R2-B5 made `tests/checks/v3_api_residual.py` part of the permanent static contract, and R3-A proved that current enforcement is incomplete: path checks do not yet police all project-owned technical comments/diagnostics/UI, and some machine scenario/profile identifiers remain Portuguese. R3-B1 repaired behavior-affecting front-matter generator/observer defects needed for truthful evidence but deliberately did not absorb the broader language-policy cleanup. R3-B4/#255 still owns the scoped permanent enforcement repair; R3-B2/#253 is the current stage. The final invariants remain: zero Portuguese project-owned technical paths, zero removed Portuguese project API in runtime or behavior-affecting engineering generators, zero Portuguese project-owned technical comments or diagnostics/UI, zero canonical examples using removed API, and zero archive/museum directories in the active tree. Rendered academic Portuguese, official wording, bibliography data, literal output under test, and genuine upstream identifiers remain protected content/boundaries.",
)

# CTAN remains future work; only the development gate advances.
replace_regex_once(
    "docs/CTAN-RELEASE.md",
    r"- Development gate: V3-R2 runtime/API migration is complete through B5/PR #249 at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` and its canonical closeout baseline is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`\. R3-A/#250 is complete and R3-B1/#252 is active; B2–B5 remain required before R4\. A v3\.0\.0 CTAN upload must not be performed during R3: publication remains a later explicit action after R3 hardening, R4 certification, and R5 foundation freeze/final documentation reach the roadmap's release-ready state and the intended candidate is revalidated proportionally\.",
    f"- Development gate: V3-R2 runtime/API migration is complete through B5/PR #249 at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` and its canonical closeout baseline is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-A/#250 and R3-B1/#252 are complete; B1 merged through PR #{PR} at `{CLOSURE_SHA}` with `{LINUX_RESULT}`. R3-B2/#253 is active and B3–B5 remain required before R4. A v3.0.0 CTAN upload must not be performed during R3: publication remains a later explicit action after R3 hardening, R4 certification, and R5 foundation freeze/final documentation reach the roadmap's release-ready state and the intended candidate is revalidated proportionally.",
)

roadmap = f"""# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-03

## Status

**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 ACTIVE.**

R3-A inventory source is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-B1/#252 closed through PR #{PR}: implementation head `{IMPLEMENTATION_HEAD}`, squash-merged main `{CLOSURE_SHA}`. Focused enforcement run `{TARGETED_RUN}` passed; PR Static `{STATIC_RUN}` passed; Linux integration `{LINUX_RUN}` / job `{LINUX_JOB}` passed `{LINUX_RESULT}`. The deliberate negative front-matter fixture was rejected on `dedication.position.start`. No normative rule ID, expected value, locator, tolerance, applicability, or proof-state policy changed. Active implementation issue: #253. Machine authority: `release/v3-roadmap.json`.

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
| R3-B1 | DONE | issue #252; PR #{PR} → `{CLOSURE_SHA}` | front-matter observers/generators repaired; proof-contributing evidence fail-closed; negative rejection proven | None |
| R3-B2 | ACTIVE | issue #253; entry `{CLOSURE_SHA}` | harden normative proof-state and coverage semantics | classify 17 manual/conditional rules; distinguish enforced, bounded-positive, conditional/manual and support-only evidence |
| R3-B3 | PENDING | issue #254 | semantic test integrity + expanded residual enforcement | after B2 |
| R3-B4 | PENDING | issue #255 | engineering-language enforcement + contract consolidation | after B3 |
| R3-B5 | PENDING | issue #256 | R3 closeout and immutable R4 entry | after B4 |
| V3-R4 | BLOCKED | — | final certification | after R3-B5 |
| V3-R5 | BLOCKED | — | foundation freeze and final docs | after R4 |
| V3-A1/A2 | BLOCKED | — | scientific-article work | after certified foundation |
| CTAN submission | FUTURE | explicit release action | no upload yet | release-ready stage only |

## R3-B1 closeout

B1 repaired the evidence model before considering runtime changes. The approval matrix now exercises the intended six canonical v3 types rather than relying on a stale v2 substitution. Summary paragraph counting recognizes `\\ufcSummaryKeywords`. Title-page/approval markers were shortened to survive PDF extraction, dedication spacing fixtures no longer create accidental physical-line wrapping, and short-epigraph geometry coalesces extractor fragments without relaxing the normative tolerance.

Spacing and alignment are now intentionally separated: explicit-line fixtures prove spacing while natural-wrap fixtures prove justification. Proof-contributing front-matter runners execute enforced semantics; optional-list and TOC checkers expose enforcement explicitly, while pagination retains its pre-existing intrinsic fail-closed behavior. The negative fixture deliberately places the dedication above its permitted start and the gate proves rejection at `dedication.position.start`.

The full PR gate passed all 30 integration checks. The R3-A front-matter findings are therefore resolved as observer/generator/enforcement defects, not as evidence requiring a normative or runtime-format change.

## R3-B2 entry

The baseline remains 19 sources and 181 active rules: 164 currently classified automatic and 17 manual/conditional, with 11 project-policy/technical-profile rules, 32 runner gates, 10 registered evidence checks and 9 validator checks. B1 makes front-matter enforcement trustworthy but does not by itself prove that the aggregate coverage vocabulary distinguishes enforcement from mere observation.

B2/#253 must inventory all 17 manual/conditional rules, audit every `automatic-partial` rule, reconcile strict traceability/proof-state/evidence registries, and expose coverage counts that do not call a rule covered merely because a named check ran. Source authority, precedence, rule IDs, expected values, tolerances, locators and applicability stay fixed absent new current normative evidence.

## Immediate action

Execute **R3-B2 / issue #253** from `{CLOSURE_SHA}`. Start with source-only inventory and targeted normative/validator checks. Use `make check` before merge only if integration evidence semantics are touched, and `make release-check` only if release-only proof-state behavior changes.
"""
write("docs/ROADMAP-V3.0.0.md", roadmap)

handoff = f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- R2 product closure: `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`; merged-main release run `33745603468` = `PASS=32 FAIL=0 SKIP=0`.
- R2 closeout / R3-A inventory source: `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`.
- R3-A/#250: **DONE**.
- R3-B1/#252: **DONE** through PR #{PR}.
- R3-B1 implementation head: `{IMPLEMENTATION_HEAD}`.
- R3-B1 closure/main SHA: `{CLOSURE_SHA}`.
- R3-B1 focused enforcement run: `{TARGETED_RUN}` — PASS, including deliberate rejection of `dedication.position.start`.
- R3-B1 PR gates: Static `{STATIC_RUN}` PASS; Linux `{LINUX_RUN}` / job `{LINUX_JOB}` = `{LINUX_RESULT}`.
- Active phase: **V3-R3**.
- Active stage: **R3-B2 — normative proof-state and coverage semantics hardening**.
- Active issue: **#253**.
- R3 inventory: `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## What R3-B1 established

Front-matter proof evidence is now fail-closed. B1 fixed the stale approval-profile generator, canonical summary keyword observation, extraction-sensitive title/approval markers, dedication spacing fixture behavior, and short-epigraph extractor fragmentation. It separated explicit-line spacing evidence from natural-wrap alignment evidence, enforced proof-contributing front-matter checkers, preserved pagination's intrinsic fail-closed behavior, and added a negative fixture that must be rejected.

The final PR integration gate passed all 30 checks. The changes did not modify normative source authority, rule IDs, expected values, locators, tolerances, applicability, runtime API, or proof-state policy.

## R3 lots

| Lot | Issue | Status | Purpose |
|---|---:|---|---|
| R3-B1 | #252 | DONE | front-matter evidence truthfulness and fail-closed enforcement |
| R3-B2 | #253 | ACTIVE | normative proof-state and coverage semantics |
| R3-B3 | #254 | PENDING | semantic test integrity and expanded residual enforcement |
| R3-B4 | #255 | PENDING | engineering-language enforcement and closed-contract consolidation |
| R3-B5 | #256 | PENDING | R3 closeout and exact R4 entry |

## Immediate action

Execute issue #253 from `{CLOSURE_SHA}`. Inventory all 17 manual/conditional rules, audit `automatic-partial` proof claims, reconcile strict traceability with the proof/evidence registries, and make coverage metrics distinguish enforced automatic evidence, bounded positive evidence, conditional/manual evidence and support-only observations without changing normative meaning.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, values, locators, tolerances, applicability or proof state without current evidence. `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` stay unchanged unless source/currency facts change. Do not start R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission during R3-B2 through R3-B4. Literal Windows-font certification remains R4-owned.
"""
write("docs/HANDOFF-V3.0.0.md", handoff)

inventory_doc = f"""# R3 Hardening Inventory

Updated: 2026-09-03

## Purpose

R3 hardens the truthfulness of the v3 foundation before final certification. The original R3-A inventory was taken from `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`; its baseline had 19 sources, 181 rules, 164 automatic rules, 17 manual/conditional rules, 11 project-policy/technical-profile rules, 32 runner gates, 10 registered evidence checks and 9 validator checks.

R3-B1/#252 is now closed through PR #{PR} at `{CLOSURE_SHA}`. R3-B2/#253 is active.

## R3-B1 closeout evidence

- implementation head: `{IMPLEMENTATION_HEAD}`;
- focused enforced front-matter run: `{TARGETED_RUN}` — PASS;
- PR Static contract: `{STATIC_RUN}` — PASS;
- PR Linux integration: `{LINUX_RUN}` / job `{LINUX_JOB}` — `{LINUX_RESULT}`;
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
| Summary canonical keyword macro not recognized | Source paragraph observer recognizes canonical `\\ufcSummaryKeywords` while retaining the genuine upstream `\\keywords` boundary. |
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
| R3-B1/#252 | DONE | PR #{PR} → `{CLOSURE_SHA}`; `{LINUX_RESULT}` |
| R3-B2/#253 | ACTIVE | entry `{CLOSURE_SHA}` |
| R3-B3/#254 | PENDING | after B2 |
| R3-B4/#255 | PENDING | after B3 |
| R3-B5/#256 | PENDING | after B4; closes R3 and records immutable R4 entry |

## R3-B2 entry contract

B2 must not equate `validation.checks` membership with enforcement. It must inventory the 17 manual/conditional rules, audit every `automatic-partial` rule, reconcile `normative_traceability --strict-evidence` with the proof-state and evidence registries, and expose coverage classes that distinguish enforced automatic evidence, bounded-positive evidence, conditional/manual evidence, and support-only observation where the current schemas permit.

No source/currency fact changed in B1, so `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` remain intentionally unchanged. The R2 migration guide also remains unchanged because B1 changed no public runtime API.
"""
write("docs/R3-HARDENING-INVENTORY.md", inventory_doc)

# Canonical machine roadmap.
roadmap_path = ROOT / "release/v3-roadmap.json"
roadmap_data = json.loads(roadmap_path.read_text(encoding="utf-8"))
roadmap_data["updated_at"] = "2026-09-03"
roadmap_data["phase"] = "V3-R3"
roadmap_data["stage"] = "R3-B2"
roadmap_data["stage_name"] = "normative proof-state and coverage semantics hardening"
roadmap_data["active_branch"] = "main"
roadmap_data["next_action"] = (
    f"Execute V3-R3/R3-B2 issue #{NEXT_ISSUE} from {CLOSURE_SHA}: classify all 17 manual/conditional rules, "
    "audit automatic-partial proof claims, reconcile strict traceability with proof/evidence registries, and make coverage metrics distinguish enforcement from support-only observation without changing normative meaning."
)
roadmap_data["active_implementation_lot"] = {
    "stage": "R3-B2",
    "issue": NEXT_ISSUE,
    "entry_product_main_sha": CLOSURE_SHA,
    "status": "ACTIVE",
    "implementation_branch_rule": "branch from the merged R3-B1 fail-closed evidence checkpoint",
}
r3 = roadmap_data["r3"]
r3["status"] = "ACTIVE"
r3["stage"] = "R3-B2"
r3["stage_name"] = "normative proof-state and coverage semantics hardening"
r3["issue"] = NEXT_ISSUE
r3["next_issue"] = NEXT_ISSUE
r3["lots"]["R3-B1"].update({
    "status": "DONE",
    "implementation_head_sha": IMPLEMENTATION_HEAD,
    "pr": PR,
    "merge_main_sha": CLOSURE_SHA,
    "focused_enforcement_run_id": TARGETED_RUN,
    "static_contract_run_id": STATIC_RUN,
    "linux_integration_run_id": LINUX_RUN,
    "linux_integration_job_id": LINUX_JOB,
    "linux_integration_result": LINUX_RESULT,
    "negative_rejection_rule": "dedication.position.start",
    "proof_contributing_frontmatter_fail_closed": True,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
})
r3["lots"]["R3-B2"].update({
    "status": "ACTIVE",
    "entry_product_main_sha": CLOSURE_SHA,
})
roadmap_data["r3_b1_closeout"] = {
    "status": "DONE",
    "issue": ISSUE,
    "pr": PR,
    "entry_main_sha": "9bc2861d581c5562bcb1791a3ca294506298a911",
    "implementation_head_sha": IMPLEMENTATION_HEAD,
    "merge_main_sha": CLOSURE_SHA,
    "focused_enforcement_run_id": TARGETED_RUN,
    "static_contract_run_id": STATIC_RUN,
    "linux_integration_run_id": LINUX_RUN,
    "linux_integration_job_id": LINUX_JOB,
    "linux_integration_result": LINUX_RESULT,
    "positive_frontmatter_findings_unresolved": 0,
    "negative_rejection_rule": "dedication.position.start",
    "explicit_enforced_frontmatter_runners": 10,
    "pagination_intrinsic_fail_closed": True,
    "runtime_api_changed": False,
    "normative_semantics_changed": False,
    "locator_policy_changed": False,
    "reference_tolerances_changed": False,
    "proof_state_changed": False,
}
roadmap_path.write_text(json.dumps(roadmap_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Living R3 inventory: preserve R3-A provenance and mark B1 findings resolved.
inv_path = ROOT / "release/v3-r3-inventory.json"
inv = json.loads(inv_path.read_text(encoding="utf-8"))
inv["stage"] = "R3-B2"
inv["status"] = "ACTIVE"
inv["reviewed_at"] = "2026-09-03"
inv["r3_a_source_main_sha"] = inv.get("source_main_sha")
inv["current_entry_main_sha"] = CLOSURE_SHA
resolutions = {
    "frontmatter-audit-not-enforced": "Proof-contributing front-matter evidence is enforced; pagination retains intrinsic fail-closed behavior.",
    "approval-profile-generator-stale-v2-substitution": "Canonical type variants are generated and asserted before compilation.",
    "summary-canonical-keyword-macro-not-recognized": "Canonical \\ufcSummaryKeywords is recognized by source paragraph observation.",
    "dedication-spacing-discrepancy": "Fixture marker wrapping caused the doubled gap; controlled markers now match calibrated spacing.",
    "short-epigraph-alignment-discrepancy": "Extractor fragments are geometrically coalesced; natural-wrap alignment passes without tolerance relaxation.",
    "title-approval-marker-discrepancies": "Short extraction-stable markers prove title/approval order and the intended academic/project profile behavior.",
}
for finding in inv["findings"]:
    if finding["id"] in resolutions:
        finding["status"] = "RESOLVED"
        finding["resolved_by"] = "R3-B1"
        finding["resolution"] = resolutions[finding["id"]]
        finding["closure_sha"] = CLOSURE_SHA
    else:
        finding.setdefault("status", "OPEN")
inv["lots"]["R3-B1"].update({
    "status": "DONE",
    "pr": PR,
    "implementation_head_sha": IMPLEMENTATION_HEAD,
    "merge_main_sha": CLOSURE_SHA,
    "focused_enforcement_run_id": TARGETED_RUN,
    "static_contract_run_id": STATIC_RUN,
    "linux_integration_run_id": LINUX_RUN,
    "linux_integration_result": LINUX_RESULT,
})
inv["lots"]["R3-B2"].update({
    "status": "ACTIVE",
    "entry_product_main_sha": CLOSURE_SHA,
})
inv["r3_b1_closeout"] = {
    "issue": ISSUE,
    "pr": PR,
    "implementation_head_sha": IMPLEMENTATION_HEAD,
    "merge_main_sha": CLOSURE_SHA,
    "focused_enforcement_run_id": TARGETED_RUN,
    "static_contract_run_id": STATIC_RUN,
    "linux_integration_run_id": LINUX_RUN,
    "linux_integration_job_id": LINUX_JOB,
    "linux_integration_result": LINUX_RESULT,
    "negative_rejection_rule": "dedication.position.start",
    "unresolved_positive_frontmatter_findings": 0,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
}
inv["next_stage"] = "R3-B2"
inv["next_issue"] = NEXT_ISSUE
inv_path.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Guard documents whose facts were intentionally unchanged.
for path in (
    "docs/NORMATIVE-BASE.md",
    "docs/NORMATIVE-CURRENCY.md",
    "docs/MIGRATING-TO-V3.md",
):
    if not (ROOT / path).is_file():
        raise SystemExit(f"required unchanged document missing: {path}")

print("R3-B1 closeout documentation reconciled; R3-B2 is active.")
