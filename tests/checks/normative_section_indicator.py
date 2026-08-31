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

SCENARIO = ROOT / "standards" / "section-indicator-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-sections-footnotes-nature.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULE_ORDER = [
    "section.indicator.alignment",
    "section.indicator.separator",
]
LEVEL_ORDER = ["section", "subsection", "subsubsection", "paragraph", "subparagraph"]
NUMBER_RE = re.compile(r"[0-9]+(?:\.[0-9]+)*")


def fail(message: str) -> None:
    raise SystemExit(f"Section indicator validation failed: {message}")


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


def number_left_of_marker(page: Any, marker_word: Any, expected: str, vertical_tolerance: float) -> Any:
    candidates = [
        word
        for word in page.words
        if NUMBER_RE.fullmatch(word.text.strip())
        and word.text.strip() == expected
        and word.box.x_max <= marker_word.box.x_min
        and abs(word.box.center_y - marker_word.box.center_y) <= vertical_tolerance
    ]
    if len(candidates) != 1:
        fail(
            f"heading {expected} left of {marker_word.text!r}: expected one indicator, "
            f"found {[word.text for word in candidates]}"
        )
    return candidates[0]


def record(rule_id: str, status: str, expected: Any, measured: Any) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftotext -bbox-layout",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure section-indicator evidence from a final PDF.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locator = load_json(LOCATOR_AUDIT)
    policy = load_json(VALIDATION_POLICY)
    if (
        scenario.get("schema_version") != 1

        or scenario.get("component") != "section-indicator"
        or scenario.get("locator_ruleset") != "sections.indicator"
    ):
        fail("invalid scenario schema/component/ruleset")
    if policy.get("schema_version") != 2:
        fail("invalid validation policy schema")

    locator_matches = [
        item
        for item in locator.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == scenario["locator_ruleset"]
    ]
    if len(locator_matches) != 1:
        fail(f"locator ruleset drift: found {len(locator_matches)} matches")
    locator_rules = locator_matches[0].get("rule_ids")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    contract_scope = [rule_id for rule_id in RULE_ORDER if rule_id in rules and rules[rule_id].get("authority") == "normative"]
    if locator_rules != RULE_ORDER or scenario.get("rules") != RULE_ORDER or contract_scope != RULE_ORDER:
        fail(
            f"section indicator scope drift: locator={locator_rules} "
            f"scenario={scenario.get('rules')} contract={contract_scope}"
        )

    levels = scenario.get("levels")
    if not isinstance(levels, list) or len(levels) != 5:
        fail("scenario must contain exactly five controlled hierarchy levels")
    if [item.get("level") for item in levels if isinstance(item, dict)] != LEVEL_ORDER:
        fail("hierarchy level order drift")
    required_keys = {"level", "title_marker", "number", "calibration_left", "calibration_right"}
    if not all(
        isinstance(item, dict)
        and set(item) == required_keys
        and isinstance(item["title_marker"], str)
        and item["title_marker"]
        and isinstance(item["number"], str)
        and NUMBER_RE.fullmatch(item["number"])
        and isinstance(item["calibration_left"], str)
        and item["calibration_left"]
        and isinstance(item["calibration_right"], str)
        and item["calibration_right"]
        for item in levels
    ):
        fail("invalid controlled level specification")

    try:
        horizontal_tolerance = float(policy["tolerances"]["horizontal_position_pt"])
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid validation tolerances: {exc}")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    measurements: list[dict[str, Any]] = []
    for item in levels:
        title_page, title_word = unique_word(pages, item["title_marker"])
        indicator_word = number_left_of_marker(title_page, title_word, item["number"], vertical_tolerance)
        cal_left_page, cal_left_word = unique_word(pages, item["calibration_left"])
        cal_right_page, cal_right_word = unique_word(pages, item["calibration_right"])
        if cal_left_page.index != cal_right_page.index:
            fail(f"{item['level']}: calibration words split across pages")
        if abs(cal_left_word.box.center_y - cal_right_word.box.center_y) > vertical_tolerance:
            fail(f"{item['level']}: calibration words are not on the same line")
        if cal_right_word.box.x_min <= cal_left_word.box.x_max:
            fail(f"{item['level']}: invalid calibration word order")

        heading_gap = title_word.box.x_min - indicator_word.box.x_max
        calibration_gap = cal_right_word.box.x_min - cal_left_word.box.x_max
        measurements.append(
            {
                "level": item["level"],
                "page": title_page.index,
                "indicator": indicator_word.text.strip(),
                "indicator_x_min_pt": round(indicator_word.box.x_min, 4),
                "title_marker": item["title_marker"],
                "title_x_min_pt": round(title_word.box.x_min, 4),
                "calibration_left_x_min_pt": round(cal_left_word.box.x_min, 4),
                "alignment_delta_pt": round(abs(indicator_word.box.x_min - cal_left_word.box.x_min), 4),
                "heading_gap_pt": round(heading_gap, 4),
                "single_space_calibration_gap_pt": round(calibration_gap, 4),
                "separator_delta_pt": round(abs(heading_gap - calibration_gap), 4),
            }
        )

    alignment_rule = rules["section.indicator.alignment"]
    alignment_expected = alignment_rule["values"]
    alignment_pass = (
        alignment_expected.get("alignment") == "left"
        and all(item["alignment_delta_pt"] <= horizontal_tolerance for item in measurements)
    )

    separator_rule = rules["section.indicator.separator"]
    separator_expected = separator_rule["values"]
    separator_pass = (
        separator_expected.get("separator") == "single-character-space"
        and all(item["separator_delta_pt"] <= horizontal_tolerance for item in measurements)
    )

    evidence = [
        record(
            "section.indicator.alignment",
            "PASS" if alignment_pass else "FAIL",
            alignment_expected,
            {
                "horizontal_tolerance_pt": horizontal_tolerance,
                "levels": [
                    {
                        "level": item["level"],
                        "indicator_x_min_pt": item["indicator_x_min_pt"],
                        "calibration_left_x_min_pt": item["calibration_left_x_min_pt"],
                        "delta_pt": item["alignment_delta_pt"],
                    }
                    for item in measurements
                ],
            },
        ),
        record(
            "section.indicator.separator",
            "PASS" if separator_pass else "FAIL",
            separator_expected,
            {
                "horizontal_tolerance_pt": horizontal_tolerance,
                "calibration": "same-document single literal space in the corresponding section-level font",
                "levels": [
                    {
                        "level": item["level"],
                        "heading_gap_pt": item["heading_gap_pt"],
                        "single_space_gap_pt": item["single_space_calibration_gap_pt"],
                        "delta_pt": item["separator_delta_pt"],
                    }
                    for item in measurements
                ],
            },
        ),
    ]

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "component": "section-indicator",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "measurements": measurements,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "VALIDATION-EVIDENCE section-indicator-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" levels={len(measurements)}"
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
