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

from normative_full import load_full_contract
from pdf_measurement import PDFMeasurementError, Box, bbox_pages, find_marker
from pdf_vector_measurement import VectorRule, vector_rules

SCENARIO = ROOT / "normativa" / "table-ibge-vector-final-pdf-scenario.json"
CAMPAIGN_PLAN = ROOT / "normativa" / "n9-campaign-plan.json"
LOCATOR = ROOT / "normativa" / "locator-audit-final.json"
ORACLE_POLICY = ROOT / "normativa" / "oracle-policy.json"
EXTENSION = ROOT / "normativa" / "vector-rule-oracle-extension.json"
CALIBRATION_RUNTIME = ROOT / "artifacts" / "normative-layout" / "vector-rule-oracle-calibration.json"

RULES = [
    "table.ibge.open-sides",
    "table.ibge.body-grid",
    "table.ibge.top-rule",
    "table.ibge.header-rule",
    "table.ibge.bottom-rule",
]
EXPECTED = {
    "table.ibge.open-sides": {"open_sides": True},
    "table.ibge.body-grid": {"body_grid": False},
    "table.ibge.top-rule": {"top_rule": True},
    "table.ibge.header-rule": {"header_rule": True},
    "table.ibge.bottom-rule": {"bottom_rule": True},
}


def fail(message: str) -> None:
    raise SystemExit(f"N9 IBGE vector oracle failed: {message}")


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


def union_box(*boxes: Box) -> Box:
    return Box(
        min(box.x_min for box in boxes),
        min(box.y_min for box in boxes),
        max(box.x_max for box in boxes),
        max(box.y_max for box in boxes),
    )


def rule_center_x(rule: VectorRule) -> float:
    return rule.box.center_x


def rule_center_y(rule: VectorRule) -> float:
    return rule.box.center_y


def candidate_dicts(rules: list[VectorRule]) -> list[dict[str, object]]:
    return [rule.to_dict() for rule in rules]


