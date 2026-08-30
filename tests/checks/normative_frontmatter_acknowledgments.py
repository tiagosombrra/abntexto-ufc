#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import get_rule, load_catalog
from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, normalize, typography_runs

SCENARIO = ROOT / "standards" / "frontmatter-acknowledgements-scenario.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-policy.json"
PT_PER_MM = 72.0 / 25.4
HEADING = "AGRADECIMENTOS"


def fail(message: str) -> None:
    raise SystemExit(f"Acknowledgements validation failed: {message}")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {label}: {exc}")
    if not isinstance(data, dict):
        fail(f"{label} must be an object")
    return data


def full_rule_map() -> dict[str, dict[str, Any]]:
    return {rule["id"]: rule for rule in load_full_contract()["rules"]}


def bbox_root(pdf: Path) -> ET.Element:
    completed = subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        fail(completed.stderr.decode("utf-8", errors="replace").strip())
    try:
        return ET.fromstring(completed.stdout)
    except ET.ParseError as exc:
        fail(f"invalid pdftotext bbox XML: {exc}")


def word_text(node: ET.Element) -> str:
    return "".join(node.itertext()).strip()


def words(node: ET.Element) -> list[ET.Element]:
    return [item for item in node.iter() if local(item.tag) == "word"]


def lines(page: ET.Element) -> list[ET.Element]:
    return [
        item
        for item in page.iter()
        if local(item.tag) == "line"
        and any(local(child.tag) == "word" for child in item)
    ]


def page_list(root: ET.Element) -> list[ET.Element]:
    result = [item for item in root.iter() if local(item.tag) == "page"]
    if not result:
        fail("pdftotext returned no pages")
    return result


def find_marker_page(
    pages: list[ET.Element], marker: str
) -> tuple[int, ET.Element]:
    wanted = normalize(marker)
    matches: list[tuple[int, ET.Element]] = []
    for index, page in enumerate(pages, start=1):
        if any(normalize(word_text(item)) == wanted for item in words(page)):
            matches.append((index, page))
    if len(matches) != 1:
        fail(f"marker {marker}: expected one page, found {len(matches)}")
    return matches[0]


def find_marker_line(page: ET.Element, marker: str) -> tuple[int, ET.Element]:
    wanted = normalize(marker)
    matches: list[tuple[int, ET.Element]] = []
    for index, line in enumerate(lines(page)):
        if any(normalize(word_text(item)) == wanted for item in words(line)):
            matches.append((index, line))
    if len(matches) != 1:
        fail(f"marker {marker}: expected one line on target page, found {len(matches)}")
    return matches[0]


def find_heading_word(page: ET.Element) -> ET.Element:
    matches = [
        item for item in words(page) if normalize(word_text(item)) == HEADING
    ]
    if len(matches) != 1:
        fail(f"heading {HEADING}: expected one word, found {len(matches)}")
    return matches[0]


def line_bounds(line: ET.Element) -> tuple[float, float, float]:
    try:
        x_min = float(line.attrib["xMin"])
        x_max = float(line.attrib["xMax"])
        center_y = (
            float(line.attrib["yMin"]) + float(line.attrib["yMax"])
        ) / 2.0
    except (KeyError, ValueError) as exc:
        fail(f"invalid line bounds: {line.attrib}")
        raise AssertionError from exc
    return x_min, x_max, center_y


def average_gap(target_lines: list[ET.Element]) -> float:
    centers = [line_bounds(line)[2] for line in target_lines]
    gaps = [
        centers[index + 1] - centers[index]
        for index in range(len(centers) - 1)
    ]
    if not gaps or any(gap <= 0 for gap in gaps):
        fail(f"invalid top-to-bottom line geometry: {centers}")
    return mean(gaps)


def typography_contains(runs: list[Any], page: int, marker: str) -> Any:
    wanted = normalize(marker)
    matches = [
        run
        for run in runs
        if run.page == page and wanted in normalize(run.text)
    ]
    if len(matches) != 1:
        raise PDFMeasurementError(
            f"typography marker {marker}: expected one containing run on page "
            f"{page}, found {len(matches)}"
        )
    return matches[0]


