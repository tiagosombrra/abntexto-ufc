#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

B2_ENTRY = "32c3221c813790e938ffb29d1f4ee55c2812c47d"
B2_HEAD = "55a833fc17daddc2526c4f42e6830470de6df873"
B2_MERGE = "1d9e6373ed674fb7503b968b3e852e4be5fc14ea"
B2_INVENTORY_RUN = 33764122865
B2_INDEPENDENT_RUN = 33768364069
B2_STATIC_RUN = 33768911131
B2_LINUX_RUN = 33768911126
B2_LINUX_JOB = 100694266254
B2_RELEASE_RUN = 33772854355
B2_RESULT = "PASS=31 FAIL=0 SKIP=0"
B2_CONTRIBUTION = {
    "rules": 181,
    "automatic_declared": 164,
    "automatic_partial": 113,
    "automatic_partial_bounded_positive": 113,
    "enforced_automatic": 37,
    "support_only": 14,
    "conditional_review": 10,
    "manual_review": 6,
    "not_applicable": 1,
    "automation_gap": 0,
}


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"required replacement not found: {label}")
    return text.replace(old, new)


def replace_section(text: str, start: str, replacement: str) -> str:
    idx = text.find(start)
    if idx < 0:
        raise SystemExit(f"section not found: {start}")
    return text[:idx] + replacement.rstrip() + "\n"


# ROADMAP
path = "docs/ROADMAP-V3.0.0.md"
text = read(path)
text = replace_required(
    text,
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 ACTIVE.**",
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 DONE; R3-B3 ACTIVE.**",
    "roadmap status",
)
intro_pattern = re.compile(r"R3-A inventory source is .*?Machine authority: `release/v3-roadmap\.json`\.", re.S)
intro = (
    f"R3-A inventory source is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. "
    f"R3-B1/#252 closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. "
    f"R3-B2/#253 closed through PR #260: final implementation head `{B2_HEAD}`, squash-merged main `{B2_MERGE}`. "
    f"Inventory run `{B2_INVENTORY_RUN}` found 113 `automatic-partial` rules, 94 with direct owner evidence and 19 ownership/evidence gaps. "
    f"Independent full validation `{B2_INDEPENDENT_RUN}` and PR Linux `{B2_LINUX_RUN}` / job `{B2_LINUX_JOB}` both passed `{B2_RESULT}`; PR Static `{B2_STATIC_RUN}` passed. "
    "The final contribution gate classified all 113/113 `automatic-partial` rules as bounded-positive with zero automation gaps, while preserving conservative proof states. "
    "No normative rule ID, expected value, locator, tolerance, applicability, source authority/precedence, proof-state default, or public runtime API changed. "
    "Active implementation issue: #254. Machine authority: `release/v3-roadmap.json`."
)
text, count = intro_pattern.subn(intro, text, count=1)
if count != 1:
    raise SystemExit("roadmap intro replacement failed")
