#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize

SCENARIO = ROOT / "standards" / "section-hierarchy-scenario.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULE_ORDER = [
    "section.numbering.progressive",
    "section.levels.max",
    "section.primary.new-page",
]
LEVEL_ORDER = ["section", "subsection", "subsubsection", "paragraph", "subparagraph"]
NUMBER_RE = re.compile(r"[0-9]+(?:\.[0-9]+)*")


def fail(message: str) -> None:
    raise SystemExit(f"Section hierarchy validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def unique_word(pages: list[Any], marker: str) -> tuple[Any, Any]:
    wanted = normalize(marker)
    matches = [
        (page, word)
        for page in pages
        for word in page.words
        if normalize(word.text) == wanted
    ]
    if len(matches) != 1:
        fail(f"marker {marker!r}: expected one word, found {[(p.index, w.text) for p, w in matches]}")
    return matches[0]


def number_left_of_marker(page: Any, marker_word: Any, vertical_tolerance: float) -> str | None:
    candidates = [
        word
        for word in page.words
        if NUMBER_RE.fullmatch(word.text.strip())
        and word.box.x_max <= marker_word.box.x_min
        and abs(word.box.center_y - marker_word.box.center_y) <= vertical_tolerance
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda word: word.box.x_max).text.strip()


def record(rule_id: str, status: str, expected: Any, measured: Any) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftotext -bbox-layout",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure section-hierarchy evidence from a final PDF.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    policy = load_json(VALIDATION_POLICY)
    if (
        scenario.get("schema_version") != 1

        or scenario.get("component") != "section-hierarchy"
        or scenario.get("parent_rule") != "section.hierarchy"
    ):
        fail("invalid scenario schema/phase/component/parent")
    if policy.get("schema_version") != 2:
        fail("invalid validation policy schema")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    parent = scenario["parent_rule"]
    derived = [
        rule["id"]
        for rule in contract["rules"]
        if rule.get("authority") == "normative" and rule.get("parent_rule") == parent
    ]
    aliases = contract.get("compatibility_aliases", {}).get(parent)
    if derived != RULE_ORDER or aliases != RULE_ORDER or scenario.get("rules") != RULE_ORDER:
        fail(f"section hierarchy scope drift: derived={derived} aliases={aliases} scenario={scenario.get('rules')}")

    levels = scenario.get("levels")
    if not isinstance(levels, list) or len(levels) != 5:
        fail("scenario must contain exactly five hierarchy levels")
    if [item.get("level") for item in levels if isinstance(item, dict)] != LEVEL_ORDER:
        fail("hierarchy level order drift")
    if not all(
        isinstance(item, dict)
        and set(item) == {"level", "marker", "number"}
        and isinstance(item["marker"], str)
        and item["marker"]
        and isinstance(item["number"], str)
        and NUMBER_RE.fullmatch(item["number"])
        for item in levels
    ):
        fail("invalid hierarchy level specification")

    second_primary = scenario.get("second_primary")
    body_marker = scenario.get("first_primary_body_marker")
    if not (
        isinstance(second_primary, dict)
        and set(second_primary) == {"marker", "number"}
        and isinstance(second_primary["marker"], str)
        and second_primary["marker"]
        and isinstance(second_primary["number"], str)
        and NUMBER_RE.fullmatch(second_primary["number"])
        and isinstance(body_marker, str)
        and body_marker
    ):
        fail("invalid primary-section control markers")

    try:
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid vertical tolerance: {exc}")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    measured_levels: list[dict[str, Any]] = []
    level_pages: list[int] = []
    observed_numbers: list[str | None] = []
    for item in levels:
        page, word = unique_word(pages, item["marker"])
        number = number_left_of_marker(page, word, vertical_tolerance)
        level_pages.append(page.index)
        observed_numbers.append(number)
        measured_levels.append(
            {
                "level": item["level"],
                "marker": item["marker"],
                "page": page.index,
                "expected_number": item["number"],
                "observed_number": number,
            }
        )

    body_page, _ = unique_word(pages, body_marker)
    second_page, second_word = unique_word(pages, second_primary["marker"])
    second_number = number_left_of_marker(second_page, second_word, vertical_tolerance)

    first_group_pages = set(level_pages + [body_page.index])
    if len(first_group_pages) != 1:
        fail(f"controlled first hierarchy must fit on one page; observed={sorted(first_group_pages)}")
    first_group_page = next(iter(first_group_pages))
    if second_page.index <= first_group_page:
        fail(
            "controlled second primary section must follow the first hierarchy: "
            f"first={first_group_page} second={second_page.index}"
        )

    evidence: list[dict[str, Any]] = []

    progressive_rule = rules["section.numbering.progressive"]
    progressive_expected = progressive_rule["values"]
    expected_numbers = [item["number"] for item in levels] + [second_primary["number"]]
    actual_numbers = observed_numbers + [second_number]
    progressive_pass = progressive_expected.get("progressive") is True and actual_numbers == expected_numbers
    evidence.append(
        record(
            "section.numbering.progressive",
            "PASS" if progressive_pass else "FAIL",
            progressive_expected,
            {
                "expected_sequence": expected_numbers,
                "observed_sequence": actual_numbers,
                "levels": measured_levels,
                "second_primary": {
                    "marker": second_primary["marker"],
                    "page": second_page.index,
                    "expected_number": second_primary["number"],
                    "observed_number": second_number,
                },
            },
        )
    )

    levels_rule = rules["section.levels.max"]
    levels_expected = levels_rule["values"]
    observed_depths = [len(number.split(".")) for number in observed_numbers if number is not None]
    observed_max_depth = max(observed_depths, default=0)
    levels_pass = (
        levels_expected.get("max_levels") == 5
        and len(measured_levels) == 5
        and observed_max_depth == 5
        and observed_numbers[-1] == levels[-1]["number"]
    )
    evidence.append(
        record(
            "section.levels.max",
            "PASS" if levels_pass else "FAIL",
            levels_expected,
            {
                "controlled_levels": len(measured_levels),
                "observed_max_depth": observed_max_depth,
                "deepest_expected_number": levels[-1]["number"],
                "deepest_observed_number": observed_numbers[-1],
                "positive_evidence_only": True,
            },
        )
    )

    page_rule = rules["section.primary.new-page"]
    page_expected = page_rule["values"]
    page_delta = second_page.index - first_group_page
    page_pass = page_expected.get("primary_starts_new_page") is True and second_page.index > first_group_page
    evidence.append(
        record(
            "section.primary.new-page",
            "PASS" if page_pass else "FAIL",
            page_expected,
            {
                "first_primary_control_page": first_group_page,
                "first_primary_body_page": body_page.index,
                "second_primary_page": second_page.index,
                "page_delta": page_delta,
                "page_delta_is_observational": True,
            },
        )
    )

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "component": "section-hierarchy",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "VALIDATION-EVIDENCE section-hierarchy-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" levels={len(measured_levels)} first_primary_page={first_group_page}"
        + f" second_primary_page={second_page.index}"
    )
    for item in evidence:
        print(
            f"VALIDATION-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
