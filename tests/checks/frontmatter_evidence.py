#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import get_rule, load_catalog
from normative_full import load_full_contract
from pdf_measurement import (
    PDFMeasurementError,
    Page,
    Typography,
    Word,
    bbox_pages,
    normalize,
    typography_runs,
)

SCENARIOS = ROOT / "standards" / "frontmatter-scenarios.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
PT_PER_MM = 72.0 / 25.4
QUOTE_CHARS = {'"', '“', '”', '„', '«', '»'}


def fail(message: str) -> None:
    raise SystemExit(f"Front matter validation failed: {message}")


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {label}: {exc}")
    if not isinstance(data, dict):
        fail(f"{label} must be an object")
    return data


def full_rule_map() -> dict[str, dict[str, Any]]:
    contract = load_full_contract()
    return {rule["id"]: rule for rule in contract["rules"]}


def find_scenario_marker(pages: list[Page], marker: str) -> tuple[Page, Word]:
    wanted = normalize(marker)
    matches: list[tuple[Page, Word]] = []
    wrappers = "".join(QUOTE_CHARS)
    for page in pages:
        for word in page.words:
            if normalize(word.text.strip(wrappers)) == wanted:
                matches.append((page, word))
    if len(matches) != 1:
        raise PDFMeasurementError(
            f"marker {marker}: expected exactly one quote-tolerant word, found {len(matches)}"
        )
    return matches[0]


def marker_series(pages: list[Page], markers: list[str]) -> tuple[Page, list[Word]]:
    found = [find_scenario_marker(pages, marker) for marker in markers]
    page_indexes = {page.index for page, _ in found}
    if len(page_indexes) != 1:
        raise PDFMeasurementError(
            f"markers {markers} must be on one page, found pages {sorted(page_indexes)}"
        )
    return found[0][0], [word for _, word in found]


def average_vertical_gap(words: list[Word]) -> float:
    if len(words) < 2:
        raise PDFMeasurementError("at least two markers are required for spacing evidence")
    centers = [word.box.center_y for word in words]
    gaps = [centers[index + 1] - centers[index] for index in range(len(centers) - 1)]
    if any(gap <= 0 for gap in gaps):
        raise PDFMeasurementError(f"markers are not in top-to-bottom order: {centers}")
    return mean(gaps)


def typography_for_marker(runs: list[Typography], marker: str) -> Typography:
    wanted = normalize(marker)
    matches = [run for run in runs if wanted in normalize(run.text)]
    if len(matches) != 1:
        raise PDFMeasurementError(
            f"typography marker {marker}: expected one containing run, found {len(matches)}"
        )
    return matches[0]


def page_text(page: Page) -> str:
    return " ".join(word.text for word in page.words)


def record(
    rule_id: str,
    status: str,
    expected: Any,
    measured: Any,
    tool: str,
    *,
    tolerance: float | None = None,
    reason: str = "",
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": tool,
    }
    if tolerance is not None:
        result["tolerance"] = tolerance
    if reason:
        result["reason"] = reason
    return result


def close_status(actual: float, expected: float, tolerance: float) -> str:
    return "PASS" if abs(actual - expected) <= tolerance else "FAIL"


def boolean_status(actual: bool, expected: bool) -> str:
    return "PASS" if actual is expected else "FAIL"