text = replace_required(
    text,
    "| R3-B2 | ACTIVE | issue #253; entry `afb9f16403aafd8752a0aa8b0713f85c41204d1b` | harden normative proof-state and coverage semantics | classify 17 manual/conditional rules; distinguish enforced, bounded-positive, conditional/manual and support-only evidence |",
    f"| R3-B2 | DONE | issue #253; PR #260 → `{B2_MERGE}` | 17 non-automatic rules classified; 113/113 `automatic-partial` bounded-positive; explicit enforced/support-only semantics | None |",
    "roadmap B2 row",
)
text = replace_required(
    text,
    "| R3-B3 | PENDING | issue #254 | semantic test integrity + expanded residual enforcement | after B2 |",
    f"| R3-B3 | ACTIVE | issue #254; entry `{B2_MERGE}` | semantic test integrity + expanded residual enforcement | audit generators/check semantics; expand fail-closed residual scope; couple positive/negative evidence |",
    "roadmap B3 row",
)
replacement = f"""## R3-B2 closeout

B2 repaired the distinction between traceable mechanisms, current-run rule-specific contribution, and conservative proof state. The 17 non-automatic rules are explicitly classified as 10 `conditional-review`, 6 `manual-review`, and 1 `not-applicable`; none was promoted merely because a related gate was green.

The coordinated contribution gate now runs after complete validation and intersects current-run structured evidence with each rule's declared owners. The final PR run closed with 181 rules: 113/113 `automatic-partial` as `bounded-positive`, 37 `enforced-automatic`, 14 `support-only`, 10 `conditional-review`, 6 `manual-review`, 1 `not-applicable`, and zero `automation-gap`. `bounded-positive` remains `PARTIAL`, not `PROVEN`.

B2 entered from `{B2_ENTRY}`, used inventory run `{B2_INVENTORY_RUN}`, and merged through PR #260 at `{B2_MERGE}`. Static `{B2_STATIC_RUN}` passed; Linux integration `{B2_LINUX_RUN}` / job `{B2_LINUX_JOB}` and independent validation `{B2_INDEPENDENT_RUN}` both passed `{B2_RESULT}`. Source authority, precedence, rule IDs, expected values, tolerances, locators, applicability, proof-state defaults and public runtime API were unchanged.

## R3-B3 entry

R3-B3/#254 starts from `{B2_MERGE}`. It must prove that active test/generator labels correspond to real semantic variation and expand the permanent removed-v2 residual contract across behavior-affecting project-owned engineering surfaces. The lot audits `.sh`, `.py`, workflows, machine JSON/tool surfaces, generator substitutions, duplicate/orphan/support-only checks, and positive/negative rule-ID coupling while preserving explicit migration records, negative tests, rendered academic content and genuine upstream boundaries.

B3 gates are proportional but fail closed: `make static-check` must include the expanded residual contract, each repaired generator gets a focused semantic assertion, and full `make check` is required before merge.

## Immediate action

Execute **R3-B3 / issue #254** from `{B2_MERGE}`. Start with the generator/residual-scope inventory, then repair bounded semantic no-op risks and extend permanent residual enforcement. Do not start R3-B4, R3-B5, R4, R5, V3-A1/A2, or CTAN submission before their recorded entry conditions.
"""
text = replace_section(text, "## R3-B2 entry", replacement)
write(path, text)

