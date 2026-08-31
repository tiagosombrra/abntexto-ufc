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

SCENARIO = ROOT / "standards" / "subsection-spacing-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-sections-footnotes-nature.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULE_ID = "section.subsection.before-after-spacing"
RULESET_ID = "sections.subsection-spacing"


def fail(message: str) -> None:
    raise SystemExit(f"Subsection spacing validation failed: {message}")


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
        description="Measure N6 subsection before/after spacing from a final PDF."
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
        or scenario.get("component") != "subsection-spacing"
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

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    rule = rules.get(RULE_ID)
    if not isinstance(rule, dict) or rule.get("authority") != "normative":
        fail(f"missing normative rule {RULE_ID}")
    if locator_rules != [RULE_ID] or scenario.get("rules") != [RULE_ID]:
        fail(
            f"subsection spacing scope drift: locator={locator_rules} "
            f"scenario={scenario.get('rules')}"
        )

    expected = rule.get("values")
    if not isinstance(expected, dict) or set(expected) != {"before_factor", "after_factor"}:
        fail(f"unexpected contract values for {RULE_ID}: {expected}")
    calibration = scenario.get("calibration")
    if not isinstance(calibration, dict):
        fail("missing calibration specification")
    try:
        expected_before = float(expected["before_factor"])
        expected_after = float(expected["after_factor"])
        calibration_before = float(calibration["before_factor"])
        calibration_after = float(calibration["after_factor"])
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid factor/tolerance configuration: {exc}")
    if (
        expected_before != 1.5
        or expected_after != 1.5
        or calibration_before != expected_before
        or calibration_after != expected_after
    ):
        fail(
            "factor drift: "
            f"contract=({expected_before},{expected_after}) "
            f"calibration=({calibration_before},{calibration_after})"
        )
    if vertical_tolerance <= 0:
        fail("vertical tolerance must be positive")

    markers = scenario.get("markers")
    required_markers = {
        "before",
        "heading",
        "after",
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

    before_page, before_word = unique_word(pages, markers["before"])
    heading_page, heading_word = unique_word(pages, markers["heading"])
    after_page, after_word = unique_word(pages, markers["after"])
    cal_top_page, cal_top_word = unique_word(pages, markers["calibration_top"])
    cal_bottom_page, cal_bottom_word = unique_word(pages, markers["calibration_bottom"])

    controlled_pages = {before_page.index, heading_page.index, after_page.index}
    if len(controlled_pages) != 1:
        fail(f"controlled subsection markers must share one page: {sorted(controlled_pages)}")
    if cal_top_page.index != cal_bottom_page.index:
        fail(
            "calibration markers must share one page: "
            f"top={cal_top_page.index} bottom={cal_bottom_page.index}"
        )

    before_y = before_word.box.center_y
    heading_y = heading_word.box.center_y
    after_y = after_word.box.center_y
    cal_top_y = cal_top_word.box.center_y
    cal_bottom_y = cal_bottom_word.box.center_y
    if not before_y < heading_y < after_y:
        fail(
            "controlled markers are not in reading order: "
            f"before={before_y} heading={heading_y} after={after_y}"
        )
    if cal_bottom_y <= cal_top_y:
        fail(
            "calibration markers are not top-to-bottom: "
            f"top={cal_top_y} bottom={cal_bottom_y}"
        )

    before_gap = heading_y - before_y
    after_gap = after_y - heading_y
    calibration_gap = cal_bottom_y - cal_top_y
    before_delta = abs(before_gap - calibration_gap)
    after_delta = abs(after_gap - calibration_gap)
    passed = before_delta <= vertical_tolerance and after_delta <= vertical_tolerance

    evidence = [
        {
            "rule_id": RULE_ID,
            "status": "PASS" if passed else "FAIL",
            "expected": expected,
            "measured": {
                "page": heading_page.index,
                "before_center_gap_pt": round(before_gap, 4),
                "after_center_gap_pt": round(after_gap, 4),
                "calibration_page": cal_top_page.index,
                "calibration_center_gap_pt": round(calibration_gap, 4),
                "before_delta_pt": round(before_delta, 4),
                "after_delta_pt": round(after_delta, 4),
                "same_document_calibration": True,
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": vertical_tolerance,
        }
    ]

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if passed else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "component": "subsection-spacing",
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
        "N6-EVIDENCE subsection-spacing-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" before_pt={before_gap:.4f} after_pt={after_gap:.4f} "
        + f"calibration_pt={calibration_gap:.4f}"
    )
    item = evidence[0]
    print(
        f"N6-EVIDENCE rule={RULE_ID} status={item['status']} "
        f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
    )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
