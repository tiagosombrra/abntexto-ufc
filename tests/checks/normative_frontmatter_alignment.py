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

from normative_catalog import get_rule, load_catalog
from normative_full import load_full_contract
from pdf_measurement import normalize

SCENARIOS = ROOT / "standards" / "frontmatter-alignment-scenarios.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-policy.json"
PT_PER_MM = 72.0 / 25.4
QUOTE_CHARS = {'"', '“', '”', '„', '«', '»'}


def fail(message: str) -> None:
    raise SystemExit(f"Front matter alignment validation failed: {message}")


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


def full_rule_map() -> dict[str, dict[str, Any]]:
    contract = load_full_contract()
    return {rule["id"]: rule for rule in contract["rules"]}


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


def word_text(word: ET.Element) -> str:
    return "".join(word.itertext()).strip()


def marker_word_matches(word: ET.Element, marker: str) -> bool:
    wrappers = "".join(QUOTE_CHARS)
    return normalize(word_text(word).strip(wrappers)) == normalize(marker)


def page_lines(page: ET.Element) -> list[ET.Element]:
    return [
        line
        for line in page.iter()
        if local(line.tag) == "line"
        and any(local(node.tag) == "word" for node in line)
    ]


def find_target_page(root: ET.Element, marker: str) -> tuple[int, ET.Element]:
    matches: list[tuple[int, ET.Element]] = []
    pages = [node for node in root.iter() if local(node.tag) == "page"]
    for page_index, page in enumerate(pages, start=1):
        if any(
            marker_word_matches(word, marker)
            for word in page.iter()
            if local(word.tag) == "word"
        ):
            matches.append((page_index, page))
    if len(matches) != 1:
        fail(f"marker {marker}: expected one target page, found {len(matches)}")
    return matches[0]


def line_bounds(line: ET.Element) -> tuple[float, float]:
    try:
        return float(line.attrib["xMin"]), float(line.attrib["xMax"])
    except (KeyError, ValueError) as exc:
        fail(f"invalid line bounds: {line.attrib}")
        raise AssertionError from exc


def audit_scenario(
    scenario: dict[str, Any],
    root: ET.Element,
    rules: dict[str, dict[str, Any]],
    margin_left_mm: float,
    margin_right_mm: float,
    tolerance_pt: float,
) -> dict[str, Any]:
    page_index, page = find_target_page(root, scenario["marker"])
    lines = page_lines(page)
    minimum_lines = int(scenario["minimum_lines"])
    if len(lines) < minimum_lines:
        fail(
            f"{scenario['id']}: expected at least {minimum_lines} naturally wrapped lines, "
            f"found {len(lines)}"
        )

    alignment_rule = rules[scenario["alignment_rule"]]
    indent_rule = rules[scenario["indent_rule"]]
    expected_alignment = alignment_rule["values"]["alignment"]
    if expected_alignment != "justified":
        fail(
            f"{scenario['alignment_rule']}: unsupported expected alignment "
            f"{expected_alignment!r}"
        )

    page_width = float(page.attrib["width"])
    indent_mm = float(indent_rule["values"]["left_indent_mm"])
    expected_left = (margin_left_mm + indent_mm) * PT_PER_MM
    expected_right = page_width - margin_right_mm * PT_PER_MM

    bounds = [line_bounds(line) for line in lines]
    left_deltas = [abs(x_min - expected_left) for x_min, _ in bounds]
    right_deltas = [abs(x_max - expected_right) for _, x_max in bounds[:-1]]
    passed = (
        all(delta <= tolerance_pt for delta in left_deltas)
        and bool(right_deltas)
        and all(delta <= tolerance_pt for delta in right_deltas)
    )

    return {
        "scenario_id": scenario["id"],
        "component": scenario["component"],
        "route": scenario["route"],
        "page": page_index,
        "marker": scenario["marker"],
        "rule_id": scenario["alignment_rule"],
        "status": "PASS" if passed else "FAIL",
        "expected": expected_alignment,
        "measured": {
            "line_count": len(lines),
            "expected_left_pt": round(expected_left, 4),
            "expected_right_pt": round(expected_right, 4),
            "line_bounds_pt": [
                {"x_min": round(x_min, 4), "x_max": round(x_max, 4)}
                for x_min, x_max in bounds
            ],
            "left_deltas_pt": [round(delta, 4) for delta in left_deltas],
            "non_final_right_deltas_pt": [round(delta, 4) for delta in right_deltas],
        },
        "tolerance_pt": tolerance_pt,
        "tool": "pdftotext -bbox-layout",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure front matter dedication and epigraph justification from wrapped PDF text."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    if not pdf.is_file():
        fail(f"PDF not found: {pdf}")

    scenarios_data = load_json(SCENARIOS, "front matter alignment scenarios")
    validation_policy = load_json(VALIDATION_POLICY, "validation policy")
    if scenarios_data.get("schema_version") != 2:
        fail("invalid alignment scenario schema")
    if validation_policy.get("schema_version") != 2:
        fail("invalid validation policy schema")

    scenarios = scenarios_data.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) != 3:
        fail("expected exactly three wrapped alignment scenarios")

    tolerance_pt = validation_policy.get("tolerances", {}).get("horizontal_position_pt")
    if not isinstance(tolerance_pt, (int, float)) or tolerance_pt <= 0:
        fail("horizontal_position_pt tolerance must be positive")

    rules = full_rule_map()
    required = {
        rule_id
        for scenario in scenarios
        for rule_id in (scenario["alignment_rule"], scenario["indent_rule"])
    }
    missing = sorted(required - set(rules))
    if missing:
        fail("scenario rules missing from full contract: " + ", ".join(missing))

    catalog = load_catalog()
    recto = get_rule(catalog, "margin.recto")
    margin_left_mm = float(recto["values"]["left_mm"])
    margin_right_mm = float(recto["values"]["right_mm"])
    root = bbox_root(pdf)

    results = [
        audit_scenario(
            scenario,
            root,
            rules,
            margin_left_mm,
            margin_right_mm,
            float(tolerance_pt),
        )
        for scenario in scenarios
    ]

    pages = [result["page"] for result in results]
    distinct_pages = len(set(pages)) == len(pages)
    if not distinct_pages:
        fail(f"target scenarios must occupy distinct pages: {pages}")

    counts = Counter(result["status"] for result in results)
    findings = [result["rule_id"] for result in results if result["status"] == "FAIL"]
    payload = {
        "schema_version": 1,
        "validation_scope": "frontmatter",
        "scope": "dedication-epigraph-alignment",
        "mode": "enforce" if args.enforce else "audit",
        "source_commit_sha": args.commit_sha,
        "fixture": scenarios_data["fixture"],
        "pdf": pdf.name,
        "target_pages_are_distinct": distinct_pages,
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
        "FRONTMATTER-EVIDENCE alignment-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        + f" distinct_pages={distinct_pages}"
    )
    for result in results:
        print(
            f"FRONTMATTER-EVIDENCE rule={result['rule_id']} status={result['status']} "
            f"expected={json.dumps(result['expected'], ensure_ascii=False)} "
            f"measured={json.dumps(result['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if args.enforce and findings:
        fail("enforcement requested with unresolved alignment findings")


if __name__ == "__main__":
    main()