# HANDOFF: canonical continuation point is easier to keep exact by rewriting the bounded handoff.
write("docs/HANDOFF-V3.0.0.md", f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- R2 product closure: `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`; merged-main release run `33745603468` = `PASS=32 FAIL=0 SKIP=0`.
- R2 closeout / R3-A inventory source: `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`.
- R3-A/#250: **DONE**.
- R3-B1/#252: **DONE** through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`.
- R3-B2/#253: **DONE** through PR #260.
- R3-B2 entry checkpoint: `{B2_ENTRY}`.
- R3-B2 implementation head: `{B2_HEAD}`.
- R3-B2 closure/main SHA: `{B2_MERGE}`.
- R3-B2 inventory run: `{B2_INVENTORY_RUN}` — 113 `automatic-partial`, 94 direct-owner evidence, 19 ownership/evidence gaps, unsafe `PROVEN` = 0.
- R3-B2 independent full validation: `{B2_INDEPENDENT_RUN}` — `{B2_RESULT}`.
- R3-B2 PR gates: Static `{B2_STATIC_RUN}` PASS; Linux `{B2_LINUX_RUN}` / job `{B2_LINUX_JOB}` = `{B2_RESULT}`.
- R3-B2 final contribution: 181 rules; 113/113 `automatic-partial` bounded-positive; 37 enforced-automatic; 14 support-only; 10 conditional-review; 6 manual-review; 1 not-applicable; automation-gap = 0.
- Post-merge technical release run: `{B2_RELEASE_RUN}` — recorded as the current-state release gate for `{B2_MERGE}`; its final conclusion must be green before this closeout PR is merged.
- Active phase: **V3-R3**.
- Active stage: **R3-B3 — semantic test integrity and expanded residual enforcement**.
- Active issue: **#254**.
- R3 inventory: `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.

Git facts, `release/v3-roadmap.json`, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## What R3-B2 established

A named or green validation mechanism is no longer treated as proof by association. Complete coordinated runs now classify current-run rule-specific contribution against declared evidence owners. Every `automatic-partial` rule must produce a current rule-specific PASS from a declared owner or the contribution gate fails closed with `automation-gap`.

The 17 non-automatic rules are individually justified. The final runtime projection is 37 `enforced-automatic` + 113 `bounded-positive` + 14 `support-only` = 164 automatic declarations, with 10 conditional reviews, 6 manual reviews and 1 not-applicable rule. This projection does not alter the proof-state baseline: bounded-positive rules remain `PARTIAL`; support-only observations are not enforcement.

No normative source authority, precedence, rule ID, expected value, locator, tolerance, applicability, proof-state default, rendered-format requirement, or public runtime API changed in B2.

## R3 lots

| Lot | Issue | Status | Purpose |
|---|---:|---|---|
| R3-B1 | #252 | DONE | front-matter evidence truthfulness and fail-closed enforcement |
| R3-B2 | #253 | DONE | normative proof-state and coverage semantics |
| R3-B3 | #254 | ACTIVE | semantic test integrity and expanded residual enforcement |
| R3-B4 | #255 | PENDING | engineering-language enforcement and closed-contract consolidation |
| R3-B5 | #256 | PENDING | R3 closeout and exact R4 entry |

## Immediate action

Execute issue #254 from `{B2_MERGE}`. Audit fixture/test generators for substitutions and semantic no-ops, add fail-closed assertions that generated variants actually differ and use canonical v3 values, expand removed-v2 residual scanning to behavior-affecting project-owned shell/Python/workflow/JSON/tool surfaces, inventory duplicate/orphan/support-only/label-behavior mismatches, and keep positive/negative evidence coupled to the same rule IDs.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, values, locators, tolerances, applicability or proof state without current evidence. `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` stay unchanged unless source/currency facts change. `docs/MIGRATING-TO-V3.md` stays unchanged unless the public API changes. Do not start R3-B4/B5, R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission before their recorded entry conditions. Literal Windows-font certification remains R4-owned.
""")

# README bounded status updates.
path = "README.md"
text = read(path)
text = replace_required(
    text,
    "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE: R3-A and R3-B1 are DONE; R3-B2 normative proof-state/coverage hardening is ACTIVE through issue #253.**",
    "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE: R3-A, R3-B1 and R3-B2 are DONE; R3-B3 semantic test integrity/residual hardening is ACTIVE through issue #254.**",
    "README status",
)
pattern = re.compile(r"R2 closed through B5/PR #249.*?final Windows/literal-font recertification remains R4-owned\.", re.S)
para = (
    f"R2 closed through B5/PR #249 at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` and its control plane was reconciled at `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. "
    f"R3-A classified the remaining foundation gaps; R3-B1 closed front-matter evidence truthfulness through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. "
    f"R3-B2/#253 then closed through PR #260 at `{B2_MERGE}`: Static `{B2_STATIC_RUN}` passed and Linux `{B2_LINUX_RUN}` passed `{B2_RESULT}` with 113/113 `automatic-partial` rules contributing bounded-positive evidence and zero automation gaps. "
    "No normative semantics, proof-state defaults or public runtime API changed. R3-B3/#254 is active. "
    "The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned."
)
text, count = pattern.subn(para, text, count=1)
if count != 1:
    raise SystemExit("README status paragraph replacement failed")
text = text.replace(
    "R3-A and R3-B1 are complete; `docs/R3-HARDENING-INVENTORY.md` records the resolved B1 findings and the remaining evidence gaps. R3-B2/#253 is active; issues #254–#256 remain ordered after it.",
    "R3-A, R3-B1 and R3-B2 are complete; `docs/R3-HARDENING-INVENTORY.md` records the resolved evidence findings and remaining lots. R3-B3/#254 is active; issues #255–#256 remain ordered after it.",
)
text = text.replace(
    "R3-A/#250 and R3-B1/#252 are complete. B1 merged through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b` after Static `33758758911` and Linux `33758758877` = `PASS=30 FAIL=0 SKIP=0`; R3-B2/#253 is active and issues #254–#256 define the remaining R3 sequence.",
    f"R3-A/#250, R3-B1/#252 and R3-B2/#253 are complete. B2 merged through PR #260 at `{B2_MERGE}` after Static `{B2_STATIC_RUN}` and Linux `{B2_LINUX_RUN}` = `{B2_RESULT}`; R3-B3/#254 is active and issues #255–#256 define the remaining R3 sequence.",
)
write(path, text)

