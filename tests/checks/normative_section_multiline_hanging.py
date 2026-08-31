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
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize

SCENARIO = ROOT / "standards" / "section-multiline-hanging-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-sections-footnotes-nature.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULE_ID = "section.multiline.hanging"
LEVEL_ORDER = ["section", "subsection", "subsubsection", "paragraph", "subparagraph"]
NUMBER_RE = re.compile(r"[0-9]+(?:\.[0-9]+)*")
PREFIX_RE = re.compile(r"HLH[A-Z]")


def fail(message: str) -> None:
    raise SystemExit(f"Section multiline hanging validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def expected_markers(prefix: str, count: int) -> list[str]:
    return [f"{prefix}{index:02d}MARK" for index in range(1, count + 1)]


def controlled_words(pages: list[Any], markers: list[str]) -> list[tuple[Any, Any]]:
    wanted = {normalize(marker): marker for marker in markers}
    found: dict[str, list[tuple[Any, Any]]] = {key: [] for key in wanted}
    for page in pages:
        for word in page.words:
            key = normalize(word.text)
            if key in found:
                found[key].append((page, word))
    bad = {wanted[key]: matches for key, matches in found.items() if len(matches) != 1}
    if bad:
        fail(
            "controlled marker multiplicity drift: "
            + ", ".join(f"{marker}={len(matches)}" for marker, matches in bad.items())
        )
    return [found[normalize(marker)][0] for marker in markers]


def group_lines(words: list[Any], vertical_tolerance: float) -> list[list[Any]]:
    lines: list[list[Any]] = []
    for word in sorted(words, key=lambda item: (item.box.center_y, item.box.x_min)):
        for line in lines:
            center_y = sum(item.box.center_y for item in line) / len(line)
            if abs(word.box.center_y - center_y) <= vertical_tolerance:
                line.append(word)
                break
        else:
            lines.append([word])
    lines.sort(key=lambda line: sum(item.box.center_y for item in line) / len(line))
    for line in lines:
        line.sort(key=lambda item: item.box.x_min)
    return lines


def number_left_of_first_line(page: Any, first_word: Any, expected: str, vertical_tolerance: float) -> Any:
    candidates = [
        word
        for word in page.words
        if NUMBER_RE.fullmatch(word.text.strip())
        and word.text.strip() == expected
        and word.box.x_max <= first_word.box.x_min
        and abs(word.box.center_y - first_word.box.center_y) <= vertical_tolerance
    ]
    if len(candidates) != 1:
        fail(
            f"heading {expected}: expected one numeric indicator left of first title word, "
            f"found {[word.text for word in candidates]}"
        )
    return candidates[0]


def record(status: str, expected: Any, measured: Any) -> dict[str, Any]:
    return {
        "rule_id": RULE_ID,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": "pdftotext -bbox-layout",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure multiline section hanging alignment from a final PDF.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locator = load_json(LOCATOR_AUDIT)
    policy = load_json(VALIDATION_POLICY)

    if (
        scenario.get("schema_version") != 1

        or scenario.get("component") != "section-multiline-hanging"
        or scenario.get("locator_ruleset") != "sections.multiline-hanging"
        or scenario.get("rules") != [RULE_ID]
    ):
        fail("invalid scenario schema/component/ruleset/rules")
    if policy.get("schema_version") != 2:
        fail("invalid validation policy schema")

    locator_matches = [
        item
        for item in locator.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == scenario["locator_ruleset"]
    ]
    if len(locator_matches) != 1:
        fail(f"locator ruleset drift: found {len(locator_matches)} matches")
    if locator_matches[0].get("rule_ids") != [RULE_ID]:
        fail(f"locator scope drift: {locator_matches[0].get('rule_ids')}")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    rule = rules.get(RULE_ID)
    if not isinstance(rule, dict) or rule.get("authority") != "normative":
        fail("full-contract rule missing or non-normative")
    expected = rule.get("values")
    if expected != {"enabled": True}:
        fail(f"stored predicate drift: {expected}")

    levels = scenario.get("levels")
    if not isinstance(levels, list) or len(levels) != 5:
        fail("scenario must contain exactly five controlled hierarchy levels")
    if [item.get("level") for item in levels if isinstance(item, dict)] != LEVEL_ORDER:
        fail("hierarchy level order drift")
    required_keys = {"level", "number", "marker_prefix", "marker_count"}
    if not all(
        isinstance(item, dict)
        and set(item) == required_keys
        and isinstance(item["number"], str)
        and NUMBER_RE.fullmatch(item["number"])
        and isinstance(item["marker_prefix"], str)
        and PREFIX_RE.fullmatch(item["marker_prefix"])
        and isinstance(item["marker_count"], int)
        and 8 <= item["marker_count"] <= 30
        for item in levels
    ):
        fail("invalid controlled level specification")

    try:
        horizontal_tolerance = float(policy["tolerances"]["horizontal_position_pt"])
        vertical_tolerance = float(policy["tolerances"]["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid validation tolerances: {exc}")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    measurements: list[dict[str, Any]] = []
    total_continuation_lines = 0

    for item in levels:
        markers = expected_markers(item["marker_prefix"], item["marker_count"])
        matches = controlled_words(pages, markers)
        page_indexes = {page.index for page, _ in matches}
        if len(page_indexes) != 1:
            fail(f"{item['level']}: title markers span pages {sorted(page_indexes)}")
        page_index = next(iter(page_indexes))
        page = next(page for page in pages if page.index == page_index)
        words = [word for _, word in matches]
        lines = group_lines(words, vertical_tolerance)
        if len(lines) < 2:
            fail(f"{item['level']}: controlled title did not wrap to multiple lines")

        first_word = min(lines[0], key=lambda word: word.box.x_min)
        indicator = number_left_of_first_line(page, first_word, item["number"], vertical_tolerance)
        first_x = first_word.box.x_min
        continuation = []
        for line_number, line in enumerate(lines[1:], start=2):
            first = min(line, key=lambda word: word.box.x_min)
            delta = abs(first.box.x_min - first_x)
            continuation.append(
                {
                    "line": line_number,
                    "x_min_pt": round(first.box.x_min, 4),
                    "delta_pt": round(delta, 4),
                }
            )

        total_continuation_lines += len(continuation)
        measurements.append(
            {
                "level": item["level"],
                "page": page_index,
                "indicator": indicator.text.strip(),
                "indicator_x_min_pt": round(indicator.box.x_min, 4),
                "first_title_x_min_pt": round(first_x, 4),
                "line_count": len(lines),
                "continuation_lines": continuation,
            }
        )

    passed = expected.get("enabled") is True and all(
        line["delta_pt"] <= horizontal_tolerance
        for measurement in measurements
        for line in measurement["continuation_lines"]
    )

    evidence = [
        record(
            "PASS" if passed else "FAIL",
            expected,
            {
                "horizontal_tolerance_pt": horizontal_tolerance,
                "alignment_reference": "first title-text character on the first line",
                "levels": measurements,
            },
        )
    ]
    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if passed else "FAIL"
    payload = {
        "schema_version": 1,
        "component": "section-multiline-hanging",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "measurements": measurements,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "VALIDATION-EVIDENCE section-multiline-hanging-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" levels={len(measurements)} continuation_lines={total_continuation_lines}"
    )
    for item in evidence:
        print(
            f"VALIDATION-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
