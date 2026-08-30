#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import normalize

SCENARIO = ROOT / "standards" / "frontmatter-title-page-scenario.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-policy.json"
PT_PER_MM = 72.0 / 25.4


def fail(message: str) -> None:
    raise SystemExit(f"Title-page validation failed: {message}")


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


def page_width(page: ET.Element) -> float:
    try:
        return float(page.attrib["width"])
    except (KeyError, ValueError) as exc:
        fail(f"page width unavailable: {page.attrib}")
        raise AssertionError from exc


def find_line(page: ET.Element, marker: str) -> ET.Element | None:
    wanted = normalize(marker)
    matches = [line for line in lines(page) if wanted in normalize(line_text(line))]
    return matches[0] if len(matches) == 1 else None


def find_word(page: ET.Element, marker: str) -> ET.Element | None:
    wanted = normalize(marker)
    for word in words(page):
        token = normalize(word_text(word)).strip(".,;:!?()[]{}")
        if token == wanted:
            return word
    return None


def y_min(node: ET.Element | None) -> float | None:
    if node is None:
        return None
    try:
        return float(node.attrib["yMin"])
    except (KeyError, ValueError):
        return None


def x_min(node: ET.Element | None) -> float | None:
    if node is None:
        return None
    try:
        return float(node.attrib["xMin"])
    except (KeyError, ValueError):
        return None


def x_max(node: ET.Element | None) -> float | None:
    if node is None:
        return None
    try:
        return float(node.attrib["xMax"])
    except (KeyError, ValueError):
        return None


def line_y(page: ET.Element, marker: str) -> float | None:
    return y_min(find_line(page, marker))


def marker_page(pages: list[ET.Element], marker: str) -> int | None:
    wanted = normalize(marker)
    hits = [
        index for index, page in enumerate(pages, start=1)
        if wanted in normalized_page_text(page)
    ]
    return hits[0] if len(hits) == 1 else None


def marker_gap(page: ET.Element, markers: list[str]) -> float | None:
    positions = [line_y(page, marker) for marker in markers]
    if any(value is None for value in positions):
        return None
    values = [float(value) for value in positions if value is not None]
    if len(values) < 2 or values != sorted(values):
        return None
    gaps = [b - a for a, b in zip(values, values[1:])]
    return statistics.mean(gaps)


