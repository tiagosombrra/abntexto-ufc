#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract

MANIFEST = ROOT / "normativa" / "n11-scope-reconciliation.json"
WORKFLOW = ROOT / ".github" / "workflows" / "latex-preflight.yml"
RUNNER = ROOT / "tests" / "run.py"


def fail(message: str) -> None:
    raise SystemExit(f"N11 scope reconciliation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def ruleset(document: dict[str, Any], ruleset_id: str) -> dict[str, Any]:
    matches = [
        item for item in document.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == ruleset_id
    ]
    if len(matches) != 1:
        fail(f"locator ruleset {ruleset_id}: expected one match, found {len(matches)}")
    return matches[0]


def main() -> None:
    manifest = load_json(MANIFEST)
    if manifest.get("schema_version") != 1 or manifest.get("phase") != "N11":
        fail("invalid manifest schema/phase")
    if manifest.get("scope") != "research-project-profile":
        fail("unexpected N11 scope label")

    normative_ids = set(manifest.get("normative_rule_ids", []))
    technical_ids = set(manifest.get("technical_profile_rule_ids", []))
    policy_ids = set(manifest.get("project_policy_rule_ids", []))
    expected_scope = normative_ids | technical_ids | policy_ids
    if len(expected_scope) != 5 or manifest.get("total_rules") != 5:
        fail(f"expected exactly 5 N11 rules, found {len(expected_scope)}")
    if len(normative_ids) != 3 or len(technical_ids) != 1 or len(policy_ids) != 1:
        fail(
            "unexpected N11 authority partition: "
            f"normative={len(normative_ids)} technical={len(technical_ids)} policy={len(policy_ids)}"
        )
    if (normative_ids & technical_ids) or (normative_ids & policy_ids) or (technical_ids & policy_ids):
        fail("N11 authority partitions overlap")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    contract_project_ids = {
        rule_id for rule_id, rule in rules.items()
        if rule.get("category") == "project"
    }
    if contract_project_ids != expected_scope:
        fail(
            "project scope drifted against full contract: "
            f"manifest_only={sorted(expected_scope - contract_project_ids)} "
            f"contract_only={sorted(contract_project_ids - expected_scope)}"
        )

    actual_normative = {
        rule_id for rule_id in expected_scope
        if rules[rule_id].get("authority") == "normative"
    }
    actual_technical = {
        rule_id for rule_id in expected_scope
        if rules[rule_id].get("authority") == "technical-profile"
    }
    actual_policy = {
        rule_id for rule_id in expected_scope
        if rules[rule_id].get("authority") == "project-policy"
    }
    if actual_normative != normative_ids:
        fail(f"normative project partition drifted: {sorted(actual_normative)}")
    if actual_technical != technical_ids:
        fail(f"technical-profile partition drifted: {sorted(actual_technical)}")
    if actual_policy != policy_ids:
        fail(f"project-policy partition drifted: {sorted(actual_policy)}")

    policy = manifest.get("authority_policy", {})
    if policy.get("normative_rules") != len(normative_ids):
        fail("normative authority count drifted")
    if policy.get("technical_profile_rules") != len(technical_ids):
        fail("technical-profile authority count drifted")
    if policy.get("project_policy_rules") != len(policy_ids):
        fail("project-policy authority count drifted")
    if policy.get("proof_state_changed") is not False:
        fail("scope reconciliation must not change proof-state")
    if policy.get("broad_project_regressions_are_support_only") is not True:
        fail("broad project regressions must remain support-only")

    locator_path = ROOT / manifest["locator_file"]
    locator = load_json(locator_path)
    project_locator = ruleset(locator, manifest["locator_ruleset"])
    if project_locator.get("status") != policy.get("nbr15287_locator_status"):
        fail("NBR 15287 locator status drifted")
    locator_ids = set(project_locator.get("rule_ids", []))
    if locator_ids != normative_ids:
        fail(
            "NBR 15287 locator scope drifted: "
            f"manifest_only={sorted(normative_ids - locator_ids)} "
            f"locator_only={sorted(locator_ids - normative_ids)}"
        )

    for rule_id in normative_ids:
        sources = rules[rule_id].get("sources", [])
        if sources != ["abnt-nbr-15287-2025"]:
            fail(f"unexpected normative source for {rule_id}: {sources}")
    for rule_id in technical_ids | policy_ids:
        if rules[rule_id].get("sources"):
            fail(f"non-normative project rule claims external source: {rule_id}")

    bounded = manifest.get("existing_bounded_positive", [])
    bounded_ids = {
        item.get("rule_id") for item in bounded if isinstance(item, dict)
    }
    expected_bounded = {
        "project.cover.optional",
        "project.title-page.required",
        "project.anonymization.policy",
    }
    if bounded_ids != expected_bounded or len(bounded) != 3:
        fail(f"bounded baseline drifted: {sorted(item for item in bounded_ids if item)}")

    support_ids = set(manifest.get("support_only_rule_ids", []))
    expected_support = expected_scope - expected_bounded
    if support_ids != expected_support or len(support_ids) != 2:
        fail(
            "support-only partition drifted: "
            f"missing={sorted(expected_support - support_ids)} "
            f"extra={sorted(support_ids - expected_support)}"
        )
    if bounded_ids & support_ids:
        fail("bounded and support-only sets overlap")

    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    runner_text = RUNNER.read_text(encoding="utf-8")
    required_checks = manifest.get("required_pr_check_ids", [])
    if set(required_checks) != {"pretextual", "project", "profiles"}:
        fail(f"unexpected required PR check set: {required_checks}")
    for check_id in required_checks:
        if check_id not in workflow_text:
            fail(f"required PR check {check_id} is not selected by latex-preflight")
        if f'"{check_id}"' not in runner_text and f"'{check_id}'" not in runner_text:
            fail(f"required PR check {check_id} is not registered in tests/run.py")

    for item in bounded:
        path = ROOT / item["evidence_file"]
        if not path.is_file():
            fail(f"bounded evidence file missing: {path}")
        text = path.read_text(encoding="utf-8")
        missing_tokens = [token for token in item.get("required_tokens", []) if token not in text]
        if missing_tokens:
            fail(f"bounded evidence {item['rule_id']} lost required tokens: {missing_tokens}")
        for check_id in item.get("required_check_ids", []):
            if check_id not in required_checks:
                fail(f"bounded evidence depends on non-required PR check: {check_id}")

    campaigns = manifest.get("campaigns", [])
    if len(campaigns) != 1 or campaigns[0].get("id") != "project-structure-final-pdf":
        fail("N11 must have exactly one residual project-structure campaign")
    campaign = campaigns[0]
    campaign_ids = set(campaign.get("rule_ids", []))
    if campaign_ids != support_ids or campaign.get("rules") != len(support_ids):
        fail(
            "residual campaign does not cover exactly support-only rules: "
            f"campaign={sorted(campaign_ids)} support={sorted(support_ids)}"
        )

    host = manifest.get("scope_checker_host", {})
    host_script = ROOT / host.get("script", "")
    if host.get("check_id") != "project" or not host_script.is_file():
        fail("invalid N11 scope-checker host")
    host_text = host_script.read_text(encoding="utf-8")
    if host.get("checker") not in host_text:
        fail("N11 scope checker is not wired into its mandatory PR host")

    print(
        "N11-EVIDENCE scope-reconciliation "
        f"total={len(expected_scope)} existing_bounded_positive={len(bounded_ids)} "
        f"support_only={len(support_ids)}"
    )
    print("N11-EVIDENCE normative rule_ids=" + json.dumps(sorted(normative_ids)))
    print("N11-EVIDENCE technical-profile rule_ids=" + json.dumps(sorted(technical_ids)))
    print("N11-EVIDENCE project-policy rule_ids=" + json.dumps(sorted(policy_ids)))
    print("N11-EVIDENCE bounded-existing rule_ids=" + json.dumps(sorted(bounded_ids)))
    print("N11-EVIDENCE support-only rule_ids=" + json.dumps(sorted(support_ids)))
    print(
        "N11-EVIDENCE campaign-plan campaigns=1 residual_rules=2 "
        "campaign=project-structure-final-pdf"
    )
    print(
        "N11-EVIDENCE authority-boundary "
        "nbr15287=UNAVAILABLE_WITH_REASON technical-profile=internal "
        "project-policy=internal proof_state_changed=false"
    )


if __name__ == "__main__":
    main()
