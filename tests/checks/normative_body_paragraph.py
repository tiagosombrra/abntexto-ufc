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

SCENARIO = ROOT / "standards" / "body-paragraph-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-typography-paragraphs.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULESET_ID = "layout.body-paragraph"
INDENT_RULE_ID = "paragraph.first-line.indent"
SPACING_RULE_ID = "paragraph.spacing.extra"
MM_TO_PT = 72.0 / 25.4


def fail(message: str) -> None:
    raise SystemExit(f"Body paragraph validation failed: {message}")


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
        fail(
            f"marker {marker!r}: expected one word, "
            f"found {[(page.index, word.text) for page, word in matches]}"
        )
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure N6 body paragraph indentation and extra spacing from a final PDF."
    )
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
        or scenario.get("phase") != "N6"
        or scenario.get("component") != "body-paragraph"
        or scenario.get("locator_ruleset") != RULESET_ID
    ):
        fail("invalid scenario schema/phase/component/ruleset")
    if policy.get("schema_version") != 2:
        fail("invalid validation policy schema")

    locator_matches = [
        item
        for item in locator.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == RULESET_ID
    ]
    if len(locator_matches) != 1:
        fail(f"locator ruleset drift: found {len(locator_matches)} matches")
    locator_rules = locator_matches[0].get("rule_ids")
    expected_rule_ids = [INDENT_RULE_ID, SPACING_RULE_ID]
    if locator_rules != expected_rule_ids or scenario.get("rules") != expected_rule_ids:
        fail(
            f"body paragraph scope drift: locator={locator_rules} "
            f"scenario={scenario.get('rules')}"
        )

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    indent_rule = rules.get(INDENT_RULE_ID)
    spacing_rule = rules.get(SPACING_RULE_ID)
    if not isinstance(indent_rule, dict) or indent_rule.get("authority") != "normative":
        fail(f"missing normative rule {INDENT_RULE_ID}")
    if not isinstance(spacing_rule, dict) or spacing_rule.get("authority") != "normative":
        fail(f"missing normative rule {SPACING_RULE_ID}")

    indent_expected = indent_rule.get("values")
    spacing_expected = spacing_rule.get("values")
    if (
        not isinstance(indent_expected, dict)
        or set(indent_expected) != {"first_line_indent_mm"}
    ):
        fail(f"unexpected contract values for {INDENT_RULE_ID}: {indent_expected}")
    if (
        not isinstance(spacing_expected, dict)
        or set(spacing_expected) != {"paragraph_extra_spacing_pt"}
    ):
        fail(f"unexpected contract values for {SPACING_RULE_ID}: {spacing_expected}")

    try:
        indent_mm = float(indent_expected["first_line_indent_mm"])
        extra_spacing_pt = float(spacing_expected["paragraph_extra_spacing_pt"])
        horizontal_tolerance = float(policy["tolerances"]["horizontal_position_pt"])
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid contract/tolerance configuration: {exc}")

    if indent_mm != 20.0 or extra_spacing_pt != 0.0:
        fail(
            f"contract drift: indent_mm={indent_mm} "
            f"paragraph_extra_spacing_pt={extra_spacing_pt}"
        )
    if horizontal_tolerance <= 0 or vertical_tolerance <= 0:
        fail("position tolerances must be positive")

    markers = scenario.get("markers")
    required_markers = {
        "indent_first",
        "indent_second",
        "margin_control",
        "calibration_top",
        "calibration_bottom",
    }
    if not isinstance(markers, dict) or set(markers) != required_markers:
        fail("invalid marker specification")
    if not all(isinstance(value, str) and value for value in markers.values()):
        fail("all markers must be non-empty strings")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    first_page, first_word = unique_word(pages, markers["indent_first"])
    second_page, second_word = unique_word(pages, markers["indent_second"])
    margin_page, margin_word = unique_word(pages, markers["margin_control"])
    cal_top_page, cal_top_word = unique_word(pages, markers["calibration_top"])
    cal_bottom_page, cal_bottom_word = unique_word(pages, markers["calibration_bottom"])

    observed_pages = {
        first_page.index,
        second_page.index,
        margin_page.index,
        cal_top_page.index,
        cal_bottom_page.index,
    }
    if len(observed_pages) != 1:
        fail(f"controlled markers must share one page: {sorted(observed_pages)}")

    expected_indent_pt = indent_mm * MM_TO_PT
    first_indent_pt = first_word.box.x_min - margin_word.box.x_min
    second_indent_pt = second_word.box.x_min - margin_word.box.x_min
    first_indent_delta = abs(first_indent_pt - expected_indent_pt)
    second_indent_delta = abs(second_indent_pt - expected_indent_pt)
    indent_passed = (
        first_indent_delta <= horizontal_tolerance
        and second_indent_delta <= horizontal_tolerance
    )

    first_y = first_word.box.center_y
    second_y = second_word.box.center_y
    cal_top_y = cal_top_word.box.center_y
    cal_bottom_y = cal_bottom_word.box.center_y
    if second_y <= first_y:
        fail(
            f"measured paragraphs are not top-to-bottom: first={first_y} second={second_y}"
        )
    if cal_bottom_y <= cal_top_y:
        fail(
            f"calibration lines are not top-to-bottom: top={cal_top_y} bottom={cal_bottom_y}"
        )

    paragraph_gap = second_y - first_y
    calibration_gap = cal_bottom_y - cal_top_y
    measured_extra_spacing = paragraph_gap - calibration_gap
    spacing_delta = abs(measured_extra_spacing - extra_spacing_pt)
    spacing_passed = spacing_delta <= vertical_tolerance

    evidence = [
        {
            "rule_id": INDENT_RULE_ID,
            "status": "PASS" if indent_passed else "FAIL",
            "expected": indent_expected,
            "measured": {
                "page": first_page.index,
                "expected_indent_pt": round(expected_indent_pt, 4),
                "margin_control_x_min_pt": round(margin_word.box.x_min, 4),
                "paragraphs": [
                    {
                        "marker": markers["indent_first"],
                        "x_min_pt": round(first_word.box.x_min, 4),
                        "indent_pt": round(first_indent_pt, 4),
                        "delta_pt": round(first_indent_delta, 4),
                    },
                    {
                        "marker": markers["indent_second"],
                        "x_min_pt": round(second_word.box.x_min, 4),
                        "indent_pt": round(second_indent_pt, 4),
                        "delta_pt": round(second_indent_delta, 4),
                    },
                ],
                "same_font_margin_control": True,
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": horizontal_tolerance,
        },
        {
            "rule_id": SPACING_RULE_ID,
            "status": "PASS" if spacing_passed else "FAIL",
            "expected": spacing_expected,
            "measured": {
                "page": first_page.index,
                "paragraph_center_gap_pt": round(paragraph_gap, 4),
                "calibration_center_gap_pt": round(calibration_gap, 4),
                "measured_extra_spacing_pt": round(measured_extra_spacing, 4),
                "delta_pt": round(spacing_delta, 4),
                "same_document_body_line_calibration": True,
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": vertical_tolerance,
        },
    ]

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if indent_passed and spacing_passed else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "component": "body-paragraph",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "evidence": evidence,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "N6-EVIDENCE body-paragraph-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" indent_one_pt={first_indent_pt:.4f}"
        + f" indent_two_pt={second_indent_pt:.4f}"
        + f" paragraph_gap_pt={paragraph_gap:.4f}"
        + f" calibration_gap_pt={calibration_gap:.4f}"
    )
    for item in evidence:
        print(
            f"N6-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
