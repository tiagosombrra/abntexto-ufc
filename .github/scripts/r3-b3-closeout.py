#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_MAIN = "fbee5bd329f98a389c2880932af40547c8d1674e"
B3_ENTRY = "44874c84b375396de8b9e3b24a40c47b5006f19b"
B3_HEAD = "5c35979e2d86b0559c5ad5373a88b83be2daf829"
B3_MERGE = EXPECTED_MAIN
B3_STATIC = 33792280764
B3_LINUX = 33792280797
B3_LINUX_JOB = 100771483526
B3_RELEASE = 33794112546
B3_RELEASE_JOB = 100777542613


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one exact replacement, found {count}: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def regex_once(path: str, pattern: str, replacement: str, flags: int = 0) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"{path}: expected one regex replacement, found {count}: {pattern}")
    p.write_text(updated, encoding="utf-8")


def update_readme() -> None:
    replace_once(
        "README.md",
        "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE: R3-A, R3-B1 and R3-B2 are DONE; R3-B3 semantic test integrity/residual hardening is ACTIVE through issue #254.**",
        "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE: R3-A and R3-B1 through R3-B3 are DONE; R3-B4 engineering-language enforcement/contract consolidation is ACTIVE through issue #255.**",
    )
    replace_once(
        "README.md",
        "R3-B3/#254 is active. The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.",
        "R3-B3/#254 closed through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`: Static `33792280764` passed, Linux `33792280797` / job `100771483526` passed `PASS=31 FAIL=0 SKIP=0`, and post-merge Linux release `33794112546` / job `100777542613` passed `PASS=33 FAIL=0 SKIP=0`. The permanent residual gate now covers 134 LaTeX and 169 behavior-affecting engineering sources (303 total), retained test/check reachability is 147/147 with zero orphaned scripts, and negative paths require positive evidence for the same `rule_id`. R3-B4/#255 is active. The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.",
    )
    replace_once(
        "README.md",
        "R3-B3/#254 is active; issues #255–#256 remain ordered after it.",
        "R3-B3/#254 is complete; R3-B4/#255 is active and R3-B5/#256 remains ordered after it.",
    )
    replace_once(
        "README.md",
        "R3-B3/#254 is active and issues #255–#256 define the remaining R3 sequence.",
        "R3-B3/#254 is complete through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`; R3-B4/#255 is active and R3-B5/#256 is the remaining R3 closeout lot.",
    )


def update_agents() -> None:
    old = "- R3-B2/#253 is DONE through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. Static `33768911131` passed; Linux `33768911126` / job `100694266254` and independent validation `33768364069` passed `PASS=31 FAIL=0 SKIP=0`. Final contribution was 113/113 `automatic-partial` bounded-positive, 37 enforced-automatic, 14 support-only, 10 conditional-review, 6 manual-review, 1 not-applicable, zero automation gaps. R3-B3/#254 is ACTIVE; B4/#255 and B5/#256 remain ordered and pending."
    new = "- R3-B2/#253 is DONE through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. Static `33768911131` passed; Linux `33768911126` / job `100694266254` and independent validation `33768364069` passed `PASS=31 FAIL=0 SKIP=0`. Final contribution was 113/113 `automatic-partial` bounded-positive, 37 enforced-automatic, 14 support-only, 10 conditional-review, 6 manual-review, 1 not-applicable, zero automation gaps.\n- R3-B3/#254 is DONE through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`, entered canonically after the B2→B3 control-plane checkpoint `44874c84b375396de8b9e3b24a40c47b5006f19b`. Static `33792280764` passed; Linux `33792280797` / job `100771483526` passed `PASS=31 FAIL=0 SKIP=0`; post-merge release `33794112546` / job `100777542613` passed `PASS=33 FAIL=0 SKIP=0`. The residual gate covers 303 behavior-relevant sources (134 LaTeX + 169 engineering), test/check reachability is 147/147 with zero orphans, and negative paths are coupled to positive PASS evidence by the same `rule_id`.\n- R3-B4/#255 is ACTIVE. R3-B5/#256 remains pending. Do not start R4 until B5 records the immutable certification entry."
    replace_once("AGENTS.md", old, new)


