#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "normativa" / "catalog.json"
PLAN = ROOT / "normativa" / "atomicity-plan.json"


def fail(message: str) -> None:
    raise SystemExit(f"Normative atomicity plan failed: {message}")


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    plan = json.loads(PLAN.read_text(encoding="utf-8"))

    if plan.get("schema_version") != 1:
        fail("unsupported schema_version")
    if plan.get("statuses") != ["keep-atomic", "split", "retire-in-n4"]:
        fail("unexpected status vocabulary")

    catalog_ids = {rule["id"] for rule in catalog["rules"]}
    entries = plan.get("rules")
    if not isinstance(entries, dict):
        fail("rules must be an object")
    if set(entries) != catalog_ids:
        missing = sorted(catalog_ids - set(entries))
        extra = sorted(set(entries) - catalog_ids)
        fail(f"catalog coverage mismatch; missing={missing}, extra={extra}")

    target_owner: dict[str, str] = {}
    split_count = 0
    target_count = 0
    for parent, entry in entries.items():
        status = entry.get("status")
        if status not in plan["statuses"]:
            fail(f"{parent}: invalid status {status}")
        targets = entry.get("targets", [])
        if status == "split":
            split_count += 1
            if not isinstance(targets, list) or len(targets) < 2:
                fail(f"{parent}: split requires at least two targets")
            if len(targets) != len(set(targets)):
                fail(f"{parent}: duplicate targets")
            for target in targets:
                if not isinstance(target, str) or not target:
                    fail(f"{parent}: invalid target id")
                if target in catalog_ids:
                    fail(f"{parent}: atomic target collides with current catalog rule {target}")
                owner = target_owner.get(target)
                if owner:
                    fail(f"atomic target {target} assigned to both {owner} and {parent}")
                target_owner[target] = parent
            target_count += len(targets)
        elif targets:
            fail(f"{parent}: only split entries may declare targets")

        if status == "retire-in-n4" and not entry.get("reason"):
            fail(f"{parent}: retirement requires a reason")

    if entries["deposit.pdfa"]["targets"] != ["deposit.pdfa.required", "pdfa.profile.project"]:
        fail("PDF/A institutional requirement and project profile must be separated")
    if entries["project.standard"]["status"] != "retire-in-n4":
        fail("project.standard must be replaced by individual NBR 15287 rules")

    print(
        "Normative atomicity plan passed: "
        f"{len(entries)} parent rules, {split_count} composite rules, "
        f"{target_count} planned atomic targets."
    )


if __name__ == "__main__":
    main()
