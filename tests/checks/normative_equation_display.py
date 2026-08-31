#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, bbox_pages, normalize

SCENARIO = ROOT / "standards" / "equation-display-final-pdf-scenario.json"
LOCATOR = ROOT / "standards" / "locator-audit-objects-equations.json"
VALIDATION_POLICY = ROOT / "standards" / "validation-reference-policy.json"
RULE_ID = "equation.display"
EXPECTED = {"displayed": True}


def fail(message: str) -> None:
    raise SystemExit(f"equation display validation failed: {message}")


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
        item for item in document.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == ruleset_id
    ]
    if len(matches) != 1:
        fail(f"locator ruleset {ruleset_id}: expected one match, found {len(matches)}")
    return matches[0]


def unique_word(pages: list[Any], marker: str) -> tuple[Any, Any]:
    wanted = normalize(marker)
    matches = [
        (page, word) for page in pages for word in page.words
        if normalize(word.text) == wanted
    ]
    if len(matches) != 1:
        fail(f"marker {marker!r}: expected one word, found {len(matches)}")
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure bounded equation display evidence.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()
    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locator = load_json(LOCATOR)
    validation = load_json(VALIDATION_POLICY)

    if (
        scenario.get("schema_version") != 1

        or scenario.get("component") != "equation-display-final-pdf"
        or scenario.get("campaign_id") != "equation-display-final-pdf"
        or scenario.get("rules") != [RULE_ID]
    ):
        fail("invalid scenario schema/phase/component/scope")


    presentation_rules = ruleset(locator, "equations.presentation").get("rule_ids", [])
    if RULE_ID not in presentation_rules:
        fail("equation display locator scope drifted")

    contract = load_full_contract()
    contract_rules = {rule["id"]: rule for rule in contract["rules"]}
    rule = contract_rules.get(RULE_ID)
    if not isinstance(rule, dict) or rule.get("values") != EXPECTED:
        fail(f"equation display contract values drifted: {None if rule is None else rule.get('values')}")

    tolerances = validation.get("tolerances", {})
    try:
        vertical_tol = float(tolerances["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid validation vertical tolerance: {exc}")
    if "pdftotext -bbox-layout" not in set(validation.get("tools", {}).values()):
        fail("equation display tool left validation policy")

    fixture = scenario.get("fixture", {})
    markers = scenario.get("markers", {})
    if fixture.get("engine") != "pdflatex" or fixture.get("passes") != 2:
        fail("fixture engine/pass contract drift")
    if set(markers) != {"before", "equation", "after"}:
        fail("equation display marker contract drift")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))
    if len(pages) != fixture.get("expected_pages"):
        fail(f"fixture page count drifted: expected={fixture.get('expected_pages')} actual={len(pages)}")

    page_before, before = unique_word(pages, markers["before"])
    page_equation, equation = unique_word(pages, markers["equation"])
    page_after, after = unique_word(pages, markers["after"])
    if len({page_before.index, page_equation.index, page_after.index}) != 1:
        fail("controlled equation markers must share one page")

    before_gap = equation.box.y_min - before.box.y_max
    after_gap = after.box.y_min - equation.box.y_max
    ordered_centers = before.box.center_y < equation.box.center_y < after.box.center_y
    non_overlapping = before_gap > 0.0 and after_gap > 0.0
    distinct_bands = (
        equation.box.center_y - before.box.center_y > vertical_tol
        and after.box.center_y - equation.box.center_y > vertical_tol
    )
    passed = ordered_centers and non_overlapping and distinct_bands

    measured = {
        "page": page_equation.index,
        "before_y_max_pt": round(before.box.y_max, 4),
        "equation_y_min_pt": round(equation.box.y_min, 4),
        "equation_y_max_pt": round(equation.box.y_max, 4),
        "after_y_min_pt": round(after.box.y_min, 4),
        "before_gap_pt": round(before_gap, 4),
        "after_gap_pt": round(after_gap, 4),
        "ordered_vertical_centers": ordered_centers,
        "non_overlapping_vertical_bands": non_overlapping,
        "distinct_from_body_by_validation_vertical_tolerance": distinct_bands,
        "equation_x_min_pt_observation": round(equation.box.x_min, 4),
        "horizontal_alignment_not_frozen": True,
        "exact_vertical_gaps_not_frozen": True,
    }
    evidence = {
        "rule_id": RULE_ID,
        "status": "PASS" if passed else "FAIL",
        "expected": EXPECTED,
        "measured": measured,
        "tool": "pdftotext -bbox-layout",
        "tolerance": {"vertical_position_pt": vertical_tol},
    }
    result = evidence["status"]
    payload = {
        "schema_version": 1,
        "component": "equation-display-final-pdf",
        "source_commit_sha": args.commit_sha or "",
        "pdf": str(args.pdf),
        "result": result,
        "evidence": [evidence],
        "proof_state_changed": False,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"VALIDATION-EVIDENCE equation-display-final-pdf-summary {result}=1 "
        f"before_gap_pt={before_gap:.4f} after_gap_pt={after_gap:.4f}"
    )
    print(
        f"VALIDATION-EVIDENCE rule={RULE_ID} status={result} "
        f"expected={json.dumps(EXPECTED, ensure_ascii=False, sort_keys=True)} "
        f"measured={json.dumps(measured, ensure_ascii=False, sort_keys=True)}"
    )
    if not passed:
        fail("equation was not measured as a distinct displayed block")


if __name__ == "__main__":
    main()
