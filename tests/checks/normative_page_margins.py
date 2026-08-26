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
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages

SCENARIO = ROOT / "normativa" / "page-margins-scenario.json"
LOCATORS = ROOT / "normativa" / "locator-audit-layout-pagination.json"
ORACLE_POLICY = ROOT / "normativa" / "oracle-policy.json"
PT_PER_MM = 72.0 / 25.4
PAGE_RULE = "page.a4"
RECTO_RULES = [
    "margin.recto.left",
    "margin.recto.top",
    "margin.recto.right",
    "margin.recto.bottom",
]
VERSO_RULES = [
    "margin.verso.left",
    "margin.verso.top",
    "margin.verso.right",
    "margin.verso.bottom",
]
EXPECTED_RULE_IDS = [PAGE_RULE, *RECTO_RULES, *VERSO_RULES]
NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
TOKEN_PATTERN = re.compile(rf"[MLHVZmlhvz]|{NUMBER}")
MATRIX_PATTERN = re.compile(
    rf"^\s*matrix\(\s*({NUMBER})[\s,]+({NUMBER})[\s,]+({NUMBER})[\s,]+"
    rf"({NUMBER})[\s,]+({NUMBER})[\s,]+({NUMBER})\s*\)\s*$"
)
IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
THIN_LIMIT_PT = 2.0


def fail(message: str) -> None:
    raise SystemExit(f"N7 page/margins oracle failed: {message}")


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


def parse_path_points(data: str) -> list[tuple[float, float]]:
    tokens = TOKEN_PATTERN.findall(data)
    compact = re.sub(r"[\s,]+", "", data)
    token_compact = "".join(tokens)
    if compact.lower() != token_compact.lower():
        return []

    points: list[tuple[float, float]] = []
    current = (0.0, 0.0)
    start = (0.0, 0.0)
    command: str | None = None
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token
            index += 1
            if command in "Zz":
                current = start
                points.append(current)
                command = None
                continue
        if command is None:
            return []

        relative = command.islower()
        upper = command.upper()
        if upper in {"M", "L"}:
            if index + 1 >= len(tokens) or tokens[index].isalpha() or tokens[index + 1].isalpha():
                return []
            x = float(tokens[index])
            y = float(tokens[index + 1])
            index += 2
            if relative:
                x += current[0]
                y += current[1]
            current = (x, y)
            points.append(current)
            if upper == "M":
                start = current
                command = "l" if relative else "L"
        elif upper == "H":
            if index >= len(tokens) or tokens[index].isalpha():
                return []
            x = float(tokens[index])
            index += 1
            if relative:
                x += current[0]
            current = (x, current[1])
            points.append(current)
        elif upper == "V":
            if index >= len(tokens) or tokens[index].isalpha():
                return []
            y = float(tokens[index])
            index += 1
            if relative:
                y += current[1]
            current = (current[0], y)
            points.append(current)
        else:
            return []
    return points


def iter_shapes(
    element: ET.Element,
    inherited: tuple[float, float, float, float, float, float] = IDENTITY,
    in_defs: bool = False,
) -> Iterator[dict[str, float | str]]:
    name = local_name(element.tag)
    current_defs = in_defs or name == "defs"
    current = compose(inherited, parse_matrix(element.attrib.get("transform")))

    points: list[tuple[float, float]] = []
    if not current_defs and name == "path":
        raw_points = parse_path_points(element.attrib.get("d", ""))
        points = [transform_point(current, x, y) for x, y in raw_points]
    elif not current_defs and name == "rect":
        try:
            x = float(element.attrib.get("x", "0"))
            y = float(element.attrib.get("y", "0"))
            width = float(element.attrib["width"])
            height = float(element.attrib["height"])
        except (KeyError, ValueError):
            points = []
        else:
            points = [
                transform_point(current, x, y),
                transform_point(current, x + width, y),
                transform_point(current, x, y + height),
                transform_point(current, x + width, y + height),
            ]

    if points:
        xs = [item[0] for item in points]
        ys = [item[1] for item in points]
        yield {
            "x_min": min(xs),
            "x_max": max(xs),
            "y_min": min(ys),
            "y_max": max(ys),
            "width": max(xs) - min(xs),
            "height": max(ys) - min(ys),
            "stroke_width": element.attrib.get("stroke-width", ""),
            "element": name,
        }

    for child in element:
        yield from iter_shapes(child, current, current_defs)


def render_svg(pdf: Path, page: int) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
    temp_dir = tempfile.TemporaryDirectory(prefix=f"ufc-n7-page-margins-{page}-")
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
        fail(f"pdftocairo failed for page {page}: {completed.stdout.strip()}")
    return output, temp_dir


