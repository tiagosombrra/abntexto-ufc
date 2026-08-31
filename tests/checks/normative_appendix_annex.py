#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, normalize, typography_runs

SCENARIO = ROOT / "standards" / "appendix-annex-final-pdf-scenario.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
PT_PER_MM = 72.0 / 25.4
DASH_CHARS = "-‐‑‒–—―"


def fail(message: str) -> None:
    raise SystemExit(f"N10 appendix/annex validation failed: {message}")


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


def page_index_for_marker(page_nodes: list[ET.Element], marker: str) -> int:
    wanted = normalize(marker)
    matches: list[int] = []
    for index, page in enumerate(page_nodes, start=1):
        if any(normalize(word_text(word)) == wanted for word in words(page)):
            matches.append(index)
    if len(matches) != 1:
        fail(f"marker {marker}: expected one page, found {len(matches)}")
    return matches[0]


def heading_line(page: ET.Element, keyword: str, title_marker: str) -> ET.Element:
    key = normalize(keyword)
    title = normalize(title_marker)
    matches = [
        line
        for line in lines(page)
        if key in normalize(line_text(line)) and title in normalize(line_text(line))
    ]
    if len(matches) != 1:
        fail(
            f"heading {keyword}/{title_marker}: expected one line, found {len(matches)}"
        )
    return matches[0]


def line_center_x(line: ET.Element) -> float:
    try:
        return (float(line.attrib["xMin"]) + float(line.attrib["xMax"])) / 2.0
    except (KeyError, ValueError) as exc:
        fail(f"invalid line bounds: {line.attrib}")
        raise AssertionError from exc


def typography_containing(runs: list[Any], page: int, marker: str) -> Any:
    wanted = normalize(marker)
    matches = [
        run
        for run in runs
        if run.page == page and wanted in normalize(run.text)
    ]
    if len(matches) != 1:
        raise PDFMeasurementError(
            f"typography marker {marker}: expected one run on page {page}, "
            f"found {len(matches)}"
        )
    return matches[0]


def record(rule_id: str, status: str, expected: Any, measured: Any, tool: str) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": tool,
    }


def expected_values(rules: dict[str, dict[str, Any]], rule_id: str, supported: dict[str, Any]) -> dict[str, Any]:
    values = rules[rule_id].get("values")
    if values != supported:
        fail(f"unsupported contract drift for {rule_id}: {values!r}")
    return values


def uppercase_text(value: str) -> bool:
    letters = [char for char in value if char.isalpha()]
    return bool(letters) and all(char == char.upper() for char in letters)


def pattern_measurement(raw: str, keyword: str, letter: str, title: str) -> dict[str, Any]:
    compact = re.sub(r"\s+", " ", raw).strip()
    normalized = normalize(compact)
    pattern = re.compile(
        rf"^{normalize(keyword)}\s+([A-Z])\s*([{re.escape(DASH_CHARS)}])\s*{normalize(title)}$"
    )
    match = pattern.fullmatch(normalized)
    return {
        "line": compact,
        "matched": match is not None,
        "expected_letter": letter,
        "observed_letter": None if match is None else match.group(1),
        "observed_dash": None if match is None else match.group(2),
        "exact_dash_glyph_not_frozen": True,
    }