# AGENTS current control rules.
path = "AGENTS.md"
text = read(path)
old = "- R3-B1/#252 is DONE through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. Static `33758758911` and Linux `33758758877` passed, with Linux `PASS=30 FAIL=0 SKIP=0`; the deliberate front-matter negative fixture was rejected on `dedication.position.start`. R3-B2/#253 is ACTIVE; B3/#254, B4/#255, and B5/#256 remain ordered and pending."
new = (
    "- R3-B1/#252 is DONE through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. Static `33758758911` and Linux `33758758877` passed, with Linux `PASS=30 FAIL=0 SKIP=0`; the deliberate front-matter negative fixture was rejected on `dedication.position.start`.\n"
    f"- R3-B2/#253 is DONE through PR #260 at `{B2_MERGE}`. Static `{B2_STATIC_RUN}` passed; Linux `{B2_LINUX_RUN}` / job `{B2_LINUX_JOB}` and independent validation `{B2_INDEPENDENT_RUN}` passed `{B2_RESULT}`. Final contribution was 113/113 `automatic-partial` bounded-positive, 37 enforced-automatic, 14 support-only, 10 conditional-review, 6 manual-review, 1 not-applicable, zero automation gaps. R3-B3/#254 is ACTIVE; B4/#255 and B5/#256 remain ordered and pending."
)
text = replace_required(text, old, new, "AGENTS R3 status")
text = replace_required(
    text,
    "- R3-B1 established the front-matter invariant: proof-contributing evidence is enforced, while spacing and natural-wrap alignment use distinct observers. Keep the general fail-closed rule: an aggregate PASS must not be treated as proof when proof-contributing evidence contains an unclassified FAIL/UNASSESSED record.",
    "- R3-B1 established the front-matter fail-closed invariant. R3-B2 generalized evidence truthfulness: mechanism traceability, current rule-specific contribution and conservative proof state are distinct; `automatic-partial` contribution must come from a declared owner, `bounded-positive` is not `PROVEN`, and support-only evidence is never counted as enforcement.",
    "AGENTS invariant",
)
write(path, text)

# ARCHITECTURE status and R3 semantics.
path = "docs/ARCHITECTURE.md"
text = read(path)
old = "R3-A is DONE from `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-B1/#252 is DONE through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b` after Static `33758758911` and Linux `33758758877` = `PASS=30 FAIL=0 SKIP=0`; front-matter proof-contributing evidence is now fail-closed and includes deliberate negative rejection. R3-B2/#253 is active. The remaining R3 architecture work is proof-state/coverage, semantic test/residual scope, engineering-language/contracts, and closeout/R4 entry."
new = f"R3-A is DONE from `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-B1/#252 is DONE through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 is DONE through PR #260 at `{B2_MERGE}` after Static `{B2_STATIC_RUN}` and Linux `{B2_LINUX_RUN}` = `{B2_RESULT}`; complete runs now distinguish declared mechanisms, current rule-specific contribution and conservative proof state, with 113/113 `automatic-partial` rules bounded-positive and zero automation gaps. R3-B3/#254 is active. Remaining R3 architecture work is semantic test/residual scope, engineering-language/contracts, and closeout/R4 entry."
text = replace_required(text, old, new, "architecture current R3")
needle = "A validation producer must declare whether its observations contribute proof or are audit/support-only. Proof-contributing normative FAIL cannot coexist with a successful owning gate. R3-B1 made this invariant executable for front matter: proof-contributing runners enforce their findings, pagination retains its intrinsic fail-closed path, optional-list and TOC evidence expose explicit enforcement, alignment is measured only from natural wrapping, and a deliberately invalid dedication must be rejected. Test generators must fail closed when a requested semantic variation was not actually applied. Permanent residual/language checks must cover project-owned engineering sources that can affect runtime or test behavior while exempting only explicit migration documentation, negative tests, rendered academic content, and genuine upstream boundaries."
replacement = "A validation producer must declare whether its observations contribute proof or are audit/support-only. Proof-contributing normative FAIL cannot coexist with a successful owning gate. R3-B1 made this invariant executable for front matter. R3-B2 generalized it across the full contract: current-run rule-specific PASS evidence is intersected with declared owners; `automatic-partial` rules fail closed on `automation-gap`; `bounded-positive` remains conservative `PARTIAL`; and non-partial automatic rules without rule-specific evidence remain visible as `support-only`. Test generators must fail closed when a requested semantic variation was not actually applied. R3-B3 now owns expansion of permanent residual enforcement across project-owned engineering sources that can affect runtime or test behavior while exempting only explicit migration documentation/contracts, negative tests, rendered academic content, and genuine upstream boundaries."
text = replace_required(text, needle, replacement, "architecture R3 invariant")
write(path, text)