def update_roadmap() -> None:
    replace_once(
        "docs/ROADMAP-V3.0.0.md",
        "**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 DONE; R3-B3 ACTIVE.**",
        "**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 DONE; R3-B3 DONE; R3-B4 ACTIVE.**",
    )
    regex_once(
        "docs/ROADMAP-V3.0.0.md",
        r"R3-A inventory source is .*? Machine authority: `release/v3-roadmap\.json`\.",
        "R3-A inventory source is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-B1/#252 closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 closed through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`, with 113/113 `automatic-partial` rules bounded-positive and zero automation gaps. The B2→B3 control-plane checkpoint is `44874c84b375396de8b9e3b24a40c47b5006f19b`. R3-B3/#254 closed through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`: Static `33792280764` PASS; Linux `33792280797` / job `100771483526` = `PASS=31 FAIL=0 SKIP=0`; post-merge release `33794112546` / job `100777542613` = `PASS=33 FAIL=0 SKIP=0`. Its permanent residual contract covers 303 sources (134 LaTeX + 169 engineering), retained test/check reachability is 147/147 with zero orphaned scripts, and controlled negative paths require a positive PASS for the same `rule_id`. No normative rule ID, expected value, locator, tolerance, applicability, source authority/precedence, proof-state default, rendered requirement, or public runtime API changed. Active implementation issue: #255. Machine authority: `release/v3-roadmap.json`.",
        flags=re.S,
    )
    replace_once(
        "docs/ROADMAP-V3.0.0.md",
        "| R3-B3 | ACTIVE | issue #254; entry `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` | semantic test integrity + expanded residual enforcement | audit generators/check semantics; expand fail-closed residual scope; couple positive/negative evidence |\n| R3-B4 | PENDING | issue #255 | engineering-language enforcement + contract consolidation | after B3 |",
        "| R3-B3 | DONE | issue #254; PR #262; canonical entry `44874c84b375396de8b9e3b24a40c47b5006f19b`; merge `fbee5bd329f98a389c2880932af40547c8d1674e` | 303-source residual gate; 147/147 reachable checks; zero orphaned scripts; Linux 31/0/0; release 33/0/0 | None |\n| R3-B4 | ACTIVE | issue #255; entry `fbee5bd329f98a389c2880932af40547c8d1674e` | engineering-language enforcement + contract consolidation | enforce scoped English engineering policy; migrate technical profile IDs; audit closed migration-contract consumers |",
    )
    regex_once(
        "docs/ROADMAP-V3.0.0.md",
        r"## R3-B3 entry\n.*?## Immediate action\n\n.*$",
        "## R3-B3 closeout\n\nR3-B3/#254 entered from the reconciled B2→B3 control-plane checkpoint `44874c84b375396de8b9e3b24a40c47b5006f19b`, not directly from the earlier B2 product SHA. Its implementation head was `5c35979e2d86b0559c5ad5373a88b83be2daf829` and PR #262 squash-merged at `fbee5bd329f98a389c2880932af40547c8d1674e`.\n\nThe six-profile generator is fail-closed and bound to canonical v3 values; `tests/checks/v3_api_residual.py` now covers 134 LaTeX plus 169 behavior-affecting engineering sources; deliberate removed-v2 literals require narrow `negative-test-literal` annotation; retained test/check scripts are 147/147 reachable with three standalone certification/release checks explicitly classified and zero orphaned scripts; obsolete `frontmatter_validation.py` was removed; public/distribution bundle checks reject the removed forwarding layer; and negative-path evidence requires a positive PASS for the same `rule_id`.\n\nStatic `33792280764` passed. PR Linux integration `33792280797` / job `100771483526` passed `PASS=31 FAIL=0 SKIP=0`. Post-merge Linux release `33794112546` / job `100777542613` passed `PASS=33 FAIL=0 SKIP=0`, including release-only PDF/A checks. Normative semantics, proof-state defaults and the public runtime API did not change.\n\n## R3-B4 entry\n\nR3-B4/#255 starts from product checkpoint `fbee5bd329f98a389c2880932af40547c8d1674e`. It owns executable engineering-language enforcement, consumer-safe migration of project-owned Portuguese technical profile/scenario identifiers to canonical English terminology, translation of project-owned technical diagnostics/comments/UI while protecting rendered Brazilian academic content and genuine upstream boundaries, and the consumer audit/consolidation of closed migration contracts. `release/v3-api-migration.json` remains retained because the permanent residual gate consumes it.\n\n## Immediate action\n\nExecute **R3-B4 / issue #255** from `fbee5bd329f98a389c2880932af40547c8d1674e`. Inventory the remaining project-owned Portuguese engineering vocabulary and consumers of `release/v3-test-migration.json` / `release/v3-path-migration.json`, then implement a scoped permanent language gate with explicit academic/normative/upstream exemptions. Do not start R3-B5, R4, R5, V3-A1/A2, or CTAN submission before their recorded entry conditions.\n",
        flags=re.S,
    )