def frame_from_svg(svg_path: Path, page_width: float, page_height: float) -> dict[str, Any]:
    try:
        root = ET.parse(svg_path).getroot()
    except (OSError, ET.ParseError) as exc:
        fail(f"cannot parse SVG {svg_path}: {exc}")

    shapes = list(iter_shapes(root))
    horizontal = [
        item
        for item in shapes
        if float(item["width"]) >= page_width * 0.5
        and float(item["height"]) <= THIN_LIMIT_PT
    ]
    vertical = [
        item
        for item in shapes
        if float(item["height"]) >= page_height * 0.5
        and float(item["width"]) <= THIN_LIMIT_PT
    ]
    if len(horizontal) != 2 or len(vertical) != 2:
        fail(
            "expected two horizontal and two vertical text-area frame paths, "
            f"found horizontal={horizontal}, vertical={vertical}, shapes={shapes}"
        )

    horizontal.sort(key=lambda item: (float(item["y_min"]) + float(item["y_max"])) / 2.0)
    vertical.sort(key=lambda item: (float(item["x_min"]) + float(item["x_max"])) / 2.0)
    top, bottom = horizontal
    left, right = vertical

    left_x = (float(left["x_min"]) + float(left["x_max"])) / 2.0
    right_x = (float(right["x_min"]) + float(right["x_max"])) / 2.0
    top_y = (float(top["y_min"]) + float(top["y_max"])) / 2.0
    bottom_y = (float(bottom["y_min"]) + float(bottom["y_max"])) / 2.0

    corner_deltas = [
        abs(float(top["x_min"]) - left_x),
        abs(float(top["x_max"]) - right_x),
        abs(float(bottom["x_min"]) - left_x),
        abs(float(bottom["x_max"]) - right_x),
        abs(float(left["y_min"]) - top_y),
        abs(float(left["y_max"]) - bottom_y),
        abs(float(right["y_min"]) - top_y),
        abs(float(right["y_max"]) - bottom_y),
    ]
    if max(corner_deltas) > THIN_LIMIT_PT:
        fail(f"frame paths do not meet at one text-area rectangle: deltas={corner_deltas}")

    return {
        "left_x": left_x,
        "right_x": right_x,
        "top_y": top_y,
        "bottom_y": bottom_y,
        "corner_deltas": corner_deltas,
        "horizontal": horizontal,
        "vertical": vertical,
    }