# ENGINEERING-LANGUAGE stage pointer only; substantive language work remains B4-owned.
path = "docs/ENGINEERING-LANGUAGE.md"
text = read(path)
text = replace_required(
    text,
    "R3-B4/#255 still owns the scoped permanent enforcement repair; R3-B2/#253 is the current stage.",
    f"R3-B4/#255 still owns the scoped permanent language-enforcement repair. R3-B2/#253 closed at `{B2_MERGE}` without broadening language policy; R3-B3/#254 is the current stage and owns engineering residual/test-integrity scope.",
    "engineering language stage",
)
write(path, text)

# CTAN release gate pointer.
path = "docs/CTAN-RELEASE.md"
text = read(path)
text = replace_required(
    text,
    "R3-A/#250 and R3-B1/#252 are complete; B1 merged through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b` with `PASS=30 FAIL=0 SKIP=0`. R3-B2/#253 is active and B3–B5 remain required before R4.",
    f"R3-A/#250, R3-B1/#252 and R3-B2/#253 are complete; B2 merged through PR #260 at `{B2_MERGE}` with Linux `{B2_LINUX_RUN}` = `{B2_RESULT}` and 113/113 `automatic-partial` rule contributions. R3-B3/#254 is active and B4–B5 remain required before R4.",
    "CTAN development gate",
)
write(path, text)

# R3 inventory: rewrite current bounded status while preserving the original R3-A baseline.
write("docs/R3-HARDENING-INVENTORY.md", f"""# R3 Hardening Inventory

Updated: 2026-09-03

## Purpose

R3 hardens the truthfulness of the v3 foundation before final certification. The original R3-A inventory was taken from `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`; its baseline had 19 sources, 181 rules, 164 automatic declarations, 17 manual/conditional rules, 11 project-policy/technical-profile rules, 32 runner gates, 10 registered evidence checks and 9 validator checks.

R3-B1/#252 is closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 is closed through PR #260 at `{B2_MERGE}`. R3-B3/#254 is active.

## R3-B1 closeout evidence

- implementation head: `347a80a8f88dd03c037ff19faf4f741cfbab7d6f`;
- focused enforced front-matter run: `33758202351` — PASS;
- PR Static contract: `33758758911` — PASS;
- PR Linux integration: `33758758877` / job `100659542227` — `PASS=30 FAIL=0 SKIP=0`;
- negative evidence: `FRONTMATTER-NEGATIVE-EVIDENCE status=PASS rejected_rule=dedication.position.start`;
- normative semantics / proof-state policy / runtime API changed: **no**.

## R3-B2 closeout evidence

- entry checkpoint: `{B2_ENTRY}`;
- final implementation head: `{B2_HEAD}`;
- merge/main SHA: `{B2_MERGE}`;
- issue / PR: #253 / #260;
- inventory run: `{B2_INVENTORY_RUN}` — 113 `automatic-partial`, 94 direct-owner contributions, 19 ownership/evidence gaps, unsafe `PROVEN` = 0;
- independent complete validation: `{B2_INDEPENDENT_RUN}` — `{B2_RESULT}`;
- PR Static contract: `{B2_STATIC_RUN}` — PASS;
- PR Linux integration: `{B2_LINUX_RUN}` / job `{B2_LINUX_JOB}` — `{B2_RESULT}`;
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
| Summary canonical keyword macro not recognized | Canonical `\\ufcSummaryKeywords` is recognized while retaining the genuine upstream `\\keywords` boundary. | R3-B1 |
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
| R3-B2/#253 | DONE | PR #260 → `{B2_MERGE}`; `{B2_RESULT}`; 113/113 bounded-positive, automation-gap=0 |
| R3-B3/#254 | ACTIVE | entry `{B2_MERGE}` |
| R3-B4/#255 | PENDING | after B3 |
| R3-B5/#256 | PENDING | after B4; closes R3 and records immutable R4 entry |

## R3-B3 entry contract

B3 must prove that test/generator labels correspond to actual semantic behavior. It audits generated profile/type substitutions and other no-op risks, adds fail-closed assertions for canonical v3 generated values, expands the permanent removed-v2 residual scan beyond LaTeX/runtime files to behavior-affecting project-owned shell/Python/workflow/JSON/tool surfaces, inventories duplicate/orphan/support-only/label-mismatched checks, and verifies that negative-path families use the same rule identifiers as positive evidence.

The permanent residual contract must exempt only narrow explicit migration documentation/contracts, deliberate negative tests, rendered academic content and genuine upstream boundaries. B3 requires `make static-check`, focused checks for repaired generators and full `make check` before merge.

No source/currency fact changed in B1 or B2, so `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` remain intentionally unchanged. The v3 migration guide also remains unchanged because B2 changed no public runtime API.
""")

