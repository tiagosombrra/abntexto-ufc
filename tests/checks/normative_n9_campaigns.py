#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RECONCILIATION = ROOT / "normativa" / "n9-scope-reconciliation.json"
CAMPAIGN_PLAN = ROOT / "normativa" / "n9-campaign-plan.json"
ORACLE_POLICY = ROOT / "normativa" / "oracle-policy.json"
VECTOR_EXTENSION = ROOT / "normativa" / "vector-rule-oracle-extension.json"
EXPECTED_CAMPAIGNS = {
    "illustration-final-pdf": 8,
    "table-final-pdf": 7,
    "equation-display-final-pdf": 1,
}
EXPECTED_ORACLE_EXTENSION = {
    "table.ibge.open-sides",
    "table.ibge.body-grid",
    "table.ibge.top-rule",
    "table.ibge.header-rule",
    "table.ibge.bottom-rule",
}


def fail(message: str) -> None:
    raise SystemExit(f"N9 campaign reconciliation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def rule_ids(items: list[dict[str, Any]]) -> list[str]:
    result: list[str] = []
    for item in items:
        values = item.get("rule_ids")
        if not isinstance(values, list) or not values or not all(
            isinstance(rule_id, str) and rule_id for rule_id in values
        ):
            fail(f"{item.get('id')}: rule_ids must be non-empty strings")
        result.extend(values)
    return result


def main() -> None:
    reconciliation = load_json(RECONCILIATION)
    plan = load_json(CAMPAIGN_PLAN)
    oracle = load_json(ORACLE_POLICY)
    extension = load_json(VECTOR_EXTENSION)

    if reconciliation.get("schema_version") != 1 or reconciliation.get("phase") != "N9":
        fail("invalid N9 reconciliation schema/phase")
    if plan.get("schema_version") != 1 or plan.get("phase") != "N9":
        fail("invalid campaign plan schema/phase")
    if oracle.get("schema_version") != 1 or oracle.get("phase") != "N5":
        fail("invalid N5 oracle policy schema/phase")
    if (
        extension.get("schema_version") != 1
        or extension.get("phase") != "N5"
        or extension.get("component") != "vector-rule-geometry"
    ):
        fail("invalid vector-rule oracle extension schema/phase/component")

    required_policy = (
        "campaigns_must_partition_support_only_rules",
        "existing_n5_oracle_is_preferred_when_capable",
        "new_measurement_capability_requires_explicit_oracle_extension",
        "no_visual_predicate_closes_from_tex_log_or_source_structure_alone",
    )
    policy = plan.get("policy")
    if not isinstance(policy, dict) or not all(
        policy.get(key) is True for key in required_policy
    ):
        fail("campaign policy drifted")

    groups = reconciliation.get("groups")
    if not isinstance(groups, list):
        fail("reconciliation groups are required")
    support_groups = [
        group for group in groups if group.get("classification") == "support-only"
    ]
    support_ids = rule_ids(support_groups)
    if len(support_ids) != len(set(support_ids)):
        fail("support-only rules are duplicated in the reconciliation")
    support_set = set(support_ids)

    campaigns = plan.get("campaigns")
    if not isinstance(campaigns, list) or len(campaigns) != 3:
        fail("expected exactly three N9 residual campaigns")
    campaign_ids = [campaign.get("id") for campaign in campaigns]
    if set(campaign_ids) != set(EXPECTED_CAMPAIGNS) or len(campaign_ids) != len(
        set(campaign_ids)
    ):
        fail(f"campaign IDs drifted: {campaign_ids}")

    planned_ids = rule_ids(campaigns)
    if len(planned_ids) != len(set(planned_ids)):
        fail("a residual predicate appears in more than one N9 campaign")
    planned_set = set(planned_ids)
    if planned_set != support_set:
        fail(
            "campaign partition does not match support-only residuals: "
            f"missing={sorted(support_set - planned_set)}, "
            f"extra={sorted(planned_set - support_set)}"
        )

    by_id = {campaign["id"]: campaign for campaign in campaigns}
    for campaign_id, expected_count in EXPECTED_CAMPAIGNS.items():
        actual = len(by_id[campaign_id]["rule_ids"])
        if actual != expected_count:
            fail(f"{campaign_id}: expected {expected_count} rules, found {actual}")

    allowed_tools = set(oracle.get("tools", {}).values())
    if not allowed_tools:
        fail("N5 oracle tools are missing")
    for campaign_id in ("illustration-final-pdf", "equation-display-final-pdf"):
        campaign = by_id[campaign_id]
        if campaign.get("measurement_status") != "existing-n5-capability":
            fail(f"{campaign_id}: expected existing N5 capability")
        tools = campaign.get("measurement_tools")
        if not isinstance(tools, list) or not tools or not set(tools) <= allowed_tools:
            fail(f"{campaign_id}: measurement tools are outside N5 policy: {tools}")

    table = by_id["table-final-pdf"]
    if table.get("measurement_status") != "mixed-capability":
        fail("table-final-pdf must remain mixed-capability")
    existing_table = table.get("existing_n5_rule_ids")
    extension_table = table.get("oracle_extension_required_rule_ids")
    if not isinstance(existing_table, list) or set(existing_table) != {
        "font.size.reduced.table-caption",
        "font.size.reduced.table-source",
    }:
        fail(f"table N5-capable subset drifted: {existing_table}")
    if not isinstance(extension_table, list) or set(extension_table) != EXPECTED_ORACLE_EXTENSION:
        fail(f"table oracle-extension subset drifted: {extension_table}")
    if set(existing_table) | set(extension_table) != set(table["rule_ids"]):
        fail("table capability subsets do not partition the table campaign")
    if table.get("oracle_extension") != "normativa/vector-rule-oracle-extension.json":
        fail("table campaign is not bound to the vector-rule oracle extension")
    if table.get("oracle_extension_runtime_calibration_required") is not True:
        fail("table campaign must require same-run vector calibration")

    if oracle.get("tools", {}).get("vector_geometry") != extension.get("tool"):
        fail("vector tool registration drifted between oracle policy and extension")
    if oracle.get("vector_geometry_extension") != "normativa/vector-rule-oracle-extension.json":
        fail("oracle policy extension binding drifted")
    if "vector-rule-geometry" not in oracle.get("exit_capabilities", []):
        fail("vector-rule-geometry capability is not registered")
    extension_policy = extension.get("policy", {})
    if not isinstance(extension_policy, dict) or not all(
        extension_policy.get(key) is expected
        for key, expected in {
            "additive_capability_only": True,
            "existing_n5_tolerances_unchanged": True,
            "rasterization_not_used": True,
            "proof_state_changed": False,
        }.items()
    ):
        fail("vector-rule extension policy drifted")

    extension_set = set(extension_table)
    existing_n5_set = planned_set - extension_set
    expected_counts = plan.get("expected_counts")
    measured_counts = {
        "campaigns": len(campaigns),
        "residual_rules": len(planned_set),
        "existing_n5_capability_rules": len(existing_n5_set),
        "oracle_extension_required_rules": len(extension_set),
    }
    if expected_counts != measured_counts:
        fail(f"campaign count drift: expected={expected_counts}, measured={measured_counts}")
    if measured_counts != {
        "campaigns": 3,
        "residual_rules": 16,
        "existing_n5_capability_rules": 11,
        "oracle_extension_required_rules": 5,
    }:
        fail(f"unexpected N9 campaign baseline: {measured_counts}")

    print(
        "N9-EVIDENCE campaign-plan "
        f"campaigns={measured_counts['campaigns']} "
        f"residual_rules={measured_counts['residual_rules']} "
        f"existing_n5_capability_rules={measured_counts['existing_n5_capability_rules']} "
        f"oracle_extension_required_rules={measured_counts['oracle_extension_required_rules']}"
    )
    print(
        "N9-EVIDENCE oracle-extension-required rule_ids="
        + json.dumps(sorted(extension_set), ensure_ascii=False)
    )
    print(
        "N9-EVIDENCE oracle-extension-registered "
        f"tool={extension.get('tool')} capability=vector-rule-geometry "
        "same_run_calibration_required=true"
    )


if __name__ == "__main__":
    main()