def update_handoff() -> None:
    regex_once(
        "docs/HANDOFF-V3.0.0.md",
        r"- R3-B2/#253: \*\*DONE\*\* through PR #260\..*?- Certified R1 candidate remains",
        "- R3-B2/#253: **DONE** through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`; final contribution = 113/113 `automatic-partial` bounded-positive with zero automation gaps.\n- B2→B3 control-plane checkpoint: `44874c84b375396de8b9e3b24a40c47b5006f19b`.\n- R3-B3/#254: **DONE** through PR #262.\n- R3-B3 implementation head: `5c35979e2d86b0559c5ad5373a88b83be2daf829`.\n- R3-B3 closure/main SHA: `fbee5bd329f98a389c2880932af40547c8d1674e`.\n- R3-B3 PR gates: Static `33792280764` PASS; Linux `33792280797` / job `100771483526` = `PASS=31 FAIL=0 SKIP=0`.\n- R3-B3 post-merge release: `33794112546` / job `100777542613` = `PASS=33 FAIL=0 SKIP=0`.\n- R3-B3 integrity: 303 residual-scanned sources (134 LaTeX + 169 engineering), 147/147 retained scripts reachable, 3 standalone checks classified, 0 orphaned, negative evidence coupled to positive PASS by identical `rule_id`.\n- Active phase: **V3-R3**.\n- Active stage: **R3-B4 — engineering-language enforcement and closed-contract consolidation**.\n- Active issue: **#255**.\n- R3 inventory: `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`.\n- Certified R1 candidate remains",
        flags=re.S,
    )
    regex_once(
        "docs/HANDOFF-V3.0.0.md",
        r"## What R3-B2 established\n.*?## R3 lots",
        "## What R3-B3 established\n\nThe active semantic-test surface is now fail-closed against generator no-ops and removed-v2 API residue across behavior-affecting engineering sources. The six-profile generator asserts canonical variation, the residual gate scans 303 sources, and deliberate historical/negative literals require narrow explicit annotation rather than broad file exemptions.\n\nEvery retained test/check script is either reachable from a repository-owned gate or explicitly classified as standalone certification/release support: 147/147 reachable, three standalone, zero orphaned. Negative-path cases must observe a current positive PASS for the same normative `rule_id` before controlled rejection can count.\n\nNo normative source authority, precedence, rule ID, expected value, locator, tolerance, applicability, proof-state default, rendered-format requirement, or public runtime API changed in B3.\n\n## R3 lots",
        flags=re.S,
    )
    replace_once(
        "docs/HANDOFF-V3.0.0.md",
        "| R3-B3 | #254 | ACTIVE | semantic test integrity and expanded residual enforcement |\n| R3-B4 | #255 | PENDING | engineering-language enforcement and closed-contract consolidation |",
        "| R3-B3 | #254 | DONE | semantic test integrity and expanded residual enforcement |\n| R3-B4 | #255 | ACTIVE | engineering-language enforcement and closed-contract consolidation |",
    )
    regex_once(
        "docs/HANDOFF-V3.0.0.md",
        r"## Immediate action\n\n.*?## Hard boundaries",
        "## Immediate action\n\nExecute issue #255 from `fbee5bd329f98a389c2880932af40547c8d1674e`. Add scoped permanent engineering-language enforcement, preserve rendered/official/bibliographic/upstream Portuguese boundaries, migrate project-owned Portuguese technical profile/scenario identifiers consumer-safely, translate remaining project-owned diagnostics/comments/UI, and audit `release/v3-test-migration.json` plus `release/v3-path-migration.json` for live consumers before consolidation/removal.\n\n## Hard boundaries",
        flags=re.S,
    )
    replace_once(
        "docs/HANDOFF-V3.0.0.md",
        "Do not start R3-B4/B5, R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission before their recorded entry conditions.",
        "Do not start R3-B5, R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission before their recorded entry conditions.",
    )


