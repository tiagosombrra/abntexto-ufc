#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, normalize, typography_runs

SCENARIO = ROOT / "standards" / "index-glossary-final-pdf-scenario.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
PT_PER_MM = 72.0 / 25.4


def fail(message: str) -> None:
    raise SystemExit(f"index/glossary validation failed: {message}")


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {label}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    return value


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


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
        fail(f"invalid pdftotext bbox XML: {exc}")


def pages(root: ET.Element) -> list[ET.Element]:
    result = [node for node in root.iter() if local(node.tag) == "page"]
    if not result:
        fail("pdftotext returned no pages")
    return result


def words(node: ET.Element) -> list[ET.Element]:
    return [item for item in node.iter() if local(item.tag) == "word"]


def lines(node: ET.Element) -> list[ET.Element]:
    return [
        item
        for item in node.iter()
        if local(item.tag) == "line"
        and any(local(child.tag) == "word" for child in item)
    ]


def word_text(node: ET.Element) -> str:
    return "".join(node.itertext()).strip()


def line_text(node: ET.Element) -> str:
    return re.sub(r"\s+", " ", " ".join(word_text(word) for word in words(node))).strip()


def document_text(page_nodes: list[ET.Element]) -> str:
    return normalize(" ".join(word_text(word) for page in page_nodes for word in words(page)))


def document_has_heading(page_nodes: list[ET.Element], keyword: str) -> bool:
    wanted = normalize(keyword)
    return any(
        normalize(line_text(line)) == wanted
        for page in page_nodes
        for line in lines(page)
    )


def page_index_for_marker(page_nodes: list[ET.Element], marker: str) -> int:
    wanted = normalize(marker)
    matches: list[int] = []
    for index, page in enumerate(page_nodes, start=1):
        page_text = normalize(" ".join(word_text(word) for word in words(page)))
        if wanted in page_text:
            matches.append(index)
    if len(matches) != 1:
        fail(f"marker {marker}: expected one page, found {len(matches)}")
    return matches[0]


def heading_line(page: ET.Element, keyword: str) -> ET.Element:
    wanted = normalize(keyword)
    matches = [line for line in lines(page) if wanted in normalize(line_text(line))]
    if len(matches) != 1:
        fail(f"heading keyword {keyword}: expected one line, found {len(matches)}")
    return matches[0]


def line_center_x(line: ET.Element) -> float:
    try:
        return (float(line.attrib["xMin"]) + float(line.attrib["xMax"])) / 2.0
    except (KeyError, ValueError) as exc:
        fail(f"invalid line bounds: {line.attrib}")
        raise AssertionError from exc


def typography_containing(runs: list[Any], page: int, marker: str) -> Any:
    wanted = normalize(marker)
    matches = [run for run in runs if run.page == page and wanted in normalize(run.text)]
    if len(matches) != 1:
        raise PDFMeasurementError(
            f"typography marker {marker}: expected one run on page {page}, found {len(matches)}"
        )
    return matches[0]


def uppercase_text(value: str) -> bool:
    letters = [char for char in value if char.isalpha()]
    return bool(letters) and all(char == char.upper() for char in letters)


def record(rule_id: str, status: str, expected: Any, measured: Any, tool: str) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": tool,
    }


