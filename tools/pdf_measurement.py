#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


class PDFMeasurementError(RuntimeError):
    pass


@dataclass(frozen=True)
class Box:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def width(self) -> float:
        return self.x_max - self.x_min

    @property
    def height(self) -> float:
        return self.y_max - self.y_min

    @property
    def center_x(self) -> float:
        return (self.x_min + self.x_max) / 2.0

    @property
    def center_y(self) -> float:
        return (self.y_min + self.y_max) / 2.0

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


@dataclass(frozen=True)
class Word:
    text: str
    box: Box


@dataclass(frozen=True)
class Page:
    index: int
    width: float
    height: float
    words: tuple[Word, ...]


@dataclass(frozen=True)
class Typography:
    page: int
    text: str
    box: Box
    font_id: str
    font_size: float
    family: str
    color: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["box"] = self.box.to_dict()
        return payload


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKD", text)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", value).strip().upper()


def _tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise PDFMeasurementError(f"required PDF tool not found: {name}")
    return path


def _run(command: list[str]) -> bytes:
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise PDFMeasurementError(
            f"command failed ({completed.returncode}): {' '.join(command)}: {stderr}"
        )
    return completed.stdout


def bbox_pages(pdf: Path) -> list[Page]:
    payload = _run([_tool("pdftotext"), "-bbox-layout", str(pdf), "-"])
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise PDFMeasurementError(f"invalid pdftotext bbox XML: {exc}") from exc

    pages: list[Page] = []
    for page_index, element in enumerate(
        (node for node in root.iter() if _local(node.tag) == "page"),
        start=1,
    ):
        words: list[Word] = []
        for word in (node for node in element.iter() if _local(node.tag) == "word"):
            words.append(
                Word(
                    text="".join(word.itertext()).strip(),
                    box=Box(
                        float(word.attrib["xMin"]),
                        float(word.attrib["yMin"]),
                        float(word.attrib["xMax"]),
                        float(word.attrib["yMax"]),
                    ),
                )
            )
        pages.append(
            Page(
                index=page_index,
                width=float(element.attrib["width"]),
                height=float(element.attrib["height"]),
                words=tuple(words),
            )
        )
    if not pages:
        raise PDFMeasurementError("pdftotext returned no PDF pages")
    return pages


def find_marker(pages: list[Page], marker: str) -> tuple[Page, Word]:
    wanted = normalize(marker)
    matches: list[tuple[Page, Word]] = []
    for page in pages:
        for word in page.words:
            if normalize(word.text) == wanted:
                matches.append((page, word))
    if len(matches) != 1:
        raise PDFMeasurementError(
            f"marker {marker}: expected exactly one word, found {len(matches)}"
        )
    return matches[0]


def typography_runs(pdf: Path) -> list[Typography]:
    payload = _run(
        [
            _tool("pdftohtml"),
            "-xml",
            "-hidden",
            "-i",
            "-q",
            "-zoom",
            "1.0",
            "-stdout",
            str(pdf),
        ]
    )
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise PDFMeasurementError(f"invalid pdftohtml XML: {exc}") from exc

    fonts: dict[str, dict[str, str]] = {}
    for spec in (node for node in root.iter() if _local(node.tag) == "fontspec"):
        font_id = spec.attrib.get("id")
        if font_id:
            fonts[font_id] = dict(spec.attrib)

    runs: list[Typography] = []
    page_index = 0
    for page in (node for node in root.iter() if _local(node.tag) == "page"):
        page_index += 1
        for text_node in (node for node in page.iter() if _local(node.tag) == "text"):
            text = "".join(text_node.itertext()).strip()
            if not text:
                continue
            font_id = text_node.attrib.get("font", "")
            spec = fonts.get(font_id, {})
            try:
                font_size = float(spec.get("size", "nan"))
            except ValueError as exc:
                raise PDFMeasurementError(
                    f"invalid font size for font id {font_id}: {spec.get('size')}"
                ) from exc
            runs.append(
                Typography(
                    page=page_index,
                    text=text,
                    box=Box(
                        float(text_node.attrib.get("left", "0")),
                        float(text_node.attrib.get("top", "0")),
                        float(text_node.attrib.get("left", "0"))
                        + float(text_node.attrib.get("width", "0")),
                        float(text_node.attrib.get("top", "0"))
                        + float(text_node.attrib.get("height", "0")),
                    ),
                    font_id=font_id,
                    font_size=font_size,
                    family=spec.get("family", ""),
                    color=spec.get("color", ""),
                )
            )
    if not runs:
        raise PDFMeasurementError("pdftohtml returned no typography runs")
    return runs


def find_typography_marker(runs: list[Typography], marker: str) -> Typography:
    wanted = normalize(marker)
    matches = [run for run in runs if normalize(run.text) == wanted]
    if len(matches) != 1:
        raise PDFMeasurementError(
            f"typography marker {marker}: expected exactly one run, found {len(matches)}"
        )
    return matches[0]


def pdf_info(pdf: Path) -> dict[str, str]:
    payload = _run([_tool("pdfinfo"), str(pdf)]).decode("utf-8", errors="replace")
    result: dict[str, str] = {}
    for line in payload.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def font_inventory(pdf: Path) -> list[dict[str, str]]:
    payload = _run([_tool("pdffonts"), str(pdf)]).decode("utf-8", errors="replace")
    rows: list[dict[str, str]] = []
    for line in payload.splitlines()[2:]:
        parts = line.split()
        if len(parts) < 8:
            continue
        rows.append(
            {
                "name": parts[0],
                "type": parts[1],
                "encoding": parts[2],
                "embedded": parts[-5],
                "subset": parts[-4],
                "unicode": parts[-3],
            }
        )
    return rows
