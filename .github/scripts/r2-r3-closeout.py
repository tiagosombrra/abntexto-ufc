#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

R2_PRODUCT_SHA = "ecd5926760080003148e8b1621dc8d4e4e8c7e5e"
R2_ENTRY_SHA = "bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261"
R2_HEAD_SHA = "2a8d7223a4aa9ffc80908adc9a84d0784f8dcaf4"
R2_ISSUE = 240
R2_PR = 249
R2_STATIC_RUN = 33743809498
R2_LINUX_RUN = 33743809431
R2_LINUX_JOB = 100611794384
R2_RELEASE_RUN = 33745603468
R2_RELEASE_JOB = 100617225595
R3_ISSUE = 250


def verify_entry() -> None:
    current_main = subprocess.check_output(
        ["git", "rev-parse", "origin/main"], cwd=ROOT, text=True
    ).strip()
    if current_main != R2_PRODUCT_SHA:
        raise SystemExit(
            f"R2/R3 closeout entry moved: expected {R2_PRODUCT_SHA}, got {current_main}"
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
        raise SystemExit(f"Expected text not found in {relative}: {old[:100]!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def update_machine_state() -> None:
    roadmap = load_json("release/v3-roadmap.json")
    roadmap.update(
        {
            "updated_at": "2026-09-03",
            "status": "ACTIVE",
            "phase": "V3-R3",
            "stage": "R3-A",
            "stage_name": "standards tests and engineering-language hardening inventory",
            "active_branch": "main",
            "next_action": (
                f"Execute V3-R3/R3-A issue #{R3_ISSUE}: inventory current standards, "
                "semantic test coverage, engineering-language enforcement and proof-state gaps; "
                "define bounded R3 implementation lots before any semantic or normative change."
            ),
        }
    )

    r2 = roadmap.setdefault("r2", {})
    r2.update(
        {
            "status": "DONE",
            "stage": "R2-B5",
            "stage_name": "final consumer migration and forwarding-layer removal",
            "closure_main_sha": R2_PRODUCT_SHA,
            "closure_issue": R2_ISSUE,
            "closure_pr": R2_PR,
        }
    )
    lots = r2.setdefault("lots", {})
    b5 = lots.setdefault("R2-B5", {})
    b5.update(
        {
            "status": "DONE",
            "issue": R2_ISSUE,
            "name": "final consumer migration and forwarding-layer removal",
            "product_entry_main_sha": R2_ENTRY_SHA,
            "implementation_head_sha": R2_HEAD_SHA,
            "pr": R2_PR,
            "merge_main_sha": R2_PRODUCT_SHA,
            "static_contract_run_id": R2_STATIC_RUN,
            "linux_integration_run_id": R2_LINUX_RUN,
            "linux_integration_job_id": R2_LINUX_JOB,
            "linux_integration_result": "PASS",
            "linux_release_check_run_id": R2_RELEASE_RUN,
            "linux_release_check_job_id": R2_RELEASE_JOB,
            "linux_release_check_result": "PASS=32 FAIL=0 SKIP=0",
            "forwarding_layer_removed": True,
            "migration_guide": "docs/MIGRATING-TO-V3.md",
            "permanent_residual_gate": "tests/checks/v3_api_residual.py",
            "runtime_alias_layer_added": False,
            "normative_semantics_changed": False,
            "proof_state_changed": False,
        }
    )

    roadmap["r2_b5_closeout"] = {
        "status": "DONE",
        "issue": R2_ISSUE,
        "pr": R2_PR,
        "product_entry_main_sha": R2_ENTRY_SHA,
        "implementation_head_sha": R2_HEAD_SHA,
        "merge_main_sha": R2_PRODUCT_SHA,
        "static_run_id": R2_STATIC_RUN,
        "linux_integration_run_id": R2_LINUX_RUN,
        "linux_integration_job_id": R2_LINUX_JOB,
        "linux_integration_result": "PASS",
        "linux_release_check_run_id": R2_RELEASE_RUN,
        "linux_release_check_job_id": R2_RELEASE_JOB,
        "linux_release_check_result": "PASS=32 FAIL=0 SKIP=0",
        "forwarding_layer_absent": True,
        "migration_guide_present": True,
        "permanent_residual_gate_present": True,
        "runtime_alias_layer_added": False,
        "normative_semantics_changed": False,
        "proof_state_changed": False,
    }

    roadmap["r3"] = {
        "status": "ACTIVE",
        "stage": "R3-A",
        "stage_name": "standards tests and engineering-language hardening inventory",
        "issue": R3_ISSUE,
        "entry_product_main_sha": R2_PRODUCT_SHA,
        "goal": (
            "Inventory the current standards/evidence model, semantic test suite and "
            "project-owned engineering-language enforcement before defining bounded R3 changes."
        ),
        "implementation_lots_defined": False,
        "constraints": [
            "preserve the closed v3 API and do not reintroduce runtime compatibility aliases",
            "do not change normative rule IDs values tolerances locators or proof state without explicit current evidence",
            "do not start R4 final certification R5 foundation freeze V3-A1/A2 or CTAN submission during R3-A",
            "classify gaps before editing runtime semantics",
        ],
        "exit": (
            "Current-state inventory is recorded, gaps are classified by owner/evidence, "
            "and bounded R3 implementation lots with proportional gates are defined."
        ),
    }
    roadmap["active_implementation_lot"] = {
        "stage": "R3-A",
        "issue": R3_ISSUE,
        "entry_product_main_sha": R2_PRODUCT_SHA,
        "status": "ACTIVE",
        "implementation_branch_rule": "branch from the merged R2 closeout control-plane checkpoint",
    }
    write_json("release/v3-roadmap.json", roadmap)

    api = load_json("release/v3-api-migration.json")
    api.update(
        {
            "status": "R2_DONE",
            "current_stage": "R2-CLOSED",
            "current_main_sha": R2_PRODUCT_SHA,
            "active_implementation_lot": {
                "stage": "R2-B5",
                "issue": R2_ISSUE,
                "status": "DONE",
                "merge_main_sha": R2_PRODUCT_SHA,
            },
            "r2_b5_closeout": {
                "status": "DONE",
                "issue": R2_ISSUE,
                "pr": R2_PR,
                "merge_main_sha": R2_PRODUCT_SHA,
                "static_run_id": R2_STATIC_RUN,
                "linux_integration_run_id": R2_LINUX_RUN,
                "linux_release_check_run_id": R2_RELEASE_RUN,
                "forwarding_layer_removed": True,
                "migration_guide": "docs/MIGRATING-TO-V3.md",
                "permanent_residual_gate": "tests/checks/v3_api_residual.py",
            },
            "retention": (
                "Retained as the machine-readable v3 API migration mapping and as input "
                "to the permanent fail-closed residual API gate."
            ),
        }
    )
    write_json("release/v3-api-migration.json", api)

    tests = load_json("release/v3-test-migration.json")
    tests.update(
        {
            "status": "R2_CONSUMER_MIGRATION_DONE",
            "current_stage": "R2-CLOSED",
            "r2_b5_closeout": {
                "status": "DONE",
                "issue": R2_ISSUE,
                "pr": R2_PR,
                "merge_main_sha": R2_PRODUCT_SHA,
                "static_run_id": R2_STATIC_RUN,
                "linux_integration_run_id": R2_LINUX_RUN,
                "linux_release_check_run_id": R2_RELEASE_RUN,
                "permanent_residual_gate": "tests/checks/v3_api_residual.py",
            },
        }
    )
    tests.setdefault("r2_api_consumer_policy", {})["active_lot"] = None
    tests["r2_api_consumer_policy"]["final_residual_lot"] = "R2-B5"
    write_json("release/v3-test-migration.json", tests)

    paths = load_json("release/v3-path-migration.json")
    paths.update(
        {
            "status": "R1_PATHS_DONE_R2_RUNTIME_ABSORPTION_DONE",
            "current_stage": "R2-CLOSED",
            "r2_b5_closeout": {
                "status": "DONE",
                "issue": R2_ISSUE,
                "pr": R2_PR,
                "merge_main_sha": R2_PRODUCT_SHA,
                "removed_path": "abntexto-ufc/public-api.def",
                "class_load_removed": True,
            },
        }
    )
    remaining = paths.pop("remaining_runtime_path_action", None)
    if remaining is not None:
        remaining["status"] = "DONE"
        remaining["closure_main_sha"] = R2_PRODUCT_SHA
        paths["completed_runtime_path_action"] = remaining
    write_json("release/v3-path-migration.json", paths)


def write_primary_docs() -> None:
    handoff = f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- R2-B5 product merge: `{R2_PRODUCT_SHA}` through PR #{R2_PR}.
- R2-B5 Static contract: `{R2_STATIC_RUN}` = PASS.
- R2-B5 Linux integration: `{R2_LINUX_RUN}` = PASS.
- Post-merge Linux release check: `{R2_RELEASE_RUN}` = `PASS=32 FAIL=0 SKIP=0`.
- Active phase: **V3-R3**.
- Active stage: **R3-A — standards, tests, and engineering-language hardening inventory**.
- Active issue: **#{R3_ISSUE}**.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## R2 closure

| Lot | Status | Main checkpoint | Validation |
|---|---|---|---|
| B1 | DONE | `ded5e77733795aa2958606e899d4e27f12f64df4` | Linux `33668283890` = `30/0/0` |
| B2 | DONE | `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout `0650845b922271fc134d20ef2a8c36ebb999ef91` | Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0` |
| B3 | DONE | `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Static `33704346418`; Linux `33704346429` = `30/0/0` |
| B4 | DONE | `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` | Static `33736117556`; Linux `33736117558` = `30/0/0` |
| B5 | DONE | `{R2_PRODUCT_SHA}` | Static `{R2_STATIC_RUN}`; Linux `{R2_LINUX_RUN}` PASS; release `{R2_RELEASE_RUN}` = `32/0/0` |

R2-B5 removed `abntexto-ufc/public-api.def` and its class load, added `docs/MIGRATING-TO-V3.md`, and made `tests/checks/v3_api_residual.py` a permanent fail-closed source gate. No runtime compatibility alias layer was added.

## Current runtime/API state

The v3 project API is directly owned by its behavior modules. The forwarding-only layer is absent. Removed v2 project API is migration-documentation material only; active runtime/template/test consumers are protected by the permanent residual gate.

## Immediate action

Execute issue #{R3_ISSUE} as **R3-A inventory/planning only**. Inventory current `standards/` authority/proof state, semantic test coverage and engineering-language enforcement, classify gaps, then define bounded R3 implementation lots. Do not infer or pre-stage later R3 lots before the inventory establishes them.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, expected values, tolerances, locators or proof state without explicit current evidence. Do not start R4 final certification, R5 foundation freeze, V3-A1/A2 scientific-article work, or CTAN submission during R3-A.
"""
    (ROOT / "docs/HANDOFF-V3.0.0.md").write_text(handoff, encoding="utf-8")

    roadmap = f"""# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-03

## Status

**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A standards/tests/engineering-language hardening inventory.**

R2 closed on product merge `{R2_PRODUCT_SHA}` after PR #{R2_PR}, Static `{R2_STATIC_RUN}`, Linux integration `{R2_LINUX_RUN}`, and post-merge Linux release check `{R2_RELEASE_RUN}` = `PASS=32 FAIL=0 SKIP=0`. Active R3 entry issue: #{R3_ISSUE}. Machine authority: `release/v3-roadmap.json`.

## Roadmap summary

| Stage | Status | Checkpoint / issue | Result | Remaining work |
|---|---|---|---|---|
| R1-S0 | DONE | repository sanitation | History governance rebaselined | None |
| R1-S1 | DONE | `1c7291592689f10a0e6fb043d404597ae8e53c02` | Control plane repaired | None |
| R1-S2 | DONE | `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1` | v3 promoted to `main` | None |
| R1-B1 | DONE | `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd` | Canonical physical naming | None |
| R1-B2 | DONE | `03d7f5ceb1a325d26c712ba5e619ee85530a022b` | Legacy purge/minimization | None |
| R1-B3 | DONE | `7a3b018a43630ed46b375117790acc732ae67b40` | Semantic/path-consumer closure | None |
| R1-B4 | DONE | `1a126c37653728941ce1ada762376c5fec69cb02` | Tools/validator/metadata/language rebaseline | None |
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` | Deterministic release/public bundles | CTAN submission remains later |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` | Permanent static contract | None |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` | Permanent optimized workflows | Optional branch-rule enforcement |
| R1-B8 | DONE | candidate `9b1752565ac217c04ffa22a9ef272cdf078af380` | Windows/font/Unicode/embedding/PDF-A-2b certification | None |
| V3-R1 closeout | DONE | PR #233 → `0a2c2c3879986ca27b731f54b974db12524258df` | R1 closed | None |
| R2-A | DONE | issue #232 | Direct owners/upstream boundaries/lots classified | None |
| R2-B1 | DONE | PR #236 → `ded5e77733795aa2958606e899d4e27f12f64df4` | Setup/state direct ownership | None |
| R2-B2 | DONE | PR #242 / closeout #243 | Academic/front-matter direct ownership | None |
| R2-B3 | DONE | PR #245 → `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Structural/object direct ownership | None |
| R2-B4 | DONE | PR #247 → `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` | Bibliography/back-matter direct ownership | None |
| R2-B5 | DONE | PR #{R2_PR} → `{R2_PRODUCT_SHA}` | Forwarding layer removed; migration guide + permanent residual gate | None |
| V3-R2 closeout | DONE | issue #{R2_ISSUE} | v3 project API/runtime migration closed | None |
| R3-A | ACTIVE | issue #{R3_ISSUE} | Standards/tests/language current-state inventory and lot definition | Complete inventory; classify gaps; define bounded R3 lots |
| V3-R3 implementation | PENDING | defined by R3-A evidence | Semantic hardening | Do not predefine lots before inventory |
| V3-R4 | BLOCKED | — | Final certification | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and final docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |
| CTAN submission | FUTURE | explicit release action | No upload yet | Release-ready stage only |

## R2 closure record

R2-A classified direct owners and upstream boundaries. B1 moved setup/state to direct ownership; B2 moved academic/front-matter rendering; B3 moved structural/object APIs and hooks; B4 moved bibliography/reference/glossary/index APIs. B5 removed the empty forwarding-only `public-api.def`, removed its class load, published the v3 migration guide, and added the permanent fail-closed residual API gate.

B5 PR #{R2_PR} head `{R2_HEAD_SHA}` passed Static `{R2_STATIC_RUN}` and Linux integration `{R2_LINUX_RUN}` before squash merge `{R2_PRODUCT_SHA}`. The merged-main `Linux release check` `{R2_RELEASE_RUN}` then passed all 32 release checks. No runtime aliases, normative semantic changes, or proof-state changes were introduced by B5.

The pre-existing observational `FRONTMATTER-EVIDENCE` FAIL records remain baseline observations inside passing aggregate gates; R2 did not promote them into normative failures.

## R3 entry rule

R3 is intentionally activated through **R3-A inventory/planning**, because the prior roadmap defined the R3 objective but did not define trustworthy implementation lots. Issue #{R3_ISSUE} must first inventory:

- current `standards/` source authority, rule coverage, currency and proof state;
- semantic test/check/document coverage, duplicated/orphaned assertions and missing invariants;
- project-owned engineering-language enforcement across runtime, tests, tools, validator, documentation and machine contracts;
- gaps that require new normative evidence versus engineering-only hardening.

Only after that inventory may bounded R3 implementation lots and proportional gates be recorded.

## Immediate action

Execute **R3-A issue #{R3_ISSUE}**. Do not start R4, R5, V3-A1/A2, or CTAN submission and do not change normative semantics merely to satisfy an inventory finding.
"""
    (ROOT / "docs/ROADMAP-V3.0.0.md").write_text(roadmap, encoding="utf-8")


def update_secondary_docs() -> None:
    replace_exact(
        "README.md",
        "**V3-R1 is DONE. V3-R2 is ACTIVE in R2-B5 — final consumer migration and forwarding-layer removal, tracked by issue #240.**",
        f"**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE in R3-A — standards/tests/engineering-language hardening inventory, tracked by issue #{R3_ISSUE}.**",
    )
    replace_exact(
        "README.md",
        "The R2-B4 product merge is `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` after PR #247 passed Static `33736117556` and Linux `33736117558` at `PASS=30 FAIL=0 SKIP=0`; this is the product entry for the B4-to-B5 closeout. The certified R1 candidate is `9b1752565ac217c04ffa22a9ef272cdf078af380`. Windows run `33649620219` built the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX `template/main.tex` matrix. Final Linux inspection run `33655108349` passed literal institutional text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b for all four artifacts. No runtime/API, normative semantics or proof-state change was required, and no proprietary Microsoft font was redistributed.",
        f"R2 closed through B5/PR #{R2_PR} at `{R2_PRODUCT_SHA}`. B5 Static `{R2_STATIC_RUN}` and Linux integration `{R2_LINUX_RUN}` passed before merge; the merged-main Linux release check `{R2_RELEASE_RUN}` then passed `PASS=32 FAIL=0 SKIP=0`. The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; its Windows/Linux font, Unicode, embedding, and PDF/A-2b certification record remains unchanged. R3-A is an inventory/planning stage and does not itself recertify the product.",
    )
    replace_exact(
        "README.md",
        "R2-A and R2-B1 through R2-B4 completed direct ownership of setup/state, academic/front-matter, structural/object, and bibliography/back-matter surfaces. R2-B5 now removes the empty forwarding layer, closes residual engineering identifiers and produces the v3 migration guide. See `docs/R2-API-OWNERSHIP.md` for the bounded migration sequence.",
        "R2-A and R2-B1 through R2-B5 are complete. The v3 public/runtime API is directly owned, the forwarding-only layer is absent, `docs/MIGRATING-TO-V3.md` documents the breaking migration, and `tests/checks/v3_api_residual.py` permanently rejects removed project API in active consumers. R3-A now inventories standards, semantic test coverage, and engineering-language enforcement before bounded hardening lots are defined.",
    )
    replace_exact(
        "README.md",
        "R2-A and R2-B1 through R2-B4 are complete. B4 PR #247 merged at `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` after full Linux integration `33736117558` passed `PASS=30 FAIL=0 SKIP=0`. V3-R2/R2-B5 is active through issue #240.",
        f"R2-A and R2-B1 through R2-B5 are complete. B5 PR #{R2_PR} merged at `{R2_PRODUCT_SHA}` after Static `{R2_STATIC_RUN}` and Linux integration `{R2_LINUX_RUN}` passed; merged-main release run `{R2_RELEASE_RUN}` passed `PASS=32 FAIL=0 SKIP=0`. V3-R3/R3-A is active through issue #{R3_ISSUE}.",
    )

    replace_exact(
        "AGENTS.md",
        "- V3-R2 is ACTIVE in R2-B5 via issue #240. R2-A plus R2-B1 through R2-B4 are complete and recorded in `docs/R2-API-OWNERSHIP.md`.",
        f"- V3-R2 is DONE through R2-B5/PR #{R2_PR} at `{R2_PRODUCT_SHA}`. R2-A plus R2-B1 through R2-B5 are complete and recorded in `docs/R2-API-OWNERSHIP.md`.",
    )
    replace_exact(
        "AGENTS.md",
        "- R2-B4 is DONE through PR #247 at `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`; final Static `33736117556` and Linux `33736117558` passed `PASS=30 FAIL=0 SKIP=0`. Bibliography/reference/glossary/index commands are directly owned and `public-api.def` is empty.",
        "- R2-B4 is DONE through PR #247 at `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`; final Static `33736117556` and Linux `33736117558` passed `PASS=30 FAIL=0 SKIP=0`. Bibliography/reference/glossary/index commands are directly owned; B4 left `public-api.def` empty for its B5 physical removal.",
    )
    replace_exact(
        "AGENTS.md",
        "- R2-B5/#240 owns the final residual scan, physical removal of the empty `public-api.def` and its class load, migration-guide generation and R2 contract reconciliation. Do not add a runtime compatibility layer.",
        f"- R2-B5/#240 is DONE. `public-api.def` and its class load are absent; `docs/MIGRATING-TO-V3.md` is the user migration guide; `tests/checks/v3_api_residual.py` is the permanent fail-closed residual gate. Static `{R2_STATIC_RUN}`, Linux `{R2_LINUX_RUN}`, and post-merge release `{R2_RELEASE_RUN}` are green.",
    )
    replace_exact(
        "AGENTS.md",
        "- Preserve rendered behavior and normative rule IDs, values, tolerances, locators and proof state during R2 unless explicit new evidence authorizes a normative change.",
        f"- V3-R3 is ACTIVE in R3-A via issue #{R3_ISSUE}. R3-A is inventory/planning only: classify standards/proof-state, semantic-test, and engineering-language gaps before defining implementation lots.\n- Preserve rendered behavior and normative rule IDs, values, tolerances, locators and proof state unless explicit current evidence authorizes a normative change.",
    )
    replace_exact(
        "AGENTS.md",
        "- Do not perform actual CTAN submission during R2 implementation.",
        "- Do not perform actual CTAN submission before the roadmap reaches its explicit release-ready stage.",
    )

    replace_exact(
        "docs/ARCHITECTURE.md",
        "Updated: 2026-09-02",
        "Updated: 2026-09-03",
    )
    replace_exact(
        "docs/ARCHITECTURE.md",
        "A project-owned internal control sequence has one behavior owner. Public commands are implemented directly by the module that owns the behavior; no forwarding-only compatibility layer is part of the final v3 runtime. `public-api.def` is therefore transitional R2 debt and must disappear after direct ownership is absorbed.",
        "A project-owned internal control sequence has one behavior owner. Public commands are implemented directly by the module that owns the behavior; no forwarding-only compatibility layer is part of the final v3 runtime. R2-B5 completed this invariant: `public-api.def` and its class load are absent.",
    )
    replace_exact(
        "docs/ARCHITECTURE.md",
        "The target architecture above is implemented through bounded owner-based lots documented in `docs/R2-API-OWNERSHIP.md`. R2-A and B1 through B4 are complete. B4 merged through PR #247 at `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261` after Static `33736117556` and Linux `33736117558` passed `PASS=30 FAIL=0 SKIP=0`. Bibliography/reference/glossary/index commands are now directly owned; `public-api.def` is empty. R2-B5/#240 is active and removes that forwarding-only file/load, closes residual project-owned runtime/internal naming debt, generates the migration guide, and reconciles the R2 contracts. Template and test consumers move atomically with each behavior owner.",
        f"The target architecture above was implemented through bounded owner-based lots documented in `docs/R2-API-OWNERSHIP.md`. R2-A and B1 through B5 are complete. B5 merged through PR #{R2_PR} at `{R2_PRODUCT_SHA}`, removed the forwarding-only file/load, published `docs/MIGRATING-TO-V3.md`, and added `tests/checks/v3_api_residual.py` as a permanent fail-closed residual gate. Template and test consumers moved atomically with each behavior owner.",
    )
    replace_exact(
        "docs/ARCHITECTURE.md",
        "R1-BLOCK-7 and R1-BLOCK-8 are DONE. The permanent orchestration surface is exactly `Static contract`, `Linux integration`, and `Linux release check`, each delegating to its repository-owned entry point (`make static-check`, `make check`, and `make release-check`). B7-D confirmed read-only permissions, immutable action pins, bounded concurrency, stable status semantics, and zero temporary workflow residue. The current `Stable branches` ruleset has no required-status rule; the recorded recommendation is to require `Static contract` and `Linux integration`, while `Linux release check` remains a post-merge/manual release gate. B8 certified complete candidate `9b1752565ac217c04ffa22a9ef272cdf078af380` across Times New Roman/Arial × pdfLaTeX/LuaLaTeX with final literal text-family, math-policy, Unicode, embedding and PDF/A-2b inspection. V3-R2 is active in R2-B3; B1/B2 forwarding debt has been absorbed, and `public-api.def` now contains only remaining B3/B4 transitional forwarding until canonical public behavior is fully owned and the file is removed in B5.",
        f"R1-BLOCK-7 and R1-BLOCK-8 are DONE. The permanent orchestration surface is exactly `Static contract`, `Linux integration`, and `Linux release check`, each delegating to its repository-owned entry point (`make static-check`, `make check`, and `make release-check`). B7-D confirmed read-only permissions, immutable action pins, bounded concurrency, stable status semantics, and zero temporary workflow residue. The current `Stable branches` ruleset has no required-status rule; the recorded recommendation is to require `Static contract` and `Linux integration`, while `Linux release check` remains a post-merge/manual release gate. B8 certified complete candidate `9b1752565ac217c04ffa22a9ef272cdf078af380` across Times New Roman/Arial × pdfLaTeX/LuaLaTeX with final literal text-family, math-policy, Unicode, embedding and PDF/A-2b inspection. V3-R2 is DONE through B5 at `{R2_PRODUCT_SHA}`; the forwarding-only API layer is absent and permanent residual enforcement is part of `make static-check`. V3-R3 is active only at the R3-A inventory/planning boundary.",
    )
    replace_exact(
        "docs/ARCHITECTURE.md",
        "`docs/` contains current engineering and maintainer documentation. `release/` contains current machine-readable migration/release state plus source material required to construct current release candidates, such as `release/ctan/`. A migration contract remains tracked only while an active migration consumes it; after use it is removed or consolidated.",
        "`docs/` contains current engineering and maintainer documentation. `release/` contains current machine-readable migration/release state plus source material required to construct current release candidates, such as `release/ctan/`. A closed migration mapping may remain only when a permanent gate or the active reconstruction control plane still consumes it; otherwise it is removed or consolidated rather than kept as a historical ledger.",
    )

    ownership = f"""# V3-R2 API Ownership Inventory

Updated: 2026-09-03

## Purpose

This document records the completed R2 owner map and bounded B1–B5 migration sequence. It is engineering control-plane documentation, not a normative formatting source.

R2-A entry: `0a2c2c3879986ca27b731f54b974db12524258df`. B1 merge: `ded5e77733795aa2958606e899d4e27f12f64df4`. B2 merge: `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`. B3 merge: `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. B4 merge: `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`. B5 merge/R2 product closure: `{R2_PRODUCT_SHA}`. Mapping authority retained for permanent residual enforcement: `release/v3-api-migration.json`.

## Final-state finding

R2 is **DONE**. Every canonical v3 project API/runtime surface has a direct behavior owner. `abntexto-ufc/public-api.def` and its class load are absent. User migration is documentation-only through `docs/MIGRATING-TO-V3.md`; no runtime alias layer exists. `tests/checks/v3_api_residual.py` permanently rejects removed project-owned API in active runtime/template/test sources.

## Responsibility ownership

| Runtime surface | Direct owner | R2 status |
|---|---|---|
| setup, profile state, metadata | `core.def` | B1 DONE |
| fonts | `fonts.def` | B1 DONE |
| optional module state | `modules.def` | B1/B4 DONE |
| layout/structural lists/section hook | `layout.def` | B1/B2/B3 DONE |
| front matter + definition list | `frontmatter.def` | B2/B3 DONE |
| institutional assets | `institutional.def` | B1 DONE |
| academic cover/title/catalog card | `academic-works.def` | B1/B2 DONE |
| research-project specialization | `research-projects.def` | B1/B2 DONE |
| objects/source/note/lists/listing/minted/algorithm/object hook | `objects.def` | B3 DONE |
| ABNTexto definition-list integration/upstream boundary | `integrations/abntexto.def` | B3 DONE |
| bibliography resources/references | `bibliography.def` | B4 DONE |
| glossary/index | `backmatter.def` | B4 DONE |
| forwarding-only layer | — | B5 REMOVED |

## Upstream boundaries

Dependency-owned identifiers remain only where required by the dependency contract, including `grafico` / `quadro` and upstream commands such as `\\legend`, `\\keywords`, `\\appendix`, `\\annex`, `\\pretextual`, and `\\textual`. Rendered Portuguese labels remain protected document content.

## Lots and evidence

| Lot | Status | Product evidence |
|---|---|---|
| R2-B1 | DONE | issue #234 / PR #236; Linux `33668283890` = `30/0/0` |
| R2-B2 | DONE | issue #237 / PR #242; Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0` |
| R2-B3 | DONE | issue #238 / PR #245; Static `33704346418`; Linux `33704346429` = `30/0/0` |
| R2-B4 | DONE | issue #239 / PR #247; Static `33736117556`; Linux `33736117558` = `30/0/0` |
| R2-B5 | DONE | issue #{R2_ISSUE} / PR #{R2_PR}; Static `{R2_STATIC_RUN}`; Linux `{R2_LINUX_RUN}` PASS; merged-main release `{R2_RELEASE_RUN}` = `32/0/0` |

B5 removed the forwarding file/load, completed the residual project-owned API sweep, created the migration guide, and made residual scanning permanent. No runtime aliases, normative semantics, locator policy, tolerances, or proof state changed.

## Invariants after R2

Project-owned engineering identifiers are English; rendered Brazilian academic content remains as required. Genuine upstream non-English identifiers remain only at explicit integration boundaries. Removed v2 project API remains documentation/migration-contract material only. Proprietary Microsoft fonts stay external. CTAN submission remains a later explicit release action.
"""
    (ROOT / "docs/R2-API-OWNERSHIP.md").write_text(ownership, encoding="utf-8")

    replace_exact(
        "docs/CTAN-RELEASE.md",
        "- Development gate: V3-R2 runtime/API migration is active in R2-B5. R2-B4 bibliography/back-matter ownership is complete through PR #247 at `bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261`, with Static `33736117556` PASS and Linux `33736117558` `PASS=30 FAIL=0 SKIP=0`. Only the B5 forwarding-layer removal, residual migration closure and migration documentation remain before R2 can close. A v3.0.0 CTAN upload must not be performed from an intermediate R2 lot; publication remains a later explicit action after the roadmap reaches its release-ready stage and the intended candidate is revalidated proportionally.",
        f"- Development gate: V3-R2 runtime/API migration is complete through B5/PR #{R2_PR} at `{R2_PRODUCT_SHA}`. Static `{R2_STATIC_RUN}`, Linux integration `{R2_LINUX_RUN}`, and merged-main Linux release `{R2_RELEASE_RUN}` are green; the forwarding layer is absent and the migration guide/residual gate are permanent. V3-R3 is now active at inventory/planning only. A v3.0.0 CTAN upload still must not be performed: publication remains a later explicit action after R3, R4, and R5 reach the roadmap's release-ready state and the intended candidate is revalidated proportionally.",
    )

    replace_exact(
        "docs/ENGINEERING-LANGUAGE.md",
        "Temporary migration contracts may exist only while the active migration consumes them.",
        "Closed migration mappings may remain only when a permanent enforcement gate or the active reconstruction control plane consumes them; otherwise they are consolidated or removed.",
    )
    replace_exact(
        "docs/ENGINEERING-LANGUAGE.md",
        "Permanent enforcement must be scoped so valid Brazilian academic content is not confused with engineering nomenclature. The final invariants are: zero Portuguese project-owned technical paths, zero removed Portuguese project API in runtime, zero Portuguese project-owned technical comments or diagnostics/UI, zero canonical examples using removed API, and zero archive/museum directories in the active tree.",
        "Permanent enforcement must be scoped so valid Brazilian academic content is not confused with engineering nomenclature. R2-B5 made `tests/checks/v3_api_residual.py` part of the permanent static contract, closing removed project API/runtime residuals while allowing classified migration documentation and genuine upstream boundaries. The final invariants are: zero Portuguese project-owned technical paths, zero removed Portuguese project API in runtime, zero Portuguese project-owned technical comments or diagnostics/UI, zero canonical examples using removed API, and zero archive/museum directories in the active tree. R3-A now inventories any remaining engineering-language enforcement gaps before bounded hardening work is defined.",
    )


def main() -> None:
    verify_entry()
    update_machine_state()
    write_primary_docs()
    update_secondary_docs()


if __name__ == "__main__":
    main()
