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

SCENARIO = ROOT / "standards" / "section-primary-after-spacing-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-sections-footnotes-nature.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULE_ID = "section.primary.after-spacing"
RULESET_ID = "sections.primary-after-spacing"


def fail(message: str) -> None:
    raise SystemExit(f"Primary section after-spacing validation failed: {message}")


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


def record(status: str, expected: Any, measured: Any, tolerance: float) -> dict[str, Any]:
    return {
        "rule_id": RULE_ID,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftotext -bbox-layout",
        "tolerance": tolerance,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure primary-section after-spacing evidence from a final PDF."
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

        or scenario.get("component") != "section-primary-after-spacing"
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
            f"primary after-spacing scope drift: locator={locator_rules} "
            f"scenario={scenario.get('rules')}"
        )

    expected = rule.get("values")
    if not isinstance(expected, dict) or set(expected) != {"after_factor"}:
        fail(f"unexpected contract values for {RULE_ID}: {expected}")
    try:
        expected_factor = float(expected["after_factor"])
        calibration_factor = float(scenario["calibration"]["factor"])
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid factor/tolerance configuration: {exc}")
    if expected_factor != 1.5 or calibration_factor != expected_factor:
        fail(
            f"factor drift: contract={expected_factor} calibration={calibration_factor}"
        )
    if vertical_tolerance <= 0:
        fail("vertical tolerance must be positive")

    markers = scenario.get("markers")
    required_markers = {
        "heading",
        "body",
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

    heading_page, heading_word = unique_word(pages, markers["heading"])
    body_page, body_word = unique_word(pages, markers["body"])
    cal_top_page, cal_top_word = unique_word(pages, markers["calibration_top"])
    cal_bottom_page, cal_bottom_word = unique_word(pages, markers["calibration_bottom"])

    if heading_page.index != body_page.index:
        fail(
            "controlled heading/body must share one page: "
            f"heading={heading_page.index} body={body_page.index}"
        )
    if cal_top_page.index != cal_bottom_page.index:
        fail(
            "calibration markers must share one page: "
            f"top={cal_top_page.index} bottom={cal_bottom_page.index}"
        )

    heading_y = heading_word.box.center_y
    body_y = body_word.box.center_y
    cal_top_y = cal_top_word.box.center_y
    cal_bottom_y = cal_bottom_word.box.center_y
    if body_y <= heading_y:
        fail(f"body marker is not below heading: heading={heading_y} body={body_y}")
    if cal_bottom_y <= cal_top_y:
        fail(
            "calibration markers are not top-to-bottom: "
            f"top={cal_top_y} bottom={cal_bottom_y}"
        )

    measured_gap = body_y - heading_y
    calibration_gap = cal_bottom_y - cal_top_y
    delta = abs(measured_gap - calibration_gap)
    passed = delta <= vertical_tolerance

    evidence = [
        record(
            "PASS" if passed else "FAIL",
            expected,
            {
                "heading_page": heading_page.index,
                "body_page": body_page.index,
                "heading_to_body_center_gap_pt": round(measured_gap, 4),
                "calibration_page": cal_top_page.index,
                "calibration_factor": calibration_factor,
                "calibration_center_gap_pt": round(calibration_gap, 4),
                "delta_pt": round(delta, 4),
                "same_document_calibration": True,
            },
            vertical_tolerance,
        )
    ]

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if passed else "FAIL"
    payload = {
        "schema_version": 1,
        "component": "section-primary-after-spacing",
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
        "VALIDATION-EVIDENCE section-primary-after-spacing-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" gap_pt={measured_gap:.4f} calibration_pt={calibration_gap:.4f}"
    )
    item = evidence[0]
    print(
        f"VALIDATION-EVIDENCE rule={RULE_ID} status={item['status']} "
        f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
    )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