def update_inventory_doc() -> None:
    replace_once(
        "docs/R3-HARDENING-INVENTORY.md",
        "R3-B1/#252 is closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 is closed through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. R3-B3/#254 is active.",
        "R3-B1/#252 is closed through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 is closed through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`. The B2→B3 control-plane checkpoint is `44874c84b375396de8b9e3b24a40c47b5006f19b`. R3-B3/#254 is closed through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`. R3-B4/#255 is active.",
    )
    marker = "## Findings resolved\n"
    p = ROOT / "docs/R3-HARDENING-INVENTORY.md"
    text = p.read_text(encoding="utf-8")
    if marker not in text:
        raise SystemExit("inventory: missing Findings resolved marker")
    closeout = "## R3-B3 closeout evidence\n\n- canonical B3 entry/control-plane checkpoint: `44874c84b375396de8b9e3b24a40c47b5006f19b`;\n- implementation head: `5c35979e2d86b0559c5ad5373a88b83be2daf829`;\n- merge/main SHA: `fbee5bd329f98a389c2880932af40547c8d1674e`;\n- issue / PR: #254 / #262;\n- bounded executor: `33792107946` / job `100770917618`;\n- PR Static contract: `33792280764` — PASS;\n- PR Linux integration: `33792280797` / job `100771483526` — `PASS=31 FAIL=0 SKIP=0`;\n- post-merge Linux release: `33794112546` / job `100777542613` — `PASS=33 FAIL=0 SKIP=0`;\n- residual scope: 134 LaTeX + 169 engineering = 303 sources; runtime aliases = 0; forwarding layer absent;\n- test surface: 147/147 retained scripts reachable, 3 standalone classified, 0 orphaned;\n- profile generator: six canonical values, six distinct generated sources, fail-closed no-op detection;\n- negative paths require same-`rule_id` positive PASS before controlled rejection;\n- normative semantics / proof-state defaults / public runtime API changed: **no**.\n\n"
    if "## R3-B3 closeout evidence" not in text:
        text = text.replace(marker, closeout + marker, 1)
    p.write_text(text, encoding="utf-8")
    replace_once(
        "docs/R3-HARDENING-INVENTORY.md",
        "| Residual gate engineering scope gap | R3-B3 | #254 | ACTIVE | Extend semantic/residual protection to behavior-affecting project-owned scripts/generators/workflows/machine/tool surfaces. |\n| Generator semantic no-op risk | R3-B3 | #254 | ACTIVE | Generated matrices must assert intended canonical variation and reject stale substitutions/no-ops. |\n| Test purpose/evidence integrity | R3-B3 | #254 | ACTIVE | Classify duplicate, orphan, support-only and label/behavior-mismatched checks; couple positive/negative rule IDs. |",
        "| Engineering-language diagnostics gap | R3-B4 | #255 | ACTIVE | Enforce English technical diagnostics/comments/UI without touching rendered academic Portuguese. |\n| Engineering profile identifiers remain Portuguese | R3-B4 | #255 | ACTIVE | Migrate project-owned machine identifiers where consumer-safe and preserve genuine content/upstream boundaries. |\n| Closed migration contract cleanup | R3-B4 | #255 | ACTIVE | Prove consumers before consolidating/removing closed R2 contracts. |",
    )
    # Remove duplicated pending B4 rows left below the replacement.
    regex_once(
        "docs/R3-HARDENING-INVENTORY.md",
        r"\| Engineering-language diagnostics gap \| R3-B4 \| #255 \| PENDING .*?\n\| Engineering profile identifiers remain Portuguese \| R3-B4 \| #255 \| PENDING .*?\n\| Closed migration contract cleanup \| R3-B4 \| #255 \| PENDING .*?\n",
        "",
    )
    replace_once(
        "docs/R3-HARDENING-INVENTORY.md",
        "| R3-B3/#254 | ACTIVE | entry `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` |\n| R3-B4/#255 | PENDING | after B3 |",
        "| R3-B3/#254 | DONE | entry `44874c84b375396de8b9e3b24a40c47b5006f19b`; PR #262 → `fbee5bd329f98a389c2880932af40547c8d1674e`; PR `PASS=31 FAIL=0 SKIP=0`; release `PASS=33 FAIL=0 SKIP=0` |\n| R3-B4/#255 | ACTIVE | entry `fbee5bd329f98a389c2880932af40547c8d1674e` |",
    )
    regex_once(
        "docs/R3-HARDENING-INVENTORY.md",
        r"## R3-B3 entry contract\n.*$",
        "## R3-B4 entry contract\n\nB4 starts from `fbee5bd329f98a389c2880932af40547c8d1674e`. It must make the English-first engineering policy executable without confusing rendered Brazilian academic content, official normative wording, bibliography data, literal output under test, or genuine upstream identifiers with project-owned engineering nomenclature. It owns a scoped permanent source checker, consumer-safe migration of remaining project-owned Portuguese profile/scenario identifiers, translation of project-owned technical diagnostics/comments/UI, and a fail-closed consumer audit of closed migration contracts.\n\n`release/v3-api-migration.json` remains a live dependency of `tests/checks/v3_api_residual.py` and must be retained while consumed. `release/v3-test-migration.json` and `release/v3-path-migration.json` may be consolidated or removed only after current consumers are proven absent or migrated. B4 requires `make static-check`, targeted exemption/false-positive tests, and full `make check` when scenario identifiers or integration scripts change.\n\nNo source/currency fact changed in B3, so `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` remain intentionally unchanged. The v3 migration guide also remains unchanged because B3 changed no public runtime API.\n",
        flags=re.S,
    )


