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

SCENARIO = ROOT / "normativa" / "typography-scenario.json"
LOCATOR_TYPOGRAPHY = ROOT / "normativa" / "locator-audit-typography-paragraphs.json"
LOCATOR_FINAL = ROOT / "normativa" / "locator-audit-final.json"
EVIDENCE_REGISTRY = ROOT / "normativa" / "evidence-registry.json"
ORACLE_POLICY = ROOT / "normativa" / "oracle-policy.json"

RULE_ORDER = [
    "format.text.color",
    "font.family.body",
    "font.size.body",
    "spacing.body",
    "font.size.reduced.pagination",
]
DIRECT_RULES = [
    "format.text.color",
    "font.size.body",
    "spacing.body",
    "font.size.reduced.pagination",
]
BLACK = {"#000000", "black"}
HEADER_LIMIT_PT = 80.0


def fail(message: str) -> None:
    raise SystemExit(f"N7 typography oracle failed: {message}")


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


def unique_word(pages: list[Any], marker: str) -> tuple[Any, Any]:
    wanted = normalize(marker)
    matches = [
        (page, word)
        for page in pages
        for word in page.words
        if normalize(word.text) == wanted
    ]
    if len(matches) != 1:
        fail(
            f"marker {marker!r}: expected one word, "
            f"found {[(page.index, word.text) for page, word in matches]}"
        )
    return matches[0]


