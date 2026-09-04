#!/usr/bin/env python3
"""Reconcile the canonical R3-B5 control plane without changing product semantics."""

from __future__ import annotations

import json
from pathlib import Path

ENTRY = "e5d6ab1962ee04935ee68a6ae36f268350d59a3b"
B4_PRODUCT = "59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390"
ACTIVATION_PR = 265
PR_STATIC_RUN = 33817862525
PR_LINUX_RUN = 33817846901
PR_LINUX_JOB = 100853855647
POST_MERGE_STATIC_RUN = 33821489030


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str, payload: dict) -> None:
    Path(path).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one occurrence in {path}, found {count}: {old!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


# Canonical machine roadmap: repair all current-stage pointers that still described R3-B4.
roadmap_path = "release/v3-roadmap.json"
roadmap = load_json(roadmap_path)
roadmap["updated_at"] = "2026-09-03"
roadmap["status"] = "ACTIVE"
roadmap["phase"] = "V3-R3"
roadmap["stage"] = "R3-B5"
roadmap["stage_name"] = "R3 closeout and R4 certification entry"
roadmap["active_branch"] = "main"
roadmap["active_implementation_lot"] = {
    "phase": "V3-R3",
    "stage": "R3-B5",
    "issue": 256,
    "entry_product_main_sha": B4_PRODUCT,
    "name": "R3 closeout and R4 certification entry",
    "id": "R3-B5",
    "status": "ACTIVE",
    "entry_main_sha": ENTRY,
    "activation_pr": ACTIVATION_PR,
}
r3 = roadmap["r3"]
r3["status"] = "ACTIVE"
r3["stage"] = "R3-B5"
r3["stage_name"] = "R3 closeout and R4 certification entry"
r3["issue"] = 256
r3["next_issue"] = 256
r3["active_issue"] = 256
r3["activation_control_plane_pr"] = ACTIVATION_PR
r3["activation_control_plane_main_sha"] = ENTRY
# These phase-level fields were stale snapshots of the B3 merge and are ambiguous now.
r3.pop("pr", None)
r3.pop("merge_main_sha", None)
r3_b5 = r3["lots"]["R3-B5"]
r3_b5["status"] = "ACTIVE"
r3_b5["issue"] = 256
r3_b5["entry_product_main_sha"] = B4_PRODUCT
r3_b5["entry_main_sha"] = ENTRY
r3_b5["activation_pr"] = ACTIVATION_PR
write_json(roadmap_path, roadmap)

# R3 inventory: preserve the B4 product closure while moving the actual B5 execution entry
# to the merged B4->B5 control-plane checkpoint.
inventory_path = "release/v3-r3-inventory.json"
inventory = load_json(inventory_path)
inventory["phase"] = "V3-R3"
inventory["stage"] = "R3-B5"
inventory["status"] = "ACTIVE"
evidence = inventory["evidence"]
evidence.update(
    {
        "r3_b5_activation_pr": ACTIVATION_PR,
        "r3_b5_control_plane_entry_sha": ENTRY,
        "r3_b5_activation_static_run_id": PR_STATIC_RUN,
        "r3_b5_activation_linux_run_id": PR_LINUX_RUN,
        "r3_b5_activation_linux_job_id": PR_LINUX_JOB,
        "r3_b5_activation_linux_result": "PASS=31 FAIL=0 SKIP=0",
        "r3_b5_entry_post_merge_static_run_id": POST_MERGE_STATIC_RUN,
    }
)
lot_b5 = inventory["lots"]["R3-B5"]
lot_b5["status"] = "ACTIVE"
lot_b5["entry_product_main_sha"] = B4_PRODUCT
lot_b5["entry_control_plane_main_sha"] = ENTRY
lot_b5["activation_pr"] = ACTIVATION_PR
inventory["next_stage"] = "R3-B5"
inventory["next_issue"] = 256
inventory["current_entry_main_sha"] = ENTRY
inventory["r3_b5_activation"] = {
    "status": "ACTIVE",
    "issue": 256,
    "activation_pr": ACTIVATION_PR,
    "b4_product_main_sha": B4_PRODUCT,
    "control_plane_entry_sha": ENTRY,
    "static_contract_run_id": PR_STATIC_RUN,
    "linux_integration_run_id": PR_LINUX_RUN,
    "linux_integration_job_id": PR_LINUX_JOB,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "post_merge_static_run_id": POST_MERGE_STATIC_RUN,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
}
write_json(inventory_path, inventory)

# B2 proof-semantics registry was left at an entry-time status even though B2 closed.
proof_path = "release/v3-r3-b2-proof-semantics.json"
proof = load_json(proof_path)
if proof.get("closeout_status") != "VALIDATION_PENDING":
    raise SystemExit(
        f"Unexpected B2 proof closeout status: {proof.get('closeout_status')!r}"
    )
proof["closeout_status"] = "DONE"
proof["closeout"] = {
    "issue": 253,
    "pr": 260,
    "merge_main_sha": "1d9e6373ed674fb7503b968b3e852e4be5fc14ea",
    "static_contract_run_id": 33768911131,
    "linux_integration_run_id": 33768911126,
    "linux_integration_job_id": 100694266254,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "post_merge_release_run_id": 33772854355,
    "post_merge_release_job_id": 100707196590,
    "post_merge_release_result": "PASS=33 FAIL=0 SKIP=0",
    "automatic_partial_bounded_positive": 113,
    "automation_gap": 0,
    "proof_state_changed": False,
    "normative_semantics_changed": False,
    "runtime_public_api_changed": False,
}
write_json(proof_path, proof)

# Human control-plane surfaces.
replace_once(
    "README.md",
    "R3-B5/#256 is active. The certified R1 candidate remains",
    f"R3-B5/#256 is active from the canonical B4->B5 control-plane checkpoint `{ENTRY}` (PR #265). The certified R1 candidate remains",
)
replace_once(
    "README.md",
    "R3-B4/#255 is active and R3-B5/#256 is the remaining R3 closeout lot.",
    f"R3-B4/#255 is complete through PR #264; R3-B5/#256 is active from `{ENTRY}` and is the remaining R3 closeout lot.",
)
replace_once(
    "README.md",
    "R3-B3/#254 and R3-B4/#255 are complete; R3-B5/#256 is active and owns final R3 reconciliation plus the exact R4 certification entry.",
    f"R3-B3/#254 and R3-B4/#255 are complete; R3-B5/#256 is active from `{ENTRY}` and owns final R3 reconciliation plus the exact R4 certification entry.",
)

replace_once(
    "docs/HANDOFF-V3.0.0.md",
    f"- B5 entry product checkpoint: `{B4_PRODUCT}`; the canonical B5 control-plane checkpoint is the merge produced by this B4→B5 reconciliation.",
    f"- B5 product predecessor: `{B4_PRODUCT}`.\n- Canonical B5 execution/control-plane entry: `{ENTRY}` from PR #265.\n- B5 activation PR gates: Static `{PR_STATIC_RUN}` — PASS; Linux `{PR_LINUX_RUN}` / job `{PR_LINUX_JOB}` — `PASS=31 FAIL=0 SKIP=0`.\n- B5 entry post-merge Static `{POST_MERGE_STATIC_RUN}` — PASS; the post-merge release run is current-state evidence and is recorded when it completes.",
)
replace_once(
    "docs/HANDOFF-V3.0.0.md",
    "Execute issue #256 from the canonical B4→B5 control-plane checkpoint.",
    f"Execute issue #256 from canonical control-plane checkpoint `{ENTRY}`.",
)

replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"| R3-B5 | ACTIVE | issue #256; entry `{B4_PRODUCT}` | R3 closeout and immutable R4 entry | reconcile final candidate; run Static + full Linux; record exact R4 entry SHA |",
    f"| R3-B5 | ACTIVE | issue #256; control-plane entry `{ENTRY}` | R3 closeout and immutable R4 entry | reconcile final candidate; run Static + full Linux; record exact R4 entry SHA |",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"R3-B5/#256 starts after this B4→B5 control-plane checkpoint, from product SHA `{B4_PRODUCT}`.",
    f"R3-B5/#256 starts from the canonical B4→B5 control-plane checkpoint `{ENTRY}` (PR #265); its product predecessor remains `{B4_PRODUCT}`.",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "Execute **R3-B5 / issue #256** from the canonical B4→B5 checkpoint.",
    f"Execute **R3-B5 / issue #256** from canonical control-plane checkpoint `{ENTRY}`.",
)

replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    f"| R3-B5/#256 | ACTIVE | entry product `{B4_PRODUCT}`; closes R3 and records immutable R4 entry |",
    f"| R3-B5/#256 | ACTIVE | product predecessor `{B4_PRODUCT}`; control-plane entry `{ENTRY}` (PR #265); closes R3 and records immutable R4 entry |",
)
replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    f"B5 starts only after the B4→B5 control-plane checkpoint merges. Its product entry is `{B4_PRODUCT}`.",
    f"B5 starts from the merged B4→B5 control-plane checkpoint `{ENTRY}` (PR #265); its product predecessor is `{B4_PRODUCT}`.",
)

replace_once(
    "AGENTS.md",
    "R3-B5/#256 is ACTIVE and owns R3 closeout plus the immutable R4 entry. Do not start R4 certification before B5 closes.",
    f"B4→B5 control-plane PR #265 merged at `{ENTRY}` after Static `{PR_STATIC_RUN}` and Linux `{PR_LINUX_RUN}` = `PASS=31 FAIL=0 SKIP=0`. R3-B5/#256 is ACTIVE from that canonical checkpoint and owns R3 closeout plus the immutable R4 entry. Do not start R4 certification before B5 closes.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    "R3-B5/#256 is ACTIVE and owns only R3 closeout/R4 entry.",
    f"R3-B5/#256 is ACTIVE from canonical control-plane checkpoint `{ENTRY}` and owns only R3 closeout/R4 entry.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "R3-B5 now owns final cross-surface reconciliation and the immutable R4 entry checkpoint.",
    f"R3-B5 now owns final cross-surface reconciliation from `{ENTRY}` and the immutable R4 entry checkpoint.",
)

