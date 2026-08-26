#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "normativa" / "n9-scope-reconciliation.json"
CAMPAIGN_PLAN = ROOT / "normativa" / "n9-campaign-plan.json"
PROMOTIONS = ROOT / "normativa" / "n9-bounded-promotions.json"
PR_WORKFLOW = ROOT / ".github" / "workflows" / "latex-preflight.yml"
PR_CHECK_SCRIPTS = {
    "object-geometry": "tests/v2-object-geometry-check.sh",
    "objects": "tests/v2-object-check.sh",
    "table-ibge": "tests/v2-table-ibge-check.sh",
    "documentary-source": "tests/v2-documentary-source-check.sh",
    "normative-complement": "tests/v2-normative-complement-check.sh",
    "math": "tests/v2-math-check.sh",
    "code-typography": "tests/v2-code-typography-check.sh",
}


def fail(message: str) -> None:
    raise SystemExit(f"N9 bounded promotion check failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def classified_rules(groups: list[dict[str, Any]], classification: str) -> set[str]:
    result: set[str] = set()
    for group in groups:
        if group.get("classification") != classification:
            continue
        values = group.get("rule_ids")
        if not isinstance(values, list) or not values:
            fail(f"group {group.get('id')}: invalid rule_ids")
        duplicate = result & set(values)
        if duplicate:
            fail(f"duplicate {classification} rules: {sorted(duplicate)}")
        result.update(values)
    return result


def selected_pr_checks() -> set[str]:
    source = PR_WORKFLOW.read_text(encoding="utf-8", errors="replace")
    selected: set[str] = set()
    for match in re.findall(r"--only\s+([A-Za-z0-9_.-]+(?:,[A-Za-z0-9_.-]+)*)", source):
        selected.update(item for item in match.split(",") if item)
    if not selected:
        fail("PR workflow contains no tests/run.py --only selections")
    return selected


def verify_repo_evidence(entry: dict[str, Any], selected: set[str]) -> None:
    sources = entry.get("evidence_sources")
    if not isinstance(sources, list) or not sources:
        fail(f"{entry.get('id')}: evidence_sources are required")
    for relative in sources:
        if not isinstance(relative, str) or not (ROOT / relative).is_file():
            fail(f"{entry.get('id')}: missing evidence source {relative}")

    checks = entry.get("required_pr_checks")
    if not isinstance(checks, list) or not checks:
        fail(f"{entry.get('id')}: required_pr_checks are required")
    missing = sorted(set(checks) - selected)
    if missing:
        fail(f"{entry.get('id')}: evidence left PR preflight: {missing}")
    for check in checks:
        script = PR_CHECK_SCRIPTS.get(check)
        if script is None or script not in sources:
            fail(f"{entry.get('id')}: PR check {check} is not tied to its script")

    tokens = entry.get("required_tokens")
    if not isinstance(tokens, dict) or not tokens:
        fail(f"{entry.get('id')}: required_tokens are required")
    for relative, required in tokens.items():
        path = ROOT / relative
        if not path.is_file() or not isinstance(required, list) or not required:
            fail(f"{entry.get('id')}: invalid token source {relative}")
        source = path.read_text(encoding="utf-8", errors="replace")
        absent = [token for token in required if token not in source]
        if absent:
            fail(f"{entry.get('id')}: evidence drift in {relative}: {absent}")


def verify_runtime(entry: dict[str, Any], expected_sha: str) -> dict[str, Any]:
    relative = entry.get("evidence_json")
    if not isinstance(relative, str) or not relative:
        fail(f"{entry.get('id')}: evidence_json is required")
    evidence = load_json(ROOT / relative)
    if evidence.get("phase") != "N9" or evidence.get("result") != "PASS":
        fail(f"{entry.get('id')}: runtime evidence did not PASS")
    if evidence.get("proof_state_changed") is not False:
        fail(f"{entry.get('id')}: runtime evidence changed proof-state")
    actual_sha = evidence.get("source_commit_sha", "")
    if expected_sha and actual_sha != expected_sha:
        fail(f"{entry.get('id')}: runtime SHA mismatch: expected={expected_sha}, actual={actual_sha}")
    return evidence


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate current N9 bounded-positive promotions.")
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    baseline = load_json(BASELINE)
    plan = load_json(CAMPAIGN_PLAN)
    promotions = load_json(PROMOTIONS)
    if baseline.get("schema_version") != 1 or baseline.get("phase") != "N9":
        fail("invalid baseline reconciliation")
    if plan.get("schema_version") != 1 or plan.get("phase") != "N9":
        fail("invalid campaign plan")
    if promotions.get("schema_version") != 1 or promotions.get("phase") != "N9":
        fail("invalid promotions schema/phase")

    required_policy = (
        "promotions_must_originate_from_baseline_support_only",
        "promotion_requires_runtime_pass_evidence",
        "promotion_requires_pr_preflight_binding",
        "proof_state_must_remain_unchanged",
    )
    policy = promotions.get("policy")
    if not isinstance(policy, dict) or not all(policy.get(key) is True for key in required_policy):
        fail("promotion policy drifted")

    groups = baseline.get("groups")
    if not isinstance(groups, list):
        fail("baseline groups are required")
    baseline_bounded = classified_rules(groups, "existing-bounded-positive")
    baseline_support = classified_rules(groups, "support-only")
    if len(baseline_bounded) != 7 or len(baseline_support) != 16 or baseline_bounded & baseline_support:
        fail("baseline 7/16 reconciliation drifted")

    campaigns = {
        item.get("id"): item for item in plan.get("campaigns", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    if set(campaigns) != {"illustration-final-pdf", "table-final-pdf", "equation-display-final-pdf"}:
        fail("campaign map drifted")

    selected = selected_pr_checks()
    expected_sha = args.commit_sha or os.environ.get("SOURCE_COMMIT_SHA") or os.environ.get("GITHUB_SHA") or ""
    entries = promotions.get("promotions")
    if not isinstance(entries, list):
        fail("promotions must be a list")

    promoted: set[str] = set()
    runtime_summaries: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            fail("promotion entries must be objects")
        promotion_id = entry.get("id")
        campaign_id = entry.get("campaign_id")
        if not isinstance(promotion_id, str) or campaign_id not in campaigns:
            fail(f"invalid promotion/campaign: {promotion_id}/{campaign_id}")
        values = entry.get("rule_ids")
        if not isinstance(values, list) or not values or len(values) != len(set(values)):
            fail(f"{promotion_id}: invalid rule_ids")
        entry_rules = set(values)
        campaign_rules = set(campaigns[campaign_id].get("rule_ids", []))
        if not entry_rules <= campaign_rules:
            fail(f"{promotion_id}: rules escaped campaign {campaign_id}")
        if not entry_rules <= baseline_support:
            fail(f"{promotion_id}: promotion did not originate from baseline support-only")
        if promoted & entry_rules:
            fail(f"{promotion_id}: rules promoted more than once")
        if entry.get("proof_state_changed") is not False:
            fail(f"{promotion_id}: promotion must not change proof-state")

        verify_repo_evidence(entry, selected)
        runtime = verify_runtime(entry, expected_sha)
        passed_rules = {
            item.get("rule_id") for item in runtime.get("evidence", [])
            if isinstance(item, dict) and item.get("status") == "PASS"
        }
        if passed_rules != entry_rules:
            fail(f"{promotion_id}: runtime PASS rule set mismatch")
        promoted.update(entry_rules)
        runtime_summaries.append({"id": promotion_id, "campaign_id": campaign_id, "rules": len(entry_rules), "evidence_json": entry["evidence_json"]})

    current_bounded = baseline_bounded | promoted
    current_support = baseline_support - promoted
    measured = {
        "total": 23,
        "baseline_existing_bounded_positive": len(baseline_bounded),
        "promoted_bounded_positive": len(promoted),
        "current_existing_bounded_positive": len(current_bounded),
        "current_support_only": len(current_support),
    }
    if promotions.get("expected_counts") != measured:
        fail(f"promotion count drift: expected={promotions.get('expected_counts')}, measured={measured}")

    print("N9-EVIDENCE bounded-progress " + " ".join(f"{key}={value}" for key, value in measured.items()))
    print("N9-EVIDENCE promoted rule_ids=" + json.dumps(sorted(promoted), ensure_ascii=False))
    print("N9-EVIDENCE current-support-only rule_ids=" + json.dumps(sorted(current_support), ensure_ascii=False))
    print("N9-EVIDENCE promotion-runtime " + json.dumps(runtime_summaries, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