def unique_run(runs: list[Any], marker: str) -> Any:
    wanted = normalize(marker)
    matches = [run for run in runs if normalize(run.text) == wanted]
    if len(matches) != 1:
        fail(
            f"typography marker {marker!r}: expected one run, "
            f"found {[(run.page, run.text) for run in matches]}"
        )
    return matches[0]


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
    parser = argparse.ArgumentParser(description="Measure bounded N7 typography evidence.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locator_typography = load_json(LOCATOR_TYPOGRAPHY)
    locator_final = load_json(LOCATOR_FINAL)
    registry = load_json(EVIDENCE_REGISTRY)
    policy = load_json(ORACLE_POLICY)

    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N7"
        or scenario.get("component") != "typography"
        or scenario.get("rules") != RULE_ORDER
        or scenario.get("direct_pdf_rules") != DIRECT_RULES
    ):
        fail("invalid scenario schema/phase/component/scope")

    expected_locator_map = {
        "format.text.color": "format.text-color",
        "font.family.body": "typography.body",
        "font.size.body": "typography.body",
        "spacing.body": "layout.body-spacing",
        "font.size.reduced.pagination": "typography.reduced-font",
    }
    if scenario.get("locator_rulesets") != expected_locator_map:
        fail("scenario locator mapping drift")

    if ruleset(locator_final, "format.text-color").get("rule_ids") != ["format.text.color"]:
        fail("format.text-color locator scope drift")
    body_locator = ruleset(locator_typography, "typography.body").get("rule_ids")
    if body_locator != ["font.family.body", "font.size.body"]:
        fail(f"typography.body locator scope drift: {body_locator}")
    if ruleset(locator_typography, "layout.body-spacing").get("rule_ids") != ["spacing.body"]:
        fail("layout.body-spacing locator scope drift")
    reduced_locator = ruleset(locator_typography, "typography.reduced-font").get("rule_ids")
    if not isinstance(reduced_locator, list) or "font.size.reduced.pagination" not in reduced_locator:
        fail("pagination reduced-font locator disappeared")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    missing = [rule_id for rule_id in RULE_ORDER if rule_id not in rules]
    if missing:
        fail("contract rules missing: " + ", ".join(missing))

    color_expected = rules["format.text.color"]["values"]
    family_expected = rules["font.family.body"]["values"]
    body_size_expected = float(rules["font.size.body"]["values"]["pt"])
    spacing_expected = float(rules["spacing.body"]["values"]["factor"])
    pagination_size_expected = float(
        rules["font.size.reduced.pagination"]["values"]["pt"]
    )
    if (
        color_expected != {"text": "black", "other_colors_allowed_for": ["illustrations"]}
        or family_expected != {"allowed": ["Arial", "Times New Roman"]}
        or body_size_expected != 12.0
        or spacing_expected != 1.5
        or pagination_size_expected != 10.0
    ):
        fail("typography contract values drifted")

    tolerances = policy.get("tolerances", {})
    try:
        font_tolerance = float(tolerances["font_size_pt"])
        vertical_tolerance = float(tolerances["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid oracle tolerances: {exc}")

    baseline = scenario.get("literal_family_baseline")
    if not isinstance(baseline, dict):
        fail("literal_family_baseline is required")
    required_baseline_keys = {
        "commit_sha",
        "workflow_run_id",
        "build_job_id",
        "certification_job_id",
        "artifact_name",
        "artifact_digest",
        "result",
    }
    if set(baseline) != required_baseline_keys:
        fail(f"literal family baseline keys drifted: {sorted(baseline)}")
    if (
        not re.fullmatch(r"[0-9a-f]{40}", str(baseline["commit_sha"]))
        or not isinstance(baseline["workflow_run_id"], int)
        or not isinstance(baseline["build_job_id"], int)
        or not isinstance(baseline["certification_job_id"], int)
        or baseline["artifact_name"] != "v2-windows-literal-font-pdfs"
        or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(baseline["artifact_digest"]))
        or baseline["result"] != "PASS"
    ):
        fail("invalid literal family baseline evidence")

    registry_items = {
        item.get("id"): item
        for item in registry.get("evidence", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for evidence_id in ("font.literal", "windows-font-poc", "windows-font-pdfa"):
        if evidence_id not in registry_items:
            fail(f"registered literal-font evidence disappeared: {evidence_id}")

    markers = scenario.get("markers")
    required_markers = {
        "body_alpha",
        "body_beta",
        "body_gamma",
        "body_delta",
        "calibration_alpha",
        "calibration_beta",
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
    if len(pages) != 2:
        fail(f"typography fixture must contain two pages, got {len(pages)}")

    evidence: list[dict[str, Any]] = []

    non_black = [
        {
            "page": run.page,
            "text": run.text,
            "color": run.color,
        }
        for run in runs
        if run.color.strip().lower() not in BLACK
    ]
    evidence.append(
        evidence_record(
            "format.text.color",
            not non_black,
            color_expected,
            {
                "typography_run_count": len(runs),
                "non_black_runs": non_black,
                "all_fixture_text_runs_black": not non_black,
            },
            "pdftohtml -xml -zoom 1.0",
        )
    )

    evidence.append(
        evidence_record(
            "font.family.body",
            True,
            family_expected,
            {
                "baseline_commit_sha": baseline["commit_sha"],
                "workflow_run_id": baseline["workflow_run_id"],
                "build_job_id": baseline["build_job_id"],
                "certification_job_id": baseline["certification_job_id"],
                "artifact_name": baseline["artifact_name"],
                "artifact_digest": baseline["artifact_digest"],
                "certifies": [
                    "Times New Roman literal identity",
                    "Arial literal identity",
                    "pdfLaTeX",
                    "LuaLaTeX",
                    "no TeX Gyre or Nimbus textual fallback",
                    "Unicode extraction",
                    "font embedding",
                    "PDF/A-2b",
                ],
                "portable_fixture_family_is_not_used_as_literal-family-proof": True,
            },
            "GitHub Actions Windows literal-font certification baseline",
        )
    )

    body_markers = [
        markers["body_alpha"],
        markers["body_beta"],
        markers["body_gamma"],
        markers["body_delta"],
    ]
    body_runs = [unique_run(runs, marker) for marker in body_markers]
    body_deltas = [abs(run.font_size - body_size_expected) for run in body_runs]
    evidence.append(
        evidence_record(
            "font.size.body",
            all(delta <= font_tolerance for delta in body_deltas),
            rules["font.size.body"]["values"],
            {
                "samples": [
                    {
                        "marker": marker,
                        "page": run.page,
                        "font_pt": round(run.font_size, 4),
                        "delta_pt": round(delta, 4),
                        "family_observation": run.family,
                    }
                    for marker, run, delta in zip(body_markers, body_runs, body_deltas)
                ]
            },
            "pdftohtml -xml -zoom 1.0",
            font_tolerance,
        )
    )

    body_words = [
        unique_word(pages, markers[key])[1]
        for key in ("body_alpha", "body_beta", "body_gamma")
    ]
    body_pages = [unique_word(pages, markers[key])[0].index for key in ("body_alpha", "body_beta", "body_gamma")]
    if len(set(body_pages)) != 1:
        fail(f"body spacing markers must share one page: {body_pages}")
    body_gaps = [
        body_words[index + 1].box.center_y - body_words[index].box.center_y
        for index in range(len(body_words) - 1)
    ]
    cal_page_a, cal_word_a = unique_word(pages, markers["calibration_alpha"])
    cal_page_b, cal_word_b = unique_word(pages, markers["calibration_beta"])
    if cal_page_a.index != cal_page_b.index:
        fail("spacing calibration markers must share one page")
    calibration_gap = cal_word_b.box.center_y - cal_word_a.box.center_y
    if calibration_gap <= 0 or any(gap <= 0 for gap in body_gaps):
        fail(f"invalid spacing gaps: body={body_gaps}, calibration={calibration_gap}")
    expected_body_gap = calibration_gap * spacing_expected
    spacing_deltas = [abs(gap - expected_body_gap) for gap in body_gaps]
    evidence.append(
        evidence_record(
            "spacing.body",
            all(delta <= vertical_tolerance for delta in spacing_deltas),
            rules["spacing.body"]["values"],
            {
                "page": body_pages[0],
                "body_line_gaps_pt": [round(value, 4) for value in body_gaps],
                "single_spacing_calibration_gap_pt": round(calibration_gap, 4),
                "expected_1_5_gap_pt": round(expected_body_gap, 4),
                "gap_deltas_pt": [round(value, 4) for value in spacing_deltas],
                "same_document_12pt_single_spacing_calibration": True,
            },
            "pdftotext -bbox-layout",
            vertical_tolerance,
        )
    )

    pagination_runs: list[Any] = []
    pagination_by_page: dict[int, list[Any]] = {}
    for page in pages:
        matches = [
            run
            for run in runs
            if run.page == page.index
            and run.box.y_min < HEADER_LIMIT_PT
            and re.fullmatch(r"[0-9]+", run.text.strip())
        ]
        pagination_by_page[page.index] = matches
        if len(matches) != 1:
            fail(
                f"page {page.index}: expected one Arabic header number run, "
                f"found {[(run.text, run.font_size) for run in matches]}"
            )
        pagination_runs.extend(matches)
    pagination_deltas = [
        abs(run.font_size - pagination_size_expected) for run in pagination_runs
    ]
    evidence.append(
        evidence_record(
            "font.size.reduced.pagination",
            all(delta <= font_tolerance for delta in pagination_deltas),
            {"pt": pagination_size_expected},
            {
                "samples": [
                    {
                        "page": run.page,
                        "text": run.text,
                        "font_pt": round(run.font_size, 4),
                        "delta_pt": round(delta, 4),
                        "family_observation": run.family,
                        "color": run.color,
                    }
                    for run, delta in zip(pagination_runs, pagination_deltas)
                ]
            },
            "pdftohtml -xml -zoom 1.0",
            font_tolerance,
        )
    )

    if [item["rule_id"] for item in evidence] != RULE_ORDER:
        fail("evidence order drift")
    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N7",
        "component": "typography",
        "source_commit_sha": args.commit_sha,
        "fixture": "tests/normativa/textual-oracle-typography.tex",
        "result": result,
        "status_counts": status_counts,
        "literal_family_baseline": baseline,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "N7-EVIDENCE typography-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" body_gaps={','.join(f'{value:.4f}' for value in body_gaps)}"
        + f" calibration_gap={calibration_gap:.4f}"
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
