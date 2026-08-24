#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import ACTIVE_STATUSES, load_catalog, source_map
from normative_full import load_full_contract

RECONCILIATION = ROOT / "normativa" / "reconciliation.json"
VERSION_POLICY = ROOT / "normativa" / "version-policy.json"
SOURCE_AUDIT = ROOT / "normativa" / "source-audit.json"

DETAIL_CLASSIFICATIONS = {
    "current-compatible-institutional-requirement",
    "superseded-guidance",
    "recommendation",
    "project-policy",
    "unknown-review",
}


def fail(message: str) -> None:
    raise SystemExit(f"Normative reconciliation failed: {message}")


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {label}: {exc}")
    if not isinstance(data, dict):
        fail(f"{label} must be an object")
    return data


def source_is_ufc(source: dict[str, Any]) -> bool:
    return source.get("publisher") == "Universidade Federal do Ceará"


def classify_rule(
    rule: dict[str, Any],
    runtime_sources: dict[str, dict[str, Any]],
) -> tuple[str | None, list[str]]:
    authority = rule.get("authority", "normative")
    if authority == "project-policy":
        return "project-policy", []
    if authority != "normative":
        return None, []

    resolution = rule.get("resolution")
    if not isinstance(resolution, dict):
        return "unknown-review", []
    if resolution.get("status") != "resolved":
        return "unknown-review", []

    governing = resolution.get("governing_sources", [])
    if not isinstance(governing, list) or not governing:
        return "unknown-review", []

    ufc_governing = [
        source_id
        for source_id in governing
        if source_id in runtime_sources and source_is_ufc(runtime_sources[source_id])
    ]
    if not ufc_governing:
        return None, []

    normativity = str(rule.get("normativity", "")).lower()
    if "recommendation" in normativity:
        return "recommendation", ufc_governing
    if "project-policy" in normativity:
        return "project-policy", ufc_governing
    return "current-compatible-institutional-requirement", ufc_governing


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    reconciliation = load_json(RECONCILIATION, "N2 reconciliation ledger")
    version_policy = load_json(VERSION_POLICY, "version policy")
    source_audit = load_json(SOURCE_AUDIT, "source audit")
    catalog = load_catalog()
    contract = load_full_contract(catalog)
    runtime_sources = source_map(catalog)

    if reconciliation.get("schema_version") != 1:
        fail("unsupported reconciliation schema_version")
    try:
        reconciliation_reviewed = date.fromisoformat(reconciliation["reviewed_at"])
        version_reviewed = date.fromisoformat(version_policy["reviewed_at"])
        source_reviewed = date.fromisoformat(source_audit["reviewed_at"])
    except (KeyError, TypeError, ValueError) as exc:
        fail("reconciliation, version policy and source audit need ISO reviewed_at")
        raise AssertionError from exc
    if reconciliation_reviewed < max(version_reviewed, source_reviewed):
        fail("reconciliation ledger is older than its source contracts")

    classifications = reconciliation.get("detail_classifications")
    if not isinstance(classifications, dict) or set(classifications) != DETAIL_CLASSIFICATIONS:
        fail("detail classification vocabulary does not match the N2 roadmap")
    if reconciliation.get("unknown_review_allowed_at_n2_exit") is not False:
        fail("N2 exit must not permit unknown-review relationships")

    audited_sources = {
        source["id"]: source
        for source in source_audit.get("sources", [])
        if isinstance(source, dict) and isinstance(source.get("id"), str)
    }
    if not audited_sources:
        fail("source audit has no usable sources")

    for source_id, source in audited_sources.items():
        if source.get("kind") == "institutional-guide" and source_is_ufc(source):
            if source.get("technical_authority") is not False:
                fail(f"UFC guide must not claim technical authority: {source_id}")

    ledger_mappings = reconciliation.get("superseded_references")
    policy_mappings = version_policy.get("supersessions")
    if not isinstance(ledger_mappings, list) or not ledger_mappings:
        fail("reconciliation ledger needs superseded_references")
    if not isinstance(policy_mappings, list) or not policy_mappings:
        fail("version policy needs supersessions")

    def mapping_key(item: dict[str, Any]) -> tuple[str, str, str, str]:
        fields = (
            "context_source",
            "superseded_reference",
            "current_reference",
            "current_source",
        )
        values = tuple(item.get(field) for field in fields)
        if not all(isinstance(value, str) and value for value in values):
            fail("every supersession mapping needs complete source/reference fields")
        return values  # type: ignore[return-value]

    ledger_by_key: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for item in ledger_mappings:
        if not isinstance(item, dict):
            fail("every reconciliation supersession entry must be an object")
        key = mapping_key(item)
        if key in ledger_by_key:
            fail(f"duplicate reconciliation mapping: {key}")
        if item.get("classification") != "superseded-guidance":
            fail(f"stale technical reference is not classified as superseded-guidance: {key}")
        if item.get("conflict_status") != "resolved-current-edition":
            fail(f"stale technical reference is not explicitly resolved to current edition: {key}")
        ledger_by_key[key] = item

    policy_keys = {
        mapping_key(item)
        for item in policy_mappings
        if isinstance(item, dict)
    }
    if set(ledger_by_key) != policy_keys:
        missing = sorted(policy_keys - set(ledger_by_key))
        extra = sorted(set(ledger_by_key) - policy_keys)
        fail(f"reconciliation/version-policy mapping drift; missing={missing}, extra={extra}")

    for context, _old, _current, current_source in ledger_by_key:
        context_source = audited_sources.get(context)
        if not context_source:
            fail(f"unknown UFC context source in reconciliation: {context}")
        if context_source.get("kind") != "institutional-guide" or not source_is_ufc(context_source):
            fail(f"superseded guidance context is not a UFC institutional guide: {context}")
        if context_source.get("technical_authority") is not False:
            fail(f"superseded guidance context claims technical authority: {context}")
        replacement = runtime_sources.get(current_source)
        if not replacement:
            fail(f"current replacement source is absent from runtime catalog: {current_source}")
        if replacement.get("kind") != "technical-standard":
            fail(f"current replacement is not a technical standard: {current_source}")
        if replacement.get("status") not in ACTIVE_STATUSES:
            fail(f"current replacement is not active: {current_source}")

    runtime_ufc_guides = {
        source_id
        for source_id, source in runtime_sources.items()
        if source.get("role") == "institutional-guide" and source_is_ufc(source)
    }
    for source_id in runtime_ufc_guides:
        audited = audited_sources.get(source_id)
        if not audited:
            fail(f"runtime UFC guide is absent from source audit: {source_id}")
        if audited.get("technical_authority") is not False:
            fail(f"runtime UFC guide is not explicitly non-technical in source audit: {source_id}")

    counts: Counter[str] = Counter()
    rule_report: list[dict[str, Any]] = []
    technical_with_ufc_support = 0

    for rule in contract["rules"]:
        classification, governing_ufc = classify_rule(rule, runtime_sources)
        resolution = rule.get("resolution")
        sources = rule.get("sources", [])

        if rule.get("authority", "normative") == "normative" and isinstance(resolution, dict):
            scope = resolution.get("scope")
            governing = resolution.get("governing_sources", [])
            if scope == "technical":
                governing_guides = [
                    source_id
                    for source_id in governing
                    if source_id in runtime_sources
                    and runtime_sources[source_id].get("role") == "institutional-guide"
                ]
                if governing_guides:
                    fail(
                        f"technical rule is governed by UFC institutional guide: "
                        f"{rule['id']} / {governing_guides}"
                    )

        if classification:
            counts[classification] += 1
            rule_report.append(
                {
                    "rule_id": rule["id"],
                    "classification": classification,
                    "governing_ufc_sources": governing_ufc,
                }
            )
        elif rule.get("authority", "normative") == "normative":
            ufc_support = [
                source_id
                for source_id in sources
                if source_id in runtime_sources and source_is_ufc(runtime_sources[source_id])
            ]
            if ufc_support:
                technical_with_ufc_support += 1

    if counts["unknown-review"]:
        unresolved = [
            item["rule_id"]
            for item in rule_report
            if item["classification"] == "unknown-review"
        ]
        fail("N2 has unresolved unknown-review rules: " + ", ".join(unresolved))

    if not counts["current-compatible-institutional-requirement"]:
        fail("no UFC-governed institutional details were classified")
    if not counts["recommendation"]:
        fail("no UFC recommendation was classified; expected adopted recommendation paths")
    if not counts["project-policy"]:
        fail("no project-policy detail was classified")

    report = {
        "schema_version": 1,
        "reviewed_at": reconciliation["reviewed_at"],
        "superseded_guidance_mappings": len(ledger_by_key),
        "detail_counts": dict(sorted(counts.items())),
        "technical_rules_with_compatible_ufc_support": technical_with_ufc_support,
        "rules": rule_report,
    }
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "Normative reconciliation passed: "
        f"{len(ledger_by_key)} superseded UFC technical-reference mappings; "
        f"institutional={counts['current-compatible-institutional-requirement']}, "
        f"recommendation={counts['recommendation']}, "
        f"project-policy={counts['project-policy']}, "
        f"technical-with-UFC-support={technical_with_ufc_support}, "
        f"unknown-review={counts['unknown-review']}."
    )


if __name__ == "__main__":
    main()
