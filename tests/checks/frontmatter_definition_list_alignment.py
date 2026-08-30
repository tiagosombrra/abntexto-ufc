#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from pdf_measurement import PDFMeasurementError, bbox_pages, find_marker

ALIGNMENT_TOLERANCE_PT = 1.0
COLUMN_TOLERANCE_PT = 1.0
POSITION_TOLERANCE_PT = 1.0
PDF_PT_PER_MM = 72.0 / 25.4
TEXT_MARGIN_LEFT_PT = 30.0 * PDF_PT_PER_MM
DEFINITION_COLUMN_X_PT = 60.0 * PDF_PT_PER_MM


def fail(message: str) -> None:
    raise SystemExit(f"Front matter definition-list alignment failed: {message}")


def locate(pdf: Path, marker: str):
    try:
        return find_marker(bbox_pages(pdf), marker)
    except PDFMeasurementError as exc:
        fail(f"{pdf}: {exc}")


def row_measurement(pdf: Path, label: str, definition_start: str) -> dict[str, float | int | str]:
    label_page, label_word = locate(pdf, label)
    definition_page, definition_word = locate(pdf, definition_start)
    if label_page.index != definition_page.index:
        fail(
            f"{pdf}: row markers {label!r}/{definition_start!r} landed on different pages "
            f"({label_page.index}/{definition_page.index})"
        )

    vertical_delta = abs(label_word.box.y_min - definition_word.box.y_min)
    if vertical_delta > ALIGNMENT_TOLERANCE_PT:
        fail(
            f"{pdf}: row {label!r}/{definition_start!r} is vertically misaligned: "
            f"delta={vertical_delta:.3f}pt > {ALIGNMENT_TOLERANCE_PT:.3f}pt"
        )

    label_left_delta = abs(label_word.box.x_min - TEXT_MARGIN_LEFT_PT)
    if label_left_delta > POSITION_TOLERANCE_PT:
        fail(
            f"{pdf}: label {label!r} is not left-aligned with the text area: "
            f"x={label_word.box.x_min:.3f}pt expected={TEXT_MARGIN_LEFT_PT:.3f}pt "
            f"delta={label_left_delta:.3f}pt > {POSITION_TOLERANCE_PT:.3f}pt"
        )

    definition_x_delta = abs(definition_word.box.x_min - DEFINITION_COLUMN_X_PT)
    if definition_x_delta > POSITION_TOLERANCE_PT:
        fail(
            f"{pdf}: definition {definition_start!r} moved from the 3 cm list offset: "
            f"x={definition_word.box.x_min:.3f}pt expected={DEFINITION_COLUMN_X_PT:.3f}pt "
            f"delta={definition_x_delta:.3f}pt > {POSITION_TOLERANCE_PT:.3f}pt"
        )

    return {
        "page": label_page.index,
        "label": label,
        "definition_start": definition_start,
        "label_x": label_word.box.x_min,
        "definition_x": definition_word.box.x_min,
        "label_y": label_word.box.y_min,
        "definition_y": definition_word.box.y_min,
        "vertical_delta_pt": vertical_delta,
        "label_left_delta_pt": label_left_delta,
        "definition_x_delta_pt": definition_x_delta,
    }


def assert_column_consistency(rows: list[dict[str, float | int | str]], key: str) -> float:
    values = [float(row[key]) for row in rows]
    spread = max(values) - min(values)
    if spread > COLUMN_TOLERANCE_PT:
        fail(
            f"column {key} is inconsistent across rows: "
            f"spread={spread:.3f}pt > {COLUMN_TOLERANCE_PT:.3f}pt"
        )
    return spread


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regression-check two-column alignment in abbreviation and symbol lists."
    )
    parser.add_argument("abbreviations_pdf", type=Path)
    parser.add_argument("symbols_pdf", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    for pdf in (args.abbreviations_pdf, args.symbols_pdf):
        if not pdf.is_file():
            fail(f"PDF not found: {pdf}")

    abbreviation_rows = [
        row_measurement(args.abbreviations_pdf, "ABNT", "Associação"),
        row_measurement(args.abbreviations_pdf, "UFC", "Universidade"),
    ]

    # Mathematical glyph bounding boxes are font-dependent and do not expose
    # the TeX baseline directly. The symbol fixture therefore keeps real math
    # symbols for rendering coverage and adds one textual control row solely
    # to measure the generic label/definition alignment mechanism.
    symbol_rows = [
        row_measurement(args.symbols_pdf, "SYMALIGN", "DEFALIGN"),
    ]
    all_rows = [*abbreviation_rows, *symbol_rows]

    label_spread = assert_column_consistency(all_rows, "label_x")
    definition_spread = assert_column_consistency(all_rows, "definition_x")
    max_vertical_delta = max(float(row["vertical_delta_pt"]) for row in all_rows)
    max_label_left_delta = max(float(row["label_left_delta_pt"]) for row in all_rows)
    max_definition_x_delta = max(float(row["definition_x_delta_pt"]) for row in all_rows)

    payload = {
        "schema_version": 1,
        "component": "frontmatter-definition-list-alignment",
        "result": "PASS",
        "alignment_tolerance_pt": ALIGNMENT_TOLERANCE_PT,
        "column_tolerance_pt": COLUMN_TOLERANCE_PT,
        "position_tolerance_pt": POSITION_TOLERANCE_PT,
        "expected_text_margin_left_pt": TEXT_MARGIN_LEFT_PT,
        "expected_definition_column_x_pt": DEFINITION_COLUMN_X_PT,
        "abbreviation_rows": abbreviation_rows,
        "symbol_rows": symbol_rows,
        "symbol_probe": {
            "kind": "textual-control-row",
            "purpose": "measure generic list-row alignment without math-glyph bbox bias",
            "math_symbols_retained_in_fixture": True,
        },
        "label_x_spread_pt": label_spread,
        "definition_x_spread_pt": definition_spread,
        "max_vertical_delta_pt": max_vertical_delta,
        "max_label_left_delta_pt": max_label_left_delta,
        "max_definition_x_delta_pt": max_definition_x_delta,
        "normative_contract_changed": False,
    }

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(
        "LAYOUT-EVIDENCE frontmatter-definition-lists status=PASS "
        f"rows={len(all_rows)} "
        f"max_vertical_delta_pt={max_vertical_delta:.3f} "
        f"max_label_left_delta_pt={max_label_left_delta:.3f} "
        f"max_definition_x_delta_pt={max_definition_x_delta:.3f} "
        f"label_x_spread_pt={label_spread:.3f} "
        f"definition_x_spread_pt={definition_spread:.3f}"
    )


if __name__ == "__main__":
    main()