def measurement(
    rule_id: str,
    expected: dict[str, Any],
    actual: float,
    expected_value: float,
    tolerance: float,
    detail: dict[str, Any],
) -> dict[str, Any]:
    delta = abs(actual - expected_value)
    measured = dict(detail)
    measured.update(
        {
            "actual_pt": round(actual, 4),
            "expected_pt": round(expected_value, 4),
            "delta_pt": round(delta, 4),
        }
    )
    return {
        "rule_id": rule_id,
        "status": "PASS" if delta <= tolerance else "FAIL",
        "expected": expected,
        "measured": measured,
        "tool": "pdftocairo -svg; pdftotext -bbox-layout",
        "tolerance": tolerance,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure N7 A4 page size and recto/verso margins from final-PDF geometry."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locator_rulesets = ruleset_map(load_json(LOCATORS))
    policy = load_json(ORACLE_POLICY)
    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N7"
        or scenario.get("component") != "page-margins"
    ):
        fail("invalid scenario schema/phase/component")
    if scenario.get("rules") != EXPECTED_RULE_IDS:
        fail(f"page/margins scenario scope drift: {scenario.get('rules')}")
    if policy.get("schema_version") != 1 or policy.get("phase") != "N5":
        fail("invalid oracle policy schema/phase")

    expected_locator_map = {PAGE_RULE: "layout.page-a4"}
    expected_locator_map.update({rule_id: "layout.margin-recto" for rule_id in RECTO_RULES})
    expected_locator_map.update({rule_id: "layout.margin-verso" for rule_id in VERSO_RULES})
    declared_locator_map = scenario.get("locator_rulesets")
    if not isinstance(declared_locator_map, dict):
        fail("scenario locator_rulesets is required")
    for rule_id, ruleset_id in expected_locator_map.items():
        if declared_locator_map.get(rule_id) != ruleset_id:
            fail(f"locator mapping drift for {rule_id}")
        ruleset = locator_rulesets.get(ruleset_id)
        if not isinstance(ruleset, dict) or rule_id not in ruleset.get("rule_ids", []):
            fail(f"locator ruleset {ruleset_id} no longer contains {rule_id}")

    pages_spec = scenario.get("pages")
    if pages_spec != {"recto": 1, "verso": 2}:
        fail(f"unexpected controlled page mapping: {pages_spec}")
    measurement_spec = scenario.get("measurement")
    if not isinstance(measurement_spec, dict):
        fail("measurement metadata is required")
    if measurement_spec.get("page_tool") != "pdftotext -bbox-layout":
        fail("page measurement tool drift")
    if measurement_spec.get("vector_tool") != "pdftocairo -svg":
        fail("vector measurement tool drift")
    if measurement_spec.get("frame") != "textwidth-by-textheight content frame":
        fail("frame definition drift")
    if measurement_spec.get("frame_paths_per_page") != 4:
        fail("frame path count drift")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    selected: dict[str, dict[str, Any]] = {}
    for rule_id in EXPECTED_RULE_IDS:
        rule = rules.get(rule_id)
        if not isinstance(rule, dict) or rule.get("authority") != "normative":
            fail(f"missing normative rule {rule_id}")
        selected[rule_id] = rule

    page_values = selected[PAGE_RULE].get("values")
    if not isinstance(page_values, dict) or page_values.get("width_mm") != 210 or page_values.get("height_mm") != 297:
        fail(f"unexpected contract values for {PAGE_RULE}: {page_values}")
    expected_margin_values = {
        "margin.recto.left": ("left_mm", 30),
        "margin.recto.top": ("top_mm", 30),
        "margin.recto.right": ("right_mm", 20),
        "margin.recto.bottom": ("bottom_mm", 20),
        "margin.verso.left": ("left_mm", 20),
        "margin.verso.top": ("top_mm", 30),
        "margin.verso.right": ("right_mm", 30),
        "margin.verso.bottom": ("bottom_mm", 20),
    }
    for rule_id, (key, value) in expected_margin_values.items():
        rule_values = selected[rule_id].get("values")
        if not isinstance(rule_values, dict) or rule_values.get(key) != value:
            fail(f"unexpected contract values for {rule_id}: {rule_values}")

    try:
        page_tolerance = float(policy["tolerances"]["page_size_pt"])
        horizontal_tolerance = float(policy["tolerances"]["horizontal_position_pt"])
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid oracle tolerance configuration: {exc}")
    if min(page_tolerance, horizontal_tolerance, vertical_tolerance) <= 0:
        fail("oracle tolerances must be positive")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))
    if len(pages) != 2 or [page.index for page in pages] != [1, 2]:
        fail(f"isolated page/margins fixture must contain pages 1 and 2, got {[page.index for page in pages]}")

    frames: dict[int, dict[str, Any]] = {}
    for page in pages:
        svg_path, temp_dir = render_svg(args.pdf.resolve(), page.index)
        try:
            frames[page.index] = frame_from_svg(svg_path, page.width, page.height)
        finally:
            temp_dir.cleanup()

    evidence: list[dict[str, Any]] = []
    expected_width_pt = float(page_values["width_mm"]) * PT_PER_MM
    expected_height_pt = float(page_values["height_mm"]) * PT_PER_MM
    width_deltas = [abs(page.width - expected_width_pt) for page in pages]
    height_deltas = [abs(page.height - expected_height_pt) for page in pages]
    page_passed = max([*width_deltas, *height_deltas]) <= page_tolerance
    evidence.append(
        {
            "rule_id": PAGE_RULE,
            "status": "PASS" if page_passed else "FAIL",
            "expected": page_values,
            "measured": {
                "pages": [
                    {
                        "page": page.index,
                        "width_pt": round(page.width, 4),
                        "height_pt": round(page.height, 4),
                        "width_delta_pt": round(width_deltas[index], 4),
                        "height_delta_pt": round(height_deltas[index], 4),
                    }
                    for index, page in enumerate(pages)
                ],
                "expected_width_pt": round(expected_width_pt, 4),
                "expected_height_pt": round(expected_height_pt, 4),
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": page_tolerance,
        }
    )

    for side, page_index, rule_ids in (
        ("recto", 1, RECTO_RULES),
        ("verso", 2, VERSO_RULES),
    ):
        page = pages[page_index - 1]
        frame = frames[page_index]
        actuals = {
            "left": float(frame["left_x"]),
            "top": float(frame["top_y"]),
            "right": page.width - float(frame["right_x"]),
            "bottom": page.height - float(frame["bottom_y"]),
        }
        for rule_id in rule_ids:
            dimension = rule_id.rsplit(".", 1)[-1]
            key, _ = expected_margin_values[rule_id]
            rule_values = selected[rule_id]["values"]
            expected_pt = float(rule_values[key]) * PT_PER_MM
            tolerance = horizontal_tolerance if dimension in {"left", "right"} else vertical_tolerance
            evidence.append(
                measurement(
                    rule_id,
                    rule_values,
                    actuals[dimension],
                    expected_pt,
                    tolerance,
                    {
                        "page": page_index,
                        "side": side,
                        "page_width_pt": round(page.width, 4),
                        "page_height_pt": round(page.height, 4),
                        "frame": {
                            "left_x_pt": round(float(frame["left_x"]), 4),
                            "right_x_pt": round(float(frame["right_x"]), 4),
                            "top_y_pt": round(float(frame["top_y"]), 4),
                            "bottom_y_pt": round(float(frame["bottom_y"]), 4),
                            "max_corner_delta_pt": round(max(frame["corner_deltas"]), 4),
                        },
                    },
                )
            )

    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    status_counts = dict(Counter(item["status"] for item in evidence))
    payload = {
        "schema_version": 1,
        "phase": "N7",
        "component": "page-margins",
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

    recto_frame = frames[1]
    verso_frame = frames[2]
    print(
        "N7-EVIDENCE page-margins-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" recto_frame={recto_frame['left_x']:.4f},{recto_frame['top_y']:.4f},"
        + f"{recto_frame['right_x']:.4f},{recto_frame['bottom_y']:.4f}"
        + f" verso_frame={verso_frame['left_x']:.4f},{verso_frame['top_y']:.4f},"
        + f"{verso_frame['right_x']:.4f},{verso_frame['bottom_y']:.4f}"
    )
    for item in evidence:
        print(
            f"N7-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
