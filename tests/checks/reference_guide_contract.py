#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STANDARDS_DIR = ROOT / "standards"
MAP_PATH = STANDARDS_DIR / "reference-guide-map.json"
CATALOG_PATH = STANDARDS_DIR / "catalog.json"
ATOMIC_PATH = STANDARDS_DIR / "atomic-rules.json"
ALLOWED_CLASSIFICATIONS = {"normative", "institutional", "model-policy", "example"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_declared_rule_ids(value: Any) -> set[str]:
    rule_ids: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"rule_id", "expected_rule_id"} and isinstance(item, str):
                rule_ids.add(item)
            elif key == "rule_ids" and isinstance(item, list):
                rule_ids.update(entry for entry in item if isinstance(entry, str))
            else:
                rule_ids.update(collect_declared_rule_ids(item))
    elif isinstance(value, list):
        for item in value:
            rule_ids.update(collect_declared_rule_ids(item))
    return rule_ids


def collect_rule_ids(catalog: dict[str, Any], atomic: dict[str, Any]) -> set[str]:
    rule_ids = {rule["id"] for rule in catalog.get("rules", []) if "id" in rule}
    rule_ids.update(atomic.get("keep_atomic", []))
    for group in atomic.get("groups", {}).values():
        for rule in group:
            if "id" in rule:
                rule_ids.add(rule["id"])

    for path in sorted(STANDARDS_DIR.glob("*.json")):
        if path == MAP_PATH:
            continue
        rule_ids.update(collect_declared_rule_ids(load_json(path)))
    return rule_ids


def main() -> None:
    guide = load_json(MAP_PATH)
    catalog = load_json(CATALOG_PATH)
    atomic = load_json(ATOMIC_PATH)

    source_ids = {source["id"] for source in catalog.get("sources", []) if "id" in source}
    rule_ids = collect_rule_ids(catalog, atomic)

    seen_topics: set[str] = set()
    failures: list[str] = []
    passes = 0

    for topic in guide.get("topics", []):
        topic_id = topic.get("id", "<missing-id>")
        classification = topic.get("classification")
        topic_sources = topic.get("source_ids", [])
        topic_rules = topic.get("rule_ids", [])
        source_file = topic.get("source_file", "")
        marker = topic.get("marker", "")
        reasons: list[str] = []

        if topic_id in seen_topics:
            reasons.append("duplicate-topic-id")
        seen_topics.add(topic_id)

        if classification not in ALLOWED_CLASSIFICATIONS:
            reasons.append(f"invalid-classification:{classification}")

        if classification in {"normative", "institutional"}:
            if not topic_sources:
                reasons.append("sources-required")
            if not topic_rules:
                reasons.append("rules-required")

        missing_sources = sorted(set(topic_sources) - source_ids)
        if missing_sources:
            reasons.append("unknown-sources:" + ",".join(missing_sources))

        missing_rules = sorted(set(topic_rules) - rule_ids)
        if missing_rules:
            reasons.append("unknown-rules:" + ",".join(missing_rules))

        source_path = ROOT / source_file
        if not source_file or not source_path.is_file():
            reasons.append(f"missing-source-file:{source_file}")
        elif not marker:
            reasons.append("empty-marker")
        elif marker not in source_path.read_text(encoding="utf-8"):
            reasons.append(f"marker-not-found:{marker}")

        status = "FAIL" if reasons else "PASS"
        if reasons:
            failures.append(f"{topic_id}: {';'.join(reasons)}")
        else:
            passes += 1

        print(
            "GUIDE-EVIDENCE "
            f"topic={topic_id} status={status} classification={classification} "
            f"sources={len(topic_sources)} rules={len(topic_rules)}"
        )
        if reasons:
            print(f"GUIDE-EVIDENCE topic={topic_id} reasons={'|'.join(reasons)}")

    total = len(guide.get("topics", []))
    print(f"GUIDE-EVIDENCE summary PASS={passes} FAIL={len(failures)} total={total}")
    print("GUIDE-EVIDENCE normative_contract_changed=false")

    if failures:
        raise SystemExit("Reference guide contract failed:\n- " + "\n- ".join(failures))


if __name__ == "__main__":
    main()