def update_architecture_language_ctan() -> None:
    replace_once(
        "docs/ARCHITECTURE.md",
        "R3-B3/#254 is active. Remaining R3 architecture work is semantic test/residual scope, engineering-language/contracts, and closeout/R4 entry.",
        "R3-B3/#254 is DONE through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`: semantic generator variation is fail-closed, the permanent residual gate covers 303 behavior-relevant sources, and the retained test/check surface has zero orphans. R3-B4/#255 is active. Remaining R3 architecture work is engineering-language/closed-contract enforcement followed by B5 closeout/R4 entry.",
    )
    replace_once(
        "docs/ARCHITECTURE.md",
        "R3-B3 now owns expansion of permanent residual enforcement across project-owned engineering sources that can affect runtime or test behavior while exempting only explicit migration documentation/contracts, negative tests, rendered academic content, and genuine upstream boundaries.",
        "R3-B3 completed permanent residual expansion across project-owned engineering sources that can affect runtime or test behavior while retaining only narrow explicit migration/negative-test/upstream boundaries. It also makes profile generation fail closed, classifies all retained test/check scripts by reachability/purpose, and couples negative-path rejection to same-`rule_id` positive evidence. R3-B4 now owns executable engineering-language enforcement and closed-contract consolidation.",
    )
    replace_once(
        "docs/ENGINEERING-LANGUAGE.md",
        "R3-B2/#253 closed at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` without broadening language policy; R3-B3/#254 is the current stage and owns engineering residual/test-integrity scope.",
        "R3-B2/#253 closed at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` without broadening language policy. R3-B3/#254 closed through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`, expanding removed-v2 residual enforcement across 303 behavior-relevant sources while keeping deliberate negative literals narrowly annotated. R3-B4/#255 is now active and owns the scoped permanent engineering-language source checker, technical identifier migration, and closed-contract audit.",
    )
    replace_once(
        "docs/CTAN-RELEASE.md",
        "R3-B3/#254 is active and B4–B5 remain required before R4.",
        "R3-B3/#254 is complete through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`; its PR Linux gate passed `PASS=31 FAIL=0 SKIP=0` and post-merge release run `33794112546` passed `PASS=33 FAIL=0 SKIP=0`. R3-B4/#255 is active and B5 remains required before R4.",
    )