# B2-specific docs retain their detailed model and receive exact closure evidence.
path = "docs/R3-B2-EVIDENCE-CONTRIBUTION.md"
text = read(path)
if "## Closeout evidence" not in text:
    text += f"""

## Closeout evidence

R3-B2 closed through PR #260 at `{B2_MERGE}`. Static `{B2_STATIC_RUN}` passed; Linux `{B2_LINUX_RUN}` / job `{B2_LINUX_JOB}` and independent validation `{B2_INDEPENDENT_RUN}` passed `{B2_RESULT}`. The final contribution projection was 113/113 `automatic-partial` = `bounded-positive`, 37 `enforced-automatic`, 14 `support-only`, 10 `conditional-review`, 6 `manual-review`, 1 `not-applicable`, and zero `automation-gap`. Proof-state defaults were unchanged.
"""
write(path, text)

path = "docs/R3-B2-NONAUTOMATIC-CLASSIFICATION.md"
text = read(path)
if "R3-B2 closed through PR #260" not in text:
    text += f"\nR3-B2 closed through PR #260 at `{B2_MERGE}` with this 17-rule classification unchanged and with no non-automatic rule promoted merely from a green related gate.\n"
write(path, text)

# Machine R3 inventory.
path = Path("release/v3-r3-inventory.json")
data = json.loads(path.read_text(encoding="utf-8"))
data["stage"] = "R3-B3"
data["status"] = "ACTIVE"
data["reviewed_at"] = "2026-09-03"
data.setdefault("evidence", {}).update({
    "r3_b2_product_main_sha": B2_MERGE,
    "r3_b2_inventory_run_id": B2_INVENTORY_RUN,
    "r3_b2_static_run_id": B2_STATIC_RUN,
    "r3_b2_linux_run_id": B2_LINUX_RUN,
    "r3_b2_linux_job_id": B2_LINUX_JOB,
    "r3_b2_linux_result": B2_RESULT,
    "r3_b2_independent_run_id": B2_INDEPENDENT_RUN,
    "r3_b2_independent_result": B2_RESULT,
    "r3_b2_post_merge_release_run_id": B2_RELEASE_RUN,
})
for finding in data.get("findings", []):
    if finding.get("id") == "coverage-check-name-does-not-imply-enforcement":
        finding.update({
            "status": "RESOLVED",
            "resolved_by": "R3-B2",
            "resolution": "Complete-run contribution intersects rule-specific PASS evidence with declared owners; mechanism registration alone is not enforcement.",
            "closure_sha": B2_MERGE,
        })
    elif finding.get("id") == "manual-conditional-rules-require-classification":
        finding.update({
            "status": "RESOLVED",
            "resolved_by": "R3-B2",
            "resolution": "All 17 non-automatic rules are explicit: 10 conditional-review, 6 manual-review, 1 not-applicable; no green-gate auto-promotion.",
            "closure_sha": B2_MERGE,
        })
    elif finding.get("owner") == "R3-B3" and finding.get("status") == "OPEN":
        finding["status"] = "ACTIVE"