def page_has_number(page: ET.Element, number: int) -> bool:
    wanted = str(number)
    return any(word_text(word).strip() == wanted for word in words(page))


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure N10 appendix/annex final-PDF evidence.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    if not pdf.is_file():
        fail(f"PDF not found: {pdf}")

    scenario = load_json(SCENARIO, "scenario")
    validation = load_json(VALIDATION_POLICY, "validation policy")
    if scenario.get("schema_version") != 1 or scenario.get("phase") != "N10":
        fail("invalid scenario schema/phase")
    if validation.get("schema_version") != 2:
        fail("invalid validation policy schema/phase")

    scenario_rules = scenario.get("rules")
    if not isinstance(scenario_rules, list) or len(scenario_rules) != 13:
        fail("scenario rule scope is invalid")

    rules = {rule["id"]: rule for rule in load_full_contract()["rules"]}
    missing = sorted(set(scenario_rules) - set(rules))
    if missing:
        fail("campaign rules missing from full contract: " + ", ".join(missing))

    supported = {
        "appendix.page.own": {"new_page": True},
        "appendix.heading.case": {"uppercase": True},
        "appendix.heading.weight": {"bold": True},
        "appendix.heading.font-size": {"font_pt": 12},
        "appendix.heading.alignment": {"centered": True},
        "annex.page.own": {"new_page": True},
        "annex.heading.case": {"uppercase": True},
        "annex.heading.weight": {"bold": True},
        "annex.heading.font-size": {"font_pt": 12},
        "annex.heading.alignment": {"centered": True},
        "appendix.identification.pattern": {"pattern": ["APÊNDICE", "letter", "dash", "title"]},
        "annex.identification.pattern": {"pattern": ["ANEXO", "letter", "dash", "title"]},
        "pagination.appendix-annex.continuous": {"continuous": True},
    }
    if set(scenario_rules) != set(supported):
        fail("scenario rules drifted from the supported full-contract scope")

    for rule_id, value in supported.items():
        expected_values(rules, rule_id, value)

    horizontal_tolerance = float(validation["tolerances"]["horizontal_position_pt"])
    font_tolerance = float(validation["tolerances"]["font_size_pt"])
    left_mm = float(rules["margin.recto.left"]["values"]["left_mm"])
    right_mm = float(rules["margin.recto.right"]["values"]["right_mm"])

    root = bbox_root(pdf)
    page_nodes = pages(root)
    typo = typography_runs(pdf)

    text_marker = scenario["page_control"]["text_marker"]
    text_page = page_index_for_marker(page_nodes, text_marker)
    logical_start = int(scenario["page_control"]["logical_start"])
    regular = typography_containing(
        typo, text_page, scenario["font_weight_calibration"]["regular"]
    )
    bold = typography_containing(
        typo, text_page, scenario["font_weight_calibration"]["bold"]
    )
    if regular.font_id == bold.font_id:
        fail("regular/bold calibration did not produce distinct font ids")

    samples: dict[str, list[dict[str, Any]]] = {"appendix": [], "annex": []}
    ordered_pages: list[dict[str, Any]] = [
        {"kind": "text", "page": text_page, "marker": text_marker}
    ]

    for kind, keyword, items in (
        ("appendix", "APÊNDICE", scenario["appendices"]),
        ("annex", "ANEXO", scenario["annexes"]),
    ):
        for item in items:
            body_page = page_index_for_marker(page_nodes, item["body_marker"])
            page = page_nodes[body_page - 1]
            heading = heading_line(page, keyword, item["rendered_title"])
            raw_heading = line_text(heading)
            heading_type = typography_containing(
                typo, body_page, item["rendered_title"]
            )
            page_width = float(page.attrib["width"])
            text_center = (
                left_mm * PT_PER_MM
                + (page_width - right_mm * PT_PER_MM)
            ) / 2.0
            center = line_center_x(heading)
            pattern = pattern_measurement(
                raw_heading, keyword, item["letter"], item["rendered_title"]
            )
            sample = {
                "letter": item["letter"],
                "source_title": item["source_title"],
                "rendered_title": item["rendered_title"],
                "body_marker": item["body_marker"],
                "physical_page": body_page,
                "heading": raw_heading,
                "uppercase": uppercase_text(raw_heading),
                "font_id": heading_type.font_id,
                "font_pt": heading_type.font_size,
                "font_delta_pt": abs(heading_type.font_size - 12.0),
                "matches_bold_calibration": heading_type.font_id == bold.font_id,
                "differs_from_regular_calibration": heading_type.font_id != regular.font_id,
                "heading_center_pt": center,
                "text_area_center_pt": text_center,
                "center_delta_pt": abs(center - text_center),
                "pattern": pattern,
            }
            samples[kind].append(sample)
            ordered_pages.append(
                {"kind": kind, "page": body_page, "marker": item["body_marker"]}
            )

    appendix_samples = samples["appendix"]
    annex_samples = samples["annex"]
    evidence: list[dict[str, Any]] = []

    def own_page(kind_samples: list[dict[str, Any]], prior_page: int) -> tuple[bool, list[dict[str, Any]]]:
        checks: list[dict[str, Any]] = []
        previous = prior_page
        passed = True
        for sample in kind_samples:
            current = int(sample["physical_page"])
            starts_new = current > previous
            checks.append(
                {
                    "physical_page": current,
                    "previous_element_page": previous,
                    "physical_page_delta": current - previous,
                    "physical_page_delta_is_observational": True,
                    "starts_new_page": starts_new,
                }
            )
            passed = passed and starts_new
            previous = current
        return passed, checks

    appendix_page_pass, appendix_page_checks = own_page(appendix_samples, text_page)
    annex_page_pass, annex_page_checks = own_page(
        annex_samples, int(appendix_samples[-1]["physical_page"])
    )
    evidence.append(record(
        "appendix.page.own",
        "PASS" if appendix_page_pass else "FAIL",
        supported["appendix.page.own"],
        {"samples": appendix_page_checks},
        "pdftotext -bbox-layout",
    ))
    evidence.append(record(
        "appendix.heading.case",
        "PASS" if all(item["uppercase"] for item in appendix_samples) else "FAIL",
        supported["appendix.heading.case"],
        {"samples": [{"heading": item["heading"], "uppercase": item["uppercase"]} for item in appendix_samples]},
        "pdftotext -bbox-layout",
    ))
    evidence.append(record(
        "appendix.heading.weight",
        "PASS" if all(item["matches_bold_calibration"] and item["differs_from_regular_calibration"] for item in appendix_samples) else "FAIL",
        supported["appendix.heading.weight"],
        {
            "regular_calibration_font_id": regular.font_id,
            "bold_calibration_font_id": bold.font_id,
            "samples": [
                {
                    "font_id": item["font_id"],
                    "matches_bold_calibration": item["matches_bold_calibration"],
                    "differs_from_regular_calibration": item["differs_from_regular_calibration"],
                }
                for item in appendix_samples
            ],
        },
        "pdftohtml -xml -zoom 1.0",
    ))
    evidence.append(record(
        "appendix.heading.font-size",
        "PASS" if all(item["font_delta_pt"] <= font_tolerance for item in appendix_samples) else "FAIL",
        supported["appendix.heading.font-size"],
        {"tolerance_pt": font_tolerance, "samples": [{"font_pt": item["font_pt"], "delta_pt": item["font_delta_pt"]} for item in appendix_samples]},
        "pdftohtml -xml -zoom 1.0",
    ))
    evidence.append(record(
        "appendix.heading.alignment",
        "PASS" if all(item["center_delta_pt"] <= horizontal_tolerance for item in appendix_samples) else "FAIL",
        supported["appendix.heading.alignment"],
        {"tolerance_pt": horizontal_tolerance, "samples": [{"heading_center_pt": item["heading_center_pt"], "text_area_center_pt": item["text_area_center_pt"], "delta_pt": item["center_delta_pt"]} for item in appendix_samples]},
        "pdftotext -bbox-layout",
    ))

    evidence.append(record(
        "annex.page.own",
        "PASS" if annex_page_pass else "FAIL",
        supported["annex.page.own"],
        {"samples": annex_page_checks},
        "pdftotext -bbox-layout",
    ))
    evidence.append(record(
        "annex.heading.case",
        "PASS" if all(item["uppercase"] for item in annex_samples) else "FAIL",
        supported["annex.heading.case"],
        {"samples": [{"heading": item["heading"], "uppercase": item["uppercase"]} for item in annex_samples]},
        "pdftotext -bbox-layout",
    ))
    evidence.append(record(
        "annex.heading.weight",
        "PASS" if all(item["matches_bold_calibration"] and item["differs_from_regular_calibration"] for item in annex_samples) else "FAIL",
        supported["annex.heading.weight"],
        {
            "regular_calibration_font_id": regular.font_id,
            "bold_calibration_font_id": bold.font_id,
            "samples": [
                {
                    "font_id": item["font_id"],
                    "matches_bold_calibration": item["matches_bold_calibration"],
                    "differs_from_regular_calibration": item["differs_from_regular_calibration"],
                }
                for item in annex_samples
            ],
        },
        "pdftohtml -xml -zoom 1.0",
    ))
    evidence.append(record(
        "annex.heading.font-size",
        "PASS" if all(item["font_delta_pt"] <= font_tolerance for item in annex_samples) else "FAIL",
        supported["annex.heading.font-size"],
        {"tolerance_pt": font_tolerance, "samples": [{"font_pt": item["font_pt"], "delta_pt": item["font_delta_pt"]} for item in annex_samples]},
        "pdftohtml -xml -zoom 1.0",
    ))
    evidence.append(record(
        "annex.heading.alignment",
        "PASS" if all(item["center_delta_pt"] <= horizontal_tolerance for item in annex_samples) else "FAIL",
        supported["annex.heading.alignment"],
        {"tolerance_pt": horizontal_tolerance, "samples": [{"heading_center_pt": item["heading_center_pt"], "text_area_center_pt": item["text_area_center_pt"], "delta_pt": item["center_delta_pt"]} for item in annex_samples]},
        "pdftotext -bbox-layout",
    ))

    appendix_pattern_pass = (
        [item["pattern"]["observed_letter"] for item in appendix_samples] == ["A", "B"]
        and all(item["pattern"]["matched"] for item in appendix_samples)
    )
    annex_pattern_pass = (
        [item["pattern"]["observed_letter"] for item in annex_samples] == ["A", "B"]
        and all(item["pattern"]["matched"] for item in annex_samples)
    )
    evidence.append(record(
        "appendix.identification.pattern",
        "PASS" if appendix_pattern_pass else "FAIL",
        supported["appendix.identification.pattern"],
        {"samples": [item["pattern"] for item in appendix_samples], "consecutive_letters": ["A", "B"]},
        "pdftotext -bbox-layout",
    ))
    evidence.append(record(
        "annex.identification.pattern",
        "PASS" if annex_pattern_pass else "FAIL",
        supported["annex.identification.pattern"],
        {"samples": [item["pattern"] for item in annex_samples], "consecutive_letters": ["A", "B"]},
        "pdftotext -bbox-layout",
    ))

    continuity_samples: list[dict[str, Any]] = []
    continuity_pass = True
    for item in ordered_pages:
        physical = int(item["page"])
        expected_logical = logical_start + (physical - text_page)
        present = page_has_number(page_nodes[physical - 1], expected_logical)
        continuity_samples.append(
            {
                "kind": item["kind"],
                "physical_page": physical,
                "expected_logical_page": expected_logical,
                "visible_expected_number_present": present,
            }
        )
        continuity_pass = continuity_pass and present
    evidence.append(record(
        "pagination.appendix-annex.continuous",
        "PASS" if continuity_pass else "FAIL",
        supported["pagination.appendix-annex.continuous"],
        {
            "fixture_logical_start": logical_start,
            "samples": continuity_samples,
            "physical_page_delta_is_observational": True,
            "no_reset_detected": continuity_pass,
        },
        "pdftotext -bbox-layout",
    ))

    if [item["rule_id"] for item in evidence] != scenario_rules:
        fail("evidence order does not match exact campaign rule order")

    counts = Counter(item["status"] for item in evidence)
    findings = [item["rule_id"] for item in evidence if item["status"] != "PASS"]
    baseline = len(scope.get("existing_bounded_positive", []))
    promoted = len(evidence) if not findings else sum(item["status"] == "PASS" for item in evidence)
    current = baseline + promoted
    remaining = int(scope["total_rules"]) - current
    payload = {
        "schema_version": 1,
        "phase": "N10",
        "campaign": "appendix-annex-final-pdf",
        "source_commit_sha": args.commit_sha,
        "fixture": scenario["fixture"],
        "rendered_engine": scenario["engine"],
        "engine_matrix_deferred_to": scenario["engine_matrix_deferred_to"],
        "status_counts": dict(sorted(counts.items())),
        "findings": findings,
        "evidence_policy": scenario["evidence_policy"],
        "bounded_progress": {
            "total": scope["total_rules"],
            "baseline_existing_bounded_positive": baseline,
            "promoted_bounded_positive": promoted,
            "current_bounded_positive": current,
            "current_support_only": remaining,
        },
        "evidence": evidence,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "N10-EVIDENCE appendix-annex-final-pdf-summary "
        f"PASS={counts.get('PASS', 0)} FAIL={counts.get('FAIL', 0)} "
        f"appendix_pages={','.join(str(item['physical_page']) for item in appendix_samples)} "
        f"annex_pages={','.join(str(item['physical_page']) for item in annex_samples)}"
    )
    for item in evidence:
        print(
            f"N10-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
    print(
        "N10-EVIDENCE bounded-progress "
        f"total={scope['total_rules']} baseline_existing_bounded_positive={baseline} "
        f"promoted_bounded_positive={promoted} current_bounded_positive={current} "
        f"current_support_only={remaining} proof_state_changed=false"
    )

    if findings:
        fail("campaign has unresolved findings: " + ", ".join(findings))


if __name__ == "__main__":
    try:
        main()
    except (PDFMeasurementError, KeyError, TypeError, ValueError) as exc:
        fail(str(exc))
