#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_catalog import get_rule, load_catalog
from pdf_measurement import (
    PDFMeasurementError,
    bbox_pages,
    find_marker,
    find_typography_marker,
    font_inventory,
    pdf_info,
    typography_runs,
)

POLICY = ROOT / "normativa" / "oracle-policy.json"
PT_PER_MM = 72.0 / 25.4


def fail(message: str) -> None:
    raise SystemExit(f"PDF oracle core failed: {message}")


def load_policy() -> dict[str, Any]:
    try:
        data = json.loads(POLICY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load oracle policy: {exc}")
    if data.get("schema_version") != 1 or data.get("phase") != "N5":
        fail("invalid oracle policy schema/phase")
    tolerances = data.get("tolerances")
    if not isinstance(tolerances, dict):
        fail("oracle tolerances are required")
    for key in (
        "page_size_pt",
        "horizontal_position_pt",
        "vertical_position_pt",
        "font_size_pt",
    ):
        value = tolerances.get(key)
        if not isinstance(value, (int, float)) or value <= 0:
            fail(f"invalid oracle tolerance: {key}")
    return data


def assertion(
    assertion_id: str,
    actual: float,
    expected: float,
    tolerance: float,
    unit: str,
) -> dict[str, Any]:
    delta = abs(actual - expected)
    return {
        "id": assertion_id,
        "actual": round(actual, 4),
        "expected": round(expected, 4),
        "tolerance": tolerance,
        "unit": unit,
        "delta": round(delta, 4),
        "status": "PASS" if delta <= tolerance else "FAIL",
    }


def minimum_assertion(
    assertion_id: str,
    actual: float,
    minimum: float,
    tolerance: float,
    unit: str,
) -> dict[str, Any]:
    passed = actual + tolerance >= minimum
    return {
        "id": assertion_id,
        "actual": round(actual, 4),
        "expected_minimum": round(minimum, 4),
        "tolerance": tolerance,
        "unit": unit,
        "status": "PASS" if passed else "FAIL",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the N5 PDF oracle core fixture.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    if not pdf.is_file():
        fail(f"PDF not found: {pdf}")

    policy = load_policy()
    tolerances = policy["tolerances"]
    catalog = load_catalog()
    page_rule = get_rule(catalog, "page.a4")
    margin_rule = get_rule(catalog, "margin.recto")
    body_font_rule = get_rule(catalog, "font.size.body")
    reduced_font_rule = get_rule(catalog, "font.size.reduced")

    try:
        pages = bbox_pages(pdf)
        typography = typography_runs(pdf)
        info = pdf_info(pdf)
        fonts = font_inventory(pdf)

        if len(pages) != 1:
            fail(f"isolated oracle fixture must contain one page, got {len(pages)}")
        page = pages[0]

        _, left = find_marker(pages, "UFCORACLELEFT")
        _, right = find_marker(pages, "UFCORACLERIGHT")
        _, block = find_marker(pages, "UFCORACLEBLOCK")
        _, body = find_marker(pages, "UFCORACLEBODY")
        _, reduced = find_marker(pages, "UFCORACLEREDUCED")

        body_type = find_typography_marker(typography, "UFCORACLEBODY")
        reduced_type = find_typography_marker(typography, "UFCORACLEREDUCED")
    except PDFMeasurementError as exc:
        fail(str(exc))

    width_expected = page_rule["values"]["width_mm"] * PT_PER_MM
    height_expected = page_rule["values"]["height_mm"] * PT_PER_MM
    left_expected = margin_rule["values"]["left_mm"] * PT_PER_MM
    right_expected = page.width - margin_rule["values"]["right_mm"] * PT_PER_MM
    body_font_expected = float(body_font_rule["values"]["pt"])
    reduced_font_expected = float(reduced_font_rule["values"]["pt"])

    checks = [
        assertion(
            "page.width",
            page.width,
            width_expected,
            tolerances["page_size_pt"],
            "pt",
        ),
        assertion(
            "page.height",
            page.height,
            height_expected,
            tolerances["page_size_pt"],
            "pt",
        ),
        assertion(
            "marker.left.x-min",
            left.box.x_min,
            left_expected,
            tolerances["horizontal_position_pt"],
            "pt",
        ),
        assertion(
            "marker.right.x-max",
            right.box.x_max,
            right_expected,
            tolerances["horizontal_position_pt"],
            "pt",
        ),
        minimum_assertion(
            "block.below-page-midpoint",
            block.box.y_min,
            page.height / 2.0,
            tolerances["vertical_position_pt"],
            "pt",
        ),
        assertion(
            "typography.body.font-size",
            body_type.font_size,
            body_font_expected,
            tolerances["font_size_pt"],
            "pt",
        ),
        assertion(
            "typography.reduced.font-size",
            reduced_type.font_size,
            reduced_font_expected,
            tolerances["font_size_pt"],
            "pt",
        ),
    ]

    result = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N5",
        "fixture": "tests/normativa/pdf-oracle-core.tex",
        "pdf": pdf.name,
        "source_commit_sha": args.commit_sha,
        "policy_reviewed_at": policy["reviewed_at"],
        "result": result,
        "page": {
            "index": page.index,
            "width": page.width,
            "height": page.height,
        },
        "markers": {
            "left": left.box.to_dict(),
            "right": right.box.to_dict(),
            "block": block.box.to_dict(),
            "body": body.box.to_dict(),
            "reduced": reduced.box.to_dict(),
        },
        "typography": {
            "body": body_type.to_dict(),
            "reduced": reduced_type.to_dict(),
        },
        "pdfinfo": info,
        "fonts": fonts,
        "assertions": checks,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    failed = [item["id"] for item in checks if item["status"] != "PASS"]
    if failed:
        fail("measurement assertions failed: " + ", ".join(failed))

    print(
        "PDF oracle core passed: "
        f"page={page.width:.2f}x{page.height:.2f}pt, "
        f"left={left.box.x_min:.2f}pt, right={right.box.x_max:.2f}pt, "
        f"block-y={block.box.y_min:.2f}pt, "
        f"font-body={body_type.font_size:.2f}pt, "
        f"font-reduced={reduced_type.font_size:.2f}pt."
    )


if __name__ == "__main__":
    main()