lots = data.setdefault("lots", {})
lots.setdefault("R3-B2", {}).update({
    "issue": 253,
    "status": "DONE",
    "name": "normative proof-state and coverage semantics hardening",
    "entry_product_main_sha": B2_ENTRY,
    "pr": 260,
    "implementation_head_sha": B2_HEAD,
    "merge_main_sha": B2_MERGE,
    "inventory_run_id": B2_INVENTORY_RUN,
    "static_contract_run_id": B2_STATIC_RUN,
    "linux_integration_run_id": B2_LINUX_RUN,
    "linux_integration_job_id": B2_LINUX_JOB,
    "linux_integration_result": B2_RESULT,
    "independent_validation_run_id": B2_INDEPENDENT_RUN,
    "independent_validation_result": B2_RESULT,
    "post_merge_release_run_id": B2_RELEASE_RUN,
    "contribution": B2_CONTRIBUTION,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
})
lots.setdefault("R3-B3", {}).update({
    "issue": 254,
    "status": "ACTIVE",
    "name": "semantic test integrity and expanded residual enforcement",
    "entry_product_main_sha": B2_MERGE,
})
data["next_stage"] = "R3-B3"
data["next_issue"] = 254
data["current_entry_main_sha"] = B2_MERGE
data["r3_b2_closeout"] = {
    "issue": 253,
    "pr": 260,
    "entry_main_sha": B2_ENTRY,
    "implementation_head_sha": B2_HEAD,
    "merge_main_sha": B2_MERGE,
    "inventory_run_id": B2_INVENTORY_RUN,
    "static_contract_run_id": B2_STATIC_RUN,
    "linux_integration_run_id": B2_LINUX_RUN,
    "linux_integration_job_id": B2_LINUX_JOB,
    "linux_integration_result": B2_RESULT,
    "independent_validation_run_id": B2_INDEPENDENT_RUN,
    "independent_validation_result": B2_RESULT,
    "post_merge_release_run_id": B2_RELEASE_RUN,
    "contribution": B2_CONTRIBUTION,
    "proof_state_baseline": {"PARTIAL": 113, "NOT_PROVEN": 51, "MANUAL": 6, "CONDITIONAL": 10, "NOT_APPLICABLE": 1},
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
}
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Canonical machine roadmap: update explicit control fields and recursively close/open issue-owned lot records.
path = Path("release/v3-roadmap.json")
data = json.loads(path.read_text(encoding="utf-8"))
data["updated_at"] = "2026-09-03"
data["status"] = "ACTIVE"
data["phase"] = "V3-R3"
data["stage"] = "R3-B3"
data["stage_name"] = "semantic test integrity and expanded residual enforcement"
data["next_action"] = f"Execute V3-R3/R3-B3 issue #254 from {B2_MERGE}: audit semantic generator integrity and expand permanent removed-v2 residual enforcement across behavior-affecting project-owned engineering surfaces."


def visit(node):
    if isinstance(node, dict):
        issue = node.get("issue")
        if issue == 253 and node.get("status") in {"ACTIVE", "PENDING", "OPEN", None}:
            node["status"] = "DONE"
            node.setdefault("pr", 260)
            node.setdefault("merge_main_sha", B2_MERGE)
        if issue == 254 and node.get("status") in {"PENDING", "OPEN", None}:
            node["status"] = "ACTIVE"
            node.setdefault("entry_product_main_sha", B2_MERGE)
        for value in node.values():
            visit(value)
    elif isinstance(node, list):
        for value in node:
            visit(value)

visit(data)
r3 = data.setdefault("r3", {})
r3["status"] = "ACTIVE"
r3["stage"] = "R3-B3"
r3["stage_name"] = "semantic test integrity and expanded residual enforcement"
r3["active_issue"] = 254
r3["b2_closeout"] = {
    "issue": 253,
    "pr": 260,
    "entry_main_sha": B2_ENTRY,
    "implementation_head_sha": B2_HEAD,
    "merge_main_sha": B2_MERGE,
    "inventory_run_id": B2_INVENTORY_RUN,
    "static_contract_run_id": B2_STATIC_RUN,
    "linux_integration_run_id": B2_LINUX_RUN,
    "linux_integration_job_id": B2_LINUX_JOB,
    "linux_integration_result": B2_RESULT,
    "independent_validation_run_id": B2_INDEPENDENT_RUN,
    "independent_validation_result": B2_RESULT,
    "post_merge_release_run_id": B2_RELEASE_RUN,
    "contribution": B2_CONTRIBUTION,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
}
r3["b3"] = {
    "issue": 254,
    "status": "ACTIVE",
    "entry_product_main_sha": B2_MERGE,
    "name": "semantic test integrity and expanded residual enforcement",
}
data["active_implementation_lot"] = {
    "phase": "V3-R3",
    "stage": "R3-B3",
    "issue": 254,
    "entry_product_main_sha": B2_MERGE,
    "name": "semantic test integrity and expanded residual enforcement",
}
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("R3-B2 closeout reconciliation staged; R3-B3 activated.")
