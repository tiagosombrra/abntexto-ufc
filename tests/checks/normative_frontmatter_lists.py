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

SCENARIO = ROOT / "standards" / "frontmatter-lists-scenario.json"
RULE_ORDER = [
    "list.illustrations.optional",
    "list.tables.optional",
    "list.abbreviations.optional",
    "list.symbols.optional",
]


def fail(message: str) -> None:
    raise SystemExit(f"Optional lists validation failed: {message}")


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


def record(rule_id: str, status: str, expected: Any, measured: Any) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftotext -bbox-layout",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure front matter optional front matter list final-PDF evidence."
    )
    parser.add_argument("illustrations_pdf", type=Path)
    parser.add_argument("tables_pdf", type=Path)
    parser.add_argument("abbreviations_pdf", type=Path)
    parser.add_argument("symbols_pdf", type=Path)
    parser.add_argument("absent_pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    present_pdfs = {
        RULE_ORDER[0]: args.illustrations_pdf,
        RULE_ORDER[1]: args.tables_pdf,
        RULE_ORDER[2]: args.abbreviations_pdf,
        RULE_ORDER[3]: args.symbols_pdf,
    }
    for pdf in [*present_pdfs.values(), args.absent_pdf]:
        if not pdf.is_file():
            fail(f"PDF not found: {pdf}")

    scenario = load_json(SCENARIO)
    if (
        scenario.get("schema_version") != 2

        or scenario.get("component") != "optional-frontmatter-lists"
    ):
        fail("invalid optional-list scenario schema/component")

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
    if scenario.get("rules") != RULE_ORDER:
        fail("optional-list rule order drift")

    list_specs = scenario.get("lists")
    if not isinstance(list_specs, dict) or set(list_specs) != scenario_scope:
        fail("list specification keys must match the scenario rule scope exactly")
    for rule_id, spec in list_specs.items():
        if not isinstance(spec, dict) or set(spec) != {"heading"}:
            fail(f"invalid list specification for {rule_id}")
        heading = spec.get("heading")
        if not isinstance(heading, str) or not heading:
            fail(f"empty list heading for {rule_id}")

    fixtures = scenario.get("fixtures")
    expected_fixture_keys = scenario_scope | {"absent"}
    if not isinstance(fixtures, dict) or set(fixtures) != expected_fixture_keys:
        fail("fixture mapping must contain exactly four rule fixtures plus absent")

    sentinel = scenario.get("sentinel")
    if not isinstance(sentinel, str) or not sentinel:
        fail("sentinel marker is required")

    try:
        present_pages = {
            rule_id: bbox_pages(pdf) for rule_id, pdf in present_pdfs.items()
        }
        absent_pages = bbox_pages(args.absent_pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    fixture_summary: dict[str, Any] = {}
    for rule_id, pages in present_pages.items():
        sentinel_pages = marker_pages(pages, sentinel)
        if len(sentinel_pages) != 1:
            fail(f"sentinel must occur once for {rule_id}: {sentinel_pages}")
        fixture_summary[rule_id] = {
            "page_count": len(pages),
            "sentinel_pages": sentinel_pages,
        }

    absent_sentinel = marker_pages(absent_pages, sentinel)
    if len(absent_sentinel) != 1:
        fail(f"absent sentinel must occur once: {absent_sentinel}")

    evidence: list[dict[str, Any]] = []
    for rule_id in RULE_ORDER:
        rule = rules[rule_id]
        required = rule.get("values", {}).get("required")
        heading = list_specs[rule_id]["heading"]
        own_heading_pages = marker_pages(present_pages[rule_id], heading)
        absent_heading_pages = marker_pages(absent_pages, heading)

        passed = (
            required is False
            and len(own_heading_pages) == 1
            and len(absent_heading_pages) == 0
        )
        evidence.append(
            record(
                rule_id,
                "PASS" if passed else "FAIL",
                {"required": required},
                {
                    "present_heading_pages": own_heading_pages,
                    "absent_heading_pages": absent_heading_pages,
                },
            )
        )

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"

    payload = {
        "schema_version": 1,
        "validation_scope": "frontmatter",
        "component": "optional-frontmatter-lists",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "present_fixtures": fixture_summary,
        "absent_fixture": {
            "page_count": len(absent_pages),
            "sentinel_pages": absent_sentinel,
        },
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "FRONTMATTER-EVIDENCE optional-lists-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" present_fixtures={len(present_pages)}"
        + f" absent_pages={len(absent_pages)}"
    )
    for item in evidence:
        print(
            f"FRONTMATTER-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )


if __name__ == "__main__":
    main()
