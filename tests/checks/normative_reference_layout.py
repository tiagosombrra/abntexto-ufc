#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize, typography_runs

SCENARIO = ROOT / "standards" / "reference-layout-scenario.json"
LOCATOR = ROOT / "standards" / "locator-audit-references.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"

RULE_ORDER = [
    "references.font.size",
    "references.line-spacing",
    "references.alignment",
    "references.entry-spacing",
]
LINE_CLUSTER_TOLERANCE_PT = 2.5


def fail(message: str) -> None:
    raise SystemExit(f"reference layout validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def ruleset(document: dict[str, Any], ruleset_id: str) -> dict[str, Any]:
    matches = [
        item
        for item in document.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == ruleset_id
    ]
    if len(matches) != 1:
        fail(f"locator ruleset {ruleset_id}: expected one match, found {len(matches)}")
    return matches[0]


def token(text: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", normalize(text))


def unique_word(pages: list[Any], marker: str) -> tuple[Any, Any]:
    wanted = token(marker)
    matches = [
        (page, word)
        for page in pages
        for word in page.words
        if token(word.text) == wanted
    ]
    if len(matches) != 1:
        fail(
            f"marker {marker!r}: expected one word, "
            f"found {[(page.index, word.text) for page, word in matches]}"
        )
    return matches[0]


def marker_runs(runs: list[Any], marker: str) -> list[Any]:
    wanted = normalize(marker)
    matches = [run for run in runs if wanted in normalize(run.text)]
    if not matches:
        fail(f"typography marker {marker!r}: no matching run")
    return matches


def cluster_lines(words: list[Any]) -> list[dict[str, Any]]:
    ordered = sorted(words, key=lambda word: (word.box.center_y, word.box.x_min))
    clusters: list[list[Any]] = []
    centers: list[float] = []
    for word in ordered:
        if not clusters or abs(word.box.center_y - centers[-1]) > LINE_CLUSTER_TOLERANCE_PT:
            clusters.append([word])
            centers.append(word.box.center_y)
            continue
        clusters[-1].append(word)
        centers[-1] = sum(item.box.center_y for item in clusters[-1]) / len(clusters[-1])

    result: list[dict[str, Any]] = []
    for cluster in clusters:
        cluster.sort(key=lambda word: word.box.x_min)
        result.append(
            {
                "center_y": sum(word.box.center_y for word in cluster) / len(cluster),
                "x_min": min(word.box.x_min for word in cluster),
                "x_max": max(word.box.x_max for word in cluster),
                "text": " ".join(word.text for word in cluster),
            }
        )
    return result


def line_at(page: Any, center_y: float) -> dict[str, Any]:
    words = [
        word
        for word in page.words
        if abs(word.box.center_y - center_y) <= LINE_CLUSTER_TOLERANCE_PT
    ]
    lines = cluster_lines(words)
    if len(lines) != 1:
        fail(f"expected one line around y={center_y:.4f}, found {len(lines)}")
    return lines[0]


def evidence_record(
    rule_id: str,
    passed: bool,
    expected: Any,
    measured: Any,
    tool: str,
    tolerance: float | None = None,
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": "PASS" if passed else "FAIL",
        "expected": expected,
        "measured": measured,
        "tool": tool,
        "tolerance": tolerance,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure bounded reference layout evidence.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locator = load_json(LOCATOR)
    policy = load_json(VALIDATION_POLICY)

    if (
        scenario.get("schema_version") != 1

        or scenario.get("component") != "reference-layout"
        or scenario.get("rules") != RULE_ORDER
        or scenario.get("locator_ruleset") != "references.layout"
    ):
        fail("invalid scenario schema/phase/component/scope")

    locator_scope = ruleset(locator, "references.layout").get("rule_ids")
    if locator_scope != RULE_ORDER:
        fail(f"references.layout locator scope drift: {locator_scope}")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    missing = [rule_id for rule_id in RULE_ORDER if rule_id not in rules]
    if missing:
        fail("contract rules missing: " + ", ".join(missing))

    font_expected = float(rules["references.font.size"]["values"]["font_pt"])
    spacing_expected = float(rules["references.line-spacing"]["values"]["line_spacing"])
    alignment_expected = rules["references.alignment"]["values"]["alignment"]
    blank_lines_expected = int(
        rules["references.entry-spacing"]["values"]["blank_lines_between"]
    )
    if (
        font_expected != 12.0
        or spacing_expected != 1.0
        or alignment_expected != "left"
        or blank_lines_expected != 1
    ):
        fail("reference layout contract values drifted")

    tolerances = policy.get("tolerances", {})
    try:
        font_tolerance = float(tolerances["font_size_pt"])
        horizontal_tolerance = float(tolerances["horizontal_position_pt"])
        vertical_tolerance = float(tolerances["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid validation tolerances: {exc}")

    markers = scenario.get("markers")
    required_markers = {
        "margin_control",
        "calibration_alpha",
        "calibration_beta",
        "entry_alpha",
        "entry_beta",
    }
    if not isinstance(markers, dict) or set(markers) != required_markers:
        fail("invalid marker specification")
    if not all(isinstance(value, str) and value for value in markers.values()):
        fail("all markers must be non-empty strings")

    try:
        pages = bbox_pages(args.pdf)
        runs = typography_runs(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    margin_page, margin_word = unique_word(pages, markers["margin_control"])
    cal_page_a, cal_word_a = unique_word(pages, markers["calibration_alpha"])
    cal_page_b, cal_word_b = unique_word(pages, markers["calibration_beta"])
    alpha_page, alpha_word = unique_word(pages, markers["entry_alpha"])
    beta_page, beta_word = unique_word(pages, markers["entry_beta"])

    if cal_page_a.index != cal_page_b.index or margin_page.index != cal_page_a.index:
        fail("margin and spacing calibration markers must share one page")
    if alpha_page.index != beta_page.index:
        fail("reference entries must share one page in the isolated fixture")
    if alpha_page.index == cal_page_a.index:
        fail("references must be isolated from calibration content on a separate page")
    if beta_word.box.center_y <= alpha_word.box.center_y:
        fail("reference entry order is not alpha then beta")

    calibration_gap = cal_word_b.box.center_y - cal_word_a.box.center_y
    if calibration_gap <= 0:
        fail(f"invalid single-spacing calibration gap: {calibration_gap}")

    alpha_words = [
        word
        for word in alpha_page.words
        if word.box.center_y >= alpha_word.box.center_y - LINE_CLUSTER_TOLERANCE_PT
        and word.box.center_y < beta_word.box.center_y - LINE_CLUSTER_TOLERANCE_PT
    ]
    alpha_lines = cluster_lines(alpha_words)
    if len(alpha_lines) < 2:
        fail(f"first reference must span at least two lines, got {len(alpha_lines)}")

    internal_gaps = [
        alpha_lines[index + 1]["center_y"] - alpha_lines[index]["center_y"]
        for index in range(len(alpha_lines) - 1)
    ]
    if any(gap <= 0 for gap in internal_gaps):
        fail(f"invalid internal reference gaps: {internal_gaps}")
    expected_internal_gap = calibration_gap * spacing_expected
    internal_deltas = [abs(gap - expected_internal_gap) for gap in internal_gaps]

    beta_line = line_at(alpha_page, beta_word.box.center_y)
    alpha_first_line = alpha_lines[0]
    alpha_last_line = alpha_lines[-1]
    entry_gap = beta_line["center_y"] - alpha_last_line["center_y"]
    expected_entry_gap = calibration_gap * (1 + blank_lines_expected)
    entry_gap_delta = abs(entry_gap - expected_entry_gap)
    if entry_gap <= 0:
        fail(f"invalid inter-entry gap: {entry_gap}")

    alignment_samples = [
        (markers["entry_alpha"], alpha_first_line["x_min"]),
        (markers["entry_beta"], beta_line["x_min"]),
    ]
    alignment_deltas = [
        abs(x_min - margin_word.box.x_min) for _, x_min in alignment_samples
    ]

    alpha_runs = marker_runs(runs, markers["entry_alpha"])
    beta_runs = marker_runs(runs, markers["entry_beta"])
    font_samples = [
        (markers["entry_alpha"], run) for run in alpha_runs
    ] + [
        (markers["entry_beta"], run) for run in beta_runs
    ]
    font_deltas = [abs(run.font_size - font_expected) for _, run in font_samples]

    evidence = [
        evidence_record(
            "references.font.size",
            all(delta <= font_tolerance for delta in font_deltas),
            rules["references.font.size"]["values"],
            {
                "samples": [
                    {
                        "marker": marker,
                        "page": run.page,
                        "font_pt": round(run.font_size, 4),
                        "delta_pt": round(delta, 4),
                        "family_observation": run.family,
                    }
                    for (marker, run), delta in zip(font_samples, font_deltas)
                ]
            },
            "pdftohtml -xml -zoom 1.0",
            font_tolerance,
        ),
        evidence_record(
            "references.line-spacing",
            all(delta <= vertical_tolerance for delta in internal_deltas),
            rules["references.line-spacing"]["values"],
            {
                "page": alpha_page.index,
                "first_entry_line_count": len(alpha_lines),
                "internal_line_gaps_pt": [round(value, 4) for value in internal_gaps],
                "single_spacing_calibration_gap_pt": round(calibration_gap, 4),
                "expected_internal_gap_pt": round(expected_internal_gap, 4),
                "gap_deltas_pt": [round(value, 4) for value in internal_deltas],
                "same_document_12pt_single_spacing_calibration": True,
            },
            "pdftotext -bbox-layout",
            vertical_tolerance,
        ),
        evidence_record(
            "references.alignment",
            all(delta <= horizontal_tolerance for delta in alignment_deltas),
            rules["references.alignment"]["values"],
            {
                "page": alpha_page.index,
                "margin_control_x_min_pt": round(margin_word.box.x_min, 4),
                "entry_starts": [
                    {
                        "marker": marker,
                        "x_min_pt": round(x_min, 4),
                        "delta_pt": round(delta, 4),
                    }
                    for (marker, x_min), delta in zip(
                        alignment_samples, alignment_deltas
                    )
                ],
                "continuation_line_x_min_pt_observation": [
                    round(line["x_min"], 4) for line in alpha_lines[1:]
                ],
                "continuation_alignment_is_observational": True,
            },
            "pdftotext -bbox-layout",
            horizontal_tolerance,
        ),
        evidence_record(
            "references.entry-spacing",
            entry_gap_delta <= vertical_tolerance,
            rules["references.entry-spacing"]["values"],
            {
                "page": alpha_page.index,
                "last_line_first_entry_center_y_pt": round(alpha_last_line["center_y"], 4),
                "first_line_second_entry_center_y_pt": round(beta_line["center_y"], 4),
                "measured_entry_gap_pt": round(entry_gap, 4),
                "single_spacing_calibration_gap_pt": round(calibration_gap, 4),
                "expected_entry_gap_pt": round(expected_entry_gap, 4),
                "delta_pt": round(entry_gap_delta, 4),
                "blank_lines_between": blank_lines_expected,
                "same_document_calibration": True,
            },
            "pdftotext -bbox-layout",
            vertical_tolerance,
        ),
    ]

    if [item["rule_id"] for item in evidence] != RULE_ORDER:
        fail("evidence order drift")

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "component": "reference-layout",
        "source_commit_sha": args.commit_sha,
        "fixture": "tests/documents/reference-layout-test.tex",
        "bibliography_fixture": "tests/fixtures/reference-layout.bib",
        "result": result,
        "status_counts": status_counts,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "VALIDATION-EVIDENCE reference-layout-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" internal_gap_pt={sum(internal_gaps) / len(internal_gaps):.4f}"
        + f" calibration_gap_pt={calibration_gap:.4f}"
        + f" entry_gap_pt={entry_gap:.4f}"
    )
    for item in evidence:
        print(
            f"VALIDATION-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    failed = [item["rule_id"] for item in evidence if item["status"] != "PASS"]
    if failed:
        fail("measurement predicates failed: " + ", ".join(failed))


if __name__ == "__main__":
    main()
