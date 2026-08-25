#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import get_rule, load_catalog
from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, normalize, typography_runs

SCENARIO = ROOT / "normativa" / "pretextual-summary-scenario.json"
ORACLE_POLICY = ROOT / "normativa" / "oracle-policy.json"
PT_PER_MM = 72.0 / 25.4


def fail(message: str) -> None:
    raise SystemExit(f"Summary oracle failed: {message}")


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
        if local(item.tag) == "line" and any(local(child.tag) == "word" for child in item)
    ]


def line_text(line: ET.Element) -> str:
    return " ".join(word_text(item) for item in words(line))


def page_list(root: ET.Element) -> list[ET.Element]:
    result = [item for item in root.iter() if local(item.tag) == "page"]
    if not result:
        fail("pdftotext returned no pages")
    return result


def find_marker_page(pages: list[ET.Element], marker: str) -> tuple[int, ET.Element]:
    wanted = normalize(marker)
    matches: list[tuple[int, ET.Element]] = []
    for index, page in enumerate(pages, start=1):
        if any(normalize(word_text(item)).strip(".,;:!?()[]{}") == wanted for item in words(page)):
            matches.append((index, page))
    if len(matches) != 1:
        fail(f"marker {marker}: expected one page, found {len(matches)}")
    return matches[0]


def find_marker_line(page: ET.Element, marker: str) -> tuple[int, ET.Element]:
    wanted = normalize(marker)
    matches: list[tuple[int, ET.Element]] = []
    for index, line in enumerate(lines(page)):
        if any(normalize(word_text(item)).strip(".,;:!?()[]{}") == wanted for item in words(line)):
            matches.append((index, line))
    if len(matches) != 1:
        fail(f"marker {marker}: expected one line on target page, found {len(matches)}")
    return matches[0]


def find_heading_line(page: ET.Element, heading: str) -> ET.Element | None:
    wanted = normalize(heading)
    matches = [line for line in lines(page) if normalize(line_text(line)) == wanted]
    return matches[0] if len(matches) == 1 else None


def find_keyword_line(page: ET.Element, label: str) -> ET.Element | None:
    wanted = normalize(label)
    matches = [line for line in lines(page) if normalize(line_text(line)).startswith(wanted)]
    return matches[0] if len(matches) == 1 else None


def line_bounds(line: ET.Element) -> tuple[float, float, float]:
    try:
        x_min = float(line.attrib["xMin"])
        x_max = float(line.attrib["xMax"])
        center_y = (float(line.attrib["yMin"]) + float(line.attrib["yMax"])) / 2.0
    except (KeyError, ValueError) as exc:
        fail(f"invalid line bounds: {line.attrib}")
        raise AssertionError from exc
    return x_min, x_max, center_y


def average_gap(target_lines: list[ET.Element]) -> float:
    centers = [line_bounds(line)[2] for line in target_lines]
    gaps = [centers[index + 1] - centers[index] for index in range(len(centers) - 1)]
    if not gaps or any(gap <= 0 for gap in gaps):
        fail(f"invalid top-to-bottom line geometry: {centers}")
    return mean(gaps)


