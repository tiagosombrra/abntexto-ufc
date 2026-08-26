#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract

MANIFEST = ROOT / "normativa" / "n10-scope-reconciliation.json"
POSTTEXTUAL_LOCATOR = ROOT / "normativa" / "locator-audit-posttextual.json"
PAGINATION_LOCATOR = ROOT / "normativa" / "locator-audit-layout-pagination.json"
WORKFLOW = ROOT / ".github" / "workflows" / "latex-preflight.yml"
RUNNER = ROOT / "tests" / "run.py"


def fail(message: str) -> None:
    raise SystemExit(f"N10 scope reconciliation failed: {message}")


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
    post_locator = load_json(POSTTEXTUAL_LOCATOR)
    pagination_locator = load_json(PAGINATION_LOCATOR)

    if manifest.get("schema_version") != 1 or manifest.get("phase") != "N10":
        fail("invalid manifest schema/phase")
    if manifest.get("scope") != "posttextual-and-multivolume":
        fail("unexpected N10 scope label")

    post_ids = manifest.get("posttextual_rule_ids", [])
    cross_ids = manifest.get("cross_scope_rule_ids", [])
    if not isinstance(post_ids, list) or not isinstance(cross_ids, list):
        fail("scope lists must be arrays")
    expected_scope = set(post_ids) | set(cross_ids)
    if len(expected_scope) != 20 or manifest.get("total_rules") != 20:
        fail(f"expected exactly 20 N10 rules, found {len(expected_scope)}")
    if len(post_ids) != 17 or len(cross_ids) != 3:
        fail(f"unexpected N10 partition: posttextual={len(post_ids)} cross={len(cross_ids)}")

    locator_post_ids: set[str] = set()
    for item in post_locator.get("rulesets", []):
        if not isinstance(item, dict):
            continue
        if item.get("status") != manifest["authority_policy"]["posttextual_locator_status"]:
            fail(f"posttextual locator status drifted for {item.get('id')}")
        locator_post_ids.update(item.get("rule_ids", []))
    if locator_post_ids != set(post_ids):
        fail(
            "posttextual locator scope drifted: "
            f"manifest_only={sorted(set(post_ids) - locator_post_ids)} "
            f"locator_only={sorted(locator_post_ids - set(post_ids))}"
        )

    pagination = ruleset(pagination_locator, "pagination.general")
    if pagination.get("status") != manifest["authority_policy"]["pagination_locator_status"]:
        fail("pagination locator status drifted")
    pagination_ids = set(pagination.get("rule_ids", []))
    reserved = {"pagination.multivolume.continuous", "pagination.appendix-annex.continuous"}
    if not reserved <= pagination_ids:
        fail(f"N10 pagination rules escaped pagination.general: {sorted(reserved - pagination_ids)}")
    if set(cross_ids) != reserved | {"volume.number.cover-title-page"}:
        fail(f"cross-scope rule set drifted: {cross_ids}")

    contract = load_full_contract()
    contract_rules = {rule["id"]: rule for rule in contract["rules"]}
    missing = sorted(expected_scope - set(contract_rules))
    if missing:
        fail(f"N10 rules missing from full contract: {missing}")
    non_normative = sorted(
        rule_id for rule_id in expected_scope
        if contract_rules[rule_id].get("authority") == "project-policy"
    )
    if non_normative:
        fail(f"project-policy rules leaked into N10 normative scope: {non_normative}")

    bounded = manifest.get("existing_bounded_positive", [])
    bounded_ids = {
        item.get("rule_id") for item in bounded if isinstance(item, dict)
    }
    expected_bounded = {"volume.number.cover-title-page", "pagination.multivolume.continuous"}
    if bounded_ids != expected_bounded or len(bounded) != 2:
        fail(f"bounded baseline drifted: {sorted(item for item in bounded_ids if item)}")

    support_ids = set(manifest.get("support_only_rule_ids", []))
    if support_ids != expected_scope - expected_bounded or len(support_ids) != 18:
        fail(
            "support-only partition drifted: "
            f"missing={sorted((expected_scope - expected_bounded) - support_ids)} "
            f"extra={sorted(support_ids - (expected_scope - expected_bounded))}"
        )
    if bounded_ids & support_ids:
        fail("bounded and support-only sets overlap")

    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    runner_text = RUNNER.read_text(encoding="utf-8")
    required_checks = manifest.get("required_pr_check_ids", [])
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
    campaign_ids = {item.get("id") for item in campaigns if isinstance(item, dict)}
    if campaign_ids != {"appendix-annex-final-pdf", "index-glossary-final-pdf"}:
        fail(f"unexpected N10 campaign set: {sorted(item for item in campaign_ids if item)}")
    campaign_rule_ids: set[str] = set()
    campaign_count = 0
    for item in campaigns:
        ids = item.get("rule_ids", [])
        if item.get("rules") != len(ids):
            fail(f"campaign {item.get('id')} rule count drifted")
        overlap = campaign_rule_ids & set(ids)
        if overlap:
            fail(f"campaign rules overlap: {sorted(overlap)}")
        campaign_rule_ids.update(ids)
        campaign_count += len(ids)
    if campaign_rule_ids != support_ids or campaign_count != 18:
        fail(
            "campaigns do not cover exactly the support-only residuals: "
            f"missing={sorted(support_ids - campaign_rule_ids)} "
            f"extra={sorted(campaign_rule_ids - support_ids)} count={campaign_count}"
        )

    policy = manifest.get("authority_policy", {})
    if policy.get("proof_state_changed") is not False:
        fail("scope reconciliation must not change proof-state")
    if policy.get("broad_posttextual_regressions_are_support_only") is not True:
        fail("broad posttextual regressions must remain support-only")

    host = manifest.get("scope_checker_host", {})
    host_script = ROOT / host.get("script", "")
    if host.get("check_id") != "posttextual" or not host_script.is_file():
        fail("invalid N10 scope-checker host")
    host_text = host_script.read_text(encoding="utf-8")
    if host.get("checker") not in host_text:
        fail("N10 scope checker is not wired into its mandatory PR host")

    print(
        "N10-EVIDENCE scope-reconciliation "
        f"total={len(expected_scope)} existing_bounded_positive={len(bounded_ids)} "
        f"support_only={len(support_ids)}"
    )
    print("N10-EVIDENCE bounded-existing rule_ids=" + json.dumps(sorted(bounded_ids)))
    print("N10-EVIDENCE support-only rule_ids=" + json.dumps(sorted(support_ids)))
    print(
        "N10-EVIDENCE campaign-plan "
        f"campaigns={len(campaigns)} residual_rules={campaign_count} "
        "split=13+5"
    )
    print(
        "N10-EVIDENCE authority-boundary "
        "posttextual=PARTIAL_WITH_REASON pagination=PARTIAL_WITH_REASON "
        "proof_state_changed=false"
    )


if __name__ == "__main__":
    main()