def record(rule_id: str, status: str, expected: Any, measured: Any, tool: str) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": tool,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure front matter title-page final-PDF evidence.")
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
    policy = load_json(VALIDATION_POLICY)
    if scenario.get("schema_version") != 2:
        fail("invalid title-page scenario schema")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    explicit_cross_scope = {
        "volume.number.cover-title-page",
        "nature.line-spacing",
        "nature.block.alignment",
        "project.title-page.required",
        "project.anonymization.policy",
    }
    expected_scope = {
        rule_id for rule_id in rules if rule_id.startswith("title-page.")
    } | explicit_cross_scope
    scenario_scope = set(scenario.get("rules", []))
    if scenario_scope != expected_scope or len(expected_scope) != 7:
        fail(
            "title-page scope mismatch: "
            f"scenario_only={sorted(scenario_scope - expected_scope)} "
            f"contract_only={sorted(expected_scope - scenario_scope)} "
            f"count={len(expected_scope)}"
        )

    academic_pages = page_nodes(bbox_root(args.academic_pdf))
    project_pages = page_nodes(bbox_root(args.project_pdf))
    anonymized_pages = page_nodes(bbox_root(args.anonymized_project_pdf))

    academic = scenario["academic"]
    cover_index = int(academic["cover_page"])
    title_index = int(academic["title_page"])
    if len(academic_pages) < title_index:
        fail(f"academic fixture has too few pages: {len(academic_pages)}")
    cover_page = academic_pages[cover_index - 1]
    title_page = academic_pages[title_index - 1]
    am = academic["markers"]
    cover_text = normalized_page_text(cover_page)
    title_text = normalized_page_text(title_page)

    evidence: list[dict[str, Any]] = []

    rule = rules["title-page.element.required"]
    expected_required = bool(rule["values"]["required"])
    academic_required_markers = [
        am["author"], am["title"], am["subtitle"], am["volume"], am["nature"],
        am["advisor"], am["coadvisor"], am["city"], am["year"],
    ]
    academic_presence = {
        marker: normalize(marker) in title_text for marker in academic_required_markers
    }
    title_page_present = all(academic_presence.values())
    evidence.append(record(
        rule["id"],
        "PASS" if title_page_present == expected_required else "FAIL",
        expected_required,
        {
            "title_page": title_index,
            "page_count": len(academic_pages),
            "markers": academic_presence,
        },
        "pdftotext -bbox-layout",
    ))

    rule = rules["title-page.fields.order"]
    expected_order = rule["values"]["order"]
    supported_order = [
        "author", "title", "subtitle-if-present", "volume-if-present", "nature",
        "advisor-and-coadvisor-if-present", "city", "year",
    ]
    if expected_order != supported_order:
        fail(f"unsupported title-page order contract: {expected_order}")

    author_y = line_y(title_page, am["author"])
    title_y = line_y(title_page, am["title"])
    subtitle_y = line_y(title_page, am["subtitle"])
    volume_y = line_y(title_page, am["volume"])
    nature_y = line_y(title_page, am["nature"])
    advisor_y = line_y(title_page, am["advisor"])
    coadvisor_y = line_y(title_page, am["coadvisor"])
    city_y = line_y(title_page, am["city"])
    year_y = line_y(title_page, am["year"])
    title_line = find_line(title_page, am["title"])
    title_line_text = "" if title_line is None else normalize(line_text(title_line))
    title_before_subtitle = (
        normalize(am["title"]) in title_line_text
        and normalize(am["subtitle"]) in title_line_text
        and title_line_text.index(normalize(am["title"]))
        < title_line_text.index(normalize(am["subtitle"]))
    )
    vertical_values = [author_y, title_y, volume_y, nature_y, advisor_y, coadvisor_y, city_y, year_y]
    vertical_order = (
        all(value is not None for value in vertical_values)
        and author_y < title_y <= volume_y < nature_y < advisor_y <= coadvisor_y < city_y < year_y
        and subtitle_y is not None
        and abs(float(subtitle_y) - float(title_y)) <= 1.0
    )
    evidence.append(record(
        rule["id"],
        "PASS" if vertical_order and title_before_subtitle else "FAIL",
        expected_order,
        {
            "author_y_pt": author_y,
            "title_y_pt": title_y,
            "subtitle_y_pt": subtitle_y,
            "volume_y_pt": volume_y,
            "nature_y_pt": nature_y,
            "advisor_y_pt": advisor_y,
            "coadvisor_y_pt": coadvisor_y,
            "city_y_pt": city_y,
            "year_y_pt": year_y,
            "title_before_subtitle": title_before_subtitle,
        },
        "pdftotext -bbox-layout",
    ))

    rule = rules["volume.number.cover-title-page"]
    expected_locations = rule["values"]["locations"]
    if expected_locations != ["cover", "title-page"]:
        fail(f"unsupported volume location contract: {expected_locations}")
    volume_cover = normalize(am["volume"]) in cover_text
    volume_title = normalize(am["volume"]) in title_text
    evidence.append(record(
        rule["id"],
        "PASS" if volume_cover and volume_title else "FAIL",
        expected_locations,
        {
            "volume_marker": am["volume"],
            "cover_page": cover_index,
            "cover_present": volume_cover,
            "title_page": title_index,
            "title_page_present": volume_title,
        },
        "pdftotext -bbox-layout",
    ))

    project = scenario["project"]
    project_title_index = int(project["title_page"])
    if len(project_pages) < 2:
        fail("project fixture must contain title page plus calibration page")
    project_title_page = project_pages[project_title_index - 1]
    project_calibration_page = project_pages[1]
    pm = project["markers"]

    rule = rules["nature.line-spacing"]
    expected_factor = float(rule["values"]["factor"])
    nature_gap = marker_gap(project_title_page, pm["nature_lines"])
    calibration_gap = marker_gap(project_calibration_page, pm["calibration_lines"])
    vertical_tol = float(policy["tolerances"]["vertical_position_pt"])
    spacing_pass = (
        expected_factor == 1.0
        and nature_gap is not None
        and calibration_gap is not None
        and abs(nature_gap - calibration_gap) <= vertical_tol
    )
    evidence.append(record(
        rule["id"],
        "PASS" if spacing_pass else "FAIL",
        {"factor": expected_factor, "same_document_calibration": "singlesp"},
        {
            "nature_average_gap_pt": nature_gap,
            "calibration_average_gap_pt": calibration_gap,
            "delta_pt": None if nature_gap is None or calibration_gap is None else abs(nature_gap - calibration_gap),
        },
        "pdftotext -bbox-layout",
    ))

    rule = rules["nature.block.alignment"]
    expected_extent = rule["values"]["horizontal_extent"]
    if expected_extent != "mid-text-block-to-right-margin":
        fail(f"unsupported nature-block extent contract: {expected_extent}")
    left_rule = rules["margin.recto.left"]
    right_rule = rules["margin.recto.right"]
    left_margin_pt = float(left_rule["values"]["left_mm"]) * PT_PER_MM
    right_margin_pt = float(right_rule["values"]["right_mm"]) * PT_PER_MM
    width_pt = page_width(project_title_page)
    text_width_pt = width_pt - left_margin_pt - right_margin_pt
    expected_left_pt = left_margin_pt + text_width_pt / 2.0
    expected_right_pt = width_pt - right_margin_pt
    left_marker = find_word(project_title_page, pm["nature_left"])
    right_marker = find_word(project_title_page, pm["nature_right"])
    measured_left_pt = x_min(left_marker)
    measured_right_pt = x_max(right_marker)
    horizontal_tol = float(policy["tolerances"]["horizontal_position_pt"])
    alignment_pass = (
        measured_left_pt is not None
        and measured_right_pt is not None
        and abs(measured_left_pt - expected_left_pt) <= horizontal_tol
        and abs(measured_right_pt - expected_right_pt) <= horizontal_tol
    )
    evidence.append(record(
        rule["id"],
        "PASS" if alignment_pass else "FAIL",
        {
            "horizontal_extent": expected_extent,
            "expected_left_pt": round(expected_left_pt, 4),
            "expected_right_pt": round(expected_right_pt, 4),
        },
        {
            "measured_left_pt": measured_left_pt,
            "measured_right_pt": measured_right_pt,
            "left_delta_pt": None if measured_left_pt is None else round(abs(measured_left_pt - expected_left_pt), 4),
            "right_delta_pt": None if measured_right_pt is None else round(abs(measured_right_pt - expected_right_pt), 4),
        },
        "pdftotext -bbox-layout",
    ))

    rule = rules["project.title-page.required"]
    expected_project_required = bool(rule["values"]["required"])
    project_title_text = normalized_page_text(project_title_page)
    anon = scenario["anonymized_project"]
    anon_title_index = int(anon["title_page"])
    anon_title_page = anonymized_pages[anon_title_index - 1]
    anon_text = normalized_page_text(anon_title_page)
    anon_markers = anon["markers"]
    project_present = (
        normalize(pm["author"]) in project_title_text
        and normalize(pm["title"]) in project_title_text
        and normalize(pm["nature_left"]) in project_title_text
    )
    anon_present = (
        normalize(anon_markers["public_identifier"]) in anon_text
        and normalize(anon_markers["title"]) in anon_text
    )
    project_required_pass = expected_project_required and project_present and anon_present
    evidence.append(record(
        rule["id"],
        "PASS" if project_required_pass else "FAIL",
        {
            "required": expected_project_required,
            "profiles": rule.get("applicability", {}).get("profiles"),
        },
        {
            "projeto": {"title_page": project_title_index, "present": project_present},
            "projetoanonimizado": {"title_page": anon_title_index, "present": anon_present},
        },
        "pdftotext -bbox-layout",
    ))

    rule = rules["project.anonymization.policy"]
    hidden = rule["values"]["hide"]
    public_required = bool(rule["values"]["public_identifier_required"])
    if hidden != ["author", "advisor"] or not public_required:
        fail(f"unsupported anonymization contract: {rule['values']}")
    anon_all_text = normalize(" ".join(normalized_page_text(page) for page in anonymized_pages))
    hidden_author_present = normalize(anon_markers["hidden_author"]) in anon_all_text
    hidden_advisor_present = normalize(anon_markers["hidden_advisor"]) in anon_all_text
    public_identifier_present = normalize(anon_markers["public_identifier"]) in anon_all_text
    anonymization_pass = (
        not hidden_author_present
        and not hidden_advisor_present
        and public_identifier_present
    )
    evidence.append(record(
        rule["id"],
        "PASS" if anonymization_pass else "FAIL",
        rule["values"],
        {
            "hidden_author_present": hidden_author_present,
            "hidden_advisor_present": hidden_advisor_present,
            "public_identifier_present": public_identifier_present,
        },
        "pdftotext -bbox-layout",
    ))

    counts = Counter(item["status"] for item in evidence)
    findings = [item["rule_id"] for item in evidence if item["status"] == "FAIL"]
    payload = {
        "schema_version": 1,
        "validation_scope": "frontmatter",
        "scope": "title-page",
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
        "FRONTMATTER-EVIDENCE title-page-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        + f" academic_pages={len(academic_pages)} project_pages={len(project_pages)}"
    )
    for item in evidence:
        print(
            f"FRONTMATTER-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if args.enforce and findings:
        fail("enforcement requested with unresolved title-page findings")


if __name__ == "__main__":
    main()
