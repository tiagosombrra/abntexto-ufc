from pathlib import Path
import subprocess


def main_file(path: str) -> str:
    return subprocess.check_output(["git", "show", f"origin/main:{path}"], text=True)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


api_path = "release/v3-api-migration.json"
api = main_file(api_path)
api = replace_once(api, '  "status": "ACTIVE_R2_A_INVENTORY",', '  "status": "R2_A_DONE_R2_B1_ACTIVE",', api_path)
api = replace_once(api, '  "current_stage": "R2-A",', '  "current_stage": "R2-B1",', api_path)
api = replace_once(
    api,
    '  "current_stage_goal": "inventory runtime/API ownership and define bounded migration lots before behavioral changes",\n',
    '  "current_stage_goal": "canonical setup and internal state vocabulary",\n'
    '  "r2_a_inventory": {\n'
    '    "status": "DONE",\n'
    '    "completed_at": "2026-09-02",\n'
    '    "canonical_main_sha": "0a2c2c3879986ca27b731f54b974db12524258df",\n'
    '    "operational_issue": 232,\n'
    '    "ownership_document": "docs/R2-API-OWNERSHIP.md",\n'
    '    "active_implementation_lot": {"stage": "R2-B1", "issue": 234},\n'
    '    "planned_lots": ["R2-B1", "R2-B2", "R2-B3", "R2-B4", "R2-B5"],\n'
    '    "key_findings": [\n'
    '      "public-api.def is forwarding-only transitional debt rather than a behavior owner",\n'
    '      "template and test consumers migrate atomically with each direct behavior owner",\n'
    '      "genuine upstream non-English identifiers remain only at explicit integration boundaries",\n'
    '      "rendered Portuguese academic labels are protected document content"\n'
    '    ]\n'
    '  },\n',
    api_path,
)
Path(api_path).write_text(api, encoding="utf-8")

path_name = "release/v3-path-migration.json"
path_text = main_file(path_name)
path_text = replace_once(path_text, '  "phase": "V3-R0",', '  "phase": "V3-R2",', path_name)
path_text = replace_once(path_text, '  "status": "FROZEN_FOR_V3_R1",', '  "status": "R1_PATHS_DONE_R2_RUNTIME_ABSORPTION_PENDING",', path_name)
path_text = replace_once(
    path_text,
    '  "status": "R1_PATHS_DONE_R2_RUNTIME_ABSORPTION_PENDING",\n',
    '  "status": "R1_PATHS_DONE_R2_RUNTIME_ABSORPTION_PENDING",\n'
    '  "current_stage": "R2-B1",\n'
    '  "r1_path_restructuring_status": "DONE",\n'
    '  "remaining_runtime_path_action": {"path": "abntexto-ufc/public-api.def", "action": "remove-after-absorption", "planned_lot": "R2-B5"},\n',
    path_name,
)
Path(path_name).write_text(path_text, encoding="utf-8")

# Preserve the original compact style while moving the test contract into R2 consumer migration.
test_name = "release/v3-test-migration.json"
test_text = main_file(test_name)
test_text = replace_once(test_text, '  "phase": "V3-R1",', '  "phase": "V3-R2",', test_name)
test_text = replace_once(test_text, '  "status": "ACTIVE_R1_RECONCILIATION",', '  "status": "ACTIVE_R2_API_CONSUMER_MIGRATION",', test_name)
test_text = replace_once(
    test_text,
    '  "status": "ACTIVE_R2_API_CONSUMER_MIGRATION",\n',
    '  "status": "ACTIVE_R2_API_CONSUMER_MIGRATION",\n'
    '  "current_stage": "R2-B1",\n'
    '  "r1_reconciliation_status": "DONE",\n'
    '  "r2_api_consumer_policy": {"owner_inventory": "docs/R2-API-OWNERSHIP.md", "active_lot": "R2-B1", "final_residual_lot": "R2-B5", "runtime_alias_tests_allowed": false},\n',
    test_name,
)
Path(test_name).write_text(test_text, encoding="utf-8")
