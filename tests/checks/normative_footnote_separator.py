#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize

SCENARIO = ROOT / "standards" / "footnote-separator-scenario.json"
FOOTNOTE_LOCATORS = ROOT / "standards" / "locator-audit-sections-footnotes-nature.json"
ORACLE_POLICY = ROOT / "standards" / "oracle-policy.json"
RULE_ID = "footnote.separator.length"
EXPECTED_RULE_IDS = [RULE_ID]
NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
LINE_PATTERN = re.compile(
    rf"^\s*M\s*({NUMBER})[\s,]+({NUMBER})\s+L\s*({NUMBER})[\s,]+({NUMBER})\s*$"
)
MATRIX_PATTERN = re.compile(
    rf"^\s*matrix\(\s*({NUMBER})[\s,]+({NUMBER})[\s,]+({NUMBER})[\s,]+"
    rf"({NUMBER})[\s,]+({NUMBER})[\s,]+({NUMBER})\s*\)\s*$"
)
IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
VECTOR_AXIS_TOLERANCE_PT = 0.5


def fail(message: str) -> None:
    raise SystemExit(f"N7 footnote separator oracle failed: {message}")


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


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_matrix(value: str | None) -> tuple[float, float, float, float, float, float]:
    if value is None:
        return IDENTITY
    match = MATRIX_PATTERN.fullmatch(value)
    if not match:
        fail(f"unsupported SVG transform: {value!r}")
    return tuple(float(item) for item in match.groups())  # type: ignore[return-value]


def compose(
    outer: tuple[float, float, float, float, float, float],
    inner: tuple[float, float, float, float, float, float],
) -> tuple[float, float, float, float, float, float]:
    a1, b1, c1, d1, e1, f1 = outer
    a2, b2, c2, d2, e2, f2 = inner
    return (
        a1 * a2 + c1 * b2,
        b1 * a2 + d1 * b2,
        a1 * c2 + c1 * d2,
        b1 * c2 + d1 * d2,
        a1 * e2 + c1 * f2 + e1,
        b1 * e2 + d1 * f2 + f1,
    )


def transform_point(
    matrix: tuple[float, float, float, float, float, float],
    x: float,
    y: float,
) -> tuple[float, float]:
    a, b, c, d, e, f = matrix
    return a * x + c * y + e, b * x + d * y + f


def iter_vector_paths(
    element: ET.Element,
    inherited: tuple[float, float, float, float, float, float] = IDENTITY,
    in_defs: bool = False,
) -> Iterator[tuple[ET.Element, tuple[float, float, float, float, float, float]]]:
    name = local_name(element.tag)
    current_defs = in_defs or name == "defs"
    current = compose(inherited, parse_matrix(element.attrib.get("transform")))
    if name == "path" and not current_defs:
        yield element, current
    for child in element:
        yield from iter_vector_paths(child, current, current_defs)


def extract_horizontal_lines(svg_path: Path) -> list[dict[str, float | str]]:
    try:
        root = ET.parse(svg_path).getroot()
    except (OSError, ET.ParseError) as exc:
        fail(f"cannot parse SVG {svg_path}: {exc}")

    lines: list[dict[str, float | str]] = []
    for element, matrix in iter_vector_paths(root):
        if element.attrib.get("fill") != "none":
            continue
        stroke = element.attrib.get("stroke")
        if not stroke or stroke == "none":
            continue
        match = LINE_PATTERN.fullmatch(element.attrib.get("d", ""))
        if not match:
            continue
        x1, y1, x2, y2 = (float(item) for item in match.groups())
        tx1, ty1 = transform_point(matrix, x1, y1)
        tx2, ty2 = transform_point(matrix, x2, y2)
        if abs(ty2 - ty1) > VECTOR_AXIS_TOLERANCE_PT:
            continue
        length = math.hypot(tx2 - tx1, ty2 - ty1)
        lines.append(
            {
                "x_min": min(tx1, tx2),
                "x_max": max(tx1, tx2),
                "y": (ty1 + ty2) / 2.0,
                "length": length,
                "stroke_width": element.attrib.get("stroke-width", ""),
            }
        )
    return lines


def render_svg(pdf: Path, page: int) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
    temp_dir = tempfile.TemporaryDirectory(prefix="ufc-n7-footnote-separator-")
    output = Path(temp_dir.name) / "page.svg"
    try:
        completed = subprocess.run(
            [
                "pdftocairo",
                "-svg",
                "-f",
                str(page),
                "-l",
                str(page),
                str(pdf),
                str(output),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            check=False,
        )
    except FileNotFoundError as exc:
        temp_dir.cleanup()
        fail(f"pdftocairo not found: {exc}")
    if completed.returncode != 0 or not output.is_file():
        temp_dir.cleanup()
        fail(f"pdftocairo failed: {completed.stdout.strip()}")
    return output, temp_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure the N7 footnote separator directly from final-PDF vector content."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locators = ruleset_map(load_json(FOOTNOTE_LOCATORS))
    policy = load_json(ORACLE_POLICY)

    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N7"
        or scenario.get("component") != "footnote-separator"
    ):
        fail("invalid scenario schema/phase/component")
    if scenario.get("rules") != EXPECTED_RULE_IDS:
        fail(f"footnote separator scenario scope drift: {scenario.get('rules')}")
    if policy.get("schema_version") != 1 or policy.get("phase") != "N5":
        fail("invalid oracle policy schema/phase")

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
        fail(f"invalid oracle tolerance configuration: {exc}")
    if min(horizontal_tolerance, vertical_tolerance) <= 0:
        fail("oracle tolerances must be positive")

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

    svg_path, temp_dir = render_svg(args.pdf.resolve(), margin_page.index)
    try:
        horizontal_lines = extract_horizontal_lines(svg_path)
    finally:
        temp_dir.cleanup()

    if len(horizontal_lines) != 1:
        fail(f"expected one non-glyph horizontal stroked vector path, found {horizontal_lines}")
    line = horizontal_lines[0]

    expected_length_pt = float(expected["length_mm"]) * 72.0 / 25.4
    measured_length_pt = float(line["length"])
    measured_start_x_pt = float(line["x_min"])
    measured_y_pt = float(line["y"])
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
        "stroke_width": line["stroke_width"],
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
        "phase": "N7",
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
        f"N7-EVIDENCE footnote-separator-summary {status}=1 "
        f"expected_length_pt={expected_length_pt:.4f} "
        f"measured_length_pt={measured_length_pt:.4f} "
        f"length_delta_pt={length_delta_pt:.4f} "
        f"origin_delta_pt={origin_delta_pt:.4f}"
    )
    print(
        f"N7-EVIDENCE rule={RULE_ID} status={status} "
        f"expected={json.dumps(expected, ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(measured, ensure_ascii=False, sort_keys=True)}"
    )

    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