def evidence(
    rule_id: str,
    passed: bool,
    measured: dict[str, Any],
    horizontal_tol: float,
    vertical_tol: float,
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": "PASS" if passed else "FAIL",
        "expected": EXPECTED[rule_id],
        "measured": measured,
        "tool": "pdftocairo -svg; pdftotext -bbox-layout",
        "tolerance": {
            "horizontal_position_pt": horizontal_tol,
            "vertical_position_pt": vertical_tol,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure the five residual N9 IBGE table predicates.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()
    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    scenario = load_json(SCENARIO)
    plan = load_json(CAMPAIGN_PLAN)
    locator = load_json(LOCATOR)
    oracle = load_json(ORACLE_POLICY)
    extension = load_json(EXTENSION)
    calibration = load_json(CALIBRATION_RUNTIME)

    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N9"
        or scenario.get("component") != "table-ibge-vector-final-pdf"
        or scenario.get("campaign_id") != "table-final-pdf"
        or scenario.get("rules") != RULES
    ):
        fail("invalid scenario schema/phase/component/scope")
    if scenario.get("oracle_extension") != "normativa/vector-rule-oracle-extension.json":
        fail("scenario oracle-extension binding drifted")
    if scenario.get("locator_ruleset") != "objects.table-ibge":
        fail("scenario locator binding drifted")

    campaigns = {
        item.get("id"): item for item in plan.get("campaigns", [])
        if isinstance(item, dict)
    }
    campaign = campaigns.get("table-final-pdf")
    if not isinstance(campaign, dict):
        fail("table-final-pdf campaign is missing")
    if set(campaign.get("oracle_extension_required_rule_ids", [])) != set(RULES):
        fail("table vector residual scope drifted")
    if not set(RULES) <= set(campaign.get("rule_ids", [])):
        fail("IBGE rules escaped the table campaign")

    located = ruleset(locator, "objects.table-ibge")
    if set(located.get("rule_ids", [])) != set(RULES):
        fail("IBGE locator scope drifted")

    contract = load_full_contract()
    contract_rules = {rule["id"]: rule for rule in contract["rules"]}
    values = {rule_id: contract_rules[rule_id]["values"] for rule_id in RULES}
    if values != EXPECTED:
        fail(f"IBGE contract values drifted: {values}")

    if oracle.get("tools", {}).get("vector_geometry") != "pdftocairo -svg":
        fail("vector geometry tool left N5 oracle policy")
    if "vector-rule-geometry" not in oracle.get("exit_capabilities", []):
        fail("N5 vector-rule-geometry capability is not active")
    if extension.get("component") != "vector-rule-geometry" or extension.get("tool") != "pdftocairo -svg":
        fail("invalid vector-rule oracle extension")
    if calibration.get("phase") != "N5" or calibration.get("component") != "vector-rule-geometry" or calibration.get("result") != "PASS":
        fail("same-run vector-rule calibration did not PASS")
    if calibration.get("proof_state_changed") is not False:
        fail("vector-rule calibration changed proof-state")
    expected_sha = args.commit_sha or ""
    if expected_sha and calibration.get("source_commit_sha") != expected_sha:
        fail(
            "vector-rule calibration SHA mismatch: "
            f"expected={expected_sha}, actual={calibration.get('source_commit_sha')}"
        )

    try:
        horizontal_tol = float(oracle["tolerances"]["horizontal_position_pt"])
        vertical_tol = float(oracle["tolerances"]["vertical_position_pt"])
        parser_cfg = extension["parser"]
        axis_tol = float(parser_cfg["axis_classification_tolerance_pt"])
        max_thickness = float(parser_cfg["max_rule_thickness_pt"])
        min_length = float(parser_cfg["min_rule_length_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid oracle configuration: {exc}")

    markers = scenario.get("markers", {})
    expected_marker_keys = {
        "caption",
        "header_left",
        "header_right",
        "body_first",
        "body_middle",
        "body_last",
        "table_source_marker",
    }
    if set(markers) != expected_marker_keys:
        fail("IBGE marker contract drifted")

    try:
        pages = bbox_pages(args.pdf)
    except PDFMeasurementError as exc:
        fail(str(exc))
    if len(pages) != scenario.get("fixture", {}).get("expected_pages"):
        fail(f"fixture page count drifted: {len(pages)}")

    found: dict[str, tuple[Any, Any]] = {}
    for key, marker in markers.items():
        try:
            found[key] = find_marker(pages, marker)
        except PDFMeasurementError as exc:
            fail(str(exc))
    page_indices = {page.index for page, _word in found.values()}
    if len(page_indices) != 1:
        fail(f"all controlled markers must share one page: {sorted(page_indices)}")
    page_index = next(iter(page_indices))

    caption = found["caption"][1].box
    header_left = found["header_left"][1].box
    header_right = found["header_right"][1].box
    header = union_box(header_left, header_right)
    body_first = found["body_first"][1].box
    body_middle = found["body_middle"][1].box
    body_last = found["body_last"][1].box
    table_source = found["table_source_marker"][1].box
    content_left = min(header_left.x_min, body_first.x_min, body_middle.x_min, body_last.x_min)
    content_right = max(header_right.x_max, header_left.x_max)

    try:
        rules = vector_rules(
            args.pdf,
            page=page_index,
            axis_tolerance_pt=axis_tol,
            max_rule_thickness_pt=max_thickness,
            min_rule_length_pt=min_length,
        )
    except PDFMeasurementError as exc:
        fail(str(exc))

    horizontal = [rule for rule in rules if rule.orientation == "horizontal"]
    vertical = [rule for rule in rules if rule.orientation == "vertical"]
    covering = [
        rule for rule in horizontal
        if rule.box.x_min <= content_left + horizontal_tol
        and rule.box.x_max >= content_right - horizontal_tol
    ]

    top_candidates = [
        rule for rule in covering
        if caption.y_max - vertical_tol <= rule_center_y(rule) <= header.y_min + vertical_tol
    ]
    header_candidates = [
        rule for rule in covering
        if header.y_max - vertical_tol <= rule_center_y(rule) <= body_first.y_min + vertical_tol
    ]
    bottom_candidates = [
        rule for rule in covering
        if body_last.y_max - vertical_tol <= rule_center_y(rule) <= table_source.y_min + vertical_tol
    ]

    top_pass = len(top_candidates) == 1
    header_pass = len(header_candidates) == 1
    bottom_pass = len(bottom_candidates) == 1
    boundaries_valid = top_pass and header_pass and bottom_pass

    side_verticals: list[VectorRule] = []
    body_horizontal_grid: list[VectorRule] = []
    body_vertical_grid: list[VectorRule] = []
    table_bounds: dict[str, float] | None = None
    if boundaries_valid:
        top_rule = top_candidates[0]
        header_rule = header_candidates[0]
        bottom_rule = bottom_candidates[0]
        table_left = min(top_rule.box.x_min, header_rule.box.x_min, bottom_rule.box.x_min)
        table_right = max(top_rule.box.x_max, header_rule.box.x_max, bottom_rule.box.x_max)
        table_top = rule_center_y(top_rule)
        table_bottom = rule_center_y(bottom_rule)
        table_bounds = {
            "x_min_pt": round(table_left, 4),
            "x_max_pt": round(table_right, 4),
            "y_top_pt": round(table_top, 4),
            "y_bottom_pt": round(table_bottom, 4),
        }

        table_verticals = [
            rule for rule in vertical
            if table_left - horizontal_tol <= rule_center_x(rule) <= table_right + horizontal_tol
            and rule.box.y_max >= table_top - vertical_tol
            and rule.box.y_min <= table_bottom + vertical_tol
        ]
        side_verticals = [
            rule for rule in table_verticals
            if abs(rule_center_x(rule) - table_left) <= horizontal_tol
            or abs(rule_center_x(rule) - table_right) <= horizontal_tol
        ]

        body_horizontal_grid = [
            rule for rule in covering
            if body_first.y_max + axis_tol < rule_center_y(rule) < body_last.y_min - axis_tol
        ]
        body_vertical_grid = [
            rule for rule in table_verticals
            if table_left + horizontal_tol < rule_center_x(rule) < table_right - horizontal_tol
            and rule.box.y_max >= body_first.y_min - vertical_tol
            and rule.box.y_min <= body_last.y_max + vertical_tol
        ]

    open_sides_pass = boundaries_valid and not side_verticals
    body_grid_pass = boundaries_valid and not body_horizontal_grid and not body_vertical_grid

    evidence_items = [
        evidence(
            RULES[0],
            open_sides_pass,
            {
                "boundary_rules_identified": boundaries_valid,
                "table_bounds": table_bounds,
                "side_vertical_rule_count": len(side_verticals),
                "side_vertical_rules": candidate_dicts(side_verticals),
                "open_sides": open_sides_pass,
            },
            horizontal_tol,
            vertical_tol,
        ),
        evidence(
            RULES[1],
            body_grid_pass,
            {
                "boundary_rules_identified": boundaries_valid,
                "body_horizontal_grid_rule_count": len(body_horizontal_grid),
                "body_vertical_grid_rule_count": len(body_vertical_grid),
                "body_horizontal_grid_rules": candidate_dicts(body_horizontal_grid),
                "body_vertical_grid_rules": candidate_dicts(body_vertical_grid),
                "body_grid": not body_grid_pass,
            },
            horizontal_tol,
            vertical_tol,
        ),
        evidence(
            RULES[2],
            top_pass,
            {
                "candidate_count": len(top_candidates),
                "candidates": candidate_dicts(top_candidates),
                "position_band": "caption-to-header",
                "exact_gap_not_frozen": True,
            },
            horizontal_tol,
            vertical_tol,
        ),
        evidence(
            RULES[3],
            header_pass,
            {
                "candidate_count": len(header_candidates),
                "candidates": candidate_dicts(header_candidates),
                "position_band": "header-to-first-body-row",
                "exact_gap_not_frozen": True,
            },
            horizontal_tol,
            vertical_tol,
        ),
        evidence(
            RULES[4],
            bottom_pass,
            {
                "candidate_count": len(bottom_candidates),
                "candidates": candidate_dicts(bottom_candidates),
                "position_band": "last-body-row-to-source",
                "exact_gap_not_frozen": True,
            },
            horizontal_tol,
            vertical_tol,
        ),
    ]

    counts = Counter(item["status"] for item in evidence_items)
    result = "PASS" if counts.get("FAIL", 0) == 0 else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N9",
        "component": "table-ibge-vector-final-pdf",
        "source_commit_sha": args.commit_sha or "",
        "pdf": str(args.pdf),
        "result": result,
        "vector_rule_inventory": {
            "total": len(rules),
            "horizontal": len(horizontal),
            "vertical": len(vertical),
            "covering_table_content": len(covering),
        },
        "evidence": evidence_items,
        "proof_state_changed": False,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "N9-EVIDENCE table-ibge-vector-final-pdf-summary "
        f"PASS={counts.get('PASS', 0)} FAIL={counts.get('FAIL', 0)} "
        f"horizontal_rules={len(horizontal)} vertical_rules={len(vertical)}"
    )
    for item in evidence_items:
        print(
            f"N9-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