def update_machine_state() -> None:
    p = ROOT / "release/v3-roadmap.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["updated_at"] = "2026-09-03"
    data["phase"] = "V3-R3"
    data["stage"] = "R3-B4"
    data["stage_name"] = "engineering-language enforcement and closed-contract consolidation"
    data["next_action"] = f"Execute V3-R3/R3-B4 issue #255 from {B3_MERGE}: enforce scoped English project engineering language, migrate technical profile/scenario identifiers consumer-safely, and audit closed migration-contract consumers."
    data["active_implementation_lot"] = {
        "phase": "V3-R3",
        "stage": "R3-B4",
        "issue": 255,
        "entry_product_main_sha": B3_MERGE,
        "name": "engineering-language enforcement and closed-contract consolidation",
    }
    r3 = data["r3"]
    r3["stage"] = "R3-B4"
    r3["stage_name"] = "engineering-language enforcement and closed-contract consolidation"
    r3["issue"] = 255
    r3["next_issue"] = 255
    r3["active_issue"] = 255
    r3["pr"] = 262
    r3["merge_main_sha"] = B3_MERGE
    b3 = r3["lots"]["R3-B3"]
    b3.update({
        "status": "DONE",
        "entry_product_main_sha": B3_ENTRY,
        "implementation_head_sha": B3_HEAD,
        "pr": 262,
        "merge_main_sha": B3_MERGE,
        "static_contract_run_id": B3_STATIC,
        "linux_integration_run_id": B3_LINUX,
        "linux_integration_job_id": B3_LINUX_JOB,
        "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
        "post_merge_release_run_id": B3_RELEASE,
        "post_merge_release_job_id": B3_RELEASE_JOB,
        "post_merge_release_result": "PASS=33 FAIL=0 SKIP=0",
        "residual_sources": {"latex": 134, "engineering": 169, "total": 303},
        "test_surface": {"retained": 147, "reachable": 147, "standalone_classified": 3, "orphaned": 0},
        "normative_semantics_changed": False,
        "proof_state_changed": False,
        "public_runtime_api_changed": False,
    })
    r3["lots"]["R3-B4"].update({"status": "ACTIVE", "entry_product_main_sha": B3_MERGE})
    r3["b3"] = dict(b3)
    r3["b3_closeout"] = dict(b3)
    data["r3_b3_closeout"] = dict(b3)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    p = ROOT / "release/v3-r3-inventory.json"
    inv = json.loads(p.read_text(encoding="utf-8"))
    inv["stage"] = "R3-B4"
    inv["reviewed_at"] = "2026-09-03"
    inv["evidence"].update({
        "r3_b3_control_plane_entry_sha": B3_ENTRY,
        "r3_b3_product_main_sha": B3_MERGE,
        "r3_b3_static_run_id": B3_STATIC,
        "r3_b3_linux_run_id": B3_LINUX,
        "r3_b3_linux_job_id": B3_LINUX_JOB,
        "r3_b3_linux_result": "PASS=31 FAIL=0 SKIP=0",
        "r3_b3_post_merge_release_run_id": B3_RELEASE,
        "r3_b3_post_merge_release_job_id": B3_RELEASE_JOB,
        "r3_b3_post_merge_release_result": "PASS=33 FAIL=0 SKIP=0",
    })
    for finding in inv["findings"]:
        if finding["id"] == "residual-gate-engineering-scope-gap":
            finding.update({
                "status": "RESOLVED",
                "resolved_by": "R3-B3",
                "resolution": "Residual enforcement covers 134 LaTeX plus 169 behavior-affecting engineering sources with narrow explicit exemptions; runtime aliases remain zero.",
                "closure_sha": B3_MERGE,
            })
        elif finding.get("owner") == "R3-B4" and finding["status"] == "OPEN":
            finding["status"] = "ACTIVE"
    inv["lots"]["R3-B3"].update({
        "status": "DONE",
        "entry_product_main_sha": B3_ENTRY,
        "implementation_head_sha": B3_HEAD,
        "pr": 262,
        "merge_main_sha": B3_MERGE,
        "static_contract_run_id": B3_STATIC,
        "linux_integration_run_id": B3_LINUX,
        "linux_integration_job_id": B3_LINUX_JOB,
        "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
        "post_merge_release_run_id": B3_RELEASE,
        "post_merge_release_job_id": B3_RELEASE_JOB,
        "post_merge_release_result": "PASS=33 FAIL=0 SKIP=0",
        "residual_sources": {"latex": 134, "engineering": 169, "total": 303},
        "test_surface": {"retained": 147, "reachable": 147, "standalone_classified": 3, "orphaned": 0},
        "normative_semantics_changed": False,
        "proof_state_changed": False,
        "public_runtime_api_changed": False,
    })
    inv["lots"]["R3-B4"].update({"status": "ACTIVE", "entry_product_main_sha": B3_MERGE})
    inv["next_stage"] = "R3-B4"
    inv["next_issue"] = 255
    inv["current_entry_main_sha"] = B3_MERGE
    inv["r3_b3_closeout"] = dict(inv["lots"]["R3-B3"])
    p.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_state() -> None:
    roadmap = json.loads((ROOT / "release/v3-roadmap.json").read_text(encoding="utf-8"))
    inventory = json.loads((ROOT / "release/v3-r3-inventory.json").read_text(encoding="utf-8"))
    assert roadmap["stage"] == "R3-B4"
    assert roadmap["r3"]["lots"]["R3-B3"]["status"] == "DONE"
    assert roadmap["r3"]["lots"]["R3-B4"]["status"] == "ACTIVE"
    assert roadmap["r3"]["lots"]["R3-B3"]["entry_product_main_sha"] == B3_ENTRY
    assert inventory["stage"] == "R3-B4"
    assert inventory["lots"]["R3-B3"]["status"] == "DONE"
    assert inventory["lots"]["R3-B4"]["status"] == "ACTIVE"
    for path in ["README.md", "AGENTS.md", "docs/ROADMAP-V3.0.0.md", "docs/HANDOFF-V3.0.0.md", "docs/R3-HARDENING-INVENTORY.md", "docs/ARCHITECTURE.md", "docs/ENGINEERING-LANGUAGE.md", "docs/CTAN-RELEASE.md"]:
        text = (ROOT / path).read_text(encoding="utf-8")
        if "R3-B4" not in text:
            raise SystemExit(f"{path}: missing R3-B4 state")