def typography_exact(runs: list[Any], page: int, text: str) -> Any:
    wanted = normalize(text)
    matches = [
        run
        for run in runs
        if run.page == page and normalize(run.text) == wanted
    ]
    if len(matches) != 1:
        raise PDFMeasurementError(
            f"typography text {text}: expected one exact run on page {page}, "
            f"found {len(matches)}"
        )
    return matches[0]


def record(
    rule_id: str,
    status: str,
    expected: Any,
    measured: Any,
    tool: str,
    *,
    tolerance: float | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": tool,
    }
    if tolerance is not None:
        payload["tolerance"] = tolerance
    return payload


def boolean_status(actual: bool, expected: bool) -> str:
    return "PASS" if actual is expected else "FAIL"


def close_status(actual: float, expected: float, tolerance: float) -> str:
    return "PASS" if abs(actual - expected) <= tolerance else "FAIL"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure front matter acknowledgement-page final-PDF evidence."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    if not pdf.is_file():
        fail(f"PDF not found: {pdf}")

    scenario = load_json(SCENARIO, "acknowledgements scenario")
    validation_policy = load_json(VALIDATION_POLICY, "validation policy")
    if scenario.get("schema_version") != 2:
        fail("invalid acknowledgements scenario schema")
    if validation_policy.get("schema_version") != 2:
        fail("invalid validation policy schema")

    rules = full_rule_map()
    required = scenario.get("rules")
    if not isinstance(required, list) or len(required) != 8:
        fail("expected exactly eight acknowledgement atomic rules")
    missing = sorted(set(required) - set(rules))
    if missing:
        fail("scenario rules missing from full contract: " + ", ".join(missing))

    horizontal_tolerance = validation_policy.get("tolerances", {}).get(
        "horizontal_position_pt"
    )
    font_tolerance = validation_policy.get("tolerances", {}).get("font_size_pt")
    spacing_tolerance = scenario.get("tolerances", {}).get("line_spacing_pt")
    if not all(
        isinstance(value, (int, float)) and value > 0
        for value in (
            horizontal_tolerance,
            font_tolerance,
            spacing_tolerance,
        )
    ):
        fail("positive horizontal/font/spacing tolerances are required")

    catalog = load_catalog()
    recto = get_rule(catalog, "margin.recto")
    margin_left_mm = float(recto["values"]["left_mm"])
    margin_right_mm = float(recto["values"]["right_mm"])

    root = bbox_root(pdf)
    pages = page_list(root)
    markers = scenario["markers"]
    previous_page_index, _ = find_marker_page(pages, markers["previous_page"])
    body_page_index, body_page = find_marker_page(pages, markers["body_start"])
    end_page_index, _ = find_marker_page(pages, markers["body_end"])
    if body_page_index != end_page_index:
        fail("acknowledgement body start/end markers must be on one page")

    heading_word = find_heading_word(body_page)
    typography = typography_runs(pdf)
    heading_type = typography_exact(typography, body_page_index, HEADING)
    body_type = typography_contains(
        typography, body_page_index, markers["body_start"]
    )

    body_lines_all = lines(body_page)
    start_index, _ = find_marker_line(body_page, markers["body_start"])
    end_index, _ = find_marker_line(body_page, markers["body_end"])
    if start_index > end_index:
        fail("body markers are not in reading order")
    body_lines = body_lines_all[start_index : end_index + 1]
    minimum_lines = int(scenario["minimum_body_lines"])
    if len(body_lines) < minimum_lines:
        fail(
            f"expected at least {minimum_lines} naturally wrapped body lines, "
            f"found {len(body_lines)}"
        )

    calibration = scenario["calibration"]
    spacing_markers = calibration["line_spacing"]
    calibration_pages = [
        find_marker_page(pages, marker)[0] for marker in spacing_markers
    ]
    if len(set(calibration_pages)) != 1:
        fail(
            "spacing calibration markers must share one page: "
            f"{calibration_pages}"
        )
    calibration_page_index = calibration_pages[0]
    calibration_page = pages[calibration_page_index - 1]
    calibration_lines = [
        find_marker_line(calibration_page, marker)[1]
        for marker in spacing_markers
    ]
    calibrated_gap = average_gap(calibration_lines)
    body_gap = average_gap(body_lines)

    weight_markers = calibration["font_weight"]
    regular_type = typography_contains(
        typography,
        calibration_page_index,
        weight_markers["regular"],
    )
    bold_type = typography_contains(
        typography,
        calibration_page_index,
        weight_markers["bold"],
    )
    if regular_type.font_id == bold_type.font_id:
        fail(
            "font-weight calibration did not produce distinct regular and bold "
            f"font ids: {regular_type.font_id}"
        )

    page_width = float(body_page.attrib["width"])
    expected_left = margin_left_mm * PT_PER_MM
    expected_right = page_width - margin_right_mm * PT_PER_MM
    expected_center = (expected_left + expected_right) / 2.0
    heading_center = (
        float(heading_word.attrib["xMin"]) + float(heading_word.attrib["xMax"])
    ) / 2.0

    bounds = [line_bounds(line) for line in body_lines]
    non_first_left_deltas = [
        abs(item[0] - expected_left) for item in bounds[1:]
    ]
    non_final_right_deltas = [
        abs(item[1] - expected_right) for item in bounds[:-1]
    ]
    body_justified = (
        bool(non_first_left_deltas)
        and bool(non_final_right_deltas)
        and all(
            delta <= float(horizontal_tolerance)
            for delta in non_first_left_deltas
        )
        and all(
            delta <= float(horizontal_tolerance)
            for delta in non_final_right_deltas
        )
    )

    evidence: list[dict[str, Any]] = []

    rule = rules["acknowledgements.page.own"]
    expected = bool(rule["values"]["new_page"])
    actual = body_page_index > previous_page_index
    evidence.append(
        record(
            rule["id"],
            boolean_status(actual, expected),
            expected,
            {
                "previous_page": previous_page_index,
                "acknowledgements_page": body_page_index,
            },
            "pdftotext -bbox-layout",
        )
    )

    rule = rules["acknowledgements.heading.case"]
    expected = bool(rule["values"]["heading_uppercase"])
    raw_heading = word_text(heading_word)
    actual = raw_heading == raw_heading.upper() and normalize(raw_heading) == HEADING
    evidence.append(
        record(
            rule["id"],
            boolean_status(actual, expected),
            expected,
            raw_heading,
            "pdftotext -bbox-layout",
        )
    )

    rule = rules["acknowledgements.heading.weight"]
    expected = bool(rule["values"]["heading_bold"])
    actual = (
        heading_type.font_id == bold_type.font_id
        and heading_type.font_id != regular_type.font_id
    )
    evidence.append(
        record(
            rule["id"],
            boolean_status(actual, expected),
            expected,
            {
                "heading_font_id": heading_type.font_id,
                "heading_family": heading_type.family,
                "regular_font_id": regular_type.font_id,
                "regular_family": regular_type.family,
                "bold_font_id": bold_type.font_id,
                "bold_family": bold_type.family,
                "matches_bold_calibration": actual,
            },
            "pdftohtml -xml same-document font-id calibration",
        )
    )

    rule = rules["acknowledgements.heading.alignment"]
    expected = bool(rule["values"]["heading_centered"])
    center_delta = abs(heading_center - expected_center)
    actual = center_delta <= float(horizontal_tolerance)
    evidence.append(
        record(
            rule["id"],
            boolean_status(actual, expected),
            expected,
            {
                "heading_center_pt": round(heading_center, 4),
                "text_area_center_pt": round(expected_center, 4),
                "delta_pt": round(center_delta, 4),
            },
            "pdftotext -bbox-layout",
            tolerance=float(horizontal_tolerance),
        )
    )

    rule = rules["acknowledgements.heading.font-size"]
    expected_font = float(rule["values"]["font_pt"])
    evidence.append(
        record(
            rule["id"],
            close_status(
                heading_type.font_size,
                expected_font,
                float(font_tolerance),
            ),
            expected_font,
            {
                "font_pt": round(heading_type.font_size, 4),
                "family": heading_type.family,
            },
            "pdftohtml -xml",
            tolerance=float(font_tolerance),
        )
    )

    rule = rules["acknowledgements.body.font-size"]
    expected_font = float(rule["values"]["font_pt"])
    evidence.append(
        record(
            rule["id"],
            close_status(
                body_type.font_size,
                expected_font,
                float(font_tolerance),
            ),
            expected_font,
            {
                "font_pt": round(body_type.font_size, 4),
                "family": body_type.family,
            },
            "pdftohtml -xml",
            tolerance=float(font_tolerance),
        )
    )

    rule = rules["acknowledgements.body.line-spacing"]
    expected_spacing = float(rule["values"]["line_spacing"])
    evidence.append(
        record(
            rule["id"],
            close_status(
                body_gap,
                calibrated_gap,
                float(spacing_tolerance),
            ),
            {
                "contract": expected_spacing,
                "calibrated_gap_pt": round(calibrated_gap, 4),
            },
            {
                "body_average_gap_pt": round(body_gap, 4),
                "line_count": len(body_lines),
            },
            "pdftotext -bbox-layout + same-document spacing calibration",
            tolerance=float(spacing_tolerance),
        )
    )

    rule = rules["acknowledgements.body.alignment"]
    expected_alignment = rule["values"]["alignment"]
    if expected_alignment != "justified":
        fail(
            f"unsupported acknowledgement body alignment: {expected_alignment!r}"
        )
    evidence.append(
        record(
            rule["id"],
            "PASS" if body_justified else "FAIL",
            expected_alignment,
            {
                "line_count": len(body_lines),
                "first_line_x_min_pt": round(bounds[0][0], 4),
                "expected_left_pt": round(expected_left, 4),
                "expected_right_pt": round(expected_right, 4),
                "non_first_left_deltas_pt": [
                    round(delta, 4) for delta in non_first_left_deltas
                ],
                "non_final_right_deltas_pt": [
                    round(delta, 4) for delta in non_final_right_deltas
                ],
            },
            "pdftotext -bbox-layout",
            tolerance=float(horizontal_tolerance),
        )
    )

    counts = Counter(item["status"] for item in evidence)
    findings = [
        item["rule_id"] for item in evidence if item["status"] == "FAIL"
    ]
    payload = {
        "schema_version": 1,
        "validation_scope": "frontmatter",
        "scope": "acknowledgements",
        "mode": "enforce" if args.enforce else "audit",
        "source_commit_sha": args.commit_sha,
        "fixture": scenario["fixture"],
        "pdf": pdf.name,
        "status_counts": dict(sorted(counts.items())),
        "findings": findings,
        "measurement": {
            "acknowledgements_page": body_page_index,
            "body_line_count": len(body_lines),
            "calibration_page": calibration_page_index,
            "regular_font_id": regular_type.font_id,
            "bold_font_id": bold_type.font_id,
        },
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "FRONTMATTER-EVIDENCE acknowledgements-summary "
        + " ".join(
            f"{key}={value}" for key, value in sorted(counts.items())
        )
        + f" page={body_page_index} body_lines={len(body_lines)}"
    )
    for item in evidence:
        print(
            f"FRONTMATTER-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if args.enforce and findings:
        fail("enforcement requested with unresolved acknowledgement findings")


if __name__ == "__main__":
    try:
        main()
    except (PDFMeasurementError, KeyError, TypeError, ValueError) as exc:
        fail(str(exc))