replace_once(
    "docs/ENGINEERING-LANGUAGE.md",
    "R3-B5/#256 is ACTIVE and owns R3 closeout/R4 entry; it must not broaden this policy or change the public runtime API.",
    f"R3-B5/#256 is ACTIVE from canonical control-plane checkpoint `{ENTRY}` and owns R3 closeout/R4 entry; it must not broaden this policy or change the public runtime API.",
)

replace_once(
    "docs/CTAN-RELEASE.md",
    "R3-B5/#256 is active and remains required before R4.",
    f"R3-B5/#256 is active from canonical control-plane checkpoint `{ENTRY}` and remains required before R4.",
)

# Cross-surface fail-closed assertions.
roadmap = load_json(roadmap_path)
inventory = load_json(inventory_path)
proof = load_json(proof_path)
assert roadmap["stage"] == "R3-B5"
assert roadmap["active_implementation_lot"]["stage"] == "R3-B5"
assert roadmap["active_implementation_lot"]["issue"] == 256
assert roadmap["active_implementation_lot"]["entry_main_sha"] == ENTRY
assert roadmap["r3"]["stage"] == "R3-B5"
assert roadmap["r3"]["issue"] == 256
assert roadmap["r3"]["next_issue"] == 256
assert roadmap["r3"]["active_issue"] == 256
assert roadmap["r3"]["lots"]["R3-B5"]["entry_main_sha"] == ENTRY
assert inventory["stage"] == "R3-B5"
assert inventory["next_issue"] == 256
assert inventory["current_entry_main_sha"] == ENTRY
assert inventory["lots"]["R3-B5"]["entry_control_plane_main_sha"] == ENTRY
assert proof["closeout_status"] == "DONE"
assert proof["closeout"]["automation_gap"] == 0

readme = Path("README.md").read_text(encoding="utf-8")
if "R3-B4/#255 is active" in readme:
    raise SystemExit("README still claims R3-B4 is active")

print("R3-B5 control-plane reconciliation prepared successfully.")
