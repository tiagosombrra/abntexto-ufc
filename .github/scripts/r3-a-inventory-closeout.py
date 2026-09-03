#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_MAIN_SHA = "345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5"
R2_PRODUCT_SHA = "ecd5926760080003148e8b1621dc8d4e4e8c7e5e"
R2_RELEASE_RUN = 33745603468
R3_A_ISSUE = 250
R3_B1_ISSUE = 252
R3_B2_ISSUE = 253
R3_B3_ISSUE = 254
R3_B4_ISSUE = 255
R3_B5_ISSUE = 256
STATIC_RUN = 33747658673
LINUX_RUN = 33747658602


def verify_entry() -> None:
    current_main = subprocess.check_output(
        ["git", "rev-parse", "origin/main"], cwd=ROOT, text=True
    ).strip()
    if current_main != SOURCE_MAIN_SHA:
        raise SystemExit(
            f"R3-A inventory entry moved: expected {SOURCE_MAIN_SHA}, got {current_main}"
        )


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, data: dict) -> None:
    (ROOT / relative).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def replace_exact(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Expected text not found in {relative}: {old[:120]!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def update_machine_state() -> None:
    roadmap = load_json("release/v3-roadmap.json")
    roadmap.update(
        {
            "updated_at": "2026-09-03",
            "status": "ACTIVE",
            "phase": "V3-R3",
            "stage": "R3-B1",
            "stage_name": "front-matter evidence truthfulness and fail-closed enforcement",
            "active_branch": "main",
            "next_action": (
                f"Execute V3-R3/R3-B1 issue #{R3_B1_ISSUE}: repair front-matter fixture/observer "
                "truthfulness, discriminate unresolved findings, and make proof-contributing "
                "front-matter evidence fail-closed before changing normative semantics."
            ),
        }
    )

    r3 = roadmap.setdefault("r3", {})
    r3.update(
        {
            "status": "ACTIVE",
            "stage": "R3-B1",
            "stage_name": "front-matter evidence truthfulness and fail-closed enforcement",
            "issue": R3_B1_ISSUE,
            "inventory_document": "docs/R3-HARDENING-INVENTORY.md",
            "inventory_contract": "release/v3-r3-inventory.json",
            "implementation_lots_defined": True,
            "next_issue": R3_B1_ISSUE,
            "goal": (
                "Harden evidence truthfulness, normative proof semantics, semantic test integrity, "
                "engineering-language enforcement, and closed-contract hygiene before R4 certification."
            ),
            "exit": (
                "R3-B1 through R3-B5 are complete, proof-contributing evidence is fail-closed, "
                "the engineering policy is enforced, and an immutable R4 certification entry is recorded."
            ),
        }
    )
    r3["r3_a"] = {
        "status": "DONE",
        "issue": R3_A_ISSUE,
        "source_main_sha": SOURCE_MAIN_SHA,
        "inventory_document": "docs/R3-HARDENING-INVENTORY.md",
        "inventory_contract": "release/v3-r3-inventory.json",
        "static_run_id": STATIC_RUN,
        "linux_integration_run_id": LINUX_RUN,
        "linux_integration_result": "PASS=30 FAIL=0 SKIP=0",
        "normative_sources": 19,
        "normative_rules": 181,
        "automatic_rules": 164,
        "manual_or_conditional_rules": 17,
        "implementation_lots_defined": True,
        "normative_semantics_changed": False,
        "proof_state_changed": False,
    }
    r3["lots"] = {
        "R3-B1": {
            "status": "ACTIVE",
            "issue": R3_B1_ISSUE,
            "name": "front-matter evidence truthfulness and fail-closed enforcement",
            "entry_product_main_sha": SOURCE_MAIN_SHA,
        },
        "R3-B2": {
            "status": "PENDING",
            "issue": R3_B2_ISSUE,
            "name": "normative proof-state and coverage semantics hardening",
        },
        "R3-B3": {
            "status": "PENDING",
            "issue": R3_B3_ISSUE,
            "name": "semantic test integrity and expanded residual enforcement",
        },
        "R3-B4": {
            "status": "PENDING",
            "issue": R3_B4_ISSUE,
            "name": "engineering-language enforcement and closed-contract consolidation",
        },
        "R3-B5": {
            "status": "PENDING",
            "issue": R3_B5_ISSUE,
            "name": "R3 closeout and R4 certification entry",
        },
    }

    roadmap["r3_a_closeout"] = {
        "status": "DONE",
        "issue": R3_A_ISSUE,
        "source_main_sha": SOURCE_MAIN_SHA,
        "inventory_document": "docs/R3-HARDENING-INVENTORY.md",
        "inventory_contract": "release/v3-r3-inventory.json",
        "static_run_id": STATIC_RUN,
        "linux_integration_run_id": LINUX_RUN,
        "linux_integration_result": "PASS=30 FAIL=0 SKIP=0",
        "lots": [R3_B1_ISSUE, R3_B2_ISSUE, R3_B3_ISSUE, R3_B4_ISSUE, R3_B5_ISSUE],
        "normative_semantics_changed": False,
        "proof_state_changed": False,
    }
    roadmap["active_implementation_lot"] = {
        "stage": "R3-B1",
        "issue": R3_B1_ISSUE,
        "entry_product_main_sha": SOURCE_MAIN_SHA,
        "status": "ACTIVE",
        "implementation_branch_rule": "branch from the merged R3-A inventory/control-plane checkpoint",
    }
    write_json("release/v3-roadmap.json", roadmap)

    inventory = load_json("release/v3-r3-inventory.json")
    inventory["status"] = "DONE"
    inventory["next_stage"] = "R3-B1"
    inventory["next_issue"] = R3_B1_ISSUE
    inventory["lots"]["R3-B1"]["status"] = "ACTIVE"
    write_json("release/v3-r3-inventory.json", inventory)


def write_primary_docs() -> None:
    handoff = f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- R2 product closure: `{R2_PRODUCT_SHA}`; merged-main release run `{R2_RELEASE_RUN}` = `PASS=32 FAIL=0 SKIP=0`.
- R2 closeout/control-plane source baseline and R3-A inventory source: `{SOURCE_MAIN_SHA}`.
- R3-A planning issue: **#{R3_A_ISSUE} — DONE**.
- R3-A validation evidence: Static `{STATIC_RUN}` PASS; Linux `{LINUX_RUN}` = `PASS=30 FAIL=0 SKIP=0`.
- Active phase: **V3-R3**.
- Active stage: **R3-B1 — front-matter evidence truthfulness and fail-closed enforcement**.
- Active issue: **#{R3_B1_ISSUE}**.
- R3 inventory: `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## R3-A findings

R3-A did not discover new normative source/currency evidence. The source baseline remains 19 sources and 181 rules: 164 classified automatic and 17 manual/conditional. The current integration suite is green, but front-matter evidence truthfulness is not yet sufficient for R4 because audit-only producers can emit FAIL while the umbrella gate exits successfully.

Two concrete semantic defects were established before any runtime change:

1. `frontmatter-approval-evidence.sh` still substitutes the removed v2 text `tipo = tese` even though the fixture uses canonical `type = doctoral-thesis`; the profile matrix is therefore not proven to vary as labelled.
2. the summary source-paragraph observer does not recognize canonical `\\ufcSummaryKeywords`, producing a false two-paragraph vernacular finding.

Additional dedication, short-epigraph, title-page and approval observations remain unresolved until B1 discriminates fixture/observer behavior from runtime behavior.

## R3 lots

| Lot | Issue | Status | Purpose |
|---|---:|---|---|
| R3-B1 | #{R3_B1_ISSUE} | ACTIVE | front-matter evidence truthfulness and fail-closed enforcement |
| R3-B2 | #{R3_B2_ISSUE} | PENDING | normative proof-state and coverage semantics |
| R3-B3 | #{R3_B3_ISSUE} | PENDING | semantic test integrity and expanded residual enforcement |
| R3-B4 | #{R3_B4_ISSUE} | PENDING | engineering-language enforcement and closed-contract consolidation |
| R3-B5 | #{R3_B5_ISSUE} | PENDING | R3 closeout and exact R4 entry |

## Immediate action

Execute issue #{R3_B1_ISSUE}. Repair fixtures/observers first; do not change runtime behavior merely to remove an audit FAIL. Once front-matter proof-contributing evidence is truthful, enable enforcement or explicitly classify support-only observations so an aggregate PASS cannot hide a normative FAIL.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, values, locators, tolerances, applicability or proof state without current evidence. Do not start R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission during R3-B1 through R3-B4. Literal Windows-font certification remains R4-owned.
"""
    (ROOT / "docs/HANDOFF-V3.0.0.md").write_text(handoff, encoding="utf-8")

    roadmap_doc = f"""# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-03

## Status

**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 ACTIVE.**

R3-A inventory source is `{SOURCE_MAIN_SHA}`. Its validating Static `{STATIC_RUN}` passed and Linux integration `{LINUX_RUN}` passed `PASS=30 FAIL=0 SKIP=0`. The inventory is recorded in `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json`. Active implementation issue: #{R3_B1_ISSUE}. Machine authority: `release/v3-roadmap.json`.

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
| R2-B5 | DONE | PR #249 → `{R2_PRODUCT_SHA}` | forwarding layer removed; migration guide + permanent residual gate | None |
| V3-R2 closeout | DONE | PR #251 → `{SOURCE_MAIN_SHA}` | canonical control plane reconciled; R3-A opened | None |
| R3-A | DONE | issue #{R3_A_ISSUE}; inventory source `{SOURCE_MAIN_SHA}` | current standards/test/language/proof gaps classified; five bounded lots defined | None |
| R3-B1 | ACTIVE | issue #{R3_B1_ISSUE} | make front-matter evidence truthful and fail-closed | repair generator/observer defects; discriminate remaining findings; enforce proof |
| R3-B2 | PENDING | issue #{R3_B2_ISSUE} | harden normative proof-state and coverage semantics | after B1 |
| R3-B3 | PENDING | issue #{R3_B3_ISSUE} | semantic test integrity + expanded residual enforcement | after B2 |
| R3-B4 | PENDING | issue #{R3_B4_ISSUE} | engineering-language enforcement + contract consolidation | after B3 |
| R3-B5 | PENDING | issue #{R3_B5_ISSUE} | R3 closeout and immutable R4 entry | after B4 |
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

Execute **R3-B1 / issue #{R3_B1_ISSUE}**. Use targeted front-matter validation during iteration, then full `make check` before merge. Do not treat current audit findings as authority to change normative values or runtime semantics until fixture/observer defects are excluded.
"""
    (ROOT / "docs/ROADMAP-V3.0.0.md").write_text(roadmap_doc, encoding="utf-8")


def update_secondary_docs() -> None:
    replace_exact(
        "README.md",
        "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE in R3-A — standards/tests/engineering-language hardening inventory, tracked by issue #250.**",
        f"**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE: R3-A inventory is DONE and R3-B1 front-matter evidence hardening is ACTIVE through issue #{R3_B1_ISSUE}.**",
    )
    replace_exact(
        "README.md",
        "R2 closed through B5/PR #249 at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e`. B5 Static `33743809498` and Linux integration `33743809431` passed before merge; the merged-main Linux release check `33745603468` then passed `PASS=32 FAIL=0 SKIP=0`. The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; its Windows/Linux font, Unicode, embedding, and PDF/A-2b certification record remains unchanged. R3-A is an inventory/planning stage and does not itself recertify the product.",
        f"R2 closed through B5/PR #249 at `{R2_PRODUCT_SHA}` and its control plane was reconciled at `{SOURCE_MAIN_SHA}`. R3-A then classified the current standards/test/language/proof gaps without changing normative semantics. Its source baseline remains green under Static `{STATIC_RUN}` and Linux `{LINUX_RUN}` = `PASS=30 FAIL=0 SKIP=0`. The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.",
    )
    replace_exact(
        "README.md",
        "R2-A and R2-B1 through R2-B5 are complete. The v3 public/runtime API is directly owned, the forwarding-only layer is absent, `docs/MIGRATING-TO-V3.md` documents the breaking migration, and `tests/checks/v3_api_residual.py` permanently rejects removed project API in active consumers. R3-A now inventories standards, semantic test coverage, and engineering-language enforcement before bounded hardening lots are defined.",
        f"R2-A and R2-B1 through R2-B5 are complete. The v3 public/runtime API is directly owned, the forwarding-only layer is absent, `docs/MIGRATING-TO-V3.md` documents the breaking migration, and `tests/checks/v3_api_residual.py` permanently rejects removed project API in its current source scope. R3-A is complete; `docs/R3-HARDENING-INVENTORY.md` records the evidence gaps and issues #{R3_B1_ISSUE}–#{R3_B5_ISSUE} define the bounded R3 sequence. R3-B1 is active.",
    )
    replace_exact(
        "README.md",
        "- `docs/HANDOFF-V3.0.0.md`",
        "- `docs/HANDOFF-V3.0.0.md`\n- `docs/R3-HARDENING-INVENTORY.md`",
    )
    replace_exact(
        "README.md",
        "R2-A and R2-B1 through R2-B5 are complete. B5 PR #249 merged at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` after Static `33743809498` and Linux integration `33743809431` passed; merged-main release run `33745603468` passed `PASS=32 FAIL=0 SKIP=0`. V3-R3/R3-A is active through issue #250.",
        f"R2-A and R2-B1 through R2-B5 are complete. B5 PR #249 merged at `{R2_PRODUCT_SHA}` and R2 closeout PR #251 established `{SOURCE_MAIN_SHA}`. R3-A/#250 is complete and the active hardening lot is R3-B1/#{R3_B1_ISSUE}; issues #{R3_B2_ISSUE}–#{R3_B5_ISSUE} define the remaining R3 sequence.",
    )

    replace_exact(
        "AGENTS.md",
        "- V3-R3 is ACTIVE in R3-A via issue #250. R3-A is inventory/planning only: classify standards/proof-state, semantic-test, and engineering-language gaps before defining implementation lots.",
        f"- V3-R3 is ACTIVE. R3-A/#250 is DONE from source baseline `{SOURCE_MAIN_SHA}`; `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json` define the evidence-driven lot sequence.\n- R3-B1/#{R3_B1_ISSUE} is ACTIVE and owns front-matter evidence truthfulness/fail-closed enforcement. R3-B2/#{R3_B2_ISSUE}, B3/#{R3_B3_ISSUE}, B4/#{R3_B4_ISSUE}, and B5/#{R3_B5_ISSUE} remain ordered and pending.",
    )
    replace_exact(
        "AGENTS.md",
        "- Preserve rendered behavior and normative rule IDs, values, tolerances, locators and proof state unless explicit current evidence authorizes a normative change.",
        "- Repair fixture/observer defects before changing runtime behavior in response to an audit finding. An aggregate PASS must not be treated as proof when its proof-contributing evidence contains an unclassified FAIL/UNASSESSED record.\n- Preserve rendered behavior and normative rule IDs, values, tolerances, locators and proof state unless explicit current evidence authorizes a normative change.",
    )

    replace_exact(
        "docs/ARCHITECTURE.md",
        f"V3-R2 is DONE through B5 at `{R2_PRODUCT_SHA}`; the forwarding-only API layer is absent and permanent residual enforcement is part of `make static-check`. V3-R3 is active only at the R3-A inventory/planning boundary.",
        f"V3-R2 is DONE through B5 at `{R2_PRODUCT_SHA}`; the forwarding-only API layer is absent and permanent residual enforcement is part of `make static-check`. R3-A is DONE from `{SOURCE_MAIN_SHA}` and R3-B1/#{R3_B1_ISSUE} is active. The R3 architecture work is evidence hardening: B1 front matter, B2 proof-state/coverage, B3 semantic test/residual scope, B4 engineering-language/contracts, and B5 closeout/R4 entry.",
    )
    marker = "## Validator\n"
    architecture_path = ROOT / "docs/ARCHITECTURE.md"
    architecture = architecture_path.read_text(encoding="utf-8")
    if "## R3 hardening architecture" not in architecture:
        if marker not in architecture:
            raise SystemExit("ARCHITECTURE validator marker missing")
        r3_section = f"""## R3 hardening architecture

R3-A established that the remaining foundation risk is primarily evidence truthfulness and policy enforcement rather than missing module ownership. `docs/R3-HARDENING-INVENTORY.md` is the current inventory. The bounded sequence is: R3-B1/#{R3_B1_ISSUE} front-matter truthfulness, R3-B2/#{R3_B2_ISSUE} proof-state/coverage semantics, R3-B3/#{R3_B3_ISSUE} semantic test integrity/residual scanning, R3-B4/#{R3_B4_ISSUE} engineering-language enforcement/contract consolidation, and R3-B5/#{R3_B5_ISSUE} closeout/R4 entry.

A validation producer must declare whether its observations contribute proof or are audit/support-only. Proof-contributing normative FAIL cannot coexist with a successful owning gate. Test generators must fail closed when a requested semantic variation was not actually applied. Permanent residual/language checks must cover project-owned engineering sources that can affect runtime or test behavior while exempting only explicit migration documentation, negative tests, rendered academic content, and genuine upstream boundaries.

"""
        architecture_path.write_text(architecture.replace(marker, r3_section + marker), encoding="utf-8")

    replace_exact(
        "docs/ENGINEERING-LANGUAGE.md",
        "Permanent enforcement must be scoped so valid Brazilian academic content is not confused with engineering nomenclature. R2-B5 made `tests/checks/v3_api_residual.py` part of the permanent static contract, closing removed project API/runtime residuals while allowing classified migration documentation and genuine upstream boundaries. The final invariants are: zero Portuguese project-owned technical paths, zero removed Portuguese project API in runtime, zero Portuguese project-owned technical comments or diagnostics/UI, zero canonical examples using removed API, and zero archive/museum directories in the active tree. R3-A now inventories any remaining engineering-language enforcement gaps before bounded hardening work is defined.",
        f"Permanent enforcement must be scoped so valid Brazilian academic content is not confused with engineering nomenclature. R2-B5 made `tests/checks/v3_api_residual.py` part of the permanent static contract, but R3-A proved that current enforcement is incomplete: path checks do not yet police project-owned technical comments/diagnostics/UI, front-matter scripts still contain Portuguese technical diagnostics, and some machine scenario/profile identifiers remain Portuguese. R3-B4/#{R3_B4_ISSUE} owns the scoped permanent enforcement repair. The final invariants remain: zero Portuguese project-owned technical paths, zero removed Portuguese project API in runtime or behavior-affecting engineering generators, zero Portuguese project-owned technical comments or diagnostics/UI, zero canonical examples using removed API, and zero archive/museum directories in the active tree. Rendered academic Portuguese, official wording, bibliography data, literal output under test, and genuine upstream identifiers remain protected content/boundaries.",
    )

    replace_exact(
        "docs/CTAN-RELEASE.md",
        f"- Development gate: V3-R2 runtime/API migration is complete through B5/PR #249 at `{R2_PRODUCT_SHA}`. Static `33743809498`, Linux integration `33743809431`, and merged-main Linux release `{R2_RELEASE_RUN}` are green; the forwarding layer is absent and the migration guide/residual gate are permanent. V3-R3 is now active at inventory/planning only. A v3.0.0 CTAN upload still must not be performed: publication remains a later explicit action after R3, R4, and R5 reach the roadmap's release-ready state and the intended candidate is revalidated proportionally.",
        f"- Development gate: V3-R2 runtime/API migration is complete through B5/PR #249 at `{R2_PRODUCT_SHA}` and its canonical closeout baseline is `{SOURCE_MAIN_SHA}`. R3-A/#250 is complete and R3-B1/#{R3_B1_ISSUE} is active; B2–B5 remain required before R4. A v3.0.0 CTAN upload must not be performed during R3: publication remains a later explicit action after R3 hardening, R4 certification, and R5 foundation freeze/final documentation reach the roadmap's release-ready state and the intended candidate is revalidated proportionally.",
    )


def main() -> None:
    verify_entry()
    update_machine_state()
    write_primary_docs()
    update_secondary_docs()


if __name__ == "__main__":
    main()
