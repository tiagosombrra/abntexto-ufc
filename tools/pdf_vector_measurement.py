#!/usr/bin/env python3
from __future__ import annotations

import math
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator

from pdf_measurement import Box, PDFMeasurementError

NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
PATH_TOKEN = re.compile(rf"[MmLlHhVvZz]|{NUMBER}")
UNSUPPORTED_PATH_COMMAND = re.compile(r"[CcQqSsTtAa]")
TRANSFORM = re.compile(r"(matrix|translate|scale)\s*\(([^)]*)\)")
IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


@dataclass(frozen=True)
class VectorRule:
    page: int
    orientation: str
    box: Box
    length: float
    thickness: float
    paint: str

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = asdict(self)
        payload["box"] = self.box.to_dict()
        return payload


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _compose(
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


def _transform_point(
    matrix: tuple[float, float, float, float, float, float],
    x: float,
    y: float,
) -> tuple[float, float]:
    a, b, c, d, e, f = matrix
    return a * x + c * y + e, b * x + d * y + f


def _parse_numbers(raw: str) -> list[float]:
    return [float(value) for value in re.findall(NUMBER, raw)]


def _parse_transform(value: str | None) -> tuple[float, float, float, float, float, float]:
    if not value:
        return IDENTITY
    current = IDENTITY
    cursor = 0
    matches = list(TRANSFORM.finditer(value))
    if not matches:
        raise PDFMeasurementError(f"unsupported SVG transform: {value!r}")
    for match in matches:
        if value[cursor:match.start()].strip(" ,\t\r\n"):
            raise PDFMeasurementError(f"unsupported SVG transform syntax: {value!r}")
        kind, raw_args = match.groups()
        args = _parse_numbers(raw_args)
        if kind == "matrix" and len(args) == 6:
            matrix = tuple(args)  # type: ignore[assignment]
        elif kind == "translate" and len(args) in {1, 2}:
            matrix = (1.0, 0.0, 0.0, 1.0, args[0], args[1] if len(args) == 2 else 0.0)
        elif kind == "scale" and len(args) in {1, 2}:
            matrix = (args[0], 0.0, 0.0, args[1] if len(args) == 2 else args[0], 0.0, 0.0)
        else:
            raise PDFMeasurementError(f"unsupported SVG transform: {value!r}")
        current = _compose(current, matrix)
        cursor = match.end()
    if value[cursor:].strip(" ,\t\r\n"):
        raise PDFMeasurementError(f"unsupported SVG transform syntax: {value!r}")
    return current


def _iter_paths(
    element: ET.Element,
    inherited: tuple[float, float, float, float, float, float] = IDENTITY,
    in_defs: bool = False,
) -> Iterator[tuple[ET.Element, tuple[float, float, float, float, float, float]]]:
    name = _local(element.tag)
    current_defs = in_defs or name == "defs"
    current = _compose(inherited, _parse_transform(element.attrib.get("transform")))
    if name == "path" and not current_defs:
        yield element, current
    for child in element:
        yield from _iter_paths(child, current, current_defs)


def _path_subpaths(d: str) -> list[tuple[list[tuple[float, float]], bool]]:
    if not d or UNSUPPORTED_PATH_COMMAND.search(d):
        return []
    tokens = PATH_TOKEN.findall(d.replace(",", " "))
    if not tokens:
        return []

    subpaths: list[tuple[list[tuple[float, float]], bool]] = []
    points: list[tuple[float, float]] = []
    start: tuple[float, float] | None = None
    current = (0.0, 0.0)
    command: str | None = None
    index = 0

    def finish(closed: bool = False) -> None:
        nonlocal points, start
        if points:
            subpaths.append((points, closed))
        points = []
        start = None

    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token
            index += 1
            if command in "Zz":
                if start is not None and points and points[-1] != start:
                    points.append(start)
                finish(True)
                command = None
            continue
        if command is None:
            return []

        if command in "MmLl":
            if index + 1 >= len(tokens) or tokens[index + 1].isalpha():
                return []
            x = float(tokens[index])
            y = float(tokens[index + 1])
            index += 2
            if command.islower():
                x += current[0]
                y += current[1]
            current = (x, y)
            if command in "Mm":
                if points:
                    finish(False)
                points = [current]
                start = current
                command = "l" if command == "m" else "L"
            else:
                if not points:
                    points = [current]
                    start = current
                else:
                    points.append(current)
            continue

        if command in "Hh":
            x = float(tokens[index])
            index += 1
            if command == "h":
                x += current[0]
            current = (x, current[1])
            if not points:
                points = [current]
                start = current
            else:
                points.append(current)
            continue

        if command in "Vv":
            y = float(tokens[index])
            index += 1
            if command == "v":
                y += current[1]
            current = (current[0], y)
            if not points:
                points = [current]
                start = current
            else:
                points.append(current)
            continue

        return []

    if points:
        finish(False)
    return subpaths


def _axis_aligned(points: list[tuple[float, float]], tolerance: float) -> bool:
    return all(
        abs(x2 - x1) <= tolerance or abs(y2 - y1) <= tolerance
        for (x1, y1), (x2, y2) in zip(points, points[1:])
    )


def _box(points: list[tuple[float, float]]) -> Box:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return Box(min(xs), min(ys), max(xs), max(ys))


def _stroke_width(element: ET.Element) -> float:
    raw = element.attrib.get("stroke-width", "1")
    match = re.search(NUMBER, raw)
    return float(match.group(0)) if match else 1.0


def _active_paint(element: ET.Element, name: str) -> bool:
    value = element.attrib.get(name)
    if value is None:
        return name == "fill"
    if value.lower() == "none":
        return False
    opacity = element.attrib.get(f"{name}-opacity")
    return opacity is None or float(opacity) > 0.0


def _rule_from_subpath(
    *,
    element: ET.Element,
    matrix: tuple[float, float, float, float, float, float],
    points: list[tuple[float, float]],
    closed: bool,
    page: int,
    axis_tolerance_pt: float,
    max_rule_thickness_pt: float,
    min_rule_length_pt: float,
) -> VectorRule | None:
    transformed = [_transform_point(matrix, x, y) for x, y in points]
    if len(transformed) < 2 or not _axis_aligned(transformed, axis_tolerance_pt):
        return None
    box = _box(transformed)
    fill = _active_paint(element, "fill")
    stroke = _active_paint(element, "stroke")

    if closed and fill:
        if box.width >= min_rule_length_pt and box.height <= max_rule_thickness_pt:
            return VectorRule(page, "horizontal", box, box.width, box.height, "filled-thin-rectangle")
        if box.height >= min_rule_length_pt and box.width <= max_rule_thickness_pt:
            return VectorRule(page, "vertical", box, box.height, box.width, "filled-thin-rectangle")

    if stroke:
        stroke_width = _stroke_width(element)
        if stroke_width > max_rule_thickness_pt:
            return None
        if box.width >= min_rule_length_pt and box.height <= axis_tolerance_pt:
            return VectorRule(page, "horizontal", box, box.width, stroke_width, "stroked-line")
        if box.height >= min_rule_length_pt and box.width <= axis_tolerance_pt:
            return VectorRule(page, "vertical", box, box.height, stroke_width, "stroked-line")
    return None


def vector_rules(
    pdf: Path,
    *,
    page: int = 1,
    axis_tolerance_pt: float = 0.5,
    max_rule_thickness_pt: float = 2.0,
    min_rule_length_pt: float = 5.0,
) -> list[VectorRule]:
    if not pdf.is_file():
        raise PDFMeasurementError(f"PDF not found: {pdf}")
    if page < 1:
        raise PDFMeasurementError("page must be >= 1")
    if min(axis_tolerance_pt, max_rule_thickness_pt, min_rule_length_pt) <= 0:
        raise PDFMeasurementError("vector rule parser thresholds must be positive")

    with tempfile.TemporaryDirectory(prefix="ufc-vector-rule-") as directory:
        output = Path(directory) / "page.svg"
        completed = subprocess.run(
            [
                "pdftocairo",
                "-svg",
                "-f",
                str(page),
                "-l",
                str(page),
                str(pdf.resolve()),
                str(output),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            check=False,
        )
        if completed.returncode != 0 or not output.is_file():
            raise PDFMeasurementError(f"pdftocairo -svg failed: {completed.stdout.strip()}")
        try:
            root = ET.parse(output).getroot()
        except (OSError, ET.ParseError) as exc:
            raise PDFMeasurementError(f"invalid pdftocairo SVG: {exc}") from exc

        result: list[VectorRule] = []
        for element, matrix in _iter_paths(root):
            for points, closed in _path_subpaths(element.attrib.get("d", "")):
                rule = _rule_from_subpath(
                    element=element,
                    matrix=matrix,
                    points=points,
                    closed=closed,
                    page=page,
                    axis_tolerance_pt=axis_tolerance_pt,
                    max_rule_thickness_pt=max_rule_thickness_pt,
                    min_rule_length_pt=min_rule_length_pt,
                )
                if rule is not None and math.isfinite(rule.length) and math.isfinite(rule.thickness):
                    result.append(rule)
    return result