def require_value(rules: dict[str, dict[str, Any]], rule_id: str, expected: dict[str, Any]) -> None:
    actual = rules[rule_id].get("values")
    if actual != expected:
        fail(f"unsupported contract drift for {rule_id}: {actual!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure index/glossary final-PDF evidence.")
    parser.add_argument("present_pdf", type=Path)
    parser.add_argument("absent_pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    present_pdf = args.present_pdf.resolve()
    absent_pdf = args.absent_pdf.resolve()
    for pdf in (present_pdf, absent_pdf):
        if not pdf.is_file():
            fail(f"PDF not found: {pdf}")

    scenario = load_json(SCENARIO, "scenario")
    validation = load_json(VALIDATION_POLICY, "validation policy")
    if scenario.get("schema_version") != 1:
        fail("invalid scenario schema/phase")
    if validation.get("schema_version") != 2:
        fail("invalid validation policy schema")

    scenario_rules = scenario.get("rules")
    if not isinstance(scenario_rules, list) or len(scenario_rules) != 5:
        fail("scenario rule scope is invalid")

    rules = {rule["id"]: rule for rule in load_full_contract()["rules"]}
    missing = sorted(set(scenario_rules) - set(rules))
    if missing:
        fail("campaign rules missing from full contract: " + ", ".join(missing))

    supported = {
        "index.heading.case": {"heading_uppercase": True},
        "index.heading.weight": {"heading_bold": True},
        "index.heading.alignment": {"heading_centered": True},
        "index.heading.font-size": {"font_pt": 12},
        "glossary.element.optional": {"required": False},
    }
    if set(scenario_rules) != set(supported):
        fail("scenario rules drifted from the supported full-contract scope")

    for rule_id, expected in supported.items():
        require_value(rules, rule_id, expected)

    horizontal_tolerance = float(validation["tolerances"]["horizontal_position_pt"])
    font_tolerance = float(validation["tolerances"]["font_size_pt"])
    left_mm = float(rules["margin.recto.left"]["values"]["left_mm"])
    right_mm = float(rules["margin.recto.right"]["values"]["right_mm"])
    markers = scenario["markers"]

    present_root = bbox_root(present_pdf)
    absent_root = bbox_root(absent_pdf)
    present_pages = pages(present_root)
    absent_pages = pages(absent_root)
    present_text = document_text(present_pages)
    absent_text = document_text(absent_pages)

    index_page = page_index_for_marker(present_pages, markers["present_index_entry"])
    source_page = page_index_for_marker(present_pages, markers["regular_calibration"])
    index_page_node = present_pages[index_page - 1]
    index_heading = heading_line(index_page_node, markers["index_heading_keyword"])
    raw_heading = line_text(index_heading)

    typo = typography_runs(present_pdf)
    regular = typography_containing(typo, source_page, markers["regular_calibration"])
    bold = typography_containing(typo, source_page, markers["bold_calibration"])
    heading_type = typography_containing(typo, index_page, markers["index_heading_keyword"])
    if regular.font_id == bold.font_id:
        fail("regular/bold calibration did not produce distinct font ids")

    page_width = float(index_page_node.attrib["width"])
    text_area_center = (
        left_mm * PT_PER_MM + (page_width - right_mm * PT_PER_MM)
    ) / 2.0
    heading_center = line_center_x(index_heading)
    center_delta = abs(heading_center - text_area_center)
    font_delta = abs(float(heading_type.font_size) - 12.0)

    present_glossary_heading = document_has_heading(
        present_pages, markers["glossary_heading_keyword"]
    )
    present_glossary_entry = normalize(markers["present_glossary_entry"]) in present_text
    absent_glossary_heading = document_has_heading(
        absent_pages, markers["glossary_heading_keyword"]
    )
    absent_glossary_entry = normalize(markers["present_glossary_entry"]) in absent_text
    absent_index_entry = normalize(markers["absent_index_entry"]) in absent_text

    evidence = [
        record(
            "index.heading.case",
            "PASS" if uppercase_text(raw_heading) else "FAIL",
            supported["index.heading.case"],
            {
                "heading": raw_heading,
                "uppercase": uppercase_text(raw_heading),
                "exact_heading_text_frozen": False,
            },
            "pdftotext -bbox-layout",
        ),
        record(
            "index.heading.weight",
            "PASS" if heading_type.font_id == bold.font_id and heading_type.font_id != regular.font_id else "FAIL",
            supported["index.heading.weight"],
            {
                "heading_font_id": heading_type.font_id,
                "bold_calibration_font_id": bold.font_id,
                "regular_calibration_font_id": regular.font_id,
                "matches_bold_calibration": heading_type.font_id == bold.font_id,
                "differs_from_regular_calibration": heading_type.font_id != regular.font_id,
            },
            "pdftohtml -xml -zoom 1.0",
        ),
        record(
            "index.heading.alignment",
            "PASS" if center_delta <= horizontal_tolerance else "FAIL",
            supported["index.heading.alignment"],
            {
                "heading_center_pt": heading_center,
                "text_area_center_pt": text_area_center,
                "delta_pt": center_delta,
                "tolerance_pt": horizontal_tolerance,
            },
            "pdftotext -bbox-layout",
        ),
        record(
            "index.heading.font-size",
            "PASS" if font_delta <= font_tolerance else "FAIL",
            supported["index.heading.font-size"],
            {
                "font_pt": heading_type.font_size,
                "delta_pt": font_delta,
                "tolerance_pt": font_tolerance,
            },
            "pdftohtml -xml -zoom 1.0",
        ),
        record(
            "glossary.element.optional",
            "PASS"
            if present_glossary_heading
            and present_glossary_entry
            and not absent_glossary_heading
            and not absent_glossary_entry
            and absent_index_entry
            else "FAIL",
            supported["glossary.element.optional"],
            {
                "present_route": {
                    "pdf_rendered": True,
                    "heading_present": present_glossary_heading,
                    "entry_present": present_glossary_entry,
                },
                "absent_route": {
                    "pdf_rendered": True,
                    "heading_absent": not absent_glossary_heading,
                    "present_route_entry_absent": not absent_glossary_entry,
                    "independent_index_entry_present": absent_index_entry,
                },
                "glossary_typography_is_predicate": False,
            },
            "pdftotext -bbox-layout",
        ),
    ]

    passed = sum(item["status"] == "PASS" for item in evidence)
    failed = len(evidence) - passed
    payload = {
        "schema_version": 1,
        "campaign": "index-glossary-final-pdf",
        "source_commit_sha": args.commit_sha or None,
        "rendered_engine": "lualatex",
        "engine_matrix_deferred_to_n12": True,
        "proof_state_changed": False,
        "rules": evidence,
        "summary": {
            "pass": passed,
            "fail": failed,
            "n10_current_bounded_positive": 15 + passed,
            "n10_current_support_only": 5 - passed,
        },
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "VALIDATION-EVIDENCE index-glossary-final-pdf-summary "
        f"PASS={passed} FAIL={failed} index_page={index_page} "
        f"index_heading={json.dumps(raw_heading, ensure_ascii=False)}"
    )
    for item in evidence:
        print(
            f"VALIDATION-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
    print(
        "VALIDATION-EVIDENCE bounded-progress total=20 "
        "baseline_existing_bounded_positive=2 appendix_annex_bounded_positive=13 "
        f"promoted_bounded_positive={passed} current_bounded_positive={15 + passed} "
        f"current_support_only={5 - passed} proof_state_changed=false"
    )

    if failed:
        fail(f"{failed} of 5 final predicates failed")


if __name__ == "__main__":
    main()
