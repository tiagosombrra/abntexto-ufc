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

SCENARIO = ROOT / "standards" / "frontmatter-toc-scenario.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-policy.json"
RULE_ORDER = [
    "toc.frontmatter-exclusion",
    "toc.heading.alignment",
    "toc.heading.case",
    "toc.page-number.position",
    "toc.section-hierarchy.mirror",
]
NON_NORMATIVE_RULE_ORDER = ["toc.leaders.dotted.project"]
LEVEL_ORDER = ["section", "subsection", "subsubsection", "paragraph", "subparagraph"]


def fail(message: str) -> None:
    raise SystemExit(f"TOC validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def page_text(page: Any) -> str:
    return " ".join(word.text for word in page.words)


def word_matches(pages: list[Any], marker: str) -> list[tuple[Any, Any]]:
    wanted = normalize(marker)
    return [
        (page, word)
        for page in pages
        for word in page.words
        if normalize(word.text) == wanted
    ]


def run_matches(runs: list[Any], marker: str) -> list[Any]:
    wanted = normalize(marker)
    return [run for run in runs if wanted in normalize(run.text)]


def mm_to_pdf_pt(value: float) -> float:
    return value * 72.0 / 25.4


def record(rule_id: str, status: str, expected: Any, measured: Any, tool: str) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": tool,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure front matter table-of-contents final-PDF evidence.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    policy = load_json(VALIDATION_POLICY)
    if (
        scenario.get("schema_version") != 2

        or scenario.get("component") != "table-of-contents"
    ):
        fail("invalid TOC scenario schema/component")
    if policy.get("schema_version") != 2:
        fail("invalid validation policy schema")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    all_toc_scope = {rule_id for rule_id in rules if rule_id.startswith("toc.")}
    expected_scope = {
        rule_id
        for rule_id in all_toc_scope
        if rules[rule_id].get("authority") == "normative"
    }
    expected_non_normative = all_toc_scope - expected_scope
    scenario_scope = set(scenario.get("rules", []))
    scenario_non_normative = set(scenario.get("non_normative_rules", []))
    if expected_scope != scenario_scope or len(expected_scope) != 5:
        fail(
            "normative TOC scope mismatch: "
            f"scenario_only={sorted(scenario_scope - expected_scope)} "
            f"contract_only={sorted(expected_scope - scenario_scope)} "
            f"count={len(expected_scope)}"
        )
    if expected_non_normative != scenario_non_normative:
        fail(
            "non-normative TOC scope mismatch: "
            f"scenario_only={sorted(scenario_non_normative - expected_non_normative)} "
            f"contract_only={sorted(expected_non_normative - scenario_non_normative)}"
        )
    if scenario.get("rules") != RULE_ORDER:
        fail("TOC normative rule order drift")
    if scenario.get("non_normative_rules") != NON_NORMATIVE_RULE_ORDER:
        fail("TOC non-normative rule order drift")

    project_rule = rules["toc.leaders.dotted.project"]
    if (
        project_rule.get("authority") != "project-policy"
        or project_rule.get("values", {}).get("normative_claim") is not False
    ):
        fail("dotted-leader project policy authority drift")

    heading = scenario.get("heading")
    frontmatter_markers = scenario.get("frontmatter_markers")
    hierarchy = scenario.get("hierarchy")
    if not isinstance(heading, str) or not heading:
        fail("TOC heading marker is required")
    if not isinstance(frontmatter_markers, list) or not frontmatter_markers:
        fail("front matter markers are required")
    if not all(isinstance(marker, str) and marker for marker in frontmatter_markers):
        fail("front matter markers must be non-empty strings")
    if not isinstance(hierarchy, list) or len(hierarchy) != 5:
        fail("TOC hierarchy must contain exactly five levels")
    if [item.get("level") for item in hierarchy if isinstance(item, dict)] != LEVEL_ORDER:
        fail("TOC hierarchy level order drift")
    if not all(
        isinstance(item, dict)
        and set(item) == {"level", "marker"}
        and isinstance(item["marker"], str)
        and item["marker"]
        for item in hierarchy
    ):
        fail("invalid TOC hierarchy specification")

    tolerances = policy.get("tolerances")
    if not isinstance(tolerances, dict):
        fail("validation tolerances are required")
    try:
        horizontal_tolerance = float(tolerances["horizontal_position_pt"])
        vertical_tolerance = float(tolerances["vertical_position_pt"])
        font_tolerance = float(tolerances["font_size_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid validation tolerances: {exc}")

    try:
        pages = bbox_pages(args.pdf)
        runs = typography_runs(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    heading_matches = word_matches(pages, heading)
    if len(heading_matches) != 1:
        fail(f"TOC heading must occur once: {[(page.index, word.text) for page, word in heading_matches]}")
    toc_heading_page, heading_word = heading_matches[0]
    toc_start_page = toc_heading_page.index

    hierarchy_bbox: dict[str, dict[str, Any]] = {}
    for item in hierarchy:
        marker = item["marker"]
        matches = word_matches(pages, marker)
        if len(matches) != 2:
            fail(f"hierarchy marker {marker} must occur exactly twice: {[(p.index, w.text) for p, w in matches]}")
        ordered = sorted(matches, key=lambda pair: pair[0].index)
        toc_match, body_match = ordered
        if toc_match[0].index < toc_start_page or body_match[0].index <= toc_match[0].index:
            fail(f"invalid TOC/body ordering for {marker}")
        hierarchy_bbox[item["level"]] = {
            "marker": marker,
            "toc_page": toc_match[0],
            "toc_word": toc_match[1],
            "body_page": body_match[0],
            "body_word": body_match[1],
        }

    first_text_page = min(item["body_page"].index for item in hierarchy_bbox.values())
    if first_text_page <= toc_start_page:
        fail("textual content must follow the TOC")
    toc_pages = [page for page in pages if toc_start_page <= page.index < first_text_page]
    toc_page_indexes = {page.index for page in toc_pages}
    if not toc_pages:
        fail("no TOC pages identified")
    if any(item["toc_page"].index not in toc_page_indexes for item in hierarchy_bbox.values()):
        fail("hierarchy TOC marker fell outside the identified TOC page range")

    evidence: list[dict[str, Any]] = []

    exclusion_rule = rules["toc.frontmatter-exclusion"]
    exclusion_expected = exclusion_rule["values"]["frontmatter_entries"]
    toc_text = normalize(" ".join(page_text(page) for page in toc_pages))
    leaked = [marker for marker in frontmatter_markers if normalize(marker) in toc_text]
    evidence.append(
        record(
            "toc.frontmatter-exclusion",
            "PASS" if exclusion_expected is False and not leaked else "FAIL",
            {"frontmatter_entries": exclusion_expected},
            {
                "toc_pages": sorted(toc_page_indexes),
                "checked_markers": frontmatter_markers,
                "leaked_markers": leaked,
            },
            "pdftotext -bbox-layout",
        )
    )

    left_rule = rules.get("margin.recto.left")
    right_rule = rules.get("margin.recto.right")
    if left_rule is None or right_rule is None:
        fail("recto margin rules required for TOC geometry calibration")
    left_pt = mm_to_pdf_pt(float(left_rule["values"]["left_mm"]))
    right_pt = mm_to_pdf_pt(float(right_rule["values"]["right_mm"]))
    expected_right = toc_heading_page.width - right_pt
    expected_center = (left_pt + expected_right) / 2.0

    alignment_rule = rules["toc.heading.alignment"]
    alignment_expected = alignment_rule["values"]["heading_centered"]
    heading_center_delta = abs(heading_word.box.center_x - expected_center)
    evidence.append(
        record(
            "toc.heading.alignment",
            "PASS"
            if alignment_expected is True and heading_center_delta <= horizontal_tolerance
            else "FAIL",
            {"heading_centered": alignment_expected},
            {
                "page": toc_heading_page.index,
                "heading_center_pt": round(heading_word.box.center_x, 4),
                "text_area_center_pt": round(expected_center, 4),
                "delta_pt": round(heading_center_delta, 4),
            },
            "pdftotext -bbox-layout",
        )
    )

    case_rule = rules["toc.heading.case"]
    case_expected = case_rule["values"]["heading_uppercase"]
    raw_heading = heading_word.text
    heading_uppercase = raw_heading == raw_heading.upper() and any(char.isalpha() for char in raw_heading)
    evidence.append(
        record(
            "toc.heading.case",
            "PASS" if case_expected is True and heading_uppercase else "FAIL",
            {"heading_uppercase": case_expected},
            {"text": raw_heading, "uppercase": heading_uppercase},
            "pdftotext -bbox-layout",
        )
    )

    page_rule = rules["toc.page-number.position"]
    page_expected = page_rule["values"]["page_numbers"]
    page_measurements: dict[str, Any] = {}
    page_position_pass = page_expected == "right"
    for level in LEVEL_ORDER:
        item = hierarchy_bbox[level]
        page = item["toc_page"]
        marker_word = item["toc_word"]
        candidates = [
            word
            for word in page.words
            if re.fullmatch(r"\d+", word.text.strip())
            and word.box.x_min > marker_word.box.x_max
            and abs(word.box.center_y - marker_word.box.center_y) <= vertical_tolerance
        ]
        if not candidates:
            page_measurements[level] = {"page": page.index, "page_number": None}
            page_position_pass = False
            continue
        page_word = max(candidates, key=lambda word: word.box.x_max)
        delta = abs(page_word.box.x_max - expected_right)
        page_measurements[level] = {
            "page": page.index,
            "page_number": page_word.text,
            "x_max_pt": round(page_word.box.x_max, 4),
            "expected_right_pt": round(expected_right, 4),
            "delta_pt": round(delta, 4),
        }
        if delta > horizontal_tolerance:
            page_position_pass = False
    evidence.append(
        record(
            "toc.page-number.position",
            "PASS" if page_position_pass else "FAIL",
            {"page_numbers": page_expected},
            page_measurements,
            "pdftotext -bbox-layout",
        )
    )

    hierarchy_rule = rules["toc.section-hierarchy.mirror"]
    hierarchy_expected = hierarchy_rule["values"]["mirror_section_hierarchy"]
    hierarchy_measurements: dict[str, Any] = {}
    hierarchy_pass = hierarchy_expected is True
    for item in hierarchy:
        level = item["level"]
        marker = item["marker"]
        matches = run_matches(runs, marker)
        toc_runs = [run for run in matches if run.page in toc_page_indexes]
        body_runs = [run for run in matches if run.page >= first_text_page]
        if len(toc_runs) != 1 or len(body_runs) != 1:
            hierarchy_measurements[level] = {
                "marker": marker,
                "toc_run_count": len(toc_runs),
                "body_run_count": len(body_runs),
            }
            hierarchy_pass = False
            continue
        toc_run = toc_runs[0]
        body_run = body_runs[0]
        font_delta = abs(toc_run.font_size - body_run.font_size)
        style_match = (
            toc_run.font_id == body_run.font_id
            and toc_run.family == body_run.family
            and font_delta <= font_tolerance
        )
        hierarchy_measurements[level] = {
            "marker": marker,
            "toc": {
                "page": toc_run.page,
                "text": toc_run.text,
                "font_id": toc_run.font_id,
                "family": toc_run.family,
                "font_pt": toc_run.font_size,
            },
            "body": {
                "page": body_run.page,
                "text": body_run.text,
                "font_id": body_run.font_id,
                "family": body_run.family,
                "font_pt": body_run.font_size,
            },
            "font_size_delta_pt": round(font_delta, 4),
            "style_match": style_match,
        }
        if not style_match:
            hierarchy_pass = False
    evidence.append(
        record(
            "toc.section-hierarchy.mirror",
            "PASS" if hierarchy_pass else "FAIL",
            {"mirror_section_hierarchy": hierarchy_expected},
            hierarchy_measurements,
            "pdftohtml -xml -zoom 1.0",
        )
    )

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "validation_scope": "frontmatter",
        "component": "table-of-contents",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "normative_rules": RULE_ORDER,
        "non_normative_rules": NON_NORMATIVE_RULE_ORDER,
        "toc_pages": sorted(toc_page_indexes),
        "first_text_page": first_text_page,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "FRONTMATTER-EVIDENCE toc-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" toc_pages={','.join(str(page) for page in sorted(toc_page_indexes))}"
        + f" hierarchy_levels={len(hierarchy)}"
        + f" non_normative={len(NON_NORMATIVE_RULE_ORDER)}"
    )
    for item in evidence:
        print(
            f"FRONTMATTER-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )


if __name__ == "__main__":
    main()
