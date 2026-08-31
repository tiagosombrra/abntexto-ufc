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

SCENARIO = ROOT / "standards" / "pagination-geometry-scenario.json"
LOCATORS = ROOT / "standards" / "locator-audit-layout-pagination.json"
POLICY = ROOT / "standards" / "validation-reference-policy.json"
PT_PER_MM = 72.0 / 25.4
HEADER_REGION_PT = 100.0

RULE_ORDER = [
    "pagination.recto.position",
    "pagination.recto.offset.top",
    "pagination.recto.offset.right",
    "pagination.verso.position",
    "pagination.verso.offset.top",
    "pagination.verso.offset.left",
]


def fail(message: str) -> None:
    raise SystemExit(f"N7 pagination geometry validation failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def find_marker_page(pages: list[Any], marker: str) -> int:
    wanted = normalize(marker)
    matches = [
        page.index
        for page in pages
        for word in page.words
        if normalize(word.text) == wanted
    ]
    if len(matches) != 1:
        fail(f"marker {marker}: expected one page, found {matches}")
    return matches[0]


def page_number(page: Any) -> Any:
    matches = [
        word
        for word in page.words
        if word.box.y_min < HEADER_REGION_PT and re.fullmatch(r"[0-9]+", word.text.strip())
    ]
    if len(matches) != 1:
        fail(
            f"page {page.index}: expected one Arabic header number, "
            f"found {[(word.text, word.box.to_dict()) for word in matches]}"
        )
    return matches[0]


def exact_assertion(
    rule_id: str,
    expected: dict[str, Any],
    actual_pt: float,
    expected_pt: float,
    tolerance_pt: float,
    measured: dict[str, Any],
) -> dict[str, Any]:
    delta = abs(actual_pt - expected_pt)
    payload = dict(measured)
    payload.update(
        {
            "actual_pt": round(actual_pt, 4),
            "expected_pt": round(expected_pt, 4),
            "delta_pt": round(delta, 4),
        }
    )
    return {
        "rule_id": rule_id,
        "status": "PASS" if delta <= tolerance_pt else "FAIL",
        "expected": expected,
        "measured": payload,
        "tolerance_pt": tolerance_pt,
    }


def position_assertion(
    rule_id: str,
    expected: dict[str, Any],
    page: Any,
    number: Any,
    side: str,
) -> dict[str, Any]:
    upper = number.box.center_y < page.height / 2.0
    if side == "recto":
        outer = number.box.center_x > page.width / 2.0
        measured_position = "upper-right" if upper and outer else "not-upper-right"
    else:
        outer = number.box.center_x < page.width / 2.0
        measured_position = "upper-left" if upper and outer else "not-upper-left"
    return {
        "rule_id": rule_id,
        "status": "PASS" if measured_position == expected["position"] else "FAIL",
        "expected": expected,
        "measured": {
            "position": measured_position,
            "page": page.index,
            "page_width_pt": round(page.width, 4),
            "page_height_pt": round(page.height, 4),
            "number": number.text,
            "number_box": number.box.to_dict(),
            "upper_half": upper,
            "outer_half": outer,
            "position_only": True,
        },
        "tolerance_pt": None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure bounded N7 pagination geometry evidence.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    locators = load_json(LOCATORS)
    policy = load_json(POLICY)
    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N7"
        or scenario.get("component") != "pagination-geometry"
        or scenario.get("rules") != RULE_ORDER
        or scenario.get("locator_ruleset") != "pagination.general"
    ):
        fail("invalid scenario schema/phase/component/scope")

    locator_matches = [
        item
        for item in locators.get("rulesets", [])
        if isinstance(item, dict) and item.get("id") == "pagination.general"
    ]
    if len(locator_matches) != 1:
        fail("pagination.general locator ruleset is missing or duplicated")
    locator_rule_ids = locator_matches[0].get("rule_ids", [])
    missing_locator_rules = [rule_id for rule_id in RULE_ORDER if rule_id not in locator_rule_ids]
    if missing_locator_rules:
        fail("pagination locator scope drift: " + ", ".join(missing_locator_rules))

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    missing_contract_rules = [rule_id for rule_id in RULE_ORDER if rule_id not in rules]
    if missing_contract_rules:
        fail("contract rules missing: " + ", ".join(missing_contract_rules))

    expected = {rule_id: rules[rule_id]["values"] for rule_id in RULE_ORDER}
    expected_sanity = {
        "pagination.recto.position": {"position": "upper-right"},
        "pagination.recto.offset.top": {"top_mm": 20},
        "pagination.recto.offset.right": {"right_mm": 20},
        "pagination.verso.position": {"position": "upper-left"},
        "pagination.verso.offset.top": {"top_mm": 20},
        "pagination.verso.offset.left": {"left_mm": 20},
    }
    if expected != expected_sanity:
        fail(f"pagination contract values drifted: {expected}")

    tolerances = policy.get("tolerances", {})
    try:
        horizontal_tolerance = float(tolerances["horizontal_position_pt"])
        vertical_tolerance = float(tolerances["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid N5 position tolerances: {exc}")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))
    if len(pages) != 2:
        fail(f"pagination fixture must contain exactly two pages, got {len(pages)}")

    markers = scenario.get("markers")
    if not isinstance(markers, dict) or set(markers) != {"recto", "verso"}:
        fail("invalid marker specification")
    recto_page_index = find_marker_page(pages, str(markers["recto"]))
    verso_page_index = find_marker_page(pages, str(markers["verso"]))
    if recto_page_index != 1 or verso_page_index != 2:
        fail(
            f"fixture parity drift: recto marker page={recto_page_index}, "
            f"verso marker page={verso_page_index}"
        )

    recto_page = pages[recto_page_index - 1]
    verso_page = pages[verso_page_index - 1]
    recto_number = page_number(recto_page)
    verso_number = page_number(verso_page)
    if recto_number.text != "1" or verso_number.text != "2":
        fail(
            f"unexpected textual pagination sequence: "
            f"recto={recto_number.text}, verso={verso_number.text}"
        )

    recto_top_expected = float(expected["pagination.recto.offset.top"]["top_mm"]) * PT_PER_MM
    recto_right_expected = float(expected["pagination.recto.offset.right"]["right_mm"]) * PT_PER_MM
    verso_top_expected = float(expected["pagination.verso.offset.top"]["top_mm"]) * PT_PER_MM
    verso_left_expected = float(expected["pagination.verso.offset.left"]["left_mm"]) * PT_PER_MM

    evidence = [
        position_assertion(
            "pagination.recto.position",
            expected["pagination.recto.position"],
            recto_page,
            recto_number,
            "recto",
        ),
        exact_assertion(
            "pagination.recto.offset.top",
            expected["pagination.recto.offset.top"],
            recto_number.box.y_min,
            recto_top_expected,
            vertical_tolerance,
            {
                "page": recto_page.index,
                "number": recto_number.text,
                "number_box": recto_number.box.to_dict(),
                "reference": "physical-page-top-to-glyph-box-top",
            },
        ),
        exact_assertion(
            "pagination.recto.offset.right",
            expected["pagination.recto.offset.right"],
            recto_page.width - recto_number.box.x_max,
            recto_right_expected,
            horizontal_tolerance,
            {
                "page": recto_page.index,
                "number": recto_number.text,
                "page_width_pt": round(recto_page.width, 4),
                "number_box": recto_number.box.to_dict(),
                "reference": "physical-page-right-to-glyph-box-right",
            },
        ),
        position_assertion(
            "pagination.verso.position",
            expected["pagination.verso.position"],
            verso_page,
            verso_number,
            "verso",
        ),
        exact_assertion(
            "pagination.verso.offset.top",
            expected["pagination.verso.offset.top"],
            verso_number.box.y_min,
            verso_top_expected,
            vertical_tolerance,
            {
                "page": verso_page.index,
                "number": verso_number.text,
                "number_box": verso_number.box.to_dict(),
                "reference": "physical-page-top-to-glyph-box-top",
            },
        ),
        exact_assertion(
            "pagination.verso.offset.left",
            expected["pagination.verso.offset.left"],
            verso_number.box.x_min,
            verso_left_expected,
            horizontal_tolerance,
            {
                "page": verso_page.index,
                "number": verso_number.text,
                "number_box": verso_number.box.to_dict(),
                "reference": "physical-page-left-to-glyph-box-left",
            },
        ),
    ]

    if [item["rule_id"] for item in evidence] != RULE_ORDER:
        fail("evidence order drift")
    counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N7",
        "component": "pagination-geometry",
        "source_commit_sha": args.commit_sha,
        "fixture": scenario["fixture"],
        "result": result,
        "status_counts": counts,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "N7-EVIDENCE pagination-geometry-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        + f" recto_box={recto_number.box.x_min:.4f},{recto_number.box.y_min:.4f},"
        f"{recto_number.box.x_max:.4f},{recto_number.box.y_max:.4f}"
        + f" verso_box={verso_number.box.x_min:.4f},{verso_number.box.y_min:.4f},"
        f"{verso_number.box.x_max:.4f},{verso_number.box.y_max:.4f}"
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
