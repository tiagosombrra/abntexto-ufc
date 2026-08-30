#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract

AUDIT = ROOT / "standards" / "locator-audit.json"
SUPPLEMENT_GLOB = "locator-audit-*.json"
SOURCE_STATUSES = {"VERIFIED", "UNAVAILABLE_WITH_REASON", "NOT_APPLICABLE"}


def fail(message: str) -> None:
    raise SystemExit(f"Normative locator audit failed: {message}")


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {label}: {exc}")
    if not isinstance(data, dict):
        fail(f"{label} must be an object")
    return data


def load_audit() -> dict[str, Any]:
    data = load_json(AUDIT, "locator audit")
    if data.get("schema_version") != 1:
        fail("unsupported schema_version")
    if data.get("coverage_mode") not in {"incremental", "complete"}:
        fail("coverage_mode must be incremental or complete")
    policy = data.get("policy")
    if not isinstance(policy, dict):
        fail("policy block is required")
    allowed = policy.get("allowed_statuses")
    if not isinstance(allowed, list) or not allowed:
        fail("policy allowed_statuses must be a non-empty list")

    rulesets = data.get("rulesets")
    if not isinstance(rulesets, list) or not rulesets:
        fail("rulesets must be a non-empty list")

    reviewed_dates = [data.get("reviewed_at")]
    merged_rulesets = list(rulesets)
    for path in sorted(AUDIT.parent.glob(SUPPLEMENT_GLOB)):
        supplement = load_json(path, f"locator audit supplement {path.name}")
        if supplement.get("schema_version") != 1:
            fail(f"{path.name}: unsupported schema_version")
        supplement_rulesets = supplement.get("rulesets")
        if not isinstance(supplement_rulesets, list) or not supplement_rulesets:
            fail(f"{path.name}: rulesets must be a non-empty list")
        reviewed_dates.append(supplement.get("reviewed_at"))
        merged_rulesets.extend(supplement_rulesets)

    data["rulesets"] = merged_rulesets
    data["manifest_reviewed_at"] = reviewed_dates
    return data


def validate_source_checks(
    rule_id: str,
    rule: dict[str, Any],
    ruleset_status: str,
    checks: Any,
) -> None:
    if not isinstance(checks, list) or not checks:
        fail(f"{rule_id}: source_checks must be a non-empty list")

    by_source: dict[str, dict[str, Any]] = {}
    for check in checks:
        if not isinstance(check, dict):
            fail(f"{rule_id}: every source check must be an object")
        source_id = check.get("source_id")
        if not isinstance(source_id, str) or not source_id or source_id in by_source:
            fail(f"{rule_id}: invalid or duplicate source check {source_id}")
        status = check.get("status")
        if status not in SOURCE_STATUSES:
            fail(f"{rule_id}: invalid source-check status {status}")
        try:
            date.fromisoformat(check["checked_at"])
        except (KeyError, TypeError, ValueError) as exc:
            fail(f"{rule_id}: source check {source_id} needs ISO checked_at")
            raise AssertionError from exc

        if status == "VERIFIED":
            if not isinstance(check.get("locator"), str) or not check["locator"].strip():
                fail(f"{rule_id}: verified source {source_id} needs a locator")
        elif status == "UNAVAILABLE_WITH_REASON":
            if check.get("locator") not in {None, ""}:
                fail(f"{rule_id}: unavailable source {source_id} must not claim a locator")
            if not isinstance(check.get("reason"), str) or not check["reason"].strip():
                fail(f"{rule_id}: unavailable source {source_id} needs a reason")
        elif status == "NOT_APPLICABLE" and rule.get("authority") == "normative":
            fail(f"{rule_id}: normative source cannot be NOT_APPLICABLE")
        by_source[source_id] = check

    expected_sources = set(rule.get("sources", []))
    if set(by_source) != expected_sources:
        missing = sorted(expected_sources - set(by_source))
        extra = sorted(set(by_source) - expected_sources)
        fail(f"{rule_id}: source-check coverage mismatch; missing={missing}, extra={extra}")

    source_states = {check["status"] for check in checks}
    if ruleset_status == "VERIFIED" and source_states != {"VERIFIED"}:
        fail(f"{rule_id}: VERIFIED ruleset requires every source to be VERIFIED")
    if ruleset_status == "PARTIAL_WITH_REASON":
        if "VERIFIED" not in source_states or "UNAVAILABLE_WITH_REASON" not in source_states:
            fail(f"{rule_id}: PARTIAL_WITH_REASON requires verified and unavailable-with-reason sources")
    if ruleset_status == "UNAVAILABLE_WITH_REASON" and source_states != {"UNAVAILABLE_WITH_REASON"}:
        fail(f"{rule_id}: UNAVAILABLE_WITH_REASON requires every source to be unavailable")


