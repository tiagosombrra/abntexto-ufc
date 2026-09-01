#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize
from pdf_vector_measurement import vector_rules

SCENARIO = ROOT / "standards" / "footnote-separator-scenario.json"
FOOTNOTE_LOCATORS = ROOT / "standards" / "locator-audit-sections-footnotes-nature.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULE_ID = "footnote.separator.length"
EXPECTED_RULE_IDS = [RULE_ID]


def fail(message: str) -> None:
    raise SystemExit(f"footnote separator validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def ruleset_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in data.get("rulesets", []):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            fail("invalid locator ruleset entry")
        result[item["id"]] = item
    return result


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
        description="Measure the footnote separator directly from final-PDF vector content."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locators = ruleset_map(load_json(FOOTNOTE_LOCATORS))
    policy = load_json(VALIDATION_POLICY)

    if (
        scenario.get("schema_version") != 1
        or scenario.get("component") != "footnote-separator"
    ):
        fail("invalid scenario schema/component")
    if scenario.get("rules") != EXPECTED_RULE_IDS:
        fail(f"footnote separator scenario scope drift: {scenario.get('rules')}")
    if policy.get("schema_version") != 2:
        fail("invalid validation policy schema")

    declared_locator_map = scenario.get("locator_rulesets")
    if not isinstance(declared_locator_map, dict):
        fail("scenario locator_rulesets is required")
    if declared_locator_map.get(RULE_ID) != "footnotes.separator":
        fail(f"locator mapping drift for {RULE_ID}")
    locator_ruleset = locators.get("footnotes.separator")
    if not isinstance(locator_ruleset, dict) or RULE_ID not in locator_ruleset.get("rule_ids", []):
        fail(f"locator ruleset footnotes.separator no longer contains {RULE_ID}")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    rule = rules.get(RULE_ID)
    if not isinstance(rule, dict) or rule.get("authority") != "normative":
        fail(f"missing normative rule {RULE_ID}")
    expected = rule.get("values")
    if expected != {"length_mm": 50, "origin": "left-margin"}:
        fail(f"unexpected contract values for {RULE_ID}: {expected}")

    try:
        horizontal_tolerance = float(policy["tolerances"]["horizontal_position_pt"])
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid validation tolerance configuration: {exc}")
    if min(horizontal_tolerance, vertical_tolerance) <= 0:
        fail("validation tolerances must be positive")

    markers = scenario.get("markers")
    if not isinstance(markers, dict) or set(markers) != {"margin_control", "footnote_text"}:
        fail("invalid marker specification")
    if not all(isinstance(value, str) and value for value in markers.values()):
        fail("all markers must be non-empty strings")

    measurement = scenario.get("measurement")
    if not isinstance(measurement, dict):
        fail("measurement metadata is required")
    if measurement.get("vector_tool") != "pdftocairo -svg":
        fail("vector measurement tool drift")
    if measurement.get("text_tool") != "pdftotext -bbox-layout":
        fail("text measurement tool drift")
    if measurement.get("origin_reference") != "same-document left-margin text marker":
        fail("origin reference drift")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    margin_page, margin_word = unique_word(pages, markers["margin_control"])
    footnote_page, footnote_word = unique_word(pages, markers["footnote_text"])
    if margin_page.index != footnote_page.index:
        fail(
            "controlled markers must share one page: "
            f"margin={margin_page.index}, footnote={footnote_page.index}"
        )

    try:
        horizontal_rules = [
            item
            for item in vector_rules(args.pdf.resolve(), page=margin_page.index)
            if item.orientation == "horizontal"
        ]
    except PDFMeasurementError as exc:
        fail(str(exc))

    if len(horizontal_rules) != 1:
        fail(
            "expected one non-glyph horizontal vector rule, found "
            f"{[item.to_dict() for item in horizontal_rules]}"
        )
    line = horizontal_rules[0]

    expected_length_pt = float(expected["length_mm"]) * 72.0 / 25.4
    measured_length_pt = float(line.length)
    measured_start_x_pt = float(line.box.x_min)
    measured_y_pt = float(line.box.center_y)
    length_delta_pt = abs(measured_length_pt - expected_length_pt)
    origin_delta_pt = abs(measured_start_x_pt - margin_word.box.x_min)
    separator_above_footnote = measured_y_pt <= footnote_word.box.y_min + vertical_tolerance

    length_passed = length_delta_pt <= horizontal_tolerance
    origin_passed = origin_delta_pt <= horizontal_tolerance
    passed = length_passed and origin_passed and separator_above_footnote
    status = "PASS" if passed else "FAIL"

    measured = {
        "page": margin_page.index,
        "expected_length_pt": round(expected_length_pt, 4),
        "vector_length_pt": round(measured_length_pt, 4),
        "length_delta_pt": round(length_delta_pt, 4),
        "vector_start_x_pt": round(measured_start_x_pt, 4),
        "margin_control_x_min_pt": round(margin_word.box.x_min, 4),
        "origin_delta_pt": round(origin_delta_pt, 4),
        "vector_y_pt": round(measured_y_pt, 4),
        "footnote_text_y_min_pt": round(footnote_word.box.y_min, 4),
        "separator_above_footnote_text": separator_above_footnote,
        "vector_thickness_pt": round(float(line.thickness), 4),
        "vector_paint": line.paint,
    }
    evidence = {
        "rule_id": RULE_ID,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftocairo -svg; pdftotext -bbox-layout",
        "tolerance": {
            "length_pt": horizontal_tolerance,
            "origin_pt": horizontal_tolerance,
            "vertical_identity_pt": vertical_tolerance,
        },
    }
    payload = {
        "schema_version": 1,
        "component": "footnote-separator",
        "source_commit_sha": args.commit_sha,
        "result": status,
        "status_counts": {status: 1},
        "evidence": [evidence],
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"VALIDATION-EVIDENCE footnote-separator-summary {status}=1 "
        f"expected_length_pt={expected_length_pt:.4f} "
        f"measured_length_pt={measured_length_pt:.4f} "
        f"length_delta_pt={length_delta_pt:.4f} "
        f"origin_delta_pt={origin_delta_pt:.4f}"
    )
    print(
        f"VALIDATION-EVIDENCE rule={RULE_ID} status={status} "
        f"expected={json.dumps(expected, ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(measured, ensure_ascii=False, sort_keys=True)}"
    )

    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
