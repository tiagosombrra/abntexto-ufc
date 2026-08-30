#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, normalize

SCENARIO = ROOT / "normativa" / "pretextual-cover-scenario.json"


def fail(message: str) -> None:
    raise SystemExit(f"Cover oracle failed: {message}")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def run(command: list[str]) -> bytes:
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        fail(f"command failed: {' '.join(command)}: {stderr}")
    return completed.stdout


def bbox_root(pdf: Path) -> ET.Element:
    payload = run(["pdftotext", "-bbox-layout", str(pdf), "-"])
    try:
        return ET.fromstring(payload)
    except ET.ParseError as exc:
        fail(f"invalid pdftotext XML for {pdf.name}: {exc}")


def html_root(pdf: Path) -> ET.Element:
    payload = run([
        "pdftohtml", "-xml", "-hidden", "-q", "-zoom", "1.0", "-stdout", str(pdf)
    ])
    try:
        return ET.fromstring(payload)
    except ET.ParseError as exc:
        fail(f"invalid pdftohtml XML for {pdf.name}: {exc}")


def page_nodes(root: ET.Element) -> list[ET.Element]:
    pages = [node for node in root.iter() if local(node.tag) == "page"]
    if not pages:
        fail("PDF extractor returned no pages")
    return pages


def words(node: ET.Element) -> list[ET.Element]:
    return [item for item in node.iter() if local(item.tag) == "word"]


def lines(node: ET.Element) -> list[ET.Element]:
    return [
        item for item in node.iter()
        if local(item.tag) == "line" and any(local(child.tag) == "word" for child in item)
    ]


def word_text(node: ET.Element) -> str:
    return "".join(node.itertext()).strip()


def line_text(node: ET.Element) -> str:
    return " ".join(word_text(item) for item in words(node))


def normalized_page_text(page: ET.Element) -> str:
    return normalize(" ".join(line_text(line) for line in lines(page)))


def find_word(page: ET.Element, marker: str) -> ET.Element | None:
    wanted = normalize(marker)
    for word in words(page):
        token = normalize(word_text(word)).strip(".,;:!?()[]{}")
        if token == wanted:
            return word
    return None


def find_line_containing(page: ET.Element, marker: str) -> ET.Element | None:
    wanted = normalize(marker)
    matches = [line for line in lines(page) if wanted in normalize(line_text(line))]
    return matches[0] if len(matches) == 1 else None


def y_min(node: ET.Element) -> float:
    try:
        return float(node.attrib["yMin"])
    except (KeyError, ValueError) as exc:
        fail(f"invalid bbox node: {node.attrib}")
        raise AssertionError from exc


def html_page(root: ET.Element, index: int) -> ET.Element:
    pages = page_nodes(root)
    if index < 1 or index > len(pages):
        fail(f"HTML page {index} out of range; pages={len(pages)}")
    return pages[index - 1]


def html_images(page: ET.Element) -> list[ET.Element]:
    return [node for node in page.iter() if local(node.tag) == "image"]


def html_text_nodes(page: ET.Element) -> list[ET.Element]:
    return [node for node in page.iter() if local(node.tag) == "text" and "".join(node.itertext()).strip()]


def html_text_top(page: ET.Element, marker: str) -> float | None:
    wanted = normalize(marker)
    matches = [
        node for node in html_text_nodes(page)
        if wanted in normalize("".join(node.itertext()))
    ]
    if len(matches) != 1:
        return None
    try:
        return float(matches[0].attrib["top"])
    except (KeyError, ValueError):
        return None


def image_top(page: ET.Element) -> float | None:
    images = html_images(page)
    if len(images) != 1:
        return None
    try:
        return float(images[0].attrib["top"])
    except (KeyError, ValueError):
        return None


def marker_page(pages: list[ET.Element], marker: str) -> int | None:
    hits = [index for index, page in enumerate(pages, start=1) if normalize(marker) in normalized_page_text(page)]
    return hits[0] if len(hits) == 1 else None


