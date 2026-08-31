#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import get_rule, load_catalog
from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize

SCENARIO = ROOT / "standards" / "section-unnumbered-centered-scenario.json"
LOCATOR_AUDIT = ROOT / "standards" / "locator-audit-sections-footnotes-nature.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULE_ID = "heading.unnumbered.centered"
RULESET_ID = "sections.unnumbered-centered"
PT_PER_MM = 72.0 / 25.4


def fail(message: str) -> None:
    raise SystemExit(f"Unnumbered heading centering validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure N6 unnumbered-heading centering from a final PDF."
    )
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
        or scenario.get("phase") != "N6"
        or scenario.get("component") != "section-unnumbered-centered"
        or scenario.get("locator_ruleset") != RULESET_ID
        or scenario.get("rules") != [RULE_ID]
    ):
        fail("invalid scenario schema/phase/component/ruleset/rules")
    if policy.get("schema_version") != 1 or policy.get("phase") != "N5":
        fail("invalid validation policy schema/phase")

    locator_matches = [
        item
        for item in locator.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == RULESET_ID
    ]
    if len(locator_matches) != 1:
        fail(f"locator ruleset drift: found {len(locator_matches)} matches")
    if locator_matches[0].get("rule_ids") != [RULE_ID]:
        fail(f"locator scope drift: {locator_matches[0].get('rule_ids')}")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    rule = rules.get(RULE_ID)
    if not isinstance(rule, dict) or rule.get("authority") != "normative":
        fail(f"missing normative rule {RULE_ID}")
    expected = rule.get("values")
    if expected != {"alignment": "centered"}:
        fail(f"stored predicate drift: {expected}")

    surfaces = scenario.get("surfaces")
    required_surface_keys = {"id", "marker", "implementation"}
    if (
        not isinstance(surfaces, list)
        or len(surfaces) != 3
        or not all(
            isinstance(item, dict)
            and set(item) == required_surface_keys
            and all(isinstance(item[key], str) and item[key] for key in required_surface_keys)
            for item in surfaces
        )
    ):
        fail("scenario must contain exactly three valid implementation surfaces")
    if len({item["implementation"] for item in surfaces}) != 3:
        fail("implementation surfaces must be distinct")

    try:
        horizontal_tolerance = float(policy["tolerances"]["horizontal_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid horizontal tolerance: {exc}")
    if horizontal_tolerance <= 0:
        fail("horizontal tolerance must be positive")

    catalog = load_catalog()
    recto = get_rule(catalog, "margin.recto")
    try:
        left_mm = float(recto["values"]["left_mm"])
        right_mm = float(recto["values"]["right_mm"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid recto margin contract: {exc}")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))

    measurements: list[dict[str, Any]] = []
    for surface in surfaces:
        page, word = unique_word(pages, surface["marker"])
        text_left = left_mm * PT_PER_MM
        text_right = page.width - right_mm * PT_PER_MM
        text_center = (text_left + text_right) / 2.0
        heading_center = word.box.center_x
        delta = abs(heading_center - text_center)
        measurements.append(
            {
                "surface": surface["id"],
                "implementation": surface["implementation"],
                "marker": word.text,
                "page": page.index,
                "heading_center_pt": round(heading_center, 4),
                "text_area_center_pt": round(text_center, 4),
                "delta_pt": round(delta, 4),
            }
        )

    passed = all(item["delta_pt"] <= horizontal_tolerance for item in measurements)
    evidence = [
        {
            "rule_id": RULE_ID,
            "status": "PASS" if passed else "FAIL",
            "expected": expected,
            "measured": {
                "surfaces": measurements,
                "alignment_reference": "recto text-area center from normative margins",
            },
            "tool": "pdftotext -bbox-layout",
            "tolerance": horizontal_tolerance,
        }
    ]
    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if passed else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "component": "section-unnumbered-centered",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "measurements": measurements,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    max_delta = max(item["delta_pt"] for item in measurements)
    print(
        "N6-EVIDENCE section-unnumbered-centered-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" surfaces={len(measurements)} max_delta_pt={max_delta:.4f}"
    )
    print(
        f"N6-EVIDENCE rule={RULE_ID} status={evidence[0]['status']} "
        f"expected={json.dumps(expected, ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(evidence[0]['measured'], ensure_ascii=False, sort_keys=True)}"
    )

    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