def main() -> None:
    audit = load_audit()
    contract = load_full_contract()
    contract_reviewed = date.fromisoformat(contract["reviewed_at"])

    manifest_dates: list[date] = []
    for reviewed_at in audit["manifest_reviewed_at"]:
        try:
            manifest_dates.append(date.fromisoformat(reviewed_at))
        except (TypeError, ValueError) as exc:
            fail("every locator audit manifest needs an ISO reviewed_at")
            raise AssertionError from exc
    if max(manifest_dates) < contract_reviewed:
        fail("incremental locator audit set does not reach the current full-contract review")

    rules = {rule["id"]: rule for rule in contract["rules"]}
    normative_ids = {rule_id for rule_id, rule in rules.items() if rule.get("authority") == "normative"}
    allowed_statuses = set(audit["policy"]["allowed_statuses"])

    rulesets = audit["rulesets"]
    seen_rulesets: set[str] = set()
    audited_rules: set[str] = set()
    status_counts: Counter[str] = Counter()

    for ruleset in rulesets:
        if not isinstance(ruleset, dict):
            fail("every ruleset must be an object")
        ruleset_id = ruleset.get("id")
        if not isinstance(ruleset_id, str) or not ruleset_id or ruleset_id in seen_rulesets:
            fail(f"invalid or duplicate ruleset id: {ruleset_id}")
        seen_rulesets.add(ruleset_id)

        status = ruleset.get("status")
        if status not in allowed_statuses:
            fail(f"{ruleset_id}: invalid status {status}")
        rule_ids = ruleset.get("rule_ids")
        if not isinstance(rule_ids, list) or not rule_ids:
            fail(f"{ruleset_id}: rule_ids must be a non-empty list")
        locator = ruleset.get("current_locator")
        checks = ruleset.get("source_checks")

        for rule_id in rule_ids:
            if not isinstance(rule_id, str) or not rule_id:
                fail(f"{ruleset_id}: invalid rule id")
            if rule_id in audited_rules:
                fail(f"rule appears in more than one ruleset: {rule_id}")
            rule = rules.get(rule_id)
            if rule is None:
                fail(f"{ruleset_id}: unknown rule {rule_id}")
            if rule.get("authority") != "normative":
                if status != "NOT_APPLICABLE":
                    fail(f"{rule_id}: non-normative rule must be NOT_APPLICABLE")
            elif status == "NOT_APPLICABLE":
                fail(f"{rule_id}: normative rule cannot be NOT_APPLICABLE")
            if rule.get("locator") != locator:
                fail(f"{rule_id}: locator drift; audit={locator!r}, contract={rule.get('locator')!r}")
            validate_source_checks(rule_id, rule, status, checks)
            audited_rules.add(rule_id)
            status_counts[status] += 1

    audited_normative = audited_rules & normative_ids
    remaining = normative_ids - audited_normative
    if audit["coverage_mode"] == "complete" and remaining:
        fail("complete locator audit has unclassified normative rules: " + ", ".join(sorted(remaining)))

    status_counts["UNASSESSED"] = len(remaining)
    summary = ", ".join(f"{status}={count}" for status, count in sorted(status_counts.items()))
    print(
        "Normative locator audit: "
        f"{len(audited_normative)}/{len(normative_ids)} normative rules explicitly classified; "
        f"{summary}; mode={audit['coverage_mode']}; latest_manifest={max(manifest_dates).isoformat()}."
    )


if __name__ == "__main__":
    main()
