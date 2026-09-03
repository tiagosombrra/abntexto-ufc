#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-03"
B4_PRODUCT_ENTRY = "fb71eb0cb50f065d75aec6bbc704dcaf9091d1df"
B4_CONTROL_ENTRY = "ab900797836eb068b3f100574759816eadb039d5"
B4_HEAD = "c2afa9e283380a1ae008638c73d12561eb97e537"
B4_MERGE = "bbf34a3d0cef3a402b6847c7d0a6f5f31f8b4261"
STATIC_RUN = 33736117556
STATIC_JOB = 100586938889
LINUX_RUN = 33736117558
LINUX_JOB = 100587276948
LINUX_RESULT = "PASS=30 FAIL=0 SKIP=0"
B5_NAME = "final consumer migration and forwarding-layer removal"


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def save_json(path: str, data) -> None:
    (ROOT / path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"{path}: expected exactly one replacement, found {count}: {old!r}"
        )
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def changed_paths() -> set[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return {line for line in result.stdout.splitlines() if line}


b4_closeout = {
    "status": "DONE",
    "issue": 239,
    "pr": 247,
    "product_entry_main_sha": B4_PRODUCT_ENTRY,
    "control_plane_entry_main_sha": B4_CONTROL_ENTRY,
    "implementation_head_sha": B4_HEAD,
    "merge_main_sha": B4_MERGE,
    "static_run_id": STATIC_RUN,
    "static_job_id": STATIC_JOB,
    "linux_integration_run_id": LINUX_RUN,
    "linux_integration_job_id": LINUX_JOB,
    "linux_integration_result": LINUX_RESULT,
    "fail_closed_linux_runs": [
        {
            "run_id": 33708110732,
            "result": "PASS=29 FAIL=1 SKIP=0",
            "finding": "generic index evidence locator was ambiguous",
        },
        {
            "run_id": 33731936681,
            "result": "PASS=29 FAIL=1 SKIP=0",
            "finding": "synthetic locator was not rendered by imakeidx",
        },
        {
            "run_id": 33733036724,
            "result": "PASS=29 FAIL=1 SKIP=0",
            "finding": "indexname override did not control the rendered imakeidx heading",
        },
    ],
    "heading_observer_repaired": True,
    "heading_observer_final_rendered_text": "ÍNDICE REMISSIVO",
    "heading_observer_final_delta_pt": 0.0002,
    "runtime_alias_layer_added": False,
    "normative_semantics_changed": False,
    "locator_policy_changed": False,
    "reference_tolerances_changed": False,
    "proof_state_changed": False,
}

roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("stage") != "R2-B4":
    raise SystemExit(f"roadmap top stage drift: {roadmap.get('stage')}")
nested_stage = roadmap.get("r2", {}).get("stage")
if nested_stage not in {"R2-B3", "R2-B4"}:
    raise SystemExit(f"roadmap nested stage unexpected: {nested_stage}")
roadmap["updated_at"] = DATE
roadmap["stage"] = "R2-B5"
roadmap["stage_name"] = B5_NAME
roadmap["next_action"] = (
    "Execute R2-B5 issue #240: remove public-api.def and its class load, run "
    "fail-closed residual API/engineering-language scans, create "
    "docs/MIGRATING-TO-V3.md from the authoritative migration contract, reconcile "
    "consumed migration contracts, and close V3-R2 only after current-state gates "
    "are green."
)
r2 = roadmap["r2"]
r2["stage"] = "R2-B5"
r2["stage_name"] = B5_NAME
r2["lots"]["R2-B4"].update(
    {
        "status": "DONE",
        "issue": 239,
        "name": "bibliography back-matter API and plumbing internalization",
        "product_entry_main_sha": B4_PRODUCT_ENTRY,
        "control_plane_entry_main_sha": B4_CONTROL_ENTRY,
        "implementation_head_sha": B4_HEAD,
        "pr": 247,
        "merge_main_sha": B4_MERGE,
        "static_contract_run_id": STATIC_RUN,
        "static_contract_job_id": STATIC_JOB,
        "linux_integration_run_id": LINUX_RUN,
        "linux_integration_job_id": LINUX_JOB,
        "linux_integration_result": LINUX_RESULT,
        "runtime_alias_layer_added": False,
        "normative_semantics_changed": False,
        "proof_state_changed": False,
    }
)
r2["lots"]["R2-B5"].update(
    {
        "status": "ACTIVE",
        "issue": 240,
        "name": B5_NAME,
        "product_entry_main_sha": B4_MERGE,
    }
)
roadmap["r2_b4_closeout"] = b4_closeout
roadmap["active_implementation_lot"] = {
    "stage": "R2-B5",
    "issue": 240,
    "product_entry_main_sha": B4_MERGE,
    "status": "ACTIVE",
    "implementation_branch_rule": (
        "branch from the merged B4-to-B5 control-plane closeout checkpoint"
    ),
}
save_json("release/v3-roadmap.json", roadmap)

api = load_json("release/v3-api-migration.json")
if api.get("current_stage") != "R2-B4":
    raise SystemExit(f"api stage drift: {api.get('current_stage')}")
api["status"] = "R2_B4_DONE_R2_B5_ACTIVE"
api["current_stage"] = "R2-B5"
api["current_stage_goal"] = B5_NAME
api["current_main_sha"] = B4_MERGE
api["r2_b4_closeout"] = b4_closeout
api["active_implementation_lot"] = {
    "stage": "R2-B5",
    "issue": 240,
    "product_entry_main_sha": B4_MERGE,
    "status": "ACTIVE",
}
save_json("release/v3-api-migration.json", api)

tests = load_json("release/v3-test-migration.json")
if tests.get("current_stage") != "R2-B4":
    raise SystemExit(f"test stage drift: {tests.get('current_stage')}")
tests["current_stage"] = "R2-B5"
tests["r2_api_consumer_policy"]["active_lot"] = "R2-B5"
tests["r2_b4_closeout"] = {
    **b4_closeout,
    "consumer_migration": (
        "bibliography/back-matter owners, template/tests and shared heading "
        "observer migrated atomically"
    ),
}
tests["active_implementation_lot"] = {
    "stage": "R2-B5",
    "issue": 240,
    "product_entry_main_sha": B4_MERGE,
}
save_json("release/v3-test-migration.json", tests)

paths = load_json("release/v3-path-migration.json")
if paths.get("current_stage") != "R2-B4":
    raise SystemExit(f"path stage drift: {paths.get('current_stage')}")
paths["current_stage"] = "R2-B5"
remaining = paths.get("remaining_runtime_path_action", {})
if remaining.get("path") != "abntexto-ufc/public-api.def":
    raise SystemExit(f"unexpected remaining runtime path: {remaining}")
if remaining.get("planned_lot") != "R2-B5":
    raise SystemExit(f"unexpected remaining path lot: {remaining}")
paths["r2_b4_closeout"] = {
    "status": "DONE",
    "issue": 239,
    "pr": 247,
    "control_plane_entry_main_sha": B4_CONTROL_ENTRY,
    "implementation_head_sha": B4_HEAD,
    "merge_main_sha": B4_MERGE,
    "public_api_state": (
        "empty transitional file retained for physical removal in R2-B5"
    ),
    "next_lot": "R2-B5",
    "next_issue": 240,
}
save_json("release/v3-path-migration.json", paths)

(ROOT / "docs/HANDOFF-V3.0.0.md").write_text(
    f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: {DATE}

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- R2-B4 product merge on `main`: `{B4_MERGE}`.
- B4 control-plane entry used by PR #247: `{B4_CONTROL_ENTRY}`.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-B5 — final consumer migration and forwarding-layer removal**.
- Active issue: **#240**.
- R2-B4 / #239: **DONE through PR #247; issue closed completed**.
- R2-B3 / #238, R2-B2 / #237, R2-B1 / #234 and R2-A / #232: **DONE**.
- Certified R1 candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, machine contracts, this handoff, the roadmap and `AGENTS.md` must agree. Disagreement fails closed.

## R2 evidence

| Lot | Status | Main checkpoint | Validation |
|---|---|---|---|
| B1 | DONE | `ded5e77733795aa2958606e899d4e27f12f64df4` | Linux `33668283890` = `30/0/0` |
| B2 | DONE | `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout `0650845b922271fc134d20ef2a8c36ebb999ef91` | Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0` |
| B3 | DONE | `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Static `33704346418`; Linux `33704346429` = `30/0/0` |
| B4 | DONE | `{B4_MERGE}` | Static `{STATIC_RUN}`; Linux `{LINUX_RUN}` = `30/0/0` |
| B5 | ACTIVE | issue #240; product entry `{B4_MERGE}` | implementation pending after this closeout merges |

## B4 closure finding

Bibliography/reference/glossary/index public commands are direct owners. The repeated B4 `29/1/0` runs were fail-closed evidence-observer failures, not runtime layout regressions. The final observer measures the full rendered heading line: `ÍNDICE REMISSIVO` passed centered with delta `0.0002 pt`; validator locator policy, tolerances and proof state remained unchanged.

## Current runtime/API state

All semantic public API surfaces migrated in B1–B4 are directly owned. `public-api.def` is now an empty transitional file and the class still loads it once. B5 removes that file and load, performs the final project-owned Portuguese runtime/internal residual scan, reconciles the migration contracts as consumed, and creates `docs/MIGRATING-TO-V3.md` from the authoritative mappings.

## Immediate action

Execute #240 only from the merged B4-to-B5 control-plane checkpoint. Remove `public-api.def` and its class load, validate the final residual boundaries, generate the migration guide, and run proportional permanent gates. Do not mark R2 closed until the B5 implementation is merged and its closure evidence is reconciled.

## Hard boundaries

No runtime aliases; preserve rendered Portuguese academic wording and genuine upstream APIs; no normative rule/value/tolerance/locator-policy/proof-state changes without evidence; no proprietary-font redistribution; no CTAN submission during R2.
""",
    encoding="utf-8",
)

(ROOT / "docs/ROADMAP-V3.0.0.md").write_text(
    f"""# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: {DATE}

## Status

**V3-R1 DONE. V3-R2 ACTIVE — R2-B5 final consumer migration and forwarding-layer removal.**

R2-B4 product merge on `main`: `{B4_MERGE}`. Active implementation issue: #240. Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`. Machine authority: `release/v3-roadmap.json`.

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
| R2-B1 | DONE | PR #236 → `ded5e77733795aa2958606e899d4e27f12f64df4` | Setup/state direct ownership; `30/0/0` | None |
| R2-B2 | DONE | PR #242 → `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout #243 → `0650845b922271fc134d20ef2a8c36ebb999ef91` | Academic/front-matter direct ownership; `30/0/0`; release `32/0/0` | None |
| R2-B3 | DONE | issue #238; PR #245 → `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` | Structural/object direct ownership; Linux `33704346429` = `30/0/0` | None |
| R2-B4 | DONE | issue #239; PR #247 → `{B4_MERGE}` | Bibliography/reference/glossary/index direct ownership; Static `{STATIC_RUN}`; Linux `{LINUX_RUN}` = `30/0/0` | None |
| R2-B5 | ACTIVE | issue #240; product entry `{B4_MERGE}` | Final residual migration and forwarding-layer removal | Remove `public-api.def`/class load; residual scan; migration guide; close R2 |
| V3-R3 | BLOCKED | no issue activated yet | Standards/tests/language semantic hardening | After R2 |
| V3-R4 | BLOCKED | — | Final certification | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and final docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |
| CTAN submission | FUTURE | explicit release action | No upload during R2 | Release-ready stage only |

## R1 certification record

R1-B8 certified the complete `template/main.tex` matrix on Windows run `33649620219` and final Linux inspection run `33655108349`. Literal institutional text-family identity, engine-appropriate math-font policy, Unicode extraction, embedding and PDF/A-2b passed. PR #233 closed R1 with Static `33656361564` and Linux integration `33656361474`, `PASS=30 FAIL=0 SKIP=0`.

## R2 progress record

R2-A established direct behavior ownership and the B1–B5 sequence. `public-api.def` is transitional forwarding debt, not a behavior owner.

R2-B1 moved canonical setup/state into direct owners. Its first full integration failed closed at `24/6/0`, exposing six stale dynamic consumers; final run `33668283890` passed `30/0/0`, and PR #236 merged at `ded5e77733795aa2958606e899d4e27f12f64df4`.

R2-B2 moved academic/front-matter rendering into direct ownership. PR #242 merged at `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`; closeout #243 established B3 entry `0650845b922271fc134d20ef2a8c36ebb999ef91`. Release-source audit `33696155771` reconciled CTAN/example/public-bundle consumers.

R2-B3 made structural/object environments, source/note/list APIs, optional listing/minted APIs, hooks and project-owned object IDs direct owners. Final Linux `33704346429` passed `30/0/0`; PR #245 squash-merged at `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`.

R2-B4 used control-plane entry `{B4_CONTROL_ENTRY}`. Bibliography/reference/glossary/index commands became direct owners and non-semantic plumbing became private. Three integration attempts failed closed at `29/1/0` on the shared unnumbered-heading evidence locator while the dedicated index gate remained green. The final observer measures the complete rendered heading line instead of a single locator word; `ÍNDICE REMISSIVO` passed at delta `0.0002 pt`. Final head `{B4_HEAD}` passed Static `{STATIC_RUN}` and Linux `{LINUX_RUN}` / `{LINUX_JOB}` at `{LINUX_RESULT}`. PR #247 squash-merged at `{B4_MERGE}` and issue #239 closed completed. `public-api.def` is now empty and reserved solely for physical removal in B5.

The pre-existing observational `FRONTMATTER-EVIDENCE` FAIL records remain baseline observations inside passing aggregate gates and were not changed by the API migration.

## Immediate action

Execute **R2-B5 issue #240** only after this B4-to-B5 control-plane closeout is merged. Remove `abntexto-ufc/public-api.def` and its load from `abntexto-ufc.cls`; run the fail-closed repository-wide residual scan for project-owned Portuguese runtime/API/internal identifiers; create `docs/MIGRATING-TO-V3.md` from `release/v3-api-migration.json`; reconcile the migration contracts as consumed; validate with Static/Linux and release checks when warranted; then close R2. Do not activate an R3 issue until one is explicitly created.
""",
    encoding="utf-8",
)

(ROOT / "docs/R2-API-OWNERSHIP.md").write_text(
    f"""# V3-R2 API Ownership Inventory

Updated: {DATE}

## Purpose

This document records the R2 owner map and bounded B1–B5 migration sequence. It is engineering control-plane documentation, not a normative formatting source.

R2-A entry: `0a2c2c3879986ca27b731f54b974db12524258df`. B1 merge: `ded5e77733795aa2958606e899d4e27f12f64df4`. B2 merge: `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`. B3 merge: `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`. B4 control-plane entry: `{B4_CONTROL_ENTRY}`. B4 merge/B5 product entry: `{B4_MERGE}`. Authority: `release/v3-api-migration.json`.

## Current-state finding

B1 through B4 forwarding has been absorbed by direct owners. `public-api.def` is now intentionally empty; B5 removes that file and its class load, runs the final residual migration scan, reconciles the consumed contracts, and creates the user migration guide.

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
| forwarding-only layer | `public-api.def` | empty; physical removal in B5 |

## Upstream boundaries

Dependency-owned identifiers remain only where required by the dependency contract, including `grafico` / `quadro` and upstream commands such as `\\legend`, `\\keywords`, `\\appendix`, `\\annex`, `\\pretextual`, and `\\textual`. Rendered Portuguese labels remain protected document content.

## Lots

### R2-B1 — DONE
Issue #234 / PR #236. Final Linux `33668283890` = `30/0/0`.

### R2-B2 — DONE
Issue #237 / PR #242; closeout #243. Final implementation Linux `33680378846` = `30/0/0`; release `33687588772` = `32/0/0`.

### R2-B3 — DONE
Issue #238 / PR #245. Merge `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`; Static `33704346418`; Linux `33704346429` = `30/0/0`.

### R2-B4 — DONE
Issue #239 / PR #247. Product entry `{B4_PRODUCT_ENTRY}`, control-plane entry `{B4_CONTROL_ENTRY}`, head `{B4_HEAD}`, merge `{B4_MERGE}`. Final Static `{STATIC_RUN}` passed and Linux `{LINUX_RUN}` / `{LINUX_JOB}` = `{LINUX_RESULT}`. The final heading observer preserved the rendered `ÍNDICE REMISSIVO` and measured the whole line; no runtime aliases, normative semantics, locator policy, tolerances or proof-state changed.

### R2-B5 — ACTIVE
Issue #240. After this closeout merges: remove `public-api.def` and its class load, perform the final project-owned Portuguese runtime/API/internal residual sweep, reconcile consumed contracts, and generate `docs/MIGRATING-TO-V3.md`. Migration support remains documentation-only; no runtime aliases.

## Invariants

Project-owned engineering identifiers are English; rendered Brazilian academic content remains as required. Owner and consumers move together. No normative rule/value/tolerance/locator-policy/proof-state change without evidence. Proprietary Microsoft fonts stay external. CTAN submission is a later explicit release action.
""",
    encoding="utf-8",
)

replace_once(
    "docs/ARCHITECTURE.md",
    "The target architecture above is implemented through bounded owner-based lots documented in `docs/R2-API-OWNERSHIP.md`. R2-A, B1, B2 and B3 are complete. B3 merged through PR #245 at `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` after Static `33704346418` and Linux `33704346429` passed `PASS=30 FAIL=0 SKIP=0`. R2-B4/#239 is active from that checkpoint and absorbs bibliography/reference/glossary/index public ownership. R2-B5 then removes `public-api.def` and closes the residual migration. Template and test consumers move atomically with each behavior owner.",
    f"The target architecture above is implemented through bounded owner-based lots documented in `docs/R2-API-OWNERSHIP.md`. R2-A and B1 through B4 are complete. B4 merged through PR #247 at `{B4_MERGE}` after Static `{STATIC_RUN}` and Linux `{LINUX_RUN}` passed `{LINUX_RESULT}`. Bibliography/reference/glossary/index commands are now directly owned; `public-api.def` is empty. R2-B5/#240 is active and removes that forwarding-only file/load, closes residual project-owned runtime/internal naming debt, generates the migration guide, and reconciles the R2 contracts. Template and test consumers move atomically with each behavior owner.",
)

replace_once(
    "docs/CTAN-RELEASE.md",
    "- Development gate: V3-R2 runtime/API migration is active in R2-B4. R2-B3 structural/object migration is complete through PR #245 at `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df`, with Static `33704346418` PASS and Linux `33704346429` `PASS=30 FAIL=0 SKIP=0`. Only B4 bibliography/back-matter ownership and B5 final forwarding-layer removal remain before R2 can close. A v3.0.0 CTAN upload must not be performed from an intermediate R2 lot; publication remains a later explicit action after the roadmap reaches its release-ready stage and the intended candidate is revalidated proportionally.",
    f"- Development gate: V3-R2 runtime/API migration is active in R2-B5. R2-B4 bibliography/back-matter ownership is complete through PR #247 at `{B4_MERGE}`, with Static `{STATIC_RUN}` PASS and Linux `{LINUX_RUN}` `{LINUX_RESULT}`. Only the B5 forwarding-layer removal, residual migration closure and migration documentation remain before R2 can close. A v3.0.0 CTAN upload must not be performed from an intermediate R2 lot; publication remains a later explicit action after the roadmap reaches its release-ready stage and the intended candidate is revalidated proportionally.",
)

replace_once(
    "AGENTS.md",
    "- V3-R2 is ACTIVE in R2-B4 via issue #239. R2-A plus R2-B1, R2-B2 and R2-B3 are complete and recorded in `docs/R2-API-OWNERSHIP.md`.",
    "- V3-R2 is ACTIVE in R2-B5 via issue #240. R2-A plus R2-B1 through R2-B4 are complete and recorded in `docs/R2-API-OWNERSHIP.md`.",
)
replace_once(
    "AGENTS.md",
    "- R2-B4/#239 owns bibliography/reference/glossary/index public commands and non-semantic plumbing internalization. Migrate owners and consumers atomically; do not perform a blind global replacement.",
    f"- R2-B4 is DONE through PR #247 at `{B4_MERGE}`; final Static `{STATIC_RUN}` and Linux `{LINUX_RUN}` passed `{LINUX_RESULT}`. Bibliography/reference/glossary/index commands are directly owned and `public-api.def` is empty.",
)
replace_once(
    "AGENTS.md",
    "- `public-api.def` is transitional R2 debt. Remove migrated forwarding entries as each owner absorbs them; do not add a reverse compatibility layer. The file is removed completely in R2-B5.",
    "- R2-B5/#240 owns the final residual scan, physical removal of the empty `public-api.def` and its class load, migration-guide generation and R2 contract reconciliation. Do not add a runtime compatibility layer.",
)

replace_once(
    "README.md",
    "**V3-R1 is DONE. V3-R2 is ACTIVE in R2-B4 — bibliography and back-matter API ownership, tracked by issue #239.**",
    "**V3-R1 is DONE. V3-R2 is ACTIVE in R2-B5 — final consumer migration and forwarding-layer removal, tracked by issue #240.**",
)
replace_once(
    "README.md",
    "The canonical R2-B4 product entry checkpoint is `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` after B3 PR #245 passed Static `33704346418` and Linux `33704346429` at `PASS=30 FAIL=0 SKIP=0`.",
    f"The R2-B4 product merge is `{B4_MERGE}` after PR #247 passed Static `{STATIC_RUN}` and Linux `{LINUX_RUN}` at `{LINUX_RESULT}`; this is the product entry for the B4-to-B5 closeout.",
)
replace_once(
    "README.md",
    "Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. R1 rebuilt and certified the foundation. R2-A completed the runtime/API ownership inventory, R2-B1 completed direct canonical setup/state migration, and R2-B2 completed direct academic/front-matter rendering ownership. R2-B3 completed structural/object direct ownership. R2-B4 now moves bibliography/reference/glossary/index commands directly into responsibility-owning modules. See `docs/R2-API-OWNERSHIP.md` for the bounded migration sequence.",
    "Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. R1 rebuilt and certified the foundation. R2-A and R2-B1 through R2-B4 completed direct ownership of setup/state, academic/front-matter, structural/object, and bibliography/back-matter surfaces. R2-B5 now removes the empty forwarding layer, closes residual engineering identifiers and produces the v3 migration guide. See `docs/R2-API-OWNERSHIP.md` for the bounded migration sequence.",
)
replace_once(
    "README.md",
    "R1-BLOCK-8 is DONE. Windows run `33649620219` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX candidate matrix. Final Linux inspection run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b. `TeXGyreTermesX-Regular` under pdfLaTeX is a legitimate `newtxmath` component, not institutional text fallback. R2-A, R2-B1, R2-B2 and R2-B3 are complete. B3 PR #245 merged at `fb71eb0cb50f065d75aec6bbc704dcaf9091d1df` after full Linux integration `33704346429` passed `PASS=30 FAIL=0 SKIP=0`. V3-R2/R2-B4 is active through issue #239.",
    f"R1-BLOCK-8 is DONE. Windows run `33649620219` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX candidate matrix. Final Linux inspection run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b. `TeXGyreTermesX-Regular` under pdfLaTeX is a legitimate `newtxmath` component, not institutional text fallback. R2-A and R2-B1 through R2-B4 are complete. B4 PR #247 merged at `{B4_MERGE}` after full Linux integration `{LINUX_RUN}` passed `{LINUX_RESULT}`. V3-R2/R2-B5 is active through issue #240.",
)

expected = {
    "release/v3-roadmap.json",
    "release/v3-api-migration.json",
    "release/v3-test-migration.json",
    "release/v3-path-migration.json",
    "docs/ROADMAP-V3.0.0.md",
    "docs/HANDOFF-V3.0.0.md",
    "docs/R2-API-OWNERSHIP.md",
    "docs/ARCHITECTURE.md",
    "docs/CTAN-RELEASE.md",
    "AGENTS.md",
    "README.md",
}
actual = changed_paths()
if actual != expected:
    raise SystemExit(
        f"closeout changed paths mismatch: expected={sorted(expected)} actual={sorted(actual)}"
    )

print(f"R2-B4 closeout reconciled: B4 merge={B4_MERGE}; B5 active; files={len(actual)}")
