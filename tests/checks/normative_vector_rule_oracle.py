#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from pdf_measurement import PDFMeasurementError
from pdf_vector_measurement import vector_rules

EXTENSION = ROOT / "normativa" / "vector-rule-oracle-extension.json"
ORACLE_POLICY = ROOT / "normativa" / "oracle-policy.json"


def fail(message: str) -> None:
    raise SystemExit(f"N5 vector rule oracle calibration failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Calibrate the additive N5 vector-rule oracle.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()
    if not args.pdf.is_file():
        fail(f"PDF not found: {args.pdf}")

    extension = load_json(EXTENSION)
    oracle = load_json(ORACLE_POLICY)
    if (
        extension.get("schema_version") != 1
        or extension.get("phase") != "N5"
        or extension.get("component") != "vector-rule-geometry"
    ):
        fail("invalid extension schema/phase/component")
    if oracle.get("schema_version") != 1 or oracle.get("phase") != "N5":
        fail("invalid oracle policy schema/phase")
    if extension.get("tool") != "pdftocairo -svg":
        fail("vector tool drifted")
    if oracle.get("tools", {}).get("vector_geometry") != extension.get("tool"):
        fail("vector tool is not registered in oracle-policy.json")
    if "vector-rule-geometry" not in oracle.get("exit_capabilities", []):
        fail("vector-rule-geometry capability is not registered")
    if oracle.get("vector_geometry_extension") != "normativa/vector-rule-oracle-extension.json":
        fail("oracle extension binding drifted")

    policy = extension.get("policy", {})
    if not all(
        policy.get(key) is expected
        for key, expected in {
            "additive_capability_only": True,
            "existing_n5_tolerances_unchanged": True,
            "rasterization_not_used": True,
            "proof_state_changed": False,
        }.items()
    ):
        fail("vector extension policy drifted")

    parser_cfg = extension.get("parser", {})
    try:
        axis_tol = float(parser_cfg["axis_classification_tolerance_pt"])
        max_thickness = float(parser_cfg["max_rule_thickness_pt"])
        min_length = float(parser_cfg["min_rule_length_pt"])
        horizontal_tol = float(oracle["tolerances"]["horizontal_position_pt"])
        vertical_tol = float(oracle["tolerances"]["vertical_position_pt"])
    except (KeyError, TypeError, ValueError) as exc:
        fail(f"invalid vector/oracle numeric configuration: {exc}")

    calibration = extension.get("calibration", {})
    if calibration.get("expected_horizontal_rules") != 1 or calibration.get("expected_vertical_rules") != 1:
        fail("calibration rule-count contract drifted")
    if calibration.get("horizontal_length_tolerance_binding") != "oracle-policy.tolerances.horizontal_position_pt":
        fail("horizontal tolerance binding drifted")
    if calibration.get("vertical_length_tolerance_binding") != "oracle-policy.tolerances.vertical_position_pt":
        fail("vertical tolerance binding drifted")

    try:
        rules = vector_rules(
            args.pdf,
            page=1,
            axis_tolerance_pt=axis_tol,
            max_rule_thickness_pt=max_thickness,
            min_rule_length_pt=min_length,
        )
    except PDFMeasurementError as exc:
        fail(str(exc))

    horizontal = [rule for rule in rules if rule.orientation == "horizontal"]
    vertical = [rule for rule in rules if rule.orientation == "vertical"]
    if len(horizontal) != 1 or len(vertical) != 1:
        fail(
            "expected one horizontal and one vertical calibration rule, found "
            f"horizontal={len(horizontal)} vertical={len(vertical)} rules={[rule.to_dict() for rule in rules]}"
        )

    expected_horizontal = float(calibration["horizontal_length_mm"]) * 72.0 / 25.4
    expected_vertical = float(calibration["vertical_length_mm"]) * 72.0 / 25.4
    horizontal_delta = abs(horizontal[0].length - expected_horizontal)
    vertical_delta = abs(vertical[0].length - expected_vertical)
    horizontal_pass = horizontal_delta <= horizontal_tol
    vertical_pass = vertical_delta <= vertical_tol
    result = "PASS" if horizontal_pass and vertical_pass else "FAIL"

    checks = [
        {
            "id": "horizontal-length",
            "status": "PASS" if horizontal_pass else "FAIL",
            "expected_length_pt": round(expected_horizontal, 4),
            "measured": horizontal[0].to_dict(),
            "delta_pt": round(horizontal_delta, 4),
            "tolerance_pt": horizontal_tol,
        },
        {
            "id": "vertical-length",
            "status": "PASS" if vertical_pass else "FAIL",
            "expected_length_pt": round(expected_vertical, 4),
            "measured": vertical[0].to_dict(),
            "delta_pt": round(vertical_delta, 4),
            "tolerance_pt": vertical_tol,
        },
    ]
    payload = {
        "schema_version": 1,
        "phase": "N5",
        "component": "vector-rule-geometry",
        "source_commit_sha": args.commit_sha or "",
        "pdf": str(args.pdf),
        "result": result,
        "checks": checks,
        "proof_state_changed": False,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "N5-EVIDENCE vector-rule-oracle-calibration "
        f"PASS={sum(item['status'] == 'PASS' for item in checks)} "
        f"FAIL={sum(item['status'] == 'FAIL' for item in checks)} "
        f"horizontal_length_pt={horizontal[0].length:.4f} "
        f"vertical_length_pt={vertical[0].length:.4f}"
    )
    for item in checks:
        print("N5-EVIDENCE vector-rule-check " + json.dumps(item, ensure_ascii=False, sort_keys=True))
    if result != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