def main() -> None:
    run("git", "fetch", "origin", "main")
    actual_main = run("git", "rev-parse", "origin/main")
    if actual_main != EXPECTED_MAIN:
        raise SystemExit(f"origin/main moved: expected {EXPECTED_MAIN}, got {actual_main}")
    if run("git", "merge-base", "HEAD", "origin/main") != EXPECTED_MAIN:
        raise SystemExit("branch is not based on the expected B3 product checkpoint")

    update_readme()
    update_agents()
    update_roadmap()
    update_handoff()
    update_inventory_doc()
    update_architecture_language_ctan()
    update_machine_state()
    validate_state()

    subprocess.check_call(["git", "rm", ".github/scripts/r3-b3-closeout.py", ".github/workflows/r3-b3-closeout.yml"], cwd=ROOT)
    subprocess.check_call(["make", "static-check"], cwd=ROOT)
    subprocess.check_call(["git", "diff", "--check"], cwd=ROOT)

    subprocess.check_call(["git", "add", "README.md", "AGENTS.md", "docs/ROADMAP-V3.0.0.md", "docs/HANDOFF-V3.0.0.md", "docs/R3-HARDENING-INVENTORY.md", "docs/ARCHITECTURE.md", "docs/ENGINEERING-LANGUAGE.md", "docs/CTAN-RELEASE.md", "release/v3-roadmap.json", "release/v3-r3-inventory.json"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT)
    subprocess.check_call(["git", "commit", "-m", "docs: close R3-B3 and activate R3-B4"], cwd=ROOT)
    subprocess.check_call(["git", "push", "origin", "HEAD"], cwd=ROOT)


if __name__ == "__main__":
    main()
