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
from pdf_measurement import (
    PDFMeasurementError,
    bbox_pages,
    normalize,
    typography_runs,
)

SCENARIO = ROOT / "normativa" / "footnote-text-scenario.json"
TYPOGRAPHY_LOCATORS = ROOT / "normativa" / "locator-audit-typography-paragraphs.json"
FOOTNOTE_LOCATORS = ROOT / "normativa" / "locator-audit-sections-footnotes-nature.json"
ORACLE_POLICY = ROOT / "normativa" / "oracle-policy.json"

FONT_RULE_ID = "font.size.reduced.footnote"
SPACING_RULE_ID = "footnote.line-spacing"
HANGING_RULE_ID = "footnote.hanging-alignment"
EXPECTED_RULE_IDS = [FONT_RULE_ID, SPACING_RULE_ID, HANGING_RULE_ID]


def fail(message: str) -> None:
    raise SystemExit(f"N7 footnote text oracle failed: {message}")


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


def unique_typography_containing(runs: list[Any], marker: str) -> Any:
    wanted = normalize(marker)
    matches = [run for run in runs if wanted in normalize(run.text)]
    if len(matches) != 1:
        fail(
            f"typography marker {marker!r}: expected one run, "
            f"found {[(run.page, run.text) for run in matches]}"
        )
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure N7 footnote font size, line spacing and hanging alignment from a final PDF."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    typography_locators = ruleset_map(load_json(TYPOGRAPHY_LOCATORS))
    footnote_locators = ruleset_map(load_json(FOOTNOTE_LOCATORS))
    policy = load_json(ORACLE_POLICY)

    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N7"
        or scenario.get("component") != "footnote-text"
    ):
        fail("invalid scenario schema/phase/component")
    if scenario.get("rules") != EXPECTED_RULE_IDS:
        fail(f"footnote text scenario scope drift: {scenario.get('rules')}")
    if policy.get("schema_version") != 1 or policy.get("phase") != "N5":
        fail("invalid oracle policy schema/phase")

    expected_locator_map = {
        FONT_RULE_ID: (typography_locators, "typography.reduced-font"),
        SPACING_RULE_ID: (footnote_locators, "footnotes.line-spacing"),
        HANGING_RULE_ID: (footnote_locators, "footnotes.hanging-alignment"),
    }
    declared_locator_map = scenario.get("locator_rulesets")
    if not isinstance(declared_locator_map, dict):
        fail("scenario locator_rulesets is required")
    for rule_id, (locator_map, ruleset_id) in expected_locator_map.items():
        if declared_locator_map.get(rule_id) != ruleset_id:
            fail(f"locator mapping drift for {rule_id}")
        ruleset = locator_map.get(ruleset_id)
        if not isinstance(ruleset, dict) or rule_id not in ruleset.get("rule_ids", []):
            fail(f"locator ruleset {ruleset_id} no longer contains {rule_id}")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    selected: dict[str, dict[str, Any]] = {}
    for rule_id in EXPECTED_RULE_IDS:
        rule = rules.get(rule_id)
        if not isinstance(rule, dict) or rule.get("authority") != "normative":
            fail(f"missing normative rule {rule_id}")
        selected[rule_id] = rule

    font_expected = selected[FONT_RULE_ID].get("values")
    spacing_expected = selected[SPACING_RULE_ID].get("values")
    hanging_expected = selected[HANGING_RULE_ID].get("values")
    if font_expected != {"pt": 10}:
        fail(f"unexpected contract values for {FONT_RULE_ID}: {font_expected}")
    if spacing_expected != {"factor": 1.0}:
        fail(f"unexpected contract values for {SPACING_RULE_ID}: {spacing_expected}")
    if hanging_expected != {"enabled": True}:
        fail(f"unexpected contract values for {HANGING_RULE_ID}: {hanging_expected}")

    try:
        font_tolerance = float(policy["tolerances"]["font_size_pt"])
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
        horizontal_tolerance = float(policy["tolerances"]["horizontal_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid oracle tolerance configuration: {exc}")
    if min(font_tolerance, vertical_tolerance, horizontal_tolerance) <= 0:
        fail("oracle tolerances must be positive")

    markers = scenario.get("markers")
    required_markers = {
        "calibration_top",
        "calibration_bottom",
        "footnote_first",
        "footnote_second",
        "footnote_third",
    }
    if not isinstance(markers, dict) or set(markers) != required_markers:
        fail("invalid marker specification")
    if not all(isinstance(value, str) and value for value in markers.values()):
        fail("all markers must be non-empty strings")

    excluded = scenario.get("excluded_residual")
    if (
        not isinstance(excluded, dict)
        or excluded.get("rule") != "footnote.separator.length"
        or not excluded.get("reason")
    ):
        fail("footnote separator must remain an explicit residual in this scenario")

    try:
        pages = bbox_pages(args.pdf)
        typography = typography_runs(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    cal_top_page, cal_top = unique_word(pages, markers["calibration_top"])
    cal_bottom_page, cal_bottom = unique_word(pages, markers["calibration_bottom"])
    foot_first_page, foot_first = unique_word(pages, markers["footnote_first"])
    foot_second_page, foot_second = unique_word(pages, markers["footnote_second"])
    foot_third_page, foot_third = unique_word(pages, markers["footnote_third"])

    controlled_pages = {
        cal_top_page.index,
        cal_bottom_page.index,
        foot_first_page.index,
        foot_second_page.index,
        foot_third_page.index,
    }
    if len(controlled_pages) != 1:
        fail(f"controlled markers must share one page: {sorted(controlled_pages)}")

    foot_types = [
        unique_typography_containing(typography, markers["footnote_first"]),
        unique_typography_containing(typography, markers["footnote_second"]),
        unique_typography_containing(typography, markers["footnote_third"]),
    ]
    font_samples = []
    font_passed = True
    expected_font_pt = float(font_expected["pt"])
    for marker, run in zip(
        (markers["footnote_first"], markers["footnote_second"], markers["footnote_third"]),
        foot_types,
    ):
        delta = abs(run.font_size - expected_font_pt)
        font_samples.append(
            {
                "marker": marker,
                "page": run.page,
                "font_pt": round(run.font_size, 4),
                "delta_pt": round(delta, 4),
                "family": run.family,
            }
        )
        font_passed = font_passed and delta <= font_tolerance

    cal_gap = cal_bottom.box.center_y - cal_top.box.center_y
    foot_gap_one = foot_second.box.center_y - foot_first.box.center_y
    foot_gap_two = foot_third.box.center_y - foot_second.box.center_y
    if min(cal_gap, foot_gap_one, foot_gap_two) <= 0:
        fail(
            "line markers are not top-to-bottom: "
            f"cal={cal_gap}, foot1={foot_gap_one}, foot2={foot_gap_two}"
        )
    spacing_deltas = [abs(foot_gap_one - cal_gap), abs(foot_gap_two - cal_gap)]
    spacing_passed = all(delta <= vertical_tolerance for delta in spacing_deltas)

    first_x = foot_first.box.x_min
    hanging_samples = [
        {
            "marker": markers["footnote_second"],
            "x_min_pt": round(foot_second.box.x_min, 4),
            "delta_pt": round(abs(foot_second.box.x_min - first_x), 4),
        },
        {
            "marker": markers["footnote_third"],
            "x_min_pt": round(foot_third.box.x_min, 4),
            "delta_pt": round(abs(foot_third.box.x_min - first_x), 4),
        },
    ]
    hanging_passed = all(
        item["delta_pt"] <= horizontal_tolerance for item in hanging_samples
    )

    evidence = [
        {
            "rule_id": FONT_RULE_ID,
            "status": "PASS" if font_passed else "FAIL",
            "expected": font_expected,
            "measured": {"samples": font_samples},
            "tool": "pdftohtml -xml -zoom 1.0",
            "tolerance": font_tolerance,
        },
        {
            "rule_id": SPACING_RULE_ID,
            "status": "PASS" if spacing_passed else "FAIL",
            "expected": spacing_expected,
            "measured": {
                "page": foot_first_page.index,
                "calibration_center_gap_pt": round(cal_gap, 4),
                "footnote_center_gaps_pt": [round(foot_gap_one, 4), round(foot_gap_two, 4)],
                "gap_deltas_pt": [round(delta, 4) for delta in spacing_deltas],
                "same_document_10pt_single_spacing_calibration": True,
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": vertical_tolerance,
        },
        {
            "rule_id": HANGING_RULE_ID,
            "status": "PASS" if hanging_passed else "FAIL",
            "expected": hanging_expected,
            "measured": {
                "page": foot_first_page.index,
                "first_text_x_min_pt": round(first_x, 4),
                "continuation_lines": hanging_samples,
                "alignment_reference": "first text character on the first footnote line",
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": horizontal_tolerance,
        },
    ]

    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    status_counts = dict(Counter(item["status"] for item in evidence))
    payload = {
        "schema_version": 1,
        "phase": "N7",
        "component": "footnote-text",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "excluded_residual": excluded,
        "evidence": evidence,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "N7-EVIDENCE footnote-text-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" calibration_gap_pt={cal_gap:.4f}"
        + f" footnote_gaps_pt={foot_gap_one:.4f},{foot_gap_two:.4f}"
    )
    for item in evidence:
        print(
            f"N7-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
    print(
        "N7-RESIDUAL rule=footnote.separator.length status=UNASSESSED "
        "reason=requires-final-pdf-vector-measurement"
    )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