def source_body_paragraphs(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read fixture {path}: {exc}")
    before_macro = re.split(r"\\(?:palavraschave|keywords)\s*\{", text, maxsplit=1)[0].strip()
    paragraphs = [chunk.strip() for chunk in re.split(r"\n\s*\n", before_macro) if chunk.strip()]
    return len(paragraphs)


def typography_contains(runs: list[Any], page: int, marker: str) -> Any:
    wanted = normalize(marker)
    matches = [run for run in runs if run.page == page and wanted in normalize(run.text)]
    if len(matches) != 1:
        raise PDFMeasurementError(
            f"typography marker {marker}: expected one containing run on page {page}, found {len(matches)}"
        )
    return matches[0]


def normalized_word_count(target_lines: list[ET.Element], markers: set[str]) -> int:
    wanted = {normalize(marker) for marker in markers}
    count = 0
    for line in target_lines:
        for word in words(line):
            token = normalize(word_text(word)).strip(".,;:!?()[]{}")
            if token and token not in wanted:
                count += 1
    return count


def keyword_payload(line: ET.Element | None) -> str | None:
    if line is None:
        return None
    text = line_text(line).strip()
    if ":" not in text:
        return None
    return text.split(":", 1)[1].strip()


def starts_lowercase(keyword: str) -> bool:
    for char in keyword.strip():
        if char.isalpha():
            return char.islower()
    return False


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


def component_measurement(
    *,
    name: str,
    config: dict[str, Any],
    page_index: int,
    page: ET.Element,
    typography: list[Any],
    calibrated_gap: float,
    expected_left: float,
    expected_right: float,
    horizontal_tolerance: float,
    font_tolerance: float,
    spacing_tolerance: float,
    keyword_gap_tolerance: float,
) -> dict[str, Any]:
    start_index, _ = find_marker_line(page, config["body_start"])
    end_index, _ = find_marker_line(page, config["body_end"])
    if start_index > end_index:
        fail(f"{name}: body markers are not in reading order")

    page_lines = lines(page)
    body_lines = page_lines[start_index : end_index + 1]
    minimum_lines = int(load_json(SCENARIO, "scenario")["minimum_body_lines"])
    if len(body_lines) < minimum_lines:
        fail(f"{name}: expected at least {minimum_lines} wrapped body lines, found {len(body_lines)}")

    heading_line = find_heading_line(page, config["heading"])
    keyword_line = find_keyword_line(page, config["keyword_label"])
    body_type = typography_contains(typography, page_index, config["body_start"])

    bounds = [line_bounds(line) for line in body_lines]
    body_gap = average_gap(body_lines)
    left_deltas = [abs(item[0] - expected_left) for item in bounds]
    right_deltas = [abs(item[1] - expected_right) for item in bounds[:-1]]
    first_x = bounds[0][0]
    continuation_x = median(item[0] for item in bounds[1:])

    keyword_gap = None
    if keyword_line is not None:
        keyword_gap = line_bounds(keyword_line)[2] - bounds[-1][2]

    payload = keyword_payload(keyword_line)
    keywords = []
    if payload is not None:
        keywords = [item.strip().rstrip(".") for item in payload.split(";")]

    fixture_path = ROOT / (
        "tests/fixtures/pretextuais/n6-summary.tex"
        if name == "vernacular"
        else "tests/fixtures/pretextuais/n6-abstract.tex"
    )

    return {
        "page": page_index,
        "heading_present": heading_line is not None,
        "body_lines": body_lines,
        "body_line_count": len(body_lines),
        "word_count": normalized_word_count(
            body_lines, {config["body_start"], config["body_end"]}
        ),
        "font_size": body_type.font_size,
        "font_family": body_type.family,
        "body_gap": body_gap,
        "spacing_matches": abs(body_gap - calibrated_gap) <= spacing_tolerance,
        "first_line_x": first_x,
        "continuation_x": continuation_x,
        "zero_indent": (
            abs(first_x - expected_left) <= horizontal_tolerance
            and abs(first_x - continuation_x) <= horizontal_tolerance
        ),
        "left_deltas": left_deltas,
        "right_deltas": right_deltas,
        "justified": (
            all(delta <= horizontal_tolerance for delta in left_deltas)
            and all(delta <= horizontal_tolerance for delta in right_deltas)
        ),
        "source_paragraphs": source_body_paragraphs(fixture_path),
        "keyword_present": keyword_line is not None and payload is not None,
        "keyword_payload": payload,
        "keywords": keywords,
        "keyword_gap": keyword_gap,
        "keyword_position_ok": (
            keyword_gap is not None
            and keyword_gap > 0
            and abs(keyword_gap - (2.0 * calibrated_gap)) <= keyword_gap_tolerance
        ),
        "separator_ok": (
            payload is not None
            and payload.count(";") == config["keyword_text"].count(";")
            and "," not in payload
        ),
        "terminal_ok": payload is not None and payload.endswith("."),
        "initial_case_ok": bool(keywords) and all(starts_lowercase(item) for item in keywords),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure N6 summary/abstract final-PDF evidence.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    if not pdf.is_file():
        fail(f"PDF not found: {pdf}")

    scenario = load_json(SCENARIO, "summary scenario")
    oracle = load_json(ORACLE_POLICY, "oracle policy")
    if scenario.get("schema_version") != 1 or scenario.get("phase") != "N6":
        fail("invalid summary scenario schema/phase")
    if oracle.get("schema_version") != 1 or oracle.get("phase") != "N5":
        fail("invalid oracle policy schema/phase")

    full = load_full_contract()
    rules = {rule["id"]: rule for rule in full["rules"]}
    scenario_rules = set(scenario.get("rules", []))
    contract_summary_rules = {rule_id for rule_id in rules if rule_id.startswith("summary.")}
    if scenario_rules != contract_summary_rules:
        fail(
            "summary scenario/full-contract mismatch: "
            f"scenario_only={sorted(scenario_rules - contract_summary_rules)} "
            f"contract_only={sorted(contract_summary_rules - scenario_rules)}"
        )
    if len(scenario_rules) != 14:
        fail(f"expected 14 active summary rules, found {len(scenario_rules)}")

    horizontal_tolerance = oracle.get("tolerances", {}).get("horizontal_position_pt")
    font_tolerance = oracle.get("tolerances", {}).get("font_size_pt")
    spacing_tolerance = scenario.get("tolerances", {}).get("line_spacing_pt")
    keyword_gap_tolerance = scenario.get("tolerances", {}).get("keyword_blank_line_gap_pt")
    if not all(
        isinstance(value, (int, float)) and value > 0
        for value in (
            horizontal_tolerance,
            font_tolerance,
            spacing_tolerance,
            keyword_gap_tolerance,
        )
    ):
        fail("positive horizontal/font/spacing/keyword-gap tolerances are required")

    catalog = load_catalog()
    recto = get_rule(catalog, "margin.recto")
    expected_left = float(recto["values"]["left_mm"]) * PT_PER_MM

    root = bbox_root(pdf)
    pages = page_list(root)
    typography = typography_runs(pdf)

    calibration_markers = scenario["calibration"]
    calibration_pages = [find_marker_page(pages, marker)[0] for marker in calibration_markers]
    if len(set(calibration_pages)) != 1:
        fail(f"spacing calibration markers must share one page: {calibration_pages}")
    calibration_page = pages[calibration_pages[0] - 1]
    calibration_lines = [find_marker_line(calibration_page, marker)[1] for marker in calibration_markers]
    calibrated_gap = average_gap(calibration_lines)

    measurements: dict[str, dict[str, Any]] = {}
    for name, config in scenario["components"].items():
        page_index, page = find_marker_page(pages, config["body_start"])
        end_page, _ = find_marker_page(pages, config["body_end"])
        if page_index != end_page:
            fail(f"{name}: body start/end markers must share one page")
        page_width = float(page.attrib["width"])
        expected_right = page_width - float(recto["values"]["right_mm"]) * PT_PER_MM
        measurements[name] = component_measurement(
            name=name,
            config=config,
            page_index=page_index,
            page=page,
            typography=typography,
            calibrated_gap=calibrated_gap,
            expected_left=expected_left,
            expected_right=expected_right,
            horizontal_tolerance=float(horizontal_tolerance),
            font_tolerance=float(font_tolerance),
            spacing_tolerance=float(spacing_tolerance),
            keyword_gap_tolerance=float(keyword_gap_tolerance),
        )

    vern = measurements["vernacular"]
    foreign = measurements["foreign"]
    evidence: list[dict[str, Any]] = []

    rule = rules["summary.vernacular.required"]
    expected = bool(rule["values"]["required"])
    actual = vern["heading_present"] and vern["page"] > 0
    evidence.append(record(rule["id"], "PASS" if actual == expected else "FAIL", expected,
                           {"page": vern["page"], "heading_present": vern["heading_present"]},
                           "pdftotext -bbox-layout"))

    rule = rules["summary.foreign.required"]
    expected = bool(rule["values"]["required"])
    actual = foreign["heading_present"] and foreign["page"] > 0 and foreign["page"] != vern["page"]
    evidence.append(record(rule["id"], "PASS" if actual == expected else "FAIL", expected,
                           {"page": foreign["page"], "heading_present": foreign["heading_present"],
                            "distinct_from_vernacular": foreign["page"] != vern["page"]},
                           "pdftotext -bbox-layout"))

    rule = rules["summary.paragraph.single"]
    expected = int(rule["values"]["paragraphs"])
    measured_paragraphs = {
        "vernacular": vern["source_paragraphs"],
        "foreign": foreign["source_paragraphs"],
    }
    continuity = {
        "vernacular_gap_delta_pt": round(abs(vern["body_gap"] - calibrated_gap), 4),
        "foreign_gap_delta_pt": round(abs(foreign["body_gap"] - calibrated_gap), 4),
    }
    actual = (
        vern["source_paragraphs"] == expected
        and foreign["source_paragraphs"] == expected
        and vern["spacing_matches"]
        and foreign["spacing_matches"]
    )
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL", expected,
                           {"source_paragraphs": measured_paragraphs, "pdf_continuity": continuity},
                           "fixture source + pdftotext -bbox-layout"))

    rule = rules["summary.word-count.range"]
    minimum = int(rule["values"]["academic_work_min"])
    maximum = int(rule["values"]["academic_work_max"])
    counts = {"vernacular": vern["word_count"], "foreign": foreign["word_count"]}
    actual = all(minimum <= value <= maximum for value in counts.values())
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL",
                           {"min": minimum, "max": maximum}, counts,
                           "pdftotext -bbox-layout"))

    rule = rules["summary.keywords.required"]
    expected = bool(rule["values"]["required"])
    actual = vern["keyword_present"] and foreign["keyword_present"]
    evidence.append(record(rule["id"], "PASS" if actual == expected else "FAIL", expected,
                           {"vernacular": vern["keyword_present"], "foreign": foreign["keyword_present"]},
                           "pdftotext -bbox-layout"))

    rule = rules["summary.foreign.keywords.required"]
    expected = bool(rule["values"]["required"])
    actual = foreign["keyword_present"]
    evidence.append(record(rule["id"], "PASS" if actual == expected else "FAIL", expected,
                           {"foreign": foreign["keyword_present"], "payload": foreign["keyword_payload"]},
                           "pdftotext -bbox-layout"))

    rule = rules["summary.keywords.position"]
    expected = rule["values"]
    actual = vern["keyword_position_ok"] and foreign["keyword_position_ok"]
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL", expected,
                           {
                               "calibrated_body_gap_pt": round(calibrated_gap, 4),
                               "expected_keyword_gap_pt": round(2.0 * calibrated_gap, 4),
                               "vernacular_keyword_gap_pt": None if vern["keyword_gap"] is None else round(vern["keyword_gap"], 4),
                               "foreign_keyword_gap_pt": None if foreign["keyword_gap"] is None else round(foreign["keyword_gap"], 4),
                           },
                           "pdftotext -bbox-layout + same-document spacing calibration",
                           tolerance=float(keyword_gap_tolerance)))

    rule = rules["summary.keywords.separator"]
    expected = rule["values"]["separator"]
    actual = vern["separator_ok"] and foreign["separator_ok"]
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL", expected,
                           {"vernacular": vern["keyword_payload"], "foreign": foreign["keyword_payload"]},
                           "pdftotext"))

    rule = rules["summary.keywords.terminal-punctuation"]
    expected = rule["values"]["terminal"]
    actual = vern["terminal_ok"] and foreign["terminal_ok"]
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL", expected,
                           {"vernacular": vern["keyword_payload"], "foreign": foreign["keyword_payload"]},
                           "pdftotext"))

    rule = rules["summary.keywords.initial-case"]
    expected = rule["values"]["default_initial"]
    actual = vern["initial_case_ok"] and foreign["initial_case_ok"]
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL", expected,
                           {"vernacular": vern["keywords"], "foreign": foreign["keywords"]},
                           "pdftotext"))

    rule = rules["summary.font.size"]
    expected_font = float(rule["values"]["font_pt"])
    font_values = {"vernacular": vern["font_size"], "foreign": foreign["font_size"]}
    actual = all(abs(value - expected_font) <= float(font_tolerance) for value in font_values.values())
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL", expected_font,
                           {key: round(value, 4) for key, value in font_values.items()},
                           "pdftohtml -xml", tolerance=float(font_tolerance)))

    rule = rules["summary.line-spacing"]
    expected_spacing = float(rule["values"]["line_spacing"])
    actual = vern["spacing_matches"] and foreign["spacing_matches"]
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL",
                           {"contract": expected_spacing, "calibrated_gap_pt": round(calibrated_gap, 4)},
                           {"vernacular_gap_pt": round(vern["body_gap"], 4),
                            "foreign_gap_pt": round(foreign["body_gap"], 4)},
                           "pdftotext -bbox-layout + same-document spacing calibration",
                           tolerance=float(spacing_tolerance)))

    rule = rules["summary.first-line.indent"]
    expected_indent = float(rule["values"]["first_line_indent_mm"])
    actual = vern["zero_indent"] and foreign["zero_indent"]
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL", expected_indent,
                           {
                               "expected_left_pt": round(expected_left, 4),
                               "vernacular_first_x_pt": round(vern["first_line_x"], 4),
                               "vernacular_continuation_x_pt": round(vern["continuation_x"], 4),
                               "foreign_first_x_pt": round(foreign["first_line_x"], 4),
                               "foreign_continuation_x_pt": round(foreign["continuation_x"], 4),
                           },
                           "pdftotext -bbox-layout", tolerance=float(horizontal_tolerance)))

    rule = rules["summary.alignment"]
    expected_alignment = rule["values"]["alignment"]
    if expected_alignment != "justified":
        fail(f"unsupported summary alignment: {expected_alignment!r}")
    actual = vern["justified"] and foreign["justified"]
    evidence.append(record(rule["id"], "PASS" if actual else "FAIL", expected_alignment,
                           {
                               "vernacular": {
                                   "line_count": vern["body_line_count"],
                                   "max_left_delta_pt": round(max(vern["left_deltas"]), 4),
                                   "max_non_final_right_delta_pt": round(max(vern["right_deltas"]), 4),
                               },
                               "foreign": {
                                   "line_count": foreign["body_line_count"],
                                   "max_left_delta_pt": round(max(foreign["left_deltas"]), 4),
                                   "max_non_final_right_delta_pt": round(max(foreign["right_deltas"]), 4),
                               },
                           },
                           "pdftotext -bbox-layout", tolerance=float(horizontal_tolerance)))

    counts = Counter(item["status"] for item in evidence)
    findings = [item["rule_id"] for item in evidence if item["status"] == "FAIL"]
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "scope": "summary-abstract-keywords",
        "mode": "enforce" if args.enforce else "audit",
        "source_commit_sha": args.commit_sha,
        "fixture": scenario["fixture"],
        "pdf": pdf.name,
        "status_counts": dict(sorted(counts.items())),
        "findings": findings,
        "measurement": {
            "vernacular_page": vern["page"],
            "foreign_page": foreign["page"],
            "calibration_page": calibration_pages[0],
            "vernacular_body_lines": vern["body_line_count"],
            "foreign_body_lines": foreign["body_line_count"],
        },
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "N6-EVIDENCE summary-abstract-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        + f" vernacular_page={vern['page']} foreign_page={foreign['page']}"
        + f" words={vern['word_count']}/{foreign['word_count']}"
    )
    for item in evidence:
        print(
            f"N6-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if args.enforce and findings:
        fail("enforcement requested with unresolved summary findings")


if __name__ == "__main__":
    try:
        main()
    except (PDFMeasurementError, KeyError, TypeError, ValueError) as exc:
        fail(str(exc))
