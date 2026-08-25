#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize

SCENARIO = ROOT / "normativa" / "pretextual-lists-scenario.json"


def fail(message: str) -> None:
    raise SystemExit(f"Optional lists oracle failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def page_text(page: Any) -> str:
    return normalize(" ".join(word.text for word in page.words))


def marker_pages(pages: list[Any], marker: str) -> list[int]:
    wanted = normalize(marker)
    return [page.index for page in pages if wanted in page_text(page)]


def record(
    rule_id: str,
    status: str,
    expected: Any,
    measured: Any,
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftotext -bbox-layout",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure N6 optional pre-textual list final-PDF evidence."
    )
    parser.add_argument("present_pdf", type=Path)
    parser.add_argument("absent_pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    for pdf in (args.present_pdf, args.absent_pdf):
        if not pdf.is_file():
            fail(f"PDF not found: {pdf}")

    scenario = load_json(SCENARIO)
    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N6"
        or scenario.get("component") != "optional-pretextual-lists"
    ):
        fail("invalid optional-list scenario schema/phase/component")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    expected_scope = {
        rule_id
        for rule_id in rules
        if rule_id.startswith("list.") and rule_id.endswith(".optional")
    }
    scenario_scope = set(scenario.get("rules", []))
    if scenario_scope != expected_scope or len(expected_scope) != 4:
        fail(
            "optional-list scope mismatch: "
            f"scenario_only={sorted(scenario_scope - expected_scope)} "
            f"contract_only={sorted(expected_scope - scenario_scope)} "
            f"count={len(expected_scope)}"
        )

    list_specs = scenario.get("lists")
    if not isinstance(list_specs, dict) or set(list_specs) != scenario_scope:
        fail("list specification keys must match the scenario rule scope exactly")
    for rule_id, spec in list_specs.items():
        if not isinstance(spec, dict) or set(spec) != {"heading", "entry_marker"}:
            fail(f"invalid list specification for {rule_id}")
        if not all(isinstance(spec[key], str) and spec[key] for key in spec):
            fail(f"empty list marker for {rule_id}")

    sentinel = scenario.get("sentinel")
    if not isinstance(sentinel, str) or not sentinel:
        fail("sentinel marker is required")

    try:
        present_pages = bbox_pages(args.present_pdf)
        absent_pages = bbox_pages(args.absent_pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    present_sentinel = marker_pages(present_pages, sentinel)
    absent_sentinel = marker_pages(absent_pages, sentinel)
    if len(present_sentinel) != 1 or len(absent_sentinel) != 1:
        fail(
            "sentinel must occur on exactly one page in each fixture: "
            f"present={present_sentinel} absent={absent_sentinel}"
        )

    evidence: list[dict[str, Any]] = []
    supplemental: dict[str, Any] = {}

    for rule_id in scenario["rules"]:
        rule = rules[rule_id]
        required = rule.get("values", {}).get("required")
        spec = list_specs[rule_id]
        present_heading_pages = marker_pages(present_pages, spec["heading"])
        absent_heading_pages = marker_pages(absent_pages, spec["heading"])
        entry_pages = marker_pages(present_pages, spec["entry_marker"])

        passed = (
            required is False
            and len(present_heading_pages) == 1
            and len(absent_heading_pages) == 0
        )
        evidence.append(
            record(
                rule_id,
                "PASS" if passed else "FAIL",
                {"required": required},
                {
                    "present_heading_pages": present_heading_pages,
                    "absent_heading_pages": absent_heading_pages,
                },
            )
        )

        list_page = present_heading_pages[0] if len(present_heading_pages) == 1 else None
        supplemental[rule_id] = {
            "entry_marker": spec["entry_marker"],
            "entry_pages": entry_pages,
            "entry_observed_on_list_page": list_page in entry_pages if list_page else False,
        }

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    supplemental_pass = all(
        item["entry_observed_on_list_page"] for item in supplemental.values()
    )

    payload = {
        "schema_version": 1,
        "phase": "N6",
        "component": "optional-pretextual-lists",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "present_fixture": {
            "page_count": len(present_pages),
            "sentinel_pages": present_sentinel,
        },
        "absent_fixture": {
            "page_count": len(absent_pages),
            "sentinel_pages": absent_sentinel,
        },
        "supplemental_route_integrity": {
            "all_entries_observed_on_list_pages": supplemental_pass,
            "lists": supplemental,
        },
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "N6-EVIDENCE optional-lists-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" present_pages={len(present_pages)}"
        + f" absent_pages={len(absent_pages)}"
    )
    for item in evidence:
        print(
            f"N6-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
    print(
        "N6-EVIDENCE optional-lists-route-integrity "
        f"all_entries_observed_on_list_pages={str(supplemental_pass).lower()} "
        f"measured={json.dumps(supplemental, ensure_ascii=False, sort_keys=True)}"
    )


if __name__ == "__main__":
    main()
