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
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize, typography_runs

SCENARIO = ROOT / "standards" / "long-quotation-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-citations.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULESET_ID = "citations.direct-long"
RULE_IDS = [
    "quotation.long.block",
    "quotation.long.indent.left",
    "quotation.long.font.size",
    "quotation.long.line-spacing",
    "quotation.long.quotation-marks",
]
MM_TO_PT = 72.0 / 25.4
FORBIDDEN_QUOTES = set("\"'“”‘’«»„‟‹›")


def fail(message: str) -> None:
    raise SystemExit(f"Long quotation validation failed: {message}")


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


def cluster_lines(words: list[Any], tolerance: float = 1.0) -> list[list[Any]]:
    ordered = sorted(words, key=lambda word: (word.box.center_y, word.box.x_min))
    lines: list[list[Any]] = []
    for word in ordered:
        if not lines:
            lines.append([word])
            continue
        center = sum(item.box.center_y for item in lines[-1]) / len(lines[-1])
        if abs(word.box.center_y - center) <= tolerance:
            lines[-1].append(word)
        else:
            lines.append([word])
    for line in lines:
        line.sort(key=lambda word: word.box.x_min)
    return lines


def typography_containing(runs: list[Any], marker: str) -> Any:
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
        description="Measure long direct quotation layout from a final PDF."
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

        or scenario.get("component") != "long-quotation"
        or scenario.get("locator_ruleset") != RULESET_ID
    ):
        fail("invalid scenario schema/component/ruleset")
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
    if locator_rules != RULE_IDS or scenario.get("rules") != RULE_IDS:
        fail(
            f"long quotation scope drift: locator={locator_rules} "
            f"scenario={scenario.get('rules')}"
        )

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    selected: dict[str, dict[str, Any]] = {}
    expected_keys = {
        "quotation.long.block": {"block"},
        "quotation.long.indent.left": {"left_indent_mm"},
        "quotation.long.font.size": {"font_pt"},
        "quotation.long.line-spacing": {"line_spacing"},
        "quotation.long.quotation-marks": {"quotation_marks"},
    }
    for rule_id in RULE_IDS:
        rule = rules.get(rule_id)
        if not isinstance(rule, dict) or rule.get("authority") != "normative":
            fail(f"missing normative rule {rule_id}")
        values = rule.get("values")
        if not isinstance(values, dict) or set(values) != expected_keys[rule_id]:
            fail(f"unexpected contract values for {rule_id}: {values}")
        applicability = rule.get("applicability")
        if not isinstance(applicability, dict) or set(applicability) != {"min_lines"}:
            fail(f"unexpected applicability for {rule_id}: {applicability}")
        selected[rule_id] = rule

    try:
        min_lines = int(selected[RULE_IDS[0]]["applicability"]["min_lines"])
        left_indent_mm = float(
            selected["quotation.long.indent.left"]["values"]["left_indent_mm"]
        )
        font_pt = float(selected["quotation.long.font.size"]["values"]["font_pt"])
        line_spacing = float(
            selected["quotation.long.line-spacing"]["values"]["line_spacing"]
        )
        quotation_marks = selected["quotation.long.quotation-marks"]["values"][
            "quotation_marks"
        ]
        block_expected = selected["quotation.long.block"]["values"]["block"]
        horizontal_tolerance = float(policy["tolerances"]["horizontal_position_pt"])
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
        font_tolerance = float(policy["tolerances"]["font_size_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid contract/tolerance configuration: {exc}")

    for rule_id in RULE_IDS:
        if selected[rule_id]["applicability"].get("min_lines") != min_lines:
            fail(f"min_lines applicability drift across {RULESET_ID}")
    if (
        min_lines != 4
        or left_indent_mm != 40.0
        or font_pt != 10.0
        or line_spacing != 1.0
        or quotation_marks is not False
        or block_expected is not True
    ):
        fail(
            "contract drift: "
            f"min_lines={min_lines} left_indent_mm={left_indent_mm} "
            f"font_pt={font_pt} line_spacing={line_spacing} "
            f"quotation_marks={quotation_marks} block={block_expected}"
        )

    markers = scenario.get("markers")
    required_markers = {
        "margin_control",
        "before",
        "quote_start",
        "quote_middle",
        "quote_end",
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
        runs = typography_runs(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    located = {key: unique_word(pages, value) for key, value in markers.items()}
    quote_page = located["quote_start"][0]
    page_indices = {
        located[key][0].index
        for key in (
            "margin_control",
            "before",
            "quote_start",
            "quote_middle",
            "quote_end",
            "after",
        )
    }
    if len(page_indices) != 1:
        fail(f"controlled quotation markers must share one page: {sorted(page_indices)}")

    start_word = located["quote_start"][1]
    middle_word = located["quote_middle"][1]
    end_word = located["quote_end"][1]
    before_word = located["before"][1]
    after_word = located["after"][1]
    margin_word = located["margin_control"][1]

    first_y = start_word.box.center_y
    last_y = end_word.box.center_y
    if last_y <= first_y:
        fail(f"quote end must follow quote start: start={first_y} end={last_y}")
    if not (
        before_word.box.center_y
        < first_y
        < middle_word.box.center_y
        < last_y
        < after_word.box.center_y
    ):
        fail("quotation markers are not vertically ordered as a distinct block")

    quote_words = [
        word
        for word in quote_page.words
        if first_y - 1.0 <= word.box.center_y <= last_y + 1.0
    ]
    quote_lines = cluster_lines(quote_words)
    if not quote_lines:
        fail("no quotation lines measured")

    line_centers = [
        sum(word.box.center_y for word in line) / len(line) for line in quote_lines
    ]
    line_lefts = [min(word.box.x_min for word in line) for line in quote_lines]
    line_texts = [" ".join(word.text for word in line) for line in quote_lines]
    line_count = len(quote_lines)

    block_passed = (
        line_count >= min_lines
        and before_word.box.center_y < line_centers[0]
        and line_centers[-1] < after_word.box.center_y
        and all(
            abs(before_word.box.center_y - center) > 1.0
            and abs(after_word.box.center_y - center) > 1.0
            for center in line_centers
        )
    )

    expected_indent_pt = left_indent_mm * MM_TO_PT
    indent_offsets = [left - margin_word.box.x_min for left in line_lefts]
    indent_deltas = [abs(value - expected_indent_pt) for value in indent_offsets]
    indent_passed = all(delta <= horizontal_tolerance for delta in indent_deltas)

    typography_markers = [
        markers["quote_start"],
        markers["quote_middle"],
        markers["quote_end"],
    ]
    typography_samples = [
        typography_containing(runs, marker) for marker in typography_markers
    ]
    font_deltas = [abs(run.font_size - font_pt) for run in typography_samples]
    font_passed = all(delta <= font_tolerance for delta in font_deltas)

    cal_top_page, cal_top_word = located["calibration_top"]
    cal_bottom_page, cal_bottom_word = located["calibration_bottom"]
    if cal_top_page.index != cal_bottom_page.index:
        fail("line-spacing calibration markers must share one page")
    calibration_gap = cal_bottom_word.box.center_y - cal_top_word.box.center_y
    if calibration_gap <= 0:
        fail(f"invalid simple-spacing calibration gap: {calibration_gap}")

    quote_gaps = [
        line_centers[index + 1] - line_centers[index]
        for index in range(len(line_centers) - 1)
    ]
    if not quote_gaps or any(gap <= 0 for gap in quote_gaps):
        fail(f"invalid quotation line gaps: {quote_gaps}")
    spacing_deltas = [abs(gap - calibration_gap) for gap in quote_gaps]
    spacing_passed = all(delta <= vertical_tolerance for delta in spacing_deltas)

    forbidden = sorted(
        {char for text in line_texts for char in text if char in FORBIDDEN_QUOTES}
    )
    quote_marks_passed = not forbidden

    evidence = [
        {
            "rule_id": "quotation.long.block",
            "status": "PASS" if block_passed else "FAIL",
            "expected": selected["quotation.long.block"]["values"],
            "measured": {
                "page": quote_page.index,
                "line_count": line_count,
                "applicability_min_lines": min_lines,
                "before_center_y_pt": round(before_word.box.center_y, 4),
                "first_quote_center_y_pt": round(line_centers[0], 4),
                "last_quote_center_y_pt": round(line_centers[-1], 4),
                "after_center_y_pt": round(after_word.box.center_y, 4),
                "surrounding_body_lines_distinct": True,
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": None,
        },
        {
            "rule_id": "quotation.long.indent.left",
            "status": "PASS" if indent_passed else "FAIL",
            "expected": selected["quotation.long.indent.left"]["values"],
            "measured": {
                "page": quote_page.index,
                "expected_indent_pt": round(expected_indent_pt, 4),
                "margin_control_x_min_pt": round(margin_word.box.x_min, 4),
                "line_offsets_pt": [round(value, 4) for value in indent_offsets],
                "line_deltas_pt": [round(value, 4) for value in indent_deltas],
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": horizontal_tolerance,
        },
        {
            "rule_id": "quotation.long.font.size",
            "status": "PASS" if font_passed else "FAIL",
            "expected": selected["quotation.long.font.size"]["values"],
            "measured": {
                "samples": [
                    {
                        "marker": marker,
                        "page": run.page,
                        "font_pt": round(run.font_size, 4),
                        "delta_pt": round(delta, 4),
                        "family": run.family,
                    }
                    for marker, run, delta in zip(
                        typography_markers, typography_samples, font_deltas
                    )
                ]
            },
            "tool": "pdftohtml -xml -zoom 1.0",
            "tolerance": font_tolerance,
        },
        {
            "rule_id": "quotation.long.line-spacing",
            "status": "PASS" if spacing_passed else "FAIL",
            "expected": selected["quotation.long.line-spacing"]["values"],
            "measured": {
                "page": quote_page.index,
                "quote_line_gaps_pt": [round(value, 4) for value in quote_gaps],
                "calibration_gap_pt": round(calibration_gap, 4),
                "gap_deltas_pt": [round(value, 4) for value in spacing_deltas],
                "same_document_abntsmall_singlesp_calibration": True,
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": vertical_tolerance,
        },
        {
            "rule_id": "quotation.long.quotation-marks",
            "status": "PASS" if quote_marks_passed else "FAIL",
            "expected": selected["quotation.long.quotation-marks"]["values"],
            "measured": {
                "page": quote_page.index,
                "forbidden_quote_characters": forbidden,
                "quote_text_source_contains_no_quote_characters": True,
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": None,
        },
    ]

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "component": "long-quotation",
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

    average_gap = sum(quote_gaps) / len(quote_gaps)
    max_indent_delta = max(indent_deltas)
    max_spacing_delta = max(spacing_deltas)
    max_font_delta = max(font_deltas)
    print(
        "VALIDATION-EVIDENCE long-quotation-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" lines={line_count}"
        + f" max_indent_delta_pt={max_indent_delta:.4f}"
        + f" average_gap_pt={average_gap:.4f}"
        + f" calibration_gap_pt={calibration_gap:.4f}"
        + f" max_spacing_delta_pt={max_spacing_delta:.4f}"
        + f" max_font_delta_pt={max_font_delta:.4f}"
        + f" quote_marks={len(forbidden)}"
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