def audit_scenario(
    scenario: dict[str, Any],
    pages: list[Page],
    typography: list[Typography],
    rules: dict[str, dict[str, Any]],
    margin_left_pt: float,
    validation_tolerances: dict[str, float],
    spacing_tolerance: float,
    calibration: dict[str, float],
) -> dict[str, Any]:
    markers = scenario["markers"]
    page, words = marker_series(pages, markers)
    first = words[0]
    first_type = typography_for_marker(typography, markers[0])
    component = scenario["component"]
    text = page_text(page)
    normalized_text = normalize(text)
    has_quotes = any(char in text for char in QUOTE_CHARS)
    gap = average_vertical_gap(words)

    evidence: list[dict[str, Any]] = []

    if component == "dedication":
        heading_rule = rules["dedication.heading.present"]
        expected_heading = bool(heading_rule["values"]["heading"])
        heading_present = "DEDICATORIA" in normalized_text
        evidence.append(
            record(
                "dedication.heading.present",
                boolean_status(heading_present, expected_heading),
                expected_heading,
                heading_present,
                "pdftotext -bbox-layout",
            )
        )
        position_id = "dedication.position.start"
        indent_id = "dedication.indent.left"
        font_id = "dedication.font.size"
        spacing_id = "dedication.line-spacing"
        spacing_reference = calibration["onehalf_12pt"]
    elif component == "epigraph-short":
        position_id = "epigraph.short.position.start"
        indent_id = "epigraph.short.indent.left"
        font_id = "epigraph.short.font.size"
        spacing_id = "epigraph.short.line-spacing"
        quote_id = "epigraph.short.quotation-marks"
        spacing_reference = calibration["onehalf_12pt"]
    elif component == "epigraph-long":
        position_id = "epigraph.long.position.start"
        indent_id = "epigraph.long.indent.left"
        font_id = "epigraph.long.font.size"
        spacing_id = "epigraph.long.line-spacing"
        quote_id = "epigraph.long.quotation-marks"
        spacing_reference = calibration["single_10pt"]
    else:
        fail(f"unsupported front matter component: {component}")

    position_rule = rules[position_id]
    below_midpoint = first.box.y_min >= page.height / 2.0 - validation_tolerances["vertical_position_pt"]
    evidence.append(
        record(
            position_id,
            "PASS" if below_midpoint else "FAIL",
            position_rule["values"]["start"],
            {
                "first_marker_y_pt": round(first.box.y_min, 4),
                "page_midpoint_y_pt": round(page.height / 2.0, 4),
            },
            "pdftotext -bbox-layout",
            tolerance=validation_tolerances["vertical_position_pt"],
        )
    )

    indent_rule = rules[indent_id]
    indent_mm = float(indent_rule["values"]["left_indent_mm"])
    expected_x = margin_left_pt + indent_mm * PT_PER_MM
    evidence.append(
        record(
            indent_id,
            close_status(first.box.x_min, expected_x, validation_tolerances["horizontal_position_pt"]),
            {"left_indent_mm": indent_mm, "physical_x_pt": round(expected_x, 4)},
            {"physical_x_pt": round(first.box.x_min, 4)},
            "pdftotext -bbox-layout",
            tolerance=validation_tolerances["horizontal_position_pt"],
        )
    )

    font_rule = rules[font_id]
    expected_font = float(font_rule["values"]["font_pt"])
    evidence.append(
        record(
            font_id,
            close_status(first_type.font_size, expected_font, validation_tolerances["font_size_pt"]),
            expected_font,
            round(first_type.font_size, 4),
            "pdftohtml -xml",
            tolerance=validation_tolerances["font_size_pt"],
        )
    )

    spacing_rule = rules[spacing_id]
    evidence.append(
        record(
            spacing_id,
            close_status(gap, spacing_reference, spacing_tolerance),
            {
                "contract": spacing_rule["values"]["line_spacing"],
                "calibrated_gap_pt": round(spacing_reference, 4),
            },
            {"average_marker_gap_pt": round(gap, 4)},
            "pdftotext -bbox-layout + same-document spacing calibration",
            tolerance=spacing_tolerance,
        )
    )

    if component.startswith("epigraph-"):
        quote_rule = rules[quote_id]
        expected_quotes = bool(quote_rule["values"]["quotation_marks"])
        evidence.append(
            record(
                quote_id,
                boolean_status(has_quotes, expected_quotes),
                expected_quotes,
                has_quotes,
                "pdftotext -bbox-layout page text",
            )
        )

    return {
        "scenario_id": scenario["id"],
        "component": component,
        "route": scenario["route"],
        "page": page.index,
        "line_count_expected": scenario["line_count"],
        "line_count_measured": len(words),
        "markers": markers,
        "average_marker_gap_pt": round(gap, 4),
        "page_isolated_from_other_target_scenarios": True,
        "evidence": evidence,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure front matter dedication and epigraph final-PDF evidence."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    if not pdf.is_file():
        fail(f"PDF not found: {pdf}")

    scenarios_data = load_json(SCENARIOS, "front matter scenarios")
    validation_policy = load_json(VALIDATION_POLICY, "validation policy")
    if scenarios_data.get("schema_version") != 2:
        fail("invalid front matter scenario schema")
    if validation_policy.get("schema_version") != 2:
        fail("invalid validation policy schema")

    scenarios = scenarios_data.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) != 3:
        fail("expected exactly three dedication/epigraph scenarios")

    spacing_tolerance = scenarios_data.get("tolerances", {}).get("line_spacing_pt")
    if not isinstance(spacing_tolerance, (int, float)) or spacing_tolerance <= 0:
        fail("line_spacing_pt tolerance must be positive")

    validation_tolerances = validation_policy.get("tolerances")
    if not isinstance(validation_tolerances, dict):
        fail("validation tolerances are missing")

    rules = full_rule_map()
    required_rule_ids = {rule_id for scenario in scenarios for rule_id in scenario["rules"]}
    missing_rules = sorted(required_rule_ids - set(rules))
    if missing_rules:
        fail("scenario rules missing from full contract: " + ", ".join(missing_rules))

    catalog = load_catalog()
    recto = get_rule(catalog, "margin.recto")
    margin_left_pt = float(recto["values"]["left_mm"]) * PT_PER_MM

    try:
        pages = bbox_pages(pdf)
        typography = typography_runs(pdf)
        calibration_data = scenarios_data["calibration"]
        _, half_words = marker_series(pages, calibration_data["onehalf_12pt"])
        _, single_words = marker_series(pages, calibration_data["single_10pt"])
        calibration = {
            "onehalf_12pt": average_vertical_gap(half_words),
            "single_10pt": average_vertical_gap(single_words),
        }
        results = [
            audit_scenario(
                scenario,
                pages,
                typography,
                rules,
                margin_left_pt,
                validation_tolerances,
                float(spacing_tolerance),
                calibration,
            )
            for scenario in scenarios
        ]
    except (PDFMeasurementError, KeyError, TypeError, ValueError) as exc:
        fail(str(exc))

    target_pages = [item["page"] for item in results]
    isolated = len(set(target_pages)) == len(target_pages)
    for item in results:
        item["page_isolated_from_other_target_scenarios"] = isolated

    all_evidence = [entry for result in results for entry in result["evidence"]]
    counts = Counter(entry["status"] for entry in all_evidence)
    findings = [
        entry["rule_id"]
        for entry in all_evidence
        if entry["status"] in {"FAIL", "UNASSESSED"}
    ]

    payload = {
        "schema_version": 1,
        "validation_scope": "frontmatter",
        "mode": "enforce" if args.enforce else "audit",
        "source_commit_sha": args.commit_sha,
        "fixture": scenarios_data["fixture"],
        "pdf": pdf.name,
        "calibration": {
            key: round(value, 4) for key, value in calibration.items()
        },
        "target_pages_are_distinct": isolated,
        "status_counts": dict(sorted(counts.items())),
        "findings": findings,
        "scenarios": results,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "Front matter validation audit: "
        f"rules={len(all_evidence)}, "
        + ", ".join(f"{status}={count}" for status, count in sorted(counts.items()))
        + f"; distinct-pages={isolated}."
    )
    if findings:
        print("Front matter findings: " + ", ".join(findings))

    if args.enforce and (findings or not isolated):
        fail("enforcement requested with unresolved front matter findings")


if __name__ == "__main__":
    main()
