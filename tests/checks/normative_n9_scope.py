#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract

SCENARIO = ROOT / "normativa" / "n9-scope-reconciliation.json"
TARGET_CATEGORIES = {"objects", "equations", "code-algorithms"}
EXPECTED_PROJECT_POLICY = {
    "code.listing.project-policy",
    "algorithm.project-policy",
}


def fail(message: str) -> None:
    raise SystemExit(f"N9 scope reconciliation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def flatten_groups(groups: list[dict[str, Any]]) -> list[str]:
    result: list[str] = []
    for group in groups:
        rule_ids = group.get("rule_ids")
        if not isinstance(rule_ids, list) or not all(
            isinstance(rule_id, str) and rule_id for rule_id in rule_ids
        ):
            fail(f"group {group.get('id')}: rule_ids must be non-empty strings")
        result.extend(rule_ids)
    return result


def verify_evidence(group: dict[str, Any]) -> None:
    evidence = group.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        fail(f"group {group.get('id')}: evidence paths are required")
    for relative in evidence:
        if not isinstance(relative, str) or not relative:
            fail(f"group {group.get('id')}: invalid evidence path")
        if not (ROOT / relative).is_file():
            fail(f"group {group.get('id')}: evidence file missing: {relative}")

    tokens = group.get("required_tokens", {})
    if not isinstance(tokens, dict):
        fail(f"group {group.get('id')}: required_tokens must be an object")
    for relative, required in tokens.items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"group {group.get('id')}: token source missing: {relative}")
        if not isinstance(required, list) or not required:
            fail(f"group {group.get('id')}: token list missing for {relative}")
        source = path.read_text(encoding="utf-8", errors="replace")
        absent = [token for token in required if token not in source]
        if absent:
            fail(
                f"group {group.get('id')}: evidence drift in {relative}: "
                + ", ".join(repr(token) for token in absent)
            )


def main() -> None:
    scenario = load_json(SCENARIO)
    if scenario.get("schema_version") != 1 or scenario.get("phase") != "N9":
        fail("invalid schema or phase")

    derivation = scenario.get("derivation")
    if not isinstance(derivation, dict):
        fail("derivation must be an object")
    categories = derivation.get("categories")
    if not isinstance(categories, list) or set(categories) != TARGET_CATEGORIES:
        fail(f"category selector drifted: {categories}")
    cross_cutting = derivation.get("cross_cutting_rule_ids")
    if not isinstance(cross_cutting, list) or len(cross_cutting) != 4:
        fail("expected exactly four cross-cutting reduced-size rules")
    cross_cutting_set = set(cross_cutting)

    policy = scenario.get("policy")
    required_policy = (
        "full_contract_is_authoritative_for_scope",
        "visual_geometry_or_typography_requires_final_pdf_for_bounded_closure",
        "tex_log_or_source_structure_alone_is_support_only_for_visual_predicates",
        "semantic_presence_or_routing_may_use_rendered_text_and_generated_lists",
        "project_policy_capabilities_remain_non_normative",
        "existing_bounded_mapping_does_not_change_proof_state",
    )
    if not isinstance(policy, dict) or not all(policy.get(key) is True for key in required_policy):
        fail("N9 evidence policy drifted")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    derived = {
        rule_id
        for rule_id, rule in rules.items()
        if rule.get("category") in TARGET_CATEGORIES
    } | cross_cutting_set

    groups = scenario.get("groups")
    if not isinstance(groups, list) or not groups:
        fail("groups must be a non-empty list")
    group_ids = [group.get("id") for group in groups]
    if len(group_ids) != len(set(group_ids)):
        fail("group IDs must be unique")

    declared_ids = flatten_groups(groups)
    if len(declared_ids) != len(set(declared_ids)):
        duplicates = sorted(
            rule_id for rule_id, count in Counter(declared_ids).items() if count > 1
        )
        fail("rules appear in multiple groups: " + ", ".join(duplicates))
    declared = set(declared_ids)
    if declared != derived:
        missing = sorted(derived - declared)
        extra = sorted(declared - derived)
        fail(f"scope mismatch: missing={missing}, extra={extra}")

    unknown = sorted(declared - set(rules))
    if unknown:
        fail("unknown full-contract rules: " + ", ".join(unknown))

    for rule_id in sorted(declared):
        rule = rules[rule_id]
        if rule_id in EXPECTED_PROJECT_POLICY:
            if rule.get("authority") != "project-policy":
                fail(f"{rule_id}: must remain project-policy authority")
            if rule.get("values") != {"supported": True, "normative_claim": False}:
                fail(f"{rule_id}: project-policy values drifted: {rule.get('values')}")
        elif rule.get("authority") != "normative":
            fail(f"{rule_id}: unexpected non-normative authority {rule.get('authority')}")

    expected_cross = {
        "font.size.reduced.illustration-caption",
        "font.size.reduced.illustration-source",
        "font.size.reduced.table-caption",
        "font.size.reduced.table-source",
    }
    if cross_cutting_set != expected_cross:
        fail(f"cross-cutting reduced-size set drifted: {sorted(cross_cutting_set)}")
    for rule_id in expected_cross:
        if rules[rule_id].get("values") != {"pt": 10}:
            fail(f"{rule_id}: expected 10 pt contract")

    classifications: Counter[str] = Counter()
    bounded_rules: list[str] = []
    support_rules: list[str] = []
    for group in groups:
        classification = group.get("classification")
        if classification not in {"existing-bounded-positive", "support-only"}:
            fail(f"group {group.get('id')}: invalid classification {classification}")
        verify_evidence(group)
        count = len(group["rule_ids"])
        classifications[classification] += count
        if classification == "existing-bounded-positive":
            if "reason" in group:
                fail(f"group {group.get('id')}: bounded mapping should use explicit evidence, not a support reason")
            bounded_rules.extend(group["rule_ids"])
        else:
            reason = group.get("reason")
            if not isinstance(reason, str) or not reason:
                fail(f"group {group.get('id')}: support-only classification requires a reason")
            support_rules.extend(group["rule_ids"])

    expected_counts = scenario.get("expected_counts")
    measured_counts = {
        "total": len(declared),
        "existing_bounded_positive": classifications["existing-bounded-positive"],
        "support_only": classifications["support-only"],
    }
    if expected_counts != measured_counts:
        fail(f"count drift: expected={expected_counts}, measured={measured_counts}")

    if measured_counts != {
        "total": 23,
        "existing_bounded_positive": 7,
        "support_only": 16,
    }:
        fail(f"unexpected N9 baseline: {measured_counts}")

    print(
        "N9-EVIDENCE scope-reconciliation "
        f"total={measured_counts['total']} "
        f"existing_bounded_positive={measured_counts['existing_bounded_positive']} "
        f"support_only={measured_counts['support_only']}"
    )
    print(
        "N9-EVIDENCE bounded-existing rule_ids="
        + json.dumps(sorted(bounded_rules), ensure_ascii=False)
    )
    print(
        "N9-EVIDENCE support-only rule_ids="
        + json.dumps(sorted(support_rules), ensure_ascii=False)
    )
    print(
        "N9-EVIDENCE authority-boundary project_policy_rule_ids="
        + json.dumps(sorted(EXPECTED_PROJECT_POLICY), ensure_ascii=False)
        + " normative_claim=false"
    )


if __name__ == "__main__":
    main()