def record(rule_id: str, status: str, expected: Any, measured: Any, tool: str) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": tool,
    }


def project_optional_measurement(pdf: Path, before: str, after: str, hidden: str) -> dict[str, Any]:
    pages = page_nodes(bbox_root(pdf))
    before_page = marker_page(pages, before)
    after_page = marker_page(pages, after)
    hidden_present = any(normalize(hidden) in normalized_page_text(page) for page in pages)
    return {
        "pages": len(pages),
        "before_page": before_page,
        "after_page": after_page,
        "hidden_cover_token_present": hidden_present,
        "cover_suppressed": (
            len(pages) == 1
            and before_page == 1
            and after_page == 1
            and not hidden_present
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure N6 cover final-PDF evidence.")
    parser.add_argument("academic_pdf", type=Path)
    parser.add_argument("project_pdf", type=Path)
    parser.add_argument("anonymized_project_pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    for pdf in (args.academic_pdf, args.project_pdf, args.anonymized_project_pdf):
        if not pdf.is_file():
            fail(f"PDF not found: {pdf}")

    scenario = load_json(SCENARIO)
    if scenario.get("schema_version") != 1 or scenario.get("phase") != "N6":
        fail("invalid cover scenario schema/phase")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    expected_scope = {
        rule_id for rule_id in rules if rule_id.startswith("cover.")
    } | {"volume.number.cover-title-page", "project.cover.optional"}
    scenario_scope = set(scenario.get("rules", []))
    if scenario_scope != expected_scope or len(expected_scope) != 4:
        fail(
            "cover scope mismatch: "
            f"scenario_only={sorted(scenario_scope - expected_scope)} "
            f"contract_only={sorted(expected_scope - scenario_scope)} "
            f"count={len(expected_scope)}"
        )

    academic_bbox = bbox_root(args.academic_pdf)
    academic_pages = page_nodes(academic_bbox)
    academic_html = html_root(args.academic_pdf)
    config = scenario["academic"]
    cover_page_index = int(config["cover_page"])
    title_page_index = int(config["title_page"])
    if len(academic_pages) < title_page_index:
        fail(f"academic fixture has too few pages: {len(academic_pages)}")
    cover_page = academic_pages[cover_page_index - 1]
    title_page = academic_pages[title_page_index - 1]
    cover_html = html_page(academic_html, cover_page_index)
    markers = config["markers"]

    cover_text = normalized_page_text(cover_page)
    title_text = normalized_page_text(title_page)
    cover_images = html_images(cover_html)

    required_text_markers = [
        markers["institution"], markers["author"], markers["title"],
        markers["subtitle"], markers["city"], markers["year"],
    ]
    text_presence = {
        marker: normalize(marker) in cover_text for marker in required_text_markers
    }
    volume_cover = normalize(markers["volume"]) in cover_text
    volume_title_page = normalize(markers["volume"]) in title_text

    evidence: list[dict[str, Any]] = []

    rule = rules["cover.element.required"]
    expected_required = bool(rule["values"]["required"])
    cover_present = (
        len(cover_images) == 1
        and all(text_presence.values())
        and volume_cover
    )
    evidence.append(record(
        rule["id"],
        "PASS" if cover_present == expected_required else "FAIL",
        expected_required,
        {
            "cover_page": cover_page_index,
            "image_count": len(cover_images),
            "text_presence": text_presence,
            "volume_present": volume_cover,
        },
        "pdftotext -bbox-layout + pdftohtml -xml",
    ))

    rule = rules["cover.fields.order"]
    expected_order = rule["values"]["order"]
    supported_order = [
        "ufc-emblem", "institution", "author", "title", "subtitle-if-present",
        "volume-if-present", "city", "year",
    ]
    if expected_order != supported_order:
        fail(f"unsupported cover order contract: {expected_order}")

    image_y = image_top(cover_html)
    institution_y = html_text_top(cover_html, markers["institution"])
    author_y = html_text_top(cover_html, markers["author"])
    title_y = html_text_top(cover_html, markers["title"])
    subtitle_y = html_text_top(cover_html, markers["subtitle"])
    volume_y = html_text_top(cover_html, markers["volume"])
    city_y = html_text_top(cover_html, markers["city"])
    year_y = html_text_top(cover_html, markers["year"])
    y_values = [image_y, institution_y, author_y, title_y, volume_y, city_y, year_y]

    title_line = find_line_containing(cover_page, markers["title"])
    title_line_text = "" if title_line is None else normalize(line_text(title_line))
    title_before_subtitle = (
        normalize(markers["title"]) in title_line_text
        and normalize(markers["subtitle"]) in title_line_text
        and title_line_text.index(normalize(markers["title"]))
        < title_line_text.index(normalize(markers["subtitle"]))
    )
    vertical_order = (
        all(value is not None for value in y_values)
        and image_y < institution_y < author_y < title_y <= volume_y < city_y < year_y
        and subtitle_y is not None
        and abs(subtitle_y - title_y) <= 1.0
    )
    order_pass = vertical_order and title_before_subtitle
    evidence.append(record(
        rule["id"],
        "PASS" if order_pass else "FAIL",
        expected_order,
        {
            "image_top": image_y,
            "institution_top": institution_y,
            "author_top": author_y,
            "title_top": title_y,
            "subtitle_top": subtitle_y,
            "volume_top": volume_y,
            "city_top": city_y,
            "year_top": year_y,
            "title_before_subtitle": title_before_subtitle,
        },
        "pdftohtml -xml + pdftotext -bbox-layout",
    ))

    rule = rules["volume.number.cover-title-page"]
    expected_locations = rule["values"]["locations"]
    expected_volume_locations = ["cover", "title-page"]
    if expected_locations != expected_volume_locations:
        fail(f"unsupported volume location contract: {expected_locations}")
    volume_pass = volume_cover and volume_title_page
    evidence.append(record(
        rule["id"],
        "PASS" if volume_pass else "FAIL",
        expected_locations,
        {
            "volume_marker": markers["volume"],
            "cover_page": cover_page_index,
            "cover_present": volume_cover,
            "title_page": title_page_index,
            "title_page_present": volume_title_page,
        },
        "pdftotext -bbox-layout",
    ))

    profiles = scenario["project_optional"]["profiles"]
    project_measurements = {
        profiles[0]["name"]: project_optional_measurement(
            args.project_pdf,
            profiles[0]["before"],
            profiles[0]["after"],
            profiles[0]["hidden_cover_token"],
        ),
        profiles[1]["name"]: project_optional_measurement(
            args.anonymized_project_pdf,
            profiles[1]["before"],
            profiles[1]["after"],
            profiles[1]["hidden_cover_token"],
        ),
    }
    rule = rules["project.cover.optional"]
    expected_project_required = bool(rule["values"]["required"])
    optional_pass = (
        expected_project_required is False
        and all(item["cover_suppressed"] for item in project_measurements.values())
    )
    evidence.append(record(
        rule["id"],
        "PASS" if optional_pass else "FAIL",
        {"required": expected_project_required, "profiles": rule.get("applicability", {}).get("profiles")},
        project_measurements,
        "pdftotext -bbox-layout",
    ))

    counts = Counter(item["status"] for item in evidence)
    findings = [item["rule_id"] for item in evidence if item["status"] == "FAIL"]
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "scope": "cover",
        "mode": "enforce" if args.enforce else "audit",
        "source_commit_sha": args.commit_sha,
        "fixtures": scenario["fixtures"],
        "status_counts": dict(sorted(counts.items())),
        "findings": findings,
        "evidence": evidence,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "N6-EVIDENCE cover-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        + f" academic_pages={len(academic_pages)} images={len(cover_images)}"
    )
    for item in evidence:
        print(
            f"N6-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if args.enforce and findings:
        fail("enforcement requested with unresolved cover findings")


if __name__ == "__main__":
    try:
        main()
    except (PDFMeasurementError, KeyError, TypeError, ValueError) as exc:
        fail(str(exc))
